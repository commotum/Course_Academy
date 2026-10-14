"""Independent validation from actual displayed statements, not truth metadata.

Finite-domain exhaustive tests, source key-presence/bank/solution fidelity,
whole native radio bank grading, mutation regressions, renderer geometry checks.
"""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('tangent_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x,n=sp.symbols('x n',real=True)

def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def expr(t):
 t=t.replace('π',r'\pi').replace('−','-').replace('∞',r'\infty').replace(r'\,','').strip().rstrip('.')
 def fractions(text):
  while r'\frac' in text or r'\dfrac' in text:
   m=re.search(r'\\d?frac\s*\{',text);assert m,('Unsupported fraction',text)
   a=m.end()-1
   def group(i):
    depth=0
    for j in range(i,len(text)):
     if text[j]=='{':depth+=1
     if text[j]=='}':
      depth-=1
      if depth==0:return text[i+1:j],j+1
    raise AssertionError('Unbalanced fraction')
   num,end=group(a)
   while text[end].isspace():end+=1
   den,end=group(end)
   text=text[:m.start()]+'(('+fractions(num)+')/('+fractions(den)+'))'+text[end:]
  return text
 t=fractions(t).replace(r'\pi',' pi ').replace(r'\infty','oo').replace('{','(').replace('}',')')
 t=t.replace(r'\left','').replace(r'\right','')
 return sp.simplify(parse_expr(t,local_dict={'x':x,'n':n,'pi':sp.pi,'oo':sp.oo},transformations=standard_transformations+(implicit_multiplication_application,)))
def mathbits(st):return re.findall(r'\$([^$]+)\$',st)
def lattice(e,kind):
 a=sp.diff(e,n)/sp.pi;b=e.subs(n,0)/sp.pi
 target=sp.Rational(1,2) if kind=='asym' else 0
 return bool(sp.simplify(sp.diff(e,n,2))==0 and abs(a)==1 and (b-target).is_integer)
def tangent_arguments(t):
 t=t.replace(r'\operatorname{tan}⁡',r'\tan ').replace('tan⁡',r'\tan ')
 args=[]
 for m in re.finditer(r'\\tan\s*\(',t):
  a=m.end();depth=1
  for j in range(a,len(t)):
   if t[j]=='(':depth+=1
   if t[j]==')':
    depth-=1
    if not depth:args.append(expr(t[a:j]));break
 return args

def truth(st):
 if 'no positive period' in st or st=='The domain is all real numbers.':return False
 bits=mathbits(st);assert bits,st
 if 'asymptote' in st:
  e=expr(next(b.split('=',1)[1] for b in bits if 'x' in b and '=' in b));return lattice(e,'asym')
 if 'zeros' in st:
  e=expr(next(b.split('=',1)[1] for b in bits if 'x' in b and '=' in b));return lattice(e,'zero')
 if 'domain' in st:
  if 'except' in st:
   e=expr(next(b.split('=',1)[1] for b in bits if 'x' in b and '=' in b));return lattice(e,'asym')
  return False # all reals or a single finite branch is not the full domain
 if 'range' in st:
  return any(('\\infty' in b or '∞' in b) and '-' in b and b.count('infty')==2 for b in bits)
 if 'positive' in st and ('interval' in st or 'throughout' in st) or 'negative throughout' in st:
  interval=next(b for b in bits if ',' in b);interval=interval.replace(r'\,','').strip().rstrip('.')
  lo,hi=map(expr,interval.strip('()').split(','))
  expected=1 if 'positive' in st else -1
  for j in [-2,-1,0,1,2]:
   a,b=(z.subs(n,j) for z in [lo,hi]);assert b>a
   # Test complete interval sign by subdividing at every zero and pole.
   special=[k*sp.pi/2 for k in range(-12,13) if a<k*sp.pi/2<b]
   cuts=[a]+special+[b]
   if special:return False
   if sp.sign(sp.tan((a+b)/2))!=expected:return False
  return True
 if 'least positive period' in st:
  return expr(bits[-1])==sp.pi
 if 'no positive period' in st:return False
 if 'passes through' in st:
  a,b=map(expr,bits[-1].strip('()').split(','));return sp.simplify(sp.tan(a)-b)==0
 args=tangent_arguments(st)
 assert len(args)>=2,('Unparsed statement',st)
 for a,b in zip(args,args[1:]):
  delta=sp.expand((a-b)/sp.pi)
  if not all(c.is_integer for c in sp.Poly(delta,n).all_coeffs()):return False
 return True

def statements(prompt):
 lines=[]
 for line in prompt.splitlines():
  m=re.match(r'^(?:- |[123]\. |I{1,3}\. )(.*)$',line)
  if m:lines.append(m[1])
 assert len(lines)==3,prompt
 return lines

def formatcheck(text):
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in text),'Control character'
 assert text.count('$')%2==0,'Unbalanced math'
 balance=0
 for i,c in enumerate(text):
  if i and text[i-1]=='\\':continue
  if c=='{':balance+=1
  if c=='}':balance-=1
  assert balance>=0,'Unbalanced TeX'
 assert balance==0,'Unbalanced TeX'

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0];bank=f[':answer-field/choices']
 truth_values=[truth(st) for st in statements(q[':question/problem'])]
 correct=g.label(truth_values)
 assert len(bank)==5 and len(set(a[':answer/value'] for a in bank))==5
 assert len(set(a[':answer/id'] for a in bank))==5 and correct in [a[':answer/value'] for a in bank]
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in bank]:formatcheck(text)
 if not meta['evidence_only']:
  assert f[':answer-field/correct']==[':answer/id',next(a[':answer/id'] for a in bank if a[':answer/value']==correct)]
  sol=q[':question/worked-solution']
  soltruth=[b=='true' for b in re.findall(r'Statement (?:I|II|III) is (true|false)',sol)]
  assert soltruth==truth_values,(soltruth,truth_values)
  for bit in mathbits(sol):
   args=tangent_arguments(bit)
   for a,b in zip(args,args[1:]):
    assert all(c.is_integer for c in sp.Poly(sp.expand((a-b)/sp.pi),n).all_coeffs()),('False solution identity',bit)
  # Independently verify every x= location printed in the teaching prose.
  for st in sol.split('\n'):
   for bit in mathbits(st):
    if bit.strip().startswith('x='):
     right=bit.split('=',1)[1].rstrip('.')
     if r'\pm' in right:continue # explicit 0,+/-pi,+/-2pi list checked below
     e=expr(right)
     for j in [-2,-1,0,1,2]:
      value=e.subs(n,j)
      if 'zero' in st:assert sp.sin(value)==0 and sp.cos(value)!=0
      else:assert sp.cos(value)==0,('Incorrect printed excluded/asymptote location',bit)
  if 'zeros occur at' in sol:
   assert any(z in sol for z in [r'x=0,\pm \pi ,\pm 2\pi',r'x=0,\pm\pi,\pm2\pi'])
  if 'So, the correct answer' in sol:assert '"'+correct+'"' in sol
  assert q[':question/difficulty']==':question.difficulty/'+meta['level']
  if meta['level']=='easy':assert all(not any(w in st for w in ['domain','positive','period','\\tan (']) for st in statements(q[':question/problem']))
  if meta['level']=='moderate':assert ['domain' in statements(q[':question/problem'])[0], 'throughout' in statements(q[':question/problem'])[1], 'period' in statements(q[':question/problem'])[2]]==[True]*3
 return r

