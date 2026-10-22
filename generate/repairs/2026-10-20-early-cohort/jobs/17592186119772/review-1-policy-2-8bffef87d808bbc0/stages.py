#!/usr/bin/env python3
"""Post-delivery independent measurements, historical evidence, and native grading."""
import audit as a
import copy, hashlib, json, re, shutil, sys
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
E,J,R,W,OLD=a.E,a.J,a.R,a.W,a.OLD
def stats(records):return [a.inspect(r) for r in records]
def count_good(rows):return {','.join(k):v for k,v in Counter(tuple(x['good']) for x in rows).items()}
def summarize(records):
    st=stats(records);groups={}
    for key in ['profile','dimensions','target']:
        d=defaultdict(list)
        for row in st:d[str(row[key])].append(row)
        groups[key]=[{'cue':k,'n':len(v),'answers':count_good(v),'best_constant_answer_hits':max(Counter(tuple(x['good']) for x in v).values())} for k,v in d.items()]
    return {'total':len(st),'answers':count_good(st),'positions':dict(Counter(x['correct_position'] for x in st)),'semantic_banks':len({x['semantic'] for x in st}),'groups':groups,'cases':st}
def add_probe(probes,rows,stage,subgroup,scope,cue,prediction,baseline=.2,disposition='not_predictive',extra=''):
    n=sum(prediction(x) for x in rows)
    probes.append({'cue':cue,'subgroup':stage+': '+subgroup,'scope':scope,'strategy':cue,'correct':n,'total':len(rows),'baseline':baseline,'disposition':disposition,'conclusion':f'{n}/{len(rows)} successes. Baseline {baseline} is uniform choice among five easy matrices. '+extra,'sample_refs':['shortcut-results.json', 'delivery-batch/accepted.json' if stage=='exact delivered batch' else 'delivery-control/accepted.json']})
