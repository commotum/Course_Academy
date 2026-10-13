"""Independent root readback of Cartesian integrand-fragment setup templates."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105889
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(ROOT/f'generate/scratch/{K}.py','g');p=load(R/'ode-scalar-parser.py','p');h=load(R/'qa-sinusoidal-properties.py','h');x,y,z=p.x,p.y,p.z
def scalar(q):return p.scalar(q.strip().rstrip('.,').replace(r'\,','').replace(r'\cdot','*'))
def same(a,b):return s.simplify(a-b)==0
src=h.source(g,K);records=json.loads((R/f'qa/{K}-sampled.json').read_text());n=dict(records=0,partial_operators=0,metric_stages=0,substitution_stages=0,integral_bounds=0,choices=0)
for r in records:
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 F=scalar(re.search(r'\$f\(x,y,z\)=(.*?)\$',prompt)[1]);G=scalar(re.search(r'defined by \$z=(.*?)\$',prompt)[1]);dx,dy=s.diff(G,x),s.diff(G,y);pref=F.subs(z,G);M=s.sqrt(1+dx*dx+dy*dy);answer=pref*M
 domains=re.findall(r'\$([^$]+)\\le ([xy])\\le ([^$]+)\$',prompt);assert len(domains)==2 and domains[0][1]=='x' and domains[1][1]=='y';bounds=[scalar(a) for a,_,b in domains for a in (a,b)]
 assert bounds[0]<bounds[1] and bounds[2]<bounds[3]
 for var,want in [('x',dx),('y',dy)]:
  op=re.search(r'\\frac\{∂z\}\{∂'+var+r'\}=\\frac\{∂\}\{∂'+var+r'\}\((.*?)\)=([^\n]+)',sol);assert op and same(scalar(op[1]),G) and same(scalar(op[2]),want);n['partial_operators']+=1
 aligned=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];rows=re.split(r'&\s*=',aligned,maxsplit=1)[1].split(r'\\');assert len(rows)>=4
 for row in rows:
  row=re.sub(r'^\s*&\s*=','',row).strip().rstrip('.')
  if row.startswith(r'{∬}_{D}'):
   body=row[len(r'{∬}_{D}'):].split(r'\text{d}A')[0]
  else:
   m=re.match(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',row);assert m and list(map(s.Integer,m.groups()))==bounds;body=row[m.end():].split(r'\text{d}y')[0];n['integral_bounds']+=4
  if 'f(x,y,g(x,y))' in body:n['metric_stages']+=1
  else:n['substitution_stages']+=1
  body=body.replace('f(x,y,g(x,y))','('+s.latex(pref)+')').replace(r'\frac{∂z}{∂x}','('+s.latex(dx)+')').replace(r'\frac{∂z}{∂y}','('+s.latex(dy)+')')
  body=body.rstrip('\\,');assert same(scalar(body),answer),(r['generation']['template'],row,scalar(body),answer)
 f=q[':question/answer-fields'][0];bank=[scalar(v[':answer/value']) for v in f[':answer-field/choices']];expected=[answer,pref,pref*M*M,pref/M,pref*s.sqrt(dx*dx+dy*dy)];assert len(bank)==5
 remaining=list(expected)
 for a,value in zip(f[':answer-field/choices'],bank):
  matching=[j for j,v in enumerate(remaining) if same(value,v)];assert len(matching)==1;remaining.pop(matching[0]);assert same(value,answer)==(a[':answer/id']==f[':answer-field/correct'][1]);n['choices']+=1
 assert not remaining and all(not same(v,w) for j,v in enumerate(bank) for w in bank[:j]);n['records']+=1
report=dict(status='passed',kp_id=K,source=src,readback=n,response_criterion='The missing integrand fragment, not the scalar value of its integral.',script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
