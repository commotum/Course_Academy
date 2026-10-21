"""Deterministic mathematical and response-layout validation; no database writes."""
from pathlib import Path
import importlib.util,hashlib,json,re,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists());sys.path.insert(0,str(ROOT))
from scripts.generator_publish import validate_question
STAGE=HERE/'package-source';IDS=['17592186119772','17592186119784']
def load(kp,path=None):
 p=path or STAGE/(kp+'.py');spec=importlib.util.spec_from_file_location('gen_'+kp,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def check(m,rec):
 q=rec['question'];validate_question(q);meta=rec['generation'];assert meta['eligible_for_learning'] and not meta['evidence_only']
 fields=q[':question/answer-fields'];level=q[':question/difficulty'].split('/')[-1]
 if m.KP_ID==17592186119772 and level=='easy':
  assert len(fields)==1 and fields[0][':answer-field/type']==':answer-field.type/radio'
  assert all(r'\begin{bmatrix}' in a[':answer/value'] and r'[\begin{aligned}' not in a[':answer/value'] for a in fields[0][':answer-field/choices'])
  assert r'[\begin{aligned}' not in q[':question/worked-solution']
  assert all(body.count(r'\begin{bmatrix}')<=1 for body in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S))
  return
 assert all(f[':answer-field/type']==':answer-field.type/checkbox' for f in fields)
 actual=[]
 for f in fields:
  bank={a[':answer/id']:a[':answer/value'] for a in f[':answer-field/choices']}
  assert set(bank.values())=={'false','true'};actual.append(bank[f[':answer-field/correct'][1]]=='true')
 assert any(actual),'All-false normal output'
 assert 'Select all that apply.' in q[':question/problem']
 assert not re.search(r'(?:Statement |\b(?:I|II|III) only|\*\*(?:I|II|III)\.)',q[':question/worked-solution'])
 if m.KP_ID==17592186119772:
  assert not re.search(r'begin\{(?:aligned|bmatrix)\}',q[':question/problem'])
  criterion=meta['parameters']['criterion'];parsed=[]
  for f in fields:
   match=re.fullmatch(r'\$([A-E])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}\$',f[':answer-field/key'],re.S);assert match
   matrix=[[int(v.strip()) for v in row.split('&')] for row in match[2].split(r'\\')]
   assert matrix==meta['parameters']['matrices'][match[1]]
   assert m.qualifies(matrix,criterion)==actual[len(parsed)];parsed.append(matrix)
 else:
  assert q[':question/problem'].count(r'\begin{bmatrix}')==1
  parsed=m.read_matrix(q[':question/problem']);ss=m.statements('\n'.join(f[':answer-field/key'] for f in fields));assert len(ss)==3
  assert [m.truth(parsed,op,kind) for _,op,kind in ss]==actual
  assert all(f[':answer-field/key'] not in q[':question/problem'] for f in fields)

reports=[];reps=[]
for kp in IDS:
 m=load(kp);old=load(kp,ROOT/'generate/scratch'/(kp+'.py'));checks=0;catalog_fingerprints={}
 for level in m.LEVELS:
  for seed in range(100):
   rec=m.generate(level,seed);check(m,rec);assert rec==m.generate(level,seed);checks+=1
  if hasattr(m,'batch'):batch=m.batch(level,10000,17)
  else:
   profiles=[sid for sid in m.SOURCES if m.recipe(sid)['level']==level] if level!='hard' else ['hard_two','hard_three']
   unique={}
   for profile in profiles:
    for base in m.catalog(profile):
     rec=m.generate(level,17,parameters=m.fill_values(base,m.random.Random(17)),profile=profile)
     unique.setdefault(rec['generation']['mathematical_fingerprint'],rec)
   batch=list(unique.values())
  if isinstance(batch,tuple):batch=batch[0]
  for rec in batch:check(m,rec);checks+=1
  key='mathematical_fingerprint' if kp.endswith('772') else 'math_fingerprint'
  fps=[rec['generation'][key] for rec in batch];assert len(fps)==len(set(fps));catalog_fingerprints[level]=len(fps)
 raw_count=0
 if kp.endswith('772'):
  for sid in m.SOURCES:
   level=m.recipe(sid)['level'];raw=m.generate(level,5,profile='raw:'+sid);baseline=old.generate(level,5,profile='raw:'+sid)
   assert raw==baseline;raw_count+=1
   reps.append(m.generate(level,1,profile=sid))
  for profile in ('hard_two','hard_three'):reps.append(m.generate('hard',1,profile=profile))
  # Existing parameter constraints already reject every empty subset.
  profile=next(sid for sid in m.SOURCES if m.recipe(sid)['level']=='moderate')
  invalid=m.generate('moderate',1,profile=profile)['generation']['parameters']
  for matrix in invalid['matrices'].values():matrix[0][1]=matrix[1][0]=1
  try:m.generate('moderate',1,parameters=invalid,profile=profile)
  except ValueError:pass
  else:raise AssertionError('All-false explicit identification input accepted')
 else:
  for sid in m.QS:
   level=m.level(sid);raw=m.generate(level,5,template=sid,profile='source-replay');baseline=old.generate(level,5,template=sid,profile='source-replay')
   assert raw==baseline;raw_count+=1;reps.append(m.generate(level,1,template=sid))
  for matrix in [[[1,0,0],[0,2,0],[0,0,3]],[[1,2,0],[0,2,3],[0,0,3]],[[1,0,0],[2,2,0],[0,3,3]]]:reps.append(m.generate('easy',1,parameters={'matrix':matrix}))
  try:m.generate('easy',1,parameters={'matrix':[[1,2,0],[2,3,0],[0,0,4]]})
  except ValueError as e:assert 'at least one' in str(e)
  else:raise AssertionError('All-false explicit statement input accepted')
 assert (STAGE/kp/'source.json').read_bytes()==(ROOT/'generate/scratch'/kp/'source.json').read_bytes()
 reports.append({'kp':int(kp),'generator_sha256':hashlib.sha256((STAGE/(kp+'.py')).read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((STAGE/kp/'source.json').read_bytes()).hexdigest(),'normal_records_checked':checks,'finite_batch_domains':catalog_fingerprints,'raw_source_replays_equal_original':raw_count,'frozen_source_unchanged':True,'all_false_rejected':True,'runtime_files':[kp+'.py',kp+'/source.json']})
(HERE/'representative-records.json').write_text(json.dumps(reps,indent=2)+'\n')
result={'passed':True,'records':len(reps),'generators':reports,'python':sys.version.split()[0],'sympy':m.sp.__version__}
(HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
