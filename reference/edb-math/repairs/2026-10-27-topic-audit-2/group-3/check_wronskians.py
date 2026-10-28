import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));ns={'__file__':str(H/'math_check.py')};exec((H/'math_check.py').read_text().split('checks=[];unresolved=[];bad=[];completion_matches=[]')[0],ns);sp=ns['sp'];parse=ns['parse'];x=ns['SYMS']['x'];Y=ns['SYMS']['y'];D=json.loads((H/'proposed-snapshot.json').read_text());topicids={t['entity']for t in D['topics']if t['ma_id']==2547};ids={q for t,k,q in D['links']if t in topicids};checks=[];unresolved=[]
def defs(text):
 out={}
 for m in ns['maths'](text):
  m=re.sub(r'\{(y)\}',r'\1',m).replace(r'\displaystyle','');m=m.replace(r'\qquad',',').replace(r'\quad',',');hits=list(re.finditer(r'y_\{?([12])\}?\s*\(x\)\s*=',m))
  for i,h in enumerate(hits):
   v=m[h.end():hits[i+1].start()if i+1<len(hits)else len(m)];v=re.split(r',+(?:\\,|\s|,)*x\s*(?:\\in|∈)',v)[0];v=re.sub(r'(?:,|\\,|\s)+$','',v);out[int(h[1])]=parse(v)
 return out
for q in D['questions']:
 if q[':db/id']not in ids:continue
 try:
  fs=q.get(':question/answer-fields',[]);functions=defs(q[':question/problem']);checkbox=bool(fs and fs[0][':answer-field/type'][':db/id']==17592186408166)
  if checkbox:
   residual,state=ns['ode_task'](q);valid={};fieldchecks=[]
   for f in fs:
    label=f[':answer-field/key'];found=defs(label)
    for n,F in found.items():functions[n]=F;valid[n]=sp.simplify(residual.subs({Y:F,ns['SYMS']['Z']:sp.diff(F,x),ns['SYMS']['W']:sp.diff(F,x,2)},simultaneous=True))==0
   W=sp.simplify(functions[1]*sp.diff(functions[2],x)-functions[2]*sp.diff(functions[1],x));prior=[]
   for f in fs:
    label=f[':answer-field/key'];right=next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id'])[':answer/value']=='true'
    if'None of the above'in label:expected=not any(prior)
    elif'fundamental'in label:expected=all(valid.values())and W!=0
    else:expected=valid[next(iter(defs(label)))];prior.append(bool(expected))
    fieldchecks.append({'field':f[':db/id'],'expected':bool(expected),'canonical':right,'passed':bool(expected)==right})
   checks.append({'entity':q[':db/id'],'kind':'all checkbox statement mathematics','Wronskian':str(W),'functions':{k:str(v)for k,v in functions.items()},'checks':fieldchecks,'passed':all(r['passed']for r in fieldchecks)})
  elif len(functions)==2:
   W=sp.simplify(functions[1]*sp.diff(functions[2],x)-functions[2]*sp.diff(functions[1],x));fieldchecks=[]
   for f in fs:
    a=next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id']);v=a[':answer/value']
    if a[':answer/type'][':db/id']==17592186045498:expected=sp.simplify(parse(v)-W)==0
    elif v in ['dependent','independent']:expected=(v=='dependent')==(W==0)
    elif 'zero for all'in v:expected=W==0
    elif 'nonzero'in v:expected=W!=0
    else:continue
    fieldchecks.append({'field':f[':db/id'],'canonical':v,'passed':bool(expected)})
   checks.append({'entity':q[':db/id'],'kind':'Wronskian and dependence','Wronskian':str(W),'checks':fieldchecks,'passed':all(r['passed']for r in fieldchecks)})
  else:unresolved.append({'entity':q[':db/id'],'reason':'coefficient identity or general conceptual proof; reviewed separately'})
 except Exception as ex:unresolved.append({'entity':q[':db/id'],'reason':str(ex)[:180]})
(H/'wronskian-math-validation.json').write_text(json.dumps({'checks':checks,'failures':[r for r in checks if not r['passed']],'unresolved':unresolved},indent=2));print('Wronskianquestions',len(checks),'checkboxlabels',sum(len(r['checks'])for r in checks if'checkbox'in r['kind']),'fails',[r for r in checks if not r['passed']],'unresolved',len(unresolved))
