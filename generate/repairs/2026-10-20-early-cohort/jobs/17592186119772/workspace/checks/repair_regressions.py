#!/usr/bin/env python3
"""Retained findings, independently reading visible matrices and actual delivery."""
import copy
from collections import Counter,defaultdict
from decimal import Decimal
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1];E=W/'evidence';E.mkdir(exist_ok=True)
sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('current_generator',W/'17592186119772.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
REPO=Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
# Separate parser and exact-zero witness; no use of generator's metadata or predicates.
RX=re.compile(r'([A-E])\s*=\s*(?:\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\[\\begin\{aligned\}(.*?)\\end\{aligned\}\])',re.S)
def parse(text):
 out={}
 for m in RX.finditer(text):
  a=tuple(tuple(Decimal(v.strip()) for v in row.split('&')) for row in (m[2] if m[2] is not None else m[3]).split(r'\\'))
  assert a and all(len(row)==len(a) for row in a)
  assert m[1] not in out or out[m[1]]==a
  out[m[1]]=a
 return out
def kind(x):return x.get(':db/ident') if isinstance(x,dict) else x
def correct(f):
 ref=f[':answer-field/correct'];aid=ref[':answer/id'] if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def inspect(r):
 q=r['question'];fields=q[':question/answer-fields'];orientation='upper' if 'upper triangular' in q[':question/problem'] else 'lower'
 matrix=parse(q[':question/problem'])
 for f in fields:
  matrix.update(parse(f.get(':answer-field/key','')))
  for a in f[':answer-field/choices']:matrix.update(parse(a[':answer/value']))
 good=tuple(x for x,a in sorted(matrix.items()) if all(v==0 for i,row in enumerate(a) for j,v in enumerate(row) if (i>j if orientation=='upper' else i<j)))
 if kind(fields[0][':answer-field/type']).endswith('/checkbox'):
  actual=tuple(sorted(next(iter(parse(f[':answer-field/key']))) for f in fields if correct(f)=='true'))
 elif parse(correct(fields[0])):actual=tuple(parse(correct(fields[0])))
 else:actual=tuple(sorted(re.findall(r'\$([A-E])\$',correct(fields[0]))))
 assert actual==good,(q[':question/id'],actual,good)
 solution=q[':question/worked-solution']
 if len(matrix)==5 and kind(fields[0][':answer-field/type']).endswith('/radio'):
  assert re.search(r'Notice that \$([A-E])\$',solution)[1]==good[0]
  assert parse(solution)==matrix
 else:
  stated=tuple(sorted(re.findall(r'\$([A-E])\$',solution.split(' since')[0])))
  assert stated==good,(stated,good)
 for label,row,col,value in re.findall(r'\{([a-e])\}_\{([1-4])([1-4])\}\s*&\s*=(-?\d+(?:\.\d+)?)\\ne 0',solution):
  i,j=int(row)-1,int(col)-1
  assert (i>j if orientation=='upper' else i<j)
  assert matrix[label.upper()][i][j]==Decimal(value)!=0
 return {'answer':good,'orientation':orientation,'dimensions':tuple(len(a) for _,a in sorted(matrix.items())),
         'correct_position':None if len(fields)>1 else next(i for i,a in enumerate(fields[0][':answer-field/choices']) if a[':answer/value']==correct(fields[0])),
         'semantic':(orientation,tuple(sorted((len(a),tuple((i,j) for i,row in enumerate(a) for j,v in enumerate(row) if i!=j and v)) for a in matrix.values())))}
def save(name,value): (E/name).write_text(json.dumps(value,indent=2)+'\n')
def delivery(records,name):
 save(name+'-input.json',records)
 cmd=[str(PY),str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/(name+'-input.json')),'--source',str(W.parent/'source/source.json'),'--inventory',str(W.parent/'source/inventory.json'),'--difficulty','easy','--output',str(E/name),'--math-root','/media/jake/SSD/EDB/math']
 result=subprocess.run(cmd,capture_output=True,text=True)
 assert result.returncode==0,result.stderr+result.stdout
 commands.append(cmd)
 return json.loads((E/name/'accepted.json').read_text())
