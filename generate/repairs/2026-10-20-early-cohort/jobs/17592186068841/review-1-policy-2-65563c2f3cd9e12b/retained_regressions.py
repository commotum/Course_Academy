"""Retained review counterexamples, tested against current served records.
Run with the job Python: checks/regressions.py [family|shortcut|grader|render|all].
Writes evidence only. Never mutates runtime files or opens a database/service.
"""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,re,subprocess
from pathlib import Path
from independent_math import parse,value,correct,rhs,s,X,Y,K,C
W=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186068841/workspace')
REPO=next(p for p in W.parents if (p/'generate/pipeline/check_delivery.py').exists())
JOB=W.parent
EV=Path(__file__).resolve().parent/'regression-evidence';EV.mkdir(exist_ok=True)

def save(n,v):
 p=EV/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n');return p

def module():
 spec=importlib.util.spec_from_file_location('candidate',W/'17592186068841.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def call(cmd,name):
 p=subprocess.run([str(c) for c in cmd],text=True,capture_output=True)
 save(name,{'command':[str(c) for c in cmd],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 assert p.returncode==0,(name,p.stdout[-500:],p.stderr[-1500:])

def construct(r,fragment):
 """Read the response scaffold, never the generator spec or its metadata."""
 prompt=r['question'][':question/problem'];f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):return [fragment]
 m=re.search(r'\$y=-(\d+)\(\$',prompt)
 if m:return [-s.Integer(m[1])/(fragment+K)]
 assert re.search(r'\$y=\\pm \(\$',prompt) and '$+K)^{1/2}$' in prompt,prompt
 return [s.sqrt(fragment+K),-s.sqrt(fragment+K)]

def verify_math(records,name):
 results=[]
 for r in records:
  q=r['question'];ode=rhs(q[':question/problem']);f=q[':question/answer-fields'][0];valid=[];options=[]
  for option in f[':answer-field/choices']:
   expr=value(option[':answer/value']);solutions=construct(r,expr);ok=True;tests=[]
   for sol in solutions:
    residual=s.diff(sol,X)-ode.subs(Y,sol)
    vals=[]
    for x,k in [(s.Rational(1,5),3),(s.Rational(1,2),7),(s.Rational(4,5),11)]:
     sub={X:x,K:k,C:k};a=complex(residual.subs(sub).evalf(25));scale=1+abs(complex(s.diff(sol,X).subs(sub).evalf(25)))+abs(complex(ode.subs(Y,sol).subs(sub).evalf(25)));vals.append(abs(a)/scale<1e-12)
    good=all(vals) and bool(sol.free_symbols & {K,C});ok &= good
    tests.append({'solution':str(sol),'residual':str(residual),'tested_points_zero':vals})
   if ok:valid.append(option[':answer/id'])
   options.append({'value':option[':answer/value'],'checks':tests})
  # Final worked equation must give the same family as the printed keyed entry.
  last=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)[-1]
  last=last.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')[-1].replace('&','').strip().rstrip('.,')
  last=last.replace(r'\pm','')
  final=value(last); expected=construct(r,value(correct(r)))[0]
  final_match=s.simplify(final-expected)==0
  passed=valid==[f[':answer-field/correct'][1]] and final_match
  results.append({'id':q[':question/id'],'printed_rhs':str(ode),'valid_ids':valid,'final_worked_equation':last,'final_matches':final_match,'passed':passed,'options':options})
 save(name,{'method':'Independent printed TeX parser, differentiation against printed ODE at three rational points; both signs of square-root blank. Final displayed worked equation also compared exactly to the reinserted key. Positive local branches for radical source routes.','count':len(results),'results':results})
 assert all(x['passed'] for x in results),[(x['id'],x['final_matches']) for x in results if not x['passed']]

def family(m):
 records=[m.generate_moderate(730033,'q-128198',parameters={'a':a},profile=p) for a in [1,2,8] for p in ['observed','repaired']]
 for r in records:
  assert r['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/blank'
  assert r['question'][':question/problem'].count('{{field-1}}')==1
 verify_math(records,'family-math.json');save('family-records.json',records)
 print('missing-family regression: 6 records, both signs pass')

def leakage(r):
 prompt=r['question'][':question/problem'];f=r['question'][':question/answer-fields'][0];cues=[]
 for span in re.findall(r'\$([^$]+)\$',prompt):
  # Attack exactly the reported interval-copy-and-power strategy. Also detect
  # any prompt math with an arbitrary constant plus x, regardless of wording.
  if not (re.search(r'(?<![A-Za-z])[CK](?![A-Za-z])',span) and 'x' in span):continue
  bare=span.split('>')[0].split(r'\ne')[0]
  try:inner=parse(bare)
  except Exception:continue
  for power,scale in [(2,1),(2,4),(s.Rational(2,3),1)]:
   matches=[a for a in f[':answer-field/choices'] if s.simplify(value(a[':answer/value'])-inner**power/scale)==0]
   cues.append({'span':span,'power':str(power),'scale':scale,'success':len(matches)==1 and matches[0][':answer/id']==f[':answer-field/correct'][1]})
 return cues

def shortcut(m):
 records=[m.generate_moderate(730071+i,n,parameters={'a':a}) for n in ['q-8303','q-79665','q-8304'] for i,a in enumerate([1,2,7,8])]
 # The probe must actually detect the old reported defect, not be vacuously green.
 old=[x for x in json.loads((EV/'before.json').read_text()) if x.get('template')]
 old_probe=[]
 for o in old:
  r=m.generate_moderate(730061,o['template'],parameters={'a':1});r['question'][':question/problem']=o['prompt'];found=leakage(r);assert any(v['success'] for v in found);old_probe.append({'template':o['template'],'attacks':found})
 input_path=save('shortcut-records.json',records)
 call([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',input_path,'--source',JOB/'source/source.json','--inventory',JOB/'source/inventory.json','--difficulty','moderate','--output',EV/'delivery-moderate'],'delivery-moderate-command.json')
 survivors=json.loads((EV/'delivery-moderate/accepted.json').read_text());assert len(survivors)==12
 report={}
 for stage,rs in [('before',records),('delivered',survivors)]:
  attack=[{'id':r['question'][':question/id'],'cues':leakage(r)} for r in rs];assert not any(x['cues'] for x in attack)
  report[stage]={'records':len(rs),'templates':{n:sum(r['generation']['template']==n for r in rs) for n in ['q-8303','q-79665','q-8304']},'attacks':attack}
 report['old_probe_detected']=old_probe
 save('shortcut-results.json',report);verify_math(records,'shortcut-math.json')
 print('shortcut regression: old defect detected; 0 leaks in 12 raw / 12 delivered')

def grader(m):
 cases=[]
 # Retain the exact historical record and strict submission without rewriting it.
 old=json.loads((EV/'before-grader-input.json').read_text());cases+=old
 for name,coefficients in [('q-128191',[1,4]),('q-128198',[1,2,8])]:
  for a in coefficients:
   for profile in ['observed','repaired']:
    r=m.generate_moderate(730033,name,parameters={'a':a},profile=profile);answer=value(correct(r))
    prompt=r['question'][':question/problem'];assert 'nonconstant polynomial term' not in prompt
    checks=[]
    for v in [answer,answer+5,answer-s.Rational(2,3),answer+s.pi]:
     checks.append({'submitted':str(v).replace('**','^'),'expected':'accepted','purpose':'same local family after translating arbitrary K by variable-free constant'})
    for v in [2*answer,answer+X,answer+X**3,s.Integer(5)]:
     # Independent ODE witness for every proposed rejection.
     sols=construct(r,v);ode=rhs(prompt);assert any(s.simplify(s.diff(sol,X)-ode.subs(Y,sol))!=0 for sol in sols)
     checks.append({'submitted':str(v).replace('**','^'),'expected':'rejected','purpose':'changes printed differential equation, independently witnessed'})
    cases.append({'label':f'{name} a={a} {profile}','record':r,'checks':checks})
 # Same expression in inapplicable context must use ordinary equality.
 import copy
 for i,prompt in enumerate(['Simplify $y=($ {{field-1}} $+K)^{-1}$. K is an arbitrary constant.', 'Find the general solution to the differential equation. K is an arbitrary constant. $y=(x*$ {{field-1}} $+K)^{-1}$','Find the general solution to the differential equation. K is an arbitrary constant. $y=($ {{field-1}} $^2+K)^{-1}$','Find the general solution to the differential equation. K is an arbitrary constant. $y=($ {{field-1}} $+K*x)^{-1}$','Find the general solution to the differential equation. K is an arbitrary constant. $y=K($ {{field-1}} $+K)^{-1}$','Find the general solution to the differential equation. K is an arbitrary constant. $y=($ {{field-1}} $+K)^{-1}+K*x$']):
  r=copy.deepcopy(old[0]['record']);r['question'][':question/problem']=prompt
  cases.append({'label':f'negative context {i}','record':r,'checks':[{'submitted':'x^2+5','expected':'rejected','purpose':'no additive-family contract or parameter occurs in coupled positions'}]})
 inp=save('grader-input.json',cases);call([REPO/'generate/runs/current/check-engine',inp,EV/'grader-report.json'],'grader-command.json')
 print('grading regression: exact retained counterexample, 10 current blank records, 6 negative contexts pass')

def render(m):
 records=[m.generate_moderate(730033,n,parameters={'a':a},profile=p) for n,a,p in [('q-128191',1,'repaired'),('q-128191',4,'observed'),('q-128198',1,'observed'),('q-128198',8,'repaired')]]
 # Include a repaired domain prompt alongside the two blank layouts.
 records += [m.generate_moderate(730061,'q-79665',parameters={'a':2})]
 inp=save('render-input.json',records)
 call([sys.executable,REPO/'generate/pipeline/render_preview.py','--input',inp,'--output',EV/'render'],'render-command.json')
 out=[]
 for i in range(1,len(records)+1):
  html=(EV/f'render/question-{i:03}.html').read_text();blocks=re.findall(r'<pre.*?</pre>',html,re.S)
  assert not blocks,(i,blocks)
  assert '<mjx-container' in html
  out.append({'index':i,'literal_code_blocks':len(blocks),'mathjax':True})
 save('render-structure.json',out)
 print('rendering regression: 5 actual UI pages, no literal mathematical code blocks; screenshots require author inspection')

def main():
 mode=sys.argv[1] if len(sys.argv)>1 else 'all';m=module()
 for name,fn in [('family',family),('shortcut',shortcut),('grader',grader),('render',render)]:
  if mode in (name,'all'):fn(m)
if __name__=='__main__':main()
