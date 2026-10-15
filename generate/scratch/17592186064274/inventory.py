"""One-basis scoped inventory using the application's native gradable pool."""
import json,subprocess
from pathlib import Path
from integration import DB,KP,ROOT,scoped
import validate as v
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
HERE=Path(__file__).resolve().parent

def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 seen={row[0] for row in shown+reserved};(p/'snapshot.json').write_text(json.dumps(scoped(kp,b,seen),indent=2))
 subprocess.run([str(HERE/'check-pool'),str(p/'snapshot.json'),str(p/'native-pool.json')],check=True,capture_output=True,text=True)
 pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
 levels={l:[] for l in ('easy','moderate','hard')};used=set();records=[];excluded=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] not in ids:excluded.append({'id':q[':db/id'],'reason':'native pool excludes shown, reserved, unrated or ungradable'});continue
  mid=q.get(':question/math-academy-id')
  if mid:
   r=v.g.generate(profile=mid,scale=1,dilation=1)
   # The frozen source replay has already independently integrated this exact
   # source template. Check its current displayed data and complete bank rather
   # than repeat symbolic integration for every inventory read.
   assert v.displayed(q[':question/problem'])==v.displayed(r['question'][':question/problem'])
   sf=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
   import sympy as sp
   assert all(sum(sp.simplify(v.expression(a[':answer/value'])-v.expression(b[':answer/value']))==0 for b in rf[':answer-field/choices'])==1 for a in sf[':answer-field/choices'])
   assert sp.simplify(v.expression(sf[':answer-field/correct'][':answer/value'])-next(v.expression(a[':answer/value']) for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]))==0
   # Actual source fields, answers, UUIDs and notation are passed to native grading.
   r['question']={':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/answer-fields':[{':answer-field/id':str(sf[':answer-field/id']),':answer-field/key':sf[':answer-field/key'],':answer-field/type':str(sf[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(sf[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in sf[':answer-field/choices']]}]}
  else:
   known={r['question'][':question/id']:r for f in (HERE/'reference/replenishment').glob('basis-*/generated.json') for r in json.loads(f.read_text())}
   r=known[str(q[':question/id'])];v.check(r)
  records.append(r);fp=v.fingerprint(q)
  if fp not in used:levels[str(q[':question/difficulty'][':db/ident']).split('/')[-1]].append(str(q[':question/id']));used.add(fp)
 v.run_native(records,p/'available-grading')
 result={'basis':b,'available_distinct_by_level':{l:len(qs) for l,qs in levels.items()},'available_question_ids':levels,'excluded':excluded,'seen_or_reserved':sorted(seen),'native_pool':pool,'canonical_excluded':True,'deduplication':'exact displayed integrand and integration bounds; identity, seed, bank and option order ignored'}
 (p/'counts.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
 from edn import loads
 b=DB.basis();kp=DB.query((HERE/'source-query.edn').read_text(),[[KP]],HERE/'reference/current','source',b)[0][0]
 print(json.dumps(counts(kp,b,HERE/'reference/current')))
