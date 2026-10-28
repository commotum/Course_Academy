import json,re,sys,collections,traceback,signal
def timed_out(*args):raise TimeoutError("Symbolic proof exceeded per-question bound")
signal.signal(signal.SIGALRM,timed_out)
from pathlib import Path
import sympy as S
from mathlib import *
H=Path(__file__).resolve().parent;DATA=json.loads((H/'current.json').read_text());I=json.loads((H.parent/'inventory.json').read_text());links={q:k for t,k,q in I['links']};ktopic={k:t['ma_id']for t in DATA['topics']for k in t['kp_ids']};out=[];candidates=[];skips=[]

def function_data(problem):
 for _,v in maths(problem):
  vv=clean(v).replace(r'\left','').replace(r'\right','')
  m=re.search(r'([fgh])\s*\(\s*([xyz](?:\s*,\s*[xyz]){1,2})\s*\)\s*=',vv)
  if not m:continue
  expression=vv[m.end():];expression=re.split(r',\s*(?:[xyz]\s*[><]|[xyz]\\(?:gt|ge|ne))',expression)[0];f=parse(expression);vars=[SYMS[x.strip()]for x in m[2].split(',')]
  target=re.findall(r'\\partial\s*([xyz])',clean(problem))
  if not target:target=re.findall(r'[fgh]\s*\}?\s*_\{?\s*([xyz])',clean(problem))
  if not target:raise ValueError('No derivative variable')
  var=SYMS[target[-1]];point=None
  for _,vvv in maths(problem):
   vv1=clean(vvv);mm=re.search(r'[fgh]\s*\}?\s*_\{?\s*[xyz]\}?\s*\(([^()]*)\)',vv1)
   if mm:
    try:pp=[parse(x.strip())for x in mm[1].split(',')]
    except Exception:continue
    if len(pp)==len(vars)and all(not x.free_symbols for x in pp):point=pp
   elif vv1.startswith('(')and vv1.endswith(')'):
    try:pp=[parse(x.strip())for x in vv1[1:-1].split(',')]
    except Exception:continue
    if len(pp)==len(vars)and all(not x.free_symbols for x in pp):point=pp
  return f,vars,var,point
 raise ValueError('No function definition')

