"""Root independent actual ODE coefficients, printed algebra and strict format."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087866;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_sf_parser');x,y,Z=p.x,p.y,p.z;g=load(D.with_suffix('.py'),'root_sf_g');f=load(R/'root-source-fidelity.py','root_sf_fid');originals,S=f.check(g,K,D)
def scalar(z):
 z=z.replace(r'\frac{\text{d}y}{\text{d}x}','z').replace(r'\frac{dy}{dx}','z').replace(r'\underbrace','').replace('_{P(x)}','').replace('_{Q(x)}','').replace('_{⏟}','');return p.scalar(z.strip().rstrip('.,'))
def equation(z):
 z=z.replace('&','').strip().rstrip('.,').split(r'\,,')[0];left,right=z.split('=');return scalar(left),scalar(right)
def simplify(z):
 for C in s.denom(s.together(z)).atoms(s.cos):
  arg=C.args[0];z=z.xreplace({s.sin(2*arg):2*s.sin(arg)*C})
 return s.factor(s.trigsimp(s.cancel(z)))
def normalized(pair):
 residual=s.expand(pair[0]-pair[1]);coefficient=residual.coeff(Z);assert coefficient!=0
 residual=s.expand(s.cancel(residual/coefficient));assert s.diff(residual,Z)==1 and s.diff(residual,y,2)==0
 return simplify(residual.coeff(y)),simplify(residual.subs({y:0,Z:0}))
def same(a,b):return simplify(a-b)==0
def standard(pair):
 left,right=pair;return left.coeff(Z)==1 and not right.has(y,Z) and not (left-Z).subs(y,0) and s.diff(left-Z,y,2)==0
C=dict(records=0,actual_prompt_odes=0,printed_algebra_rows=0,strict_standard_candidates=0,choice_odes=0,standard_bank_pairs=0,separate_concluding_coefficients=0,domain_restrictions=0,source_prose_openings=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate(level,template=t,seed=n) for level,templates in g.FAMILIES.items() for t in templates for n in (631,917))
for rec in records:
 q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];raw=re.findall(r'\$\$(.*?)\$\$',md,re.S)[0];prompt=equation(raw);P,minusQ=normalized(prompt);C['actual_prompt_odes']+=1
 coefficient=s.expand(prompt[0]-prompt[1]).coeff(Z)
 # A cancelled derivative coefficient/denominator is a real domain restriction.
 if coefficient.has(y):assert r'y\ne 0' in md;C['domain_restrictions']+=1
 if coefficient.has(x) and coefficient.subs(x,0)==0:assert r'x\ne 0' in md or r'\ne 0' in md;C['domain_restrictions']+=1
 if family in ('q-8359','q-79697','rational-collect'):assert r'x\ne 0' in md;C['domain_restrictions']+=1
 if family=='q-103354':assert r'\cos' in md and r'\ne 0' in md;C['domain_restrictions']+=1
 if family=='q-8360':assert r'\sin x\ne 0' in md;C['domain_restrictions']+=1
 rows=sol.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(chr(92)*2)
 for row in rows:
  a,b=normalized(equation(row));assert same(a,P) and same(b,minusQ),(family,row);C['printed_algebra_rows']+=1
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];pairs=[equation(a[':answer/value']) for a in choices];assert len(pairs)==5
 accepted=[]
 for a,pair in zip(choices,pairs):
  st=standard(pair);A,B=normalized(pair);accepted.append(st and same(A,P) and same(B,minusQ));C['choice_odes']+=1;C['strict_standard_candidates']+=int(st)
 assert [a[':answer/id'] for a,good in zip(choices,accepted) if good]==[field[':answer-field/correct'][1]]
 for a,b in itertools.combinations(pairs,2):
  if standard(a) and standard(b):A,B=normalized(a);C1,D1=normalized(b);assert not(same(A,C1) and same(B,D1));C['standard_bank_pairs']+=1
 tail=sol.split('Now, the equation',1)[1];a=scalar(re.search(r'\$P\(x\)=(.*?)\$',tail)[1]);b=scalar(re.search(r'\$Q\(x\)=(.*?)\.\$',tail)[1]);assert same(a,P) and same(b,-minusQ);C['separate_concluding_coefficients']+=2
 source=originals.get(family,originals['q-16400'])[':question/worked-solution'];prefix=source.split(r'\begin{aligned}')[0].replace('$$\n\n$$\n\n','');assert sol.startswith(prefix);C['source_prose_openings']+=1
 if family=='q-16401':assert rows[0].count('^{2}')>=2 and len(rows)==4
 if family=='rational-collect':assert len(rows)==3 and not(s.simplify(P).is_Integer or s.simplify(minusQ).is_Integer)
 C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
