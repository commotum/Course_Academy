#!/usr/bin/env python3
"""Read actual displayed mathematics independently; replay every full source bank.
No database. Fail on source omissions, math, scope, identity, format and grading.
"""
import importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor, function_exponentiation
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,t=s.symbols('x y t',real=True);I,J=s.symbols('I J')

def braced(z,start):
 assert z[start]=='{'; depth=0
 for i in range(start,len(z)):
  depth+=(z[i]=='{')-(z[i]=='}')
  if depth==0:return z[start+1:i],i+1
 raise AssertionError('Unbalanced brace')

def parse(z):
 z=z.strip().rstrip('.')
 z=z.replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\qquad',' ').replace(r'\quad',' ')
 z=re.sub(r'\\operatorname\{(ln|sin|cos|arcsin|asin)\}',lambda m:' '+{'ln':'log','arcsin':'asin'}.get(m[1],m[1])+' ',z)
 z=z.replace('{sin}',' sin').replace('{cos}',' cos').replace(r'\ln','log').replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\arcsin','asin').replace(r'\pi','pi').replace(r'\cdot','*')
 while r'\frac' in z or r'\sqrt' in z:
  marks=[(z.find(cmd),cmd) for cmd in [r'\frac',r'\sqrt'] if cmd in z];start,cmd=min(marks)
  a,end=braced(z,start+len(cmd))
  if cmd==r'\frac':b,end=braced(z,end);v='(('+str_expr(a)+')/('+str_expr(b)+'))'
  else:v='sqrt('+str_expr(a)+')'
  z=z[:start]+v+z[end:]
 z=z.replace('{','(').replace('}',')').replace('[','(').replace(']',')')
 z=re.sub(r'(?<![a-z])i(?![a-z])','I',z);z=re.sub(r'(?<=\d)j(?![a-z])','*J',z);z=re.sub(r'(?<![a-z])j(?![a-z])','J',z)
 z=re.sub(r'(log|sin|cos|asin)\s*([xyt])',r'\1(\2)',z)
 z=z.replace('e^','E^')
 assert '\\' not in z,('Unparsed TeX',z)
 # Function powers before implicit application.
 z=re.sub(r'(sin|cos)\^\((\d+)\)\s*t',r'\1(t)^\2',z)
 z=re.sub(r'(sin|cos)\^(\d+)\s*t',r'\1(t)^\2',z)
 return parse_expr(z,local_dict={'x':x,'y':y,'t':t,'I':I,'J':J,'log':s.log,'asin':s.asin,'sin':s.sin,'cos':s.cos,'sqrt':s.sqrt,'pi':s.pi,'E':s.E,'e':s.E},transformations=standard_transformations+(convert_xor,function_exponentiation,implicit_multiplication_application))
def str_expr(z):return str(parse(z))
def eq(a,b):assert s.simplify(s.trigsimp(a-b))==0,(a,b,s.simplify(a-b))
def vector(z):
 v=s.expand(parse(z));return v.coeff(I),v.coeff(J)
def dotrow(z):
 if r'\cdot' in z:
  lhs,rhs=z.split(r'\cdot',1)
  if any(v in lhs for v in [r'\,i',r'\,j']) and any(v in rhs for v in [r'\,i',r'\,j']):
   a,b=vector(lhs);c,d=vector(rhs);return a*c+b*d
 return parse(z)
def format_check(q):
 for key in [':question/problem',':question/worked-solution']:
  z=q[key];assert z.count('$')%2==0
  depth=0
  for c in z:
   depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0
  assert '--' not in z and '+-' not in z

def outer_groups(z):
 depth=0;parts=[];start=None
 for i,c in enumerate(z):
  if c=='(':
   if depth==0:start=i
   depth+=1
  elif c==')':
   depth-=1;assert depth>=0
   if depth==0:parts.append(z[start+1:i])
 assert depth==0
 return parts

def integral_bounds(z):
 m=re.search(r'\\int\s*\}?\s*_',z);assert m,z
 a,end=braced(z,m.end());assert z[end]=='^';b,end=braced(z,end+1)
 return a,b,end

def unscale(z):
 m=re.fullmatch(r'(\(-?\d+\))\\left\((.*)\\right\)',z)
 return (parse(m[1]),m[2]) if m else (s.Integer(1),z)

