#!/usr/bin/env python3
"""Read actual learner TeX independently; check every component and whole bank.
Historical profiles are checked for fidelity separately from learning eligibility.
Native radio checks invoke the existing memory-only application grader.
"""
from functools import lru_cache
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gen',BASE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T,X,Y,Z,U=g.T,g.X,g.Y,g.Z,g.U
I,J,K,A,B=sp.symbols('i j k a b', real=True)

class Tex:
 def __init__(self,text):
  text=text.replace('⁡','').replace('π',r'\pi ').replace('−','-')
  for name in ['sin','cos','ln']:
   text=text.replace(r'\operatorname{'+name+'}', '\\'+name+' ')
  for token in (r'\left',r'\right',r'\,',r'\:',r'\ ',r'\qquad',r'\displaystyle'):text=text.replace(token,'')
  self.ts=re.findall(r'\\[A-Za-z]+|\d+|[a-zA-Z]|[^\s]',text);self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
 def pop(self):t=self.peek();self.i+=1;return t
 def group(self):
  op=self.pop();cl={'{':'}','(':')','[':']'}[op];val=self.expr();assert self.pop()==cl,(self.ts,self.i,cl);return val
 def atom(self):
  t=self.peek()
  if t in ('+','-'):
   self.pop();return self.atom()*(1 if t=='+' else -1)
  if t in ('{','(','['):v=self.group()
  elif t==r'\frac':self.pop();v=self.group()/self.group()
  elif t==r'\sqrt':self.pop();v=sp.sqrt(self.group())
  elif t in (r'\sin',r'\cos',r'\ln',r'\log',r'\exp'):
   self.pop();v={r'\sin':sp.sin,r'\cos':sp.cos,r'\ln':sp.log,r'\log':sp.log,r'\exp':sp.exp}[t](self.atom())
  elif t and t.isdigit():self.pop();v=sp.Integer(t)
  elif t in ('x','y','z','t','u','i','j','k','a','b',r'\pi','e'):
   self.pop();v={'x':X,'y':Y,'z':Z,'t':T,'u':U,'i':I,'j':J,'k':K,'a':A,'b':B,r'\pi':sp.pi,'e':sp.E}[t]
  else:raise AssertionError(('unsupported TeX token',t,self.ts))
  if self.peek()=='^':self.pop();v=v**self.atom()
  return v
 def product(self):
  v=self.atom()
  while self.peek() not in (None,'+','-','}',')',']',',','.',':','=','?'):
   op=self.peek()
   if op in (r'\cdot','*'):self.pop();v*=self.atom()
   elif op=='/':self.pop();v/=self.atom()
   else:v*=self.atom()
  return v
 def expr(self):
  v=self.product()
  while self.peek() in ('+','-'):
   sign=-1 if self.pop()=='-' else 1;v+=sign*self.product()
  return v
 def parse(self):
  v=self.expr();assert self.peek() is None,('unconsumed',self.ts[self.i:]);return v

def expr(s):return Tex(s.strip().rstrip('.,?')).parse()
def equal(a,b):
 if a==b:return True
 if a.has(sp.Integral) or b.has(sp.Integral):
  ai=list(a.atoms(sp.Integral));bi=list(b.atoms(sp.Integral))
  if len(ai)==len(bi)==1 and ai[0].limits==bi[0].limits:
   ca=sp.cancel(a/ai[0]);cb=sp.cancel(b/bi[0])
   if equal(ca*ai[0].function,cb*bi[0].function):return True
  return equal(evaluated(a),evaluated(b)) if evaluated(a)!=a and evaluated(b)!=b else False
 return sp.simplify(sp.expand_trig(a-b))==0

def takegroup(s,i):
 assert s[i]=='{',(s,i);start=i+1;depth=1;i+=1
 while depth:
  if s[i]=='{':depth+=1
  if s[i]=='}':depth-=1
  i+=1
 return s[start:i-1],i

def integral(s,var=T):
 s=s.strip().rstrip('.').replace(r'{\int }',r'\int').replace(r'\displaystyle','')
 idx=s.index(r'\int_');coef=s[:idx];coef=coef.strip().rstrip(r'\,');coef=expr(coef) if coef else sp.Integer(1)
 tail=s[idx+len(r'\int_'):];lo,pos=takegroup(tail,0);assert tail[pos]=='^';hi,pos=takegroup(tail,pos+1)
 body=tail[pos:];body=re.sub(r'\\(?:text|textrm)\{d\}', 'd',body);body=re.sub(r'\s*(?:\\,)?\s*d[t u]\s*$', '',body);body=body.strip().removesuffix(r'\cdot').strip()
 return coef,expr(body),expr(lo),expr(hi)
