"""Raw replay ownership and remaining public API contract negatives."""
import copy, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert (D/'source.json').read_bytes()==(D.parents[2]/'generate/runs/current/refresh-2026-10-14/sources/17592186204091.json').read_bytes()
for level in g.SUPPORTED_LEVELS:
    sol=g.generate(level,91)['question'][':question/worked-solution']
    assert '⏟' not in sol and sol.count(r'\underbrace{')==2
rejected=[]
def rejects(name, fn):
    try:fn()
    except (ValueError,TypeError):rejected.append(name)
    else:raise AssertionError(name)
for level in g.SUPPORTED_LEVELS:
    for seed in (True,1.0,[],None):rejects('batch invalid seed '+level+repr(seed),lambda level=level,seed=seed:g.batch(level,0,seed))
    wrapper=getattr(g,'generate_'+level)
    rejects('wrapper invalid profile '+level,lambda wrapper=wrapper:wrapper(profile='foreign-profile'))
for level in ([],1,'foreign-level'):rejects('batch invalid level '+repr(level),lambda level=level:g.batch(level,0))
for mid in (None,1,[],'q-foreign'):rejects('raw unknown ID '+repr(mid),lambda mid=mid:g.replay_source(mid))
cases=json.loads((D/'source-cases.json').read_text())
for c in cases:
    raw=g.replay_source(c['source_id']);assert raw==c['record']
    raw[':question/problem']='corrupted';assert g.replay_source(c['source_id'])==c['record']
    for params in ([],{},dict(c['parameters'],shift=-c['parameters']['shift'])):
        rejects('raw changed parameters '+c['source_id']+repr(params),lambda c=c,params=params:g.replay_source(c['source_id'],params))
(D/'supplemental-validation.json').write_text(json.dumps(dict(status='pass',raw_source_snapshot_byte_exact=True,canonical_seed91_all_levels=True,raw_deep_copy_checks=len(cases),rejected_contract_cases=rejected),indent=2)+'\n')
print(len(rejected),'supplemental contract negatives passed')
