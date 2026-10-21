"""Retained review counterexamples; complete-bank equality remains mandatory."""
import sys
sys.dont_write_bytecode=True
from independent import *

def main():
 sources=json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']
 results=[]
 q=next(q for q in sources if q[':question/id']=='afe0707b-0259-50d7-a719-7a8d24334500')
 source_bank=sorted(str(matrices(c[':answer/value'])[0]) for c in q[':question/answer-fields'][0][':answer-field/choices'])
 instance=dict(template='scale',matrix=[[1,2,3],[3,4,5],[4,6,7]],target=0,factor='2',letter='A')
 candidates=[]
 for cols in itertools.permutations(range(3)):
  for extra in [1,2]:
   i=dict(instance,columns=list(cols),extra_row=extra)
   try:
    record=g.build(i);candidates.append(record)
   except ValueError:continue
 # The repaired package has a distinct complete-bank profile, not another
 # partial-column assignment. Keep all original attempts and test that profile.
 try:
  candidates.append(g.build(dict(instance,profile='source:'+q[':question/id'])))
 except (ValueError,KeyError,StopIteration):pass
 save('q10252-replay-candidates.json',candidates)
 matched=[r for r in candidates if sorted(str(matrices(c[':answer/value'])[0]) for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])==source_bank]
 try:
  assert matched,'q-10252: no scaling replay bank reproduces all five captured options'
  for record in matched:
   result=check(record)
   assert result['unique_correct'] and result['final_solution_correct'],result
 except AssertionError as e:results.append({'source_id':q[':question/id'],'passed':False,'error':str(e),'tested':len(candidates)})
 else:results.append({'source_id':q[':question/id'],'passed':True})
 q=next(q for q in sources if q[':question/id']=='337ae2e1-4641-5c8b-9b2a-9435340f0134')
 inst=dict(template='add',profile='source:'+q[':question/id'],matrix=[[1,-1,2],[3,-4,4]],target=1,donor=0,coefficient=-3,letter='B')
 try:
  r=g.build(inst)
  assert sorted(str(matrices(c[':answer/value'])[0]) for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(str(matrices(c[':answer/value'])[0]) for c in q[':question/answer-fields'][0][':answer-field/choices'])
  result=check(r)
  assert result['unique_correct'] and result['final_solution_correct'],result
 except (StopIteration,AssertionError,ValueError) as e:results.append({'source_id':q[':question/id'],'passed':False,'exception':type(e).__name__,'error':str(e),'instance':inst})
 else:results.append({'source_id':q[':question/id'],'passed':True})
 save('source-replay-regression-results.json',results)
 print(json.dumps(results));return 0 if all(r['passed'] for r in results) else 1
if __name__=='__main__':raise SystemExit(main())
