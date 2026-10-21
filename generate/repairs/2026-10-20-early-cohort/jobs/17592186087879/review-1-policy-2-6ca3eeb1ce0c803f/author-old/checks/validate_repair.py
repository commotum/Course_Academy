"""Targeted visible-math, replay, counterfactual and fixture checks. No services."""
import collections, importlib.util, json, sys, types
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from coefficient_regression import g
from visible_math import expr, eq, mathcheck, promptdata, s, x
E=ROOT/'evidence'
SOURCE=ROOT.parent/'source/source.json'
def save(name,value): (E/name).write_text(json.dumps(value,indent=2,default=str))
def key(r,fi):
 f=r['question'][':question/answer-fields'][fi]
 return expr(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
def grading(rows):
 cases=[]
 for r in rows:
  p,q,t,h=promptdata(r); checks=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    v=expr(a[':answer/value'])
    valid=eq(s.diff(v,x),p*v) and v!=0 if fi==0 else eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)
    checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],
      'expected':'accepted' if valid else 'rejected','purpose':'Independent displayed ODE/IC witness'})
  cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
 return cases

def main():
 spec=importlib.util.spec_from_file_location('stages',ROOT/'17592186087879/validate.py')
 stages=importlib.util.module_from_spec(spec);spec.loader.exec_module(stages)
 old=types.ModuleType('reviewed');old.__file__=str(ROOT/'17592186087879.py')
 exec(compile((E/'reviewed-entrypoint.py').read_text(),str(E/'reviewed-entrypoint.py'),'exec'),old.__dict__)
 source=json.loads(SOURCE.read_text())['material']['kp'][':knowledge-point/questions']
 replays=[]; replaychecks=[]
 for tid,(level,fam,params,_,_) in g.OBS.items():
  r=g.generate(level,seed=432,template=tid,parameters=params,profile='observed');replays.append(r)
  q=next(q for q in source if q[':question/math-academy-id']==tid)
  banks=[]
  for f in q[':question/answer-fields']:
   rf=next(f2 for f2 in r['question'][':question/answer-fields'] if f2[':answer-field/key']==f[':answer-field/key'])
   remaining=[expr(a[':answer/value']) for a in rf[':answer-field/choices']]
   for a in f[':answer-field/choices']:
    v=expr(a[':answer/value']);i=next(i for i,b in enumerate(remaining) if eq(v,b));remaining.pop(i)
   assert not remaining
   banks.append(len(f[':answer-field/choices']))
   if ':answer-field/correct' in f:
    assert eq(key(r,0 if f[':answer-field/key']=='field-1' else 1),expr(f[':answer-field/correct'][':answer/value']))
  norm=lambda t:t.replace(r'\left','').replace(r'\right','')
  assert norm(q[':question/problem'])==norm(r['question'][':question/problem'])
  if ':question/worked-solution' in q:
   assert stages.prose(norm(q[':question/worked-solution']))==stages.prose(norm(r['question'][':question/worked-solution']))
  assert r==old.generate(level,seed=432,template=tid,parameters=params,profile='observed')
  stages.check_record(r,allow_ambiguous=r['generation']['source_ambiguous_bank'])
  replaychecks.append({'source_id':q[':question/id'],'template':tid,'prompt':True,'banks':banks,'solution':True if ':question/worked-solution' in q else 'missing; independently derived'})
 save('source-replays.json',replays);save('source-replay-results.json',replaychecks)
 rows=[g.generate('easy',seed=400+i) for i in range(36)]
 controlled=[g.generate('easy',seed=991,parameters={'a':a,'b':2,'h':-1}) for a in range(1,7)]
 controlled += [g.generate('easy',seed=991,parameters={'a':2,'b':2,'h':h}) for h in (-2,3)]
 for a in (1,6):
  for b in (1,6):
   for h in (-6,6):
    if h!=b:controlled.append(g.generate('easy',seed=827,parameters={'a':a,'b':b,'h':h}))
 assert all(eq(key(r,0),s.exp(2*x)) for r in controlled[6:8])
 assert not eq(key(controlled[6],1),key(controlled[7],1))
 irrelevant=g.generate('easy',seed=992,parameters={'a':2,'b':2,'h':-1})
 assert eq(key(controlled[1],0),key(irrelevant,0)) and eq(key(controlled[1],1),key(irrelevant,1))
 # Hold the displayed forcing Q=4 and initial value fixed, varying only P.
 fixedq=[g.generate('easy',seed=991,parameters={'a':a,'b':4//a,'h':-1}) for a in (1,2,4)]
 assert all(promptdata(r)[1]==4 for r in fixedq)
 controlled += [irrelevant]+fixedq
 other=[g.generate(level,seed=3901,template=tid) for tid,(level,fam) in g.AUTH.items() if level!='easy']
 save('sample-records.json',rows+controlled)
 save('controlled-records.json',controlled)
 checks=[mathcheck(r) for r in rows+controlled+other]
 save('math-results.json',checks)
 assert all(v['passed'] for v in checks),[v for v in checks if not v['passed']]
 # Reuse retained printed-stage validator without running its unrelated sweeps.
 stage_count=sum(stages.check_record(r) for r in controlled+other)
 save('stage-results.json',{'records':len(controlled+other),'algebra_rows':stage_count})
 rejects=[]
 for p in ({'a':0,'b':2,'h':-1},{'a':7,'b':2,'h':-1},{'a':2,'b':2,'h':2},{'a':2,'b':2,'h':0}):
  try:g.generate('easy',seed=991,parameters=p)
  except ValueError as e:rejects.append({'parameters':p,'rejected':str(e)})
  else:raise AssertionError(p)
 save('rejection-results.json',rejects)
 save('grader-input.json',grading(rows+controlled+other))
 save('render-records.json',[controlled[0],controlled[1],controlled[5],controlled[7]])
 save('validation-summary.json',{'source_cases':len(replaychecks),'source_choices':sum(sum(v['banks']) for v in replaychecks),'math_cases':len(checks),'printed_rows':stage_count,'semantic_sample_count':len({r['generation']['mathematical_fingerprint'] for r in rows+controlled}),'generator_rejections':len(rejects)})
 print((E/'validation-summary.json').read_text())

if __name__=='__main__':main()