def value(s):
 if r'\int' not in s:return expr(s)
 c,f,lo,hi=integral(s,U if re.search(r'd\}u\s*$',s) else T)
 var=U if f.has(U) else T
 return c*sp.Integral(f,(var,lo,hi))
@lru_cache(maxsize=4096)
def evaluated(e):
 try:return sp.simplify(e.doit())
 except Exception:return e

def formatting(s):
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in s),'C0 control character'
 dep=0
 for i,c in enumerate(s):
  if c not in '{}':continue
  if i and s[i-1]=='\\':continue
  dep+=1 if c=='{' else -1;assert dep>=0
 assert dep==0,'unbalanced braces'
 assert s.count('$$')%2==0 and s.replace('$$','').count('$')%2==0,'math delimiter'
 assert '+-' not in s and '--' not in s,'unparenthesized signed factor'

def prompt_math(rec):
 s=rec['question'][':question/problem'];coords=re.findall(r'\$\(([-\d, ]+)\)',s);assert len(coords)==2
 a,b=[[int(x) for x in v.split(',')] for v in coords];r=[sp.Integer(v)+(w-v)*T for v,w in zip(a,b)];d=[w-v for v,w in zip(a,b)]
 if 'function $' in s:F=re.search(r'f\(x,\s*y,\s*z\)\s*=\s*(.*?)\$',s)[1].rstrip(',')
 else:
  F=s.split('integral $',1)[1].split('$',1)[0];F=F.replace(r'{\int }_{C}','').replace(r'\displaystyle \int_(C)','');F=re.sub(r'(?:\\,\\text\{d\}s|ds)$','',F)
 f=expr(F);h=sp.simplify(f.subs({X:r[0],Y:r[1],Z:r[2]},simultaneous=True));speed=sp.sqrt(sum(v*v for v in d))
 prim=sp.integrate(h,T) if rec['generation']['template'] not in ('exponential','cosine','sine') else (sp.exp(sp.expand(r[1]*r[2])) if rec['generation']['template']=='exponential' else (sp.sin(sp.pi*(r[0]+r[2])/4)/(sp.pi*(d[0]+d[2])/4) if rec['generation']['template']=='cosine' else -sp.cos(sp.pi*r[1]/4)/(sp.pi*d[1]/4)))
 assert equal(sp.diff(prim,T),h)
 ans=sp.simplify(speed*(prim.subs(T,1)-prim.subs(T,0)))
 return a,b,r,d,f,h,speed,prim,ans

def rows(block):
 block=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
 return [v.strip().rstrip('.') for v in re.split(r'\\\\\s*',block)]
def rhs(row):return re.split(r'&\s*=',row,maxsplit=1)[1].strip().rstrip('.')
def vece(v):return sum(q*c for q,c in zip(v,(I,J,K)))
def derivative_expr(s,r,d):
 for v,c in zip(d,'xyz'):
  s=s.replace(r'\frac{\text{d}'+c+r'}{\text{d}t}',g.tex(sp.Integer(v)))
 marker=r'\frac{\text{d}}{\text{d}t}'
 while marker in s:
  start=s.index(marker);pos=start+len(marker);assert s[pos]=='('
  depth=1;end=pos+1
  while depth:
   if s[end]=='(':depth+=1
   if s[end]==')':depth-=1
   end+=1
  deriv=sp.diff(expr(s[pos+1:end-1]),T)
  s=s[:start]+'('+g.tex(deriv)+')'+s[end:]
 return expr(s)

def endpoint_stage(s):
 # Bracket evaluation of each displayed primitive at the actual bounds.
 s=s.replace(r'\left','').replace(r'\right','')
 if '[' in s and r']_{' in s:
  start=s.index('[');end=s.index(r']_{');co=expr(s[:start]);body=expr(s[start+1:end]);lo,pos=takegroup(s,end+2);assert s[pos]=='^';hi,pos=takegroup(s,pos+1);assert pos==len(s)
  return co*(body.subs(T,expr(hi))-body.subs(T,expr(lo)))
 # Source exponent/trig evaluation-bar row.
 marker=r'\,{|}_'
 if marker in s:
  body,bounds=s.split(marker);lo,pos=takegroup(bounds,0);assert bounds[pos]=='^';hi,pos=takegroup(bounds,pos+1);assert pos==len(bounds)
  primitive=expr(body);return primitive.subs(U,expr(hi))-primitive.subs(U,expr(lo))
 return None