commands=[];tests=[];source=json.loads((W.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
# Exact latest failure and its demanded sentence.
failure=json.loads((E/'minimal-failing-case.json').read_text())
swap=g.generate_easy(seed=failure['seed'],profile=failure['source_profile'],parameters=failure['parameters'])
assert inspect(swap)['answer']==('A',)
assert 'Notice that $A$' in swap['question'][':question/worked-solution']
tests.append('exact_q126354_A_E_role_swap')
# Complete source banks, original parameters, response contracts, prompt/solution.
replays=[];matched_choices=0
for original in source:
 sid=original[':question/math-academy-id'];level=kind(original[':question/difficulty']).rsplit('/',1)[1]
 r=g.generate(level,seed=19673,profile='raw:'+sid);q=r['question'];inspect(r)
 for key in [':question/problem',':question/worked-solution']:assert q[key]==original[key],(sid,key)
 assert q[':question/difficulty']==kind(original[':question/difficulty'])
 def signature(f):return (f[':answer-field/key'],kind(f[':answer-field/type']),sorted((a[':answer/value'],kind(a[':answer/type'])) for a in f[':answer-field/choices']),correct(f))
 assert sorted(map(signature,q[':question/answer-fields']))==sorted(map(signature,original[':question/answer-fields'])),sid
 matched_choices+=sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields'])
 replays.append(r)
save('source-replay-records.json',replays)
save('source-replay.json',{'banks':len(replays),'matched_choices':matched_choices,'missing':[],'contracts':'8 easy radio, 4 moderate checkbox, 1 moderate subset radio'})
tests.append('all_13_current_source_banks')
# Ordinary generation, modest per-profile regression sample, no preselected good seeds.
normal=[];easy=[];summaries={}
for original in source:
 sid=original[':question/math-academy-id'];level=kind(original[':question/difficulty']).rsplit('/',1)[1]
 rs=[g.generate(level,seed=20261022+i,profile=sid) for i in range(12 if level=='easy' else 4)]
 stats=[inspect(r) for r in rs];normal.extend(rs)
 if level=='easy':easy.extend(rs)
 answers=Counter(str(s['answer']) for s in stats)
 assert len(answers)>1,(sid,answers)
 assert len({s['dimensions'] for s in stats})==1
 summaries[sid]={'n':len(rs),'answers':dict(answers),'orientations':dict(Counter(s['orientation'] for s in stats)),'semantic_instances':len({s['semantic'] for s in stats})}
for profile in ['hard_two','hard_three']:
 for seed in [9,10]:
  r=g.generate_hard(seed=seed,profile=profile);inspect(r);normal.append(r)
save('normal-records.json',normal)
# Controlled all eligible roles: leave dimensions, diagonal values and allowed entries fixed.
controlled=[];role_coverage={}
for original in source:
 sid=original[':question/math-academy-id'];level=kind(original[':question/difficulty']).rsplit('/',1)[1]
 src={};src.update(parse(original[':question/problem']))
 for f in original[':question/answer-fields']:
  src.update(parse(f[':answer-field/key']))
  for a in f[':answer-field/choices']:src.update(parse(a[':answer/value']))
 subsets=[(x,) for x in src] if level=='easy' else [x for n in (1,2) for x in itertools.combinations(sorted(src),n)]
 roles=[]
 for good in subsets:
  mats={}
  for label,a in src.items():
   n=len(a);mat=[[0]*n for _ in range(n)]
   for i in range(n):mat[i][i]=2+ord(label)-ord('A')
   mat[0][n-1]=3 # same irrelevant allowed evidence for every role assignment
   if label not in good:mat[n-1][0]=5
   mats[label]=mat
  r=g.generate(level,seed=51,profile=sid,parameters={'criterion':'upper','matrices':mats})
  assert inspect(r)['answer']==tuple(sorted(good));controlled.append(r);roles.append(''.join(sorted(good)))
 role_coverage[sid]=roles
# Unchanged matrices, changed target orientation; valid unique answers in each direction.
p={'criterion':'upper','matrices':{'A':[[1,3],[0,2]],'B':[[1,0],[4,2]],'C':[[1,5],[6,2]],'D':[[2,7],[8,1]],'E':[[3,9],[10,1]]}}
a=g.generate_easy(seed=7,profile='q-126354',parameters=p);assert inspect(a)['answer']==('A',)
p['criterion']='lower';b=g.generate_easy(seed=7,profile='q-126354',parameters=p);assert inspect(b)['answer']==('B',)
controlled.extend([a,b])
# Change irrelevant diagonal and upper-side evidence while retaining upper membership.
p['criterion']='upper'
for mat in p['matrices'].values():
 mat[0][0]=-11;mat[1][1]=0
 mat[0][1]=-7
c=g.generate_easy(seed=7,profile='q-126354',parameters=p);assert inspect(c)['answer']==('A',)
controlled.append(c)
save('controlled-records.json',controlled)
tests+=['every_source_profile_eligible_roles_at_fixed_dimensions','unchanged_matrices_changed_orientation','irrelevant_entries_preserve_response']
# Regenerate the exact original five seeds; no replacement or favorable seed search.
old=json.loads((W.parent/'samples.json').read_text())
batch=[g.generate_easy(seed=r['generation']['seed']) for r in old]
assert len(set(inspect(r)['answer'] for r in batch))>1
surviving_batch=delivery(batch,'delivery-batch');assert len(surviving_batch)==5
assert len(set(inspect(r)['answer'] for r in surviving_batch))>1
tests.append('original_batch_seeds_after_delivery_have_multiple_answers')
# Conditional shortcut checks before and after real publisher filtering.
def shortcuts(records):
 rows=[(r,inspect(r)) for r in records];out={}
 for name,key in [('profile',lambda r,s:r['generation']['profile']),('labeled_dimensions',lambda r,s:s['dimensions']),('profile_orientation',lambda r,s:(r['generation']['profile'],s['orientation']))]:
  groups=defaultdict(list)
  for r,st in rows:groups[str(key(r,st))].append(st)
  out[name]=[{'cue':k,'n':len(v),'distinct_answers':len({x['answer'] for x in v}),'best_constant_label_hits':max(Counter(x['answer'] for x in v).values()),'baseline':0.2} for k,v in groups.items()]
  assert all(x['distinct_answers']>1 for x in out[name] if x['n']>=3),(name,out[name])
 out['fixed_label']={x:sum(st['answer']==(x,) for _,st in rows) for x in 'ABCDE'}
 out['fixed_position']=dict(Counter(st['correct_position'] for _,st in rows))
 assert max(out['fixed_label'].values())<len(rows)
 assert max(out['fixed_position'].values())<len(rows)
 out['total']=len(rows);out['semantic_instances']=len({st['semantic'] for _,st in rows})
 return out
pre=shortcuts(easy);accepted=delivery(easy,'delivery-control');post=shortcuts(accepted)
save('pedagogical-variation.json',{'before_delivery':pre,'after_delivery':post,'profiles':summaries,'controlled_eligible_roles':role_coverage,'counterfactuals':'controlled-records.json','note':'Semantic identity ignores labels, diagonal and nonzero magnitudes. Diagonal recognition is valid use of the zero-side rule, not an incidental cue.'})
save('batch-results.json',{'seeds':[r['generation']['seed'] for r in batch],'raw_answers':[inspect(r)['answer'] for r in batch],'delivered_answers':[inspect(r)['answer'] for r in surviving_batch],'accepted':len(surviving_batch)})
save('commands.json',commands)
save('regression-results.json',{'passed':True,'tests':tests,'normal_records':len(normal),'controlled_records':len(controlled),'source_banks':len(replays),'exact_counterexample':swap})
print(json.dumps({'passed':True,'source_banks':len(replays),'source_choices':matched_choices,'normal_records':len(normal),'controlled_records':len(controlled),'delivery':len(accepted),'batch_answers':[inspect(r)['answer'] for r in surviving_batch]}))
