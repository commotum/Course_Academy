#!/usr/bin/env python3
"""Independent printed-TeX mathematics, fidelity, shape and native grading QA.

A small recursive parser reads displayed repeated integrals, definite primitive
brackets and arithmetic, not generator parameter/answer metadata. It records
primitive nodes so radial and angular derivatives can also be audited. Source
Unicode application markers and redundant braces are notation only.
"""
import hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
from functools import lru_cache
import sympy as sp
BASE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('polar',BASE.with_suffix('.py'))
g=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(g)
r,t=sp.symbols('r theta',real=True)

def normalize(s):
 s=s.replace('⁡','').replace('π',r'\pi').replace('θ',r'\theta')
 s=re.sub(r'\\operatorname\{(sin|cos|csc|cot)\}',r'\1',s)
 s=re.sub(r'\{(sin|cos|csc|cot)\}',r'\1',s)
 s=re.sub(r'\\(?:textrm|mathrm|text)\s*\{?\s*d\s*\}?\s*(?:\\,)?\s*r','DR',s)
 s=re.sub(r'\\(?:textrm|mathrm|text)\s*\{?\s*d\s*\}?\s*(?:\\,)?\s*\\theta','DT',s)
 s=s.replace('dr','DR').replace(r'd\theta','DT')
 s=re.sub(r'\\(?:left|right|displaystyle|limits)','',s)
 s=s.replace(r'\,','').replace(r'\:','').replace(r'\ ','').replace(r'\cdot','*')
 s=s.replace(r'\dfrac',r'\frac')
 s=re.sub(r'\\(int|frac|sqrt|sin|cos|cot|csc|theta|pi)',r'\1',s)
 s=re.sub(r'\s+','',s).rstrip('.')
 s=s.replace('{int}','int')
 return s

@lru_cache(maxsize=16384)
def printed_integral(f,var,a,b):return sp.integrate(f,(var,a,b))

class Parser:
 def __init__(self,s):
  s=normalize(s)
  self.tokens=re.findall(r'DR|DT|theta|frac|sqrt|sin|cos|cot|csc|int|pi|[0-9]+|[{}()\[\]+*/^_=\-]|r|x',s)
  if ''.join(self.tokens)!=s:raise AssertionError('Unparsed printed TeX: '+repr(s))
  self.i=0;self.primitives=[];self.integrands=[]
 def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
 def pop(self):v=self.peek();self.i+=1;return v
 def need(self,v):assert self.pop()==v,(v,self.tokens,self.i)
 def component(self):
  if self.peek() in ('+','-'):
   sign=self.pop();return (1 if sign=='+' else -1)*self.component()
  if self.peek() in ('{','(','['):
   op=self.pop();end={'{':'}','(':')','[':']'}[op];v=self.expr({end});self.need(end);return v
  return self.atom(postfix=False)
 def atom(self,postfix=True):
  tok=self.pop()
  if tok is None:raise AssertionError('Unexpected end of TeX')
  if tok in ('{','(','['):
   end={'{':'}','(':')','[':']'}[tok];v=self.expr({end});self.need(end)
  elif tok=='frac':v=self.component()/self.component()
  elif tok=='sqrt':v=sp.sqrt(self.component())
  elif tok in ('sin','cos','csc','cot'):
   power=sp.Integer(1)
   if self.peek()=='^':self.pop();power=self.component()
   # Unparenthesized source function argument 2 theta is one complete angle.
   arg=self.component()
   if arg.is_number and self.peek()=='theta':arg*=self.atom(False)
   v=getattr(sp,tok)(arg)**power
  elif tok=='int':
   self.need('_');a=self.component();self.need('^');b=self.component()
   f=self.expr({'DR','DT'});d=self.pop();assert d in ('DR','DT')
   var=r if d=='DR' else t
   self.integrands.append((f,var,a,b))
   v=printed_integral(f,var,a,b)
  elif tok in ('pi','theta','r','x'):v={'pi':sp.pi,'theta':t,'r':r,'x':sp.Symbol('x',real=True)}[tok]
  elif tok.isdigit():v=sp.Integer(tok)
  elif tok in ('+','-'):v=(1 if tok=='+' else -1)*self.atom()
  else:raise AssertionError(('Unexpected token',tok,self.tokens))
  if postfix:
   while self.peek() in ('^','_'):
    op=self.pop();e=self.component()
    if op=='^':v=v**e
    else:
     self.need('^');b=self.component()
     var=r if r in v.free_symbols else t
     self.primitives.append((v,var,e,b))
     v=v.subs(var,b)-v.subs(var,e)
  return v
 def expr(self,stops=set()):
  v=self.atom()
  while self.peek() is not None and self.peek() not in stops:
   tok=self.peek()
   if tok in ('+','-'):
    self.pop();rhs=self.product(stops|{'+','-'});v=v+rhs if tok=='+' else v-rhs
   elif tok in ('*','/'):
    self.pop();rhs=self.atom();v=v*rhs if tok=='*' else v/rhs
   elif tok in ('}',')',']','DR','DT','='):break
   else:v*=self.atom()
  return v
 def product(self,stops):
  v=self.atom()
  while self.peek() is not None and self.peek() not in stops:
   if self.peek() in ('}',')',']','DR','DT','='):break
   if self.peek() in ('*','/'):
    op=self.pop();rhs=self.atom();v=v*rhs if op=='*' else v/rhs
   else:v*=self.atom()
  return v
 def parse(self):
  value=self.expr();assert self.i==len(self.tokens),('Unconsumed',self.tokens[self.i:]);return sp.simplify(value)

