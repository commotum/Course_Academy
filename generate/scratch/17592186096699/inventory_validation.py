"""Inventory checks using the frozen readback validator and current learner grader."""
import hashlib,importlib.util,json,subprocess,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('original_validator',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEVELS=('easy','moderate','hard')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint(q):
    der,t,value,_=v.ode(q)
    return g.fingerprint([g.s.srepr(g.s.simplify(der)),str(t),str(value)])
def independent(rec):
    assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP[':knowledge-point/id']
    assert rec['generation']['eligible_for_learning'] and rec['generation']['profile']=='authored_operations'
    v.readback(rec)
    assert rec['generation']['math_fingerprint']==fingerprint(rec['question'])
    regen=g.generate(rec['question'][':question/difficulty'].split('/')[-1],seed=rec['generation']['seed'],field_type=rec['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1],parameters=rec['generation']['parameters'])
    assert regen==rec
    for key,item in [('question',rec['question'])]+[('answer-field',f) for f in rec['question'][':question/answer-fields']]+[('answer',a) for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]:uuid.UUID(item[':'+key+'/id'])
def build_engine():
    deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs'
    libs={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)for name in ('course_academy_engine','serde_json')}
    cmd=['rustc','--edition=2024','-O',str(harness)]
    for name,p in libs.items():cmd+=['--extern',name+'='+str(p)]
    cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-current-engine')]
    subprocess.run(cmd,check=True)
    (HERE/'reference/engine-build.json').write_text(json.dumps({'harness_sha256':sha(harness),'libraries':{str(p):sha(p)for p in libs.values()},'executable_sha256':sha(HERE/'check-current-engine')},indent=2))
if __name__=='__main__':
    assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
    build_engine()
    subprocess.run([str(HERE/'check-current-engine'),str(HERE/'engine-input.json'),str(HERE/'reference/current-engine-replay.json')],check=True)
    # Distinct sampled workloads, both response forms, deterministic full replay.
    records=[g.generate(level,seed=seed,field_type=kind) for level in LEVELS for seed in range(4) for kind in ('blank','radio')]
    for r in records:independent(r)
    native=[v.engine_case(r,r['question'][':question/id'])for r in records]
    (HERE/'reference/current-native-input.json').write_text(json.dumps(native,indent=2))
    subprocess.run([str(HERE/'check-current-engine'),str(HERE/'reference/current-native-input.json'),str(HERE/'reference/current-native-report.json')],check=True)
    (HERE/'inventory-validation.json').write_text(json.dumps({'status':'pass','supported_levels':LEVELS,'hard_authored':True,'hard_scope':'Three bounded elementary primitives; one integration and one initial-condition constant, no new differential equation method.','hashes':{str(p.relative_to(ROOT)):sha(p)for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'inventory_validation.py',HERE/'check-current-engine')},'validated_sample_records':len(records),'fidelity':json.loads((HERE/'validation.json').read_text())['fidelity']},indent=2))
