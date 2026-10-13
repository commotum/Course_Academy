"""Root actual implicit curve/tangent vector and full ordered-stage readback."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','reader');x,y=p.x,p.y;i,j=p.i,p.j
n=dict(records=0,choices=0,banks=0,formal_inputs=0,symbolic_rows=0,evaluated_rows=0,rearrangements=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,known_raw_errors=0)
def scalar(t):
 t=t.strip().rstrip('.,').replace(r'\text{ }','').replace('\\\\','\\')
 t=t.replace(r'\operatorname{sin}⁡xy',r'\sin(xy)')
 return p.scalar(t)
def pair(t):
 e=s.expand(scalar(t));a,b=e.coeff(i),e.coeff(j);assert s.simplify(e-a*i-b*j)==0,(t,e);return s.Matrix([a,b])
def same(a,b):return s.simplify(a-b)==0

def check(rec):
 q=rec['question'];gen=rec['generation'];raw=gen['profile'].startswith('raw:');sid=gen['template'];blocks=re.findall(r'\$([^$]+)\$',q[':question/problem']);curve=blocks[0].rstrip('.');l,r=curve.split('=');F=scalar(l)-scalar(r);pt=blocks[-1].strip().rstrip('.');assert pt.startswith('(') and pt.endswith(')'),pt;a,b=[scalar(z) for z in pt[1:-1].split(',')];sub={x:a,y:b};grad=s.Matrix([s.diff(F,z).subs(sub) for z in (x,y)]);assert grad!=s.zeros(2,1)
 member=same(F.subs(sub),0)
 if not member:assert raw and sid=='q-130201';n['known_raw_errors']+=1
 for f in q[':question/answer-fields']:
  vs=[pair(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5
  valid=[idx for idx,v in enumerate(vs) if v!=s.zeros(2,1) and same(v.dot(grad),0)]
  opaque=gen['evidence_only'] and not raw and False
  # Changed opaque evidence can have extra valid choices; it is never eligible.
  exact_source=not (raw and ':question/math-academy-id' not in q)
  assert valid
  if gen['eligible_for_learning']:assert len(valid)==1
  if ':answer-field/correct' in f:
   designated=next(idx for idx,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]);assert designated in valid
  else:assert raw
  if gen['eligible_for_learning']:
   assert len({z[':answer/id'] for z in f[':answer-field/choices']})==5
   assert all(not same(u[0]*v[1]-u[1]*v[0],0) for idx,u in enumerate(vs) for v in vs[:idx])
   # Derive omitted first family term from the actual printed function.
   lv=q[':question/difficulty'].split('/')[-1]
   power=x**2 if lv=='easy' else x**2*y if lv=='moderate' else x*s.log(y)
   coefficient=s.expand(F).coeff(power);assert coefficient!=0
   reduced=F-coefficient*power;g2=s.Matrix([s.diff(reduced,z).subs(sub) for z in (x,y)])
   A,B=grad;C,D=g2;wanted=[s.Matrix(z) for z in ((B,-A),(A,B),(B,A),(-A,B),(D,-C))]
   assert all(sum(all(same(u,v) for u,v in zip(w,z)) for z in vs)==1 for w in wanted)
  n['choices']+=len(vs);n['banks']+=1
 sol=q.get(':question/worked-solution')
 if sol:
  aligns=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
  for align in aligns[:-1]:
   for row in align.split(r'\\'):
    l,r=row.replace('&','').split('=');z=scalar(l)-scalar(r);assert same(z,F) or same(z,-F),(sid,row,z,F);n['rearrangements']+=1
  rows=aligns[-1].split(r'\\');inputs=[]
  pattern=r'\\frac\{(?:∂|\\partial)\}\{(?:∂|\\partial) ?([xy])\}\('
  for m in re.finditer(pattern,rows[0]):
   start=m.end();end=start;depth=1
   while depth:
    depth+=(rows[0][end]=='(')-(rows[0][end]==')');end+=1
   inputs.append((m[1],scalar(rows[0][start:end-1])))
  assert [z for z,F0 in inputs]==['y','x'];FY,FX=[F0 for z,F0 in inputs];assert same(FY,FX)
  assert any(all(same(s.diff(FY,z),sign*s.diff(F,z)) for z in (x,y)) for sign in (1,-1)),(sid,FY,F)
  level=re.search(r'level curve \$f\(x,y\)=(.*?)\.\$',sol);assert level
  if not same(FY.subs(sub),scalar(level[1])):assert raw and sid in ('q-72463','q-130201');n['known_raw_errors']+=1
  symbolic=s.Matrix([s.diff(FY,y),-s.diff(FY,x)]);numeric=symbolic.subs(sub)
  for idx,row in enumerate(rows[1:]):
   rhs=row.split('&',1)[1].lstrip(' =');v=pair(rhs);expected=symbolic if idx==0 else numeric
   assert all(same(u,w) for u,w in zip(v,expected)),(sid,idx,rhs,v,expected)
   n['symbolic_rows' if idx==0 else 'evaluated_rows']+=1
  conclusion=re.search(r'Therefore, our tangent vector is \$(.*?)\$',sol);assert conclusion
  assert all(same(u,w) for u,w in zip(pair(conclusion[1]),numeric)),(sid,gen['profile'],gen['parameters'],conclusion[1],numeric)
  n['formal_inputs']+=2
 n['records']+=1

if __name__=='__main__':
 kp=17592186124455;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  z=g.generate('moderate',parameters=c['parameters'],profile=c['bank_profile']);check(z);q=z['question'];o=olds[c['source_id']]
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in o)
   if k in o:assert q[k]==(o[k][':db/ident'] if k.endswith('difficulty') else o[k])
  assert len(q[':question/answer-fields'])==len(o[':question/answer-fields'])
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:
    old=of[':answer-field/correct'][':answer/value'];new=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert old==new;n['source_refs']+=1
   n['source_values']+=len(of[':answer-field/choices'])
  n['source_prompts']+=1;n['source_solutions']+=int(':question/worked-solution' in o)
 for z in json.load(open(D/'review.json')):check(z.get('record',z))
 for lv in ('easy','moderate','hard'):
  for seed in range(20):
   a=g.generate(lv,seed=35000+seed);check(a);b=g.generate(lv,seed=45000+seed,parameters=a['generation']['parameters']);assert a['question'][':question/id']==b['question'][':question/id']
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