@lru_cache(maxsize=16384)
def parse(s):return Parser(s).parse()

@lru_cache(maxsize=16384)
def parse_side(s):
 p=Parser(s);v=p.parse();return v,tuple(p.primitives)
@lru_cache(maxsize=32768)
def equal(a,b):return sp.simplify(sp.trigsimp(a-b))==0

def format_check(s):
 assert s.count('$$')%2==0
 assert len(re.findall(r'(?<!\$)\$(?!\$)',s.replace('$$','')))%2==0
 depth=0
 for i,ch in enumerate(s):
  if ch in '{}':
   if i and s[i-1]=='\\':continue
   depth+=1 if ch=='{' else -1;assert depth>=0
 assert depth==0
 assert '--' not in s and '+-' not in s

def prompt_integral(prompt):
 spans=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S)
 integral=next(s for s in spans if r'\int' in s)
 return integral.rstrip().removesuffix('=').rstrip().rstrip('.')

def check_record(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];format_check(q[':question/problem']);format_check(q[':question/worked-solution'])
 p=Parser(prompt_integral(q[':question/problem']));z=p.parse()
 assert len(p.integrands)==2
 radial=next(v for v in p.integrands if v[1]==r)
 angular=next(v for v in p.integrands if v[1]==t)
 # Integral scale wrapper is outside operator in observed replay. Derivatives
 # of original primitive nodes match unscaled printed integral components.
 for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  if r'\begin{aligned}' in block:
   text=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
   rows=text.split('\\\\')
   for row in rows:
    left,right=row.split('&',1)
    right=right.strip();assert right.startswith('=')
    for side in (left,right[1:]):
     if not side.strip():continue
     v,primitives=parse_side(side);assert equal(v,z),(rec['generation']['template'],side,v,z)
     for primitive,var,a,b in primitives:
      target=radial[0] if var==r else angular[0]
      # Authored source-style coefficient extraction can move a scalar outside
      # the bracket. Read that scalar from the same displayed equality by
      # comparing derivative up to a constant, then verify the full row value.
      ratio=sp.simplify(sp.diff(primitive,var)/target)
      assert var not in ratio.free_symbols and ratio!=0,(primitive,target,ratio)
  else:
   # Standalone identity rows are checked independently at printed arguments.
   text=block.strip().rstrip('.')
   if '=' in text:
    lhs,rhs=text.split('=',1);assert equal(parse(lhs),parse(rhs)),text
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 vals=[];keys=[]
 for a in f[':answer-field/choices']:
  format_check(a[':answer/value']);v=parse(a[':answer/value']);assert v.is_finite
  vals.append(v)
  if a[':answer/id']==f[':answer-field/correct'][1]:keys.append(v)
 assert len(keys)==1 and equal(keys[0],z)
 assert all(not equal(x,y) for i,x in enumerate(vals) for y in vals[i+1:])
 return len(re.findall('\\\\\\\\',q[':question/worked-solution']))

