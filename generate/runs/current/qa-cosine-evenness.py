"""Parent independently reads all printed evenness tasks and their full stages."""
import importlib.util,re,json,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186176057;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('even_parent_parser',P/'vector-math-parser.py');g=module('even_parent_generator',D.with_suffix('.py'));X,Y=p.x,p.y
C=dict(instances=0,choices=0,solution_equalities=0,prose_equations=0,evenness_identities=0,periodicity_stages=0,affine_stages=0,source_banks=0,source_values=0,source_prompts=0,source_full_solutions=0,source_keys=0,missing_source_keys=0,raw_missing_records=0)
def scalar(raw,v='x'):
 raw=raw.strip().rstrip('.,').replace('π',r'\pi').replace('⁡','')
 raw=re.sub(r'\\[A-Za-z]+|[atu]',lambda m:'x' if m[0]==v else m[0],raw)
 return p.scalar(raw)
def expression(raw,given=None,v='x'):
 raw=raw.strip().rstrip('.,').replace('⁡',''); result='';pos=0;args=[]
 pattern=re.compile(r'(?:\\cos|(?<![A-Za-z])cos)\s*')
 while m:=pattern.search(raw,pos):
  result+=raw[pos:m.start()];i=m.end()
  if raw[i]=='(':
   start=i+1;depth=1;i+=1
   while depth:
    assert i<len(raw);depth+=(raw[i]=='(')-(raw[i]==')');i+=1
   arg=scalar(raw[start:i-1],v)
  else:assert raw[i] in (v,'x'),(raw,i);arg=X;i+=1
  coeff=arg.diff(X);shift=s.simplify((arg-coeff*X)/(2*s.pi));assert coeff in (-1,1) and shift.is_Integer,('Outside evenness/fullperiod',raw,arg)
  result+='y';args.append(arg);pos=i
 result+=raw[pos:];value=scalar(result,v)
 return (value.subs(Y,given) if given is not None else value),args

def check(r):
 q=r['question'];prompt=q[':question/problem'];parts=re.findall(r'\$(.*?)\$',prompt);v=re.search(r'(?:\\cos\s*|cos⁡)([xatu])',parts[0])[1];given=scalar(parts[0].split('=',1)[1],v);target=parts[-1].rsplit('=',1)[0];abstract,args=expression(target,v=v);assert len(args)==1
 arg=args[0];assert arg.diff(X)==-1;shift=s.simplify((arg+X)/(2*s.pi));a=s.diff(abstract,Y);b=s.simplify(abstract-a*Y);expected=abstract.subs(Y,given)
 f=q[':question/answer-fields'][0];values=[scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(values)==5 and all(s.simplify(v-w)!=0 for i,v in enumerate(values) for w in values[:i]);good=[z[':answer/id'] for z,val in zip(f[':answer-field/choices'],values) if s.simplify(val-expected)==0];assert len(good)==1
 raw=r['generation']['bank_profile']=='q-136634_raw'
 if raw:assert ':answer-field/correct' not in f and ':question/worked-solution' not in q;C['raw_missing_records']+=1
 else:assert good==[f[':answer-field/correct'][1]]
 level=r['generation']['level'];assert -1<=given<=1
 if level=='easy':assert shift==0 and (a,b)==(1,0)
 else:assert shift!=0 and abs(shift)<=20
 if level=='moderate':assert (a,b)==(1,0)
 if level=='hard':assert (a.is_Integer and 2<=abs(a)<=5 or (a/s.pi).is_Integer and 1<=abs(a/s.pi)<=3) and b.is_Rational and 0<abs(b)<=3 and s.denom(b)<=6
 C['choices']+=5;C['instances']+=1
 if not raw:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)=={'easy':2,'moderate':3,'hard':4}[level]
  for bi,block in enumerate(blocks):
   block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');rows=block.split(r'\\');assert len(rows)==(1 if bi==0 else 3 if level=='hard' and bi==3 else 2)
   prev=None
   for ri,row in enumerate(rows):
    pieces=row.strip().split('=');assert len(pieces)>=2
    vs=[]
    for j,part in enumerate(pieces):
     if part.strip():
      value,angles=expression(part,given,v)
      if bi==0:assert all(angle in (X,-X) for angle in angles)
      elif level!='easy' and bi==1:
       # Printed expanded multiplier must describe the exact prompt shift.
       assert all(s.simplify(angle-(arg if ri==0 else -X))==0 for angle in angles if j>0),(row,angles,arg)
      else:assert all(angle in (X,-X) or s.simplify(angle-arg)==0 for angle in angles),(part,angles,arg)
     else:assert j==0 and prev is not None;value=prev
     vs.append(value)
    assert all(s.simplify(value-vs[0])==0 for value in vs),row;prev=vs[-1];C['solution_equalities']+=len(vs)-1
   if bi==0:C['evenness_identities']+=1
   elif level!='easy' and bi==1:C['periodicity_stages']+=1
   elif level=='hard' and bi==3:assert s.simplify(prev-expected)==0;C['affine_stages']+=1
  for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
   if '=' not in inline or 'cos' not in inline or inline.startswith('y='):continue
   lhs,rhs=inline.split('=',1);v1,angles1=expression(lhs,given,v);v2,angles2=expression(rhs,given,v);assert all(z in (X,-X) or s.simplify(z-arg)==0 for z in angles1+angles2);assert s.simplify(v1-v2)==0;C['prose_equations']+=1
 return q,(level,s.srepr(given),s.srepr(a),s.srepr(b))
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q,key=check(r);old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0];unused=list(range(5));vs=[scalar(z[':answer/value']) for z in f[':answer-field/choices']]
 for choice in of[':answer-field/choices']:
  matches=[i for i in unused if s.simplify(vs[i]-scalar(choice[':answer/value']))==0];assert matches;unused.remove(matches[0]);C['source_values']+=1
 assert not unused;C['source_banks']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_full_solutions']+=1
 if of.get(':answer-field/correct'):
  actual=next(val for z,val in zip(f[':answer-field/choices'],vs) if z[':answer/id']==f[':answer-field/correct'][1]);assert s.simplify(actual-scalar(of[':answer-field/correct'][':answer/value']))==0;C['source_keys']+=1
 else:C['missing_source_keys']+=1
 for seed in range(16):check(g.generate(case['level'],seed+32,template=case['template'],profile=case['bank_profile']))
 if case.get('normal_repair_profile'):check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['normal_repair_profile']))
actual={}
for level in ('easy','moderate','hard'):
 tasks=set()
 for seed in range(100):_,key=check(g.generate(level,seed));tasks.add(key)
 assert len(tasks)>=60;actual[level]=len(tasks)
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('moderate','hard'):
 rs=[]
 for n in (-20,-1,1,20):
  params={'c':'1/3','variable':'x','n':n}
  if level=='hard':params.update(scale='2',offset='1/2')
  rs.append(g.generate(level,parameters=params));check(rs[-1])
 assert len({r['generation']['parameter_fingerprint'] for r in rs})==1 and len({r['question'][':question/id'] for r in rs})==4
freeze=json.loads((D/'freeze.json').read_text())
for path,digest in freeze['file_sha256'].items():assert hashlib.sha256((P.parents[2]/path).read_bytes()).hexdigest()==digest,path
assert hashlib.sha256((D/'validation.json').read_bytes()).hexdigest()==freeze['validation_sha256']
C['actual_default_task_counts']=actual;C['frozen_hashes_verified']=len(freeze['file_sha256']);C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
