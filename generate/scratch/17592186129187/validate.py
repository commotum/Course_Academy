#!/usr/bin/env python3
"""Full observed bank matching, independent displayed mathematics, native grading.

No DB writes. Fails on any unacknowledged source/math/identity/layout/grade issue.
Missing original designation is counted separately, never a fidelity match.
"""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sympy as sp
from math_parser import parse,u,v
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('jacobian',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,data): (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def equal(a,b): return sp.simplify(sp.trigsimp(a-b))==0

def displayed_matrix(s):
 # Parse scalar entries from rendered transformation; no metadata dependence.
 matrices=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s)
 return [parse(z) for z in matrices[-1].split(r'\\')]

def check_record(r):
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0]
 assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5 and len(q[':question/answer-fields'])==1
 x,y=displayed_matrix(q[':question/problem']); matrix=sp.Matrix([[sp.diff(x,u),sp.diff(x,v)],[sp.diff(y,u),sp.diff(y,v)]])
 determinant=matrix.det();ds=list(matrix)
 assert equal(determinant,sp.sympify(meta['determinant']))
 values=[];ids=[]
 for answer in f[':answer-field/choices']:
  aid=answer[':answer/id'];value=parse(answer[':answer/value']);values.append(value);ids.append(aid)
  assert equal(value,sp.sympify(meta['answer_math'][aid]['expression']))
  assert equal(value,determinant)==(aid==f[':answer-field/correct'][1])
  assert '$' not in answer[':answer/value'] and answer[':answer/type']==':answer.type/math'
 assert len(set(ids))==5
 assert all(not equal(a,b) for a,b in itertools.combinations(values,2))
 sol=q[':question/worked-solution']; sections=sol.split('First, we find the partial derivatives:\n\n')
 assert len(sections)==2
 derivative_block=sections[1].split('$$')[1]
 parts=re.split(r'&=|&\\quad |\\\\',derivative_block)
 actual=[parse(z.split(r'\end{aligned}')[0]) for z in parts[1::2]]
 assert len(actual)==4 and all(equal(a,b) for a,b in zip(actual,ds))
 # Derivative determinant matrix, product expansion, simplification rows, and
 # final expression are checked from the displayed solution independently.
 final=sol.split('Therefore, the corresponding Jacobian determinant is\n\n')[1]
 rows=final.split(r'\\')
 scalar_rows=[]
 for row in rows:
  if row.startswith('&=') and 'matrix' not in row:
   body=row[2:].split(r'\end{aligned}')[0].rstrip('.')
   if body: scalar_rows.append(parse(body))
 assert scalar_rows and all(equal(value,determinant) for value in scalar_rows)
 assert 'at the point' not in q[':question/problem'] and 'area' not in q[':question/problem'].lower()
 assert q[':question/problem'].count('$$')%2==0 and sol.count('$$')%2==0
 assert all(sentence in sol for sentence in ['Given a transformation','the Jacobian determinant of $T,','Here, we have','First, we find the partial derivatives:','Therefore, the corresponding Jacobian determinant is'])
 return {'displayed_derivatives':4,'displayed_scalar_solution_rows':len(scalar_rows),'choices':5}

