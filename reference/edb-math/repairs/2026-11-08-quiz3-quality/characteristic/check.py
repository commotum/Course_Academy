from pathlib import Path
exec(open(Path(__file__).with_name('math.py')).read().split("if __name__")[0])
for d in base.glob('175*'):
 rows=[]
 for q in json.loads((d/'questions.json').read_text()):
  row={'eid':q[':db/id'],'mid':q[':question/math-academy-id'],'choices':[]}
  try:ode=extract_ode(q);row['ode']=str(ode)
  except:ode=None
  prob=q[':question/problem'];var=t if 'y(t)'in prob or re.search(r't\^|\{t\}|t>',prob)else x
  if ode is not None:
   coeff=[S.expand(ode).coeff(k)for k in [Ypp,Yp,Y]];poly=S.expand(coeff[0]*(L*(L-1)if var in coeff[0].free_symbols else L**2)+(coeff[1]/var if var in coeff[1].free_symbols else coeff[1])*L+coeff[2])
   if var in coeff[0].free_symbols:poly=S.expand(coeff[0]/var**2*L*(L-1)+coeff[1]/var*L+coeff[2])
   roots=S.solve(poly,L);row.update(variable=str(var),characteristic=str(poly),roots=list(map(str,roots)))
  else:coeff=[];roots=[]
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):
    val=a[':answer/value'];r={'eid':a[':db/id'],'value':val,'stored_correct':a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id')}
    try:
     if ' or 'in val:r['parsed']=[str(tex(s.replace('$','')))for s in val.split(' or ')];r['mathematically_correct']=set(map(tex,[v.replace('$','')for v in val.split(' or ')]))==set(roots)
     elif r'\pm'in val or '\\\\pm'in val:
      r['parsed']=[str(tex(val.replace(r'\pm',z)))for z in ['+','-']];r['mathematically_correct']=set(map(str,roots))==set(r['parsed'])
     else:
      if '='in val:val=val.split('=',1)[1]if 'instance'not in prob else val.split('=')[0]
      v=tex(val);r['parsed']=str(v)
      if 'instance'in prob:
       ce=[S.expand(v).coeff(z)for z in [Ypp,Yp,Y]];r['mathematically_correct']=bool(ce[0]!=0 and all(var not in S.simplify(c/var**n).free_symbols for c,n in zip(ce,[2,1,0])))
      elif any(z in v.free_symbols for z in [x,t,A,B,P,Q,C,D]):
       resid=S.simplify(coeff[0]*S.diff(v,var,2)+coeff[1]*S.diff(v,var)+coeff[2]*v);r['residual']=str(resid);good=resid==0
       # Initial conditions can have left/right and braced unicode prime derivatives.
       cleaned=prob.replace('\\left','').replace('\\right','');cleaned=re.sub(r'\{y\}\^\{′\}|y\^\{′\}|y\x27','YP',cleaned)
       ic=[]
       for m in re.finditer(r'(YP|y)\s*\(([^()]*(?:\{[^{}]*\}[^()]*)?)\)\s*=\s*([^,\n$]+)',cleaned):
        arg=tex(m[2]);target=tex(re.split(r'\\(?:quad|qquad|,)|,',m[3])[0]);actual=S.diff(v,var)if m[1]=='YP'else v;delta=S.simplify(actual.subs(var,arg)-target);ic.append({'order':int(m[1]=='YP'),'argument':str(arg),'target':str(target),'difference':str(delta)});good=good and delta==0
       if ic:r['initial_conditions']=ic
       if any(w in prob.lower()for w in ['cannot','**not**']):good=not good
       r['mathematically_correct']=bool(good)
      else:r['mathematically_correct']=v in roots
    except Exception as e:r['error']=str(e)
    row['choices'].append(r)
  rows.append(row)
 (d/'mathematics.json').write_text(json.dumps(rows,indent=2))
 print(d.name,'errors',[(r['mid'],c['value'],c.get('error'))for r in rows for c in r['choices']if 'error'in c], 'bad keys',[(r['mid'],c['value'])for r in rows for c in r['choices']if c['stored_correct']and not c.get('mathematically_correct')])
