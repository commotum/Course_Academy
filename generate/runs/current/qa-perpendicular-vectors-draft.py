"""Root QA of actual printed vectors, each operand and each solving equation."""
import sys,importlib.util,json,re,hashlib,copy,string
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059731;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
base=(R/'ode-scalar-parser.py').read_text().replace('[atuvxyzijke]','[a-z]');p=type(sys)('parent_perp_scalar');exec(base,p.__dict__);s=p.s;p.locals_.update({c:s.Symbol(c,real=True) for c in string.ascii_lowercase})
g=module('parent_perp_draft',D.with_suffix('.py'))
def addends(text):
 depth=0;start=0;out=[]
 for i,ch in enumerate(text):
  if ch in '({[':depth+=1
  elif ch in ')}]':depth-=1
  elif ch in '+-' and depth==0 and i>start and text[start:i].strip():out.append(text[start:i].strip());start=i
 out.append(text[start:].strip());return out
C=dict(records=0,source_banks=0,source_values=0,source_keys=0,source_solutions=0,source_prompts=0,individual_operands=0,polynomial_rows=0,solving_equations=0,root_sign_conclusions=0)
tasks={k:set() for k in ('easy','moderate','hard')}
def check(r):
 r=r.get('record',r);q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];vectors=[]
 for m in re.finditer(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',prompt):vectors.append([p.scalar(z) for z in m[1].split(r'\\')])
 if not vectors:vectors=[[p.scalar(z) for z in m[1].split(',')] for m in re.finditer('⟨(.*?)⟩',prompt)]
 assert len(vectors)==2 and len(vectors[0])==len(vectors[1]) in (2,3)
 U,V=vectors;syms=set().union(*(z.free_symbols for v in vectors for z in v));assert len(syms)==1;x=next(iter(syms));dot=s.expand(sum(a*b for a,b in zip(U,V)));roots=set(s.solve(dot,x));restriction=re.search(r'\$'+str(x)+r'\s*([<>])\s*0',prompt);sign=1 if restriction and restriction[1]=='>' else -1 if restriction else 0
 eligible={z for z in roots if not sign or z*sign>0};assert len(eligible)==1;answer=next(iter(eligible))
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];vals=[p.scalar(a[':answer/value']) for a in choices];assert len(set(vals))==len(vals)
 assert [a[':answer/id'] for a,v in zip(choices,vals) if s.simplify(v-answer)==0]==[f[':answer-field/correct'][1]]
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt and re.search(r'\$'+str(x)+r'=\$\{\{',prompt)
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 rows=[[row.replace('& =','&=').strip() for row in block.split(r'\\')] for block in blocks]
 names=re.search(r'([a-z])⊥([a-z])',prompt).groups();u,v=names;formal='+'.join('{'+u+'}_{'+a+r'}\cdot {'+v+'}_{'+a+'}' for a in 'xyz'[:len(U)])
 assert rows[0][0].split('&=')[1].strip()==formal
 productrow=rows[0][1].split('&=')[1].strip();products=addends(productrow);assert len(products)==len(U)
 for expr,a,b in zip(products,U,V):
  left,right=expr.split(r'\cdot');assert s.simplify(p.scalar(left)-a)==s.simplify(p.scalar(right)-b)==0,(expr,a,b);C['individual_operands']+=2
 for row in rows[0][1:]:assert s.simplify(p.scalar(row.split('&=')[1])-dot)==0,(row,dot);C['polynomial_rows']+=1
 assert rows[1][0].replace(' ','')==u+r'\cdot'+v+'&=0'
 for row in rows[1][1:]:
  lhs,rhs=row.split('&=');lhs=p.scalar(lhs)
  if r'\pm' in rhs:
   assert lhs==x;z=p.scalar(rhs.replace(r'\pm',''));got={z,-z}
  else:got=set(s.solve(lhs-p.scalar(rhs),x))
  assert got==roots,(row,got,roots);C['solving_equations']+=1
 if sign:
  conclusions=re.findall(r'Therefore, \$'+str(x)+r'=(.*?)\.\$',sol);assert len(conclusions)==1 and s.simplify(p.scalar(conclusions[0])-answer)==0
  assert 'disregard the '+('negative' if sign>0 else 'positive')+' solution' in sol;C['root_sign_conclusions']+=1
 level=q[':question/difficulty'].split('/')[-1];poly=s.Poly(dot,x)
 if level=='hard':
  assert len(U)==3 and poly.degree()==2 and poly.nth(1)==0;rad=next(iter(roots))**2;assert 2<=s.denom(rad)<=6 and 2<=abs(poly.nth(2))<=6 and all(abs(z.as_coeff_Mul()[0])>=2 for z in U+V)
 tasks[level].add(str((U,V,sign)));C['records']+=1;return q
source={q[':question/math-academy-id']:q for q in json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
for spec in json.loads((D/'replay-specifications.json').read_text()):
 q=check(g.generate(spec['level'],seed=301,template=spec['template'],parameters=spec['parameters'],profile=spec.get('bank_profile')));old=source[spec['source_id']];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert {p.scalar(a[':answer/value']) for a in of[':answer-field/choices']}=={p.scalar(a[':answer/value']) for a in f[':answer-field/choices']};C['source_banks']+=1;C['source_values']+=len(f[':answer-field/choices'])
 if of.get(':answer-field/correct'):
  assert p.scalar(of[':answer-field/correct'][':answer/value'])==p.scalar(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]));C['source_keys']+=1
 normalize=lambda t:g.normalize_prose(t).replace('& =','&=')
 assert normalize(q[':question/problem'])==normalize(old[':question/problem']);C['source_prompts']+=1
 if old.get(':question/worked-solution'):assert normalize(q[':question/worked-solution'])==normalize(old[':question/worked-solution']);C['source_solutions']+=1
for r in json.loads((D/'review.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in tasks:
 for seed in range(600,624):check(g.generate(level,seed))
# Mutations retain final answer and key; force operands and intermediate equations to matter.
base=g.generate('moderate',template='square3_collect',parameters={'a':1,'b':3,'c':-1,'d':1,'e':-6,'f':2,'sign':-1})
mutations=[(r'{r}^{2}\cdot 3',r'{r}^{2}\cdot 4'),('3{r}^{2}-','4{r}^{2}-'),(r'{r}^{2} &=6',r'{r}^{2} &=7')]
for old,new in mutations:
 bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution'];assert old in text;bad['question'][':question/worked-solution']=text.replace(old,new,1)
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('mutation passed')
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'sampled_actual_tasks':{k:len(v) for k,v in tasks.items()},'negative_controls':len(mutations),'scope':'Linear/square perpendicular component equation; repeated square only explicit observed family. Hard authored same three products/collection/root restriction with small rational radicand, no generic quadratic or geometry branches.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
