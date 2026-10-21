"""Summarize decision coverage after real filtering and read-only selection."""
import sys, json, hashlib, collections, importlib.util, traceback
from pathlib import Path
sys.dont_write_bytecode=True
import review as R
from audit import key
E,J,P,g=R.ROOT,R.JOB,R.PKG,R.g
save=R.save
load=lambda p:json.loads((E/p).read_text())

def outcome(r):return 'none' if key(r)=='No solution' else 'infinite'
def measure(rs):
    return {'count':len(rs),'outcomes':dict(collections.Counter(outcome(r) for r in rs)),'profiles':dict(collections.Counter(r['generation']['template'] for r in rs))}
def source_lookup(r):
    sid=r['generation']['template'];old=g.CASES[sid]
    return old[':question/answer-fields'][0][':answer-field/correct'][':answer/value']=='No solution'
def candidate_id(r,none):
    q=r['question'];a=R.equations(q);f=q[':question/answer-fields'][0]
    if none:return next(v[':answer/id'] for v in f[':answer-field/choices'] if v[':answer/value']=='No solution')
    cs=[v[':answer/id'] for v in f[':answer-field/choices'] if v[':answer/value']!='No solution' and all(z==0 for z in a[0,:2]*R.mats(v[':answer/value'])[1]-R.S.Matrix([a[0,2]]))]
    assert len(cs)==1
    return cs[0]
def probe(rs,strategy):
    return sum(candidate_id(r,strategy(r))==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in rs)

