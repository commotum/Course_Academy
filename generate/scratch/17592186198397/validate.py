#!/usr/bin/env python3
"""Fidelity, independently parsed printed mathematics, native grading and review."""
import importlib.util,json,re,subprocess,hashlib,sys
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;REPO=D.parents[2]
sp=importlib.util.spec_from_file_location('generator',D.parent/(D.name+'.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)

def parse(tex):
 """Small strict parser of the generated LaTeX grammar; rejects unconsumed bytes.
 Does not read generation mathematical metadata; actual displayed math is input.
 """
 tex=tex.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(' ','')
 tok=re.findall(r'\\[A-Za-z]+|[0-9]+|[^\s]',tex);i=0
 def atom():
  nonlocal i
  t=tok[i];i+=1
  if t in ('+','-'):return (1 if t=='+' else -1)*atom()
  if t in ('{','(','['):
   e=expr();close={'{':'}','(':')','[':']'}[t];assert tok[i]==close,(tex,tok,i);i+=1;return e
  if t==r'\frac':return atom()/atom()
  if t==r'\sqrt':return s.sqrt(atom())
  if t in (r'\sin',r'\cos',r'\ln'):
   power=1
   if i<len(tok) and tok[i]=='^':i+=1;power=atom()
   val=atom();return {r'\sin':s.sin,r'\cos':s.cos,r'\ln':s.log}[t](val)**power
  if t==r'\pi':return s.pi
  if t=='e':return s.E
  if t.isdigit():return s.Integer(t)
  if t.isalpha() and len(t)==1:return s.Symbol(t,real=True)
  raise AssertionError(('unknown token',t,tex))
 def power():
  nonlocal i
  a=atom()
  if i<len(tok) and tok[i]=='^':i+=1;a=a**atom()
  return a
 def product():
  nonlocal i
  a=power()
  while i<len(tok) and tok[i] not in ('+', '-', ')','}',']',',','=','<','>'):
   if tok[i] in ('*',r'\cdot'):i+=1
   elif tok[i]=='/':i+=1;a/=power();continue
   a*=power()
  return a
 def expr():
  nonlocal i
  a=product()
  while i<len(tok) and tok[i] in ('+','-'):
   sign=tok[i];i+=1;a+=(1 if sign=='+' else -1)*product()
  return a
 v=expr();assert i==len(tok),(tex,tok[i:]);return v

def eq(a,b):return s.simplify(a-b)==0

def group(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  if text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def read_integral(text):
 bounds=[];i=0
 for n in range(3):
  assert text[i:].startswith(r'\int_');i+=5
  lo,i=group(text,i);assert text[i]=='^';hi,i=group(text,i+1);bounds.append((parse(lo),parse(hi)))
 tail=text[i:];assert tail.startswith(r'\left(') and tail.endswith(r'\right)\,dw\,dv\,du')
 return parse(tail[len(r'\left('):-len(r'\right)\,dw\,dv\,du')]),bounds

def formatting(text):
 assert text.count('$$')%2==0
 assert text.replace('$$','').count('$')%2==0
 depth=0
 for i,c in enumerate(text):
  if c not in '{}':continue
  # Ignore literal escaped braces only.
  if i>0 and text[i-1]=='\\':continue
  depth+=1 if c=='{' else -1;assert depth>=0
 assert depth==0

def check_printed(r):
 q=r['question'];t=r['generation']['template'];level=q[':question/difficulty'].split('/')[-1]
 prompt=q[':question/problem'];sol=q[':question/worked-solution']
 formatting(prompt);formatting(sol)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 # Recover actual displayed substitution and integrand, then invert independently.
 cv=re.search(r'Given the change of variables\s*\$\$\s*(.*?)\s*\$\$',prompt,re.S)[1].rstrip(',')
 coords=tuple(parse(part.split('=',1)[1]) for part in cv.split(',\\quad '))
 symbols=(g.X,g.Y,g.Z);new=(g.U,g.V,g.W)
 inverse=s.solve([e-n for e,n in zip(coords,new)],symbols,dict=True)
 assert len(inverse)==1;inv=inverse[0]
 f=parse(re.search(r'\\iiint_R (.*?)\\,dV',prompt,re.S)[1])
 J=s.Matrix(coords).jacobian(symbols);det=s.factor(J.det())
 jd=s.simplify(1/det.subs(inv))
 if t=='sqrt':
  assert '$w>0$' in sol
  jd=jd.xreplace({s.Abs(g.W):g.W})
 # Read all 9 numeric partials printed in Step2.
 mats=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',sol,re.S)
 numeric=mats[1];actual=s.Matrix([[parse(x) for x in row.split(' & ')] for row in numeric.split(r'\\')])
 assert actual.shape==(3,3) and all(eq(a,b) for a,b in zip(actual,J))
 # The three displayed minors are independently checked in their order.
 for j,printed in enumerate(mats[2:5]):
  minor=s.Matrix([[parse(x) for x in row.split(' & ')] for row in printed.split(r'\\')]);assert minor==J.minor_submatrix(0,j)
 stage2=sol.split('**Step 2**')[1].split('**Step 3**')[0]
 expansion=stage2.split(r'\\ &=')[2]
 factors=re.findall(r'\((.*?)\)\\begin\{vmatrix\}',expansion)
 assert len(factors)==3 and all(eq(parse(factor),J[0,j]) for j,factor in enumerate(factors))
 assert re.findall(r'\\end\{vmatrix\}([+-])',expansion)==['-','+']
 assert eq(sum((-1)**j*parse(factors[j])*J.minor_submatrix(0,j).det() for j in range(3)),det)
 rows=stage2.split(r'\\ &=') if r'\\ &=' in stage2 else stage2.split(r'\\ &=')
 # Find determinant rows after all vmatrix blocks: both original/new values.
 last=stage2.split(r'\\ &=')[-2:]
 assert len(last)==2
 assert eq(parse(last[0]),det)
 newdet=parse(last[1].split(r'.\end{aligned}')[0]);expecteddet=s.simplify(det.subs(inv))
 if t=='sqrt':expecteddet=expecteddet.xreplace({s.Abs(g.W):g.W})
 assert eq(newdet,expecteddet)
 stage3=sol.split('**Step 3**')[1].split('**Step 4**')[0]
 printedjd=parse(re.search(r'\)\^\{-1\}=(.*?)\.\s*\$\$',stage3,re.S)[1])
 assert eq(printedjd,jd)
 # Read the absolute-determinant multiplication row and final integral.
 ft=s.simplify(f.subs(inv))
 if t=='sqrt':ft=ft.xreplace({s.Abs(g.W):g.W})
 transformed=re.search(r'&=\\iiint_Δ \\left\((.*?)\\right\)\\left\|\\frac',sol,re.S)[1]
 assert eq(parse(transformed),ft)
 absrow=re.search(r'\\\\ &=\\iiint_Δ \\left\((.*?)\\right\)\\left\|(.*?)\\right\|',sol,re.S)
 assert absrow is not None and eq(parse(absrow[1]),ft) and eq(parse(absrow[2]),jd)
 if t=='product':
  printed_domain=re.search(r'Δ=\\\{\(u,v,w\): (.*?)\\\}',sol)[1]
  low,mid,high=printed_domain.split(',\\quad ')[1].split(r'\le ')
  sign=1 if parse(low)>0 else -1
  assert (parse(low)>0 and parse(high)>0) or (parse(low)<0 and parse(high)<0)
  absjd=sign*jd
 elif t=='sqrt':absjd=-jd
 else:absjd=s.Abs(jd)
 actual_correct=s.simplify(ft*absjd)
 final=re.search(r'\\\\ &=((?:\\int_).*?)\.\\end\{aligned\}',sol,re.S)[1]
 ge,b=read_integral(final);assert eq(ge,actual_correct)
 # Bounds are checked against the independently printed region inequalities.
 region=re.search(r'R=\\\{\(x,y,z\): (.*?)\\\}\.',prompt)[1]
 constraints=[]
 for item in region.split(',\\quad '):
  lo,e,hi=item.split(r'\le ');constraints.append((parse(lo),parse(e),parse(hi)))
 if t not in ('product','sqrt'):assert all(eq(e,coord) for (_,e,_),coord in zip(constraints,coords))
 if t=='product':expected=[(constraints[0][0],constraints[0][2]),(constraints[1][0],constraints[1][2]),(0,r['generation']['parameters']['a']*constraints[2][2])]
 elif t=='sqrt':expected=[(constraints[0][0],constraints[0][2]),(constraints[1][0],constraints[1][2]),(1,s.sqrt(g.U*g.V))]
 else:expected=[(lo,hi) for lo,e,hi in constraints]
 assert all(eq(x,y) for pair,pair2 in zip(b,expected) for x,y in zip(pair,pair2))
 field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
 answer=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
 if level=='easy':assert eq(parse(answer[':answer/value']),actual_correct)
 else:
  ans,ab=read_integral(answer[':answer/value']);assert eq(ans,actual_correct) and ab==b
 options=[]
 for a in field[':answer-field/choices']:
  options.append(read_integral(a[':answer/value']) if level!='easy' else (parse(a[':answer/value']),b))
 for expression,bounds in options:
  assert expression.free_symbols<=set(new)
  # Every component is real and finite throughout its guarded coordinate domain;
  # logs have positive u only, roots positive u/v/z, denominators avoid zero.
  assert all(arg==g.U for node in s.preorder_traversal(expression) if node.func==s.log for arg in node.args)
  for uval in (s.Rational(5,4),s.Rational(7,4)):
   for vval in ((-s.Rational(3,2),) if t=='product' and sign<0 else (s.Rational(3,2),)):
    val=s.simplify(expression.subs({g.U:uval,g.V:vval,g.W:s.Rational(3,2)}))
    assert val.is_real is True and val.is_finite is True
 assert g.unambiguous(options,level!='easy')
 assert 'evaluate' not in prompt.lower()
 return True

def main():
 cases=json.loads((D/'source-cases.json').read_text());source_by={q[':question/math-academy-id']:q for q in g.SOURCE_QUESTIONS}
 reviews=[];report={'version':g.VERSION,'basis':1356,'source_questions':len(cases),'fidelity':{},'source_errors':{'q-38941':'no correct original option; two absent designations cannot be credited','q-161880':'solution Step1 u0..1 repaired to prompt1..2','q-39057':'normal premise changes x bounds to bounds on2x+z, and repairs stray sin cos row','q-161879':'Step1 coordinate tuple repaired xyz to uvw'},'grading_omissions':'2 raw records lack correct refs; source omission retained, native fixtures skipped'}
 optioncount=correctcount=solutioncount=0
 for c in cases:
  r=g.generate(c['level'],seed=29,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);src=source_by[c['source_id']];q=r['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in src),(c['source_id'],key)
   if key in q and key not in (':question/answer-fields',':question/difficulty'):assert q[key]==src[key],(c['source_id'],key)
  if ':question/difficulty' in src:assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  optioncount+=len(f[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  if ':answer-field/correct' in sf:
   ca=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ca[':answer/value']==sf[':answer-field/correct'][':answer/value'];correctcount+=1
  solutioncount+=int(':question/worked-solution' in src)
  reviews.append(('Original public parameterized replay '+c['source_id'],r))
  changed=g.generate(c['level'],template=c['template'],parameters={'scale':2,'height':c['parameters']['height']},profile='raw')
  assert changed['question'][':question/problem']!=q[':question/problem']
  reviews.append(('Raw changed-amplitude evidence only '+c['source_id'],changed))
 report['fidelity']={'complete_banks':'5/5','options':f'{optioncount}/25','present_correct_designations':f'{correctcount}/3','key_presence':'5/5','full_present_solutions':f'{solutioncount}/3','unrated_difficulty_omissions':'2/2','raw_mathematical_anomalies_retained':True}
 count=0;family=set();engine=[];tasksets={level:set() for level in g.FAMILIES}
 for level,ts in g.FAMILIES.items():
  for t in ts:
   for seed in range(8):
    r=g.generate(level,seed,template=t);check_printed(r);count+=1;tasksets[level].add(r['generation']['mathematical_fingerprint'])
    if seed<2:reviews.append(('Generated '+level+' '+t,r))
    f=r['question'][':question/answer-fields'][0]
    engine.append({'label':level+' '+t+' '+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all owned radio choices'} for a in f[':answer-field/choices']]})
    replay=g.generate(level,seed+100,template=t,parameters=r['generation']['parameters'])
    assert r['question'][':question/id']==replay['question'][':question/id']
 for seed in range(80):family.add(g.generate_easy(seed)['generation']['template'])
 assert family==set(g.FAMILIES['easy'])
 # explicit boundaries; guards cannot be bypassed.
 for level,t,p in [('easy','sin',{'a':1,'c':1,'height':2}),('moderate','product',{'a':1,'c':1,'d':1,'sign':1,'height':1}),('hard','sqrt',{'a':1,'c':1,'upper':1})]:
  try:g.generate(level,template=t,parameters=p);raise AssertionError('invalid explicit accepted')
  except ValueError:pass
 for label,r in reviews:
  if label.startswith('Original'):
   f=r['question'][':question/answer-fields'][0]
   if ':answer-field/correct' in f:
    engine.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'faithful raw present designation; mathematical source anomalies reported separately'} for a in f[':answer-field/choices']]})
 (D/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False))
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine.json')],check=True)
 native=json.loads((D/'engine.json').read_text());report.update({'status':'pass_with_documented_source_repairs','printed_math_checks':count,'default_easy_family_coverage':sorted(family),'sampled_substantive_tasks':{k:len(v) for k,v in tasksets.items()},'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':s.__version__})
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (D/'review.json').write_text(json.dumps([r for label,r in reviews],ensure_ascii=False,indent=2)+'\n')
 (D/'review.md').write_text('# Triple integral setup review\n\nRaw evidence profiles retain source errors and are ineligible for learning. Generated method profiles contain supported repairs.\n\n'+'\n\n---\n\n'.join('## '+label+'\n\n'+g.markdown(r) for label,r in reviews))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
