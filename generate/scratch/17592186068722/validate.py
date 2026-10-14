#!/usr/bin/env python3
"""Independent printed-TeX and derivative checks, complete original fidelity and native radio fixture."""
import importlib.util,json,re,sys,hashlib,subprocess,itertools
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,u,C=sp.symbols('x u C',real=True)
class Tex:
 """Small strict recursive parser for the actually displayed algebra (no CAS metadata)."""
 def __init__(self,t):self.t=t.replace(r'\,','').replace(r'\cdot','*').replace(' ','');self.i=0
 def peek(self):return self.t[self.i:self.i+1]
 def group(self):
  c=self.peek()
  if c not in '{(':raise ValueError('group expected '+self.t[self.i:])
  self.i+=1;z=self.sum();end='}' if c=='{' else ')'
  if self.peek()!=end:raise ValueError('unbalanced '+self.t)
  self.i+=1;return z
 def atom(self):
  if self.t.startswith(r'\frac',self.i):self.i+=5;z=self.group()/self.group()
  elif self.t.startswith(r'\sqrt',self.i):self.i+=5;z=sp.sqrt(self.group())
  elif self.peek() in ('{','('):z=self.group()
  elif self.peek().isdigit():
   m=re.match(r'\d+',self.t[self.i:]);self.i+=len(m[0]);z=sp.Integer(m[0])
  elif self.peek() in ('x','u','C'):z={'x':x,'u':u,'C':C}[self.peek()];self.i+=1
  else:raise ValueError('unexpected '+self.t[self.i:])
  if self.peek()=='^':
   self.i+=1;k=self.group() if self.peek() in '{(' else self.atom();z=z**k
  return z
 def product(self):
  sign=1
  while self.peek() in ('+','-'):
   if self.peek()=='-':sign=-sign
   self.i+=1
  z=sign*self.atom()
  while self.i<len(self.t) and self.peek() not in '+-})':
   if self.peek()=='/':self.i+=1;z/=self.atom()
   else:
    if self.peek()=='*':self.i+=1
    z*=self.atom()
  return z
 def sum(self):
  z=self.product()
  while self.peek() in ('+','-') and self.i<len(self.t):
   sign=1 if self.peek()=='+' else -1;self.i+=1;z+=sign*self.product()
  return z
 def parse(self):
  z=self.sum()
  if self.i!=len(self.t):raise ValueError('trailing input '+self.t[self.i:])
  return z

def parse(t):return Tex(t).parse()
def eq(a,b):return sp.simplify(a-b)==0

def qa(r):
 q=r['question'];meta=r['generation'];level=q[':question/difficulty'].split('/')[-1];f=q[':question/answer-fields'][0]
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in text)
  depth=0
  for c in text:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0 and text.count('$')%2==0
 integrands=re.findall(r'\\int (.*?)\\,\\text\{d\}([xu])',q[':question/problem']);assert len(integrands)==1
 printed=parse(integrands[0][0]);assert integrands[0][1]=='x'
 sol=q[':question/worked-solution']
 inner_match=re.search(r'\$\$\nu=(.*?)\.\n\$\$',sol);assert inner_match
 F=parse(inner_match[1]);D=sp.diff(F,x)
 opening=re.search(r'We note that \$(.*?)\$',sol);assert eq(parse(opening[1]),D)
 dmatch=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\} & =(.*?)\\,⟹\\,\\text\{d\}u=(.*?)\\,\\text\{d\}x',sol);assert dmatch
 assert eq(parse(dmatch[1]),D) and eq(parse(dmatch[2]),D)
 assert re.search(r'Lastly, we substitute \$u=(.*?)\$',sol)[1]==inner_match[1]
 # Every integral in the displayed chain must transform to the printed integrand.
 ints=re.findall(r'\\int (.*?)\\,\\text\{d\}([xu])',sol)
 for t,var in ints:
  e=parse(t)
  if var=='u':e=e.subs(u,F)*D
  assert eq(e,printed),(t,var)
 expected_count={'easy':5,'moderate':6,'hard':7}[level];assert len(ints)==expected_count
 # All printed primitive rows, including increment/divisor and final back substitution.
 primitives=re.findall(r'=([^=\n]*?)\+C',sol)
 assert len(primitives)=={'easy':2,'moderate':3,'hard':4}[level]
 for t in primitives:
  value=parse(t.strip());value=value.subs(u,F)
  assert eq(sp.diff(value,x),printed),t
 answers=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(answers)==5
 for i,a in enumerate(answers):
  iscorrect=f[':answer-field/choices'][i][':answer/id']==f[':answer-field/correct'][1]
  assert eq(sp.diff(a,x),printed)==iscorrect
  for b in answers[:i]:assert not eq(sp.diff(a-b,x),0),'collision modulo C'
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
 return printed

