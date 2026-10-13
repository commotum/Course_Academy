#!/usr/bin/env python3
"""Printed-math oracle: independent recursive TeX reader; every displayed stage.

The parser understands exact scalar expressions, two basis vectors and their dot
product. It reads actual prompt/solutions, never generation metadata as an oracle.
Native radio grading is then tested separately using the real learning engine.
"""
import importlib.util,json,re,hashlib,subprocess,uuid,sys
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T,X,Y=s.symbols('t x y',real=True);I,J=s.symbols('axis_i axis_j',real=True)
LOC={'t':T,'x':X,'y':Y,'i':I,'j':J,'e':s.E,'pi':s.pi}
FUN={'sin':s.sin,'cos':s.cos,'tan':s.tan,'ln':s.log,'log':s.log,'arctan':s.atan,'atan':s.atan}
class Reader:
 def __init__(self,tex):
  q=tex.replace('⁡','').replace(r'\left','').replace(r'\right','')
  q=re.sub(r'\\operatorname\{(\w+)\}',r'\\\1 ',q)
  q=re.sub(r'\{(sin|cos|tan)\}',r'\\\1 ',q)
  q=re.sub(r'\\text\{[^{}]*\}','',q)
  q=q.replace(r'\,',' ').replace(r'\!','').replace(r'\;','').replace(r'\ ','')
  q=q.replace(' ','').replace('.', '')
  self.tokens=re.findall(r'\\[A-Za-z]+|\d+|[A-Za-z]|[+\-*/^(){}\[\]]',q)
  residue=re.sub(r'\\[A-Za-z]+|\d+|[A-Za-z]|[+\-*/^(){}\[\]]|\s','',q)
  if residue:raise AssertionError(('Unknown printed symbol',tex,residue))
  self.n=0
 def peek(self):return self.tokens[self.n] if self.n<len(self.tokens) else ''
 def take(self):
  q=self.peek();self.n+=1;return q
 def expr(self):
  z=self.product()
  while self.peek() in ('+','-'):
   op=self.take();w=self.product();z=z+w if op=='+' else z-w
  return z
 def starts(self):
  q=self.peek();return bool(q) and (q[0].isdigit() or q in LOC or q[0]=='\\' or q in ('(','{','['))
 def product(self):
  z=self.power()
  while self.peek() in ('*','/',r'\cdot') or self.starts():
   op=self.take() if self.peek() in ('*','/',r'\cdot') else '*'
   w=self.power()
   if op=='/':z=z/w
   elif op==r'\cdot' and z.has(I,J) and w.has(I,J):
    z=s.expand(z).coeff(I)*s.expand(w).coeff(I)+s.expand(z).coeff(J)*s.expand(w).coeff(J)
   else:z=z*w
  return z
 def power(self):
  z=self.atom()
  if self.peek()=='^':self.take();z=z**self.power()
  return z
 def group(self):
  op=self.take();assert op in ('{','(','['),self.tokens
  z=self.expr();assert self.take()=={'{':'}','(':')','[':']'}[op],self.tokens
  return z
 def argument(self):
  if self.peek() in ('{','(','['):
   z=self.group()
   if self.peek()=='^':self.take();z=z**self.power()
   return z
  z=self.power()
  # Bare source function argument: coefficient*variable or implicit xy.
  while self.peek() in ('x','y','t',r'\pi'):
   z=z*self.power()
  return z
 def atom(self):
  q=self.peek()
  if q in ('+','-'):
   self.take();z=self.power();return z if q=='+' else -z
  if q in ('{','(','['):return self.group()
  q=self.take()
  if q.isdigit():return s.Integer(q)
  if q in LOC:return LOC[q]
  if q==r'\pi':return s.pi
  if q==r'\frac':return self.group()/self.group()
  if q==r'\sqrt':return s.sqrt(self.group())
  if q.startswith('\\') and q[1:] in FUN:
   power=1
   if self.peek()=='^':self.take();power=self.group() if self.peek()=='{' else self.atom()
   return FUN[q[1:]](self.argument())**power
  raise AssertionError(('Unknown TeX atom',q,self.tokens,self.n))
@lru_cache(None)
def parse(z):
 reader=Reader(z);result=reader.expr();assert reader.n==len(reader.tokens),(z,reader.tokens[reader.n:]);return result

def eq(a,b):
 z=a-b
 if z==0:return True
 positive=s.Symbol('positive_t',positive=True)
 return s.simplify(s.trigsimp(z.subs(T,positive)))==0

def vec(z):
 z=s.expand(parse(z));a,b=z.coeff(I),z.coeff(J)
 assert eq(z,a*I+b*J),('Not a complete basis vector',z)
 return a,b

