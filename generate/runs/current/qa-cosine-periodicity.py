"""Parent reads actual conditional tasks, whole banks and every prose/math stage."""
import importlib.util,re,json,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186176048;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('periodic_parent_parser',P/'vector-math-parser.py');g=module('periodic_parent_generator',D.with_suffix('.py'));X,Y=p.x,p.y;N=s.Symbol('parent_integer',integer=True)
C=dict(instances=0,choices=0,prompt_period_reductions=0,printed_period_identities=0,solution_equalities=0,prose_equations=0,source_banks=0,source_values=0,source_prompts=0,source_full_solutions=0,source_keys=0,missing_source_keys=0,raw_duplicate_wrong_pairs=0)
def scalar(raw):
 raw=raw.strip().rstrip('.,').replace('π',r'\pi').replace('⁡','')
 raw=re.sub(r'\\[A-Za-z]+|n',lambda m:'z' if m[0]=='n' else m[0],raw)
 return p.scalar(raw).subs(p.z,N)
def expression(raw,given=None):
 raw=raw.strip().rstrip('.,').replace('⁡',''); result='';pos=0;args=[]
 pattern=re.compile(r'(?:\\cos|(?<![A-Za-z])cos)\s*')
 while m:=pattern.search(raw,pos):
  result+=raw[pos:m.start()];i=m.end()
  if raw[i]=='(':
   start=i+1;depth=1;i+=1
   while depth:
    assert i<len(raw);depth+=(raw[i]=='(')-(raw[i]==')');i+=1
   arg=scalar(raw[start:i-1])
  else:assert raw[i]=='x',(raw,i);arg=X;i+=1
  shift=s.simplify((arg-X)/(2*s.pi));assert shift.is_integer is True,('Not periodic-only argument',raw,arg,shift)
  result+='y';args.append(arg);pos=i
 result+=raw[pos:];value=scalar(result)
 return (value.subs(Y,given) if given is not None else value),args

def check(r):
 q=r['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution'];parts=re.findall(r'\$(.*?)\$',prompt);given=scalar(parts[0].split('=',1)[1]);target=parts[-1].rsplit('=',1)[0];abstract,args=expression(target);assert len(args)==1
 shift=s.simplify((args[0]-X)/(2*s.pi));assert shift.is_Integer and shift!=0
 a=s.diff(abstract,Y);b=s.simplify(abstract-a*Y);assert a.is_Integer and b.is_Integer
 expected=abstract.subs(Y,given);f=q[':question/answer-fields'][0];values=[scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(values)==5
 good=[z[':answer/id'] for z,v in zip(f[':answer-field/choices'],values) if s.simplify(v-expected)==0];assert good==[f[':answer-field/correct'][1]]
 pairs=[(i,j) for i,v in enumerate(values) for j,w in enumerate(values[:i]) if s.simplify(v-w)==0];raw=r['generation']['bank_profile']=='observed_raw_q103242';assert len(pairs)==int(raw)
 C['raw_duplicate_wrong_pairs']+=len(pairs);C['choices']+=5;C['prompt_period_reductions']+=1
 level=q[':question/difficulty'].split('/')[-1]
 assert given.is_real and 0<abs(given)<=1
 if level=='easy':assert abs(shift) in (1,2) and (a,b)==(1,0) and given in (1,-1,s.Rational(1,2),-s.Rational(1,2),s.sqrt(2)/2,-s.sqrt(2)/2,s.sqrt(3)/2,-s.sqrt(3)/2)
 elif level=='moderate':assert 3<=abs(shift)<=10 and (a,b)==(1,0)
 else:assert 2<=abs(shift)<=10 and 2<=abs(a)<=6 and 1<=abs(b)<=6
 # Read actual prose integer, then every printed angle, term and equality.
 assert re.search(r'\$n='+re.escape(str(shift))+r'\$',solution),solution
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S);assert len(blocks)==(3 if a!=1 else 2)
 for bi,block in enumerate(blocks):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');rows=block.split(r'\\');assert len(rows)==(3 if bi==2 else 1)
  previous=None
  for row in rows:
   sides=row.strip().split('=');assert len(sides)>=2
   values0=[]
   for j,side in enumerate(sides):
    if side.strip():
     value,angles=expression(side,given)
     if bi>0:assert all(angle==X or s.simplify(angle-args[0])==0 for angle in angles),(side,angles,args)
    else:assert j==0 and previous is not None;value=previous
    values0.append(value)
   assert all(s.simplify(v-values0[0])==0 for v in values0),row
   previous=values0[-1];C['solution_equalities']+=len(values0)-1
  if bi==0:
   assert '2n' in block and r'\pi' in block;C['printed_period_identities']+=1
  if bi==2:assert s.simplify(previous-expected)==0
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',solution,re.S):
  if '=' not in inline or 'cos' not in inline or inline.startswith('y='):continue
  lhs,rhs=inline.split('=',1);v1,angles1=expression(lhs,given);v2,angles2=expression(rhs,given);assert all(z==X or s.simplify(z-args[0])==0 for z in angles1+angles2);assert s.simplify(v1-v2)==0;C['prose_equations']+=1
 C['instances']+=1;return q,(s.srepr(given),str(a),str(b))
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q,key=check(r);old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0];unused=list(range(5));vs=[scalar(z[':answer/value']) for z in f[':answer-field/choices']]
 for choice in of[':answer-field/choices']:
  matches=[i for i in unused if s.simplify(vs[i]-scalar(choice[':answer/value']))==0];assert matches;unused.remove(matches[0]);C['source_values']+=1
 assert not unused;C['source_banks']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_full_solutions']+=1
 if of.get(':answer-field/correct'):
  actual=next(v for z,v in zip(f[':answer-field/choices'],vs) if z[':answer/id']==f[':answer-field/correct'][1]);assert s.simplify(actual-scalar(of[':answer-field/correct'][':answer/value']))==0;C['source_keys']+=1
 else:C['missing_source_keys']+=1
 # Changed values, signs, periods and affine terms through each source recipe.
 for seed in range(24):check(g.generate(case['level'],seed+70,template=case['template'],profile=case['bank_profile']))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
easy=set()
for c in ('1','-1','1/2','-1/2','sqrt(2)/2','-sqrt(2)/2','sqrt(3)/2','-sqrt(3)/2'):
 for n in (-2,-1,1,2):
  _,key=check(g.generate('easy',parameters={'c':c,'n':n,'a':1,'b':0}));easy.add(key)
assert len(easy)==8;C['finite_easy_actual_tasks']=len(easy)
freeze=json.loads((D/'freeze-hashes.json').read_text())
for name,digest in freeze.items():
 path=D.with_suffix('.py') if name==f'{K}.py' else P/name if name in ('check-engine','check-engine.rs') else D/name
 assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,path
C['frozen_hashes_verified']=len(freeze);C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