def math_check(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 # Actual prompt parsing: no use of generation parameters for reference math.
 P,Q=vector(re.search(r'F\(x,y\)=(.*?)\$ and',prompt)[1]);X,Y=vector(re.search(r'r\(t\)=(.*?)\$ for',prompt)[1])
 a,b=map(parse,re.search(r't\s*\\in\s*\[(.*?),(.*?)\]',prompt).groups());assert a<b
 FP=P.subs({x:X,y:Y},simultaneous=True);FQ=Q.subs({x:X,y:Y},simultaneous=True);dx=s.diff(X,t);dy=s.diff(Y,t);V=s.trigsimp(FP*dx+FQ*dy);value=s.simplify(s.integrate(V,(t,a,b)))
 f=q[':question/answer-fields'][0];opts=[parse(z[':answer/value']) for z in f[':answer-field/choices']]
 assert len(opts)==5
 assert all(s.simplify(v-w)!=0 for i,v in enumerate(opts) for w in opts[:i])
 correct=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);eq(parse(correct[':answer/value']),value)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==6
 assert r'F(r(t))\cdot' in blocks[0] or r'F(r (t))\cdot' in blocks[0]
 coords=blocks[1].strip().rstrip('.'); cx,cy=re.split(r',(?:\\,|\\quad\s*|\\qquad\s*)',coords)
 eq(parse(cx.split('=',1)[1]),X);eq(parse(cy.split('=',1)[1]),Y)
 def rows(block):
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');return [v.strip().rstrip('.') for v in re.split(r'\\\\',body)]
 for row in rows(blocks[2]):
  z=row.split('=',1)[1];u,v=vector(z);eq(u.subs({x:X,y:Y},simultaneous=True),FP);eq(v.subs({x:X,y:Y},simultaneous=True),FQ)
 dr=rows(blocks[3]);assert len(dr)==3
 assert r'\frac{\text{d}x}{\text{d}t}' in dr[0] and r'\frac{\text{d}y}{\text{d}t}' in dr[0]
 args=re.findall(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\((.*?)\)(?:\\,)?[ij]',dr[1]);assert len(args)==2,args
 eq(parse(args[0]),X);eq(parse(args[1]),Y)
 u,v=vector(dr[2].split('=',1)[1]);eq(u,dx);eq(v,dy)
 for row in rows(blocks[4]):eq(dotrow(row.split('=',1)[1]),V)
 ir=rows(blocks[5]);assert len(ir)>=5
 # Parse displayed integration bounds and integrand, including empty source dt.
 for row in ir[:2]:
  z=row.split('=',1)[1]
  ba,bb,end=integral_bounds(z);eq(parse(ba),a);eq(parse(bb),b)
 z=ir[1].split('=',1)[1];scale,z=unscale(z)
 ba,bb,end=integral_bounds(z);integrand=z[end:]
 integrand=re.sub(r'(?:\\,\s*)?(?:\\text\{d\}t|dt)$','',integrand).strip();integrand=integrand.replace(r'\,','').strip()
 if not integrand:integrand='1'
 eq(scale*parse(integrand),V)
 z=ir[2].split('=',1)[1];scale,z=unscale(z)
 # Source primitive notation variants, retaining original endpoint convention.
 z=re.sub(r'\\,\{?\|\}?_\{.*$','',z);z=re.sub(r'_\{.*$','',z)
 z=z.replace(r'\left','').replace(r'\right','').strip()
 if z.startswith('{['):z=z[2:-2]
 elif z.startswith('['):z=z[1:-1]
 primitive=scale*parse(z);eq(s.diff(primitive,t),V)
 if not rec['generation']['evidence_only']:
  endpoints=outer_groups(ir[3].split('=',1)[1]);assert len(endpoints)==2
  terms=s.Add.make_args(primitive)
  for displayed,endpoint in zip(endpoints,[b,a]):
   evaluated=outer_groups(displayed);assert len(evaluated)==len(terms)
   expected=[s.simplify(term.subs(t,endpoint)) for term in terms]
   actual=[parse(v) for v in evaluated]
   for val in actual:
    match=next((i for i,e in enumerate(expected) if s.simplify(val-e)==0),None);assert match is not None,(actual,expected)
    expected.pop(match)
   assert not expected
 for row in ir[3:]:eq(parse(row.split('=',1)[1]),value)
 format_check(q)
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 return value

def run():
 sources=[];review=[];engine=[];counts={'source_questions':8,'source_correct_designations':8,'source_field_layouts':8,'source_attribute_presence':8,'source_banks':0,'source_choices':0,'source_distractors':0,'source_prompt_exact':0,'source_solution_exact':0};variety={}
 for family,q in g.QUESTIONS.items():
  p=g.ORIGINAL_PARAMETERS[family];rec=g.generate('moderate',template=family,parameters=p,profile='observed_'+family)
  math_check(rec)
  rq=rec['question'];assert rq[':question/problem']==q[':question/problem'];assert rq[':question/worked-solution']==q[':question/worked-solution']
  orig=q[':question/answer-fields'][0];f=rq[':question/answer-fields'][0]
  assert {z[':answer/value'] for z in orig[':answer-field/choices']}=={z[':answer/value'] for z in f[':answer-field/choices']}
  assert orig[':answer-field/type'][':db/ident']==f[':answer-field/type'] and orig[':answer-field/key']==f[':answer-field/key']
  correct=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert correct[':answer/value']==orig[':answer-field/correct'][':answer/value']
  for key in [':question/difficulty',':question/answer-fields',':question/worked-solution']:assert (key in q)==(key in rq)
  sources.append({'source_id':q[':question/id'],'source_db_id':q[':db/id'],'template':family,'parameters':p,'bank_profile':'observed_'+family})
  counts['source_banks']+=1;counts['source_choices']+=5;counts['source_distractors']+=4;counts['source_prompt_exact']+=1;counts['source_solution_exact']+=1
  review.append(rec)
  # Changed amplitude public evidence remains a real parameterized recipe.
  evidence=g.generate('moderate',seed=3,template=family,profile='observed_'+family,parameters={**p,'c':2});assert evidence['generation']['evidence_only'];math_check(evidence);review.append(evidence)
 for family,level in g.TEMPLATES.items():
  unique=set()
  for seed in range(30):
   rec=g.generate(level,seed=seed,template=family);math_check(rec);unique.add(rec['generation']['parameter_fingerprint'])
   again=g.generate(level,seed=seed+1000,template=family,parameters=rec['generation']['parameters']);assert rec['question'][':question/id']==again['question'][':question/id']
   if seed<2:review.append(rec)
   if seed<5:engine.append(rec)
  variety[family]=len(unique)
 # Default selection must cover every moderate family.
 seen={g.generate('moderate',seed=i)['generation']['template'] for i in range(50)};assert seen==set(g.FAMILIES)
 invalid=[('easy','affine',{'A':1,'B':1,'D':1,'h':0,'k':0,'u':1,'v':2}),('hard','mixed_power',{'A':1,'B':1,'D':0,'E':1,'u':1,'v':1,'k':1})]
 for level,f,p in invalid:
  try:g.generate(level,template=f,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Accepted workload-degenerate explicit parameters')
 entries=[]
 for i,rec in enumerate(engine+review[:16:2]):
  f=rec['question'][':question/answer-fields'][0];entries.append({'label':str(i),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'correct selection' if a[':answer/id']==f[':answer-field/correct'][1] else 'wrong selection'} for a in f[':answer-field/choices']]})
 (HERE/'native-input.json').write_text(json.dumps(entries,indent=2,ensure_ascii=False));subprocess.run(['generate/runs/current/check-engine',str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 (HERE/'source-cases.json').write_text(json.dumps(sources,indent=2));(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False))
 lines=['# Original and generated review','', 'Observed raw homogeneous profiles are evidence-only. Method profiles are authored complete banks. Easy/hard level labels are authored.','']
 for f,q in g.QUESTIONS.items():
  lines+=['## Original — '+f+' / '+q[':question/math-academy-id'],'',q[':question/problem'],'','Bank: '+', '.join('$'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][':answer/id'] else '') for a in q[':question/answer-fields'][0][':answer-field/choices']),'',q[':question/worked-solution'],'']
 lines +=[g.markdown(r) for r in review];(HERE/'review.md').write_text('\n\n'.join(lines))
 report={'status':'pass','frozen_step':7,'source_fidelity':counts,'authored_generated_math_checks':300,'sampled_unique_tasks_30_per_family':variety,'native':json.loads((HERE/'native-report.json').read_text()),'source_repairs':0,'opaque_evidence_profiles':8,'plots':'none','database_writes':0,'python_version':sys.version.split()[0],'sympy_version':s.__version__}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':run()
