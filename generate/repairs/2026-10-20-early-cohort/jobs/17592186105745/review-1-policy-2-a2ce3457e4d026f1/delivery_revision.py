#!/usr/bin/env python3
"""Independent conditional shortcut and post-filter/selection review."""
import sys
sys.dont_write_bytecode=True
import collections,copy,hashlib,json,pathlib,re
import review_tests as t
from delivery_tests import selection
R=t.ROOT
def save(n,v):t.save(n,v)
def strategy_picks(r):
 f=r['question'][':question/answer-fields'][0];bs=f[':answer-field/choices']
 fs=[t.family(c[':answer/value']) for c in bs]
 if all(v is not None for v in fs):
  vals=[v[0].subs(t.y,0) for v in fs];signs=[t.S.sign(t.S.diff(v[0],t.y)) for v in fs]
 else:
  ms=[t.mats(c[':answer/value'])[-1] for c in bs];vals=[m[0,2] for m in ms];signs=[t.S.sign(m[0,1]) for m in ms]
 sizes=[abs(v) for v in vals];counts=collections.Counter(signs)
 old=t.shortcut(r)[0]
 return {'retained modal bank rule':old,'first authored position':[0],'last authored position':[4],
 'largest constant magnitude':[i for i,v in enumerate(sizes) if v==max(sizes)],
 'smallest constant magnitude':[i for i,v in enumerate(sizes) if v==min(sizes)],
 'majority coefficient sign':[i for i,v in enumerate(signs) if counts[v]==max(counts.values())],
 'minority coefficient sign':[i for i,v in enumerate(signs) if counts[v]==min(counts.values())],
 'shortest expression':[i for i,c in enumerate(bs) if len(c[':answer/value'])==min(len(v[':answer/value']) for v in bs)]}
def measure(rs,name):
 cases=[{'question_id':r['question'][':question/id'],'template':r['generation']['template'],'family':t.signature(r)[0],'key_position':t.keypos(r),'column_scale':r['generation']['parameters']['column_scale'],'rhs_scale':r['generation']['parameters']['rhs_scale'],'picks':strategy_picks(r)} for r in rs]
 groups=[]
 for subgroup,sub in [('overall',cases)]+[(sid,[v for v in cases if v['template']==sid]) for sid in sorted({v['template'] for v in cases})]:
  for strategy in cases[0]['picks'] if cases else []:
   hits=sum(v['picks'][strategy]==[v['key_position']] for v in sub)
   # Single, unambiguous selections only; tied set is not an answer-producing rule.
   groups.append({'subgroup':subgroup,'strategy':strategy,'correct':hits,'total':len(sub),'baseline':.2})
 return {'stage':name,'count':len(rs),'template_counts':dict(collections.Counter(v['template'] for v in cases)),'column_scale_counts':dict(collections.Counter(str(v['column_scale']) for v in cases)),'rhs_sign_counts':dict(collections.Counter('negative' if v['rhs_scale']<0 else 'positive' for v in cases)),'key_positions':dict(collections.Counter(str(v['key_position']) for v in cases)),'groups':groups,'cases':cases}
