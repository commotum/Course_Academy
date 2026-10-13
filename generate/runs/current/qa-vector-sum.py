"""Parent derives sum/constant-rule answers from actual printed vector functions."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186115390;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_vector_sum',D.with_suffix('.py'));p=module('parent_vector_parser',R/'vector-math-parser.py')
def equal(a,b):return a.shape==b.shape and all(s.simplify(s.trigsimp(x-y))==0 for x,y in zip(a,b))
def inputs(prompt):
 if '⟨' in prompt:fs=[p.vector(z) for z in re.findall('⟨[^⟩]+⟩',prompt)]
 elif r'[\begin{aligned}' in prompt:fs=[p.vector(z) for z in re.findall(r'\[\\begin\{aligned\}.*?\\end\{aligned\}\]',prompt)]
 else:
  fs=[p.vector(z) for z in re.findall(r'[fgh]\(t\)\s*&\s*=\s*(.*?)(?:\s+\\\\\s*|\\end\{aligned\})',prompt)]
 target=re.search(r'\$([^$]+)\$',prompt).group(1)
 pairs=re.findall(r'([+-]?\s*\d*)\s*([fgh])\(t\)',target);assert len(pairs)==len(fs),(target,fs)
 coeff=[]
 for token,name in pairs:
  token=token.replace(' ','');coeff.append(-1 if token=='-' else 1 if token in ('','+') else int(token))
 point=re.search(r'at \$t\s*=\s*(-?\d+)',prompt);point=s.Integer(point.group(1)) if point else None
 return fs,coeff,point
def expected(prompt):
 fs,coeff,point=inputs(prompt);result=sum((c*f.diff(p.t) for c,f in zip(coeff,fs)),s.zeros(3,1))
 return result.subs(p.t,point).applyfunc(s.simplify) if point is not None else result
def prose(text):
 text=re.sub(r'\$\$.*?\$\$',' [DISPLAY] ',text,flags=re.S);text=re.sub(r'\$[^$]*\$',' [INLINE] ',text)
 return re.sub(r'\s+',' ',text).strip()
counts=dict(source_banks=0,source_values=0,source_designations=0,shared_source_solution_layouts=0,printed_instances=0)
def check(r):
 q=r['question'];answer=expected(q[':question/problem']);f=q[':question/answer-fields'][0]
 values=[p.vector(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
 assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if equal(v,answer)]==[f[':answer-field/correct'][1]]
 fs,coeff,point=inputs(q[':question/problem'])
 if point is not None:
  for fun in fs:
   for expression in fun:
    assert not expression.subs(p.t,point).has(s.zoo,s.oo,s.nan)
    assert all(log.args[0].subs(p.t,point)>0 for log in expression.atoms(s.log))
 counts['printed_instances']+=1
 return fs,coeff,point
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);new_inputs=check(r);old_inputs=inputs(old[':question/problem'])
 assert new_inputs[1:]==old_inputs[1:]
 for n,(a,b) in enumerate(zip(old_inputs[0],new_inputs[0])):
  if c['source_id']=='q-128452' and n==0:
   assert equal(a[:2,:],b[:2,:]);assert a[2]==s.log(2*p.t) and b[2]==s.log(-2*p.t);assert s.simplify(s.diff(a[2]-b[2],p.t))==0
  else:assert equal(a,b)
 sf=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];remaining=[p.vector(a[':answer/value']) for a in f[':answer-field/choices']]
 for a in sf[':answer-field/choices']:
  matches=[n for n,b in enumerate(remaining) if equal(p.vector(a[':answer/value']),b)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1
 if ':answer-field/correct' in sf:
  selected=next(p.vector(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(selected,p.vector(sf[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 if ':question/worked-solution' in old:
  assert prose(old[':question/worked-solution'])==prose(r['question'][':question/worked-solution']),c['source_id']
  assert old[':question/worked-solution'].count(r'\\')==r['question'][':question/worked-solution'].count(r'\\'),c['source_id']
  counts['shared_source_solution_layouts']+=1
for level in ('easy','moderate','hard'):
 for seed in range(30):check(g.generate(level,seed))
for name,level in g.TEMPLATES.items():
 for seed in (42,71,91):check(g.generate(level,seed,template=name))
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