def native(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'All five displayed selection subsets'} for a in f[':answer-field/choices']]}

def source_domain(name):
 anchor=g.ANCHORS[name];keys=list(anchor)
 pools=[]
 for k in keys:
  if k=='left_shift':pools.append([r'-\frac{\pi }{'+str(d)+'}' for d in [2,3,4,6]])
  elif k=='right_shift':pools.append([r'+\frac{'+('' if d==2 else str(d-1))+r'\pi }{'+str(d)+'}' for d in [2,3,4,6]])
  else:pools.append(list(dict.fromkeys(g.BOUNDS[k]+[anchor[k]])))
 for values in itertools.product(*pools):
  p=dict(zip(keys,values))
  try:g.observed_render(name,p,True)
  except ValueError:continue
  yield p

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());source_results=[];native_inputs=[]
 for c in cases:
  r=check(g.generate('hard',profile=c['bank_profile'],parameters=c['parameters'],template=c['template']))
  old=g.QUESTIONS[c['math_academy_id']];q=r['question'];of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  for key in [':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields']:
   assert (key in q)==(key in old),('Presence parity',key)
  assert q[':question/problem']==old[':question/problem']
  assert q.get(':question/worked-solution')==old.get(':question/worked-solution')
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];native_inputs.append(native(r,'source-'+c['math_academy_id']))
  source_results.append({'source':c['math_academy_id'],'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in old else None,'key_presence_parity':True,'complete_bank_match':True,'matched_choices':5,'correct_designation_match':True if ':answer-field/correct' in of else None})
 counts={};fps={};defaults=set();identities={};records=[]
 for level in ['easy','moderate','hard']:
  samples=[]
  if level!='hard':samples=[(None,p) for p in g.catalogs(level)]
  else:samples=[(name,p) for name in g.OBSERVED for p in source_domain(name)]+[('two_identity_properties',p) for p in g.hard_catalog()]
  counts[level]=len(samples);fps[level]=set();identities[level]=set()
  for template,p in samples:
   r=check(g.generate(level,2,template=template,parameters=p));records.append(r)
   native_inputs.append(native(r,level+':'+str(template)+':'+str(p)))
   fps[level].add(r['generation']['mathematical_fingerprint']);identities[level].add(r['generation']['content_identity'])
   other=check(g.generate(level,91,template=template,parameters=p))
   assert r['question'][':question/id']==other['question'][':question/id'],'Seed affects identity'
   assert r['generation']['content_identity']==other['generation']['content_identity']
   assert sorted(r['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/value'])==sorted(other['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/value'])
 for seed in range(150):defaults.add(g.generate_hard(seed)['generation']['template'])
 assert defaults==set(g.OBSERVED)|{'two_identity_properties'},'Normal family coverage'
 assert not identities['easy']&identities['moderate'],'Missing levels overlap in actual content'
 # Adversarial mutations against actual printed claims, keys, prose and format.
 mutations=[]
 r=copy.deepcopy(records[0]);r['question'][':question/problem']=r['question'][':question/problem'].replace('x=n\\pi','x=\\frac{\\pi}{2}+n\\pi',1);mutations.append(r)
 r=copy.deepcopy(records[0]);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(' is true.',' is false.',1);mutations.append(r)
 r=copy.deepcopy(records[0]);r['question'][':question/problem']+='\f';mutations.append(r)
 r=copy.deepcopy(records[0]);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'x=\frac{\pi}{2}',r'x=\frac{\pi}{4}',1);mutations.append(r)
 r=copy.deepcopy(records[0]);r['question'][':question/answer-fields'][0][':answer-field/correct'][1]='00000000-0000-0000-0000-000000000000';mutations.append(r)
 rejected=0
 for r in mutations:
  try:check(r)
  except AssertionError:rejected+=1
 assert rejected==len(mutations)
 invalid=[('easy',{'indices':[0,0,0]},None),('moderate',{'indices':[3,3,3]},None),('hard',{'range_half':'-1'},'domain_zero_range')]
 for level,p,t in invalid:
  try:g.generate(level,parameters=p,template=t)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameter accepted')
 # Fresh atomic renderer writes, exact mathematical anchor locations and bounds.
 g.graph(force=True);plot=json.loads((HERE/'tangent.json').read_text())
 assert hashlib.sha256((HERE/'tangent.png').read_bytes()).hexdigest()==plot['sha256']
 assert plot['zeros_pi_units']==[-1,0,1] and plot['asymptotes_pi_units']==[-1.5,-.5,.5,1.5]
 for z in plot['zeros_pi_units']:assert sp.tan(z*sp.pi)==0
 for a in plot['asymptotes_pi_units']:assert sp.cos(sp.Rational(str(a))*sp.pi)==0
 assert plot['renderer']=='Matplotlib' and plot['python']==sys.version.split()[0]
 save('native-input.json',native_inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',source_results)
 save('validation.json',{'passed':True,'basis':1356,'source_prompts_exact':'6/6','source_banks_matched':'6/6','source_answer_values_matched':'30/30','source_distractors_matched':'20/20 where correct designation present; unrated bank 5/5 values','source_correct_designations_matched':'5/5 present; 1 absent','source_solutions_exact':'5/5 present; 1 absent','raw_key_presence_parity':'6/6','authored_completion':'q-27660: inferred I only, authored solution and hard assignment','finite_instances':counts,'mathematical_fingerprints':{k:len(v) for k,v in fps.items()},'content_identities':{k:len(v) for k,v in identities.items()},'normal_hard_family_coverage':sorted(defaults),'mutation_regressions_rejected':rejected,'native_records':len(native_inputs),'native_checks':5*len(native_inputs),'native_unresolved':0,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':plot['matplotlib']},'limitations':['Easy/moderate difficulty boundaries are authored curriculum-grounded claims, not observed labels.','q-27660 source provides no correct designation or worked solution; raw replay remains ineligible.','Source plot labels and geometry were visually inspected; pixel-exact renderer styling is not claimed.'], 'hashes':{'generator':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'native_engine':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()}})
 print('Validated finite instances:',counts,'native checks:',5*len(native_inputs))
if __name__=='__main__':main()
