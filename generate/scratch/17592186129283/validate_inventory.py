"""Parent reconstructs strict orientation regions from the displayed transformation."""
import importlib.util,json,re
from fractions import Fraction as F
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;R=D;K=17592186129283
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_orientation',D.with_suffix('.py'));p=module('parent_orientation_math',D/'math_parser.py')
def math(raw):return p.parse(raw.replace(r'\end{aligned}','').strip().rstrip('.,'))
def inputs(prompt):
 raw=re.search(r'⟶\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',g.normalize_prose(prompt),re.S).group(1)
 return [math(z) for z in raw.split(r'\\')]
def equal(a,b):return s.simplify(a-b)==0
def contains(spec,a,b):
 U=a-F(str(spec['h']));V=b-F(str(spec['k']));c=F(spec['coefficient']);n=spec['degree'];mode=spec['mode']
 if mode=='left':return U<0
 if mode=='right':return U>0
 if mode=='top':return V>0
 if mode=='bottom':return V<0
 if mode=='product_lt':return U*V<c
 if mode=='product_gt':return U*V>c
 if n==-1 and not U:return False
 return V<c*U**n if mode=='below' else V>c*U**n
def polynomial(expr):
 terms=[(i,j,F(str(c))) for (i,j),c in s.Poly(expr,p.u,p.v).terms()]
 return lambda a,b:sum(c*a**i*b**j for i,j,c in terms)
def relation(raw):
 raw=raw.replace('&','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip()
 a,op,b=re.fullmatch(r'(.*?)([<>])(.*)',raw).groups();return math(a)-math(b),op
def signtruth(value,op):return value>0 if op=='>' else value<0
counts=dict(raw_source_banks=0,source_values=0,source_designations=0,source_prompt_layouts=0,source_solution_layouts=0,printed_instances=0,printed_derivatives=0,printed_determinant_stages=0,strict_region_grid_checks=0,piecewise_branch_checks=0)
coords=[F(i,2) for i in range(-16,17)]
def check(r):
 q=r['question'];x,y=inputs(q[':question/problem']);ds=[s.diff(x,p.u),s.diff(x,p.v),s.diff(y,p.u),s.diff(y,p.v)];J=s.factor(ds[0]*ds[3]-ds[1]*ds[2]);op='>' if 'orientation-preserving?' in q[':question/problem'] else '<'
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);block=next(z for z in blocks if r'\cdot' in z)
 if r'\begin{vmatrix}' in block:
  entries=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',block,re.S)[-1]
  tail=block.rsplit(r'\end{vmatrix}',1)[1]
 else:
  entries=re.findall(r'=\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',block,re.S)[-1]
  tail=block.split(entries+r'\end{aligned}|',1)[1]
 actual=[math(z) for z in re.split(r'&|\\\\',entries)];assert len(actual)==4 and all(equal(a,b) for a,b in zip(actual,ds));counts['printed_derivatives']+=4
 rows=[z for z in tail.split(r'\\') if '=' in z]
 for row in rows:
  assert equal(math(row.split('=',1)[1]),J),row;counts['printed_determinant_stages']+=1
 # Exponential factors are common and strictly positive for these real graphs.
 exp_atoms=J.atoms(s.exp);polynomial_J=J
 for atom in exp_atoms:
  quotient=s.cancel(polynomial_J/atom)
  assert not quotient.has(atom);polynomial_J=quotient
 determinant=polynomial(polynomial_J)
 inequalities=next(z for z in blocks if r'\begin{aligned}' in z and ('<' in z or '>' in z))
 stages=[relation(z) for z in inequalities.split(r'\\')]
 evaluators=[]
 for expression,rel in stages:
  for atom in expression.atoms(s.exp):expression=expression/atom
  evaluators.append((polynomial(s.cancel(expression)),rel))
 f=q[':question/answer-fields'][0];specs=r['generation']['plot_specs'];correct=specs[f[':answer-field/correct'][1]]
 signatures={aid:[] for aid in specs}
 for a in coords:
  for b in coords:
   truth=signtruth(determinant(a,b),op)
   assert contains(correct,a,b)==truth,(r['generation']['template'],a,b,J,correct)
   assert all(signtruth(ev(a,b),rel)==truth for ev,rel in evaluators)
   for aid,spec in specs.items():signatures[aid].append(contains(spec,a,b))
   counts['strict_region_grid_checks']+=1
 assert len({tuple(v) for v in signatures.values()})==5
 inline=re.findall(r'\$([^$]*(?:<|>)[^$]*)\$',re.sub(r'\$\$.*?\$\$','',sol,flags=re.S))
 for n in range(0,len(inline)-1,2):
  expr,rel=relation(inline[n]);cond,cop=relation(inline[n+1])
  if not expr.has(p.v) or cond.has(p.v):continue
  for a in (F(-7),F(-3),F(1),F(4),F(7)):
   if not signtruth(cond.subs(p.u,s.Rational(a.numerator,a.denominator)),cop):continue
   for b in (F(-7),F(-2),F(0),F(3),F(7)):
    val=expr.subs({p.u:s.Rational(a.numerator,a.denominator),p.v:s.Rational(b.numerator,b.denominator)})
    assert signtruth(val,rel)==signtruth(determinant(a,b),op),(inline[n:n+2],a,b)
    counts['piecewise_branch_checks']+=1
 assert all((Path(a[':answer/value']) if a[':answer/value'].startswith('/') else Path('/media/jake/SSD/EDB/math')/a[':answer/value']).is_file() for a in f[':answer-field/choices'])
 counts['printed_instances']+=1

def task(q):
 x,y=inputs(q[':question/problem']);J=s.factor(s.diff(x,p.u)*s.diff(y,p.v)-s.diff(x,p.v)*s.diff(y,p.u))
 op='>' if 'orientation-preserving?' in q[':question/problem'] else '<'
 for atom in J.atoms(s.exp):J=s.cancel(J/atom)
 poly=s.Poly(s.expand(J),p.u,p.v);lead=poly.LC()
 if lead<0:op='<' if op=='>' else '>'
 return str(s.Poly(s.expand(J/lead),p.u,p.v).as_expr())+op+'0'

def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'entire image radio bank'} for a in f[':answer-field/choices']]

if __name__=='__main__':
 import hashlib
 replay=[]
 for c in json.loads((D/'source-cases.json').read_text()):
  r=g.generate('moderate',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r)
  old=g.QUESTIONS[c['math_academy_id']];f=old[':question/answer-fields'][c['raw_field_index']];rf=r['question'][':question/answer-fields'][0]
  norm=lambda x:x.replace('/media/jake/SSD/EDB/math/','')
  assert r['question'][':question/problem']==g.normalize_prose(old[':question/problem'])
  assert norm(r['question'][':question/worked-solution'])==g.normalize_prose(old[':question/worked-solution'])
  assert sorted(norm(a[':answer/value']) for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
  if ':answer-field/correct' in f:assert norm(next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]))==f[':answer-field/correct'][':answer/value']
  replay.append(c['template'])
 for level in g.LEVELS:
  for seed in range(8):check(g.generate(level,seed=seed))
 result={'status':'passed','counts':counts,'complete_raw_banks_replayed':len(replay),'complete_choices_replayed':len(replay)*5,'source_designation_exception':'One legacy raw field has no correct designation; current database retains one valid widget. Original evidence preserved.','hashes':{str(path.relative_to(D.parents[2])):hashlib.sha256(path.read_bytes()).hexdigest() for path in [D.with_suffix('.py'),D/'render.py',D/'math_parser.py',D/'validate_inventory.py']}}
 (D/'validation-inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