def check_solution(rec):
 a,b,r,d,F,h,speed,prim,ans=prompt_math(rec);family=rec['generation']['template'];raw=rec['generation']['evidence_only']
 text=rec['question'].get(':question/worked-solution')
 if text is None:assert raw and family in ('sum','sine');return
 formatting(text)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S);assert len(blocks)==(6 if family in ('exponential','cosine','sine') else 5)
 assert 'f(x,y,z)='+g.FUNCTION_TEX[family] in text
 # First block remains the same scalar arc-length formula.
 assert blocks[0]==r'{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,'
 param=rows(blocks[1]);assert len(param)==4
 for row in param:
  v=expr(rhs(row)).subs({A:vece(a),B:vece(b)})
  assert equal(v,vece(r)),('parametrization',row)
 # Read prose coordinates, not generation metadata.
 pp=re.search(r'Thus, we have that \$x=(.*?)\$.*?\$y=(.*?)\$.*?\$z=(.*?)\$',text,re.S).groups()
 assert all(equal(expr(v),q) for v,q in zip(pp,r))
 dr=rows(blocks[2]);assert len(dr)==(7 if family in ('quotient','cosine') else 6)
 for row in dr[:3]:assert equal(derivative_expr(rhs(row),r,d),vece(d)),('printed derivative',row)
 for row in dr[3:]:assert equal(derivative_expr(rhs(row),r,d),speed),('speed',row)
 pull=rows(blocks[3]);assert len(pull)==(3 if family=='quotient' else 4 if family=='polynomial' and not raw else 2)
 for row in pull:assert equal(expr(rhs(row)),h),('pullback stage',row)
 if family=='polynomial':
  assert '^{2}' in rhs(pull[0]) and rhs(pull[0]).count('(')>=2
  if not raw:
   assert rhs(pull[1]).count('(')>=4 and rhs(pull[2]).count('(')>=6,'squared expansion and distinct distributed products required'
   # Independent structural regression: collected algebra cannot replace distribution.
   assert rhs(pull[2]).count(')(')>=3,'each expanded square term multiplies actual x(t)'
 integ=rows(blocks[4]);assert len(integ)==(6 if family=='polynomial' else 3)
 for j,row in enumerate(integ):
  s=rhs(row)
  if j==0:
   assert s==r'{\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t';continue
  endpoint=endpoint_stage(s)
  v=endpoint if endpoint is not None else evaluated(value(s))
  assert equal(v,ans),('integral/primitive/endpoint',row,v,ans)
 if family=='polynomial':
  primitive=rhs(integ[3]);body=primitive.split('[')[1].split(r'\right]')[0]
  assert equal(sp.diff(expr(body),T),h),'displayed primitive'
  # Every signed endpoint component separately checked against derivative-derived polynomial.
  ep=rhs(integ[4]);expected_parts=[c*T**e[0] for e,c in sp.Poly(prim,T).terms()]
  actual_upper=re.search(r'^.*?\((.*?)\)-',ep)[1]
  upper=[expr(v) for v in re.findall(r'\(([^()]*)\)',actual_upper)]
  assert len(upper)==len(expected_parts)
  assert all(equal(v,w.subs(T,1)) for v,w in zip(upper,expected_parts))
  lower=re.findall(r'\(([^()]*)\)',ep.split(')-',1)[1]);assert len(lower)==len(expected_parts)
  assert all(equal(expr(v),w.subs(T,0)) for v,w in zip(lower,expected_parts))
 if family in ('exponential','cosine','sine'):
  m=re.search(r'substitution \$u=(.*?)\$, \$(.*?)\$ as follows',text).groups()
  arg=expr(m[0]);du=m[1].removeprefix(r'\text{d}u=').removesuffix(r'\,\text{d}t');der=expr(du)
  intended=r[1]*r[2] if family=='exponential' else sp.pi*(r[0]+r[2] if family=='cosine' else r[1])/4
  assert equal(arg,intended) and equal(der,sp.diff(arg,T))
  if family=='exponential':assert equal(r[0],sp.diff(r[1]*r[2],T))
  sub=rows(blocks[5]);assert len(sub)==5
  for row in sub:
   s=rhs(row);ev=endpoint_stage(s);v=ev if ev is not None else evaluated(value(s));assert equal(v,ans),('substitution or evaluated endpoint',row,v,ans)
  # Independently compare the two endpoint terms, not only their difference.
  endpoint_terms=rhs(sub[2])
  if family=='exponential':
   es=re.findall(r'\{e\}\^\{([^{}]*)\}',endpoint_terms);assert len(es)==2
   assert equal(expr(es[0]),arg.subs(T,1)) and equal(expr(es[1]),arg.subs(T,0))
  elif family=='cosine':
   es=re.findall(r'\\operatorname\{sin\}⁡\((.*?)\)',endpoint_terms);assert len(es)==2
   assert equal(expr(es[0]),arg.subs(T,1)) and equal(expr(es[1]),arg.subs(T,0))
 return ans

