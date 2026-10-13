"""Parent primitive oracle reads displayed integrands and complete option banks."""
import importlib.util,json,re,itertools
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186064245;S=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_parts',S.with_suffix('.py'));p=module('parent_parts_parser',S/'validate.py');X=p.X
def zero(e):return s.simplify(e)==0
def expected(prompt):
 displayed=re.findall(r'\$([^$]+)\$',prompt)[0];displayed=displayed.replace(r'\intx',r'\int x')
 body=displayed.split(r'\int',1)[1];body=re.split(r'(?:\\(?:text|textrm)\{d\}x|dx)',body)[0]
 return p.parse(body)
def check(r):
 q=r['question'];integrand=expected(q[':question/problem']);f=q[':question/answer-fields'][0]
 values=[(a[':answer/id'],p.parse(a[':answer/value'])) for a in f[':answer-field/choices']]
 assert [aid for aid,v in values if zero(s.diff(v,X)-integrand)]==[f[':answer-field/correct'][1]]
 assert all(not zero(s.diff(a[1]-b[1],X)) for a,b in itertools.combinations(values,2))
 assert all(a[':answer/value'].endswith('+C') for a in f[':answer-field/choices'])
 return values
n={'source_questions':0,'complete_banks':0,'source_values':0,'source_designations':0,'authored_missing_designation':0,'shared_prose_and_solution_layouts':0,'displayed_default_questions':0}
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(g.TEMPLATES[c['template']][0],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);values=check(r)
 q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert zero(expected(old[':question/problem'])-expected(q[':question/problem']))
 assert p.skeleton(old[':question/problem'])==p.skeleton(q[':question/problem'])
 if ':question/worked-solution' in old:
  assert p.skeleton(old[':question/worked-solution'])==p.skeleton(q[':question/worked-solution']);n['shared_prose_and_solution_layouts']+=1
 bank=[v for _,v in values]
 for a in of[':answer-field/choices']:
  v=p.parse(a[':answer/value']);hits=[i for i,b in enumerate(bank) if zero(s.diff(v-b,X))];assert len(hits)==1
  bank.pop(hits[0]);n['source_values']+=1
 assert not bank
 if ':answer-field/correct' in of:
  assert zero(s.diff(p.parse(of[':answer-field/correct'][':answer/value']),X)-expected(q[':question/problem']));n['source_designations']+=1
 else:n['authored_missing_designation']+=1
 assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
 n['source_questions']+=1;n['complete_banks']+=1
for name,t in g.TEMPLATES.items():
 for seed in range(10):check(g.generate(t[0],seed,template=name));n['displayed_default_questions']+=1
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
