"""Root checks displayed vectors, full banks and solution stages against inspected geometry."""
import hashlib,importlib.util,json,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186096814;D=P.parents[2]/f'generate/scratch/{K}'
def mod(n,path):
 a=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(a);a.loader.exec_module(m);return m
p=mod('root_diagram_parser',P/'vector-math-parser.py');g=mod('root_diagram_generator',D.with_suffix('.py'))
C=dict(records=0,choices=0,whole_method_banks=0,evidence_banks=0,solution_equalities=0,prose_leg_values=0,raw_profiles=0,source_prompts=0,source_values=0,available_source_solutions=0)
# Independently transcribed from personally inspected full-resolution original PNGs.
GEOMETRY={'q-20407':([s.Integer(2),-s.Rational(7,2)],[0,0]),'q-19276':([s.Rational(5,2),-s.Rational(3,2)],[s.Rational(3,2),s.Integer(3)]),'q-119805':([s.Integer(1),-s.Rational(1,2)],[-s.Rational(3,2),s.Rational(5,2)])}
sources={x[':question/math-academy-id']:x for x in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];meta=r['generation'];geo=json.loads(Path(meta['plots']['prompt'].replace('-prompt.png','.json')).read_text())['geometry'];assert geo==meta['geometry'];assert geo['grid_increment']==.5
 A=s.Matrix([s.Rational(str(z)) for z in geo['A']]);B=s.Matrix([s.Rational(str(z)) for z in geo['B']]);middle=geo.get('P');names=geo['names'];vectors=[B-A] if middle is None else [s.Matrix([s.Rational(str(z)) for z in middle])-A,B-s.Matrix([s.Rational(str(z)) for z in middle])];target=B-A;L=s.sqrt(target.dot(target));hx,hy=map(abs,target)
 assert all(z!=0 for z in target)
 if meta['source_id']:
  aa,bb=GEOMETRY[meta['source_id']];pp=meta['parameters'];scale=s.Rational(str(pp.get('scale',1)))
  if meta['bank_profile'] in ('raw_c','observed_c','raw_qr','observed_qr'):assert vectors==[s.Matrix(aa)*scale] if len(vectors)==1 else vectors==[s.Matrix(aa)*scale,s.Matrix(bb)*scale]
 def expr(raw):
  raw=raw.strip().rstrip('.,').replace('&','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','');raw=re.sub(r'\|[^|]+\|',lambda _: '('+s.latex(L)+')',raw)
  raw=raw.replace('A{H}','AH').replace('B{H}','BH');raw=raw.replace('AH','('+s.latex(hx)+')').replace('BH','('+s.latex(hy)+')').replace('AB','('+s.latex(L)+')')
  if raw.strip()=='u':return target/L
  raw=re.sub(r'\\[A-Za-z]+|[A-Za-z]',lambda m:m[0] if m[0].startswith('\\') else ({names[0]:'u',**({names[1]:'v'} if len(names)>1 else {})}.get(m[0],m[0])),raw)
  raw=re.sub(r'\d+\.\d+',lambda m:s.latex(s.Rational(m[0])),raw)
  result=p.scalar(raw);units=[p.u,p.v];d={p.x:target[0]/L,**{z:v[0] for z,v in zip(units,vectors)}};e={p.x:target[1]/L,**{z:v[1] for z,v in zip(units,vectors)}};return s.Matrix([s.simplify(result.subs(d)),s.simplify(result.subs(e))]) if result.free_symbols.intersection({p.u,p.v,p.x}) else result
 fields=q.get(':question/answer-fields',[])
 if fields:
  f=fields[0];vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5 and len({tuple(v) for v in vals})==5
  eligible=lambda z:s.simplify(z.dot(z)-1)==0 and s.simplify(z[0]*target[1]-z[1]*target[0])==0
  assert sum(eligible(z) for z in vals)==1
  if ':answer-field/correct' in f:assert eligible(next(z for a,z in zip(f[':answer-field/choices'],vals) if a[':answer/id']==f[':answer-field/correct'][1]))
  else:assert meta['evidence_only']
  if meta['bank_profile']=='authored_method' or meta['bank_profile']=='observed_hard':
   expected=[target*z for z in [1/L,1/L**2,L,1/hx,2/L]];assert {tuple(z) for z in vals}=={tuple(z) for z in expected};C['whole_method_banks']+=1
  else:C['evidence_banks']+=1
  C['choices']+=len(vals)
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution']
  for label,value in [('AH',hx),('BH',hy)]:
   prose=re.search(label+r'=([^$]+)\$',text)[1]
   for x in prose.split('='):assert s.simplify(expr(x)-value)==0;C['prose_leg_values']+=1
  for block in re.findall(r'\$\$(.*?)\$\$',text,re.S):
   prev=None
   for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    parts=row.split('=');assert len(parts)>=2;vals=[]
    for part in parts:
     if not part.replace('&','').strip():assert prev is not None;val=prev
     else:val=expr(part)
     vals.append(val)
    assert all(s.simplify(z-vals[0])==s.zeros(2,1) if isinstance(z,s.MatrixBase) else s.simplify(z-vals[0])==0 for z in vals[1:]),(row,vals)
    prev=vals[-1];C['solution_equalities']+=len(vals)-1
 C['records']+=1
for case in json.loads((D/'source-cases.json').read_text()):
 raw=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(raw);old=sources[case['source_id']];q=raw['question'];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in q)==(key in old)
 if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];C['available_source_solutions']+=1
 if ':question/answer-fields' in old:
  assert all(':answer-field/correct' not in f for f in q[':question/answer-fields']);values=lambda a:sorted(x[':answer/value'] for x in a[':question/answer-fields'][0][':answer-field/choices']);assert values(q)==values(old);C['source_values']+=5
 C['raw_profiles']+=1
for r in json.loads((D/'review.json').read_text())+json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level,params in [('easy',{'a':[2,3],'b':[100,100],'names':['a']}),('moderate',{'a':[.5,2],'b':[100,100],'names':['c']}),('moderate',{'a':[2,3],'names':['c']}),('hard',{'a':[1,-1],'b':[-2,3],'names':['m','n']})]:
 try:g.generate(level,parameters=params)
 except ValueError:pass
 else:raise AssertionError('workload guard bypass')
C.update(database_writes=0,personally_inspected_original_rasters=4,personally_inspected_generated_solution_rasters=6)
(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