def check_record(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];formatting(q[':question/problem']);a,b,r,d,F,h,s,primitive,ans=prompt_math(rec)
 assert a==rec['generation']['parameters']['a'] and b==rec['generation']['parameters']['b']
 fld=q[':question/answer-fields'][0];assert fld[':answer-field/type']==':answer-field.type/radio'
 vals=[]
 for option in fld[':answer-field/choices']:
  formatting(option[':answer/value']);vals.append(evaluated(value(option[':answer/value'])))
 assert len(vals)==5 and len({v[':answer/id'] for v in fld[':answer-field/choices']})==5
 raw=rec['generation']['evidence_only']
 if not raw:
  assert all(v.is_real is not False and not v.has(sp.oo,-sp.oo,sp.zoo,sp.nan,sp.Integral) for v in vals),'complete real bank'
  for i in range(5):
   for j in range(i):assert not equal(vals[i],vals[j]),'whole-value answer collision'
  correct=fld[':answer-field/correct'][1];index=next(i for i,v in enumerate(fld[':answer-field/choices']) if v[':answer/id']==correct)
  assert equal(vals[index],ans)
  assert q[':question/difficulty']==':question.difficulty/'+g.LEVELS[rec['generation']['template']]
 check_solution(rec)
 return vals

def prose(s):
 s=re.sub(r'\$\$.*?\$\$','',s,flags=re.S);s=re.sub(r'\$.*?\$','',s,flags=re.S)
 return ' '.join(re.findall(r'[A-Za-z]+',s)).lower()

def check_original_stages(original,rec):
 """Read every original arithmetic row; align to generated operative roles.
 Raw endpoint bracket wrappers and vector spacing are notation, not new stages.
 """
 if ':question/worked-solution' not in original:return
 a,b,r,d,F,h,speed,prim,ans=prompt_math(rec)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',original[':question/worked-solution'],re.S)
 for row in rows(blocks[1]):assert equal(expr(rhs(row)).subs({A:vece(a),B:vece(b)}),vece(r))
 rr=rows(blocks[2])
 for row in rr[:3]:assert equal(derivative_expr(rhs(row),r,d),vece(d))
 for row in rr[3:]:assert equal(derivative_expr(rhs(row),r,d),speed)
 for row in rows(blocks[3]):assert equal(expr(rhs(row)),h)
 for row in rows(blocks[4])[1:]:
  v=rhs(row).replace('{[','[').replace(']}',']')
  ev=endpoint_stage(v);assert equal(ev if ev is not None else evaluated(value(v)),ans),('original integral stage',row)
 if len(blocks)==6:
  for row in rows(blocks[5]):
   v=rhs(row);ev=endpoint_stage(v);assert equal(ev if ev is not None else evaluated(value(v)),ans),('original substitution stage',row)

