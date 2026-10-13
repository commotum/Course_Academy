"""Parent computes local area from printed transformations, points and stages."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186129282;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_local_area',D.with_suffix('.py'));p=module('parent_area_parser',D.parents[0]/'17592186129263/math_parser.py')
def math(text):return p.parse(text.replace('³','^{3}'))
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def area(text):
 text=text.replace(r'\delta A','').replace('δA','').replace('δ A','').replace(r'\,','').strip()
 return math(text) if text else s.Integer(1)
def inputs(prompt):
 matrix=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',prompt)[-1]
 x,y=[math(z) for z in matrix.split(r'\\')]
 point=re.search(r'located at the point \$\(([^)]+)\)\$',prompt).group(1)
 U,V=[math(z) for z in point.split(',')];return x,y,U,V
def prose(text):
 text=re.sub(r'\$\$.*?\$\$',' [DISPLAY] ',text,flags=re.S);text=re.sub(r'\$.*?\$',' [INLINE] ',text,flags=re.S)
 return re.sub(r'[\s,.]+',' ',text).strip()
counts=dict(raw_source_banks=0,source_values=0,original_designations_present=0,original_designations_matched=0,corrected_designations=0,missing_designations=0,source_prose_layouts=0,printed_instances=0,printed_derivative_entries=0,printed_scalar_rows=0)
def check(r):
 q=r['question'];x,y,U,V=inputs(q[':question/problem']);ds=[s.diff(x,p.u),s.diff(x,p.v),s.diff(y,p.u),s.diff(y,p.v)]
 det=ds[0]*ds[3]-ds[1]*ds[2];val=s.simplify(s.trigsimp(det.subs({p.u:U,p.v:V})));C=s.Abs(val)
 f=q[':question/answer-fields'][0];values=[area(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
 assert all(z.is_nonnegative is True for z in values)
 assert [a[':answer/id'] for a,z in zip(f[':answer-field/choices'],values) if equal(z,C)]==[f[':answer-field/correct'][1]]
 sol=q[':question/worked-solution'];matrices=re.findall(r'\\begin\{matrix\}(.*?)\\end\{matrix\}',sol);assert len(matrices)==2
 entries=[math(z) for z in re.split(r'&|\\\\',matrices[1])];assert len(entries)==4 and all(equal(a,b) for a,b in zip(entries,ds));counts['printed_derivative_entries']+=4
 body=sol.split('Computing the corresponding Jacobian determinant, we obtain the following:')[1].split('Therefore, we have')[0]
 evaluated=False
 for row in body.split(r'\\'):
  if 'big|' in row:evaluated=True;continue
  if row.startswith('& =') and 'matrix' not in row:
   raw=row[3:].split(r'\end{aligned}')[0];expected=val if evaluated else det
   assert equal(math(raw),expected),row;counts['printed_scalar_rows']+=1
 last=sol.split('Therefore, we have')[1];signed=re.search(r'\|([^|]+)\|',last).group(1);assert equal(math(signed),val)
 answer=re.search(r'& =(.+?)\\end\{aligned\}',last).group(1).strip().rstrip('.');assert equal(area(answer),C)
 counts['printed_instances']+=1
 return x,y,U,V
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']]
 for bank in c['bank_profiles']:
  r=g.generate('easy',parameters=c['parameters'],profile=bank['bank_profile']);printed=check(r);assert all(equal(a,b) for a,b in zip(inputs(old[':question/problem']),printed))
  sf=old[':question/answer-fields'][bank['source_field_index']];f=r['question'][':question/answer-fields'][0];remaining=[area(a[':answer/value']) for a in f[':answer-field/choices']]
  for a in sf[':answer-field/choices']:
   matches=[i for i,b in enumerate(remaining) if equal(area(a[':answer/value']),b)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
  assert not remaining;counts['raw_source_banks']+=1
  if ':answer-field/correct' not in sf:counts['missing_designations']+=1
  else:
   counts['original_designations_present']+=1
   actual=next(area(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);expected=area(sf[':answer-field/correct'][':answer/value'])
   if equal(actual,expected):counts['original_designations_matched']+=1
   else:
    assert c['source_id']=='q-161831' and bank['bank_profile']=='legacy_exp_product' and equal(expected,1) and equal(actual,2)
    counts['corrected_designations']+=1
  assert prose(old[':question/worked-solution'])==prose(r['question'][':question/worked-solution']),c['source_id']
  assert old[':question/worked-solution'].count(r'\\')==r['question'][':question/worked-solution'].count(r'\\'),c['source_id']
 counts['source_prose_layouts']+=1
for level in ('easy','moderate','hard'):
 for seed in range(30):check(g.generate(level,seed))
for template,(level,_,params) in g.TEMPLATES.items():
 for seed in (13,42,77):
  r=g.generate(level,seed,template=template);check(r);fixed=g.generate(level,seed+18,template=template,parameters=r['generation']['parameters'])
  assert fixed['question'][':question/id']==r['question'][':question/id']
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
