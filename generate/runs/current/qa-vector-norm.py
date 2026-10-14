"""Parent reads actual two-dimensional vector operands, norm stages and banks."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059714;D=R.parents[2]/f'generate/scratch/{K}-draft'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
P=module('root_norm_scalar',R/'ode-scalar-parser.py');G=module('root_norm_generator',D.with_suffix('.py'));F=module('root_norm_fidelity',R/'root-source-fidelity.py')
originals,fidelity=F.check(G,K,D)
comp=json.loads((D/'calculator-requirements.json').read_text());assert comp==json.loads((R/'refresh-2026-10-14/calculator-requirements.json').read_text())
flags={q[':question/math-academy-id']:q.get(':question/requires-calculator') for k,q in comp['records'] if k==K and ':question/math-academy-id' in q}
C=dict(records=0,actual_component_pairs=0,operative_norm_rows=0,choice_values=0,criterion_pairs=0,source_prose_masks=0,calculator_flags=0,complete_method_banks=0,level_domain_checks=0)
def scalar(t):return P.scalar(t.strip().rstrip('.,'))
def mask(t):
 t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S)
 return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
def check(r,raw=False):
 q,meta=r['question'],r['generation'];prompt=q[':question/problem'];mid=meta['template'];m=re.search(r'⟨(.*?),(.*?)⟩',prompt);assert m
 x,y=map(scalar,m.groups());n=s.simplify(x*x+y*y);target=s.sqrt(n);C['actual_component_pairs']+=1
 if not raw:
  level=q[':question/difficulty'].split('/')[-1]
  assert x and y and x*x!=y*y
  if level=='easy':assert all(a.is_Integer and 1<=abs(a)<=12 for a in (x,y))
  elif level=='moderate':assert all(a.is_Rational and not a.is_Integer and 2<=a.q<=5 and 1<=abs(a.p)<=15 for a in (x,y)) and x.q!=y.q
  else:
   components=[a.as_coeff_Mul() for a in (x,y)];assert all(a.is_Rational and 1<=abs(a.p)<=9 and 2<=a.q<=5 and s.simplify(b*b) in (2,3,5,6,7) for a,b in components)
   assert components[0][0].q!=components[1][0].q and s.simplify(components[0][1]**2-components[1][1]**2)!=0
  C['level_domain_checks']+=1
 assert (':question/requires-calculator' in q)==(flags.get(mid) is not None)
 if flags.get(mid) is not None:assert q[':question/requires-calculator'] is flags[mid] and 'scientific calculator' in prompt;C['calculator_flags']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];block=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(block)==1
  rows=block[0].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2)
  assert len(rows)==(4 if mid=='q-18047' else 6 if mid=='q-18048' else 5)
  assert 'x' in rows[0] and 'y' in rows[0] and rows[0].count('^{2}')+rows[0].count('^{{2}}')>=2
  for row in rows[1:]:
   rhs=row.split('=')[1];assert s.simplify(scalar(rhs)**2-n)==0 and scalar(rhs)>=0,(mid,x,y,row);C['operative_norm_rows']+=1
  # The actual squared operands and evaluated-square stages cannot be replaced
  # by repeated final roots merely because their numerical values coincide.
  squaring=rows[1].split('=')[1].strip();assert squaring.startswith(r'\sqrt{(') and squaring.count('^{2}')==2
  a,b=re.match(r'\\sqrt\{\((.*?)\)\^\{2\}\+\((.*?)\)\^\{2\}\}',squaring.replace(' ','')).groups();assert scalar(a)==x and scalar(b)==y
  evaluated=rows[2].split('=')[1].strip();terms=evaluated.removeprefix(r'\sqrt{').removesuffix('}').split('+');assert len(terms)==2 and scalar(terms[0])==x*x and scalar(terms[1])==y*y
  if mid=='q-18048':assert r'\cdot' in rows[4] and scalar(rows[4].split('=')[1])==target
  source=originals.get(mid)
  if source and ':question/worked-solution' in source:assert mask(sol)==mask(source[':question/worked-solution']);C['source_prose_masks']+=1
 if q.get(':question/answer-fields'):
  f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5 and all(v>=0 for v in vals)
  assert sum(s.simplify(v*v-n)==0 for v in vals)==1
  if not raw:
   profile=meta['profile'];expected=[target,n,abs(x)+abs(y),s.sqrt(abs(x)+abs(y)),s.sqrt(abs(x*x-y*y))] if profile=='norm-stages' else [target,n,abs(x),abs(y),abs(x)+abs(y)]
   assert profile in ('norm-stages','omit-component') and all(sum(s.simplify(v*v-w*w)==0 for v in vals)==1 for w in expected);C['complete_method_banks']+=1
  if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if s.simplify(v*v-n)==0]==[f[':answer-field/correct'][1]]
  for v,w in itertools.combinations(vals,2):assert s.simplify(v*v-w*w)!=0;C['criterion_pairs']+=1
  C['choice_values']+=5
 C['records']+=1
records=json.loads((R/f'qa/{K}-sampled.json').read_text())
for r in json.loads((D/'review.json').read_text())['normal_variants']:
 r=r.get('record',r)
 if 'question' in r and not r['generation'].get('evidence_only'):records.append(r)
for r in records:check(r)
for c in json.loads((D/'source-cases.json').read_text()):
 r=G.generate(c.get('level','easy'),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')));check(r,True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'calculator_provenance_sha256':hashlib.sha256((D/'calculator-requirements.json').read_bytes()).hexdigest(),'database_writes':0}
(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