def main():
 src=json.loads((BASE/'source.json').read_text());qs=src['record'][':knowledge-point/questions'];cases=[];reviews=[];engine=[];fidelity=[];unique={l:set() for l in ['easy','moderate','hard']};coverage=set()
 for f,sid in g.SOURCES.items():
  print('Fidelity/review:',f,flush=True)
  q=next(v for v in qs if v[':question/math-academy-id']==sid);p=g.ANCHORS[f];profile='source-'+sid;level=g.LEVELS[f]
  rec=g.generate(level,17,f,parameters=p,profile=profile);check_record(rec);check_original_stages(q,rec)
  sq=rec['question'];assert sq[':question/problem']==q[':question/problem']
  for key in (':question/difficulty',':question/worked-solution'):
   assert (key in sq)==(key in q),(sid,key,'presence')
  fld=sq[':question/answer-fields'][0];old=q[':question/answer-fields'][0]
  assert (':answer-field/correct' in fld)==(':answer-field/correct' in old)
  unmatched=list(fld[':answer-field/choices']);match=[]
  for original in old[':answer-field/choices']:
   target=value(original[':answer/value']);found=[o for o in unmatched if equal(value(o[':answer/value']),target) or equal(evaluated(value(o[':answer/value'])),evaluated(target))]
   assert len(found)==1,(sid,original[':answer/value'],found)
   choice=found[0];unmatched.remove(choice);match.append({'source_value':original[':answer/value'],'generated_value':choice[':answer/value'],'matched':True})
   if ':answer-field/correct' in old and original[':answer/id']==old[':answer-field/correct'][':answer/id']:assert choice[':answer/id']==fld[':answer-field/correct'][1]
  assert not unmatched
  if ':question/worked-solution' in q:
   assert prose(sq[':question/worked-solution'])==prose(q[':question/worked-solution']),(sid,prose(sq[':question/worked-solution']),prose(q[':question/worked-solution']))
   oldblocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);newblocks=re.findall(r'\$\$\n(.*?)\n\$\$',sq[':question/worked-solution'],re.S)
   assert [v.count('&') for v in oldblocks]==[v.count('&') for v in newblocks],(sid,'ordered stage count')
  cases.append({'source_id':sid,'template':f,'parameters':p,'bank_profile':profile,'level':level})
  fidelity.append({'source_id':sid,'options':match,'presence_parity':True,'prompt_exact':True,'designation':'matched' if ':answer-field/correct' in old else 'absent preserved; mathematically inferred normal key','solution':'shared prose and ordered operative stages; notation normalized' if ':question/worked-solution' in old else 'absent preserved'})
  reviews.append(rec)
  # Changed parameter public historical replay demonstrates every observed bank is parameterized.
  cr=g.generate(level,93,f,profile=profile);check_record(cr);reviews.append(cr)
  for seed in (10,28):
   normal=g.generate(level,seed,f);check_record(normal);reviews.append(normal)
 for l in unique:
  print('Sampling:',l,flush=True)
  for seed in range(45):
   rec=g.generate(l,seed);check_record(rec);unique[l].add(rec['generation']['mathematical_fingerprint']);coverage.add(rec['generation']['template'])
 # Every generated review record: correct accepted and every wrong option rejected,
 # historical omissions completed only in private fixture for grader eligibility.
 for idx,rec in enumerate(reviews):
  rr=copy.deepcopy(rec);fld=rr['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in fld:
   _,_,_,_,_,_,_,_,ans=prompt_math(rr);chosen=[o for o in fld[':answer-field/choices'] if equal(evaluated(value(o[':answer/value'])),ans)];assert len(chosen)==1;fld[':answer-field/correct']=[':answer/id',chosen[0][':answer/id']]
  key=fld[':answer-field/correct'][1];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'native owned radio choice; mathematics independently checked'} for a in fld[':answer-field/choices']]
  engine.append({'label':'review-'+str(idx),'record':rr,'checks':checks})
 # Identity and displayed-stage mutation tests.
 mutation_count=0
 for f in g.LEVELS:
  rec=g.generate(g.LEVELS[f],11,f);meta=rec['generation'];other=g.generate(g.LEVELS[f],193,f,parameters=meta['parameters']);assert rec['question'][':question/id']==other['question'][':question/id']
  for old,new in [('r(t) & =a+t','r(t) & =2a+t'),('Computing','\x0cComputing')]:
   bad=copy.deepcopy(rec);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(old,new,1)
   try:check_record(bad)
   except AssertionError:mutation_count+=1
   else:raise AssertionError('mutation accepted')
 # Correlated endpoint changes must fail even when their difference is unchanged.
 poly=g.generate('moderate',11,'polynomial');bad=copy.deepcopy(poly);ss=bad['question'][':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',ss,re.S);pull=rows(blocks[3]);alter=blocks[3].replace(rhs(pull[2]),rhs(pull[3]));bad['question'][':question/worked-solution']=ss.replace(blocks[3],alter)
 try:check_record(bad)
 except AssertionError:mutation_count+=1
 else:raise AssertionError('distribution stage mutation accepted')
 # Correlated signed-component mutation preserves final subtraction, but each
 # printed endpoint component must still agree with the displayed primitive.
 bad=copy.deepcopy(poly);ss=bad['question'][':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',ss,re.S);integ=rows(blocks[4]);er=rhs(integ[4]);_,_,_,_,_,_,sspeed,pprimitive,pans=prompt_math(poly)
 terms=[c*T**e[0] for e,c in sp.Poly(pprimitive,T).terms()];old_upper=g.grp(g.tex(terms[0].subs(T,1)));old_lower=g.grp(g.tex(terms[0].subs(T,0)))
 # Address full endpoint groups independently, rather than replacing all zeros.
 left,right=er.split(')-',1);left=left.replace(old_upper,g.grp(g.tex(terms[0].subs(T,1)+1)),1);right=right.replace(old_lower,g.grp('1'),1);altered=left+')-'+right
 assert equal(expr(altered),pans),'mutation must preserve the total difference'
 bad['question'][':question/worked-solution']=ss.replace(er,altered,1)
 try:check_record(bad)
 except AssertionError:mutation_count+=1
 else:raise AssertionError('correlated endpoint-component mutation accepted')
 invalid=[('radical',{'a':[0,0,1],'b':[1,1,5]}),('quotient',{'a':[-1,1,2],'b':[1,2,1]}),('exponential',{'a':[3,-2,4],'b':[4,-1,5]}),('polynomial',{'a':[1,2,0],'b':[1,1,3]}),('cosine',{'a':[0,1,0],'b':[1,1,-1]}),('sum',{'a':[1,1,1],'b':[1,1,1]})]
 for f,p in invalid:
  try:g.generate(g.LEVELS[f],template=f,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid explicit domain/workload accepted')
 (BASE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(BASE/'fidelity.json').write_text(json.dumps(fidelity,indent=2,ensure_ascii=False)+'\n');(BASE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n');(BASE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(BASE/'engine-input.json'),str(BASE/'engine-report.json')],check=True)
 er=json.loads((BASE/'engine-report.json').read_text())
 summary={'status':'worker validation passed; parent review pending','source_basis':2275,'source_sha256':hashlib.sha256((BASE/'source.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(BASE.with_suffix('.py').read_bytes()).hexdigest(),'source_questions':7,'source_option_matches':35,'source_banks':7,'source_correct_designations_matched':5,'source_correct_designations_absent':2,'source_solutions_stage_and_prose_matched':5,'source_solutions_absent':2,'source_solution_notation_normalizations':5,'source_rating_omissions_preserved':2,'normal_checks':135,'sampled_unique_tasks':{l:len(v) for l,v in unique.items()},'normal_family_coverage':sorted(coverage),'review_records':len(reviews),'native':{k:er[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'mutation_rejections':mutation_count,'explicit_guard_rejections':len(invalid),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'raw_bank_anomalies':[{'source_id':'q-123431','choices':[1,4],'issue':'pole within/at end of [0,1]; divergent/ineligible real definite integral'},{'source_id':'q-123387','choices':[2,3],'issue':'radical negative on part of [0,1]; nonreal/ineligible'}],'unresolved':['Historical distractor intent remains opaque; all seven source profiles evidence-only.','q-123128 and q-76200 have no observed rating, solution, or correct ref; normal completion and assignments are authored.'],'plots':'none'}
 (BASE/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
 review='# Originals and generated variants\n\nBasis2275. Historical profiles are evidence-only. All options are complete mathematical values. Source notation normalization is distinguished from prose/stage fidelity.\n\n'
 for f,sid in g.SOURCES.items():
  q=next(v for v in qs if v[':question/math-academy-id']==sid);review+='## '+sid+' / '+f+'\n\n### Original captured record\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No observed solution, rating or correct key.]')+'\n\n'
  for rec in [v for v in reviews if v['generation']['template']==f]:
   review+='### '+('Parameterized historical evidence' if rec['generation']['evidence_only'] else 'Generated method-bank learner variant')+'\n\n'+g.markdown(rec)+'\n\n'
 (BASE/'review.md').write_text(review)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
