#!/usr/bin/env python3
"""Fail-closed independent readback, replay, mutation, identity and native checks."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,hashlib,re,copy,subprocess,random
import sympy as s
from functools import lru_cache
H=Path(__file__).parent;ROOT=H.parents[2]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
G=load('kp00877',H.with_suffix('.py'));P=load('kp00877_reader',H/'reference/ode-scalar-parser.py');x,u=P.x,P.u

@lru_cache(maxsize=40000)
def scalar(t):
 t=t.strip().rstrip('.,').replace(r'\displaystyle','').replace(r'\dfrac',r'\frac').replace(r'\textrm{d}',r'\text{d}').replace(r'\mathrm{d}',r'\text{d}').replace(r'\!','')
 return P.scalar(t)
@lru_cache(maxsize=40000)
def same(a,b):return s.simplify(s.expand_log(a-b))==0

def group(t,i):
 assert i<len(t)
 if t[i]!='{':
  m=re.match(r'-?\d+|[a-z]',t[i:]);assert m,(t,i);return m[0],i+len(m[0])
 depth=1;j=i+1
 while depth:
  assert j<len(t);depth+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j

def clean(t):return t.strip().replace(r'{\int }',r'\int').replace(r'\displaystyle','').replace(r'\,','').replace(r'\text{d}',r'\mathrm{d}').replace(r'\textrm{d}',r'\mathrm{d}').replace(r'{|}',r'|').replace('⁡','').strip().rstrip('.,')
DIFF=r'(?:\\(?:text|mathrm|textrm)\{d\}|d)\s*([xu])'
def integral(raw):
 t=clean(raw);i=t.index(r'\int');c=scalar(t[:i])if t[:i].strip()else s.Integer(1);pos=i+4
 while t[pos].isspace():pos+=1
 assert t[pos]=='_';L,pos=group(t,pos+1);assert t[pos]=='^';Hh,pos=group(t,pos+1)
 m=re.search(DIFF,t[pos:]);assert m,t
 body=t[pos:pos+m.start()].strip().removesuffix(r'\cdot');F=scalar(body);var={'x':x,'u':u}[m[1]];end=t[pos+m.end():].strip();assert end=='',end
 return c*F,var,scalar(L),scalar(Hh)
def blocks(t):return [next(v for v in z if v)for z in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',t,re.S)]

@lru_cache(maxsize=4000)
def derive_integral(F,var,L,Hh):
 if F.has(s.Abs(var)):
  assert L>0 or Hh<0,'absolute-value branch must be fixed by the actual original interval'
  F=F.subs(s.Abs(var),var if L>0 else -var)
 # Read denominator and numerator from the actual printed integral. No generator
 # metadata and no generated correct value enter this primitive derivation.
 num,den=s.fraction(F);q=s.cancel(num/s.diff(den,var))
 if den.has(var)and not q.has(var):return q*s.log(den)
 # The radical family's actual denominator is sqrt(T^3). Work on its
 # explicitly certified positive-inner branch using a positive symbol, never
 # force=True or a global branch-erasing power identity.
 for power in den.atoms(s.Pow):
  T=power.base
  if power.exp==3 and T.is_polynomial(var) and s.degree(T,var)==2:
   coeff=s.cancel(num/s.diff(T,var));positive=s.Symbol('_positive_inner',positive=True)
   if not coeff.has(var) and same((F/s.diff(T,var)).subs(T,positive),coeff/positive**s.Rational(3,2)):
    return -2*coeff/s.sqrt(T)
 candidate=s.integrate(F,var)
 assert not candidate.has(s.Integral)and same(s.diff(candidate,var),F),(F,candidate)
 return candidate

def terms(t):
 # Top-level signed additive operands, preserving two endpoint contributions
 # even when SymPy would collect/cancel them to an unchanged total.
 t=clean(t);depth=0;parts=[];start=0
 for i,c in enumerate(t):
  depth+=(c in '({')-(c in ')}')
  if c in '+-'and i>0 and depth==0:parts.append(t[start:i]);start=i
 parts.append(t[start:]);return [scalar(z)for z in parts]

def endpoint_terms(t):
 t=clean(t);depth=0;start=None
 for i,c in enumerate(t):
  if c=='(':
   if depth==0:start=i
   depth+=1
  if c==')':
   depth-=1
   if depth==0 and i==len(t)-1:
    outer=scalar(t[:start])if t[:start]else s.Integer(1)
    ps=terms(t[start+1:i])
    if len(ps)==2:return [outer*v for v in ps]
 ps=terms(t)
 return ps if len(ps)==2 else None

def primitive_bar(t):
 t=clean(t);i=t.index('|_');body=t[:i];L,pos=group(t,i+2);assert t[pos]=='^';Hh,pos=group(t,pos+1);assert not t[pos:]
 return scalar(body),scalar(L),scalar(Hh)

def side_count(sol):
 n=0
 for bk in blocks(sol):
  if r'\int'not in bk:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',bk).replace('&','')
  n+=sum(bool(part.strip().rstrip('.,'))for row in text.split(r'\\')for part in row.split('='))
 return n
CONTRACT={sid:side_count(q.get(':question/worked-solution',''))for sid,q in G.QS.items()}
def readback(q,sid=None):
 prompt=q[':question/problem'];sol=q[':question/worked-solution'];given=next(z for z in blocks(prompt)if r'\int'in z).rstrip('= .')
 F,var,L,Hh=integral(given);assert var==x and L<Hh
 # Independently derive the exact definite value and validate pole-free domain.
 denominator=s.denom(s.cancel(F));roots=s.solveset(denominator,x,domain=s.Interval(L,Hh));assert roots==s.EmptySet,roots
 A=derive_integral(F,x,L,Hh);expected=s.simplify(A.subs(x,Hh)-A.subs(x,L))
 bks=blocks(sol);first=next(z for z in bks if r'\frac{\text{d}u}'in z);rows=re.sub(r'\\(?:begin|end)\{aligned\}','',first).split(r'\\')
 eqs=[z.replace('&','').strip().rstrip('.,').split('=',1)for z in rows]
 assert eqs[0][0].strip()=='u';T=scalar(eqs[0][1]);D=s.diff(T,x)
 assert clean(eqs[1][0])==r'\frac{\mathrm{d}u}{\mathrm{d}x}'and same(scalar(eqs[1][1]),D)
 for left,right in eqs[2:]:
  lm=re.fullmatch(r'(.*?)'+DIFF,clean(left));rm=re.fullmatch(r'(.*?)'+DIFF,clean(right));assert lm and rm
  coeff=lambda v:scalar(v)if v else s.Integer(1)
  operands=lambda m:coeff(m[1])*(D if m[2]=='u'else 1)
  assert same(operands(lm),operands(rm)),('wrong du operands',left,right)
 narrative=re.search(r'using the rule \$u=([^$]+)\$',sol);assert narrative and same(scalar(narrative[1]),T)
 table=next(z for z in bks if z.strip().startswith(r'\begin{aligned}x &'))
 table=re.sub(r'\\(?:begin|end)\{aligned\}','',table);tr=[z.strip().split('&')for z in table.split(r'\\')];assert [z[0].strip()for z in tr]==['x','u']
 xl,xh=map(scalar,tr[0][1:]);ul,uh=map(scalar,tr[1][1:]);assert same(xl,L)and same(xh,Hh)and same(T.subs(x,xl),ul)and same(T.subs(x,xh),uh)
 crit=[L,Hh]+([s.Integer(0)]if L<=0<=Hh else[]);assert min(T.subs(x,z)for z in crit)>0
 def domain_same(a,b):
  difference=a-b
  if L>0 or Hh<0:
   difference=s.refine(difference,s.Q.positive(x)if L>0 else s.Q.negative(x))
  return same(difference.subs(T,s.Symbol('_positive_inner',positive=True)),0)
 count={'formal_integrals':0,'primitive_bars':0,'individual_signed_endpoints':0,'operative_sides':0,'bound_operands':4,'du_relations':len(eqs)-2};primitive=None;checked_endpoints=False
 for bk in bks:
  if r'\int'not in bk:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',bk).replace('&','')
  for row in text.split(r'\\'):
   for side in row.split('='):
    side=side.strip().rstrip('.,')
    if not side:continue
    if r'\int'in side:
     fn,v,lo,hi=integral(side)
     assert same(lo,L if v==x else ul)and same(hi,Hh if v==x else uh),('stale input bound',side)
     actual=fn if v==x else fn.subs(u,T)*D
     assert domain_same(actual,F),('wrong formal integrand',side,actual,F)
     count['formal_integrals']+=1;count['bound_operands']+=2
    elif '|_'in clean(side):
     primitive,lo,hi=primitive_bar(side);assert same(lo,ul)and same(hi,uh);assert domain_same(s.diff(primitive.subs(u,T),x),F)
     value=primitive.subs(u,hi)-primitive.subs(u,lo);assert same(value,expected);count['primitive_bars']+=1;count['bound_operands']+=2
    else:
     actual=scalar(side);assert same(actual,expected),('wrong scalar stage',side,actual,expected)
     if primitive is not None and not checked_endpoints:
      pieces=endpoint_terms(side);assert pieces is not None,('erased endpoint stage',side)
      assert same(pieces[0],primitive.subs(u,uh))and same(pieces[1],-primitive.subs(u,ul)),('wrong individual signed endpoint',side,pieces)
      count['individual_signed_endpoints']+=2;checked_endpoints=True
    count['operative_sides']+=1
 assert count['formal_integrals']>=3 and count['primitive_bars']==1 and checked_endpoints
 if sid and CONTRACT[sid]:assert count['operative_sides']==CONTRACT[sid],('erased or added operative stage',sid,count,CONTRACT[sid])
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']]
 key=f[':answer-field/correct'][1];correct=next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==key)
 assert same(correct,expected),(correct,expected)
 for i,v in enumerate(vals):assert not any(same(v,z)for z in vals[:i])
 return expected,count


def write(name,value): (H/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def main():
 source_cases=[];reviews=[];fidelity=[];raw=[];mutations=[];coverage={};allrecords=[]
 for sid,(level,field,orig)in G.CONFIG.items():
  p=G.parameters(orig);case={'source_id':sid,'difficulty':level,'template':sid,'parameters':p,'bank_profile':'observed'};source_cases.append(case)
  r=G.generate(level,0,template=sid,parameters=p,profile='observed');q=r['question'];answer,counts=readback(q,sid)
  src=G.QS[sid];sf=src[':question/answer-fields'][0];got=[scalar(a[':answer/value'])for a in q[':question/answer-fields'][0][':answer-field/choices']];want=[scalar(a[':answer/value'])for a in sf[':answer-field/choices']]
  assert len(got)==len(want)and all(sum(same(v,z)for z in got)==1 for v in want)
  if ':answer-field/correct'in sf:assert same(answer,scalar(sf[':answer-field/correct'][':answer/value']))
  assert ':question/worked-solution'not in src or all(sentence in q[':question/worked-solution']for sentence in ['We start by changing the variable:','Next, we create a table for the limits of integration using the rule','So, the integral in terms of the new variable is','Finally, we can solve it and get'])
  fidelity.append({'source_id':sid,'bank_matched':len(want),'bank_total':len(want),'original_key_present':':answer-field/correct'in sf,'original_solution_present':':question/worked-solution'in src,'counts':counts,'repair':None if ':question/worked-solution'in src else 'authored missing key and solution, not counted as exact designation/solution replay'})
  raw.append({'source_id':sid,'raw':src,'public_eligible':':question/worked-solution'in src,'reason':None if ':question/worked-solution'in src else 'missing key/solution; supported public completion separate'})
  reviews.append({'label':sid+' original-parameters','record':r});allrecords.append(r)
  seen={r['generation']['math_fingerprint']};variants=[]
  for seed in range(300):
   try:v=G.generate(level,seed,template=sid,profile='observed')
   except ValueError:continue
   if v['generation']['math_fingerprint']in seen:continue
   readback(v['question'],sid);seen.add(v['generation']['math_fingerprint']);variants.append(v)
   if len(variants)==2:break
  assert len(variants)==2,sid
  for i,v in enumerate(variants):reviews.append({'label':sid+' changed '+str(i+1),'record':v});allrecords.append(v)
  # Every rendered operative equality remains necessary, even if its value
  # happens to equal a neighboring stage. Exact expected row shape is checked.
  base=q[':question/worked-solution'];first=G.tex(s.Integer(p['a'])*x**p['n']+p['b'])
  changes=[('wrong u',base.replace('u & ='+first,'u & ='+first+'+1',1)),('wrong du',base.replace(r'\frac{\text{d}u}{\text{d}x} & =',r'\frac{\text{d}u}{\text{d}x} & =9+',1))]
  # Change actual bound and bar independently.
  changes.append(('wrong input bound',base.replace(r'\int_{'+G.tex(p['lo'])+'}',r'\int_{99}',1)))
  changes.append(('stale endpoint',base.replace('|_{','|_{99+',1)))
  # Replace TWO signed endpoint contributions by adding the same nonzero
  # constant to F(upper), F(lower): total unchanged, individual check must fail.
  finalblock=next(b for b in blocks(base)if r'\ln(u)|_'in b or '|_'in b)
  rows=finalblock.split(r'\\');barindex=next(i for i,z in enumerate(rows)if '|_'in z);erow=rows[barindex+1];expr=erow.split('=',1)[1].strip()
  frombar=rows[barindex].split('=',1)[1].strip();pr,ul,uh=primitive_bar(frombar)
  correlated='('+G.tex(pr.subs(u,uh))+'+1)-('+G.tex(pr.subs(u,ul))+'+1)'
  changes.append(('two correlated endpoints',base.replace(erow,erow.split('=',1)[0]+'='+correlated,1)))
  changes.append(('erased equal endpoint stage',base.replace(r'\\'+erow,'',1)))
  for label,sol in changes:
   bad=copy.deepcopy(q);bad[':question/worked-solution']=sol
   try:readback(bad,sid)
   except (AssertionError,ValueError,TypeError,IndexError,StopIteration):mutations.append({'source_id':sid,'mutation':label,'caught':True})
   else:raise AssertionError((sid,'uncaught',label))
 # Slot coverage and genuine mathematical dedup across default templates.
 default_records=[]
 for level in ('easy','moderate','hard'):
  rr=[G.generate(level,seed)for seed in range(75)];[readback(r['question'],r['generation']['template'])for r in rr]
  coverage[level]={'samples':len(rr),'mathematical_tasks':len({r['generation']['math_fingerprint']for r in rr}),'slots':{k:sorted({r['generation']['parameters'][k]for r in rr})for k in G.SLOTS},'profiles':sorted({r['generation']['bank_profile']for r in rr})}
  allrecords+=rr[:4]
  default_records+=rr[:2]
  for i,r in enumerate(rr[:2]):reviews.append({'label':level+' default bank '+str(i),'record':r})
 # Determinism and stable IDs with option permutation.
 for r in allrecords:
  md=r['generation'];a=G.generate(r['question'][':question/difficulty'].split('/')[-1],1234,template=md['template'],parameters=md['parameters'],profile=md['bank_profile']);assert a['question'][':question/id']==r['question'][':question/id'];assert set(a['knowledge_point'])=={'db_id','id','title'}
 write('source-cases.json',source_cases);write('raw-source-replay.json',raw);write('non-ma-inventory.json',{'basis':2275,'entries':[],'count':0});write('review.json',reviews);write('review-cases.json',[dict(label=v['label'],difficulty=v['record']['question'][':question/difficulty'].split('/')[-1],template=v['record']['generation']['template'],parameters=v['record']['generation']['parameters'],bank_profile=v['record']['generation']['bank_profile'])for v in reviews])
 md=[]
 for row in reviews:md.append('## '+row['label']+'\n\n'+G.markdown(row['record']))
 (H/'review.md').write_text('\n\n'.join(md)+'\n')
 write('validation.json',{'status':'mathematics/fidelity passed; native pending','source_banks':len(fidelity),'source_options':sum(v['bank_total']for v in fidelity),'known_keys':sum(v['original_key_present']for v in fidelity),'known_solutions':sum(v['original_solution_present']for v in fidelity),'fidelity':fidelity,'mutations':mutations,'coverage':coverage,'force_branch_erasure':False,'database_writes':0})
 # Native checks batched, foreign/malformed submissions separate from ordinary
 # mathematical wrongs. No valid-output pruning based on grader restrictions.
 engine=ROOT/'generate/runs/current/check-engine';assert hashlib.sha256(engine.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 edge_records=[G.generate('hard',template='q-336745',parameters=p,profile='observed')for p in [dict(n=2,a=1,b=1,c=6,lo=-1,hi=1),dict(n=2,a=3,b=4,c=12,lo=0,hi=2),dict(n=2,a=5,b=-1,c=10,lo=1,hi=2)]]
 fixtures=[]
 for idx,r in enumerate(allrecords[:33]+edge_records+default_records):
  f=r['question'][':question/answer-fields'][0];checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'owned whole-bank choice'}for a in f[':answer-field/choices']]
  else:
   expected,_=readback(r['question']);canonical=f[':answer-field/choices'][0][':answer/value'];checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical exact blank'},{'submitted':G.tex(expected+1),'expected':'rejected','purpose':'ordinary wrong arithmetic'}]
   # Actual uncollected endpoint form derived independently from printed u/table.
   sol=r['question'][':question/worked-solution'];bk=next(b for b in blocks(sol)if '|_'in b);bar=next(row.split('=',1)[1].strip()for row in bk.split(r'\\')if '|_'in row);pr,ul,uh=primitive_bar(bar)
   if pr.has(s.log(u)):
    coeff=s.cancel(pr/s.log(u));alt=G.tex(coeff)+r'(\ln('+G.tex(uh)+r')-\ln('+G.tex(ul)+'))'
    power_alt=G.tex(coeff)+r'\ln(\frac{'+G.tex(uh)+'}{'+G.tex(ul)+'})'
    checks.append({'submitted':power_alt,'expected':'accepted','purpose':'uncollected endpoint log-power quotient equivalent'})
   else:
    coeff=s.simplify(pr*s.sqrt(u));alt=G.tex(coeff)+r'\frac{1}{\sqrt{'+G.tex(uh)+'}}-('+G.tex(coeff)+r'\frac{1}{\sqrt{'+G.tex(ul)+'}})'
   checks.append({'submitted':alt,'expected':'accepted','purpose':'true uncollected signed endpoint equivalent'})
  fixtures.append({'label':str(idx)+' '+r['generation']['template'],'record':r,'checks':checks})
 write('engine-input.json',fixtures)
 # Caller runs the native harness; preserve real failures for diagnosis, then
 # freeze observed outcomes without relabeling unsupported equivalence success.
 print('Independent mathematics, source banks, mutations and variety passed.',flush=True)
 subprocess.run([sys.executable,'-B',str(H/'edge-cases.py')],check=True)
 subprocess.run([sys.executable,'-B',str(H/'native.py')],check=True)
if __name__=='__main__':main()
