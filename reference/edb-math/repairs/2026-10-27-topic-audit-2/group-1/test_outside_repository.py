"""Run actual published/corrected entrypoints outside repository ancestry."""
import concurrent.futures,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4]
publications=json.loads((H.parent/'commit-group-1/generator-publications.json').read_text())
fix=json.loads((H/'policy-portability-stage.json').read_text())
bands={17592186059748:['easy','moderate'],17592186059750:['easy','moderate','hard'],
17592186064167:['easy','moderate','hard'],17592186064168:['easy','moderate','hard'],17592186064169:['easy','moderate'],
17592186096617:['easy'],17592186096618:['easy'],17592186096619:['easy','moderate'],
17592186176047:['easy','moderate','hard'],17592186176048:['easy','moderate','hard'],17592186184155:['easy','moderate','hard'],
17592186229181:['easy','moderate','hard'],17592186229182:['easy','moderate','hard'],17592186172038:['easy','moderate','hard']}
root=Path(tempfile.mkdtemp(prefix='ca-outside-repository-'));cwd=root/'cwd';cwd.mkdir()
env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('_CA_SOURCE_POLICY_CHILD',None);env['PYTHONDONTWRITEBYTECODE']='1'
staged={};scan=[]
for pub in publications:
    kp=pub['kp'];path=Path('/media/jake/SSD/EDB/math')/pub['new_reference'];manifest=json.loads((path.parent/'generator-package.json').read_text())
    hits=[]
    for name in manifest['files']:
        if name.endswith('.py'):
            text=(path.parent/name).read_text()
            if 'scripts.generator_policy'in text or'scripts/generator_policy.py'in text:hits.append(name)
    scan.append({'kp':kp,'published_reference':pub['new_reference'],'repository_policy_lookup_files':hits,'supported_difficulties':bands[kp]})
    source=Path(fix['directory'])if kp==fix['kp']else path.parent
    files=fix['files']if kp==fix['kp']else list(manifest['files']);dest=root/'runtime'/str(kp)
    for name in files:
        target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/name,target)
    entry=dest/path.name
    assert not any((p/'scripts/generator_policy.py').exists()for p in entry.parents)
    staged[kp]=entry
(H/'published-sibling-policy-scan.json').write_text(json.dumps(scan,indent=2)+'\n')
(H/'supported-difficulties.json').write_text(json.dumps([{'kp':p['kp'],'reference':p['new_reference'],'supported':bands[p['kp']],'unsupported':[b for b in['easy','moderate','hard']if b not in bands[p['kp']]]}for p in publications],indent=2)+'\n')
def run(task):
    kp,band=task;entry=staged[kp];output=root/'output'/str(kp)/band;output.mkdir(parents=True,exist_ok=True)
    local_env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output)}
    cmd=[str(R/'.venv/bin/python'),str(entry),'--difficulty',band,'--count','4'if kp==fix['kp']else'1','--seed','27102026','--format','json']
    result=subprocess.run(cmd,cwd=cwd,env=local_env,text=True,capture_output=True,timeout=100)
    records=json.loads(result.stdout)if result.returncode==0 else[]
    records=records.get('records',records.get('instances',[]))if isinstance(records,dict)else records
    return {'kp':kp,'difficulty':band,'command':cmd,'cwd':str(cwd),'script':str(entry),'returncode':result.returncode,'stderr':result.stderr,'record_count':len(records)},records
results=[];records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
    for report,batch in pool.map(run,[(kp,b)for kp in staged for b in bands[kp]]):
        results.append(report);records.extend(batch);print(report['kp'],report['difficulty'],report['returncode'],report['record_count'],report['stderr'][-180:],flush=True)
# Verify actual API wrappers, including an explicit all-false case that cannot resample.
probe=r'''
import importlib.util,json,sys
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location('cosine_standalone',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import generator_policy as policy
checks={'local_policy_file':policy.__file__,'public_nonempty_wrapper':bool(getattr(m.generate,'_nonempty_checkbox_policy',False)),'public_source_wrapper':bool(getattr(m.generate,'_source_guarded',False))}
assert Path(policy.__file__).parent==p.parent
for seed in range(128):
 raw=m._generate_legacy('hard',seed)
 if not any(raw['generation']['truth_vector']):break
else:raise AssertionError('No explicit all-false test case found')
try:m.generate('hard',seed,parameters=raw['generation']['parameters'])
except policy.EmptyCheckboxSelection:checks['explicit_empty_selection_rejected']=True
else:raise AssertionError('Nonempty guard lost')
try:m.generate('moderate',template='q-167631')
except Exception as exc:
 assert type(exc).__name__=='ExcludedSource',repr(exc);checks['excluded_source_rejected']=True
else:raise AssertionError('Excluded child source accepted')
print(json.dumps(checks))
'''
guard=subprocess.run([str(R/'.venv/bin/python'),'-c',probe,str(staged[fix['kp']])],cwd=cwd,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(root/'guard-assets')},text=True,capture_output=True,timeout=30)
assert guard.returncode==0,guard.stderr
cosine=[r for r in records if isinstance(r['knowledge_point'],dict)and r['knowledge_point'].get('db_id')==fix['kp']]
baseline=json.loads((H/'staged-cosine-portable.json').read_text());identities=sorted(r['question'][':question/id']for r in cosine)==sorted(r['question'][':question/id']for r in baseline)
assert identities
report={'passed':all(r['returncode']==0 and r['record_count']>0 for r in results),'outside_repository_root':str(root),
    'normal_environment':{'cwd':str(cwd),'PYTHONPATH':'unset','_CA_SOURCE_POLICY_CHILD':'unset in parent CLI; source guard creates its own normal child'},
    'published_packages_scanned':len(scan),'same_repository_lookup_elsewhere':[s for s in scan if s['kp']!=fix['kp']and s['repository_policy_lookup_files']],
    'entrypoint_checks':results,'guard_checks':json.loads(guard.stdout),'same_cosine_question_UUIDs_as_pre_fix_repo_working_outputs':identities,'database_writes':0}
(H/'outside-repository-validation.json').write_text(json.dumps(report,indent=2)+'\n');(H/'outside-repository-samples.json').write_text(json.dumps(records,indent=2)+'\n');print('outside validation',report['passed'],'records',len(records),'checks',len(results))