def check(q,kp):
 p=q[':question/problem'];topic=ktopic[kp];report={'entity':q.get(':db/id',q.get(':question/id')),'identity':q.get(':question/math-academy-id'),'kp':kp,'topic':topic,'checks':[]};fs=q.get(':question/answer-fields',[]);expected=None;method=None
 if topic in [4096,1929]:
  if'Find the function $h'in p:raise ValueError('Quotient numerator target requires specific derivation')
  f,vars,var,point=function_data(p);expected=S.diff(f,var)
  if point:expected=expected.subs(dict(zip(vars,point)),simultaneous=True)
  expected=simple(expected);method='independent partial derivative'+(' and point evaluation'if point else'')
 elif topic==317:
  for _,v in maths(p):
   if r'\int'not in v:continue
   v=clean(v).rstrip('= ');e=parse(v)
   if isinstance(e,S.Equality):e=e.lhs
   if isinstance(e,S.Integral):expected=e;break
  if expected is None:raise ValueError('No parsed integral')
  method='independent definite integral'if len(expected.limits[0])==3 else'antiderivative differentiation';report['integral']=str(expected)
 elif topic==1717:
  for _,v in maths(p):
   if r'\lim'in v:
    expected=parse(v).doit();method='independent exponential limit';break
  if expected is None:raise ValueError('No parsed limit')
 elif topic==1482:
  for _,v in maths(p):
   if '='not in v:continue
   try:e=parse(v)
   except Exception:continue
   if isinstance(e,S.Equality)and len(e.free_symbols)==1:
    var=next(iter(e.free_symbols));solutions=S.solve(e,var)
    if len(solutions)==1:expected=simple(solutions[0]);method='independent logarithmic equation solution';break
  if expected is None:raise ValueError('No unique exponential equation solution')
 else:
  if topic in [6353,1181,906]or kp==17592186147453:raise ValueError('Requires role-specific coefficient, classification, verification-constant or exactness check')
  f,raw=ode(p);report['ode']=str(f);report['source_ode']=raw;method='independent ODE residual'
  if f.subs({y:0,D:0},simultaneous=True)==0:report['zero_equilibrium_admissible']=True
  coeff=simple(S.diff(f,D));P=simple(S.diff(f,y)/coeff)if not S.diff(f,y).has(y,D)and not coeff.has(y)else None
  ics=initial_values(p)
  if ics:report['initial_values']=[list(map(str,ic))for ic in ics]
  for field in fs:
   k=field[':answer-field/key'];context=p[max(0,p.find('{{'+k+'}}')-80):p.find('{{'+k+'}}')]if '{{'+k+'}}'in p else'';role='integrating-factor'if re.search(r'I\([xy]\)\s*=\s*\$?\s*$',context)else'solution'
   # Only pure solution/integrating-factor choices are covered by this residual pass.
   results=[]
   for a in field.get(':answer-field/choices',[]):
    v=a[':answer/value'];result={'answer':a.get(':db/id',a[':answer/id']),'value':v}
    try:
     sol=explicit_solution(v)
     if role=='integrating-factor':
      if P is None:raise ValueError('Not a scalar linear ODE')
      r=simple(S.diff(sol,x)-P*sol);ok=r==0 and sol!=0
     else:
      if not sol.has(x)and sol.free_symbols- {A,C}:raise ValueError('Not an x solution expression')
      r=residual(f,sol);ok=r==0
      if ok and ics:ok=all(equivalent(sol.subs(x,xx),yy)for xx,yy in ics)
      if ok and ('general solution'in p.lower()or'general solution'in context.lower())and not(sol.has(A)or sol.has(C)):ok=False
     result.update({'residual':str(r),'matches':bool(ok)})
    except Exception as ex:result['error']=str(ex)[:200]
    results.append(result)
   if results:report['checks'].append({'field':field[':db/id']if':db/id'in field else field[':answer-field/id'],'key':k,'role':role,'results':results,'current_correct':field.get(':answer-field/correct',{}).get(':db/id'),'correct_candidates':[r['answer']for r in results if r.get('matches')]})
  report['method']=method;return report
 if expected is not None:
  report['expected']=str(expected);report['method']=method
  for field in fs:
   if topic in [4096,1929]:
    pos=p.find('{{'+field[':answer-field/key']+'}}')
    if pos>=0:
     ff,vv,target,pp=function_data(p[:pos]);expected=S.diff(ff,target)
     if pp:expected=expected.subs(dict(zip(vv,pp)),simultaneous=True)
     expected=simple(expected)
   results=[]
   for a in field.get(':answer-field/choices',[]):
    r={'answer':a.get(':db/id',a[':answer/id']),'value':a[':answer/value']}
    try:
     got=rhs(a[':answer/value'])
     if isinstance(got,S.Limit):got=got.doit()
     if isinstance(expected,S.Integral):
      if len(expected.limits[0])==1:r0=simple(S.diff(got,expected.variables[0])-expected.function)
      else:r0=simple(got-expected.doit())
      match=r0==0;r['residual']=str(r0)
     elif'rerounded'in p:match=False
     elif'rounded to'in p.lower()or'round your answer'in p.lower():
      digits=re.search(r'(?:to\s*\$?(\d+)\$?\s*decimal|to\s*(one|two|three)\s*decimal)',p,re.I);places=int(digits[1])if digits and digits[1]else{'one':1,'two':2,'three':3}.get(digits[2]if digits else'',3);match=abs(float(got-expected))<0.50001*10**(-places);r['rounded_places']=places
     else:match=got==expected or equivalent(got,expected)
     r['matches']=bool(match)
    except Exception as ex:r['error']=str(ex)[:200]
    results.append(r)
   report['checks'].append({'field':field.get(':db/id',field.get(':answer-field/id')),'key':field[':answer-field/key'],'results':results,'current_correct':field.get(':answer-field/correct',{}).get(':db/id'),'correct_candidates':[r['answer']for r in results if r.get('matches')]})
 return report

if __name__=='__main__':
 targets=[(q,links[q[':db/id']])for q in DATA['questions']]
 if '--generated'in sys.argv:targets=[(r['record']['question'],r['kp'])for r in json.loads((H/'generator-samples.json').read_text())]
 for i,(q,kp)in enumerate(targets):
  try:
   signal.setitimer(signal.ITIMER_REAL,4)
   r=check(q,kp);out.append(r)
   for f in r['checks']:
    if f['current_correct']and f['current_correct']not in f['correct_candidates']and any('matches'in v for v in f['results']):candidates.append({**r,'flag':'current-key-does-not-match-independent-result','affected_field':f['field']})
    elif len(f['correct_candidates'])>1:candidates.append({**r,'flag':'multiple-matching-choices','affected_field':f['field']})
  except Exception as ex:skips.append({'entity':q.get(':db/id',q.get(':question/id')),'identity':q.get(':question/math-academy-id'),'kp':kp,'reason':str(ex)[:200]})
  signal.setitimer(signal.ITIMER_REAL,0)
  if i%50==0:
   (H/'math-progress.json').write_text(json.dumps({'last':i,'checked':out,'skipped':skips,'candidates':candidates},indent=2)+'\n');print(i,flush=True)
 suffix='generated-safe'if '--generated'in sys.argv else'current-safe'
 for name,value in [('math-verification',out),('math-candidates',candidates),('math-skips',skips)]:(H/(name+'-'+suffix+'.json')).write_text(json.dumps(value,indent=2)+'\n')
 print('checked',len(out),'skipped',len(skips),'candidates',len(candidates))
