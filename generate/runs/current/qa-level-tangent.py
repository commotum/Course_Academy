"""Root full tangent-line equivalence, actual gradient inputs and stages."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','parent');x,y=p.x,p.y
n=dict(records=0,choices=0,whole_banks=0,formal_inputs=0,gradient_rows=0,tangent_rows=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,ambiguous_evidence_banks=0)
def read(t):return p.scalar(t.strip().rstrip('.,').replace(r'\text{ }',''))
def same(a,b):return s.simplify(a-b)==0
def pair(t):
 t=t.strip().rstrip('.').replace(r'\text{ }','')
 if t.startswith('⟨'):return s.Matrix([read(z) for z in t[1:-1].split(',')])
 return p.vector(t)[:2,0]
def line(t):
 m=re.fullmatch(r'⟨(.*?),(.*?)⟩\s*\\cdot\s*⟨(.*?),(.*?)⟩\s*=\s*0\.?',t.strip());assert m,t
 a,b,c,d=[read(z) for z in m.groups()];return s.expand(a*c+b*d)
def line_key(e):
 P=s.Poly(e,x,y);assert P.total_degree()==1
 a,b,c=[P.coeff_monomial(z) for z in (x,y,1)];pivot=a if a!=0 else b;assert pivot!=0;return tuple(s.simplify(z/pivot) for z in (a,b,c))
def check(rec):
 q=rec['question'];g=rec['generation'];prompt=q[':question/problem'];F=read(re.search(r'\$f\(x, ?y\)\s*=\s*(.*?)\$',prompt)[1].rstrip(','));pt=re.search(r'\$\(x, ?y\)\s*=\s*(.*?)\$',prompt)[1].rstrip('.').strip();a,b=[read(z) for z in pt[1:-1].split(',')];subs={x:a,y:b};d=s.Matrix([s.diff(F,z) for z in (x,y)]);grad=d.subs(subs).applyfunc(s.simplify);assert grad!=s.zeros(2,1);u,v=grad;want=u*(x-a)+v*(y-b);f=q[':question/answer-fields'][0];options=[line(z[':answer/value']) for z in f[':answer-field/choices']];keys=[line_key(z) for z in options];correct=[idx for idx,z in enumerate(keys) if z==line_key(want)]
 assert len(options)==5 and correct
 if g['eligible_for_learning']:
  assert len(set(keys))==5 and len(correct)==1
  profile=g['profile']
  if profile=='method:regular':expected=[want,-u*(x-a)+v*(y-b),v*(x-a)+u*(y-b),u*(x+a)+v*(y-b),u*(x-a)+v*(y+b)]
  elif profile=='method:product':
   B=s.expand(F).coeff(x*y);assert B!=0
   expected=[want,(u-B*b)*(x-a)+v*(y-b),u*(x-a)+(v-B*a)*(y-b),v*(x-a)+u*(y-b),-u*(x-a)+v*(y-b)]
  else:
   assert profile=='method:horizontal' and u==0
   expected=[want,v*(x-a)+u*(y-b),-2*a*(x-a)+v*(y-b),u*(x-a)+v*y,u*(x-a)+v*(y+b)]
  assert sorted(map(str,keys))==sorted(str(line_key(z)) for z in expected)
 elif len(correct)>1:n['ambiguous_evidence_banks']+=1
 if ':answer-field/correct' in f:assert next(idx for idx,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]) in correct
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
  rows=blocks[0].split(r'\\');assert len(rows)==6
  assert '{f}_{x}(x,y)' in rows[0] and '{f}_{y}(x,y)' in rows[0]
  ops=[]
  for m in re.finditer(r'\\frac\{∂\}\{∂([xy])\}\(',rows[1]):
   start=m.end();end=start;depth=1
   while depth:depth+=(rows[1][end]=='(')-(rows[1][end]==')');end+=1
   ops.append((m[1],read(rows[1][start:end-1])))
  assert [z for z,_ in ops]==['x','y'] and all(same(z,F) for _,z in ops)
  for idx,row in enumerate(rows[2:]):
   rhs=row.split('&',1)[1].lstrip(' =');actual=pair(rhs);wantrow=d if idx==0 else grad;assert all(same(z,w) for z,w in zip(actual,wantrow)),(g['template'],idx,rhs,actual,wantrow)
   if idx==1:assert not any(z.has(x,y) for z in actual)
  trows=blocks[1].split(r'\\');assert len(trows)==3
  assert '∇f({x}_{0},{y}_{0})' in trows[0] and 'x-{x}_{0}' in trows[0] and 'y-{y}_{0}' in trows[0]
  tp=re.search(r'f\((.*?),(.*?)\)',trows[1]);assert all(same(read(z),w) for z,w in zip(tp.groups(),(a,b)))
  disp=re.search(r'⟨(.*?),(.*?)⟩',trows[1]);assert all(same(read(z),w) for z,w in zip(disp.groups(),(x-a,y-b)))
  assert line_key(line(trows[-1].replace('&','').strip()))==line_key(want)
  n['formal_inputs']+=2;n['gradient_rows']+=4;n['tangent_rows']+=3
 n['records']+=1;n['choices']+=5;n['whole_banks']+=1
if __name__=='__main__':
 kp=17592186124454;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate('easy',parameters=c['parameters'],profile=c['bank_profile'],template=c['template']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in o)
   if k in o:assert q[k]==(o[k][':db/ident'] if k.endswith('difficulty') else o[k])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   value=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for z in json.load(open(D/'review.json')):check(z.get('record',z))
 for lv in ('easy','moderate','hard'):
  for seed in range(15):
   z=g.generate(lv,seed=73000+seed);check(z);other=g.generate(lv,seed=83000+seed,parameters=z['generation']['parameters'],template=z['generation']['template'],profile=z['generation']['profile']);assert z['question'][':question/id']==other['question'][':question/id']
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