def format_check(text):
 assert text.count('$$')%2==0
 inline=re.sub(r'\$\$.*?\$\$','',text,flags=re.S);assert inline.count('$')%2==0
 depth=0
 for c in text:
  depth+=(c=='{')-(c=='}');assert depth>=0
 assert depth==0
 assert '--' not in text and '+-' not in text

def rhs_rows(block):
 q=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
 return q.split(' & =',1)[1].split(r' \\  & =')

def split_sub(z):
 """Read supplied-coordinate substitution notation from actual printed math."""
 m=re.search(r'\\Big\|_\{([xy]|t)=',z)
 if not m:return None
 base=z[:m.start()];tail=z[m.end():-1]
 if m[1]=='t':return parse(base).subs(T,parse(tail))
 a,b=tail.split(r',\,y=');return parse(base).subs({X:parse(a),Y:parse(b)},simultaneous=True)

def equals_parts(z):
 parts=[];start=0;depth=0
 for n,c in enumerate(z):
  depth+=(c=='{')-(c=='}')
  if c=='=' and depth==0:parts.append(z[start:n]);start=n+1
 parts.append(z[start:]);return parts

def scalar(z):
 q=split_sub(z);return q if q is not None else parse(z)

MATH_CHECKS=0
def check(record):
 global MATH_CHECKS
 MATH_CHECKS+=1
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==17592186124593
 q=record['question'];p=q[':question/problem'];sol=q[':question/worked-solution']
 raw_error=record['generation'].get('raw_math_error',False)
 if raw_error:
  assert record['generation']['evidence_only'] and not record['generation']['eligible_for_learning']
  assert ')i)' in sol
  sol=sol.replace(')i)',')j)')
 format_check(p);format_check(sol)
 uuid.UUID(q[':question/id'])
 grad=re.search(r'\$∇f\(x,y\)=(.*?)\$',p,re.S)[1];curve=re.search(r'\$r\(t\)=(.*?)\$',p,re.S)[1]
 point=parse(re.search(r'at \$t=(.*?)\$',p)[1]);G=vec(grad);R=vec(curve)
 C=tuple(s.simplify(s.trigsimp(z.subs({X:R[0],Y:R[1]},simultaneous=True))) for z in G)
 V=tuple(s.diff(z,T) for z in R)
 expected=s.simplify(s.trigsimp(sum(C[n]*V[n] for n in range(2))));answer=s.simplify(s.trigsimp(expected.subs(T,point)))
 if raw_error:
  rawblocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
  rawdot=rhs_rows(rawblocks[4])[1]
  assert not eq(parse(rawdot),expected),('Raw source error accidentally repaired',rawdot)
 if record['generation']['evidence_only']:assert not record['generation']['eligible_for_learning']
 else:assert record['generation']['eligible_for_learning']
 prose=sol[sol.index('First, we substitute'):sol.index('Now, we calculate')]
 for symbol,expected_input in [('x',R[0]),('y',R[1])]:
  actual_input=re.search(r'\$'+symbol+r'=(.*?)\$',prose)[1]
  assert eq(parse(actual_input),expected_input),('Stale prose coordinate',actual_input,R)
 prose_point=re.search(r'Finally, evaluating the above at \$t=(.*?),\$',sol)[1]
 assert eq(parse(prose_point),point),('Stale evaluation prose',prose_point,point)
 # Supplied gradient is integrable, and all source/generated evaluation domains.
 assert eq(s.diff(G[0],Y),s.diff(G[1],X))
 assert not answer.has(s.nan,s.zoo,s.oo,-s.oo)
 bb=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(bb)==6
 assert bb[0]==g.FORMAL
 gr=bb[1].split('=',1)[1];assert all(eq(a,b) for a,b in zip(vec(gr),G)),('gradient supplied',gr,G)
 cr=rhs_rows(bb[2])
 for row in cr:
  z=split_sub(row)
  v=(s.expand(z).coeff(I),s.expand(z).coeff(J)) if z is not None else vec(row)
  assert all(eq(a,b) for a,b in zip(v,C)),('composition stage',row,v,C)
 dr=rhs_rows(bb[3]);assert len(dr)==2
 # Parse complete ordered derivative-operator components, including nested args.
 operator=r'\frac{\text{d}}{\text{d}t}'
 operands=dr[0].split(operator);assert len(operands)==3
 a=operands[1].rsplit(r'\,i',1)[0].rstrip('+ ');b=operands[2].rsplit(r'\,j',1)[0]
 assert eq(parse(a),R[0]) and eq(parse(b),R[1]),('derivative arguments',a,b,R)
 assert all(eq(a,b) for a,b in zip(vec(dr[1]),V)),('velocity',dr,V)
 rows=rhs_rows(bb[4]);assert rows[0]==r'∇f(r(t))\cdot {r}^{′}(t)'
 for row in rows[1:]:
  assert eq(parse(row),expected),('chain stage',row,parse(row),expected)
 # The vector factors in the dot product must contain both correct basis terms.
 dl,dd=rows[1].split(r'\cdot',1) if record['generation']['origin'].startswith('authored') else (None,None)
 if dl is not None:
  assert all(eq(a,b) for a,b in zip(vec(dl),C)) and all(eq(a,b) for a,b in zip(vec(dd),V))
 if record['generation']['template'] in ('coupled_trig','product_exp'):
  assert all(len(s.Add.make_args(z))==2 for z in G),('Hard coupled workload removed',G)
 # Every point-substitution/evaluation/reduction stage is read from print.
 er=rhs_rows(bb[5])
 for row in er:
  for part in equals_parts(row):
   if r'\Big|' in part:actual=scalar(part)
   else:actual=parse(part)
   assert eq(actual,answer),('evaluation stage',part,actual,answer)
 for phrase in ('The chain rule in vector form states that','In addition, we\'ve been given that','First, we substitute','Now, we calculate the derivative','Applying the chain rule, we get','Finally, evaluating the above at'):
  assert phrase in sol
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5
 assert not any(eq(z,w) for n,z in enumerate(vals) for w in vals[n+1:])
 correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
 ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(set(ids))==5
 for z in ids:uuid.UUID(z)
 assert sum(eq(z,answer) for z in vals)==1 and eq(vals[ids.index(correct[1])],answer)
 if not record['generation']['evidence_only']:
  gx,gy=[s.simplify(z.subs(T,point)) for z in C];vx,vy=[s.simplify(z.subs(T,point)) for z in V]
  A,B=gx*vx,gy*vy
  operations={'correct':A+B,'omit_x':B,'omit_y':A,'reverse_x':-A+B,'reverse_y':A-B,'omit_dx':gx+B,'omit_dy':A+gy,'omit_both_velocities':gx+gy,'sum_velocity':vx+vy,'subtract_y':A-B,'negative_dot':-A-B,'product_terms':A*B,'sum_gradient':gx+gy,'position_dot':gx*R[0].subs(T,point)+gy*R[1].subs(T,point),'second_derivative_dot':gx*s.diff(R[0],T,2).subs(T,point)+gy*s.diff(R[1],T,2).subs(T,point),'swapped_velocity':gx*vy+gy*vx,'gradient_norm_squared':gx**2+gy**2}
  required=[operations[k] for k in record['generation']['operations']]
  assert len(required)==5 and all(sum(eq(z,w) for w in vals)==1 for z in required),('Printed operation-bank mismatch',record['generation']['operations'])
 return vals

