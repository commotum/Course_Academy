import json,pathlib,itertools,math,copy,shutil,os,importlib.util,hashlib,collections
from audit import g,fields,answer,independently_check,save,mirror_probe
from pixel_probe import geometry
ROOT=pathlib.Path.cwd();JOB=ROOT.parent;PKG=JOB/'workspace'
source=json.load(open(JOB/'source/source.json'));cases={v['id']:v for v in json.load(open('source-analysis.json'))['source_cases']};records=json.load(open('source-replay-records.json'))
def distance(a,b):
 d=abs(a-b);return min(d,180-d)
replay=[]
for r,q in zip(records,source['material']['kp'][':knowledge-point/questions']):
 p=cases[q[':question/math-academy-id']]['points'];src=[]
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  d=geometry(pathlib.Path('/media/jake/SSD/EDB/math')/a[':answer/value'],p,'source');src.append({'asset':a[':answer/value'],'angles':[v['angle_degrees'] for v in d]})
 target=[]
 for a in fields(r)[':answer-field/choices']:
  d=json.load(open(pathlib.Path(a[':answer/value']).with_suffix('.json')));mp={tuple(pt):v for pt,v in zip(d['exact_points'],d['slopes'])};target.append({'asset':a[':answer/value'],'angles':[90 if mp[tuple(pt)]=='inf' else math.degrees(math.atan(float(__import__('fractions').Fraction(mp[tuple(pt)])))) for pt in p]})
 errors=[[max(distance(a,b) for a,b in zip(s['angles'],t['angles'])) for t in target] for s in src]
 perm=min(itertools.permutations(range(5)),key=lambda z:sum(errors[i][j] for i,j in enumerate(z)))
 row={'source_id':q[':question/math-academy-id'],'question_id':q[':question/id'],'prompt_exact':r['question'][':question/problem']==q[':question/problem'],'full_bank':[{'original':src[i],'generated':target[j],'max_angle_error_degrees':errors[i][j]} for i,j in enumerate(perm)],'max_angle_error_degrees':max(errors[i][j] for i,j in enumerate(perm))}
 row['interpretation']='same complete bank within rasterization tolerance' if row['max_angle_error_degrees']<3 else 'inspect source discrepancy'
 replay.append(row)
