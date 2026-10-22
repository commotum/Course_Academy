"""Read-only conditional coverage and concrete batch shortcut reproduction.
Run: /home/jake/Developer/Course_Academy/.venv/bin/python -B audit_delivery.py
Then: /home/jake/Developer/Course_Academy/generate/runs/current/check-engine shortcut-grader-input.json shortcut-grader-results.json
"""
from pathlib import Path
import json,re,collections,hashlib
from fractions import Fraction
E=Path(__file__).resolve().parent;J=E.parent
load=lambda p:json.loads(Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def matrices(q):
 texts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):texts += [f[':answer-field/key']]+[a[':answer/value'] for a in f[':answer-field/choices']]
 out={}
 for text in texts:
  text=text.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\\\\\','\\\\')
  for lab,body in re.findall(r'([A-E])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):out[lab]=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
 return out
def rank(m):
 a=[list(map(Fraction,row)) for row in m];r=0
 for c in range(len(a[0])):
  k=next((i for i in range(r,len(a)) if a[i][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for i in range(r+1,len(a)):
   v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def info(rec):
 q=rec['question'];r=int(re.search(r'rank of \$(\d+)',q[':question/problem'])[1]);ms=matrices(q);eligible=[k for k,m in sorted(ms.items()) if min(len(m),len(m[0]))>=r];good=[k for k,m in sorted(ms.items()) if rank(m)==r]
 return {'question_id':q[':question/id'],'profile':rec['generation']['source_id'],'target':r,'eligible':eligible,'excluded':sorted(set(ms)-set(eligible)),'matches':good,'ranks':{k:rank(m) for k,m in ms.items()},'shapes':{k:[len(m),len(m[0])] for k,m in ms.items()}}
def shortcut_group(x):return x['target']==3 and sorted(x['shapes'].values())==[[2,4],[3,4],[5,5]] and x['excluded']==['B']
def main():
 stages={name:load(E/file) for name,file in [('catalog','catalog.json'),('catalog_surviving','delivery-catalog/accepted.json'),('fresh','fresh.json'),('fresh_surviving','delivery-fresh/accepted.json'),('batch','batch.json'),('batch_surviving','delivery-batch/accepted.json')]}
 summary={};cases=[];badpair=[]
 for name,rs in stages.items():
  rows=[info(r) for r in rs];groups=collections.defaultdict(list)
  for row in rows:groups[row['profile']+' excluded='+','.join(row['excluded'])].append(row)
  summary[name]={'count':len(rows),'profiles':dict(collections.Counter(x['profile'] for x in rows)),'groups':{k:{'count':len(v),'outcomes':dict(collections.Counter(','.join(x['matches']) or 'None' for x in v))} for k,v in groups.items()},'conditional_A_shortcut':{'cue':'rank 3, matrix shapes 2x4/3x4/5x5, B dimension-excluded','successes':sum('A' in x['matches'] for x in rows if shortcut_group(x)),'attempts':sum(shortcut_group(x) for x in rows)},'records':rows}
  if name in ('catalog_surviving','batch_surviving'):
   for rec,row in zip(rs,rows):
    if not shortcut_group(row):continue
    # Treat A as always correct; inspect rank only for C. B is visibly dimension-excluded.
    guess=['A']+(['C'] if rank(matrices(rec['question'])['C'])==3 else [])
    f=rec['question'][':question/answer-fields'][0];chosen=next(a for a in f[':answer-field/choices'] if sorted(set(re.findall(r'\$([A-E])\$',a[':answer/value'])))==guess)
    cases.append({'label':name+' '+row['question_id'],'record':rec,'checks':[{'field_index':0,'submitted_answer_id':chosen[':answer/id'],'expected':'accepted' if guess==row['matches'] else 'rejected','purpose':'Hardcode A as qualifying; inspect C only; skips inspection of eligible A'}]})
    if name=='batch_surviving':badpair.append(rec)
 save('coverage-results.json',summary);save('minimal-failing-batch.json',badpair);save('shortcut-grader-input.json',cases)
 # Probe fixed displayed answer position and fixed literal answer in each recognizable profile.
 probes=[]
 for name in ('catalog_surviving','batch_surviving'):
  rs=stages[name];groups=collections.defaultdict(list)
  for r in rs:groups[r['generation']['source_id']].append(r)
  for sid,recs in groups.items():
   if recs[0]['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/checkbox'):
    actions=[','.join(info(r)['matches']) or 'None' for r in recs];cue='fixed qualifying subset'
   else:
    actions=[str(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1])) for r in recs];cue='fixed stored-bank position (UI display order is randomized separately)'
   best,count=collections.Counter(actions).most_common(1)[0];probes.append({'stage':name,'profile':sid,'cue':cue,'strategy':best,'correct':count,'total':len(recs),'conclusion':'Singleton profile is descriptive only; no universal generator defect inferred.' if len(recs)==1 else 'Compare with independently varied ranks and subset cases, not aggregate balance.'})
 save('shortcut-probes.json',probes)
 # Actual source inventory has original questions only; no generated records to reproduce.
 inv=load(J/'source/inventory.json');src=load(J/'source/source.json');sourceids={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']};originals=[q for q in inv['questions'] if q[':question/id'] in sourceids]
 save('affected-inventory.json',{'affected_questions':[]});save('inventory-review.json',{'basis':inv['basis'],'total':len(inv['questions']),'verified_original_source_questions':len(originals),'generated_records':len(inv['questions'])-len(originals),'conclusion':'Verified absence of stored generated questions in captured inventory; not an untested inventory. Original instructional questions are not reclassified as generated. Batch-only conditional selection defect has no demonstrated affected stored generated record.','original_question_ids':sorted(sourceids)})
 # Faithful read-only reproduction of select(): equal easy-band weights imply uniform within the sorted fresh pool.
 # Publication entity IDs do not yet exist: use stated hypothetical monotonically allocated IDs solely for sensitivity scenarios.
 existing=[q for q in inv['questions'] if all(':answer-field/correct' in f for f in q[':question/answer-fields'])]
 base=max(q[':db/id'] for q in inv['questions'])+1
 newids={base+i:r for i,r in enumerate(stages['batch_surviving'])};pool={q[':db/id']:q[':question/id'] for q in existing}|{i:r['question'][':question/id'] for i,r in newids.items()}
 selection={}
 for scenario,ids in [('no_seen_history',sorted(pool)),('all_originals_seen',sorted(newids))]:
  counts=collections.Counter()
  for i in range(1000):
   seed=f'task-900001/kp-17592186119848/slot-{i}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);chosen=ids[int(u*len(ids))];counts[pool[chosen]]+=1
  selection[scenario]={'candidate_count':len(ids),'draws':1000,'counts':dict(counts),'batch_shortcut_group_selections':sum(counts[r['question'][':question/id']] for r in badpair),'conditional_A_success_rate':1.0,'unconfigured_policy_first_candidate':pool[ids[0]]}
 save('learner-selection.json',{'basis':inv['basis'],'implementation':'engine/rust/question_selection.rs select: sorted unique IDs, eligible easy band; SHA256 bytes8:16 shifted11 for uniform within-band draw. learning.rs filters seen and invalid practice questions.','existing_complete_usable':len(existing),'existing_missing_keys':len(inv['questions'])-len(existing),'new_batch_valid':len(newids),'generation_rejection':'Finite batch shuffles all 39 candidates and keeps one per mathematical fingerprint (24); count>24 fails. All checkbox cases have explicit selectable None, so nonempty policy makes no further rejection.','scenarios':selection,'limits':['No publication or database access. Proposed entity IDs are hypothetical and reported, not claimed actual.','Live learner histories, reservations, retirement and policy are not in captured inputs. Examined configured positive-easy weights and legacy unconfigured branch; zero easy weight prevents all easy delivery.','Among available fresh easy records the configured selector is uniform; it does not repair a conditional A-always-correct subgroup. Future inventory may differ.'],'hypothetical_new_entity_ids':{str(k):v['question'][':question/id'] for k,v in newids.items()}})
 print(json.dumps({'batch_conditional':summary['batch_surviving']['conditional_A_shortcut'],'catalog_control':summary['catalog_surviving']['conditional_A_shortcut'],'affected_generated_inventory':0,'selection_cases':len(selection),'shortcut_grader_cases':len(cases)}))

if __name__=="__main__":main()
