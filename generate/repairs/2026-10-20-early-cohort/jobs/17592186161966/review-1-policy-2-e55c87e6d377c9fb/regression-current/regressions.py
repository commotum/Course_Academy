"""Retained repair regressions: parse visible records, never trust the generator key."""
import sys,json,copy,argparse
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode=True
import visible as v
ROOT=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186161966/workspace')
OUT=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186161966/review-1-policy-2-e55c87e6d377c9fb/regression-current');OUT.mkdir(exist_ok=True)
m=v.load_generator(ROOT/'17592186161966.py')
def save(n,x): (OUT/n).write_text(json.dumps(x,indent=2,default=int)+'\n')
def params(q):
 A,B=v.matrices(q[':question/problem']);given,p,k=v.ops(q[':question/problem'])[0]
 r=next(i for i in range(4) if A[i][p] and all(B[i][c]==0 for c in range(4) if c!=p))
 ks=[int(v.Fraction(-A[r][c],A[r][p])) if c!=p else 0 for c in range(4)]
 return dict(A=A,row=r,pivot=p,given=given,ks=ks)
def source_checks():
 src=json.load(open(ROOT/'17592186161966/source.json'))['record']
 report=[];records=[]
 for q in src[':knowledge-point/questions']:
  profile=q[':question/math-academy-id'];p=params(q)
  targets=[c for c in range(4) if c not in (p['pivot'],p['given'])]
  expected=[(c,p['pivot'],p['ks'][c]) for c in targets]
  if ':question/difficulty' not in q:
   # Retain the unrated bank evidence without inventing a difficulty or source solution.
   bank=[v.ops(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
   assert len(bank)==5 and bank.count(expected)==1
   try:m.generate(bank_profile=profile,parameters=p)
   except ValueError:pass
   else:raise AssertionError('Unrated source incorrectly sampled')
   report.append(dict(profile=profile,source_id=q[':question/id'],status='unrated-excluded',bank_verified=True));continue
  rec=m.generate(bank_profile=profile,parameters=p);v.inspect(rec);records.append(rec)
  got=[v.ops(a[':answer/value']) for a in v.field(rec)[':answer-field/choices']]
  assert v.matrices(rec['question'][':question/problem'])==v.matrices(q[':question/problem'])
  for f in q[':question/answer-fields']:
   assert sorted(got)==sorted(v.ops(a[':answer/value']) for a in f[':answer-field/choices']), profile
   if ':answer-field/correct' in f:assert v.ops(f[':answer-field/correct'][':answer/value'])==expected
  original_stages=v.matrices(q[':question/worked-solution'])
  if profile=='q-91210':
   assert original_stages[0][1][0]==7 and p['A'][1][0]==-7
   original_stages[0][1][0]=-7
  assert v.matrices(rec['question'][':question/worked-solution'])==original_stages
  report.append(dict(profile=profile,source_id=q[':question/id'],status='passed',banks=len(q[':question/answer-fields']),choices=5,pivot_value=p['A'][p['row']][p['pivot']]))
 assert {'q-130617','q-130630'}<=set(r['profile'] for r in report if r['status']=='passed')
 q=src[':knowledge-point/canonical-example'];rec=m.generate(bank_profile='q-130619',parameters=params(q));v.inspect(rec)
 assert v.matrices(rec['question'][':question/problem'])==v.matrices(q[':question/problem'])
 assert v.matrices(rec['question'][':question/worked-solution'])==v.matrices(q[':question/worked-solution'])
 records.append(rec);save('source-replays.json',records);save('source-replay-results.json',report)
 return records

def shortcut_checks():
 exact=m.generate(seed=1118318699,bank_profile='q-130619');v.inspect(exact)
 old_seeds=[m.generate(seed=731100+i,bank_profile='q-130619') for i in range(12)]
 for r in old_seeds:v.inspect(r)
 assert not all(v.shortcut(r)==v.correct_index(r) for r in old_seeds)
 records=[];report=[]
 for j,profile in enumerate(m.PROFILES):
  # All five alternatives must really become correct with exactly the same bank.
  group=[m.generate(seed=730000+j,bank_profile=profile,answer_role=role) for role in range(5)]
  for rec in group:v.inspect(rec)
  banks=[[a[':answer/value'] for a in v.field(rec)[':answer-field/choices']] for rec in group]
  assert all(b==banks[0] for b in banks),profile
  assert {v.correct_index(r) for r in group}==set(range(5)),profile
  matrices=[v.matrices(r['question'][':question/problem']) for r in group]
  changed_rows={row for row in range(4) if len({tuple(A[row]) for A,B in matrices})>1}
  assert len(changed_rows)==1
  assert len({r['question'][':question/worked-solution'] for r in group})==5
  # No bank-only deterministic rule can exceed one correct response in this group.
  report.append(dict(profile=profile,identical_visible_bank=True,correct_positions=[v.correct_index(r) for r in group],shortcut_applicable=sum(v.shortcut(r)!=None for r in group),shortcut_successes=sum(v.shortcut(r)==v.correct_index(r) for r in group),choice_only_ceiling='1/5'))
  records.extend(group)
 save('role-counterfactuals.json',records)
 save('shortcut-results.json',dict(exact={'seed':1118318699,'choices':v.coefficients(exact),'predicted':v.shortcut(exact),'correct':v.correct_index(exact)},original_regression={'attempts':12,'correct':sum(v.shortcut(r)==v.correct_index(r) for r in old_seeds)},groups=report))
 save('reported-counterexample.json',[exact]);return records
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--case',choices=['sources','shortcut','all'],default='all');args=a.parse_args()
 if args.case in ('sources','all'):source_checks()
 if args.case in ('shortcut','all'):shortcut_checks()
 print(json.dumps({'status':'passed','case':args.case}))
