"""Executable retained findings; always exercise the current entrypoint and visible equations."""
from common import *
import copy,argparse
ap=argparse.ArgumentParser();ap.add_argument('--finding',default='all');args=ap.parse_args()
g=load_generator();results=[]
def check(label,fn):
 try:fn();results.append({'check':label,'passed':True})
 except Exception as e:results.append({'check':label,'passed':False,'error':str(e)})
def bank_shortcuts():
 for sid in g.LEVELS['easy']:
  rows=[g.generate('easy',seed,sid) for seed in [11027,84533,230219,330721,984311,1234579]]
  answers=[verify(r) for r in rows]
  assert sum(old_shortcut(r['question'])==a for r,a in zip(rows,answers))<len(rows),sid
 # The exact runner record's numeric answer remains mathematically replayable, but is
 # no longer forced to occupy its old bank role by normal construction.
 p={'a':[9,-2,0,7],'u':[-1,5,-2,8],'c':5,'s':-1,'letter':'l'}
 r=g.generate('easy',2406259497,'q-34249',p);assert verify(r)==-1
 for sid in g.LEVELS['easy']:
  base=copy.deepcopy(g.CASES[sid]);bank=g.source_bank(sid)
  answers=set()
  for v in bank:
   if v=='No solution':continue
   p={**copy.deepcopy(base),'s':str(scalar(v)),'bank':bank}
   r=g.generate('easy',2406259497,sid,p);answers.add(verify(r))
  assert len(answers)==sum(v!='No solution' for v in bank),sid

def homogeneous():
 p=copy.deepcopy(g.CASES['q-34570']);old=g.generate('moderate',64193,'q-34570',p)
 assert verify(old)=='No solution'
 p['u'][0]=1;r=g.generate('moderate',64193,'q-34570',p);assert verify(r)==-6
 assert old['question'][':question/problem']!=r['question'][':question/problem']
 for sid in g.LEVELS['moderate']:
  answers={verify(g.generate('moderate',seed,sid)) for seed in range(24)}
  assert 'No solution' in answers and len(answers)>1,sid

def sources():
 source=json.loads((ROOT/'source-data.json').read_text())
 for old in source['questions']:
  if not old.get(':question/difficulty'):continue
  sid=old[':question/math-academy-id'];level=old[':question/difficulty'][':db/ident'].split('/')[-1]
  assert sid in g.PROFILES,sid
  r=g.generate(level,55001,sid,copy.deepcopy(g.CASES[sid]));verify(r);q=r['question']
  assert mats(old[':question/problem'])==mats(q[':question/problem']),sid
  assert [value(x[':answer/value']) for x in choices(old)]==[value(x[':answer/value']) for x in choices(q)],sid
  assert value(key(old))==value(key(q)),sid
  assert mats(old[':question/worked-solution'])==mats(q[':question/worked-solution']),sid

def subtraction():
 p={'a':[0,-1,1],'u':[-2,1,0],'c':2,'s':2,'letter':'j'}
 try:r=g.generate('easy',64193,'q-34241',p)
 except (ValueError,AssertionError):pass
 else:verify(r) # Strictly fail if the old inconsistent keyed record is still emitted.
 # Reject the invalid coefficient across varied vectors, not only the reported values.
 for c in [2,3,5]:
  p={'a':[2,-3,1],'u':[1,0,-2],'c':c,'s':-2,'letter':'j'}
  try:r=g.generate('easy',64193,'q-34241',p)
  except (ValueError,AssertionError):continue
  verify(r)
 p['c']=1;r=g.generate('easy',64193,'q-34241',p);assert verify(r)==-2
for label,fn in [('235081df96496a71953f',bank_shortcuts),('4c13ef97ea8cada2ddf5',homogeneous),('b209397fbfabda651f7f',sources),('3d76b97447fefd094eec',subtraction)]:
 if args.finding in ('all',label):check(label,fn)
assert results,'No finding tested'
save('regressions-'+args.finding+'.json',{'passed':all(x['passed'] for x in results),'checks':results})
print(json.dumps(results));raise SystemExit(0 if all(x['passed'] for x in results) else 1)