def main():
 source_cases=[{'source_id':n,'template':n,'level':s['level'],'parameters':{'scale':1},'bank_profile':n+'_observed'} for n,s in g.TEMPLATES.items() if n in g.QUESTIONS]
 (BASE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n')
 records=[];matches={'questions':0,'banks':0,'options':0,'distractors':0,'correct_designations':0,'prompts_raw_exact':0,'solutions_raw_exact':0,'solutions_present':0};fidelity=[]
 for case in source_cases:
  n=case['source_id'];rec=g.generate(case['level'],template=n,parameters=case['parameters'],profile=case['bank_profile']);check_record(rec)
  src=g.QUESTIONS[n];q=rec['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  original=[parse(a[':answer/value']) for a in sf[':answer-field/choices']];actual=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
  assert all(sum(equal(v,w) for w in actual)==1 for v in original)
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
  assert q[':question/problem']==src[':question/problem']
  present=':question/worked-solution' in src
  if present:assert q[':question/worked-solution']==src[':question/worked-solution']
  designated=':answer-field/correct' in sf
  if designated:
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(parse(correct[':answer/value']),parse(sf[':answer-field/correct'][':answer/value']))
  matches['questions']+=1;matches['banks']+=1;matches['options']+=5;matches['distractors']+=4 if designated else 0;matches['correct_designations']+=int(designated);matches['prompts_raw_exact']+=1;matches['solutions_raw_exact']+=int(present);matches['solutions_present']+=int(present)
  fidelity.append({'source_id':n,'bank_options_matched':5,'correct_designation':'matched' if designated else 'missing in source; independently authored 7/6','solution':'raw exact' if present else 'missing in source; authored','difficulty':'authored easy assignment' if n=='q-38127' else 'observed'})
  records.append(rec)
 print('Original fidelity passed: all ten banks/prompt layouts and nine supplied solutions.',flush=True)
 # Every complete profile at non-source parameters; two defaults per template.
 profile_records=[];default_records=[]
 for name,s in g.TEMPLATES.items():
  for seed in (41,83):
   rec=g.generate(s['level'],seed,template=name);check_record(rec);default_records.append(rec)
  if name in g.QUESTIONS:
   for scale in (2,3,4,5):
    rec=g.generate(s['level'],seed=scale,template=name,parameters={'scale':scale},profile=name+'_observed');check_record(rec);profile_records.append(rec)
 # Diverse default sampling, each template tested independently. Fixed math and
 # bank IDs survive ordering; different banks get different content IDs.
 task_counts={};positions=set()
 for name,s in g.TEMPLATES.items():
  ids=set()
  print('Checking varied defaults:',name,flush=True)
  for seed in range(24):
   rec=g.generate(s['level'],seed,template=name);check_record(rec);ids.add(rec['generation']['mathematical_fingerprint'])
   fixed=g.generate(s['level'],seed+1000,template=name,parameters=rec['generation']['parameters'],profile=rec['generation']['bank_profile'])
   assert rec['question'][':question/id']==fixed['question'][':question/id']
   f=rec['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
  assert len(ids)>=8,(name,len(ids));task_counts[name]=len(ids)
 assert positions==set(range(5))
 for name,s in g.TEMPLATES.items():
  if s['level']=='hard':
   for invalid in ({'c':1,'A':1,'beta':'pi/4'},{'c':5,'A':1,'beta':'pi/8'},{'c':1,'A':0,'beta':'pi/8'}):
    try:g.generate('hard',template=name,parameters=invalid)
    except ValueError:pass
    else:raise AssertionError('Hard bound guard failed')
 review=records+default_records+profile_records
 (BASE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 text='# Polar repeated integral review\n\nAll records are local author review data. Ten source originals have exact bank/prompt replay; the missing q-38127 solution and level are authored. Generated defaults and scaled observed banks are labeled separately.\n'
 for rec in review:
  origin=rec['generation']['bank_origin'];scale=rec['generation']['parameters'].get('scale')
  label='Original source replay' if scale==1 else 'Generated observed-profile scalar variant' if origin=='observed' else 'Generated authored operation bank'
  text+='\n\n## '+label+'\n\n'+g.markdown(rec)
 (BASE/'review.md').write_text(text)
 engine=[]
 for i,rec in enumerate(review):
  f=rec['question'][':question/answer-fields'][0]
  checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete displayed radio bank'} for a in f[':answer-field/choices']]
  engine.append({'label':str(i)+' '+rec['generation']['template'],'record':rec,'checks':checks})
 (BASE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False)+'\n')
 subprocess.run([str(Path('generate/runs/current/check-engine').resolve()),str(BASE/'engine-input.json'),str(BASE/'engine.json')],check=True)
 report={'status':'pass','database':'math','basis':1356,'source_coverage':matches,'source_fidelity':fidelity,'authored_default_templates':12,'authored_hard_templates':2,'varied_profile_records':len(profile_records),'independently_checked_default_sample_records':12*24+len(default_records),'default_sample_distinct_tasks':task_counts,'radio_correct_positions':sorted(positions),'native_grading':json.loads((BASE/'engine.json').read_text()),'limitations':['q-38127 has no original rating, correct key or worked solution; authored easy/key 7/6/solution are excluded from observed denominators.','Observed banks are homogeneous scalar-pattern replay profiles; their author mistake intent is unresolved. Defaults use separately authored operation banks.','No captured hard practice label exists; hard workload is an authored design grounded in e-7346 and integration prerequisites.']}
 (BASE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='native_grading'},indent=2))
if __name__=='__main__':main()
