"""Parent reads determinant polynomial and every displayed solve/cancellation stage."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186059750;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_unknown_det_reader',R/'determinant-readback.py');s=p.s;x=p.p.x;g=module('root_unknown_det_generator',D.with_suffix('.py'))
C=dict(instances=0,displayed_values=0,formal_determinant_checks=0,matrix_cell_checks=0,determinant_arithmetic_stages=0,equivalent_root_equations=0,hard_distribution_cancellation_rows=0,source_questions=0,source_banks=0,source_values=0,source_refs=0,source_missing_refs=0,source_field_repairs=0,source_exact_prompts=0,source_normalized_full_solutions=0,source_raw_exact_solutions=0)
def equal(a,b):return s.expand(a-b)==0
def mask(text):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$[^$]*\$','MATH',text,flags=re.S)).strip()
def check(r):
 q=r['question'];prompt=q[':question/problem'];var=re.search(r'(?:value of)\s*\$([a-z])',prompt)[1];mapping={var:'x'};a,b,c,d=p.array(prompt,mapping);det=s.expand(a*d-b*c);target=s.Integer(re.search(r'(?:\\text\{det\}|det)\([^)]*\)\s*=\s*(-?\d+)',prompt)[1]);roots=set(s.solve(det-target,x));assert len(roots)==1;answer=next(iter(roots));assert answer.is_Integer
 f=q[':question/answer-fields'][0];values=[]
 for z in f[':answer-field/choices']:
  raw=z[':answer/value'];parts=raw.split('=');assert len(parts) in (1,2)
  if len(parts)==2:assert parts[0].strip()==var
  values.append(p.scalar(parts[-1],mapping))
 assert len(set(values))==len(values);assert [z[':answer/id'] for z,v in zip(f[':answer-field/choices'],values) if v==answer]==[f[':answer-field/correct'][1]];C['displayed_values']+=len(values)
 blocks=p.displays(q[':question/worked-solution']);assert len(blocks)==3
 fa,fb,fc,fd=p.array(blocks[0]);assert equal(fa*fd-fb*fc,p.scalar(blocks[0].split('=')[-1]));C['formal_determinant_checks']+=1
 assert p.array(blocks[1],mapping)==(a,b,c,d);C['matrix_cell_checks']+=8
 arith=[]
 for row in p.rows(blocks[1]):
  raw=row.split('& =')[1]
  if 'MATRIX' in raw:continue
  assert equal(p.scalar(raw,mapping),det),(raw,det);arith.append(raw);C['determinant_arithmetic_stages']+=1
 assert len(arith)>=2
 for row in p.rows(blocks[2]):
  lhs,rhs=row.split('& =');lhs=lhs.strip();left=det if re.fullmatch(r'(?:\\text\{det\}|det)\([^)]*\)',lhs) else p.scalar(lhs,mapping);got=set(s.solve(left-p.scalar(rhs,mapping),x));assert got==roots,(row,got,roots);C['equivalent_root_equations']+=1
 level=q[':question/difficulty'].split('/')[-1]
 if level=='moderate':assert s.degree(det,x)==2 and s.degree(a*d,x)==2 and s.expand(det-target-s.Poly(det,x).nth(2)*(x-answer)**2)==0
 if level=='easy':assert s.degree(det,x)==1
 if level=='hard':
  assert s.degree(a*d,x)==s.degree(b*c,x)==2 and s.degree(det,x)==1
  assert len(arith)==4 and arith[2].count(r'\cancel')==2 and arith[1].count('{'+var+'}^{2}')==2;C['hard_distribution_cancellation_rows']+=2
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',q[':question/worked-solution']):
  m=re.fullmatch(r'det\([^)]*\)=(-?\d+),?',inline)
  if m:assert s.Integer(m[1])==target
 C['instances']+=1;return q
source={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=source[case['source_id']];C['source_questions']+=1
 if case['source_id']=='q-127614':assert q[':question/problem'].startswith(old[':question/problem']) and '{{field-1}}' in q[':question/problem'];C['source_field_repairs']+=1
 else:assert q[':question/problem']==old[':question/problem'];C['source_exact_prompts']+=1
 if old.get(':question/answer-fields'):
  sf=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];oldvals=[p.scalar(z[':answer/value'].split('=')[-1]) for z in sf[':answer-field/choices']];newvals=[p.scalar(z[':answer/value'].split('=')[-1]) for z in nf[':answer-field/choices']];assert sorted(oldvals)==sorted(newvals);C['source_banks']+=1;C['source_values']+=len(oldvals)
  if sf.get(':answer-field/correct'):assert p.scalar(sf[':answer-field/correct'][':answer/value'].split('=')[-1])==p.scalar(next(z[':answer/value'].split('=')[-1] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));C['source_refs']+=1
  else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):
  assert mask(old[':question/worked-solution'])==mask(q[':question/worked-solution']);oldblocks=p.displays(old[':question/worked-solution']);newblocks=p.displays(q[':question/worked-solution']);assert [len(p.rows(z)) for z in oldblocks]==[len(p.rows(z)) for z in newblocks];C['source_normalized_full_solutions']+=1
  C['source_raw_exact_solutions']+=old[':question/worked-solution']==q[':question/worked-solution']
review=json.loads((D/'review.json').read_text())
if isinstance(review,dict):review=review['original_parameter_replays']+review['generated_variants']
for r in review:check(r.get('record',r.get('generated',r)))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(80,104):check(g.generate(level,seed))
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
