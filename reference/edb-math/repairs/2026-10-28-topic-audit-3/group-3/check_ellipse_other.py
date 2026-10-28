import json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));ns={'__file__':str(H/'check_ellipse_params.py')};exec((H/'check_ellipse_params.py').read_text().split("for q in D['questions']:")[0],ns);globals().update({k:v for k,v in ns.items()if k not in ['__name__','__file__']});qs=json.loads((H/'ellipse-other-records.json').read_text());checks=[];unresolved=[];x,y=sp.symbols('x y',real=True)
# Image-only observations made from ellipse-arc-contact.png before reading keys.
observed_angles=[(0,1),(0,.5),(1,2),(0,1),(0,.5),(1,1.5),(.5,1.5),(1.5,2),(0,.5),(0,.5),(0,.5),(1.5,2),(0,1),(0,.5),(.5,1.5),(0,1),(0,1),(0,.5),(0,1),(.5,1),(0,.5),(0,.5),(1.5,2),(0,.5),(1,2),(.5,1.5),(.5,1)]
idx=json.loads((H/'ellipse-arc-image-index.json').read_text());obs={r['entity']:{**r,'theta_over_pi':observed_angles[r['index']],'evidence':'Independent visual review of solid blue arc vs dashed background, endpoints and coordinate axes in ellipse-arc-contact.png; theta increases counterclockwise for x=h+a cos(theta), y=k+b sin(theta), a,b>0.'}for r in idx};(H/'ellipse-arc-visual-observations.json').write_text(json.dumps(list(obs.values()),indent=2))
def coordinates(tex):
 tex=normalize_source_tex(tex).replace(r'\,',' ').replace(r'\quad',' ').replace(r'\qquad',' ');out=[]
 for var in [x,y]:
  for part in split_top(tex):
   if '='not in part:continue
   try:
    left,right=part.split('=',1);eq=scalar(left)-scalar(right)
    if not eq.has(var):continue
    roots=sp.solve(eq,var);assert len(roots)==1;out.append(roots[0]);break
   except Exception:continue
 assert len(out)==2,tex
 return sp.Matrix(out)
def residual(v):
 v=normalize_source_tex(v).replace(r'\,',' ');parts=v.split('=');assert len(parts)==2,v
 return sp.expand(scalar(parts[0])-scalar(parts[1]))
def same_zero(p,q):
 ratio=sp.cancel(p/q)
 return bool(ratio!=0 and not ratio.free_symbols)
def interval(v):
 v=normalize_source_tex(v);m=re.search(r'[\[(]([^\[\]()]+),([^\[\]()]+)[\])]',v)
 if m:return scalar(m[1]),scalar(m[2])
 raise Unsupported('interval parse '+v)
for q in qs:
 try:
  prompt=q[':question/problem'];fs=q.get(':question/answer-fields',[]);solutions=q.get(':question/worked-solution','');pmath=maths(prompt)
  if 'Cartesian'in prompt:
   P=coordinates(next(t for t in pmath if 'x'in t and'y'in t and'='in t));m=model(P);c=m['center'];Q=m['Q'];expected=sp.expand((sp.Matrix([x,y])-c).dot(Q.inv()*(sp.Matrix([x,y])-c))-1);rows=[]
   for f in fs:
    for a in f[':answer-field/choices']:
     try:
      value=a[':answer/value'];value=value+'=1'if f[':answer-field/type'][':db/id']==17592186045492 and '='not in value and re.search(r'\{\{'+re.escape(f[':answer-field/key'])+r'\}\}\s*\$=1',prompt)else value
      p=residual(value);valid=same_zero(p,expected);rows.append({'answer':a[':db/id'],'valid':valid,'residual':str(p)})
     except Exception as ex:rows.append({'answer':a[':db/id'],'valid':False,'interpretation':str(ex)})
   if fs:
    f=fs[0];cid=f[':answer-field/correct'][':db/id'];valid=[r['answer']for r in rows if r['valid']];ok=cid in valid if f[':answer-field/type'][':db/id']==17592186045492 else valid==[cid];proof={'canonical':cid,'matching_answers':valid,'choices':rows,'noncanonical_blank_bank_preserved':f[':answer-field/type'][':db/id']==17592186045492}
   else:
    eqs=[]
    for t in maths(solutions):
     if'='in t:
      try:
       if same_zero(residual(t),expected):eqs.append(t)
      except Exception:pass
    ok=bool(eqs);proof={'matching_worked_equations':eqs}
   checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'kind':'Cartesian equation','parametric_coordinates':list(map(str,P)),'center':list(map(str,c)),'shape_matrix':str(Q),'independent_equation_residual':str(expected),'passed':ok,**proof})
  elif q[':db/id']in obs:
   o=obs[q[':db/id']];expected=tuple(sp.Rational(v)*sp.pi for v in o['theta_over_pi']);rows=[]
   if len(fs)==2:
    vals={f[':answer-field/key']:next(a[':answer/value']for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id'])for f in fs};keys=re.findall(r'\{\{([^{}]+)\}\}',prompt);assert len(keys)==2;got=tuple(scalar(vals[k])for k in keys);ok=all(equal(a,b)for a,b in zip(got,expected));proof={'keys_in_prompt_order':keys,'canonical_endpoints':list(map(str,got))}
   elif fs:
    f=fs[0];cid=f[':answer-field/correct'][':db/id']
    for a in f[':answer-field/choices']:
     got=interval(a[':answer/value']);rows.append({'answer':a[':db/id'],'endpoints':list(map(str,got)),'valid':all(equal(a,b)for a,b in zip(got,expected))})
    valid=[r['answer']for r in rows if r['valid']];ok=valid==[cid];proof={'canonical':cid,'matching_answers':valid,'choices':rows}
   else:
    ok=any(all(equal(a,b)for a,b in zip(interval(t),expected))for t in maths(solutions)if'['in t);proof={'canonical_example_worked_solution':solutions}
   checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'kind':'arc parameter interval','observed_closed_endpoints':list(map(str,expected)),'image_evidence':o,'passed':ok,**proof})
  else:
   # Two canonical parametrization examples: independently stated radii/center/start; verify worked coordinate pair.
   hr=scalar(re.search(r'horizontal radius\s*\$([^$]+)',prompt)[1]);vr=scalar(re.search(r'vertical radius\s*\$([^$]+)',prompt)[1]);pts=tuples(prompt);center=sp.Matrix([0,0])if'origin'in prompt else sp.Matrix(pts[0]);start=sp.Matrix(pts[-1]);matches=[]
   for t in maths(solutions):
    try:
     P=param(t);m=model(P)
     if equal(m['center'],center)and equal(m['Q'],sp.diag(hr**2,vr**2))and equal(m['start'],start)and m['orientation']==1 and m['frequency']==1:matches.append(t)
    except Exception:pass
   checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'kind':'canonical parametrization example','center':str(center),'start':str(start),'radii':str((hr,vr)),'matching_worked_parametrizations':matches,'passed':bool(matches)})
 except Exception as ex:unresolved.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'reason':str(ex)})
(H/'ellipse-other-math-validation.json').write_text(json.dumps({'checks':checks,'failures':[r for r in checks if not r['passed']],'unresolved':unresolved},indent=2));print('checks',len(checks),'failures',sum(not r['passed']for r in checks),'unresolved',len(unresolved));print([(r['entity'],r.get('reason',r.get('kind')))for r in unresolved+[r for r in checks if not r['passed']]])
