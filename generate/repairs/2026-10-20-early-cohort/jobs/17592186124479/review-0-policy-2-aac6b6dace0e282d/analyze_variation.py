"""Reproduce the finite-batch shortcut and inspect read-only selection stages."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,pathlib,re
from collections import Counter,defaultdict
import audit

R=audit.ROOT
def facts(record):
    a=audit.matrices(record['question'][':question/problem'])[0]
    choices=audit.field(record)[':answer-field/choices']
    return {'question_id':record['question'][':question/id'],'template':record.get('generation',{}).get('template','stored'),
            'seed':record.get('generation',{}).get('seed'), 'rows':a.rows,'cols':a.cols,
            'nonzero_rows':sum(any(a.row(i)) for i in range(a.rows)),
            'nonzero_cols':sum(any(a.col(i)) for i in range(a.cols)),
            'name':re.search(r'\$([A-Z])',record['question'][':question/problem'])[1],
            'rank':int(a.rank()),'answer':audit.answer(record),
            'bank':sorted(int(c[':answer/value']) for c in choices),
            'raw_first':int(choices[0][':answer/value'])}

def summarize(records):
    fs=[facts(r) for r in records]
    return {'total':len(fs),'ranks':dict(Counter(x['rank'] for x in fs)),
            'coranks':dict(Counter(x['rows']-x['rank'] for x in fs)),
            'row_count_minus_one_successes':sum(x['rank']==x['rows']-1 for x in fs),
            'cases':fs}

def selection(candidates,seed,distribution=(1,1,1)):
    # Transcription of engine/rust/question_selection.rs::select:
    # all supplied candidates are rated moderate, so band draw selects moderate.
    ids=sorted(set(candidates));digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    uniform=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
    return ids[int(uniform*len(ids))] if ids and distribution[1]>0 else None

def main():
    batch=audit.read(R/'batch.json');normal=audit.read(R/'samples.json')
    delivered=audit.read(R/'delivery-batch/accepted.json');normal_del=audit.read(R/'delivery-samples/accepted.json')
    inv=audit.read(audit.JOB/'source/inventory.json')
    stored=[{'question':q} for q in inv['questions']]
    audit.save('inventory-records.json',stored)
    stage={'command':f'{audit.PY} {R}/analyze_variation.py','inventory_basis':inv['basis'],
       'rejection_resampling':{'normal_attempts':204,'exceptions':0,'CLI':'rank chosen first; no retry on invalid generate; CLI loops offsets for mathematical fingerprint dedup only. No statistical conditioning observed in 204 independently selected attempts.'},
       'batch_input':summarize(batch),'batch_accepted':summarize(delivered),
       'control_input':summarize(normal),'control_accepted':summarize(normal_del),
       'inventory_all':summarize(stored),'inventory_generated':summarize([r for r in stored if not r['question'].get(':question/math-academy-id')])}
    byid={q[':db/id']:{'question':q} for q in inv['questions']}
    # Publication has not assigned entity IDs: explicitly model hypothetical fresh IDs.
    newids={90000000000000+i:r for i,r in enumerate(delivered)}
    pool=byid|newids
    draws=[]
    for scenario,candidates in [('fresh combined bank',list(pool)),('only proposed batch fresh',list(newids)),('last two proposed batch fresh',list(newids)[-2:])]:
        chosen=[selection(candidates,'independent-review-619/'+str(i)) for i in range(64)]
        fs=[facts(pool[i]) for i in chosen if i is not None]
        draws.append({'scenario':scenario,'candidate_count':len(candidates),'seeds':'independent-review-619/0..63',
          'chosen_entity_ids':chosen,'row_count_minus_one_successes':sum(f['rank']==f['rows']-1 for f in fs),'total':len(fs),
          'exact_candidate_success_fraction':sum(facts(pool[i])['rank']==facts(pool[i])['rows']-1 for i in candidates)/len(candidates)})
    stage['learner_selection']={'implementation':'faithful database-free transcription of SHA256 draw and sorted unique candidates in question_selection.rs::select; all candidates moderate',
        'weights':'Any positive moderate weight yields uniform selection within the eligible moderate pool; zero moderate weight with no unrated entries yields no question. Unconfigured policy deterministically returns lowest entity ID.',
        'history':'seen_before_task removes earlier tasks; caller also excludes current prefix. Exhausted inventories can leave any proper subset of this batch, preserving its shortcut.',
        'hypothetical_new_ids':list(newids),'draws':draws,
        'limits':'Actual learner histories, active policy and future database IDs are not captured. These are explicit scenarios, not claims about a live learner.'}
    audit.save('stage-analysis.json',stage)
    probes=[]
    def probe(rs,cue,subgroup,scope,strategy,fn,ref,defect=False,intended=False):
        fs=[facts(r) for r in rs];n=len(fs);good=sum(fn(f)==f['rank'] for f in fs)
        probes.append({'cue':cue,'subgroup':subgroup,'scope':scope,'strategy':strategy,'correct':good,'total':n,'baseline':0.2,
           'disposition':'defect' if defect else 'intended_skill' if intended else 'not_predictive',
           'conclusion':f'{good}/{n} successes versus uniform random choice among five options (0.2). '+('Perfect across the exact proposed finite pool; shape alone substitutes for elimination. This is a batch-selection failure, not a universal generator predictor.' if defect else 'This strategy is not universally correct in this tested subgroup; finite testing does not prove all cues harmless.'),
           'sample_refs':[ref]})
    probe(delivered,'matrix row count','exact delivered batch','overall','select row count minus one',lambda f:f['rows']-1,'delivery-batch/accepted.json',True)
    for m in [3,4,5]:
        group=[r for r in delivered if facts(r)['rows']==m]
        probe(group,'matrix shape',f'exact delivered batch: {m} rows','other_recognizable_subgroup','select row count minus one',lambda f:f['rows']-1,'delivery-batch/accepted.json',True)
    probe(normal_del,'matrix row count','independent normal control','overall','select row count minus one',lambda f:f['rows']-1,'delivery-samples/accepted.json')
    for template in dict.fromkeys(r['generation']['template'] for r in normal_del):
        group=[r for r in normal_del if r['generation']['template']==template]
        probe(group,'template/shape signature',template,'within_template','select row count minus one',lambda f:f['rows']-1,'delivery-samples/accepted.json')
    for name in 'ABCDPQ':
        group=[r for r in normal_del if facts(r)['name']==name]
        probe(group,'matrix label',f'label {name}','other_recognizable_subgroup','always select 3',lambda f:3,'delivery-samples/accepted.json')
    for label,fn in [('maximum bank value',lambda f:max(f['bank'])),('minimum bank value',lambda f:min(f['bank'])),('raw first option',lambda f:f['raw_first']),('count nonzero rows',lambda f:f['nonzero_rows']),('min(nonzero rows, nonzero columns)',lambda f:min(f['nonzero_rows'],f['nonzero_cols']))]:
        probe(normal_del,label,'independent normal control','overall',label,fn,'delivery-samples/accepted.json')
    probe(stored,'matrix row count','captured full stored bank','overall','select row count minus one',lambda f:f['rows']-1,'inventory-records.json')
    audit.save('shortcut-probes.json',probes)
    # The finding is a defect of this exact finite batch; complying singleton records
    # in a diverse existing pool are not individually defective instances.
    audit.save('affected-inventory.json',{'affected_questions':[]})
    audit.save('inventory-assessment.json',{'basis':inv['basis'],'tested_records':len(stored),'tested_original_source_records':17,'tested_non_source_records':5,
        'finding':'No captured stored pool-wide row-count-minus-one predictor: '+str(stage['inventory_all']['row_count_minus_one_successes'])+'/22 all stored; '+str(stage['inventory_generated']['row_count_minus_one_successes'])+'/5 non-source.',
        'affected_questions_empty_reason':'Demonstrated failure concerns the newly supplied batch as a finite practice pool, whose five IDs are absent from inventory. Existing items that happen to have corank one are not individually defective. All captured records were tested for this specific predicate; this is not an assertion of no other inventory defects.',
        'generation_metadata_limit':'Captured inventory has no generation metadata; none invented or source questions relabeled. No affected record claimed, so no fabricated generated reproduction is supplied.'})
    # Strict runnable acceptance test, intentionally fails on current batch.
    audit.save('batch-shortcut-results.json',{'command':f'{audit.PY} {R}/check_batch_shortcut.py --input {R}/delivery-batch/accepted.json',
        'expected':'At least one independently valid delivered counterexample to row-count-minus-one',
        'actual':stage['batch_accepted'],'passed':not all(facts(r)['rank']==facts(r)['rows']-1 for r in delivered)})
    print(json.dumps({'batch_shortcut':str(stage['batch_accepted']['row_count_minus_one_successes'])+'/5',
                     'control_shortcut':str(stage['control_accepted']['row_count_minus_one_successes'])+'/204',
                     'inventory_shortcut':str(stage['inventory_all']['row_count_minus_one_successes'])+'/22',
                     'inventory_generated_shortcut':str(stage['inventory_generated']['row_count_minus_one_successes'])+'/5'}))

if __name__=='__main__':main()
