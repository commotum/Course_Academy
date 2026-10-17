"""Display-derived and native grading checks for direct statement checkboxes."""
import sys
sys.dont_write_bytecode=True
import copy, hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
D=Path(__file__).resolve().parent
MODULE=D.parent.with_suffix('.py')
spec=importlib.util.spec_from_file_location('statement_generator',MODULE)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def check(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in prompt+sol)
 found=re.findall(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S)
 assert len(found)==3
 dims={}
 for name,body in found:
  rows=[[x.strip() for x in row.split('&')] for row in body.split('\\\\')]
  assert len({len(row) for row in rows})==1
  assert all(re.fullmatch(r'-?\d+',v) for row in rows for v in row)
  dims[name]=(len(rows),len(rows[0]))
 fields=q[':question/answer-fields'];assert len(fields)==3
 pairs=[];truth=[];ids={q[':question/id']}
 for f in fields:
  m=re.fullmatch(r'The product \$([A-Z])([A-Z])\$ is well defined\.',f[':answer-field/key'])
  assert m,f[':answer-field/key']
  pair=m.groups();pairs.append(pair);ok=dims[pair[0]][1]==dims[pair[1]][0];truth.append(ok)
  assert f[':answer-field/type']==':answer-field.type/checkbox'
  assert f[':answer-field/id'] not in ids;ids.add(f[':answer-field/id'])
  choices=f[':answer-field/choices']
  assert sorted((a[':answer/type'],a[':answer/value']) for a in choices)==[(':answer.type/text','false'),(':answer.type/text','true')]
  for a in choices:
   assert a[':answer/id'] not in ids;ids.add(a[':answer/id'])
  assert f[':answer-field/correct'][0]==':answer/id'
  assert next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1])==str(ok).lower()
 assert len(set(pairs))==3 and any(truth)
 assert not re.search(r'\bI{1,3}\b',prompt+'\n'+sol)
 assert 'The product $' not in prompt and 'Select all that apply.' in prompt
 assert prompt.count('class="matrix-operands"')==1
 opening=sol.split('\n\n')[0]
 openingdims=re.findall(r'\$([A-Z])\$ is a \$(\d+)\\times (\d+)\$ (matrix|row vector|column vector)',opening)
 assert len(openingdims)==3
 for name,r,c,noun in openingdims:
  assert dims[name]==(int(r),int(c))
  assert noun==('row vector' if int(r)==1 else 'column vector' if int(c)==1 else 'matrix')
 prose=re.findall(r'(?:There are|There is|there are|there is) \$(\d+)\$ columns? in \$([A-Z])\$ and \$(\d+)\$ rows? in \$([A-Z])\.\$ Since the number of columns in \$([A-Z])\$ (equals|does \*\*not\*\* equal) the number of rows in \$([A-Z])(?:,\$|\$,)',sol)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
 assert len(prose)==len(blocks)==3
 for (a,b),ok,row,eq in zip(pairs,truth,prose,blocks):
  c,x,r,y,x2,relation,y2=row
  assert (x,y,x2,y2)==(a,b,a,b) and int(c)==dims[a][1] and int(r)==dims[b][0]
  assert (relation=='equals')==ok
  clean=re.sub(r'\\boxed\{\\text\{(\d+)\}\}',r'\1',eq)
  m=re.fullmatch(r'\{([A-Z])\}_\{(\d+)\\times (\d+)\}\{\\times \}_\{(✓|\\ne )\}\{([A-Z])\}_\{(\d+)\\times (\d+)\}=\\text\{(well defined|undefined)\}',clean)
  assert m,eq
  aa,ar,ac,comparison,bb,br,bc,result=m.groups()
  assert (aa,bb)==(a,b) and (int(ar),int(ac))==dims[a] and (int(br),int(bc))==dims[b]
  assert (comparison=='✓')==ok and (result=='well defined')==ok
  assert eq.count('\\boxed')==(2 if ok else 0)
 conclusion=sol.split('\n\n')[-1]
 sentences=conclusion.split('. ')
 described={}
 for sentence in sentences:
  result=sentence.endswith('well defined.') or sentence.endswith('well defined')
  assert sentence.startswith('The product')
  for pair in re.findall(r'\$([A-Z]{2})\$',sentence):
   assert pair not in described;described[pair]=result
 assert described=={a+b:ok for (a,b),ok in zip(pairs,truth)}
 assert rec['generation']['version']==g.VERSION
 assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
 assert rec['generation']['task_fingerprint']==g.digest([sorted(dims.values()),sorted((dims[a],dims[b]) for a,b in pairs)])
 return truth

