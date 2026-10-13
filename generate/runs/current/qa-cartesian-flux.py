"""Parent reconstructs Cartesian flux from printed fields, graphs and bounds."""
import importlib.util,itertools,json,re
from functools import lru_cache
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186198379;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_cartesian_flux',D.with_suffix('.py'));p=module('parent_cartesian_parser',R/'vector-math-parser.py')
x,y,z=p.x,p.y,p.z;xp,yp=s.symbols('positive_x positive_y',positive=True)
def math(raw):return p.scalar(raw.strip().replace(r'\!','').replace(r'\:',''))
def equal(a,b):return s.simplify(s.trigsimp((a-b).subs({x:xp,y:yp})))==0
@lru_cache(None)
def primitive(expression,var):
 terms=s.Add.make_args(s.expand(expression));return sum((integrate_term(term,var) for term in terms),s.S.Zero)
@lru_cache(None)
def integrate_term(term,var):
 coefficient,kernel=term.as_coeff_Mul();return coefficient*integrate_kernel(kernel,var)
@lru_cache(None)
def integrate_kernel(kernel,var):return s.integrate(kernel,var)
def definite(expression,var,lo,hi):
 antiderivative=primitive(expression,var);return s.simplify(antiderivative.subs(var,hi)-antiderivative.subs(var,lo))
def objects(prompt):
 raw=re.search('⟨(.*?)⟩',prompt.replace(r'\left\langle','⟨').replace(r'\right\rangle','⟩')).group(1);F=s.Matrix([math(z) for z in raw.split(r',\,')]);G=math(re.search(r'\$z=(.*?)\$',prompt).group(1))
 domain=re.search(r' for \$(.*?)\\le x\\le (.*?)\$ and \$(.*?)\\le y\\le (.*?)\.\$',prompt);bounds=[math(a) for a in domain.groups()];return F,G,bounds
counts=dict(source_banks=0,source_values=0,source_designations=0,source_prose_layouts=0,printed_instances=0,partial_rows=0,substituted_components=0,integration_rows=0,formal_reversed_domain_replays=0)
def check(r):
 q=r['question'];F,G,bounds=objects(q[':question/problem']);lo,hi,bottom,top=bounds;normal=s.Matrix([-s.diff(G,x),-s.diff(G,y),1]);sub=F.subs(z,G);H=s.simplify(s.trigsimp(sub.dot(normal)).subs({x:xp,y:yp})).subs({xp:x,yp:y});I=definite(H,y,bottom,top);answer=definite(I,x,lo,hi)
 formal=r['generation']['quarantined_source_domain']
 if formal:assert r['generation']['template']=='q-161481';counts['formal_reversed_domain_replays']+=1
 else:
  for j in range(1,10):assert (top-bottom).subs(x,lo+(hi-lo)*s.Rational(j,10))>0
 f=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
 assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if equal(v,answer)]==[f[':answer-field/correct'][1]]
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 for row,var in zip(blocks[1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ '),(x,y)):
  assert equal(math(row.rsplit('=',1)[1]),s.diff(G,var));counts['partial_rows']+=1
 components=re.findall(r'\\underbrace\{(.*?)\}_\{[PQR]\}',blocks[-2]);assert len(components)==3
 for text,expected in zip(components,sub):assert equal(math(text),expected);counts['substituted_components']+=1
 for row in blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ '):
  rhs=row.split(' & =',1)[1]
  if 'partial' in rhs:continue
  if r'\left[' in rhs:
   value=math(rhs.split(r'\left[',1)[1].split(r'\right]',1)[0]);is_inner=r'\mathrm{d}x' in rhs;assert equal(s.diff(value,y if is_inner else x),H if is_inner else I)
  elif r'\iint_D' in rhs or r'\int_' in rhs:
   value=math(rhs.split(r'\left(',1)[1].rsplit(r'\right)',1)[0]);has_y=r'\mathrm{d}y' in rhs;is_domain=r'\iint_D' in rhs;assert equal(value,H if (has_y or is_domain) else I)
  else:assert equal(math(rhs),answer)
  counts['integration_rows']+=1
 counts['printed_instances']+=1;return F,G,bounds
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);F,G,b=check(r);oF,oG,ob=objects(old[':question/problem']);assert all(equal(a,b) for a,b in zip(F,oF)) and equal(G,oG) and all(equal(a,b) for a,b in zip(b,ob))
 sf=old[':question/answer-fields'][0];nf=r['question'][':question/answer-fields'][0];remaining=[math(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in sf[':answer-field/choices']:
  matches=[n for n,b in enumerate(remaining) if equal(math(a[':answer/value']),b)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1
 selected=next(math(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert equal(selected,math(sf[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 assert re.split(r'\$\$\n.*?\n\$\$',old[':question/worked-solution'],flags=re.S)==re.split(r'\$\$\n.*?\n\$\$',r['question'][':question/worked-solution'],flags=re.S)
 assert [len(z.split(r' \\ ')) for z in re.findall(r'\$\$\n(.*?)\n\$\$',old[':question/worked-solution'],re.S)]==[len(z.split(r' \\ ')) for z in re.findall(r'\$\$\n(.*?)\n\$\$',r['question'][':question/worked-solution'],re.S)];counts['source_prose_layouts']+=1
for r in json.loads((D/'review.json').read_text()):check(r)
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
