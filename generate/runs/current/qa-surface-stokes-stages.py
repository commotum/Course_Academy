"""Root verifies oriented flux, direct boundary work and every printed stage."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186133928'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'g');p=load(R/'ode-scalar-parser.py','p');T=p.t;U=s.Symbol('u',real=True)
n=dict(records=0,choices=0,curl_flux_equalities=0,formal_derivatives=0,field_stages=0,dot_stages=0,primitive_components=0,endpoint_components=0,source_prompts=0,source_solutions=0,source_values=0,source_refs=0);seen=set()
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def vector(t,formal=False):
 t=t.strip();assert t.startswith(r'\langle ') and t.endswith(r'\rangle');parts=t[len(r'\langle '):-len(r'\rangle')].split(',');assert len(parts)==3;out=[]
 for part in parts:
  if formal:
   prefix=r'\frac{\mathrm d}{\mathrm dt}';assert part.strip().startswith(prefix);out.append(s.diff(p.scalar(part.strip()[len(prefix):]),T));n['formal_derivatives']+=1
  else:out.append(p.scalar(part))
 return s.Matrix(out)
def components(t):
 out=[];start=0;depth=0
 for i,ch in enumerate(t):
  depth+=(ch=='(')-(ch==')')
  if depth==0 and t[i:i+3]==' + ':out.append(t[start:i]);start=i+3
 out.append(t[start:]);return out
def normal(r):
 if not r['generation']['eligible_for_learning']:return
 q=r['question'];qid=q[':question/id']
 if qid in seen:return
 prompt=q[':question/problem'];curve=vector(re.search(r'parametrization \$r\(t\)=(.*?)\$ for',prompt)[1]);F=vector(re.search(r'F\(x,y,z\)=(.*?),\$ evaluate',prompt)[1]);lo,hi=map(p.scalar,re.search(r't\\in \[(.*?),(.*?)\)\.',prompt).groups());assert all(same(v.subs(T,lo),v.subs(T,hi)) for v in curve)
 dr=curve.diff(T);fr=F.subs(dict(zip((p.x,p.y,p.z),curve)),simultaneous=True);dot=s.expand(fr.dot(dr));answer=s.simplify(s.integrate(dot,(T,lo,hi)))
 curl=s.Matrix([s.diff(F[2],p.y)-s.diff(F[1],p.z),s.diff(F[0],p.z)-s.diff(F[2],p.x),s.diff(F[1],p.x)-s.diff(F[0],p.y)]);area=curve.cross(U*dr);restricted=curl.subs(dict(zip((p.x,p.y,p.z),U*curve)),simultaneous=True);flux=s.integrate(restricted.dot(area),(U,0,1),(T,lo,hi));assert same(flux,answer);n['curl_flux_equalities']+=1
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==6
 for j,coord in enumerate(blocks[1].split(r',\quad ')):assert coord.split('=')[0]=='xyz'[j] and same(p.scalar(coord.split('=')[1]),curve[j])
 rows=[[part.split('& =',1)[1].strip() for part in block.split(r'\\')] for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)];assert list(map(len,rows))==[3,2,5,6]
 for i,row in enumerate(rows[0]):assert all(same(a,b) for a,b in zip(vector(row),F if i==0 else fr));n['field_stages']+=1
 assert all(same(a,b) for a,b in zip(vector(rows[1][0],True),dr)) and all(same(a,b) for a,b in zip(vector(rows[1][1]),dr))
 vv=rows[2][0].split(r'\cdot ');assert len(vv)==2 and all(same(a,b) for a,b in zip(vector(vv[0]),fr)) and all(same(a,b) for a,b in zip(vector(vv[1]),dr))
 for row in rows[2][1:]:assert same(p.scalar(row),dot);n['dot_stages']+=1
 final=rows[3];assert final[0]==r'\oint_C F\cdot\mathrm dr'
 m=re.fullmatch(r'\\int_\{(.*?)\}\^\{(.*?)\} (.*)',final[1]);assert m and p.scalar(m[1])==lo and p.scalar(m[2])==hi and m[3]==r'F(r(t))\cdot r\prime(t)\,\mathrm dt'
 m=re.fullmatch(r'\\int_\{(.*?)\}\^\{(.*?)\}(.*)\\,\\mathrm dt',final[2]);assert m and p.scalar(m[1])==lo and p.scalar(m[2])==hi and same(p.scalar(m[3]),dot)
 m=re.fullmatch(r'\\left\[(.*?)\\right\]_\{(.*?)\}\^\{(.*?)\}',final[3]);assert m;primitive=p.scalar(m[1]);terms=[p.scalar(t) for t in components(m[1])];assert same(s.diff(primitive,T),dot) and p.scalar(m[2])==lo and p.scalar(m[3])==hi;n['primitive_components']+=len(terms)
 endpoint=final[4].split(r'\right)-\left(');assert len(endpoint)==2
 top=endpoint[0][len(r'\left('):];bottom=endpoint[1][:-len(r'\right)')]
 for text,t in ((top,hi),(bottom,lo)):
  vals=[p.scalar(v) for v in components(text)];assert len(vals)==len(terms)
  for a,b in zip(vals,terms):assert same(a,b.subs(T,t));n['endpoint_components']+=1
 assert same(p.scalar(final[4]),answer) and same(p.scalar(final[5]),answer)
 f=q[':question/answer-fields'][0];values=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not same(a,b) for i,a in enumerate(values) for b in values[:i]) and sum(same(v,answer) for v in values)==1;assert same(p.scalar(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])),answer)
 kind=r['generation']['template']
 if kind=='easy-circle':expected=[answer,-answer,0,s.integrate(dot,(T,lo,(lo+hi)/2)),answer/s.pi]
 elif any(v.has(s.sin,s.cos) for v in curve):
  pi_angle=any(v.has(s.sin(s.pi*T),s.cos(s.pi*T)) for v in curve);expected=[answer,-answer,0,s.integrate(dot,(T,lo,(lo+hi)/2)),answer/s.pi if pi_angle else 2*answer]
 else:
  wrong=F.subs(dict(zip((p.x,p.y,p.z),dr)),simultaneous=True);expected=[answer,-answer,s.integrate(fr.dot(curve),(T,lo,hi)),s.integrate(sum(fr),(T,lo,hi)),s.integrate(wrong.dot(dr),(T,lo,hi))]
 assert all(sum(same(v,s.sympify(e)) for e in expected)==1 for v in values)
 seen.add(qid);n['records']+=1;n['choices']+=5
for case in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);q=r['question'];o=g.SOURCES[case['source_id']];assert q[':question/problem']==o[':question/problem'] and (':question/worked-solution' in q)==(':question/worked-solution' in o) and (':question/difficulty' in q)==(':question/difficulty' in o)
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
 assert len(q[':question/answer-fields'])==len(o[':question/answer-fields'])
 for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']) and (':answer-field/correct' in f)==(':answer-field/correct' in of);n['source_values']+=5
  if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
 assert not r['generation']['eligible_for_learning'];n['source_prompts']+=1
for item in json.loads((D/'native-input.json').read_text()):normal(item['record'])
for level in ('easy','moderate','hard'):
 for seed in range(18):normal(g.generate(level,seed))
out={'status':'passed','independent_readback':n,'orientation':'Flux cross-check uses u*r(t) with r_u cross r_t, so its positive boundary follows the supplied increasing parameter; no arbitrary outward/upward assumption.'};(R/'qa/17592186133928-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