def main():
 fidelity=[];cases=[];reviews=[];replays=[];count=0;unique={l:set() for l in ('easy','moderate','hard')}
 for name,source in g.BY_TEMPLATE.items():
  level=g.TEMPLATES[name];profile=('raw_observed_' if name=='sqrt_product' else 'observed_')+source[':question/math-academy-id'];p={'c':1,'time_scale':1}
  r=g.generate(level,template=name,parameters=p,profile=profile);check(r);replays.append(r)
  q=r['question'];f=q[':question/answer-fields'][0];orig=source[':question/answer-fields'][0]
  bank=[a[':answer/value'] for a in orig[':answer-field/choices']];out=[a[':answer/value'] for a in f[':answer-field/choices']]
  assert sorted(bank)==sorted(out)
  assert q[':question/problem']==source[':question/problem'],(name,'prompt')
  expected_sol=source[':question/worked-solution']
  if name=='sqrt_product':
   normal=g.generate(level,template=name,parameters=p,profile='observed_q-94878');check(normal)
   assert normal['question'][':question/worked-solution']==expected_sol.replace(r'(-\frac{1}{\sqrt{t}})i)',r'(-\frac{1}{\sqrt{t}})j)')
   reviews.append({'kind':'Supported normal solution repair; observed bank remains evidence-only','record':normal})
  assert q[':question/worked-solution']==expected_sol,(name,'complete solution stage/prose fidelity')
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert eq(parse(correct),parse(orig[':answer-field/correct'][':answer/value']))
  fidelity.append({'source_id':source[':question/id'],'math_academy_id':source[':question/math-academy-id'],'template':name,'profile':profile,'prompt_raw_exact':True,'bank_raw_exact':True,'correct_designation_matched':True,'solution_raw_exact':True,'normal_solution_raw_exact':name!='sqrt_product','solution_after_math_repair_exact':True,'choices_matched':5})
  cases.append({'source_id':source[':question/id'],'source_db_id':source[':db/id'],'math_academy_id':source[':question/math-academy-id'],'difficulty':level,'template':name,'parameters':p,'bank_profile':profile})
  # Every observed bank exercised beyond original values, all stages preserved.
  for c,k in ((2,1),(1,2),(3,3)):
   rr=g.generate(level,seed=11,template=name,parameters={'c':c,'time_scale':k},profile=profile);check(rr);count+=1
   reviews.append({'kind':'Generated observed bank scaling/dilation; unresolved error interpretations','record':rr})
 for name,l in g.TEMPLATES.items():
  print('Checking '+name,flush=True)
  for seed in range(4):
   r=g.generate(l,seed,template=name);check(r);count+=1;unique[l].add(r['generation']['mathematical_fingerprint'])
   pp=r['generation']['parameters'];profile=r['generation']['bank_profile'];rr=g.generate(l,seed+999,template=name,parameters=pp,profile=profile)
   assert r['question'][':question/id']==rr['question'][':question/id']
   if seed<2:reviews.append({'kind':'Generated authored default; missing hard scope is an authored claim' if l=='hard' else 'Generated parameter and complete operation-bank extension','record':r})
 # Content IDs respond to banks but seed/order do not; canonical task ignores bank.
 for name,l in g.TEMPLATES.items():
  for seed in range(2):
   r=g.generate(l,seed+301,template=name);check(r)
   p=r['generation']['parameters'];banks=[]
   for profile in g.OPERATIONS:
    try:rr=g.generate(l,7,template=name,parameters=p,profile=profile)
    except ValueError:continue
    check(rr);banks.append(rr)
   assert len({z['generation']['mathematical_fingerprint'] for z in banks})==1
   assert len({z['question'][':question/id'] for z in banks})==len(banks)
 # Invalid explicit parameters/profiles/fields cannot be silently changed.
 invalid=[('easy','log_rational',{'a':1,'b':3,'d':1,'e':1,'point':'3'}),('hard','coupled_trig',{'a':1,'b':2,'d':2,'k':1,'point':'pi/4'}),('moderate','sqrt_product',{'a':1,'b':1,'d':2,'point':'pi/4'}),('easy','sqrt_sine',{'a':1,'b':1,'d':1,'point':'-pi'}),('easy','exp_cancel',{'a':0,'b':1,'d':1,'point':'1'})]
 for l,n,p in invalid:
  try:g.generate(l,template=n,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('Invalid accepted',l,n,p))
 engine=[]
 for i,r in enumerate(replays+[a['record'] for a in reviews]):
  f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
  engine.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Native choice grading; actual printed mathematics checked separately'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
 binary=HERE.parents[1]/'runs/current/check-engine'
 subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
 md=['# Source and generated review','8 practice sources; 6 easy, 2 moderate. All 40 options and all source stages preserved; q-94878 has one supported basis-vector repair.']
 for source,r in zip(g.BY_TEMPLATE.values(),replays):
  md+=['## Original '+source[':question/math-academy-id'],source[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in source[':question/answer-fields'][0][':answer-field/choices']),source[':question/worked-solution'],('## Public raw erroneous source replay — evidence-only' if source[':question/math-academy-id']=='q-94878' else '## Parameterized source replay — evidence-only'),g.markdown(r)]
 for a in reviews:md+=['## '+a['kind'],g.markdown(a['record'])]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'status':'pass','version':g.VERSION,'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'practice_sources':8,'observed_levels':{'easy':6,'moderate':2,'hard':0},'source_banks_matched':8,'source_choices_matched':40,'source_choices_total':40,'source_correct_designations_matched':8,'raw_exact_prompts':8,'raw_exact_banks':8,'raw_exact_solutions':8,'normal_raw_exact_solutions':7,'mathematically_repaired_solutions':1,'complete_solutions_after_repair':8,'fidelity':fidelity,'printed_math_checks':MATH_CHECKS,'source_mathematical_error_count':1,'known_source_math_errors':['q-94878: explicit dot-product velocity has i in both components; public raw replay is ineligible, normal replay repairs second basis to j.'],'unique_sample_tasks':{z:len(v) for z,v in unique.items()},'native_grading':json.loads((HERE/'engine-report.json').read_text()),'script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'known_limits':['Source wrong scalar-operation interpretations are underdetermined; explicit observed profiles offer only coherent gradient scaling and time dilation, while default authored parameterization varies gradient/curve/point coefficients.','Hard has no observed sources; two same-KP supplied-gradient families are authored and anchored in route/canonical/prerequisites.','Opaque source banks are evidence_only=true and eligible_for_learning=false; raw_observed_q-94878 additionally preserves its known erroneous dot row.','Source point evaluation LHS notation is retained literally for observed fidelity; authored solutions use an explicit evaluation bar.'],'unresolved_findings':[],'plot_rating':'none','database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('fidelity','native_grading')},indent=2))
if __name__=='__main__':main()