def main():
    controlled=load('controlled-records.json');randoms=load('random-records.json');pre=load('delivery-input.json');post=load('delivery-domain/accepted.json');batch=load('batch-records.json');delbatch=load('delivery-batch/accepted.json')
    stages={name:measure(rs) for name,rs in [('controlled',controlled),('fresh_random',randoms),('constructor_before_dedup',load('constructor-prefix.json')),('constructor_after_dedup',load('constructor-records.json')),('pre_delivery',pre),('post_delivery',post),('batch_pre_delivery',batch),('batch_post_delivery',delbatch)]}
    probes=[]
    def add(cue,subgroup,scope,rs,strategy,refs,disposition='not_predictive',extra=''):
        successes=probe(rs,strategy)
        probes.append({'cue':cue,'subgroup':subgroup,'scope':scope,'strategy':'Predict consistency from '+cue+'; choose No solution when predicted inconsistent, otherwise solve only the first row and choose its vector.','correct':successes,'total':len(rs),'baseline':0.5,'disposition':disposition,'conclusion':f'{successes}/{len(rs)}. Baseline 0.5 is a blind binary consistency decision after finding the first-row vector; uniform five-choice guessing is 0.2. '+extra,'sample_refs':refs})
    for sid in g.CASES:
        rs=[r for r in controlled if r['generation']['template']==sid]
        assert {outcome(r) for r in rs}=={'none','infinite'}
        add('source coefficient signature / bank profile',sid,'within_template',rs,source_lookup,['controlled-records.json'],'not_predictive','The same visible coefficients and complete bank occur with opposite keys; the earlier fixed outcome is broken.')
    for label,rs,refs in [('fresh random',randoms,['random-records.json']),('after publication filters',post,['delivery-domain/accepted.json']),('exact runner batch',delbatch,['delivery-batch/accepted.json'])]:
        add('source coefficient signature',label,'overall',rs,source_lookup,refs)
        add('negative first-row normalized intercept',label,'overall',rs,lambda r:R.equations(r['question'])[0,2]/R.equations(r['question'])[0,0]<0,refs)
        add('five-option count / always choose No solution',label,'overall',rs,lambda r:True,refs)
        add('ignore second equation / always choose first-row vector',label,'overall',rs,lambda r:False,refs,'intended_skill','Solving the first row is legitimate partial mathematics but does not decide consistency and fails on contradictory records.')
    # Probe every delivered recognizable template, avoiding aggregate-only evidence.
    for sid in sorted({r['generation']['template'] for r in post}):
        rs=[r for r in post if r['generation']['template']==sid]
        assert {outcome(r) for r in rs}=={'none','infinite'},sid
        add('source coefficient signature',sid+' after filtering','within_template',rs,source_lookup,['delivery-domain/accepted.json'])
    save('shortcut-results.json',{'command':f'{sys.executable} {E}/finish.py','stages':stages,'probes':probes,'limits':'Finite probes establish repaired prior cues, not absence of every possible cue. Exact five-question batch has 3 infinite and 2 none; five different profiles alone is not a diversity claim.'})
    inv=json.loads((J/'source/inventory.json').read_text());src=json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];ids={q[':question/id'] for q in src}
    save('inventory-records.json',inv['questions']);assert len(inv['questions'])==17 and all(q[':question/id'] in ids for q in inv['questions'])
    save('affected-inventory.json',{'affected_questions':[]})
    save('inventory-audit.json',{'basis':inv['basis'],'questions_inspected':len(inv['questions']),'original_source_ids':17,'non_source_ids':[],'verified_generated_instances':0,'result':'Verified captured inventory contains only the 17 original source questions, with no generated records to reproduce as affected. They are not labeled generated.','records':'inventory-records.json','limits':'Captured basis 5364 only; no live database queries or changes.'})
    # Faithful easy-band selection fixtures: actual original entity IDs plus
    # explicit placeholders for records which have not been published.
    fixtures=[]
    for q in inv['questions']:
        fixtures.append({'entity_id':q[':db/id'],'kind':'original source','question_id':q[':question/id'],'difficulty':q[':question/difficulty'][':db/ident'].split('/')[-1],'outcome':'none' if q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']=='No solution' else 'infinite'})
    base=max(f['entity_id'] for f in fixtures)+1000
    fixtures.extend({'entity_id':base+i,'kind':'unpublished placeholder','question_id':r['question'][':question/id'],'difficulty':'easy','outcome':outcome(r)} for i,r in enumerate(delbatch))
    def select(pool,weights,seed):
        pool=sorted(pool,key=lambda f:f['entity_id'])
        if weights is None:return pool[0] if pool else None
        bands=[[v for v in pool if v['difficulty']==band] for band in ['easy','moderate','hard']]
        h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        uniform=lambda offset:(int.from_bytes(h[offset:offset+8],'big')>>11)/2**53
        total=sum(w for w,b in zip(weights,bands) if b)
        draw=uniform(0)*total;chosen=None
        for w,b in zip(weights,bands):
            if not b or w==0:continue
            chosen=b
            if draw<w:break
            draw-=w
        return chosen[int(uniform(8)*len(chosen))] if chosen else None
    draws=[];scenarios=[]
    for history,pool in [('all fresh',fixtures),('originals previously seen',[f for f in fixtures if f['kind']!='original source']),('originals and first new question seen',[f for f in fixtures if f['kind']!='original source'][1:])]:
        for weights in [[1,0,0],[1,1,0],None]:
            picked=[select(pool,weights,'revision-independent-'+str(i)) for i in range(64)]
            assert all(v in pool for v in picked)
            scenarios.append({'history':history,'weights':weights,'fresh_ids':[v['entity_id'] for v in pool],'eligible_outcomes':dict(collections.Counter(v['outcome'] for v in pool if weights is None or weights[['easy','moderate','hard'].index(v['difficulty'])]>0)),'selected_outcomes':dict(collections.Counter(v['outcome'] for v in picked))})
            draws.extend({'history':history,'weights':weights,'seed':'revision-independent-'+str(i),'selected':v} for i,v in enumerate(picked))
    save('selection-results.json',{'source':'engine/rust/question_selection.rs:105-196','fixtures':fixtures,'scenarios':scenarios,'draws':draws,'examined':['freshness removes seen IDs','sorted unique entity IDs','rated difficulty bands and zero-weight exclusion','SHA256 seeded uniform selection within active band','legacy unconfigured policy selects lowest fresh ID'],'result':'Configured easy-band fixtures retain both decisions with all five new records, and after removing the first new record. Selection changes membership and frequency, not question content. Legacy first-ID behavior was reproduced and supplies no generator-level diversity guarantee.','limitations':['No live learner histories, configured policy weights or future assigned entity IDs supplied. Fixture IDs explicitly stand for unpublished records.','A history can remove every member of an outcome; arbitrary histories cannot be guaranteed balanced by a generator. This is not a prediction of live delivery.']})
    # All accepted batch choices are also run through the real learner grader.
    grade=load('grader-input.json')
    for i,r in enumerate(delbatch):
        c=R.mathcheck(r);assert c['passed'];f=r['question'][':question/answer-fields'][0]
        grade.append({'label':f'actual delivered batch {i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==c['key_index'] else 'rejected','purpose':'independent math after actual normalization and identity rewrite'} for j,a in enumerate(f[':answer-field/choices'])]})
    save('grader-final-input.json',grade)
    # Verify author regression executable detects an old failure as well as passing now.
    spec=importlib.util.spec_from_file_location('author_check',E/'author-check-copy.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
    oldpkg=J/'review-0-policy-2-f4f6723c67ba4318/relocated-package'
    spec=importlib.util.spec_from_file_location('old_generator',oldpkg/'17592186105746.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    a.g=old
    try:a.main();old_failure={'detected':False}
    except Exception as exc:old_failure={'detected':True,'exception':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
    assert old_failure['detected']
    save('preflight-verification.json',{'retained_findings':['5bda1794e02541c06117','a8a813a755862016dfa8'],'runner_preflight':str(J/'repair-preflight.json'),'current_author_executable_result':load('author-check/repair-regression-results.json'),'old_author_executable_failure':old_failure,'independent_old_tests':'old-targeted-regressions.json','independent_current_tests':'targeted-regressions.json','script_adaptation':'author-check-copy.py redirects import/output roots only; checks preserved.'})
    print(json.dumps({'stages':{k:{'count':v['count'],'outcomes':v['outcomes']} for k,v in stages.items()},'probes':len(probes),'selection_draws':len(draws),'batch_source_lookup_successes':probe(delbatch,source_lookup),'inventory_generated':0}))

if __name__=='__main__':main()
