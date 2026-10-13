"""Parent oracle derives Jacobians from the actual displayed functions and point."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186129263;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_evaluated_jacobian',D.with_suffix('.py'));p=module('parent_jacobian_scalar',D/'math_parser.py')
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def inputs(prompt):
 matrices=re.findall(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',prompt)
 assert len(matrices)==4
 return [p.parse(z) for m in (matrices[1],matrices[3]) for z in m.split(r'\\')]
def prose(text):
 text=re.sub(r'\$\$.*?\$\$',' [DISPLAY] ',text,flags=re.S)
 text=re.sub(r'\$.*?\$',' [INLINE] ',text,flags=re.S)
 return re.sub(r'[\s,.]+',' ',text).strip()
counts=dict(source_banks=0,source_values=0,source_designations=0,source_solution_layouts=0,printed_instances=0,printed_derivatives=0,printed_determinant_rows=0,numeric_stages=0)
def check(r):
 q=r['question'];x,y,U,V=inputs(q[':question/problem']);ds=[s.diff(x,p.u),s.diff(x,p.v),s.diff(y,p.u),s.diff(y,p.v)]
 det=s.expand(ds[0]*ds[3]-ds[1]*ds[2]);val=s.simplify(s.trigsimp(det.subs({p.u:U,p.v:V})))
 f=q[':question/answer-fields'][0];values=[p.parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
 assert [a[':answer/id'] for a,z in zip(f[':answer-field/choices'],values) if equal(z,val)]==[f[':answer-field/correct'][1]]
 sol=q[':question/worked-solution'];der=sol.split('First, we find the partial derivatives:')[1].split('$$')[1]
 actual=[]
 for raw in re.split(r'&=',der)[1:]:actual.append(p.parse(re.split(r'&\\quad|\\\\|\\end\{aligned\}',raw)[0]))
 assert len(actual)==4 and all(equal(a,b) for a,b in zip(actual,ds))
 counts['printed_derivatives']+=4
 determinant_part=sol.split('Therefore, the corresponding Jacobian determinant is')[1].split('Finally, when')[0]
 for row in determinant_part.split(r'\\'):
  if row.startswith('&=') and 'matrix' not in row:
   assert equal(p.parse(row[2:].split(r'\end{aligned}')[0].strip().rstrip('.')),det),row
   counts['printed_determinant_rows']+=1
 final=sol.rsplit('$$',2)[1];stages=final.split('}=',1)[1].strip().rstrip('.').split('=')
 assert len(stages)==2 and all(equal(p.parse(z),val) for z in stages)
 counts['numeric_stages']+=len(stages);counts['printed_instances']+=1
 return x,y,U,V,val
source=json.loads((R/'sources'/f'{K}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate('easy',parameters=c['parameters'],profile=c['bank_profile']);check(r)
 assert all(equal(a,b) for a,b in zip(inputs(old[':question/problem']),inputs(r['question'][':question/problem'])))
 assert old[':question/worked-solution'].count(r'\\')==r['question'][':question/worked-solution'].count(r'\\')
 assert prose(old[':question/worked-solution'])==prose(r['question'][':question/worked-solution']),c['source_id']
 sf=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];remaining=[p.parse(a[':answer/value']) for a in f[':answer-field/choices']]
 for a in sf[':answer-field/choices']:
  matches=[i for i,b in enumerate(remaining) if equal(p.parse(a[':answer/value']),b)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining
 selected=next(p.parse(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(selected,p.parse(sf[':answer-field/correct'][':answer/value']))
 counts['source_banks']+=1;counts['source_designations']+=1;counts['source_solution_layouts']+=1
for level in ('easy','moderate','hard'):
 for seed in range(30):check(g.generate(level,seed))
for template,(level,_) in g.TEMPLATES.items():
 for seed in (53,83,111):
  r=g.generate(level,seed,template=template);check(r)
  fixed=g.generate(level,seed+17,template=template,parameters=r['generation']['parameters'])
  assert fixed['question'][':question/id']==r['question'][':question/id']
  assert fixed['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
