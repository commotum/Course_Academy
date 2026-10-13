"""Parent derivative oracle uses displayed functions and evaluated abscissas."""
import importlib.util,json,re,itertools
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent; K=17592186096842; S=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_radical',S.with_suffix('.py'));p=module('parent_radical_parser',S/'validate.py')
def expected(prompt):
 match=re.search(r'y\s*=\s*([^$]+)',prompt);assert match,prompt
 fn=p.displayed(match[1]);d=s.diff(fn,p.x)
 if 'slope' in prompt.lower():
  z=p.displayed(re.search(r'\$x\s*=\s*([^$]+)',prompt)[1]);assert fn.subs(p.x,z).is_real is True
  d=s.simplify(d.subs(p.x,z));assert d.is_Rational is True,('easy slope adds radical simplification',prompt,d)
 return d
def eq(a,b):return s.cancel(s.powdenest(a,force=True)-s.powdenest(b,force=True))==0
def check(r):
 q=r['question'];e=expected(q[':question/problem']);f=q[':question/answer-fields'][0]
 vals=[(a[':answer/id'],p.displayed(a[':answer/value'])) for a in f[':answer-field/choices']]
 assert [aid for aid,v in vals if eq(v,e)]==[f[':answer-field/correct'][1]]
 assert all(not eq(a[1],b[1]) for a,b in itertools.combinations(vals,2))
 return vals
n={'source_questions':0,'radio_banks':0,'blanks':0,'source_values':0,'exact_prompts':0,'exact_existing_solutions':0,'source_designations':0,'authored_missing_solution_and_designation':0,'displayed_default_questions':0}
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(g.TEMPLATES[c['template']]['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r)
 q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'];n['exact_prompts']+=1
 if ':question/worked-solution' in old:
  assert q[':question/worked-solution']==old[':question/worked-solution'];n['exact_existing_solutions']+=1
 bank=[v for _,v in check(r)]
 for a in of[':answer-field/choices']:
  v=p.displayed(a[':answer/value']);hits=[i for i,b in enumerate(bank) if eq(v,b)];assert len(hits)==1;bank.pop(hits[0]);n['source_values']+=1
 assert not bank
 if ':answer-field/correct' in of:
  assert eq(expected(q[':question/problem']),p.displayed(of[':answer-field/correct'][':answer/value']));n['source_designations']+=1
 else:n['authored_missing_solution_and_designation']+=1
 assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
 n['source_questions']+=1;n['radio_banks' if f[':answer-field/type'].endswith('/radio') else 'blanks']+=1
for name,t in g.TEMPLATES.items():
 for seed in range(12):check(g.generate(t['level'],seed,template=name));n['displayed_default_questions']+=1
n['domain_equivalence_note']='Symbolic radical normalizations use the explicit positive-radicand question domain; native fractional-power limitation is reported separately.'
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
