"""Parent derives vector composition from printed functions, banks and stages."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186115392;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_vector_chain',D.with_suffix('.py'));p=module('parent_chain_parser',R/'vector-math-parser.py')
positive=s.Symbol('positive_t',positive=True)
def equal(a,b):return a.shape==b.shape and all(s.simplify(s.trigsimp((x-y).subs(p.t,positive)))==0 for x,y in zip(a,b))
def inputs(prompt):
 spans=re.findall(r'\$([^$]+)\$',prompt);return p.vector(spans[0].split('=',1)[1]),p.scalar(spans[1].split('=',1)[1])
def rows(raw):
 start=r'\begin{aligned}';end=r'\end{aligned}';raw=raw.strip()
 if raw.startswith(start):raw=raw[len(start):-len(end)]
 parts=[];depth=0;last=0;i=0
 while i<len(raw):
  if raw.startswith(start,i):depth+=1;i+=len(start)
  elif raw.startswith(end,i):depth-=1;i+=len(end)
  elif raw.startswith(r'\\',i) and depth==0:parts.append(raw[last:i].strip());i+=2;last=i
  else:i+=1
 parts.append(raw[last:].strip());assert depth==0;return parts

def read_stage(raw,H,HP):
 for variable in (p.u,p.t):
  prefix=r'\frac{\text{d}}{\text{d}'+str(variable)+r'}\left('
  while prefix in raw:
   start=raw.index(prefix);a=start+len(prefix);i=a;depth=1
   while depth:
    assert i<len(raw)
    if raw.startswith(r'\left(',i):depth+=1;i+=len(r'\left(')
    elif raw.startswith(r'\right)',i):depth-=1;i+=len(r'\right)')
    else:i+=1
   inside=raw[a:i-len(r'\right)')];value=s.diff(p.scalar(inside),variable)
   raw=raw[:start]+'('+s.latex(value)+')'+raw[i:]
 raw=raw.replace(r'u^{′}(t)','('+s.latex(HP)+')').replace('u(t)','('+s.latex(H)+')')
 if not any(z in raw for z in ('aligned','⟨','i','j','k')):return p.scalar(raw)
 if raw.startswith(r'[\begin{aligned}'):
  cut=raw.index(r'\end{aligned}]')+len(r'\end{aligned}]');v=p.vector(raw[:cut]);rest=raw[cut:].strip()
 elif raw.startswith('⟨'):
  cut=raw.index('⟩')+1;v=p.vector(raw[:cut]);rest=raw[cut:].strip()
 else:return p.vector(raw)
 return v*p.scalar(rest.removeprefix(r'\cdot').strip()) if rest else v
counts=dict(source_banks=0,source_values=0,source_designations=0,source_prompt_math=0,source_solution_prose_layouts=0,printed_instances=0,printed_derivative_rows=0,printed_substitution_rows=0)
def check(r):
 q=r['question'];F,H=inputs(q[':question/problem']);HP=s.diff(H,p.t);DF=F.diff(p.u);C=DF.subs(p.u,H)*HP;f=q[':question/answer-fields'][0]
 values=[p.vector(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
 assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if equal(v,C)]==[f[':answer-field/correct'][1]]
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==3
 for row in rows(blocks[1]):
  for raw in row.split('& =',1)[1].split('='):
   value=read_stage(raw.strip(),H,HP)
   if isinstance(value,s.MatrixBase):assert equal(value,DF),(r['generation']['template'],row)
   else:assert s.simplify(value-HP)==0,(r['generation']['template'],row)
  counts['printed_derivative_rows']+=1
 for row in rows(blocks[2])[1:]:
  value=read_stage(row.split('& =',1)[1].strip(),H,HP);assert equal(value,C),(r['generation']['template'],row);counts['printed_substitution_rows']+=1
 if q.get(':question/difficulty')==':question.difficulty/hard':assert len(s.Poly(C[2],p.t).terms())==5
 counts['printed_instances']+=1;return F,H
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);F,H=check(r);oF,oH=inputs(old[':question/problem']);assert equal(F,oF) and s.simplify(H-oH)==0;counts['source_prompt_math']+=1
 sf=old[':question/answer-fields'][0];nf=r['question'][':question/answer-fields'][0];remaining=[p.vector(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in sf[':answer-field/choices']:
  matches=[n for n,b in enumerate(remaining) if equal(p.vector(a[':answer/value']),b)];assert len(matches)==1,(c['source_id'],a[':answer/value'],p.vector(a[':answer/value']),remaining);remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1
 selected=next(p.vector(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert equal(selected,p.vector(sf[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 assert re.sub(r'\$\$.*?\$\$','[MATH]',old[':question/worked-solution'],flags=re.S)==re.sub(r'\$\$.*?\$\$','[MATH]',r['question'][':question/worked-solution'],flags=re.S)
 assert [len(rows(b)) for b in re.findall(r'\$\$(.*?)\$\$',old[':question/worked-solution'],re.S)]==[len(rows(b)) for b in re.findall(r'\$\$(.*?)\$\$',r['question'][':question/worked-solution'],re.S)];counts['source_solution_prose_layouts']+=1
for r in json.loads((D/'review.json').read_text()):check(r)
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for name,level in g.TEMPLATES.items():
 for seed in (37,82):check(g.generate(level,seed,template=name))
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