raw_before=json.loads((D/'raw-before.json').read_text());raw_after={}
for t,before in raw_before.items():
 after=g.generate(g.source_level(t),template=t,parameters=g.source_parameters(t),profile='raw-'+t)
 assert after==before,t
 assert after['generation']['evidence_only'] and not after['generation']['eligible_for_learning']
 raw_after[t]=after
(D/'raw-after.json').write_text(json.dumps(raw_after,indent=2))
records=[];reviews=[];counts={};patterns={};fingerprints={}
for t in [*g.SOURCES,'mixed-orientations']:
 level=g.source_level(t) if t in g.SOURCES else 'hard';counts[t]=0;patterns[t]=set();fingerprints[t]=set()
 for seed in range(300):
  rec=g.generate(level,seed,template=t);truth=check(rec);counts[t]+=1
  patterns[t].add(tuple(truth));fingerprints[t].add(rec['generation']['task_fingerprint'])
  assert rec==g.generate(level,seed,template=t)
  explicit=g.generate(level,seed+1000,template=t,parameters=rec['generation']['parameters'])
  assert explicit['question']==rec['question']
  if seed in [0,1,19,31,73]:records.append(rec)
  if seed==31:reviews.append(rec)
# Reproduce the reported empty-selection case and another ordinary-matrix case.
invalids=[]
for level,t,dims,pairs in [
 ('moderate','q-129437',[(3,2),(1,2),(1,5)],[[2,0],[0,2],[1,2]]),
 ('easy','q-42374',[(2,3),(2,3),(2,3)],[[0,1],[1,0],[0,2]])]:
 p={'arrays':[[[0]*c for _ in range(r)] for r,c in dims],'products':pairs}
 try:g.generate(level,template=t,parameters=p)
 except ValueError as e:assert 'at least one well-defined product' in str(e);invalids.append({'level':level,'template':t,'error':str(e)})
 else:raise AssertionError('Accepted empty selection')
 # These remain available only as explicit evidence-only source replay.
 raw=g.generate(level,template=t,parameters=p,profile='raw-'+t)
 assert not raw['generation']['eligible_for_learning'] and raw['generation']['evidence_only']
 assert all(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='false' for f in raw['question'][':question/answer-fields'])
# Check validator sensitivity to errors which this repair must prevent.
mutations=[]
for name in ['roman-label','duplicate-list','wrong-key','solution-product','missing-stage']:
 rec=copy.deepcopy(reviews[0]);q=rec['question']
 if name=='roman-label':q[':question/answer-fields'][0][':answer-field/key']='I'
 elif name=='duplicate-list':q[':question/problem']+='\n\nI. '+q[':question/answer-fields'][0][':answer-field/key']
 elif name=='wrong-key':
  f=q[':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
 elif name=='solution-product':q[':question/worked-solution']=q[':question/worked-solution'].rsplit('\n\n',1)[0]+'\n\nThe product $ZZ$ is well defined.'
 else:q[':question/worked-solution']=re.sub(r'\$\$\n.*?\n\$\$','',q[':question/worked-solution'],count=1,flags=re.S)
 try:check(rec)
 except (AssertionError,KeyError,StopIteration):mutations.append(name)
 else:raise AssertionError('Validator missed '+name)
engine=[]
for n,rec in enumerate(records+list(raw_after.values())):
 fields=rec['question'][':question/answer-fields'];checks=[];keymask=0
 for i,f in enumerate(fields):
  for a in f[':answer-field/choices']:
   correct=a[':answer/id']==f[':answer-field/correct'][1]
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'Owned Boolean member'})
   if correct and a[':answer/value']=='true':keymask|=1<<i
 engine.append({'label':str(n),'record':rec,'checks':checks,'subset_expected':[mask==keymask for mask in range(8)]})
(D/'engine-input.json').write_text(json.dumps(engine))
subprocess.run([str(D.parent/'whole-check'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
(D/'review.json').write_text(json.dumps(reviews,indent=2))
(D/'review.md').write_text('\n\n'.join(g.markdown(r) for r in reviews))
report={'passed':True,'version':g.VERSION,'generator_sha256':hashlib.sha256(MODULE.read_bytes()).hexdigest(),'raw_replays_exactly_preserved':len(raw_after),'sampled_normal_records':sum(counts.values()),'per_template':counts,'deterministic_replays':sum(counts.values()),'explicit_seed_independent_replays':sum(counts.values()),'nonempty_selection_required':True,'empty_parameter_rejections':invalids,'mutation_regressions':mutations,'native_records':len(engine),'native_field_checks':len(engine)*6,'native_subset_checks':len(engine)*8,'native_missing_or_extra_field_rejections':len(engine)*4,'truth_patterns':{t:sorted(map(list,p)) for t,p in patterns.items()},'unique_mathematical_tasks':{t:len(v) for t,v in fingerprints.items()}}
(D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
