"""Parent reconstructs concrete cross/dot setup and every printed vector stage."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186198389;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_repeated_flux',D.with_suffix('.py'));p=module('parent_repeated_parser',R/'vector-math-parser.py')
x,y,z,u,v=p.x,p.y,p.z,p.u,p.v
math=p.scalar
def equal(a,b):return s.expand(a-b)==0
def vectors(text):return re.findall('⟨([^⟨⟩]+)⟩',text)
def vector(text):return s.Matrix([math(a) for a in text.split(r',\,')])
def objects(prompt):
 F=vector(vectors(prompt)[0]);G=math(re.search(r'defined by \$z=(.*?)\$',prompt).group(1));bounds=[int(a) for a in re.search(r'for \$(-?\d+)\\le x\\le (-?\d+)\$ and \$(-?\d+)\\le y\\le (-?\d+)\.\$',prompt).groups()];return F,G,bounds
counts=dict(source_banks=0,source_values=0,source_designations=0,source_prose_layouts=0,printed_instances=0,vector_stages=0,minor_determinants=0,dot_stages=0,final_integral_fields=0)
def check(r):
 q=r['question'];F,G,bounds=objects(q[':question/problem']);RR=s.Matrix([u,v,G.subs({x:u,y:v})]);du=RR.diff(u);dv=RR.diff(v);normal=du.cross(dv);pull=F.subs(dict(zip((x,y,z),RR)),simultaneous=True);answer=s.expand(pull.dot(normal));f=q[':question/answer-fields'][0]
 values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
 assert [a[':answer/id'] for a,z in zip(f[':answer-field/choices'],values) if equal(z,answer)]==[f[':answer-field/correct'][1]]
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==8
 assert all(equal(a,b) for a,b in zip(vector(vectors(blocks[1])[0]),RR))
 assert bounds==[int(a) for a in re.search(r'(-?\d+)\\le u\\le (-?\d+).*?(-?\d+)\\le v\\le (-?\d+)',blocks[2]).groups()]
 allowed=(F,RR,du,dv,normal,pull)
 for text in vectors(q[':question/worked-solution']):
  if '∂' in text:continue
  def determinant(match):
   A,B=match[1].split(r'\\');a,b=[math(t) for t in A.split('&')];c,d=[math(t) for t in B.split('&')];counts['minor_determinants']+=1;return '('+s.latex(a*d-b*c)+')'
  text=re.sub(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',determinant,text)
  value=vector(text);assert any(all(equal(a,b) for a,b in zip(value,obj)) for obj in allowed),(r['generation']['template'],text);counts['vector_stages']+=1
 for row in blocks[6].removeprefix('\n\\begin{aligned}').removesuffix('\\end{aligned}\n').split(' & =')[1:]:
  rhs=row.split(r'\\')[0].strip().replace(r'\end{aligned}','').strip().rstrip('.')
  if vectors(rhs):continue
  assert equal(math(rhs),answer),(r['generation']['template'],rhs,answer);counts['dot_stages']+=1
 finalvec=vector(vectors(blocks[7])[0]);assert all(equal(a,b) for a,b in zip(finalvec,F));counts['final_integral_fields']+=1
 finalrow=blocks[7].split(' & =')[-1].replace(r'\end{aligned}','').strip().rstrip('.')
 actualbounds=[int(a) for pair in re.findall(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',finalrow) for a in pair];assert actualbounds==bounds
 actual=finalrow.split('}',4)[-1] if False else re.sub(r'^\{\\int \}_\{-?\d+\}\^\{-?\d+\}\{\\int \}_\{-?\d+\}\^\{-?\d+\}','',finalrow).split(r'\,\text{d}v',1)[0];assert equal(math(actual),answer)
 counts['printed_instances']+=1;return F,G,bounds
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 sid=c.get('math_academy_id',c['source_id'].removesuffix('-legacy'));old=qs[sid];r=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')));F,G,b=check(r);oF,oG,ob=objects(old[':question/problem']);assert all(equal(a,b) for a,b in zip(F,oF)) and equal(G,oG) and b==ob
 sf=old[':question/answer-fields'][c.get('raw_field_index',c.get('source_field_index',0))];nf=r['question'][':question/answer-fields'][0];remaining=[math(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in sf[':answer-field/choices']:
  matches=[n for n,b in enumerate(remaining) if equal(math(a[':answer/value']),b)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1
 if ':answer-field/correct' in sf:
  selected=next(math(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert equal(selected,math(sf[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 assert re.split(r'\$\$.*?\$\$',old[':question/worked-solution'],flags=re.S)==re.split(r'\$\$.*?\$\$',r['question'][':question/worked-solution'],flags=re.S)
 assert [len(z.split(' & =')) for z in re.findall(r'\$\$(.*?)\$\$',old[':question/worked-solution'],re.S)]==[len(z.split(' & =')) for z in re.findall(r'\$\$(.*?)\$\$',r['question'][':question/worked-solution'],re.S)];counts['source_prose_layouts']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