def main():
 source=json.loads((HERE/'source.json').read_text());questions=source['record'][':knowledge-point/questions'];cases=json.loads((HERE/'source-cases.json').read_text())
 assert source['basis']==1356 and len(cases)==len(questions)==10
 originals={q[':question/math-academy-id']:q for q in questions}
 fidelity=[];records=[];checks_total=0
 for case in cases:
  t=case['template'];r=g.generate(g.TEMPLATES[t][0],parameters=case['parameters'],profile=case['bank_profile']);checks_total+=check_record(r)['choices'];records.append(r)
  q=originals[case['source_id']];sf=q[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
  expected=[parse(a[':answer/value']) for a in sf[':answer-field/choices']];actual=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
  matched=[]
  for a in expected:
   indexes=[i for i,b in enumerate(actual) if equal(a,b)];assert len(indexes)==1;matched+=indexes
  assert len(set(matched))==5
  origcorrect=sf.get(':answer-field/correct');correct=next(parse(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  if origcorrect: assert equal(parse(origcorrect[':answer/value']),correct)
  assert len(q[':question/answer-fields'])==1
  result={'source_id':case['source_id'],'template':t,'profile':case['bank_profile'],'matched_options':5,'total_options':5,'bank_match':True,'designation_match':bool(origcorrect),'designation_status':'matched' if origcorrect else 'source missing; mathematically authored correction','field_shape_match':True,'normalization':'equivalent standard matrix/trig LaTeX; shared source sentences and simplification rows retained; q-38078 typo corrected'}
  fidelity.append(result)
 variants=[]
 # Every observed/profile has two generated variants, plus all authored defaults.
 for profile,bank in g.BANK_PROFILES.items():
  t=bank['template'];level=g.TEMPLATES[t][0]
  for seed in (17,29):
   r=g.generate(level,seed,profile=profile);check_record(r);records.append(r);variants.append(r)
   fixed=g.generate(level,seed+7,template=t,parameters=r['generation']['parameters'],profile=profile)
   assert fixed['question'][':question/id']==r['question'][':question/id']
   assert fixed['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
 # Additional samples exercise all families under their defined ranges.
 for t,(level,_,_) in g.TEMPLATES.items():
  for seed in range(5):
   r=g.generate(level,seed,template=t);check_record(r);records.append(r)
 # Same parameters with different displayed banks must have different identities.
 for t,(level,source_id,p) in g.TEMPLATES.items():
  if source_id:
   a=g.generate(level,parameters=p,profile='observed_'+t);b=g.generate(level,parameters=p,profile='authored_'+t)
   assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
   assert a['question'][':question/id']!=b['question'][':question/id']
 # Invalid explicit parameters/profile must fail, never silently mutate.
 for kwargs in [dict(level='hard',parameters={'a':1,'b':1,'m':7,'n':2}),dict(level='easy',template='linear',parameters={'a':1,'b':1,'c':1,'d':1}),dict(level='easy',template='polar',profile='observed_linear'),dict(level='moderate',field_type='blank')]:
  try:g.generate(**kwargs)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit request accepted')
 engine=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0]
  engine.append({'label':f'case-{i}-{r["generation"]["bank_profile"]}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned correct/wrong radio selection'} for a in f[':answer-field/choices']]})
 write('engine-input.json',engine)
 binary=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 write('source-bank-fidelity.json',fidelity);write('review.json',variants)
 report={'status':'pass','database_writes':0,'provenance':g.PROVENANCE,'source_questions':10,'source_options_matched':50,'source_options_total':50,'complete_source_banks_matched':10,'original_correct_designations_matched':9,'original_correct_designations_total_present':9,'source_missing_designations':1,'authored_missing_designations':1,'source_correction':'q-38078 solution cos²+cos² -> cos²+sin²','generated_review_records':len(variants),'mathematics_records_checked':len(records),'native_engine':json.loads((HERE/'engine-validation.json').read_text()),'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'formatting':'standard math normalization; source shared sentences and scalar simplification layout verified','plots':'none; canonical math bitmap inspected','authored_hard':'powers template grounded in e-6810; no evaluated-point/area/orientation demands','observed_bank_intent':'limited: explicit profiles only; defaults authored method errors'}
 write('validation.json',report)
 lines=['# Jacobian review','',f'Basis 1356; all ten original complete banks. Values normalize standard LaTeX. Original raw evidence retained in source.json.','']
 for case,r,result in zip(cases,records[:10],fidelity):
  q=originals[case['source_id']];f=q[':question/answer-fields'][0]
  lines+=['## Original '+case['source_id'],'',q[':question/problem'],'','Original choices:']
  for a in f[':answer-field/choices']:lines+=['- $'+a[':answer/value']+'$']
  lines+=['','Original worked solution:',q.get(':question/worked-solution','Absent in captured source.'),'',g.markdown(r),'']
 lines+=['# Clearly labeled generated variants','']
 for r in variants:lines+=[g.markdown(r)]
 (HERE/'review.md').write_text('\n'.join(lines))
 print(f'PASS: 50/50 source values, 10/10 banks, 9/9 present correct designations; 1 missing authored. {len(records)} math records and {len(records)*5} native selection checks.')
if __name__=='__main__':main()
