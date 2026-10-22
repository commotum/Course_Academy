import sys
sys.dont_write_bytecode=True
import json, pathlib, importlib.util, re, hashlib, subprocess, shutil, collections, platform
E=pathlib.Path(__file__).resolve().parent
J=E.parent
W=J/'workspace'
PY='/home/jake/Developer/Course_Academy/.venv/bin/python'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2)+'\n')
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
def loadmod(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
save('package-before.json',hashes())
g=loadmod(W/'17592186119847.py','candidate')
def facts(r):
 q=r['question'];t=q[':question/problem'];name,m,n,c=re.search(r'\$([A-Z])\$.*?\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$.*?\$(\d+)\$',t).groups();m,n,c=map(int,(m,n,c));non='**non-pivot**' in t;rank=n-c if non else c
 f=q[':question/answer-fields'][0];v=[int(a[':answer/value']) for a in f[':answer-field/choices']];cid=f[':answer-field/correct'][1];pos=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
 assert 0<=rank<=min(m,n) and len(v)==len(set(v))==5 and min(v)>=0 and v[pos]==rank
 sol=q[':question/worked-solution'];assert f'\\text{{rank}}({name})={rank}.' in sol
 if non: assert f'{n}-{c}={rank}.' in sol
 return dict(rank=rank,position=pos,order=sorted(v).index(rank),rows=m,columns=n,count=c,non=non,values=v)
source=json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions']
replay=[];replay_tests=[]
for q in source:
 t=q[':question/problem'];name,m,n,c=re.search(r'\$([A-Z])\$.*?\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$.*?\$(\d+)\$',t).groups();level=q[':question/difficulty'][':db/ident'].split('/')[-1];p=dict(name=name,rows=int(m),columns=int(n),count=int(c),kind='non-pivot' if '**non-pivot**' in t else 'pivot')
 r=g.generate(level,seed=921773,parameters=p,bank_profile=q[':question/math-academy-id']);f=facts(r);got=r['question'];sf=q[':question/answer-fields'][0]
 assert got[':question/problem']==t.replace(r'\cdot',r'\times')
 assert sorted(f['values'])==sorted(int(a[':answer/value']) for a in sf[':answer-field/choices'])
 if ':question/worked-solution' in q:assert got[':question/worked-solution']==q[':question/worked-solution']
 if ':answer-field/correct' in sf:assert str(f['rank'])==sf[':answer-field/correct'][':answer/value']
 replay.append(r);replay_tests.append({'source':q[':question/id'],'complete_bank_matches':True,'prompt_matches_after_documented_normalization':True,'solution_matches':True if ':question/worked-solution' in q else 'absent; reconstructed','rank':f['rank']})
save('source-replay-records.json',replay);save('source-replay-tests.json',replay_tests)
samples=[]
for level,profiles in g.PROFILES.items():
 for profile in profiles:
  for seed in (194029,284767,981011,918717,723419,554137):samples.append(g.generate(level,seed,bank_profile=profile))
for r in samples:facts(r)
save('independent-records.json',samples)
for level in ('easy','moderate'):save(level+'-records.json',[r for r in samples if r['generation']['template'].startswith(level)])
batch=json.load(open(J/'samples.json'));save('runner-batch.json',batch)
for r in batch:facts(r)
controls=[];pairs=[]
for level,profile,p in [('easy','q-79405',dict(name='Q',rows=10,columns=12,count=5,kind='pivot')),('moderate','q-139953',dict(name='Q',rows=10,columns=8,count=3,kind='non-pivot'))]:
 variants=[p,{**p,'count':p['count']-1},{**p,'name':'T','rows':11}]
 if level=='moderate':variants.append({**p,'columns':9})
 rs=[g.generate(level,88347,parameters=x,bank_profile=profile) for x in variants];fs=[facts(r) for r in rs]
 assert fs[0]['rank']!=fs[1]['rank'] and fs[0]['rank']==fs[2]['rank']
 if level=='moderate':assert fs[0]['rank']!=fs[3]['rank']
 pairs.append(dict(level=level,record_indices=list(range(len(controls),len(controls)+len(rs))),facts=fs));controls+=rs
save('control-records.json',controls);save('control-tests.json',pairs)
for level in ('easy','moderate'):save('controls-'+level+'.json',[r for r in controls if r['generation']['template'].startswith(level)])
# Changed-rule regression independently asserts success on formerly missing cases.
restrictions=[];regression_records=[]
for m,n,c in [(3,4,2),(4,7,3),(3,3,2),(3,6,3),(4,8,4),(5,10,5),(6,12,6),(7,14,7)]:
 for profile in g.PROFILES['moderate']:
  p=dict(name='A',rows=m,columns=n,count=c,kind='non-pivot')
  r=g.generate('moderate',28907,parameters=p,bank_profile=profile);f=facts(r);assert f['rank']==n-c
  restrictions.append(dict(parameters=p,profile=profile,facts=f));regression_records.append(r)
for profile in g.PROFILES['easy']:
 for m,n,c in [(3,3,1),(3,3,3),(12,15,12)]:
  p=dict(name='A',rows=m,columns=n,count=c,kind='pivot')
  r=g.generate('easy',28907,parameters=p,bank_profile=profile);facts(r);regression_records.append(r)
feasible={(n,c) for n in range(3,16) for c in range(1,13) if 1<=n-c<=12}
missing=sorted(feasible-set(g.catalog('moderate')));assert not missing
save('restriction-records.json',regression_records)
save('restriction.json',dict(seed=28907,formerly_rejected_cases=restrictions,missing_semantic_tasks=missing,all_passed=True))
# Real CLI, capacities, replay, relocation and historical failing checks.
manifest=json.load(open(W/'package.json'));R=E/'relocated';R.mkdir(exist_ok=True);shutil.copyfile(W/'package.json',R/'package.json')
for name in manifest['files']:
 dest=R/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,dest)
