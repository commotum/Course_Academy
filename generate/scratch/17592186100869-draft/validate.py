"""Independent displayed-content, fidelity, native finite-subset and identity QA."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,platform,re,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('draft00869',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def read_display(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in prompt+sol)
 found=re.findall(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S);assert len(found)==3
 dims={}
 for name,body in found:
  rows=[[x.strip() for x in r.split('&')] for r in body.split('\\\\')]
  assert rows and len({len(r) for r in rows})==1
  assert all(re.fullmatch('-?\\d+',x) for r in rows for x in r)
  dims[name]=(len(rows),len(rows[0]))
 pairs=re.findall(r'The product \$([A-Z])([A-Z])\$ is well defined',prompt);assert len(pairs)==3 and len(set(pairs))==3
 truth=[dims[a][1]==dims[b][0] for a,b in pairs]
 fields=q[':question/answer-fields'];assert len(fields)==3
 for f,k,ok in zip(fields,['I','II','III'],truth):
  assert f[':answer-field/key']==k and f[':answer-field/type']==':answer-field.type/checkbox'
  assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==[(':answer.type/text','false'),(':answer.type/text','true')]
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==str(ok).lower()
 opening=sol.split('\n\n')[0]
 openingdims=re.findall(r'\$([A-Z])\$ is a \$(\d+)\\times (\d+)\$ (matrix|row vector|column vector)',opening)
 assert len(openingdims)==3
 for name,r,c,noun in openingdims:
  assert dims[name]==(int(r),int(c))
  assert noun==('row vector' if int(r)==1 else 'column vector' if int(c)==1 else 'matrix')
 prose=re.findall(r'(?:There are|There is|there are|there is) \$(\d+)\$ columns? in \$([A-Z])\$ and \$(\d+)\$ rows? in \$([A-Z])\.\$ Since the number of columns in \$([A-Z])\$ (equals|does \*\*not\*\* equal) the number of rows in \$([A-Z])(?:,\$|\$,)',sol)
 assert len(prose)==3,prose
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==3
 for n,((a,b),ok,row,eq) in enumerate(zip(pairs,truth,prose,blocks)):
  c,x,r,y,x2,relation,y2=row
  assert (x,y,x2,y2)==(a,b,a,b) and int(c)==dims[a][1] and int(r)==dims[b][0]
  assert (relation=='equals')==ok
  # Parse actual ordered-factor annotations, not generation metadata.
  clean=re.sub(r'\\boxed\{\\text\{(\d+)\}\}',r'\1',eq)
  m=re.fullmatch(r'\{([A-Z])\}_\{(\d+)\\times (\d+)\}\{\\times \}_\{(✓|\\ne )\}\{([A-Z])\}_\{(\d+)\\times (\d+)\}=\\text\{(well defined|undefined)\}',clean)
  assert m,(eq,clean)
  aa,ar,ac,comparison,bb,br,bc,result=m.groups()
  assert (aa,bb)==(a,b) and (int(ar),int(ac))==dims[a] and (int(br),int(bc))==dims[b]
  assert (comparison=='✓')==ok and (result=='well defined')==ok
  assert eq.count('\\boxed')==(2 if ok else 0)
  if ok:assert re.findall(r'\\boxed\{\\text\{(\d+)\}\}',eq)==[str(dims[a][1]),str(dims[b][0])]
 ending=sol.split('\n\n')[-1]
 if ending=='We conclude that all three statements are true.':assert all(truth)
 elif ending=='We conclude that all three statements are false.':assert not any(truth)
 else:
  end=re.fullmatch(r'Therefore, statements? (.*?) (?:is|are) true, while statements? (.*?) (?:is|are) false\.',ending)
  assert end,ending
  yes=re.findall(r'\bI{1,3}\b',end[1]);no=re.findall(r'\bI{1,3}\b',end[2])
  assert sorted(yes+no)==['I','II','III'] and not set(yes)&set(no)
  assert [k in yes for k in ['I','II','III']]==truth
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 # Fingerprint is independently reconstructed from displayed matrix order and pairs.
 names=[n for n,b in found];assert rec['generation']['task_fingerprint']==g.digest([sorted(dims.values()),sorted((dims[a],dims[b]) for a,b in pairs)])
 return truth

def must_fail(rec):
 try:read_display(rec)
 except (AssertionError,KeyError,StopIteration):return
 raise AssertionError('Mutation escaped independent validator')

sources=[];fidelity=[]
for case in json.loads((D/'source-cases.json').read_text()):
 t=case['template'];q=g.SOURCES[t];rec=g.generate(case['level'],template=t,parameters=case['parameters'],profile=case['bank_profile']);read_display(rec);sources.append(rec)
 for key in [':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields']:
  assert (key in q)==(key in rec['question'])
 assert rec['question'][':question/problem']==g.normalize_prose(q[':question/problem'])
 assert rec['question'][':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])
 counts=[]
 for old,new in zip(q[':question/answer-fields'],rec['question'][':question/answer-fields']):
  assert old[':answer-field/key']==new[':answer-field/key'];assert old[':answer-field/type'][':db/ident']==new[':answer-field/type']
  assert sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in old[':answer-field/choices'])==sorted((a[':answer/type'],a[':answer/value']) for a in new[':answer-field/choices'])
  assert old[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);counts.append(2)
 fidelity.append({'template':t,'fields':3,'choices':6,'correct_designations':3,'prompt_exact_normalized':True,'solution_exact_normalized':True,'raw_prompt_exact':rec['question'][':question/problem']==q[':question/problem'],'raw_solution_exact':rec['question'][':question/worked-solution']==q[':question/worked-solution']})
(D/'source-fidelity.json').write_text(json.dumps({'passed':True,'MA_originals':10,'canonical_examples_counted_as_practice':0,'independent_questions':0,'complete_banks':30,'choices':60,'correct_designations':30,'reports':fidelity},indent=2))

records=[];coverage={};truthsets={};fingerprints={};templates={}
for level in g.LEVELS:
 coverage[level]=set();truthsets[level]=set();fingerprints[level]=set();templates[level]=set()
 for seed in range(240):
  r=g.generate(level,seed);truth=read_display(r);records.append(r);templates[level].add(r['generation']['template']);truthsets[level].add(tuple(truth));fingerprints[level].add(r['generation']['task_fingerprint']);coverage[level].update(tuple(x) for x in r['generation']['parameters']['products'])
  # Explicit calls use exactly the same public guards and fixed parameter identity.
  again=g.generate(level,seed+1000,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile']);assert again['question']==r['question']
  assert g.generate(level,seed)==r
 assert coverage[level]==set(itertools.permutations(range(3),2))
 assert templates[level]==set([t for t in g.SOURCES if g.source_level(t)==level] if level!='hard' else ['mixed-orientations'])
 assert len(fingerprints[level])>150
assert len(truthsets['easy'])>=6 and len(truthsets['moderate'])>=6
# Every changed requested ordered pair in a fixed array set gets independently reread.
role_checks=0
for level in g.LEVELS:
 r=g.generate(level,19);p=r['generation']['parameters']
 for pairs in itertools.permutations(list(itertools.permutations(range(3),2)),3):
  pp=copy.deepcopy(p);pp['products']=list(map(list,pairs))
  try:q=g.generate(level,template=r['generation']['template'],parameters=pp)
  except ValueError:
   assert level=='hard';continue
  read_display(q);role_checks+=1
# Statement-order and matrix-slot aliases must not create mathematical tasks.
identity_alias_checks=0
for level in g.LEVELS:
 original=g.generate(level,17);p=copy.deepcopy(original['generation']['parameters']);p['products'].reverse()
 reversed_statements=g.generate(level,template=original['generation']['template'],parameters=p)
 assert reversed_statements['generation']['task_fingerprint']==original['generation']['task_fingerprint']
 assert reversed_statements['question'][':question/id']!=original['question'][':question/id']
 identity_alias_checks+=1
# Mutations target independently read prose/annotations/stages/keys/control bytes.
r=records[0];mutations=0
for edit in ['prompt-product','opening-dimension','prose-dimension','box','comparison','conclusion','field-key','control-character','missing-stage']:
 x=copy.deepcopy(r);q=x['question']
 if edit=='prompt-product':q[':question/problem']=re.sub(r'The product \$([A-Z])([A-Z])\$',lambda m:'The product $'+m[2]+m[1]+'$',q[':question/problem'],count=1)
 elif edit=='opening-dimension':q[':question/worked-solution']=re.sub(r'is a \$\d+',lambda m:'is a $9',q[':question/worked-solution'],count=1)
 elif edit=='prose-dimension':q[':question/worked-solution']=re.sub(r'columns in \$([A-Z])\$ and \$\d+',lambda m:'columns in $'+m[1]+'$ and $9',q[':question/worked-solution'],count=1)
 elif edit=='box':q[':question/worked-solution']=q[':question/worked-solution'].replace('\\boxed{\\text{','\\text{',1)
 elif edit=='comparison':q[':question/worked-solution']=q[':question/worked-solution'].replace('{\\times }_{✓}','{\\times }_{\\ne }',1) if '✓' in q[':question/worked-solution'] else q[':question/worked-solution'].replace('{\\times }_{\\ne }','{\\times }_{✓}',1)
 elif edit=='conclusion':q[':question/worked-solution']+=' False.'
 elif edit=='field-key':q[':question/answer-fields'][0][':answer-field/key']='IV'
 elif edit=='control-character':q[':question/worked-solution']+='\f'
 else:q[':question/worked-solution']=re.sub(r'\$\$\n.*?\n\$\$','',q[':question/worked-solution'],count=1,flags=re.S)
 must_fail(x);mutations+=1
invalids=0
for level in g.LEVELS:
 base=g.generate(level,0)
 for kind in ['entry','dimension','samefactor','duplicate-pair','role']:
  p=copy.deepcopy(base['generation']['parameters'])
  if kind=='entry':p['arrays'][0][0][0]=10
  elif kind=='dimension':p['arrays'][0]=[[0]*6]
  elif kind=='samefactor':p['products'][0]=[0,0]
  elif kind=='duplicate-pair':p['products'][0]=p['products'][1]
  else:p['arrays']=[[[1]],[[1]],[[1]]]
  try:g.generate(level,template=base['generation']['template'],parameters=p)
  except ValueError:invalids+=1
  else:raise AssertionError('Invalid explicit parameters accepted')
# Native grade_field checks use both complete Boolean members in every field.
engine=[]
for n,r in enumerate(sources+records):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Full Boolean member; false is explicit unselected response'})
 engine.append({'label':str(n),'record':r,'checks':checks})
(D/'engine-input.json').write_text(json.dumps(engine));subprocess.run([str(D/'check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
reviews=[]
for t in [*g.SOURCES,'mixed-orientations']:
 level='hard' if t=='mixed-orientations' else g.source_level(t)
 for seed in [31,73]:reviews.append(g.generate(level,seed,template=t))
(D/'review.json').write_text(json.dumps(reviews,indent=2));(D/'review.md').write_text('# Original MA practice replays\n\n'+'\n\n'.join(g.markdown(r) for r in sources)+'\n\n# Generated variants (authored parameter and target slots)\n\n'+'\n\n'.join(g.markdown(r) for r in reviews))
(D/'slot-coverage.json').write_text(json.dumps({'roles':{l:sorted(map(list,s)) for l,s in coverage.items()},'truth_patterns':{l:sorted(map(list,s)) for l,s in truthsets.items()},'unique_meaningful_sampled_tasks':{l:len(s) for l,s in fingerprints.items()},'default_templates':{l:sorted(s) for l,s in templates.items()},'changed_roles_fixed_arrays':role_checks},indent=2))
# Immutable baseline path-set and all 42 current native dependencies must remain exact.
before=json.loads((D/'numeric-before-import.json').read_text());assert before['files']=={}
p=ROOT/'generate/scratch/17592186100869.py';assert not p.exists() and not p.with_suffix('').exists() and not list(p.parent.glob('__pycache__/17592186100869.*.pyc'))
paths=json.loads((D/'reference/native-42-before.json').read_text())
for p,h in paths.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
(D/'reference/native-42-after.json').write_text(json.dumps(paths,indent=2))
report={'passed':True,'python':platform.python_version(),'source_replays':10,'sampled_records':720,'explicit_seed_independent_replays':720,'fixed_array_target_role_checks':role_checks,'mathematical_identity_alias_checks':identity_alias_checks,'mutation_regressions':mutations,'invalid_explicit_cases':invalids,'native_field_checks':len(engine)*6,'native_42_recheck':True,'numeric_absence_recheck':True,'difficulty_task_domain_sizes':{l:r['canonical_meaningful_tasks'] for l,r in json.loads((D/'semantic-catalog.json').read_text())['levels'].items()},'entry_values_incidental_not_task_counted':True,'related_reports':['render-validation.json','whole-validation.json']}
(D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
