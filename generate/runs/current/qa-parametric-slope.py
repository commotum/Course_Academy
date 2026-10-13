"""Parent derivative/evaluation oracle reads printed curves and the printed t."""
import importlib.util,json,re,itertools
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186083243;S=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_parametric_slope',S.with_suffix('.py'));p=module('parent_parametric_parser',S/'mathcheck.py')
def eq(a,b):return s.trigsimp(s.simplify(a-b))==0
def read(prompt):
 x,y=p.prompt_curves(prompt)
 u=p.parse(re.search(r'where \$t=([^$]+)',prompt)[1].rstrip('.,'))
 dx,dy=s.diff(x,p.T),s.diff(y,p.T)
 assert dx.subs(p.T,u)!=0
 return x,y,u,s.simplify(dy.subs(p.T,u)/dx.subs(p.T,u))
def check(r):
 q=r['question'];x,y,u,m=read(q[':question/problem']);f=q[':question/answer-fields'][0]
 vals=[(a[':answer/id'],p.parse(a[':answer/value'])) for a in f[':answer-field/choices']]
 assert [aid for aid,v in vals if eq(v,m)]==[f[':answer-field/correct'][1]]
 assert all(not eq(a[1],b[1]) for a,b in itertools.combinations(vals,2))
 assert all(v.is_real is not False and not v.has(s.nan,s.zoo,s.oo) for _,v in vals)
 return vals
def skeleton(text):
 text=re.sub(r'!\[[^]]*\]\([^)]*\)','<plot>',text)
 text=re.sub(r'\$\$.*?\$\$|\$(?!\$).*?\$', '<math>',text,flags=re.S)
 return re.sub(r'\s+',' ',text).strip()
n={'source_questions':0,'complete_radio_banks':0,'blanks':0,'source_values':0,'source_designations':0,'displayed_default_questions':0,'shared_prose_layouts':0}
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((S/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(g.TEMPLATES[c['template']][0],template=c['template'],parameters=c['parameters'],profile=c.get('profile',c['bank_profile']));values=check(r)
 q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 oc,nc=read(old[':question/problem']),read(q[':question/problem'])
 assert all(eq(a,b) for a,b in zip(oc,nc))
 assert skeleton(old[':question/worked-solution'])==skeleton(q[':question/worked-solution']);n['shared_prose_layouts']+=1
 bank=[v for _,v in values]
 for a in of[':answer-field/choices']:
  val=p.parse(a[':answer/value']);hits=[i for i,b in enumerate(bank) if eq(val,b)];assert len(hits)==1;bank.pop(hits[0]);n['source_values']+=1
 assert not bank
 assert eq(p.parse(of[':answer-field/correct'][':answer/value']),nc[3]);n['source_designations']+=1
 assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
 n['source_questions']+=1;n['complete_radio_banks' if f[':answer-field/type'].endswith('/radio') else 'blanks']+=1
for name,t in g.TEMPLATES.items():
 for seed in range(6):check(g.generate(t[0],seed,template=name));n['displayed_default_questions']+=1
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
