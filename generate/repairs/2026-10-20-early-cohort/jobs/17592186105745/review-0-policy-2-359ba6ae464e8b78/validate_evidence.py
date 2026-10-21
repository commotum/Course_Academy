#!/usr/bin/env python3
"""Evidence-contract checks, separate from pedagogical acceptance."""
import json,pathlib,hashlib
import jsonschema
ROOT=pathlib.Path(__file__).resolve().parent
def read(p):return json.load(open(ROOT/p))
pv=read('pedagogical-variation.json')
schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
jsonschema.validate(pv,schema)
refs=[]
def inspect(v):
    if isinstance(v,dict):
        for k,val in v.items():
            if k in ('sample_refs','evidence_paths'):refs.extend(val)
            else:inspect(val)
    elif isinstance(v,list):
        for val in v:inspect(val)
inspect(pv);report=read('review.json');inspect(report)
for p in refs:
    path=ROOT/p
    assert not pathlib.Path(p).is_absolute() and path.resolve().is_relative_to(ROOT)
    assert path.is_file() and path.stat().st_size>0,p
assert set(report['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
assert not read('math-results.json')['failed']
assert read('grader-results.json')['accepted_checks']==129
assert read('grader-results.json')['rejected_checks']==309
assert read('counterfactual-grader-results.json')['accepted_checks']==2
assert read('counterfactual-grader-results.json')['rejected_checks']==2
assert read('render/rendering.json')['passed'] and read('render-irrelevant/rendering.json')['passed']
assert len(read('render/rendering.json')['cases'])==13
assert len(read('render-irrelevant/rendering.json')['cases'])==2
assert read('affected-inventory.json')=={'affected_questions':[]}
before=read('package-hashes-before.json');pkg=ROOT.parent/'workspace'
after={str(p.relative_to(pkg)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(pkg.rglob('*')) if p.is_file()}
assert before==after
ctx=read('review-context.json')
assert ctx['source_hash']=='6e3a1a26dd354115ef16fe43db99bbecfa897540c0a124a8709514ea7bf66afc'
assert ctx['inventory_hash']=='73599e0a85ee5258dc3fcac94c3d5263bc8e816bc6a2c20c5a4924c7960ea9ec'
assert ctx['batch_hash']=='d92d5e0fff0b578d4e547d92f300ad3c550faa292c81b6f7a70c2b268721719a'
out={'schema':'passed','relative_nonempty_evidence_refs':len(refs),'eight_named_checks':True,'saved_result_counts_verified':True,'package_bytes_unchanged':True,'source_inventory_batch_bindings_match':True,'database_writes':0,'pedagogical_verdict':report['verdict']}
(ROOT/'evidence-validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
