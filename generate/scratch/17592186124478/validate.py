"""Printed-matrix, checkbox replay and native application grading checks."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
OUT=HERE/'checkbox-update-2026-10-16'
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import validate_generated_record
s=importlib.util.spec_from_file_location('nonpivot_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,x):
 OUT.mkdir(exist_ok=True);(OUT/name).write_text(json.dumps(x,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def read(text):
 raw=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)[1]
 return [[int(c.strip()) for c in r.split('&')] for r in raw.split(r'\\')]
def answer_set(value,n):return set(range(1,n+1)) if value=='All the columns are non-pivot' else set(map(int,re.findall(r'\$(\d+)\$',value)))
def selected(q):
 return {i+1 for i,f in enumerate(q[':question/answer-fields']) if next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='true'}
def math_question(q):
 matrix=read(q[':question/problem']);n=len(matrix[0]);ps=[];zero=False
 for row in matrix:
  assert len(row)==n
  nonzero=[j+1 for j,x in enumerate(row) if x]
  if not nonzero:zero=True;continue
  assert not zero
  first=nonzero[0];assert not ps or first>ps[-1];ps.append(first)
 assert tuple(i+1 for i in sp.Matrix(matrix).rref()[1])==tuple(ps)
 non=set(range(1,n+1))-set(ps)
 fields=q[':question/answer-fields'];assert len(fields)==n
 assert q[':question/problem'].count('Select all that apply.')==1
 ids=[q[':question/id']]
 for i,f in enumerate(fields):
  assert f[':answer-field/type']==':answer-field.type/checkbox' and f[':answer-field/key']==f'Column {i+1}'
  bank=f[':answer-field/choices'];assert len(bank)==2
  assert {a[':answer/value'] for a in bank}=={'false','true'}
  assert all(a[':answer/type']==':answer.type/text' for a in bank)
  assert f[':answer-field/correct']==[':answer/id',next(a[':answer/id'] for a in bank if a[':answer/value']==str(i+1 in non).lower())]
  ids.extend([f[':answer-field/id']]+[a[':answer/id'] for a in bank])
 assert len(ids)==len(set(ids))
 for identity in ids:uuid.UUID(identity)
 assert selected(q)==non
 sol=q[':question/worked-solution'];assert read(sol)==matrix
 assert re.search(r'has \$(\d+)\$ pivots',sol)[1]==str(len(ps))
 section=sol.split('pivots in the ')[1].split(' columns:')[0]
 assert set(map(int,re.findall(r'\$(\d+)\$',section)))==set(ps)
 assert answer_set(sol.split('Therefore,')[1],n)==non
 assert sol.endswith(' column.' if len(non)==1 else ' columns.')
 label=re.search(r'matrix \$(\w)\$',q[':question/problem'])[1]
 assert f'${label}$ has ${len(ps)}$ pivots' in sol
 assert q[':question/difficulty']==':question.difficulty/easy'
 validate_generated_record({'question':copy.deepcopy(q)})
 return tuple(ps)
def independent(rec):
 assert rec['knowledge_point']['db_id']==g.KP_ID
 meta=rec['generation'];assert rec==g.generate('easy',meta['seed'],meta['template'],meta['parameters'])
 math_question(rec['question']);assert meta['mathematical_fingerprint']==fingerprint(rec['question']);return rec
check=independent
def checks(rec):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each checkbox owned Boolean, including unchecked false'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]
def native(label,r):return {'label':label,'record':r,'checks':checks(r)}
def reject(q):
 try:math_question(q)
 except (AssertionError,StopIteration):return
 raise AssertionError('Invalid question passed')
def main():
 inputs=[];review=[];replays=[];coverage={};tasks=set();total=0;samples=0;subset_checks=0;negative_controls=0
 source_hash=hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest()
 for sid,old in g.CASES.items():
  rec=independent(g.generate('easy',0,sid,g.DEFAULTS[sid]));q=rec['question'];original=g.field(sid)
  assert q[':question/problem'].replace('\n\nSelect all that apply.','')==old[':question/problem']
  assert q[':question/worked-solution']==g.replay_solution(sid)
  base=g.matrices(old[':question/problem'])[0];positions=set();numeric=set();by_content={}
  expected=answer_set(original[':answer-field/correct'][':answer/value'],base.cols)
  assert selected(q)==expected
  option_mappings=[]
  for a in original[':answer-field/choices']:
   ss=answer_set(a[':answer/value'],base.cols)
   assert ss<=set(range(1,base.cols+1))
   option_mappings.append({'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'selected_columns':sorted(ss),'correct':ss==expected})
  replays.append({'source':sid,'prompt_matrix_and_wording_preserved':True,'instruction_added_once':True,'correct_selection_preserved':sorted(expected),'legacy_options_mapped':option_mappings,'solution_exact':sid not in g.SOURCE_SOLUTION_REPAIRS,'solution_repair':g.SOURCE_SOLUTION_REPAIRS.get(sid),'source_snapshot_unchanged':True})
  # All old and newly expressible response subsets have exactly one Boolean per
  # displayed column. Only the independently computed complement is fully right.
  source_native_checks=[]
  for mask in itertools.product((False,True),repeat=base.cols):
   actual={i+1 for i,truth in enumerate(mask) if truth}
   accepted=all(truth==(i+1 in expected) for i,truth in enumerate(mask))
   assert accepted==(actual==expected);subset_checks+=1
   for i,(truth,f) in enumerate(zip(mask,q[':question/answer-fields'])):
    answer=next(a for a in f[':answer-field/choices'] if a[':answer/value']==str(truth).lower())
    source_native_checks.append({'field_index':i,'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if truth==(i+1 in expected) else 'rejected','purpose':'all source response subsets: '+str(sorted(actual))})
  inputs.append({'label':sid+' source replay, all response subsets','record':rec,'checks':source_native_checks})
  for permutation in itertools.permutations(range(base.cols)):
   ps=sorted(permutation[j] for j in g.pivots(base));m=sp.zeros(*base.shape)
   for i,j in enumerate(ps):
    m[i,j]=int(base[i,g.pivots(base)[i]])
    for k in range(j+1,base.cols):m[i,k]=(i+k)%5-2
   p={'matrix':[[int(x) for x in row] for row in m.tolist()],'mapping':list(permutation),'replay':False}
   r=independent(g.generate('easy',7,sid,p));total+=1;positions.add(tuple(ps));tasks.add(fingerprint(r['question']))
   assert g.generate('easy',999,sid,p)['question']==r['question']
   # Different historical role mappings with identical served content share IDs.
   key=json.dumps([r['question'][':question/problem'],r['question'][':question/worked-solution']])
   assert by_content.setdefault(key,r['question'])==r['question']
   inputs.append(native(sid+' '+str(permutation),r))
  sampled_positions=set()
  for seed in range(120):
   r=independent(g.generate('easy',seed,sid));samples+=1
   numeric.update(x for row in read(r['question'][':question/problem']) for x in row)
   sampled_positions.add(tuple(i-1 for i in math_question(r['question'])))
   assert g.generate('easy',seed+999,sid,r['generation']['parameters'])['question']==r['question']
  eligible=set(itertools.combinations(range(base.cols),len(g.pivots(base))))
  assert positions==eligible==sampled_positions
  coverage[sid]={'pivot_position_sets':sorted(positions),'eligible_position_sets':len(eligible),'unexercised':[],'sampled_integers':sorted(numeric),'permutations_checked':len(list(itertools.permutations(range(base.cols)))),'normal_seed_samples':120}
  changed=independent(g.generate('easy',123,sid));review.append('## '+sid+'\n\nCheckbox replay\n\n'+g.markdown(rec)+'\n\nChanged positions and entries\n\n'+g.markdown(changed))
  bad=copy.deepcopy(changed['question']);bad[':question/worked-solution']=bad[':question/worked-solution'].replace('pivots in the ','pivots in the $99$th and ');reject(bad);negative_controls+=1
  bad=copy.deepcopy(changed['question']);f=bad[':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]);reject(bad);negative_controls+=1
  bad=copy.deepcopy(changed['question']);bad[':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']=bad[':question/answer-fields'][1][':answer-field/choices'][0][':answer/id'];reject(bad);negative_controls+=1
  # Neither zero nor full non-pivot sets belongs to these observed rank families.
  for m in (sp.zeros(*base.shape),sp.eye(base.rows,base.cols)):
   p={'matrix':[[int(x) for x in row] for row in m.tolist()],'mapping':list(range(base.cols)),'replay':False}
   if len(m.rref()[1])==len(g.pivots(base)):continue
   try:g.generate('easy',0,sid,p)
   except AssertionError:negative_controls+=1
   else:raise AssertionError('Unsupported rank accepted')
 for level in ('moderate','hard','unclassified'):
  try:g.generate(level)
  except ValueError:negative_controls+=1
  else:raise AssertionError('Unsupported level admitted')
 batch=g.batch('easy',100,124478);assert len({fingerprint(r['question']) for r in batch})==len(batch)==40
 assert hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest()==source_hash
 save('source-replay.json',{'status':'pass','profiles':replays,'historical_source_basis':g.SNAPSHOT['basis'],'source_sha256':source_hash,'legacy_duplicate_field':'q-35391: only historical keyed bank is replayed; original unkeyed duplicate and capture remain unchanged, not a current inventory assumption'})
 save('slot-coverage.json',coverage);save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(OUT/'native-input.json'),str(OUT/'native-grading.json')],check=True)
 (OUT/'review.md').write_text('\n\n'.join(review)+'\n')
 native_report=json.loads((OUT/'native-grading.json').read_text())
 result={'status':'pass','generator_version':g.VERSION,'database_writes':0,'source_basis':g.SNAPSHOT['basis'],'supported_levels':['easy'],'source_replays':len(replays),'source_solution_repairs':g.SOURCE_SOLUTION_REPAIRS,'exhaustive_profile_permutations':total,'distinct_structural_tasks':len(tasks),'normal_sample_records':samples,'subset_response_checks':subset_checks,'negative_controls_rejected':negative_controls,'native_grading':{k:v for k,v in native_report.items() if k!='records'}|{'records':len(native_report['records']),'evidence':'native-grading.json'},'zero_and_full_correct_subsets':'Outside supported source shape/rank families; no new mathematical scope added. Empty/full learner responses remain representable and checked.','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine']}}
 save('verification.json',result)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