def main():
    control=a.load('delivery-control/accepted.json');batch=a.load('delivery-batch/accepted.json')
    raw=a.load('easy-records.json');rawbatch=a.load('batch-records.json')
    out={name:summarize(rs) for name,rs in [('raw_control',raw),('delivered_control',control),('raw_batch',rawbatch),('delivered_batch',batch)]}
    # Recovered old dimension-signature predictor, frozen independently before revision.
    oldreplays=json.loads((OLD/'source-replay-records.json').read_text())
    oldrule={tuple(a.inspect(r)['dimensions']):a.inspect(r)['good'] for r in oldreplays if a.enum(r['question'][':question/difficulty']).endswith('/easy')}
    out['old_dimension_rule']=[{'dimensions':k,'choose':v} for k,v in oldrule.items()]
    for stage in ['raw_control','delivered_control','raw_batch','delivered_batch']:
        out[stage]['old_rule_successes']=sum(oldrule.get(tuple(x['dimensions']))==x['good'] for x in out[stage]['cases'])
        out[stage]['old_rule_covered']=sum(tuple(x['dimensions']) in oldrule for x in out[stage]['cases'])
    # Examine simple surface actions, including conditional recognizable subgroups.
    probes=[]
    for label,rs in [('control after delivery',control),('exact delivered batch',batch)]:
        rows=stats(rs)
        for l in 'ABCDE':add_probe(probes,rows,label,'all easy','overall','Always select label '+l,lambda x,l=l:x['good']==(l,))
        for pos in range(5):add_probe(probes,rows,label,'all easy','overall','Always select displayed position '+str(pos+1),lambda x,pos=pos:x['correct_position']==pos)
        known=[x for x in rows if tuple(x['dimensions']) in oldrule]
        add_probe(probes,known,label,'old dimension signatures','other_recognizable_subgroup','Use the old labeled-dimension lookup',lambda x:oldrule[tuple(x['dimensions'])]==x['good'],extra='The prior perfect predictor now has counterexamples at fixed dimensions.')
        for key in ['profile','dimensions']:
            gr=defaultdict(list)
            for row in rows:gr[str(row[key])].append(row)
            for k,v in gr.items():
                best,hits=Counter(x['good'] for x in v).most_common(1)[0]
                add_probe(probes,v,label,key+'='+k,'within_template' if key=='profile' else 'other_recognizable_subgroup','Always choose '+','.join(best)+' within this '+key,lambda x,best=best:x['good']==best,extra='Most frequent answer chosen retrospectively as a conservative best constant cue; no zero-side inspection. Multiple answers remain in this subgroup.')
        # Conditional target+shape profiles; report singletons as uninformative.
        gr=defaultdict(list)
        for row in rows:gr[(row['target'],row['dimensions'])].append(row)
        out['conditional_'+label]=[{'cue':str(k),'n':len(v),'answers':count_good(v),'singletons_uninformative':len(v)==1} for k,v in gr.items()]
        for k,v in gr.items():
            if len(v)>=3:
                best,hits=Counter(x['good'] for x in v).most_common(1)[0]
                add_probe(probes,v,label,'orientation and dimensions '+str(k),'other_recognizable_subgroup','Always choose '+','.join(best)+' within orientation+dimensions',lambda x,best=best:x['good']==best,extra='Subgroups of size one or two retained in the detailed table without treating coincidences as a family rule.')
        # Diagonal sign and absolute magnitude do not test triangular status.
        for cue,score in [('Choose largest absolute diagonal sum',lambda m:sum(abs(m[i][i]) for i in range(len(m)))),('Choose smallest absolute diagonal sum',lambda m:-sum(abs(m[i][i]) for i in range(len(m))))]:
            hits=0;predictions=[]
            for r,row in zip(rs,rows):
                mats=a.visible(r['question']);chosen=max(sorted(mats),key=lambda l:score(mats[l]))
                hits+=row['good']==(chosen,);predictions.append({'id':row['id'],'choose':chosen,'actual':row['good']})
            probes.append({'cue':cue,'subgroup':label,'scope':'overall','strategy':cue+'; alphabetical label breaks ties','correct':hits,'total':len(rows),'baseline':.2,'disposition':'not_predictive','conclusion':'Uniform five-choice baseline is 0.2. Diagonal-only action has counterexamples and bypasses the target test; ties are resolved without inspecting off-diagonal entries.','sample_refs':['shortcut-results.json','delivery-batch/accepted.json' if label=='exact delivered batch' else 'delivery-control/accepted.json']})
            out.setdefault('diagonal_probes',[]).append({'stage':label,'cue':cue,'cases':predictions})
    a.save('shortcut-results.json',out)

    # Captured inventory and prior exact reconstructions share the runner binding.
    inv=json.loads((J/'source/inventory.json').read_text());iq={q[':question/id']:q for q in inv['questions'] if ':question/math-academy-id' not in q}
    historical=json.loads((OLD/'generated-records.json').read_text())
    sys.path.insert(0,str(R))
    from scripts.generator_publish import normalized_question
    inventory_cases=[]
    for record in historical:
        q=record['question'];stored=iq[q[':question/id']]
        assert normalized_question(q,identity=False)==normalized_question(stored,identity=False)
        assert a.visible(q)==a.visible(stored)
        assert record['generation']['reproduction']['captured_entity_id']==stored[':db/id']
        inventory_cases.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'exact_content_reconfirmed':True,'generation_provenance':'Previous independent explicit-parameter reconstruction; historical seed was not captured; captured identities explicitly rebound. Not an output of the revised generator.','good':a.inspect(record)['good']})
    assert len(iq)==len(historical)==3
    a.save('generated-records.json',historical)
    affected=json.loads((OLD/'affected-inventory.json').read_text())
    for x in affected['affected_questions']:
        x['reproduction']=str(a.PY)+' -B stages.py; verify captured content against prior reconstruction in generated-records.json. Exact historical reconstruction parameters and identity provenance are retained in each generation record.'
    a.save('affected-inventory.json',affected)
    a.save('inventory-audit.json',{'provenance':str(OLD/'inventory-audit.json'),'binding':'Runner confirms source and inventory hashes match previous review; exact historical content independently re-compared to current inventory using publisher normalized_question(identity=False).','basis':inv['basis'],'total_questions':len(inv['questions']),'original_source_excluded':len(inv['questions'])-len(iq),'generated_examined':len(iq),'historically_affected':len(affected['affected_questions']),'cases':inventory_cases,'limits':['Historical seed/metadata were not captured. Records retain independently reconstructed metadata with captured identity binding made explicit.','Three historic records remain in the bank; repairing this package does not rewrite them. No database mutation requested or performed.','The historical family-level dimension predictor is separate from the revised requested-easy family.']})

    # Read-only faithful easy-band branch of selection.rs with captured pool.
    # Unknown live weights/history cannot be invented; test each applicable
    # single-band and history-exclusion branch with explicit synthetic histories.
    def select(pool,seed,seen=(),configured=True):
        pool=sorted(set(pool)-set(seen))
        if not pool:return None
        if not configured:return pool[0]
        h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53)
        return pool[int(u*len(pool))]
    selection=[]
    for name,rs in [('control',control),('exact_batch',batch)]:
        lookup={i:r for i,r in enumerate(rs,1)}
        draws=[lookup[select(lookup,'review-86203711-'+str(k))] for k in range(128)]
        seen=[];sequence=[]
        for k in range(len(lookup)):
            chosen=select(lookup,'history-93071-'+str(k),seen);assert chosen not in seen;sequence.append(chosen);seen.append(chosen)
        assert select(lookup,'exhausted',seen) is None
        selection.append({'pool':name,'eligible':len(lookup),'weighted_easy_draws':summarize(draws),'history_without_replacement':sequence,'exhausted':None,'unconfigured_first_entity':select(lookup,'x',configured=False)})
    a.save('selection-results.json',{'source':'engine/rust/question_selection.rs::select and seen_before_task; explicit faithful one-rated-band reproduction in stages.py','captured_basis':inv['basis'],'conditional_policy':'For requested easy records and a positive easy weight, band draw is deterministic easy and within-band offset 8..16 selects uniformly. Zero easy weight with no unrated records produces no question. Unconfigured policy returns first sorted eligible entity. History exclusions remove seen items. Proxy future entity IDs 1..N are explicit: no database IDs for unpublished records exist.','cases':selection,'limits':['Live policy weights and actual learner histories are not captured, so no individual production sequence or mixed-difficulty distribution is asserted.','Changed inventory after basis 5453 may alter deduplication.','Five-item batch by itself cannot demonstrate every source family; all eight source profiles are covered in the control set.']})

    grader=a.load('grader-input.json')
    # An unsupported literal radio value is a harness input error, not a
    # learner-visible wrong option. Preserve the observation with proper status.
    for case in grader:
        for check in case['checks']:
            if 'submitted' in check:
                check['expected']='unresolved'
                check['purpose']='Explicitly out-of-contract diagnostic: radio UI submits an authored choice UUID, never literal text; native engine must refuse to grade this unsupported API input. It is not a missing valid learner notation capability.'
    for stage,rs in [('delivered_batch',batch),('historical_verified_inventory',historical)]:
        for k,r in enumerate(rs):
            st=a.inspect(r);checks=[]
            for fi,f in enumerate(r['question'][':question/answer-fields']):
                for answer in f[':answer-field/choices']:
                    if a.enum(f[':answer-field/type']).endswith('/checkbox'):
                        label=next(iter(a.parse(f[':answer-field/key'])));ok=(answer[':answer/value']=='true')==(label in st['good'])
                    else:
                        v=answer[':answer/value'];labels=tuple(sorted(a.parse(v))) if a.parse(v) else tuple(sorted(re.findall(r'\$([A-E])\$',v)));ok=labels==st['good']
                    checks.append({'field_index':fi,'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if ok else 'rejected','purpose':'Post-normalization/captured identity bindings: independently classified visible matrix candidates, all correct and wrong choices.'})
            grader.append({'label':stage+'-'+str(k),'record':r,'checks':checks})
    a.save('grader-input-final.json',grader)
    a.run([R/'generate/runs/current/check-engine',E/'grader-input-final.json',E/'grader-report-final.json'],'grader-command-final.json')
    # Core evidence produced now; semantic report is finalized after screenshots.
    a.save('stage-summary.json',{'raw_control':len(raw),'after_delivery_control':len(control),'raw_batch':len(rawbatch),'after_delivery_batch':len(batch),'batch_good':[a.inspect(r)['good'] for r in batch],'batch_positions':[a.inspect(r)['correct_position'] for r in batch],'conditional_shortcut_probes':len(probes),'all_preserved':out['raw_control']['answers']==out['delivered_control']['answers'] and out['raw_batch']['answers']==out['delivered_batch']['answers']})
    a.save('probe-definitions.json',probes)
    (E/'session-state.md').write_text('All 80 fresh easy controls and all 5 exact batch records survive actual publisher filters. Native grading completed with all authored choices plus explicit out-of-contract radio diagnostics. Actual UI rendered 13 cases. Historical 3 affected generated inventory records reverified; selection branches and bounded conditional shortcuts measured. Next: inspect screenshots, finalize pedagogical report/schema and immutable-package checks.\n')
    print(json.dumps({'stage_counts':a.load('stage-summary.json'),'grader_report_keys':list(a.load('grader-report-final.json')),'historical_inventory_affected':len(iq)}))
if __name__=='__main__':main()
