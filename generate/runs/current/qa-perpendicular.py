"""Parent reads actual vectors, all dot-zero roots and ordered equation stages."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186059731;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_perp_parser',R/'determinant-readback.py');s=p.s;x=p.p.x;g=module('root_perp_generator',D.with_suffix('.py'))
C=dict(instances=0,displayed_values=0,dot_product_stages=0,equivalent_root_equations=0,formal_component_rows=0,source_banks=0,source_values=0,source_refs=0,source_missing_refs=0,source_exact_solutions=0,source_exact_prompts=0)
def check(r):
 q=r['question'];problem=q[':question/problem'];unknown=re.search(r'(?:value of|then)\s*\$([a-z])',problem)[1];mapping={unknown:'x'}
 matches=re.findall(r'([a-z])\s*=\s*(\[\\begin\{aligned\}.*?\\end\{aligned\}\]|\\begin\{bmatrix\}.*?\\end\{bmatrix\}|⟨.*?⟩)',problem,re.S);assert len(matches)==2,(problem,matches)
 names=[name for name,v in matches];vectors=[]
 for name,v in matches:
  if v.startswith('⟨'):cells=v[1:-1].split(',')
  else:cells=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',v,re.S)[1].split(chr(92)*2)
  vectors.append(tuple(p.scalar(z,mapping) for z in cells))
 a,b=vectors;assert len(a)==len(b) in (2,3);dot=s.expand(sum(u*v for u,v in zip(a,b)));roots=set(s.solve(dot,x));assert roots and all(z.is_real for z in roots)
 constraint=re.search(r'\$'+unknown+r'\s*([<>])\s*0',problem);sign=0 if constraint is None else 1 if constraint[1]=='>' else -1;eligible={z for z in roots if not sign or z*sign>0};assert len(eligible)==1;answer=next(iter(eligible))
 f=q[':question/answer-fields'][0];vals=[p.scalar(a[':answer/value'],mapping) for a in f[':answer-field/choices']];assert len(set(vals))==len(vals);assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if s.simplify(v-answer)==0]==[f[':answer-field/correct'][1]];C['displayed_values']+=len(vals)
 displays=p.displays(q[':question/worked-solution']);assert len(displays)==2
 rows=p.rows(displays[0]);formal='+'.join('{'+names[0]+'}_{'+c+r'}\cdot {'+names[1]+'}_{'+c+'}' for c in 'xyz'[:len(a)]);assert rows[0].split('& =')[1].strip()==formal;C['formal_component_rows']+=1
 assert rows[1].count(r'\cdot')==len(a)
 for row in rows[1:]:assert s.expand(p.scalar(row.split('& =')[1],mapping)-dot)==0;C['dot_product_stages']+=1
 for row in p.rows(displays[1]):
  lhs,rhs=row.split('& =');lhs=lhs.strip();rhs=rhs.strip().rstrip('.')
  left=dot if lhs==names[0]+r'\cdot '+names[1] else p.scalar(lhs,mapping)
  if r'\pm' in rhs:
   assert lhs==unknown;v=p.scalar(rhs.replace(r'\pm',''),mapping);got={v,-v}
  else:got=set(s.solve(left-p.scalar(rhs,mapping),x))
  assert got==roots,(row,got,roots);C['equivalent_root_equations']+=1
 if sign:
  word='negative' if sign>0 else 'positive';assert 'We disregard the '+word+' solution' in q[':question/worked-solution'];assert '$'+unknown+('>0' if sign>0 else '<0')+'.$' in q[':question/worked-solution']
 level=q[':question/difficulty'].split('/')[-1]
 if level=='hard':
  poly=s.Poly(dot,x);assert poly.degree()==2 and len(a)==3 and poly.nth(1)==0;A=poly.nth(2);rad=-poly.nth(0)/A;assert 2<=abs(A)<=6 and 2<=rad.p<=30 and 2<=rad.q<=6 and s.sqrt(rad).is_rational is False
  assert sum(s.degree(u*v,x)==2 for u,v in zip(a,b))==2 and all(z!=0 for z in [s.LC(s.Poly(u,x)) for u in a+b]);assert all(abs(s.LC(s.Poly(u,x)))>=2 for u in a+b)
 C['instances']+=1;return q
source={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile')));old=source[case['source_id']];nf=q[':question/answer-fields'][0];sf=old[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'];C['source_exact_prompts']+=1
 assert sorted(p.scalar(a[':answer/value']) for a in nf[':answer-field/choices'])==sorted(p.scalar(a[':answer/value']) for a in sf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(sf[':answer-field/choices'])
 if sf.get(':answer-field/correct'):assert p.scalar(sf[':answer-field/correct'][':answer/value'])==p.scalar(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]));C['source_refs']+=1
 else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):assert old[':question/worked-solution']==q[':question/worked-solution'];C['source_exact_solutions']+=1
for r in json.loads((D/'review.json').read_text()):check(r['record'])
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(100,124):check(g.generate(level,seed))
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
