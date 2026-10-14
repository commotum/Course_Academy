"""Reuse frozen polynomial validator with the current application grader."""
import copy, hashlib, importlib.util, json, re, subprocess, uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('original_validator', HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEVELS=('easy','moderate','hard')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint(q):
    inputs=re.findall(r'\$([^$]*)\$',q[':question/problem'])[:2]
    assert len(inputs)==2
    vals=[g.parse_tex(s.rstrip('.')) for s in inputs]
    assert len(vals[0].free_symbols)==len(vals[1].free_symbols)==1
    x=g.sp.Symbol('X')
    return g.digest(sorted(g.sp.srepr(a.subs(next(iter(a.free_symbols)),x)) for a in vals))
def independent(rec):
    assert rec['knowledge_point']['db_id']==g.KP
    assert rec['knowledge_point']['id']==str(g.NAMESPACE)
    assert not rec['generation']['raw_source_omissions']
    v.check(rec)
    assert rec['generation']['mathematical_fingerprint']==fingerprint(rec['question'])
    regen=g.generate(rec['generation']['level'],seed=rec['generation']['seed'],template=rec['generation']['template'],parameters=rec['generation']['parameters'],profile=rec['generation']['profile'])
    def canonical(r):
        r=copy.deepcopy(r)
        for f in r["question"][":question/answer-fields"]:f[":answer-field/choices"].sort(key=lambda a:a[":answer/id"])
        return r
    assert canonical(regen)==canonical(rec)
    for key,item in [('question',rec['question'])]+[('answer-field',f) for f in rec['question'][':question/answer-fields']]+[('answer',a) for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]:uuid.UUID(item[':'+key+'/id'])
def build_engine():
    deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs'
    libs={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
    cmd=['rustc','--edition=2024','-O',str(harness)]
    for name,p in libs.items():cmd+=['--extern',name+'='+str(p)]
    cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-current-engine')]
    subprocess.run(cmd,check=True)
    (HERE/'reference/engine-build.json').write_text(json.dumps({'harness_sha256':sha(harness),'libraries':{str(p):sha(p) for p in libs.values()},'executable_sha256':sha(HERE/'check-current-engine')},indent=2)+'\n')
if __name__=='__main__':
    frozen=json.loads((ROOT/'generate/runs/current/qa/17592186152116-freeze.json').read_text())
    for path,digest in frozen.items():assert sha(ROOT/path)==digest,path
    parent=json.loads((ROOT/'generate/runs/current/qa/17592186152116.json').read_text());assert parent['parent_review']=='passed' and parent['generator_sha256']==sha(HERE.with_suffix('.py'))
    build_engine()
    subprocess.run([str(HERE/'check-current-engine'),str(HERE/'engine-input.json'),str(HERE/'reference/current-engine-replay.json')],check=True)
    records=[g.generate(level,seed=seed,field_type=kind) for level in LEVELS for seed in range(4) for kind in ('blank','radio')]
    for rec in records:independent(rec)
    (HERE/'reference/current-native-input.json').write_text(json.dumps([v.engine_item(r,r['question'][':question/id']) for r in records],indent=2)+'\n')
    subprocess.run([str(HERE/'check-current-engine'),str(HERE/'reference/current-native-input.json'),str(HERE/'reference/current-native-report.json')],check=True)
    (HERE/'inventory-validation.json').write_text(json.dumps({'status':'pass','supported_levels':LEVELS,'hard_authored':True,'hard_scope':'Recover integer contents of signed expanded multiples of the same primitive nonmonic quadratic; retain common polynomial without factorization.','hashes':{str(p.relative_to(ROOT)):sha(p) for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'inventory_validation.py',HERE/'check-current-engine')},'validated_sample_records':len(records),'fidelity':json.loads((HERE/'validation.json').read_text()),'parent_review':str(ROOT/'generate/runs/current/qa/17592186152116.json')},indent=2)+'\n')
    print('Frozen evidence verified; current native grader replay and 24 fresh sample checks passed.')
