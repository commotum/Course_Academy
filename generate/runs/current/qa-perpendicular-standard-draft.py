"""Parent independently reads points, whole lines, worked slopes and source banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186175924;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_perp_gen',D.with_suffix('.py'));H=load('root_perp_scalar',R/'ode-scalar-parser.py');x,y=H.x,H.y
parse=H.scalar
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q}
def line(t):
 a,b=t.strip().rstrip('.,?').replace('&','').split('=');p=s.Poly(s.expand(parse(a)-parse(b)),x,y);assert p.total_degree()==1;v=tuple(p.coeff_monomial(z)for z in(x,y,1));return v

def canonical(v):
 k=next(z for z in v[:2]if z);return tuple(s.cancel(z/k)for z in v)
def prompt(q):
 t=q[':question/problem'];pts=[tuple(map(s.Integer,z))for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',t)];u,v=pts[0];assert 'perpendicular'in t
 if 'line passing through the points'in t:
  (a,b),(c,d)=pts[1:];A,B,C=d-b,a-c,0;C=-A*a-B*b;assert A*a+B*b+C==0 and A*c+B*d+C==0
 else:A,B,C=line(t.split('perpendicular to ',1)[1].split('$')[1])
 assert A!=0 and B!=0;m1=-A/B;m=B/A;b=v-m*u;return(u,v,m1,-C/B,m,b,pts)
N=dict(records=0,point_checks=0,whole_line_stages=0,slope_stages=0,values=0,pairs=0,source_banks=0,source_values=0,source_keys=0,raw_records=0,recipe_banks=0,recipe_values=0);tasks={l:set()for l in G.LEVELS}
def check(r,sid=None):
 q=r['question'];u,v,m1,refb,m,b,pts=prompt(q);target=canonical((-m,1,-b));f=q[':question/answer-fields'][0];blank=f[':answer-field/type'].endswith('/blank');vals=[line('y='+a[':answer/value']if blank else a[':answer/value'])for a in f[':answer-field/choices']];assert len(vals)==(1 if blank else 5)
 for i,z in enumerate(vals):
  assert(z[0]*u+z[1]*v+z[2]==0 and z[0]+z[1]*m==0)==(f[':answer-field/choices'][i][':answer/id']==f[':answer-field/correct'][1]);N['point_checks']+=1
  for w in vals[:i]:assert canonical(z)!=canonical(w);N['pairs']+=1
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);two=len(pts)==3;assert len(blocks)==(3 if two else 2)
 for bi,block in enumerate(blocks):
  for row in block.split(r'\\'):
   lhs,rhs=row.replace('&','').strip().split('=',1)
   if bi==0 and two:
    repl={'y_2':pts[2][1],'y_1':pts[1][1],'x_2':pts[2][0],'x_1':pts[1][0]};rhs=rhs.replace('{y}_{2}','y_2').replace('{y}_{1}','y_1').replace('{x}_{2}','x_2').replace('{x}_{1}','x_1')
    for k,z in repl.items():rhs=rhs.replace(k,'('+str(z)+')')
    assert s.cancel(parse(rhs)-m1)==0,('numeric source slope stage',row);N['slope_stages']+=1
   else:
    row=row.replace('{x}_{1}','x_1').replace('{y}_{1}','y_1').replace('x_{1}','x_1').replace('y_{1}','y_1').replace('&','').replace('x_1','('+str(u)+')').replace('y_1','('+str(v)+')');row=re.sub(r'(?<![A-Za-z])m(?![A-Za-z_])','('+str(m)+')',row);z=line(row);expected=canonical((-m1,1,-refb))if bi==0 else target;assert canonical(z)==expected,('whole worked line',row,expected);N['whole_line_stages']+=1
 for val in re.findall(r'given line has a slope of \$([^$]+)\$',sol):assert parse(val.rstrip(',.'))==m1;N['slope_stages']+=1
 for val in re.findall(r'perpendicular line must have a slope of \$([^$]+)\$',sol):assert parse(val.rstrip(',.'))==m;N['slope_stages']+=1
 if two:
  rel=re.search(r'm\\cdot\s*\((.*?)\)=-1.*?m=(.*?)\.',sol,re.S);assert rel and parse(rel[1])==m1 and parse(rel[2])==m
 if sid:
  o=olds[sid];of=o[':question/answer-fields'][0];oldvals=[line('y='+a[':answer/value']if blank else a[':answer/value'])for a in of.get(':answer-field/choices',[])];recipes=[line('y='+a if blank else a)for a in G.profile(sid,G.original(sid))]
  if oldvals:
   assert len(oldvals)==len(vals)==len(recipes)and all(sum(canonical(z)==canonical(w)for w in vals)==1 and sum(canonical(z)==canonical(w)for w in recipes)==1 for z in oldvals);N['source_banks']+=1;N['source_values']+=len(vals);N['recipe_banks']+=1;N['recipe_values']+=len(recipes)
  if ':answer-field/correct'in of:
   a=of[':answer-field/correct'][':answer/value'];assert canonical(line('y='+a if blank else a))==target;N['source_keys']+=1
 tasks[q[':question/difficulty'].split('/')[-1]].add((str(m),str(b)));N['records']+=1;N['values']+=len(vals)
for sid,o in olds.items():assert G.raw_replay(sid)['question']==o;N['raw_records']+=1;check(G.generate(G.source_level(sid),template=sid,parameters=G.original(sid)),sid)
for level in G.LEVELS:
 for seed in range(48):check(G.generate(level,seed))
for value in(True,1.1,'1'):
 for f in(lambda:G.generate('easy',value),lambda:G.batch('easy',value),lambda:G.batch('easy',1,value)):
  try:f()
  except ValueError:pass
  else:raise AssertionError('invalid builtin integer accepted')
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_lines={l:len(t)for l,t in tasks.items()},scope='Observed finite nonzero slopes and standard/two-point source stages retained; absent hard is explicit authored moderate-family workload, no new skill or axis branch. Complete lines compared up to nonzero scale; blank expects RHS only.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
