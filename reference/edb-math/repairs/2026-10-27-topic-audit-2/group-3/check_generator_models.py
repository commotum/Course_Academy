import json,math,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from symbolic import parse,SYMS
import sympy as sp
checks=[];unresolved=[]
for i,s in enumerate(json.loads((H/'generator-final-samples.json').read_text())):
 kp=s['kp'];r=s['record'];g=r['generation'];p=g.get('parameters')or{};q=r['question'];fs=q.get(':question/answer-fields',[])
 if len(fs)!=1:continue
 f=fs[0];cid=f.get(':answer-field/correct');cid=cid[1]if isinstance(cid,list)else cid.get(':answer/id',cid.get(':db/id'))if isinstance(cid,dict)else None;a=next((a for a in f.get(':answer-field/choices',[])if cid in[a.get(':answer/id'),a.get(':db/id')]),None)
 if not a:continue
 val=a[':answer/value'];proof={};passed=None
 try:
  if kp==17592186078584 and p:
   A=p['ambient']
   if 'rate'in p:v=A+(p['initial']-A)*math.exp(-float(p['rate'])*p['time'])
   elif 'initial'in p:
    k=-math.log((p['observed']-A)/(p['initial']-A))/p['time'];v=-math.log((p['target']-A)/(p['initial']-A))/k
   else:
    k=-math.log((p['later']-A)/(p['observed']-A))/p['gap'];v=p['start']-math.log((p['target']-A)/(p['observed']-A))/k
   target=int(re.search(r'-?\d+',val)[0]);passed=target==math.floor(v+.5);proof={'model':'T=A+(T0−A)exp(−kt)','unrounded':v,'rounded':math.floor(v+.5),'canonical':target}
  elif kp==17592186124675 and g.get('instance'):
   p=g['instance'];A=p['a'];t0,y0=p['observations'][0]
   if p['k']is None:
    t1,y1=p['observations'][1];k=-math.log((A-y1)/(A-y0))/(t1-t0)
   else:k=float(p['k'])
   v=t0-math.log((A-p['query'])/(A-y0))/k if p['kind']=='time'else A-(A-y0)*math.exp(-k*(p['query']-t0));target=int(re.search(r'-?\d+',val)[0]);passed=target==math.floor(v+.5);proof={'model':'P=A−(A−P0)exp(−k(t−t0))','unrounded':v,'rounded':math.floor(v+.5),'canonical':target}
  elif kp in[17592186078583,17592186124674]and p:
   expr=parse(val.split('=',1)[1]);variables=expr.free_symbols-{SYMS['k']};var=next(iter(variables));rate=SYMS['k']if kp==17592186078583 or'numerator'not in p else sp.Rational(p['numerator'],p['denominator']);expected=-rate*(var-p['S'])if kp==17592186078583 else rate*(p['capacity']-var);passed=sp.simplify(expr-expected)==0;proof={'RHS':str(expr),'independent_RHS':str(expected)}
  elif kp in[17592186087839,17592186087840]and p:
   x,y=SYMS['x'],SYMS['y'];expr=parse(val.split('=',1)[0]);expected=x*x/sp.Rational(p['a'])**2+y*y/sp.Rational(p['b'])**2;passed=sp.simplify(expr-expected)==0;proof={'semiaxes':p,'expected_LHS':str(expected)}
  elif kp==17592186096698 and g.get('curves'):
   ns={'__file__':str(H/'math_check.py')};exec((H/'math_check.py').read_text().split('checks=[];unresolved=[];bad=[];completion_matches=[]')[0],ns);res,state=ns['ode_task'](q);rhs=sp.solve(res,SYMS['Z'])[0];curves=g['curves'][val];diffs=[sp.simplify(sp.diff(sp.sympify(v,locals={'x':SYMS['x']}),SYMS['x'])-rhs)for v in curves];passed=all(v==0 for v in diffs);proof={'RHS':str(rhs),'selected_curves':curves,'derivative_differences':[str(v)for v in diffs]}
  if passed is not None:checks.append({'sample':i,'kp':kp,'kind':s.get('kind','fresh'),'passed':bool(passed),'proof':proof})
 except Exception as ex:unresolved.append({'sample':i,'kp':kp,'error':str(ex)[:160]})
(H/'generator-model-geometry-validation.json').write_text(json.dumps({'checks':checks,'failures':[r for r in checks if not r['passed']],'unresolved':unresolved},indent=2));print('model/geometry',len(checks),'failed',sum(not r['passed']for r in checks),'unresolved',len(unresolved))
