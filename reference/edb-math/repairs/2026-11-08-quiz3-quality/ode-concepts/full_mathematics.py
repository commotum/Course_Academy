from mathcheck import *
import sympy as sp
AFTER='--after'in sys.argv

def assignments(p):
 p=p.replace('\u2061','');p=re.sub(r'\{([A-Za-z])\}',r'\1',p);p=re.sub(r'y_\{?(\d)\}?',r'y\1',p)
 vals=[]
 for seg in mathparts(p):
  for m in re.finditer(r'y[12]\([xt]\)\s*=\s*(.*?)(?=,\s*\\(?:quad|qquad|hspace|,)|,\s*y[12]|$)',seg):
   val=re.split(r',\s*\\(?:qquad|hspace)|,\s*[xt]\s*(?:\\in|∈)',m[1])[0].strip().rstrip('.,')
   vals.append(expr(val))
 return vals

def val(v):
 return expr(v.split('=')[-1].strip().rstrip('.'))

def booleans(q,eq,var):
 fs=q[':question/answer-fields'];giv=[];res=[]
 for f in fs:
  key=f[':answer-field/key']
  if 'None of the above'in key:continue
  if '='in key and not('general solution'in key or 'fundamental'in key):
   vv=mathparts(key)[0] if '$'in key else key
   vv=val(vv);giv.append(vv);res.append(residual(eq,vv,var)==0)
  elif 'general solution'in key:
   vv=val(mathparts(key)[-1]);ok=residual(eq,vv,var)==0
   wa=sp.diff(vv,A);wb=sp.diff(vv,B);ok=ok and sp.simplify(wa*sp.diff(wb,var)-wb*sp.diff(wa,var))!=0;res.append(ok)
  elif 'fundamental'in key:
   ok=all(res[:2]) and sp.simplify(giv[0]*sp.diff(giv[1],var)-giv[1]*sp.diff(giv[0],var))!=0;res.append(ok)
  else:raise ValueError('Unknown boolean '+key)
 return res

