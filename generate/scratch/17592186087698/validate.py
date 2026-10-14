#!/usr/bin/env python3
"""Independently read rendered matrix dimensions/properties and every answer key."""
import copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('matrix_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def read_matrices(text):
 ms=[]
 for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
  rows=[]
  for row in re.split(r'\\\\',body):
   rows.append([sp.sympify(re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',v.strip())) for v in row.split('&')])
  assert rows and rows[0] and len({len(row) for row in rows})==1
  ms.append(rows)
 return ms

def category(m):
 r,c=len(m),len(m[0])
 if all(v==0 for row in m for v in row):return 'A zero matrix'
 if r==1:return 'A row vector'
 if c==1:return 'A column vector'
 if r==c:
  if all(m[i][j]==int(i==j) for i in range(r) for j in range(c)):return 'An identity matrix'
  if all(m[i][j]==0 for i in range(r) for j in range(c) if i!=j):return 'A diagonal matrix'
  return 'A square matrix'
 return 'Other'

def audit(rec):
 q=rec['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];ms=read_matrices(p)
 assert q[':question/difficulty']==':question.difficulty/easy'
 assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP_UUID
 fs=q[':question/answer-fields'];assert sol and len(ms)==(3 if 'vectors?' in p else 1)
 if len(ms)==1:
  good=category(ms[0]);assert len(fs)==1 and fs[0][':answer-field/type']==':answer-field.type/radio'
  if good=='A row vector':assert sol=='The matrix has only one row. Hence, it is a row vector.'
  elif good=='A diagonal matrix':assert 'diagonal entries are not all ones' in sol and "Hence it's a diagonal matrix." in sol
  else:assert good=='Other' and sol=='The matrix has no special name.'
 else:
  kind='row' if 'are row vectors' in p else 'column';goodnames=[]
  assert len(fs)==3 and {f[':answer-field/key'] for f in fs}==set('ABC')
  for name,m in zip('ABC',ms):
   r,c=len(m),len(m[0]);good=(r==1 if kind=='row' else c==1)
   f=next(f for f in fs if f[':answer-field/key']==name);assert f[':answer-field/type']==':answer-field.type/checkbox'
   a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert a[':answer/value']==str(good).lower()
   line=next(s for s in sol.split('\n\n') if s.startswith('- $'+name+'$'))
   assert ('*not*' not in line)==good
   if good:assert 'only one '+kind in line;goodnames.append(name)
   elif kind=='row' and c==1:assert f'${r}$ rows' in line and "it's a column vector" in line
   elif kind=='column' and r==1:assert f'${c}$ columns' in line and "it's a row vector" in line
   else:assert f'${r if kind=="row" else c}$ '+('rows' if kind=='row' else 'columns') in line
  assert len(goodnames)==1 and sol.endswith(f'Therefore, only ${goodnames[0]}$ is a {kind} vector.')
 for f in fs:
  vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==len(set(vals))
  assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  if len(ms)==1:assert a[':answer/value']==good and len(vals)==5
  else:assert set(vals)=={'true','false'}
 for text in (p,sol):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 assert rec['generation']['mathematical_fingerprint']==g.fingerprint(q)
 return True

def grading_item(label,rec):
 return {'label':label,'record':rec,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned answer, including each explicit unchecked checkbox'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}

def source_bank(q):
 return [(f[':answer-field/key'],f[':answer-field/type'][':db/ident'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),f[':answer-field/correct'][':answer/value']) for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])]
def generated_bank(q):
 return [(f[':answer-field/key'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])) for f in q[':question/answer-fields']]

def main():
 inputs=[];fidelity=[];review=[];coverage={};records=[]
 for t,mid in g.TEMPLATES.items():
  source=g.ORIGINALS[mid];rec=g.generate(template=t,parameters=g.parameters(t));audit(rec)
  assert rec['question'][':question/problem']==source[':question/problem']
  assert rec['question'][':question/worked-solution']==source[':question/worked-solution']
  assert generated_bank(rec['question'])==source_bank(source)
  banks=source_bank(source);fidelity.append({'source':mid,'template':t,'complete_banks_matched':len(banks),'complete_banks_total':len(banks),'distractors_matched':sum(len(x[2])-1 for x in banks),'distractors_total':sum(len(x[2])-1 for x in banks),'prompt_and_solution_exact':True})
  inputs.append(grading_item('source/'+mid,rec));review.append({'source':source,'replay':rec})
  seen=set();targets=set()
  for seed in range(100):
   rec=g.generate(seed=seed,template=t);audit(rec);records.append(rec);inputs.append(grading_item(t+'/'+str(seed),rec))
   assert g.generate(seed=seed,template=t)==rec
   again=g.generate(seed=seed+1000,template=t,parameters=rec['generation']['parameters']);assert again['question']==rec['question']
   seen.add(rec['generation']['mathematical_fingerprint']);targets.add(tuple((len(m),len(m[0])) for m in read_matrices(rec['question'][':question/problem'])))
   if seed<2:review[-1].setdefault('variants',[]).append(rec)
  coverage[t]={'sampled':100,'distinct_mathematical_tasks':len(seen),'dimension_tuples':[list(x) for x in sorted(targets)]}
  assert len(seen)>=5
 # Reject sampler identity collisions by enforcing nonidentity before rendering.
 for seed in range(1000):
  p=g.sample('diagonal',g.random.Random(seed));g.validate_parameters('diagonal',p)
 # All row/column lengths and diagonal sizes in the declared bounds appear.
 assert {x[0][1] for x in coverage['row']['dimension_tuples']}==set(range(2,7))
 assert {x[0][0] for x in coverage['diagonal']['dimension_tuples']}==set(range(2,7))
 # Hold entries/shapes fixed while changing the assessed target from row to column.
 p={'matrices':[[[1,2,3]],[[4],[5],[6],[7]],[[2,1],[3,4]]]}
 pair=[g.generate(template=t,parameters=p) for t in ['rows','columns']]
 for rec in pair:audit(rec);inputs.append(grading_item('changed-target/'+rec['generation']['template'],rec))
 assert generated_bank(pair[0]['question'])!=generated_bank(pair[1]['question'])
 # Corruption checks independently catch stale correct keys and solution targets.
 corruption=0
 for field in [True,False]:
  broken=copy.deepcopy(pair[0]);f=broken['question'][':question/answer-fields'][0]
  if field:f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  else:broken['question'][':question/worked-solution']=broken['question'][':question/worked-solution'].replace('only $A$','only $C$')
  try:audit(broken)
  except AssertionError:corruption+=1
  else:raise AssertionError('Corruption escaped')
 invalid=0
 for t,p in [('row',{'matrices':[[[0,0]]]}),('diagonal',{'matrices':[[[1,0],[0,1]]]}),('other',{'matrices':[[[1,2],[3,4]]]}),('rows',{'matrices':[[[1,2]],[[3,4]],[[1,2],[3,4]]]}),('row',{'matrices':[[[1,13]]]}),('row',{'matrices':[[[1,'1/2']]]}),('rows',{'matrices':[[[0,0]],[[1],[2]],[[1,2],[3,4]]]})]:
  try:g.generate(template=t,parameters=p)
  except (AssertionError,ValueError):invalid+=1
  else:raise AssertionError('Invalid parameters passed')
 for level in ['moderate','hard']:
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported level generated')
 (D/'engine-input.json').write_text(json.dumps(inputs,indent=2))
 native=D/'check-engine';subprocess.run([str(native),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 (D/'review.json').write_text(json.dumps(review+pair,indent=2));(D/'review.md').write_text('\n\n---\n\n'.join('Source '+x['source'][':question/math-academy-id']+'\n\n'+x['source'][':question/problem']+'\n\n'+x['source'][':question/worked-solution']+'\n\n'+ '\n\n'.join(v['question'][':question/problem']+'\n\n'+v['question'][':question/worked-solution'] for v in x['variants']) for x in review))
 report={'status':'pass','source_basis':g.SOURCE['basis'],'fidelity':fidelity,'correctness':{'independently_read_variants':len(records),'changed_target_same_data':True,'caught_corruptions':corruption,'rejected_invalid_boundaries':invalid},'slot_coverage':coverage,'grading':'engine-report.json','native_grader_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False}
 (D/'validation.json').write_text(json.dumps(report,indent=2))
 (D/'frozen-hashes.json').write_text(json.dumps({str(p.relative_to(D.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D.with_suffix('.py'),D/'validate.py',D/'source.json']},indent=2))
 print(json.dumps({'status':'pass','source_questions':len(fidelity),'variants':len(records),'corruption_checks':corruption}))
if __name__=='__main__':main()
