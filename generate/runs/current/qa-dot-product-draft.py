"""Parent reads actual components, full banks and ordered dot-product teaching rows."""
import importlib.util,json,re,sys,hashlib
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186059730;D=R.parents[2]/f'generate/scratch/{K}-draft'
SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_dot_math',R/'ode-scalar-parser.py');s=p.s;g=module('root_dot_generator',D.with_suffix('.py'))
C=dict(instances=0,displayed_values=0,arithmetic_stages=0,formal_component_rows=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0,source_exact_solutions=0,source_exact_prompts=0,source_standalone_repairs=0)
def addends(text):
 depth=0;start=0;out=[]
 for i,ch in enumerate(text):
  if ch in '({[':depth+=1
  elif ch in ')}]':depth-=1
  elif ch in '+-' and depth==0 and i>start and text[start:i].strip():
   out.append(text[start:i].strip());start=i
 out.append(text[start:].strip());return out
def check(r):
 q=r['question'];problem=q[':question/problem'];pairs=re.findall(r'(?:\\overset\{\\to \}\{([a-z])\}|([a-z]))\s*=\s*⟨(.*?)⟩',problem);assert len(pairs)==2,(problem,pairs)
 names=[a or b for a,b,v in pairs];vectors=[tuple(p.scalar(v) for v in raw.split(',')) for a,b,raw in pairs];a,b=vectors;assert len(a)==len(b) in (2,3);terms=[u*v for u,v in zip(a,b)];answer=sum(terms)
 f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(set(vals))==len(vals)
 assert [z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vals) if v==answer]==[f[':answer-field/correct'][1]];C['displayed_values']+=len(vals)
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(blocks) in (1,2)
 rows=[row.split('=',1)[1].strip() for block in blocks for row in block.split(chr(92)*2)];assert len(rows)==4
 formal='+'.join('{'+names[0]+'}_{'+v+r'}\cdot {'+names[1]+'}_{'+v+'}' for v in 'xyz'[:len(a)]);assert rows[0]==formal
 for row in rows[1:]:assert s.simplify(p.scalar(row)-answer)==0,(row,answer);C['arithmetic_stages']+=1
 assert rows[1].count(r'\cdot')==len(a);assert r'\cdot' not in rows[2] and r'\cdot' not in rows[3]
 products=addends(rows[1]);summands=addends(rows[2]);assert len(products)==len(summands)==len(a)
 for expression,u,v in zip(products,a,b):
  left,right=expression.split(r'\cdot');assert p.scalar(left)==u and p.scalar(right)==v,(expression,u,v)
 assert [p.scalar(z) for z in summands]==terms,(summands,terms)
 C['individual_factor_operands']=C.get('individual_factor_operands',0)+2*len(a)
 C['individual_signed_products']=C.get('individual_signed_products',0)+len(a)
 if r['generation']['bank_profile']=='authored_operations':assert set(vals)=={answer,sum(a)+sum(b),sum(a)*sum(b),sum(terms[1:]),sum(terms[:-1])}
 level=q[':question/difficulty'].split('/')[-1]
 if level=='moderate':assert len(a)==3 and all(z.is_Integer and 2<=abs(z)<=12 for z in a+b) and min(terms)<0<max(terms)
 if level=='hard':assert len(a)==3 and all(1<=abs(z)<=6 and 10%z.q==0 for z in a+b) and sum(z.q!=1 for z in terms)>=2 and min(terms)<0<max(terms)
 C['formal_component_rows']+=1;C['instances']+=1;return q
source={q[':question/math-academy-id']:q for q in json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
for case in json.loads((D/'source-replay-specs.json').read_text()):
 q=check(g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=source[case['source_id']];sf=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert {p.scalar(a[':answer/value']) for a in sf[':answer-field/choices']}=={p.scalar(a[':answer/value']) for a in nf[':answer-field/choices']};C['source_banks']+=1;C['source_values']+=len(sf[':answer-field/choices'])
 if sf.get(':answer-field/correct'):
  assert p.scalar(sf[':answer-field/correct'][':answer/value'])==p.scalar(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]));C['source_existing_refs']+=1
 else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):assert g.normalize_prose(old[':question/worked-solution'])==q[':question/worked-solution'];C['source_exact_solutions']+=1
 if case['source_id']=='q-168035':assert q[':question/problem'].endswith(g.normalize_prose(old[':question/problem']));C['source_standalone_repairs']+=1
 else:assert g.normalize_prose(old[':question/problem'])==q[':question/problem'];C['source_exact_prompts']+=1
for r in json.loads((D/'review.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(80,120):check(g.generate(level,seed))
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'scope':'Observed 2D/3D component sum, moderate mixed signed nonzero integral terms, hard same three-term method with terminating rational components; no angle/length/orthogonality branches.','database_writes':0}
(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