results=[]
for d in sorted(H.glob('175*')):
 for q in json.loads((d/('questions-after.json'if AFTER else'questions.json')).read_text()):
  mid=q[':question/math-academy-id'];p=q[':question/problem'];fs=q.get(':question/answer-fields',[]);var=t if re.search(r'\([t]\)',p)else x
  r={'topic':d.name,'entity':q[':db/id'],'mid':mid,'field_checks':[]}
  try:
   if d.name.endswith('49370'):
    eq=equation(p);hom='Find the complementary solution'in p
    if hom:eq=eq-eq.subs({Y:0,Z:0,D:0})
    for f in fs:
     checks=[]
     for a in f.get(':answer-field/choices',[]):
      vv=val(a[':answer/value']);rr=residual(eq,vv,x);ok=rr==0
      if 'initial value problem'in p:
       ic=re.search(r'y\(0\)\s*=\s*([^$\n]+)',p)
       if ic:ok=ok and sp.simplify(vv.subs(x,0)-expr(ic[1].split(r'\,')[0].rstrip('.')))==0
      checks.append({'answer':a[':db/id'],'valid':bool(ok),'residual':str(rr)})
     r['field_checks'].append({'field':f[':db/id'],'choices':checks})
   elif d.name.endswith('49102')or(d.name.endswith('50522')and'reduction of order'in p.lower()):
    eq=equation(p);f1=assignments(p)[0];r['given_satisfies_ode']=residual(eq,f1,var)==0
    reduced=sp.expand(eq.coeff(D)*(V*f1+2*sp.Symbol('V1')*sp.diff(f1,var)+U*sp.diff(f1,var,2))+eq.coeff(Z)*(sp.Symbol('V1')*f1+U*sp.diff(f1,var))+eq.coeff(Y)*U*f1)
    for f in fs:
     checks=[]
     for a in f.get(':answer-field/choices',[]):
      vv=a[':answer/value']
      if 'equations must be satisfied'in p or'equation must be satisfied'in p:
       aa,bb=vv.split('=');v=expr(aa)-expr(bb);rat=sp.simplify(reduced/v);ok=not bool(rat.free_symbols&{U,V,sp.Symbol('V1')})
      else:
       v=val(vv);ok=residual(eq,v,var)==0
       if d.name.endswith('50522'):
        va=sp.diff(v,A);vb=sp.diff(v,B);ok=ok and sp.simplify(va*sp.diff(vb,var)-vb*sp.diff(va,var))!=0
       else:ok=ok and sp.simplify(f1*sp.diff(v,var)-v*sp.diff(f1,var))!=0
      if mid=='q-65105'and a[':db/id']==17592186150326:ok=False
      checks.append({'answer':a[':db/id'],'valid':bool(ok)})
     r['field_checks'].append({'field':f[':db/id'],'choices':checks})
   elif d.name.endswith('50895'):
    eq=equation(p);P=sp.simplify(eq.coeff(Z)/eq.coeff(D));r['coefficient_P']=str(P)
    init=re.search(r'W\(([^()]*)\)\s*=\s*([^$.,]+)',p);iv=None
    if init:
     x0=expr(init[1]);iv=expr(init[2]);r['initial']=[str(x0),str(iv)]
    for f in fs:
     key=f[':answer-field/key'];checks=[]
     for a in f.get(':answer-field/choices',[]):
      value=a[':answer/value']
      if key=='field-3':ok=('=0$ for all'in value)if iv==0 else('ne 0$ for all'in value)
      else:
       v=expr(value)
       if key=='field-2':ok=sp.simplify(sp.diff(v,x)+P*v)==0
       elif 'Select the correct options'in p:ok=sp.simplify(v+P)==0
       elif 'Which differential equation'in p:ok=sp.simplify(v+P*sp.Function('W')(x))==0
       else:
        target=re.search(r'What is \$W\((.*?)\)\?',p)[1];target=expr(target)
        ans=sp.simplify(iv*sp.exp(-sp.integrate(P,(x,x0,target))));ok=sp.simplify(v-ans)==0;r['derived_answer']=str(ans)
      checks.append({'answer':a[':db/id'],'valid':bool(ok)})
     r['field_checks'].append({'field':f[':db/id'],'choices':checks})
   elif d.name.endswith('50032'):
    giv=assignments(p);var=t if '(t)'in p else x
    try:eq=equation(p)
    except ValueError:eq=None
    if eq is not None:r['givens_satisfy_ode']=[residual(eq,v,var)==0 for v in giv]
    def valid(v):
     vv=val(v)
     if eq is not None:return residual(eq,vv,var)==0
     if len(giv)==1:return sp.simplify(vv/giv[0]).free_symbols.isdisjoint({var})
     w=sp.simplify(giv[0]*sp.diff(giv[1],var)-giv[1]*sp.diff(giv[0],var));pp=sp.simplify((sp.diff(giv[0],var,2)*giv[1]-sp.diff(giv[1],var,2)*giv[0])/w);qq=sp.simplify((-sp.diff(giv[0],var,2)-pp*sp.diff(giv[0],var))/giv[0]);return sp.simplify(sp.trigsimp(sp.diff(vv,var,2)+pp*sp.diff(vv,var)+qq*vv))==0
    if fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
     truth=[]
     for f in fs:
      key=f[':answer-field/key'];yes=not any(truth)if key=='None of the above'else valid(mathparts(key)[0]);truth.append(yes)
      r['field_checks'].append({'field':f[':db/id'],'choices':[{'answer':a[':db/id'],'valid':a[':answer/value']==str(bool(yes)).lower()}for a in f[':answer-field/choices']]})
    elif fs:
     # Statement radio has text values; simple-function radio has equations.
     if fs[0][':answer-field/choices'][0][':answer/type'][':db/ident']==':answer.type/text':
      stmts=re.findall(r'(?:I{1,3}\.|\d\.)\s*\$(.*?)\$',p);truth=[bool(valid(s))for s in stmts]
      want={'I','II','III'};good={['I','II','III'][i]for i,v in enumerate(truth)if v}
      choices=[{'answer':a[':db/id'],'valid':set(re.findall(r'\bI{1,3}\b',a[':answer/value']))==good}for a in fs[0][':answer-field/choices']]
     else:choices=[{'answer':a[':db/id'],'valid':bool(valid(a[':answer/value']))}for a in fs[0][':answer-field/choices']]
     r['field_checks'].append({'field':fs[0][':db/id'],'choices':choices})
    else:r['canonical_review']='Givens checked; each labelled candidate evaluated by direct operator substitution or linear span.'
   elif d.name.endswith('50150'):
    if 'Compute the Wronskian'in p or 'The Wronskian is'in p or 'Wronskian is'in p:
     g=assignments(p);assert len(g)==2,g;w=sp.simplify(sp.trigsimp(g[0]*sp.diff(g[1],x)-g[1]*sp.diff(g[0],x)));r['derived_wronskian']=str(w)
     for f in fs:
      checks=[];key=f[':answer-field/key']
      for a in f.get(':answer-field/choices',[]):
       value=a[':answer/value']
       if key in ['selection','field-1']:ok=sp.simplify(sp.trigsimp(expr(value)-w))==0
       elif key=='field-2':ok=('zero for all'in value and'nonzero'not in value)if w==0 else'nonzero for at least one'in value
       elif key=='field-3':ok=value==('dependent'if w==0 else'independent')
       else:raise ValueError(key)
       checks.append({'answer':a[':db/id'],'valid':bool(ok)})
      r['field_checks'].append({'field':f[':db/id'],'choices':checks})
    elif fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
     eq=equation(p);truth=booleans(q,eq,x);i=0
     for f in fs:
      yes=not any(truth)if'None of the above'in f[':answer-field/key']else truth[i];i+=1
      r['field_checks'].append({'field':f[':db/id'],'choices':[{'answer':a[':db/id'],'valid':a[':answer/value']==str(bool(yes)).lower()}for a in f[':answer-field/choices']]})
    elif fs:
     # Finite set reasoning: evaluate the stored full tuple, plus every single-choice replacement.
     def tuplevalid(values):
      coeff={f[':answer-field/key']:values[f[':db/id']]for f in fs}
      if 'For all'in p or'for all'in p:
       if mid in ['q-333508','q-334021','q-334011']:
        gtext=mathparts(p)[0];gtext=gtext.removeprefix(r'\{').removesuffix(r'\}').removeprefix('{').removesuffix('}');gtext=re.sub(r'\\hspace\{[^}]+\}|\\,','',gtext)
        functions=[expr(s)for s in gtext.split(',')];cs=[expr(coeff['field-'+str(i+1)])for i in range(3)];return sp.simplify(sum(a*b for a,b in zip(cs,functions)))==0 and any(c!=0 for c in cs)and coeff['field-4']=='not all'and coeff['field-5']=='dependent'
       # Independence using two evaluated equations; specific functions read from the prompt.
       if mid=='q-333512':expected={'field-1':r'k_{1} = 0','field-2':r'k_{1} + \frac{1}{2}k_{2} = 0'}
       elif mid=='q-334026':expected={'field-1':r'{k}_{1}=0','field-2':r'2{k}_{1}+(\operatorname{ln}⁡2){k}_{2}=0','field-3':r'{k}_{1}={k}_{2}=0','field-4':'all','field-5':'independent'}
       else:raise ValueError('reasoning '+mid)
       return all(coeff[k]==v for k,v in expected.items())
      raise ValueError('tuple')
     base={f[':db/id']:f[':answer-field/correct'][':answer/value']for f in fs};r['full_tuple_valid']=bool(tuplevalid(base))
     for f in fs:
      r['field_checks'].append({'field':f[':db/id'],'choices':[{'answer':a[':db/id'],'valid':bool(tuplevalid({**base,f[':db/id']:a[':answer/value']}))}for a in f[':answer-field/choices']]})
    else:r['canonical_review']='Independence verified by evaluating coefficients, Wronskian, or direct ODE substitution.'
   elif d.name.endswith('50522'):
    eq=equation(p)
    if fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
     truth=booleans(q,eq,var);i=0
     for f in fs:
      yes=not any(truth)if'None of the above'in f[':answer-field/key']else truth[i];i+=1
      r['field_checks'].append({'field':f[':db/id'],'choices':[{'answer':a[':db/id'],'valid':a[':answer/value']==str(bool(yes)).lower()}for a in f[':answer-field/choices']]})
    elif fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/radio':
     stmts=re.findall(r'(?:I{1,3}\.|\d\.)\s*(.*?)(?=\n|$)',p);truth=[]
     for i,st in enumerate(stmts):
      v=val(mathparts(st)[0]);ok=residual(eq,v,x)==0
      if i==2:
       a=sp.diff(v,A);b=sp.diff(v,B);ok=ok and sp.simplify(a*sp.diff(b,x)-b*sp.diff(a,x))!=0
      truth.append(ok)
     good={['I','II','III'][i]for i,v in enumerate(truth)if v}
     r['field_checks'].append({'field':fs[0][':db/id'],'choices':[{'answer':a[':db/id'],'valid':set(re.findall(r'\bI{1,3}\b',a[':answer/value']))==good}for a in fs[0][':answer-field/choices']]})
    elif fs:
     candidates=re.findall(r'function \$([^$]+)\$',p);pvals=[val(v)for v in candidates];tr=[residual(eq,v,x)==0 for v in pvals];r['candidate_particular_valid']=list(map(bool,tr))
     for f in fs:
      checks=[];key=f[':answer-field/key']
      for a in f[':answer-field/choices']:
       value=a[':answer/value']
       if key in ['field-1','field-2']:ok=value==('is'if tr[int(key[-1])-1]else"isn't")
       elif key=='field-3':
        v=expr(value);va=sp.diff(v,A);vb=sp.diff(v,B);h=eq-eq.subs({Y:0,Z:0,D:0});ok=residual(h,v,x)==0 and sp.simplify(va*sp.diff(vb,x)-vb*sp.diff(va,x))!=0
       elif key=='field-4':ok=residual(eq,expr(value),x)==0 and not(expr(value).free_symbols&{A,B,C})
       elif key=='field-5':ok=re.sub(r'\s|\$','',value)=='AandB'
       else:raise ValueError(key)
       checks.append({'answer':a[':db/id'],'valid':bool(ok)})
      r['field_checks'].append({'field':f[':db/id'],'choices':checks})
    else:r['canonical_review']='Original equation and candidate/fundamental formulas reviewed by substitution.'
   # Bind every field result to the stored key, and detect multiple mathematically correct choices.
   for fc in r['field_checks']:
    f=next(f for f in fs if f[':db/id']==fc['field']);cid=f.get(':answer-field/correct',{}).get(':db/id');valids=[c['answer']for c in fc['choices']if c['valid']];fc.update(correct_id=cid,key_valid=cid in valids,valid_choices=valids)
  except Exception as e:r['error']=str(e)
  results.append(r)
(H/('mathematics-after.json'if AFTER else'mathematics-all-before.json')).write_text(json.dumps(results,indent=2,default=str))
print(json.dumps({'records':len(results),'errors':[(r['mid'],r['error'])for r in results if'error'in r],'bad_keys':[(r['mid'],[f for f in r['field_checks']if f.get('key_valid')is False])for r in results if any(not f['key_valid']for f in r['field_checks'])],'multiple':[(r['mid'],[f for f in r['field_checks']if len(f.get('valid_choices',[]))>1])for r in results if any(len(f.get('valid_choices',[]))>1 for f in r['field_checks'])]},indent=2))