cli=[]
for level,counts in [('easy',[0,5,12,13,-1]),('moderate',[0,5,98,99,-1])]:
 for count in counts:
  cmd=[PY,'-B',str(R/manifest['entrypoint']),'--difficulty',level,'--count',str(count),'--seed','428163','--format','json'];x=subprocess.run(cmd,cwd=E,capture_output=True,text=True);a=json.loads(x.stdout)['records'] if x.returncode==0 else [];cli.append(dict(command=cmd,returncode=x.returncode,returned=len(a),stderr=x.stderr));assert len(a)==count if x.returncode==0 else count<0 or count>(12 if level=='easy' else 98)
  if a:save('cli-'+level+'-'+str(count)+'.json',a)
cmd=[PY,'-B',str(R/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','428163','--format','json'];x=subprocess.run(cmd,capture_output=True,text=True);y=subprocess.run([*cmd[:2],str(W/manifest['entrypoint']),*cmd[3:]],capture_output=True,text=True);assert x.stdout==y.stdout
save('packaging.json',dict(cli=cli,deterministic_relocated_content_equal=True,actual_dependencies={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},manifest=manifest,preflight='present; retained expected-success test rerun'))
# Retained checks are copied and redirected here, never executed in the package.
C=E/'retained-checks';C.mkdir(exist_ok=True)
for name in ['check_repair.py','check_cli_contract.py','check_restriction.py']:shutil.copyfile(W/name,C/name)
sys.path.insert(0,str(C))
pth=C/'check_repair.py';pth.write_text(pth.read_text().replace('HERE=Path(__file__).resolve().parent','HERE=Path('+repr(str(W))+')').replace("E=HERE/'evidence'",'E=Path('+repr(str(E/'retained-results'))+')'))
cr=loadmod(C/'check_repair.py','retained');cr.HERE=W;cr.E=E/'retained-results';cr.E.mkdir(exist_ok=True)
cc=sys.modules['check_cli_contract'];cc.ROOT=R;(R/'evidence').mkdir(exist_ok=True)
# Its source path HERE.parent/source resolves correctly to captured source.
import tempfile
tempfile.tempdir=str(E)
cr.main()
crr=loadmod(C/'check_restriction.py','retained_restriction');crr.main()
# Demonstrate old output envelope and silent truncation faults fail its predicate.
legacy=loadmod(W/'evidence/legacy-generator.py','legacy')
old=legacy.batch('easy',13,0)
save('historical-regressions.json',{'legacy_requested':13,'legacy_returned':len(old),'legacy_test_would_fail':len(old)!=13,'old_instances_envelope_decode':cc.decode(json.dumps({'instances':[1,2,3,4,5]})),'current_cli':cli,'preflight':json.load(open(J/'repair-preflight.json'))})
save('math-tests.json',{'records_checked':len(samples)+len(replay)+len(controls)+len(batch)+len(regression_records),'oracle':'Parse visible dimensions/count/kind, integer subtraction; assert feasibility, unique options, correct key and solution equation. No generator parameters used as math oracle.','all_passed':True})
(E/'session-state.md').write_text('Source replay, independent math, CLI/relocation and retained regressions completed. Changed-rule restriction cases all accepted; canonical rank four and equal count/rank rank two tested across all profiles. Next delivery/native grading/rendering and inventory. Package baseline package-before.json.\n')
print(json.dumps({'source_replays':len(replay),'fresh_samples':len(samples),'controls':len(controls),'missing_moderate_tasks':missing,'cli_cases':len(cli)}))