def main():
 names=['sampler-proposals-easy.json','sampler-accepted-easy.json','sampler-proposals-moderate.json','sampler-accepted-moderate.json','delivery-easy-input.json','delivery-easy/accepted.json','delivery-moderate-input.json','delivery-moderate/accepted.json','runner-batch.json','delivery-batch/accepted.json','counterfactual-records.json']
 stages=[measure(json.loads((R/n).read_text()),n) for n in names]
 save('shortcut-results.json',{'strategies':'Only answer values or authored positions; no original matrix/key/metadata enters strategy_picks. A tied candidate set is not treated as a successful single answer. UI ordering tested separately.','baseline':'Uniform five-choice guessing success rate 0.2. Controlled identical banks with all five targets separate mathematical dependency from chance matches in tiny delivered subgroups.','results':stages})
 # Faithful selection() with explicit stand-in entity IDs for new records; captured
 # originals retain their real IDs. Unknown production learner histories are not invented.
 reports=[];selection_records=[]
 inv=json.loads((t.JOB/'source/inventory.json').read_text())
 for name in ['delivery-easy/accepted.json','delivery-moderate/accepted.json','delivery-batch/accepted.json']:
  rs=json.loads((R/name).read_text());mapping={900000+i:r for i,r in enumerate(rs)}
  d=rs[0]['question'][':question/difficulty'].split('/')[-1];weights=[1.,0.,0.] if d=='easy' else [0.,1.,0.]
  cand=[(i,d) for i in mapping];draws=[]
  for i in range(80):
   seed=f'task-{846271+i}/kp-17592186105745/slot-0';entity=selection(cand,seed,weights);r=mapping[entity]
   draws.append({'seed':seed,'entity_id':entity,'question_id':r['question'][':question/id'],'template':r['generation']['template'],'key_position':t.keypos(r),'retained_rule_success':t.shortcut(r)[0]==[t.keypos(r)]})
  fresh=[];seen=set()
  for i in range(len(cand)):
   entity=selection([c for c in cand if c[0] not in seen],f'task-846271/kp-17592186105745/slot-{i}',weights);seen.add(entity);fresh.append(mapping[entity])
  prefix=name.split('/')[0];save('selection-'+prefix+'-records.json',fresh)
  reports.append({'input':name,'pool':'generated survivors only','weights':weights,'draws':draws,'no_repeat_count':len(fresh),'all_survivors_reachable':len(seen)==len(cand),'selected_distribution':measure([mapping[v['entity_id']] for v in draws],name+' 80 selections')})
  # Inventory plus proposed new batch is the applicable learner pool after capture.
  if name=='delivery-batch/accepted.json':
   originals=[(q[':db/id'],q[':question/difficulty'][':db/ident'].split('/')[-1]) for q in inv['questions']]
   lookup={q[':db/id']:q for q in inv['questions']};union=cand+originals;draws2=[]
   for i in range(80):
    seed=f'task-{846271+i}/kp-17592186105745/slot-0';entity=selection(union,seed,weights)
    draws2.append({'seed':seed,'entity_id':entity,'question_id':mapping[entity]['question'][':question/id'] if entity in mapping else lookup[entity][':question/id'],'is_new_generated':entity in mapping})
   reports.append({'input':name,'pool':'captured inventory plus proposed new batch','weights':weights,'candidate_counts':{'original_easy':sum(d=='easy' for i,d in originals),'original_moderate':sum(d=='moderate' for i,d in originals),'new_easy':len(cand)},'draws':draws2,'new_generated_selected':sum(v['is_new_generated'] for v in draws2)})
 save('selection-results.json',{'algorithm':'engine/rust/question_selection.rs select lines 125-197: sort/dedup entity IDs; difficulty-weight band draw and SHA256 within-band draw. learning.rs 598-622 filters seen and invalid records first.','cases':reports,'limitations':['Captured basis 5363. New IDs are explicit stand-ins; no production publication or database write was performed.','No active policy/learner history supplied. Positive easy-only/moderate-only policies and full no-repeat histories tested read-only; other valid weights only change band frequency, not bank construction.','Unconfigured policy selects smallest entity ID; this can prefer a generated stand-in or original depending on actual IDs. It does not transform item-local decisions.','Original bank has historical captured source cues. Those originals are not generated affected instances. No claim that this revision repairs original authored questions.']})
 # Actual normalized delivery records also receive native checks in one batch.
 cases=[]
 for name in ['delivery-easy/accepted.json','delivery-moderate/accepted.json','delivery-batch/accepted.json']:
  for i,r in enumerate(json.loads((R/name).read_text())):
   z=t.math_record(r);f=r['question'][':question/answer-fields'][0]
   cases.append({'label':name+'-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if z['valid_choices'][j] else 'rejected','purpose':'Post-delivery normalization; independent exact option classification.'} for j,c in enumerate(f[':answer-field/choices'])]})
 save('delivered-grader-input.json',cases)
 # Saturation bound tested cheaply by holding the generator output fixed; the real
 # random runs above demonstrate actual duplicate rejections.
 g=t.load_generator(t.PKG/'17592186105745.py');one=g.generate('easy',846271);calls=[]
 def fixed(*a,**k):calls.append(1);return copy.deepcopy(one)
 g.generate=fixed
 try:g.batch('easy',2,846271);error=None
 except Exception as e:error=str(e)
 save('resampling-boundary.json',{'test':'Force every proposal to the same valid fingerprint; request 2 distinct items.','proposal_calls':len(calls),'error':error,'bounded_rejection':len(calls)==2000 and error is not None})
 print(json.dumps({'batch_probes':[{k:v for k,v in z.items()} for z in stages[-3]['groups'] if z['subgroup']=='overall'],'delivery_counts':[(s['stage'],s['count']) for s in stages[4:10]],'native_delivered_cases':len(cases),'selection_pools':len(reports)}))
 (R/'session-state.md').write_text('Source, exact math, source/preflight regressions, native grading (905 checks), packaging and captured inventory complete. Read-only delivery retained 78 easy controls, 74 moderate controls and all 5 exact runner items; conditional bank probes and learner selection reproduction saved. Renderer first 6 complete; remaining 15 and final visual/contract review pending.\n')
if __name__=='__main__':main()
