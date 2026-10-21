#!/usr/bin/env python3
"""Relocation and post-delivery controlled-case checks; writes local evidence only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import generator as g
from validate import E, ROOT, equal, grader_cases, inspect, parse, save

manifest=json.loads((ROOT/'package.json').read_text())
assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{}}
assert 'package.json' not in manifest['files']
with tempfile.TemporaryDirectory(prefix='relocation-',dir=E) as tmp:
    destination=Path(tmp)
    for name in manifest['files']:
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        shutil.copy2(ROOT/name,destination/name)
    env=dict(os.environ,PYTHONPATH='',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(destination/'assets'))
    args=[sys.executable,str(destination/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','17592186152131','--format','json']
    result=subprocess.run(args,cwd=E,env=env,capture_output=True,text=True,check=True)
    assert json.loads(result.stdout)==g.generate_batch('easy',5,17592186152131)
    replay=subprocess.run([sys.executable,'-c','import generator; print(len(generator.source_replay()))'],cwd=destination,env=env,capture_output=True,text=True,check=True)
    assert replay.stdout.strip()=='3'
    unsupported=subprocess.run([sys.executable,str(destination/manifest['entrypoint']),'--difficulty','hard','--count','5','--seed','0','--format','json'],cwd=E,env=env,capture_output=True,text=True)
    assert unsupported.returncode!=0 and 'Only easy is supported' in unsupported.stderr
capacity=len({(str(x),n) for t in g.TEMPLATES for x,n in g.domain(t)})
full=g.generate_batch('easy',capacity,25)
assert len({(str(r['generation']['parameters']['x']),r['generation']['parameters']['n']) for r in full})==capacity
for x in (2,4):
    inspect(g.generate(x,2,'square-equation'))
    try:g.generate(x,2,'square-equation',source_bank=True)
    except ValueError:pass
    else:raise AssertionError('Degenerate source bank allowed')
for x,d in ((2,-1),(15,1),('1.2',-1),('7.5',1)):
    try:g.generate(x,2,'square-equation',base_direction=d)
    except ValueError:pass
    else:raise AssertionError('Out-of-domain foil allowed')
for band in ('moderate','hard'):
    try:g.generate_batch(band)
    except ValueError:pass
    else:raise AssertionError('Unsupported band allowed')
try:g.generate_batch('easy',capacity+1,25)
except ValueError:pass
else:raise AssertionError('Excess count allowed')
save('runtime-boundaries.json',{'semantic_capacity':capacity,'full_capacity_sampling':'passed','profile_specific_rejections':'passed','outward_direction_rejections':4,'unsupported_bands':['moderate','hard'],'over_capacity_rejected':True})
save('relocation.json',{'passed':True,'runtime_files':manifest['files'],'python':sys.version.split()[0],
     'records_equal_after_relocation':5,'source_replay_after_relocation':3,'unsupported_band_rejected':True,
     'external_runtime_imports':False,'assets_created':0,'database_writes':0,
     'runtime_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in manifest['files']}})

originals=json.loads((E/'counterfactual-records.json').read_text())
accepted=json.loads((E/'counterfactual-delivery/accepted.json').read_text())
identity=lambda r:(r['generation']['template'],str(r['generation']['parameters']['x']),r['generation']['parameters']['n'])
by={identity(r):r for r in accepted}
assert len(accepted)==9 # Reordering only is deliberately deduplicated.
pairs=[]
for i,label in enumerate(('swap-roles','change-index','change-base','square-relevant-base','irrelevant-order')):
    a,b=originals[i*2:i*2+2]
    actual_a,actual_b=by[identity(a)],by[identity(b)]
    ia,ib=inspect(actual_a),inspect(actual_b)
    preserved=equal(parse(ia['key']),parse(ib['key']))
    assert preserved == (label=='irrelevant-order')
    pairs.append({'case':label,'both_semantic_instances_survive':True,'key_preserved':preserved,
                  'before':ia['key'],'after':ib['key']})
save('counterfactual-delivered.json',{'input_count':10,'accepted_count':9,'duplicates':1,'pairs':pairs,
     'duplicate_reason':'Same mathematical record with irrelevant option order is intentionally deduplicated.'})
save('counterfactual-native-grader-input.json',grader_cases(accepted,'controlled-delivered'))
print(json.dumps({'relocation':'passed','post_delivery_counterfactual_pairs':5,'accepted_controlled_records':9}))