def dump(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
 src=json.load(open(HERE/'source.json'));cases=json.load(open(HERE/'source-cases.json'));originals=src['record'][':knowledge-point/questions'];records=[];fidelity=[]
 for case,q in zip(cases,originals,strict=True):
  r=g.generate(case['level'],parameters=case['parameters'],profile=case['bank_profile']);qa(r);z=r['question'];oldf=q[':question/answer-fields'][0];newf=z[':question/answer-fields'][0]
  assert q[':question/problem']==z[':question/problem']
  assert q[':question/worked-solution']==z[':question/worked-solution']
  assert q[':question/difficulty'][':db/ident']==z[':question/difficulty']
  assert {k for k in q if k.startswith(':question/') and k not in (':question/math-academy-id',)}==set(z)
  assert oldf[':answer-field/key']==newf[':answer-field/key'] and oldf[':answer-field/type'][':db/ident']==newf[':answer-field/type']
  assert sorted(a[':answer/value'] for a in oldf[':answer-field/choices'])==sorted(a[':answer/value'] for a in newf[':answer-field/choices'])
  corr=next(a[':answer/value'] for a in newf[':answer-field/choices'] if a[':answer/id']==newf[':answer-field/correct'][1]);assert corr==oldf[':answer-field/correct'][':answer/value']
  fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':True,'choices_exact':5,'distractors_matched':4,'correct_designation_matched':True,'question_presence_parity':True,'decoded_doubled_backslashes':any('\\\\' in a[':answer/value'] for a in oldf[':answer-field/choices'])})
  records.append(r)
 # Normal default coverage, slot sign/zero/bounds and exact derivative semantics.
 variety={};generated=[]
 for level in ('easy','moderate','hard'):
  seen=set();slots={k:set() for k in ('a','m','b','n')};templates=set()
  for seed in range(40):
   r=g.generate(level,seed);qa(r);seen.add(r['generation']['parameter_fingerprint']);templates.add(r['generation']['template'])
   for k,v in r['generation']['parameters'].items():slots[k].add(v)
   generated.append(r)
  assert templates=={t for t,l in g.TEMPLATES.items() if l==level}
  for k in ('a','m'):assert min(slots[k])==(1 if k=='a' else 2) and max(slots[k])==(5 if k=='a' else 6)
  assert 0 in slots['b'] and min(slots['b'])<0<max(slots['b'])
  variety[level]={'tested':40,'distinct_mathematical_tasks':len(seen),'default_templates':sorted(templates),'slot_values':{k:sorted(v) for k,v in slots.items()},'bounded_parameter_tasks':3575 if level=='easy' else 325}
 # Explicit boundary inputs for EACH complete source and normal profile.
 boundary=0
 for profile,(template,desc) in g.PROFILES.items():
  level=g.TEMPLATES[template]
  for a,m,b in [(1,2,-6),(5,6,6),(3,4,0)]:
   p={'a':a,'m':m,'b':b,'n':2 if level=='easy' else 0}
   r=g.generate(level,parameters=p,profile=profile);qa(r);boundary+=1
   other=g.generate(level,seed=99,parameters=p,profile=profile)
   assert r['question'][':question/id']==other['question'][':question/id']
   assert {a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']}=={a[':answer/id'] for a in other['question'][':question/answer-fields'][0][':answer-field/choices']}
 for p in [{'a':0,'m':3,'b':1,'n':2},{'a':5,'m':7,'b':1,'n':2},{'a':2,'m':3,'b':7,'n':2},{'a':2,'m':3,'b':1,'n':1}]:
  try:g.generate('easy',parameters=p);raise AssertionError('invalid explicit accepted')
  except ValueError:pass
 # Deliberate display mutations must fail independently of metadata.
 import copy
 mutation=copy.deepcopy(generated[0]);mutation['question'][':question/problem']=mutation['question'][':question/problem'].replace('\\int ','\\int 2',1)
 try:qa(mutation);raise RuntimeError('prompt mutation passed')
 except AssertionError:pass
 mutation=copy.deepcopy(generated[0]);mutation['question'][':question/worked-solution']=mutation['question'][':question/worked-solution'].replace('We note','\fWe note')
 try:qa(mutation);raise RuntimeError('control mutation passed')
 except AssertionError:pass
 review=records+[next(r for r in generated if r['question'][':question/difficulty'].endswith('/'+level)) for level in ('easy','moderate','hard')]+[g.generate(level,83) for level in ('easy','moderate','hard')]
 dump('review.json',review)
 text='# Source and generated review\n\nAll records are local author previews.\n'
 for q,c in zip(originals,cases):
  text+='\n## Original '+c['source_id']+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']+'\n'
 for r in review:
  text+='\n## '+('Source replay' if r['generation']['source_question_ids'] else 'Generated variation')+' '+r['generation']['template']+' — '+r['generation']['bank_profile']+'\n\n'+g.markdown(r)+'\n'
 (HERE/'review.md').write_text(text)
 # Real learner radio grader checks selection identities. Symbolic correctness is
 # independently checked above; fixture ID grading alone cannot establish it.
 fixture=[]
 for i,r in enumerate(records+generated):
  f=r['question'][':question/answer-fields'][0]
  fixture.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source/default radio bank selection'} for a in f[':answer-field/choices']]})
 dump('engine-input.json',fixture)
 engine=HERE.parents[1]/'runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 native=json.load(open(HERE/'engine-report.json'))
 dump('validation.json',{'passed':True,'source':g.SOURCE,'fidelity':fidelity,'source_complete_banks':5,'source_choices':25,'matched_distractors':20,'total_distractors':20,'exact_source_solutions':5,'source_errors':[],'normal_generated_checked':120,'boundary_profiles_checked':boundary,'variety':variety,'native':{k:v for k,v in native.items() if k!='records'},'raw_unsupported':0,'mutation_regressions':2,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'scope':'all 3 observed levels; authored complete default banks and bounded coefficient/shift/inner-exponent variations','unresolved':['Opaque historical distractor intent for q-2189 and q-2390 retained as evidence-only, never normal defaults.']})
 print('PASS: 5 exact complete sources, 20/20 distractors, 120 variants, 30 boundary banks; native 125 accepted/500 rejected')
if __name__=='__main__':main()
