"""Independent printed-matrix, complete-bank and native application grading checks."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('nonpivot_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def read(text):
 raw=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)[1]
 return [[int(c.strip()) for c in r.split('&')] for r in raw.split(r'\\')]
def answer_set(value,n):return set(range(1,n+1)) if value=='All the columns are non-pivot' else set(map(int,re.findall(r'\$(\d+)\$',value)))
def math_question(q,allow_legacy_typos=False):
 matrix=read(q[':question/problem']);n=len(matrix[0]);ps=[];zero=False
 for row in matrix:
  assert len(row)==n
  nonzero=[j+1 for j,x in enumerate(row) if x]
  if not nonzero:zero=True;continue
  assert not zero
  first=nonzero[0];assert not ps or first>ps[-1];ps.append(first)
 assert len(sp.Matrix(matrix).rref()[1])==len(ps)
 non=set(range(1,n+1))-set(ps)
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert len(f[':answer-field/choices'])==5
 options=[answer_set(a[':answer/value'],n) for a in f[':answer-field/choices']]
 assert all(s and s<=set(range(1,n+1)) for s in options)
 assert len({tuple(sorted(s)) for s in options})==5
 matches=[a[':answer/id'] for a,ss in zip(f[':answer-field/choices'],options) if ss==non]
 assert matches==[f[':answer-field/correct'][1]]
 sol=q[':question/worked-solution'];assert read(sol)==matrix
 assert re.search(r'has \$(\d+)\$ pivots',sol)[1]==str(len(ps))
 section=sol.split('pivots in the ')[1].split(' columns:')[0]
 assert set(map(int,re.findall(r'\$(\d+)\$',section)))==set(ps)
 assert answer_set(sol.split('Therefore,')[1],n)==non
 assert q[':question/difficulty']==':question.difficulty/easy'
 return tuple(ps)
def independent(rec):
 assert rec['knowledge_point']['db_id']==g.KP_ID
 meta=rec['generation'];assert rec==g.generate('easy',meta['seed'],meta['template'],meta['parameters'])
 math_question(rec['question']);assert meta['mathematical_fingerprint']==fingerprint(rec['question']);return rec
check=independent
def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all five complete bank choices through application grade_field'} for a in f[':answer-field/choices']]
def native(label,r):return {'label':label,'record':r,'checks':checks(r)}
def main():
 inputs=[];review=[];replays=[];components=[];coverage={};tasks=set();total=0
 for sid,old in g.CASES.items():
  rec=independent(g.generate('easy',0,sid,g.DEFAULTS[sid]));q=rec['question'];f=q[':question/answer-fields'][0];original=g.field(sid)
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
  replays.append({'source':sid,'complete_bank_match':True,'matched_options':5,'matched_distractors':4,'correct_value':original[':answer-field/correct'][':answer/value'],'prompt_exact':True,'solution_exact':True,'missing':[],'extra':[]})
  base=g.matrices(old[':question/problem'])[0];positions=set();numeric=set()
  components.append({'source':sid,'template':'one non-pivot' if len(set(range(base.cols))-set(g.pivots(base)))==1 else 'two non-pivots','shape':list(base.shape),'observed_matrix':g.DEFAULTS[sid]['matrix'],'pivots_zero_based':list(g.pivots(base)),'profile':sid,'source_fields':[{'key':f[':answer-field/key'],'id':f[':answer-field/id'],'has_correct':':answer-field/correct' in f,'options':f[':answer-field/choices']} for f in old[':question/answer-fields']],'recipes':[{'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'original_subset_zero_based':list(g.subset(a[':answer/value'],base.cols)),'recipe':'sort(mapping[j] for j in original_subset); render ordinal subset, or All the columns are non-pivot for the full column set','psychological_interpretation':'unresolved; exact observed subset pattern retained'} for a in original[':answer-field/choices']]})
  inputs.append(native(sid+' source replay',rec))
  for permutation in itertools.permutations(range(base.cols)):
   ps=sorted(permutation[j] for j in g.pivots(base));m=sp.zeros(*base.shape)
   for i,j in enumerate(ps):
    m[i,j]=int(base[i,g.pivots(base)[i]])
    for k in range(j+1,base.cols):m[i,k]=(i+k)%5-2
   p={'matrix':[[int(x) for x in row] for row in m.tolist()],'mapping':list(permutation),'replay':False}
   r=independent(g.generate('easy',7,sid,p));total+=1;positions.add(tuple(ps));tasks.add(fingerprint(r['question']))
   assert g.generate('easy',999,sid,p)['question']==r['question']
   inputs.append(native(sid+' '+str(permutation),r))
  for seed in range(30):
   r=independent(g.generate('easy',seed,sid));numeric.update(x for row in read(r['question'][':question/problem']) for x in row)
  eligible=set(itertools.combinations(range(base.cols),len(g.pivots(base))))
  assert positions==eligible
  coverage[sid]={'pivot_position_sets':sorted(positions),'eligible_position_sets':len(eligible),'unexercised':[],'sampled_integers':sorted(numeric),'permutations_checked':len(list(itertools.permutations(range(base.cols))))}
  changed=independent(g.generate('easy',123,sid));review.append('## '+sid+'\n\nSource\n\n'+g.markdown(rec)+'\n\nChanged positions and entries\n\n'+g.markdown(changed))
  # Hold all non-solution content fixed and ensure stale references/keys fail.
  bad=copy.deepcopy(changed);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('pivots in the ','pivots in the $99$th and ')
  try:math_question(bad['question'])
  except AssertionError:pass
  else:raise AssertionError('Stale pivot prose admitted')
  bad=copy.deepcopy(changed);f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  try:math_question(bad['question'])
  except AssertionError:pass
  else:raise AssertionError('Wrong answer key admitted')
 for level in ('moderate','hard','unclassified'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported level admitted')
 batch=g.batch('easy',100,124478);assert len({fingerprint(r['question']) for r in batch})==len(batch)
 save('source-replay.json',{'status':'pass','complete_banks':'16/16','distractors':'64/64','options':'80/80','profiles':replays,'legacy_duplicate_field':'q-35391: original unkeyed field has identical full five-value bank; source remains untouched and is excluded from inventory'})
 save('template-extraction.json',components);save('slot-coverage.json',coverage);save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'status':'pass','source_basis':g.SNAPSHOT['basis'],'supported_levels':['easy'],'source_fidelity':'16/16 complete keyed banks, 64/64 distractors; exact prompt/solution replay; original typo evidence retained','exhaustive_profile_permutations':total,'distinct_structural_tasks':len(tasks),'normal_sample_records':480,'native_grading':json.loads((HERE/'native-grading.json').read_text())|{'records':'see native-grading.json'},'negative_controls_rejected':32,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
