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
 return parse_expr(v,local_dict={'x':x,'y':y,'r':r,'theta':t,'pi':S.pi,'sin':S.sin,'cos':S.cos,'ln':S.log},transformations=TRANS)
def same(a,b):assert S.simplify(a-b)==0,(a,b)
def learner(r):return r['question'][':question/problem']+'\n'+r['question'][':question/worked-solution']+'\n'+'\n'.join(a[':answer/value'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices'])
def formatting(r):
 z=learner(r);assert not any(ord(c)<32 and c not in '\n\t\r' for c in z);assert z.count('$')%2==0
 depth=0
 for i,c in enumerate(z):
  if c in '{}' and (i==0 or z[i-1]!='\\'):depth+=1 if c=='{' else -1;assert depth>=0
 assert depth==0
 for f in r['question'][':question/answer-fields']:
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in r['question'][':question/problem']
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
 if f!='annulus_supplied':assert r'\iint_D\left('+g.tex(parse(deriv[2].removesuffix('.')))+'-('+g.tex(parse(deriv[1]))+r')\right)\,\mathrm dA' in sol
 fields=q[':question/answer-fields'];field=fields[0];bank=[parse(a[':answer/value']) for a in field[':answer-field/choices']];assert all(S.simplify(a-b)!=0 for i,a in enumerate(bank) for b in bank[i+1:])
 if f.startswith('annulus'):
  a,b=p['inner'],p['outer'];polar=S.expand_trig(C.subs({x:r*S.cos(t),y:r*S.sin(t)})*r);ans=S.integrate(S.integrate(polar,(r,a,b)),(t,0,2*S.pi));d=meta['stages'];rad=S.sympify(d['radial'],locals={'r':r});ang=S.sympify(d['angular'],locals={'theta':t});fac=S.sympify(d['factor']);G=S.sympify(d['G'],locals={'theta':t});H=S.sympify(d['H'],locals={'r':r});same(S.diff(G,t),ang);same(S.diff(H,r),rad);same(S.trigsimp(polar),S.trigsimp(fac*rad*ang));components=[G.subs(t,2*S.pi),G.subs(t,0),H.subs(r,b),H.subs(r,a)]
  # Displayed primitive row and all four endpoint components must survive.
  assert g.evaluate(g.tex(H),'r',a,b) in sol;assert g.endpoint(H,r,a,b) in sol
  if ang!=1:assert g.evaluate(g.tex(G),r'\theta',0,2*S.pi) in sol and g.endpoint(G,t,0,2*S.pi) in sol
 else:
  def integrate_bounds(B):return S.integrate(C,(x,B[0],B[1]),(y,B[2],B[3]))
  ans=integrate_bounds(p['outer'])-integrate_bounds(p['hole']);d=meta['stages'];gx=S.sympify(d['gx'],locals={'x':x});gy=S.sympify(d['gy'],locals={'y':y});G=S.sympify(d['G'],locals={'x':x});H=S.sympify(d['H'],locals={'y':y});same(gx*gy,C);same(S.diff(G,x),gx);same(S.diff(H,y),gy);components=[]
  for A in (p['outer'],p['hole']):
   components.append([G.subs(x,A[1]),G.subs(x,A[0]),H.subs(y,A[3]),H.subs(y,A[2])]);assert g.bound(A) in sol;assert g.endpoint(G,x,A[0],A[1]) in sol;assert g.endpoint(H,y,A[2],A[3]) in sol;assert g.evaluate(g.tex(G),'x',A[0],A[1]) in sol;assert g.evaluate(g.tex(H),'y',A[2],A[3]) in sol
   assert g.integ(A[2],A[3],g.integ(A[0],A[1],g.tex(S.factor(C)),'x'),'y') in sol
 def stringify(v):return [stringify(a) for a in v] if isinstance(v,list) else str(v)
 assert stringify(components)==d['endpoint_components']
 correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);same(parse(correct[':answer/value']),ans);same(S.sympify(meta['answer'],locals={'pi':S.pi}),ans);assert sol.endswith(g.tex(ans)+'.\\end{aligned}\n$$')
 return ans

def main():
 sourcecases=[];review=[];native=[];counts={'sources':0,'fields':0,'bank_values':0,'correct_designations':0,'missing_correct_designations':0,'raw_exact_prompts':0,'raw_exact_solutions':0};families=set();fingerprints=set()
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
 bad=json.loads(json.dumps(z));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(g.evaluate(g.tex(S.sympify(z['generation']['stages']['G'],locals={'x':x})),'x',p['outer'][0],p['outer'][1]),'0')
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
 # Fresh concurrent plot calls never use shared render input files.
 saved_root=g.ROOT;g.ROOT=ROOT/'concurrency';g.ROOT.mkdir(exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda p:g.generate_easy(parameters=p),[{'c':1,'inner':1,'outer':5},{'c':1,'inner':1,'outer':5},{'c':-3,'inner':2,'outer':4}]))
 g.ROOT=saved_root
 for a in results:
  png=Path(a['generation']['plot']);assert png.exists() and png.with_suffix('.json').exists();assert json.loads(png.with_suffix('.json').read_text())['parameters']==a['generation']['parameters']
 assert results[0]['generation']['plot']==results[1]['generation']['plot'] and results[0]['generation']['plot']!=results[2]['generation']['plot']
 (ROOT/'source-cases.json').write_text(json.dumps(sourcecases,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n');(ROOT/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(ROOT/'native-input.json'),str(ROOT/'native-results.json')],check=True)
 engine=json.loads((ROOT/'native-results.json').read_text());result={'pass':True,'source_fidelity':counts,'authored_easy':True,'normal_families_checked':sorted(families),'normal_checks':96,'meaningful_tasks_in_checks':len(fingerprints),'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'source_anomalies':['q-126645 duplicate legacy selection lacks correct: preserved raw; one field normal','q-126937 singular ln(sin²y): raw premise invalid; normal ln(1+sin²y)','q-126939 wrong +cos primitive: raw retained; normal -cos','q-126938 intermediate upper bound2 typo: raw retained; normal outer bound3'],'source_mathematical_eligibility':{'valid_sources':10,'invalid_premises':1},'native_ungradeable_original_fields':{'count':1,'reason':'duplicate legacy selection lacks original correct ref; raw replay retains absence'},'database_writes':0,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__,'matplotlib':g.matplotlib.__version__}}
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