save('source-bank-comparison.json',replay);print('source banks',[(r['source_id'],round(r['max_angle_error_degrees'],2)) for r in replay],flush=True)
# Verify generator actual deterministic relocation with only manifest runtime files.
manifest=json.load(open(PKG/'package.json'));rel=[]
for stem in ['relocation-a','nested/relocation-b']:
 dest=ROOT/stem;dest.mkdir(parents=True,exist_ok=True)
 for name in manifest['files']:
  p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/name,p)
 out=dest/'generated-assets';os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(out)
 spec=importlib.util.spec_from_file_location('relocated_'+str(len(rel)),dest/manifest['entrypoint']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 r=m.generate('easy',seed=73981,template='affine_fraction');rel.append({'root':str(dest),'output':str(out),'record':r})
for rr in rel:
 assert all(pathlib.Path(a[':answer/value']).is_file() and pathlib.Path(a[':answer/value']).is_relative_to(rr['output']) for a in fields(rr['record'])[':answer-field/choices'])
normalized=[json.dumps(rr['record'],sort_keys=True).replace(rr['output'],'OUTPUT') for rr in rel]
assert normalized[0]==normalized[1]
save('relocation-results.json',{'manifest':manifest,'normalized_identical':True,'records':rel,'command':'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python finish_checks.py'})
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(ROOT/'assets')
r=g.generate('easy',seed=73982,template='affine',parameters={'a':1,'b':2,'points':[[-4,1],[4,-1],[1,4]]});r2=g.generate('easy',seed=73982,template='affine',parameters={'a':1,'b':2,'points':[[-4,1],[4,-1],[1,4]]});assert r==r2
save('boundary-records.json',[r]);save('boundary-results.json',{'deterministic':True,'math':independently_check(r)})
# Shared delivery changes UUIDs and paths: measure predictions on normalized bytes, using SHA256 map to the original raster geometries.
raw=json.load(open('independent-samples.json'))+json.load(open('runner-batch.json'));sha_geometry={}
for r in raw:
 for a in fields(r)[':answer-field/choices']:
  p=pathlib.Path(a[':answer/value']);sha_geometry[hashlib.sha256(p.read_bytes()).hexdigest()]=json.load(open(p.with_suffix('.json')))['slopes']
from audit import signs
import sympy as S
stages=[];grader=[]
for folder in ['delivery-independent','delivery-runner']:
 accepted=json.load(open(ROOT/folder/'accepted.json'));probes=[]
 for r in accepted:
  f=fields(r);sl=[]
  for a in f[':answer-field/choices']:
   p=ROOT/folder/'assets'/a[':answer/value'];sl.append([S.Rational(v) for v in sha_geometry[hashlib.sha256(p.read_bytes()).hexdigest()]])
  pair=[(i,j) for i in range(5) for j in range(i) if all(a==-b for a,b in zip(sl[i],sl[j]))];entry={'id':r['question'][':question/id'],'seed':r['generation']['seed'],'template':r['generation']['template'],'pairs':pair}
  if len(pair)==1:
   ps=pair[0];scores={i:sum(a==b and a!=0 for j in range(5) if j not in ps for a,b in zip(signs(sl[i]),signs(sl[j]))) for i in ps};win=[i for i in ps if scores[i]==max(scores.values())];entry['scores']=scores
   if len(win)==1:
    aa=f[':answer-field/choices'][win[0]];expected=aa[':answer/id']==f[':answer-field/correct'][1];entry['success']=expected;entry['predicted_index']=win[0]
    grader.append({'label':folder+' visual-only prediction '+str(entry['seed']),'record':r,'checks':[{'submitted_answer_id':aa[':answer/id'],'expected':'accepted' if expected else 'rejected','purpose':'mirror-pair direction-consensus strategy; no equation used'}]})
  probes.append(entry)
 stages.append({'stage':folder,'records':probes,'decisive':sum('success' in p for p in probes),'correct':sum(p.get('success',False) for p in probes)})
save('delivered-shortcuts.json',stages);save('delivered-grader-input.json',grader)
# Faithful deterministic within-band selector for fresh usable easy candidates: policy weights [1,0,0]; stable sorted ID pool; history separately excluded.
accepted=json.load(open(ROOT/'delivery-independent/accepted.json'))+json.load(open(ROOT/'delivery-runner/accepted.json'))
# Virtual entity IDs are stable explicit fixtures, not DB assertions.
pool={900000+i:r for i,r in enumerate(accepted)};selected=[]
for i in range(96):
 seed='independent-review/'+str(i);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();uniform=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);ids=sorted(pool);qid=ids[min(int(uniform*len(ids)),len(ids)-1)];r=pool[qid];selected.append({'seed':seed,'fixture_entity':qid,'question_id':r['question'][':question/id'],'template':r['generation']['template']})
save('selection-results.json',{'basis':5125,'implementation':'engine/rust/question_selection.rs select, positively weighted easy band uniform(8), sorted unique candidate IDs; fresh synthetic candidate identities only','distribution':[1,0,0],'candidate_count':len(pool),'draws':selected,'selected_templates':dict(collections.Counter(v['template'] for v in selected)),'history_exclusion_test':{'excluded_fixture_entities':[900000,900001],'remaining_pool_count':len(pool)-2},'limits':['Live configured weights, learner history, usable-entity schema checks and database entity IDs were not supplied; this reproduction demonstrates reachability and lack of cue-aware filtering for explicitly fresh usable easy candidates. It does not predict a specific live learner sequence.']})
save('final-package-integrity.json',{'unchanged':json.load(open('package-before.json'))=={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}})
print('delivery strategies',[(s['stage'],s['correct'],s['decisive']) for s in stages]);print('relocation and deterministic boundary passed')
