import sys
sys.dont_write_bytecode=True
import json,pathlib,importlib.util,hashlib,collections,subprocess
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
legacy=mod(W/'evidence/legacy-generator.py','legacy')
inv=json.load(open(J/'source/inventory.json'));src=json.load(open(E/'source-analysis.json'));source_ids={x['id'] for x in src['source_cases']}
historical=json.load(open(W/'17592186119847/reference/replenishment/basis-2639/generated.json'));historical={r['question'][':question/id']:r for r in historical}
affected=[];records=[];tests=[]
for q in inv['questions']:
 qid=q[':question/id']
 if qid in source_ids:tests.append({'question_id':qid,'source_original':True});continue
 r=historical[qid];again=legacy.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],r['generation']['seed']);assert r==again
 assert qid==again['question'][':question/id'] and q[':question/problem']==again['question'][':question/problem'] and q[':question/worked-solution']==again['question'][':question/worked-solution']
 sf=q[':question/answer-fields'][0];gf=again['question'][':question/answer-fields'][0]
 assert {(a[':answer/id'],a[':answer/value']) for a in sf[':answer-field/choices']}=={(a[':answer/id'],a[':answer/value']) for a in gf[':answer-field/choices']}
 assert sf[':answer-field/correct'][':answer/id']==gf[':answer-field/correct'][1]
 records.append(again);tests.append({'question_id':qid,'reproduced_complete_record':True,'generation':r['generation']})
 if r['generation']['bank_profile']=='q-79405':
  values=[int(a[':answer/value']) for a in gf[':answer-field/choices']];rank=r['generation']['parameters']['count'];assert sorted(values).index(rank)==1
  affected.append({'question_id':qid,'entity_id':q[':db/id'],'finding':'Historical q-79405 bank makes rank always the second-smallest option. Current v2 changes distractor signs; stored v1 record still has this weakness.','reproduction':f'{sys.executable} -B {E}/finish-tests.py ; legacy.generate("easy", seed={r["generation"]["seed"]})','evidence_path':'generated-records.json'})
save('generated-records.json',records);save('affected-inventory.json',{'affected_questions':affected});save('inventory-tests.json',{'captured_basis':inv['basis'],'records':tests,'limits':['Original source questions excluded from generated claims.','Two non-source records have exact retained historical generation metadata and were replayed.','The new construction restriction is a missing-case defect, not an erroneous stored individual instance.']})
# Native grading for independently chosen source, control, batch and profile cases.
rs=json.load(open(E/'source-replay-records.json'))
rs+=json.load(open(E/'delivery-controls-easy/accepted.json'))+json.load(open(E/'delivery-controls-moderate/accepted.json'))+json.load(open(E/'delivery-runner-batch/accepted.json'))
samples=json.load(open(E/'independent-records.json'));rs+=samples[::20]+samples[1::20]
cases=[]
import re
for r in rs:
 q=r['question'];t=q[':question/problem'];_,m,n,c=re.search(r'\$([A-Z])\$.*?\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$.*?\$(\d+)\$',t).groups();rank=int(n)-int(c) if '**non-pivot**' in t else int(c);f=q[':question/answer-fields'][0]
 cases.append({'label':q[':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==rank else 'rejected','purpose':'Visible-count oracle: one correct and four plausible distractors, real radio UUID response'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases)
render=json.load(open(E/'delivery-controls-easy/accepted.json'))+json.load(open(E/'delivery-controls-moderate/accepted.json'))+json.load(open(E/'delivery-runner-batch/accepted.json'))
save('render-records.json',render)
# Record delivery counts and decision distributions before/after shared normalization.
def summary(rs):
 d={'count':len(rs),'profiles':{},'correct_positions':collections.Counter(),'correct_numeric_orders':collections.Counter(),'ranks':collections.Counter(),'shapes':collections.Counter()}
 for r in rs:
  f=r['question'][':question/answer-fields'][0];a=f[':answer-field/choices'];v=[int(x[':answer/value']) for x in a];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id'];i=next(i for i,x in enumerate(a) if x[':answer/id']==cid);p=r['generation']['parameters'];rank=v[i];d['correct_positions'][i+1]+=1;d['correct_numeric_orders'][sorted(v).index(rank)+1]+=1;d['ranks'][rank]+=1;d['shapes']['square' if p['rows']==p['columns'] else 'tall' if p['rows']>p['columns'] else 'wide']+=1
  prof=r['generation']['bank_profile'];x=d['profiles'].setdefault(prof,{'count':0,'positions':collections.Counter(),'orders':collections.Counter()});x['count']+=1;x['positions'][i+1]+=1;x['orders'][sorted(v).index(rank)+1]+=1
 return d
stage={}
for n in ['easy-records','moderate-records','runner-batch','controls-easy','controls-moderate']:
 stage[n]={'before':summary(json.load(open(E/(n+'.json')))),'after':summary(json.load(open(E/('delivery-'+n)/'accepted.json'))),'filter':json.load(open(E/('delivery-'+n)/'delivery.json'))}
save('delivery-coverage.json',stage)
# Faithful selector reproduction: synthetic future IDs explicitly cannot predict future actual IDs.
pool=[]
for q in inv['questions']:
 f=q.get(':question/answer-fields',[{}])[0]
 if not f.get(':answer-field/correct'):continue
 pool.append((q[':db/id'],q[':question/id'],q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]))
base=max(x[0] for x in pool)+1
fresh=json.load(open(E/'delivery-runner-batch/accepted.json'))
pool+= [(base+i,r['question'][':question/id'],'easy') for i,r in enumerate(fresh)]
def select(pool,weights,seed):
 pool=sorted(set(pool))
 if weights is None:return pool[0] if pool else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 def u(o):return (int.from_bytes(digest[o:o+8],'big')>>11)/2**53
 bands=[[x for x in pool if x[2]==b] for b in ['easy','moderate','hard']];total=sum(w for p,w in zip(bands,weights) if p)
 if total<=0:return None
 draw=u(0)*total;chosen=None
 for p,w in zip(bands,weights):
  if not p or w==0:continue
  chosen=p
  if draw<w:break
  draw-=w
 return chosen[int(u(8)*len(chosen))]
sel=[]
for weights in [None,[1,0,0],[6,3,1]]:
 for seen in [set(),{fresh[0]['question'][':question/id']}]:
  candidates=[x for x in pool if x[1] not in seen];draws=[select(candidates,weights,'review-seed-'+str(i)) for i in range(256)];ct=collections.Counter(x[1] for x in draws if x)
  sel.append({'weights':weights,'seen_excluded':sorted(seen),'draws':256,'selection_counts':ct,'batch_members_reached':sum(r['question'][':question/id'] in ct for r in fresh)})
save('selection-tests.json',{'basis':5404,'source':'engine/rust/question_selection.rs: select, seen_before_task; sorted unique IDs, SHA256 band draw then within-band draw','synthetic_future_ids':True,'candidate_pool':pool,'scenarios':sel,'limits':['Captured inventory has no learner history or active weight policy. These are explicit conditional replays, not assertions about a specific learner.','Fresh future db IDs are unknown; synthetic ordered IDs examine reachability and selection logic only.','No-policy branch selects lowest entity ID; configured weights draw by difficulty and uniformly within a band. No bank-profile or answer-dependent filtering exists in select.']})
print(json.dumps({'inventory_reproduced':len(records),'affected':len(affected),'native_cases':len(cases),'render_records':len(render),'delivery':{k:(v['filter']['input_count'],v['filter']['accepted_count']) for k,v in stage.items()}}))
