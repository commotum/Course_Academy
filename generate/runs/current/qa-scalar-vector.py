"""Parent independently differentiates complete printed scalar-vector products."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186115391;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_scalar_vector',D.with_suffix('.py'));p=module('parent_product_vector_parser',R/'vector-math-parser.py')
positive=s.Symbol('positive_t',positive=True)
def equal(a,b):return a.shape==b.shape and all(s.simplify(s.trigsimp((x-y).subs(p.t,positive)))==0 for x,y in zip(a,b))
def inputs(prompt):
 raw=re.search(r'\[\\begin\{aligned\}.*?\\end\{aligned\}\]|⟨[^⟩]+⟩',prompt,re.S).group(0);v=p.vector(raw)
 scalartext=re.search(r'\$u\(t\)\s*=\s*(.*?)\$',prompt).group(1);return p.scalar(scalartext),v
def prose(text):
 text=re.sub(r'\$\$.*?\$\$',' [DISPLAY] ',text,flags=re.S);text=re.sub(r'\$[^$]*\$',' [INLINE] ',text)
 return re.sub(r'\s+',' ',text).strip()
counts=dict(source_banks=0,source_values=0,source_designations=0,source_exact_prompts=0,source_exact_solutions=0,printed_products=0,authored_levels_checked=[])
def check(r):
 q=r['question'];u,v=inputs(q[':question/problem']);answer=(u*v).diff(p.t);f=q[':question/answer-fields'][0]
 values=[p.vector(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
 assert [a[':answer/id'] for a,z in zip(f[':answer-field/choices'],values) if equal(z,answer)]==[f[':answer-field/correct'][1]]
 counts['printed_products']+=1;return u,v
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);u,v=check(r);ou,ov=inputs(old[':question/problem'])
 assert s.simplify(u-ou)==0 and equal(v,ov)
 assert r['question'][':question/problem']==old[':question/problem'];counts['source_exact_prompts']+=1
 sf=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];remaining=[p.vector(a[':answer/value']) for a in f[':answer-field/choices']]
 for a in sf[':answer-field/choices']:
  matches=[n for n,b in enumerate(remaining) if equal(p.vector(a[':answer/value']),b)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1
 if ':answer-field/correct' in sf:
  selected=next(p.vector(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(selected,p.vector(sf[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 if ':question/worked-solution' in old:
  assert old[':question/worked-solution']==r['question'][':question/worked-solution'];counts['source_exact_solutions']+=1
 for scales in ([2,-1,3],[-3,2,-2]):
  r=g.generate(c['level'],template=c['template'],parameters={'scales':scales},profile=c['bank_profile']);check(r)
  if ':question/worked-solution' in old:
   assert prose(old[':question/worked-solution'])==prose(r['question'][':question/worked-solution'])
   assert old[':question/worked-solution'].count(r'\\')==r['question'][':question/worked-solution'].count(r'\\')
for level in ('easy','moderate','hard'):
 for seed in range(30):check(g.generate(level,seed))
 counts['authored_levels_checked'].append(level)
for level in ('easy','moderate','hard'):
 for params in ({'a':-3,'b':3,'c':-3,'d':3},{'a':3,'b':-3,'c':3,'d':-3}):
  r=g.generate(level,parameters=params);check(r);r2=g.generate(level,72,parameters=params);assert r['question'][':question/id']==r2['question'][':question/id']
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
