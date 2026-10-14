#!/usr/bin/env python3
"""Independent displayed-math, source-mask, complete-bank and real-grader checks."""
import concurrent.futures, importlib.util,json,os,re,subprocess,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).parent;spec=importlib.util.spec_from_file_location('advanced',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,r,t=g.x,g.y,g.r,g.t
TRANS=standard_transformations+(implicit_multiplication_application,)
def parse(v):
 v=v.replace('\\left','').replace('\\right','').replace('\\,','').replace('\\cdot','*').replace('\\pi','pi').replace('\\theta','theta')
 while '\\frac{' in v:
  pos=v.index('\\frac{');i=pos+5
  def group(i):
   assert v[i]=='{';j=i+1;depth=1
   while depth:
    depth+=(v[j]=='{')-(v[j]=='}');j+=1
   return v[i+1:j-1],j
  a,j=group(i);b,k=group(j);v=v[:pos]+'(('+a+')/('+b+'))'+v[k:]
 v=v.replace('^','**').replace('{','(').replace('}',')')
 for f in ('cos','sin','ln'):v=v.replace('\\'+f,f)
 v=re.sub(r'\b(cos|sin)\s*theta\b',r'\1(theta)',v)
 return parse_expr(v,local_dict={'x':x,'y':y,'r':r,'theta':t,'pi':S.pi,'sin':S.sin,'cos':S.cos,'ln':S.log},transformations=TRANS)
def same(a,b):assert S.simplify(a-b)==0,(a,b)
def learner(r):return r['question'][':question/problem']+'\n'+r['question'][':question/worked-solution']+'\n'+'\n'.join(a[':answer/value'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices'])
def formatting(r):
 z=learner(r);assert not re.search(r'[+-]\s*-',z), 'ungrouped adjacent signs in displayed learner content';assert not any(ord(c)<32 and c not in '\n\t\r' for c in z);assert z.count('$')%2==0
 depth=0
 for i,c in enumerate(z):
  if c in '{}' and (i==0 or z[i-1]!='\\'):depth+=1 if c=='{' else -1;assert depth>=0
 assert depth==0
 for f in r['question'][':question/answer-fields']:
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in r['question'][':question/problem']
def check_source_structure(meta,sol):
 """Independent transcription of source operative stages; never row-count QA."""
 f=meta['template'];p=meta['parameters'];c=p['c'];stages=meta['stages'];required=[]
 I=lambda lo,hi,z,var:r'\int_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'+z+r'\,\mathrm d '+var
 ev=lambda z,var,a,b:z+r'\big|_{'+g.tex(a)+'}^{'+g.tex(b)+'}'
 dif=lambda u,v:r'\left('+u+'-'+r'\left('+v+r'\right)'+r'\right)'
 hp=lambda v,n:'('+g.tex(v)+')^{'+str(n)+'}'
 amplitude=lambda c,z:z if c==1 else g.tex(c)+r'\cdot\left('+z+r'\right)'
 def assert_order(rows):
  pos=0
  for row in rows:
   nxt=sol.find(row,pos);assert nxt>=0,('missing source operation',f,row);pos=nxt+len(row)
 if f.startswith('annulus'):
  a,b=p['inner'],p['outer'];R=lambda z:I(0,2*S.pi,I(a,b,z,'r'),r'\theta');trig=r'\cos^2\theta+\sin^2\theta'
  assert g.tex(a)+r'\le r\le '+g.tex(b) in sol
  if f=='annulus_sin2':
   required=[g.tex(-3*c)+r'\cdot '+R(r'r^3\sin(2\theta)'),g.tex(-3*c)+r'\cdot '+I(0,2*S.pi,r'\sin(2\theta)',r'\theta')+r'\cdot '+I(a,b,'r^3','r'),g.tex(-3*c)+r'\cdot '+ev(r'\frac{\cos(2\theta)}{-2}',r'\theta',0,2*S.pi)+r'\cdot '+ev(r'\frac{r^4}{4}','r',a,b),amplitude(c,r'\frac{3}{2}')+r'\cdot (1-1)\cdot\frac{1}{4}\cdot '+dif(hp(b,4),hp(a,4))]
   for sentence in ("As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as",'But this time, our region $R$ (in polar coordinates) is given by','Therefore, we get'):assert sentence in sol
   assert 'Recall that the change of variables formula' not in sol
   assert r'0\le\theta<2\pi' in sol
   primitive_texts=(r'\frac{\cos(2\theta)}{-2}',r'\frac{r^4}{4}')
  elif f=='annulus_odd':
   sub=g.tex(3*c)+r'\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r'
   fact=g.tex(3*c)+r'r^2\sin\theta\cdot r^2('+trig+')';reduced=g.tex(3*c)+r'r^4\sin\theta'
   primitive_texts=(r'-\cos\theta',r'\frac{'+g.tex(3*c)+r'r^5}{5}')
   radial=dif(r'\frac{'+g.tex(3*c)+r'\cdot '+hp(b,5)+'}{5}',r'\frac{'+g.tex(3*c)+r'\cdot '+hp(a,5)+'}{5}')
   required=[R(sub),R(fact),R(reduced),I(0,2*S.pi,r'\sin\theta',r'\theta')+r'\cdot '+I(a,b,g.tex(3*c)+'r^4','r'),ev(primitive_texts[0],r'\theta',0,2*S.pi)+r'\cdot '+ev(primitive_texts[1],'r',a,b),dif(r'-\cos(2\pi)',r'-\cos(0)')+r'\cdot '+radial,dif('-1','-1')+r'\cdot '+radial]
  else:
   n=6 if f=='annulus_fourth' else 4;factor=-c if f=='annulus_negative' else 4*c if f=='annulus_four' else c;k=2*S.pi*factor
   sub=r'((r\cos\theta)^2+(r\sin\theta)^2)'+('^2' if n==6 else '')+r'\cdot r';fact='r^{'+str(n-2)+'}('+trig+')'+('^2' if n==6 else '')+r'\cdot r';red='r^{'+str(n-1)+'}'
   coeff=lambda z:z if factor==1 else g.tex(factor)+r'\left('+z+r'\right)'
   if f=='annulus_four':
    required=[g.tex(factor)+r'\cdot '+R(sub),g.tex(factor)+r'\cdot '+R(fact),g.tex(factor)+r'\cdot '+R(red),g.tex(factor)+r'\cdot '+I(0,2*S.pi,'',r'\theta')+r'\cdot '+I(a,b,red,'r')]
   else:required=[R(coeff(sub)),R(coeff(fact)),R(g.tex(factor*r**(n-1))),I(0,2*S.pi,'',r'\theta')+r'\cdot '+I(a,b,g.tex(factor*r**(n-1)),'r')]
   primitive_texts=('theta',r'\frac{r^{'+str(n)+'}}{'+str(n)+'}')
   required += [g.tex(k)+r'\cdot '+I(a,b,red,'r'),g.tex(k)+r'\cdot '+ev(primitive_texts[1],'r',a,b),amplitude(c,g.tex(-S.pi/2 if f=='annulus_negative' else 2*S.pi if f=='annulus_four' else S.pi/3 if n==6 else S.pi/2))+r'\cdot '+dif(hp(b,n),hp(a,n))]
  # Differentiate the ACTUALLY displayed source-style primitive strings.
  same(S.diff(parse(primitive_texts[0]),t),S.sympify(stages['angular'],locals={'theta':t}));same(S.diff(parse(primitive_texts[1]),r),S.sympify(stages['radial'],locals={'r':r}))
 else:
  X,Y={'rectangle_y2':(S.Integer(1),y**2),'rectangle_x3y2':(x**3,y**2),'rectangle_xy':(2*x,y),'rectangle_shift':(2*x,2*y),'rectangle_x2y3':(x**2,4*y**3)}[f];X=c*X;G=S.integrate(X,x);H=S.integrate(Y,y)
  expectedG={'rectangle_y2':g.tex(c*x),'rectangle_x3y2':r'\frac{'+('' if c==1 else g.tex(c))+'x^4}{4}','rectangle_xy':g.tex(c*x*x),'rectangle_shift':g.tex(c*x*x),'rectangle_x2y3':r'\frac{'+('' if c==1 else g.tex(c))+'x^3}{3}'}[f]
  expectedH={'rectangle_y2':r'\frac{y^3}{3}','rectangle_x3y2':r'\frac{y^3}{3}','rectangle_xy':r'\frac{y^2}{2}','rectangle_shift':'y^2','rectangle_x2y3':'y^4'}[f]
  same(S.diff(parse(expectedG),x),X);same(S.diff(parse(expectedH),y),Y)
  C=S.sympify(meta['curl'],locals={'x':x,'y':y})
  A,B=p['outer'],p['hole']
  repeated=lambda a:I(a[2],a[3],I(a[0],a[1],g.tex(C),'x'),'y')
  separated=lambda a:I(a[0],a[1],g.tex(X) if X!=1 else '', 'x')+r'\cdot '+I(a[2],a[3],g.tex(Y),'y')
  primitive=lambda a:ev(expectedG,'x',a[0],a[1])+r'\cdot '+ev(expectedH,'y',a[2],a[3])
  ends=lambda a:g.endpoint(G,x,a[0],a[1])+r'\cdot '+g.endpoint(H,y,a[2],a[3])
  collected=lambda a:g.par(G.subs(x,a[1])-G.subs(x,a[0]))+r'\cdot '+g.par(H.subs(y,a[3])-H.subs(y,a[2]))
  sub=lambda u,v:u+'-'+(r'\left('+v+r'\right)' if v.lstrip().startswith('-') else v)
  required=[r'\iint_{\Delta_1}'+g.tex(C)+r'\,\mathrm dA-\iint_{\Delta_2}'+g.tex(C)+r'\,\mathrm dA',sub(repeated(A),repeated(B)),sub(separated(A),separated(B)),sub(primitive(A),primitive(B)),sub(ends(A),ends(B)),sub(collected(A),collected(B))]
 assert_order(required)
 return required

def check_math(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 formatting(rec);meta=rec['generation'];f=meta['template'];p=meta['parameters'];q=rec['question'];sol=q[':question/worked-solution'];prompt=q[':question/problem'];c=p['c']
 if f=='annulus_supplied':C=parse(re.search(r'\\partial P\}\{\\partial y\}=([^$]+)',prompt)[1]);P=Q=None
 else:
  # Read actual displayed field definitions and prompt components independently.
  m=re.search(r'\\oint_\{\\partial [DR]\}\((.*?)\)\\,\\mathrm dx\+\((.*?)\)\\,\\mathrm dy',prompt);assert m
  P,Q=map(parse,m.groups());C=S.diff(Q,x)-S.diff(P,y)
  assert S.denom(S.together(P)).free_symbols.isdisjoint({x,y}) and S.denom(S.together(Q)).free_symbols.isdisjoint({x,y})
  for log in (P.atoms(S.log)|Q.atoms(S.log)):
   assert log.args[0]==1+S.sin(y)**2, 'unproved nonpositive/singular logarithm argument'
  definitions=re.search(r'P\(x,y\)=([^$]+)\$ and \$Q\(x,y\)=([^$]+)',sol);assert definitions
  same(P,parse(definitions[1]));same(Q,parse(definitions[2].removesuffix('.')))
  deriv=re.search(r'\\frac\{\\partial P\}\{\\partial y\}=([^,]+),\\qquad\\frac\{\\partial Q\}\{\\partial x\}=([^$]+)',sol);assert deriv
  same(S.diff(P,y),parse(deriv[1]));same(S.diff(Q,x),parse(deriv[2].removesuffix('.')))
  for var,field in ((y,P),(x,Q)):assert r'\frac{\partial}{\partial '+str(var)+'}'+g.par(field) in sol
  assert 'including zero contributions' in sol
  formal=re.search(r'The component derivatives, including zero contributions, are\s*\$\$(.*?)\$\$',sol,re.S)[1].strip().replace(r'\begin{aligned}','').replace(r'.\end{aligned}','')
  rows=formal.split(r'\\ ');assert len(rows)==2
  for row,var,field in zip(rows,(y,x),(P,Q)):
   pieces=row.split('=');assert len(pieces)==4
   contribution=pieces[2];components=[];depth=0;start=0
   for i,ch in enumerate(contribution):
    if ch in '({':depth+=1
    elif ch in ')}':depth-=1
    elif ch=='+' and depth==0:components.append(contribution[start:i]);start=i+1
   components.append(contribution[start:]);expected=[S.diff(p['c']*term,var) for term in S.Add.make_args(field/p['c'])];assert len(components)==len(expected)
   for displayed,required in zip(components,expected):same(parse(displayed),required)
   same(parse(pieces[2]),S.diff(field,var));same(parse(pieces[3]),S.diff(field,var))
  assert 'partial Q}{\\partial x}-\\frac{\\partial P}{\\partial y}' in sol
 same(C,S.sympify(meta['curl'],locals={'x':x,'y':y}))
 if f!='annulus_supplied':assert (r'\iint_R\left(' if f=='annulus_sin2' else r'\iint_D\left(')+g.tex(parse(deriv[2].removesuffix('.')))+'-('+g.tex(parse(deriv[1]))+r')\right)\,\mathrm dA' in sol
 fields=q[':question/answer-fields'];field=fields[0] if fields else None;bank=[parse(a[':answer/value']) for a in field[':answer-field/choices']] if field else [];assert field or meta.get('calculation_only');assert all(S.simplify(a-b)!=0 for i,a in enumerate(bank) for b in bank[i+1:])
 if f.startswith('annulus'):
  a,b=p['inner'],p['outer'];polar=S.expand_trig(C.subs({x:r*S.cos(t),y:r*S.sin(t)})*r);ans=S.integrate(S.integrate(polar,(r,a,b)),(t,0,2*S.pi));d=meta['stages'];rad=S.sympify(d['radial'],locals={'r':r});ang=S.sympify(d['angular'],locals={'theta':t});fac=S.sympify(d['factor']);G=S.sympify(d['G'],locals={'theta':t});H=S.sympify(d['H'],locals={'r':r});same(S.diff(G,t),ang);same(S.diff(H,r),rad);same(S.trigsimp(polar),S.trigsimp(fac*rad*ang));components=[G.subs(t,2*S.pi),G.subs(t,0),H.subs(r,b),H.subs(r,a)]
  # Displayed primitive row and all four endpoint components must survive.
  assert g.endpoint(H,r,a,b) in sol
  if ang!=1:assert g.endpoint(G,t,0,2*S.pi) in sol
 else:
  def integrate_bounds(B):return S.integrate(C,(x,B[0],B[1]),(y,B[2],B[3]))
  ans=integrate_bounds(p['outer'])-integrate_bounds(p['hole']);d=meta['stages'];gx=S.sympify(d['gx'],locals={'x':x});gy=S.sympify(d['gy'],locals={'y':y});G=S.sympify(d['G'],locals={'x':x});H=S.sympify(d['H'],locals={'y':y});same(gx*gy,C);same(S.diff(G,x),gx);same(S.diff(H,y),gy);components=[]
  for A in (p['outer'],p['hole']):
   components.append([G.subs(x,A[1]),G.subs(x,A[0]),H.subs(y,A[3]),H.subs(y,A[2])]);assert g.bound(A) in sol;assert g.endpoint(G,x,A[0],A[1]) in sol;assert g.endpoint(H,y,A[2],A[3]) in sol;assert g.evaluate(d['primitive_tex']['x'],'x',A[0],A[1]) in sol;assert g.evaluate(d['primitive_tex']['y'],'y',A[2],A[3]) in sol
   assert g.integ(A[2],A[3],g.integ(A[0],A[1],g.tex(S.factor(C)),'x'),'y') in sol
 def stringify(v):return [stringify(a) for a in v] if isinstance(v,list) else str(v)
 assert stringify(components)==d['endpoint_components']
 if field:
  correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);same(parse(correct[':answer/value']),ans)
 same(S.sympify(meta['answer'],locals={'pi':S.pi}),ans);assert sol.endswith(g.tex(ans)+'.\\end{aligned}\n$$');check_source_structure(meta,sol)
 return ans

def main():
 sourcecases=[];review=[];native=[];solution_fidelity=[];stage_index=[];counts={'sources':0,'fields':0,'bank_values':0,'correct_designations':0,'missing_correct_designations':0,'raw_exact_prompts':0,'raw_exact_solutions':0};families=set();fingerprints=set()
 for sid,original in g.QUESTIONS.items():
  f=g.BY_SOURCE[sid];level=g.FAMILIES[f][0];case={'source_id':sid,'template':f,'level':level,'parameters':{'amplitude':1},'bank_profile':'raw:'+sid};sourcecases.append(case);z=g.generate(level,template=f,parameters=case['parameters'],profile=case['bank_profile']);q=z['question'];assert q[':question/problem']==original[':question/problem'];assert q[':question/worked-solution']==original[':question/worked-solution'];counts['sources']+=1;counts['raw_exact_prompts']+=1;counts['raw_exact_solutions']+=1
  d=g.FAMILIES[f];curl=S.diff(d[3],x)-S.diff(d[2],y)
  if f.startswith('annulus'):
   actual=S.integrate(S.integrate(curl.subs({x:r*S.cos(t),y:r*S.sin(t)})*r,(r,d[4],d[5])),(t,0,2*S.pi))
  else:
   def sourceintegral(B):return S.integrate(curl,(x,B[0],B[1]),(y,B[2],B[3]))
   actual=sourceintegral(d[4])-sourceintegral(d[5])
  for of in original[':question/answer-fields']:
   if ':answer-field/correct' in of:same(g.scalar(of[':answer-field/correct'][':answer/value']),actual)
  assert len(q[':question/answer-fields'])==len(original[':question/answer-fields'])
  for fd,of in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   counts['fields']+=1;assert fd[':answer-field/key']==of[':answer-field/key'] and fd[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in fd[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);counts['bank_values']+=len(fd[':answer-field/choices']);correct=of.get(':answer-field/correct')
   if correct:counts['correct_designations']+=1;assert next(a[':answer/value'] for a in fd[':answer-field/choices'] if a[':answer/id']==fd[':answer-field/correct'][1])==correct[':answer/value']
   else:counts['missing_correct_designations']+=1;assert ':answer-field/correct' not in fd
  # Native replay retains every gradeable original bank. The legacy field with
  # absent designation is ungradeable evidence, excluded only from this fixture.
  native_record=json.loads(json.dumps(z));native_record['question'][':question/answer-fields']=[v for v in q[':question/answer-fields'] if ':answer-field/correct' in v]
  sourcechecks=[]
  for index,v in enumerate(native_record['question'][':question/answer-fields']):
   if v[':answer-field/type'].endswith('/blank'):
    sourcechecks.extend([{'field_index':index,'submitted':'0','expected':'accepted','purpose':'source blank canonical'},{'field_index':index,'submitted':'1-1','expected':'accepted','purpose':'source equivalent zero'},{'field_index':index,'submitted':'1','expected':'rejected','purpose':'source incorrect'}])
   else:
    sourcechecks.extend({'field_index':index,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==v[':answer-field/correct'][1] else 'rejected','purpose':'historical full-bank designation'} for a in v[':answer-field/choices'])
  native.append({'label':'raw:'+sid,'record':native_record,'checks':sourcechecks})
  # Verify raw replay is actually parameterized, including empirical banks.
  assert g.raw_scaled(2,r'\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})')==r'\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})'
  assert g.raw_scaled(2,r'F\cdot \mathrm dr')==r'F\cdot \mathrm dr'
  z2=g.generate(level,template=f,parameters={'amplitude':2},profile=case['bank_profile']);assert z2['question'][':question/problem']!=q[':question/problem'];review.append({'label':'Raw original '+sid,'record':z});review.append({'label':'Generated historical-evidence amplitude variant '+sid,'record':z2})
 for sid,source in g.QUESTIONS.items():
  f=g.BY_SOURCE[sid];d=g.FAMILIES[f];anchor={'c':1,'inner':d[4],'outer':d[5]} if f.startswith('annulus') else {'c':1,'outer':d[4],'hole':d[5]}
  original_rows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',source[':question/worked-solution'],re.S)[-1].split(r'\\')
  roles=(['external_minus_three_repeated_integral','separation','separate_primitives','both_denominator_factorizations_and_angular_endpoints','final'] if f=='annulus_sin2' else ['polar_substitution','radial_factorization','trig_cancellation_and_jacobian','separation','separate_primitives','symbolic_angular_and_held_radial_endpoints','evaluated_angular_and_held_radial_endpoints','final'] if f=='annulus_odd' else ['polar_substitution','radial_factorization','trig_cancellation_and_jacobian','separation','angular_evaluation','radial_primitive','factor_denominator_outside_endpoint_powers','final'] if f.startswith('annulus') else ['outer_minus_hole','dx_then_dy_bounds','separation','separate_primitive_products','individual_primitive_endpoint_values','collected_signed_endpoint_differences','final'])
  assert len(original_rows)==len(roles);stage_index.append({'source_id':sid,'template':f,'source_rows':[{'role':role,'actual_source_row':row.strip()} for role,row in zip(roles,original_rows)]})
  changed=g.generate(d[0],91,template=f)
  for label,p in [('original anchor',anchor),('changed parameters',changed['generation']['parameters'])]:
   calculation=g.build(d[0],f,p,'calculation-only',0,calculation_only=True)
   fixture=g.record(d[0],f,p,'calculation-only',calculation['prompt'],calculation['solution'],[],0,[],{**calculation,'calculation_only':True})
   check_math(fixture);requirements=check_source_structure(fixture['generation'],calculation['solution'])
   # Common source prose is checked against THIS source, not a generic OPEN.
   opening=source[':question/worked-solution'].split('As we saw earlier' if f=='annulus_sin2' else 'We have that')[0];assert calculation['solution'].startswith(opening)
   solution_fidelity.append({'source_id':sid,'template':f,'case':label,'parameters':p,'evidence_only':True,'bank_eligibility_not_claimed':True,'source_worked_solution':source[':question/worked-solution'],'normal_worked_solution':calculation['solution'],'checked_source_operatives_in_order':requirements,'endpoint_components':calculation['stages']['endpoint_components']})
 for f,d in g.FAMILIES.items():
  for seed in range(2):
   z=g.generate(d[0],seed+91,template=f);check_math(z);review.append({'label':'Generated variant '+f+' '+str(seed),'record':z})
  for seed in range(8):
   z=g.generate(d[0],seed*17+19,template=f);check_math(z);families.add(f);fingerprints.add(z['generation']['mathematical_fingerprint'])
   fd=z['question'][':question/answer-fields'][0];correct=fd[':answer-field/correct'][1];checks=[]
   if fd[':answer-field/type'].endswith('/blank'):
    checks=[{'submitted':'0','expected':'accepted','purpose':'canonical zero'},{'submitted':'1-1','expected':'accepted','purpose':'equivalent zero'},{'submitted':'1','expected':'rejected','purpose':'incorrect nonzero'}]
   else:checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank ID'} for a in fd[':answer-field/choices']]
   native.append({'label':f+':'+str(seed),'record':z,'checks':checks})
 signed_grammar=[]
 for f,d in g.FAMILIES.items():
  if d[0]!='hard':continue
  baseline=g.generate_hard(91,template=f)['generation']['parameters']
  for coefficient in (-3,-2,-1,1,2,3):
   parameters={**baseline,'c':coefficient};rec=g.generate_hard(91,template=f,parameters=parameters);check_math(rec)
   assert '--' not in learner(rec) and '+-' not in learner(rec)
   field=rec['question'][':question/answer-fields'][0];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'signed-grammar full bank'} for a in field[':answer-field/choices']]
   native.append({'label':f+':signed:'+str(coefficient),'record':rec,'checks':checks});signed_grammar.append({'template':f,'coefficient':coefficient,'public_generate':True,'adjacent_signs_absent':True,'record':rec})
 (ROOT/'signed-grammar-review.json').write_text(json.dumps(signed_grammar,indent=2)+'\n')
 # Reverting a complete grouped hole primitive to bare subtraction must fail.
 rec=g.generate_hard(91,template='rectangle_y2',parameters={**g.generate_hard(91,template='rectangle_y2')['generation']['parameters'],'c':-2});hole=rec['generation']['parameters']['hole'];stages=rec['generation']['stages'];product=g.evaluate(stages['primitive_tex']['x'],'x',hole[0],hole[1])+r'\cdot '+g.evaluate(stages['primitive_tex']['y'],'y',hole[2],hole[3]);grouped=r'\left('+product+r'\right)';assert '-'+grouped in rec['question'][':question/worked-solution']
 bad=json.loads(json.dumps(rec));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('-'+grouped,'-'+product,1)
 try:formatting(bad)
 except AssertionError:pass
 else:raise AssertionError('negative-hole-product grouping mutation escaped')
 for level in ('easy','moderate','hard'):
  observed={g.generate(level,seed)['generation']['template'] for seed in range(80)};assert observed=={f for f,d in g.FAMILIES.items() if d[0]==level}
 # Identity is invariant to seed/order with fixed mathematics/presentation.
 z=g.generate_hard(4);p=z['generation']['parameters'];f=z['generation']['template'];other=g.generate_hard(90,template=f,parameters=p);assert z['question'][':question/id']==other['question'][':question/id']
 # Boundary errors must not be silently resampled.
 for bad in ({'c':0,'inner':1,'outer':2},{'c':4,'inner':1,'outer':2},{'c':1,'inner':2,'outer':2}):
  try:g.generate_easy(parameters=bad)
  except ValueError:pass
  else:raise AssertionError('invalid input accepted')
 # Structural mutation: erase a required primitive while preserving final value.
 bad=json.loads(json.dumps(z));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(g.evaluate(z['generation']['stages']['primitive_tex']['x'],'x',p['outer'][0],p['outer'][1]),'0')
 try:check_math(bad)
 except AssertionError:pass
 else:raise AssertionError('primitive mutation escaped')
 bad=g.generate_hard(91,template='rectangle_xy');bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'\left(0\right)',r'\left(1\right)',1)
 try:check_math(bad)
 except AssertionError:pass
 else:raise AssertionError('individual zero-component mutation escaped')
 bad=json.loads(json.dumps(z));bad['question'][':question/problem']+='\x0c'
 try:formatting(bad)
 except AssertionError:pass
 else:raise AssertionError('control mutation escaped')
 # Source-stage mutations preserve full mathematical equality but remove an
 # operative source factor/cancellation/endpoint stage. Independent checks reject.
 structural_mutations=[]
 for f in ('annulus_quadratic','annulus_fourth','annulus_negative','annulus_four','annulus_odd','annulus_sin2'):
  original=g.generate_moderate(91,template=f);bad=json.loads(json.dumps(original));ops=original['generation']['stages']['source_operative_rows'];removed=ops[-2] if f=='annulus_odd' else ops[-1]
  replacement=ops[-1] if f=='annulus_odd' else g.tex(S.sympify(original['generation']['answer'],locals={'pi':S.pi}))
  same(parse(removed),parse(replacement));assert removed!=replacement
  bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(removed,replacement,1)
  try:check_math(bad)
  except AssertionError:structural_mutations.append({'template':f,'removed_source_stage':removed,'CAS_equivalent_replacement':replacement,'rejected':True})
  else:raise AssertionError(('equivalent source-stage mutation escaped',f))
 (ROOT/'structural-mutations.json').write_text(json.dumps(structural_mutations,indent=2)+'\n')
 (ROOT/'source-stage-index.json').write_text(json.dumps(stage_index,indent=2)+'\n');(ROOT/'solution-fidelity.json').write_text(json.dumps(solution_fidelity,indent=2)+'\n')
 fidelity_md=['# Per-source normal solution fidelity','','These are calculation-renderer comparisons, not eligibility claims for original operation banks. Rectangle anchors with colliding normal banks remain rejected by the public API. Each source’s own operative stages are checked in order, beyond mathematical equality. Raw source mistakes remain in the source column; the normal column uses documented minimal repairs.','']
 for case in solution_fidelity:
  fidelity_md += ['## '+case['source_id']+' — '+case['case'],'','Parameters: `'+json.dumps(case['parameters'],sort_keys=True)+'`.','','### Original source chain and prose','',case['source_worked_solution'],'','### Normal chain and prose','',case['normal_worked_solution'],'','Checked original operation fragments in order:','']+['- `'+row+'`' for row in case['checked_source_operatives_in_order']]+['']
 (ROOT/'solution-fidelity.md').write_text('\n'.join(fidelity_md)+'\n')
 # Fresh concurrent plot calls never use shared render input files.
 saved_root=g.ROOT;g.ROOT=ROOT/'concurrency';g.ROOT.mkdir(exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda p:g.generate_easy(parameters=p),[{'c':1,'inner':1,'outer':5},{'c':1,'inner':1,'outer':5},{'c':-3,'inner':2,'outer':4}]))
 g.ROOT=saved_root
 for a in results:
  png=Path(a['generation']['plot']);assert png.exists() and png.with_suffix('.json').exists();assert json.loads(png.with_suffix('.json').read_text())['parameters']==a['generation']['parameters']
 assert results[0]['generation']['plot']==results[1]['generation']['plot'] and results[0]['generation']['plot']!=results[2]['generation']['plot']
 (ROOT/'source-cases.json').write_text(json.dumps(sourcecases,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n');(ROOT/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(ROOT/'native-input.json'),str(ROOT/'native-results.json')],check=True)
 engine=json.loads((ROOT/'native-results.json').read_text());result={'pass':True,'source_fidelity':counts,'authored_easy':True,'normal_families_checked':sorted(families),'normal_checks':96,'signed_hard_grammar_regression':{'families':5,'coefficients':[-3,-2,-1,1,2,3],'public_cases':30,'grouping_mutation_rejected':True},'normal_source_solution_fidelity':{'anchor_cases':11,'changed_cases':11,'ordered_source_operations':True,'equivalent_stage_mutations_rejected':6},'meaningful_tasks_in_checks':len(fingerprints),'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'source_anomalies':['q-126645 duplicate legacy selection lacks correct: preserved raw; one field normal','q-126937 singular ln(sin²y): raw premise invalid; normal ln(1+sin²y)','q-126939 wrong +cos primitive: raw retained; normal -cos','q-126938 intermediate upper bound2 typo: raw retained; normal outer bound3'],'source_mathematical_eligibility':{'valid_sources':10,'invalid_premises':1},'source_presentation_normalizations':{'q-169207':'remove stray differential after an evaluated primitive product; raw retained','radial_substitutions':'explicitly group full sum under the polar Jacobian','notation':'standard TeX commands and grouped signed products'},'native_ungradeable_original_fields':{'count':1,'reason':'duplicate legacy selection lacks original correct ref; raw replay retains absence'},'database_writes':0,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__,'matplotlib':g.matplotlib.__version__}}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 lines=['# Review: raw originals and generated variants','','Original raw records preserve source mistakes and legacy-field presence. Historical amplitude variants are evidence-only empirical banks; normal generated variants use complete method-derived banks. Easy is authored supplied-curl scope. All source/bank repairs are documented in template-extraction.md.','']
 for entry in review:
  record=entry['record'];q=record['question'];lines += ['## '+entry['label'],'','Parameters: `'+json.dumps(record['generation']['parameters'],sort_keys=True)+'`; profile `'+record['generation']['profile']+'`.','',q[':question/problem'].replace('](images/','](/media/jake/SSD/EDB/math/images/'),'']
  for fd in q[':question/answer-fields']:
   lines.append('Field `'+fd[':answer-field/key']+'` ('+fd[':answer-field/type']+'):')
   for answer in fd[':answer-field/choices']:
    correct=fd.get(':answer-field/correct',[None,None])[1]==answer[':answer/id'];lines.append('- $'+answer[':answer/value']+'$'+(' (correct)' if correct else ''))
   if ':answer-field/correct' not in fd:lines.append('Original correct designation absent; retained as evidence.')
   lines.append('')
  lines += [q[':question/worked-solution'],'']
 (ROOT/'review.md').write_text('\n'.join(lines)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
