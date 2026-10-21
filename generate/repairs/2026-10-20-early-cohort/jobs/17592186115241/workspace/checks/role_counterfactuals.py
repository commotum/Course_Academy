"""Keep candidate banks fixed; make each of their five lines correct in turn."""
import json,random,sys
from pathlib import Path
sys.dont_write_bytecode=True
from validate_repair import g,E,check,field,correct,vec,system,dump
fresh=json.load(open(E/'fresh.json'));base=random.Random;records=[];report=[]
try:
 for case in g.EASY_CASES:
  seed=next(r['generation']['seed'] for r in fresh if r['generation']['decision_case']==case)
  group=[]
  for role in range(5):
   class ForcedRole(base):
    def randrange(self,*args,**kwargs):
     value=super().randrange(*args,**kwargs)
     return role if args==(5,) and not kwargs else value
   g.random.Random=ForcedRole
   r=g.generate_easy(seed=seed);check(r);group.append(r)
  banks=[sorted(str(vec(c[':answer/value'])) for c in field(r)[':answer-field/choices']) for r in group]
  answers=[str(vec(next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r)))) for r in group]
  assert all(bank==banks[0] for bank in banks)
  assert len(set(answers))==5
  assert len({str(system(r['question'][':question/problem'])) for r in group})==5
  assert len({r['question'][':question/worked-solution'] for r in group})==5
  report.append({'case':case,'seed':seed,'same_complete_visible_banks':True,'different_keyed_lines':5,'different_systems_and_solutions':5,'answers':answers})
  records+=group
finally:g.random.Random=base
dump('controlled-records.json',records+json.load(open(E/'counterfactual-records.json')))
dump('role-counterfactual-records.json',records);dump('role-counterfactual-results.json',report)
dump('role-grader-input.json',[{'label':str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'fixed answer bank with controlled role changes'} for c in field(r)[':answer-field/choices']]} for i,r in enumerate(records)])
print(json.dumps({'decision_cases':len(report),'controlled_records':len(records),'same_banks_different_keys':True}))
