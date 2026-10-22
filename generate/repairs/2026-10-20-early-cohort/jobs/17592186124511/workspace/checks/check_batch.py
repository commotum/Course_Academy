"""Guard reachability in the public count-five path and stable owned identities."""
import importlib.util,json,os,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('content_checks',ROOT/'checks/check_content.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
source=json.loads((ROOT.parent/'source/source.json').read_text())
assert source['material']['kp']==g.S['record'] and source['basis']==g.S['basis']
seen=set();batches=[]
for seed in range(30):
 records=g.batch('moderate',5,seed);assert len(records)==5
 for r in records:v.inspect(r);seen.add(r['generation']['template'])
 batches.append({'seed':seed,'templates':[r['generation']['template'] for r in records]})
 if seen==set(g.TEMPLATES):break
assert seen==set(g.TEMPLATES),(seen,set(g.TEMPLATES)-seen)
for t in g.TEMPLATES:
 r=g.generate(template=t,seed=3);p=r['generation']['parameters'];a=g.generate(template=t,seed=4,parameters=p);b=g.generate(template=t,seed=5,parameters=p)
 assert a['question'][':question/id']==b['question'][':question/id']
 assert {f[':answer-field/id'] for f in a['question'][':question/answer-fields']}=={f[':answer-field/id'] for f in b['question'][':question/answer-fields']}
cmd=[sys.executable,str(ROOT/'17592186124511.py'),'--difficulty','moderate','--count','5','--seed','2026','--format','json']
r=subprocess.run(cmd,capture_output=True,text=True,check=True,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(ROOT/'evidence/assets')});records=json.loads(r.stdout)
for rec in records:v.inspect(rec)
v.save('samples.json',records)
v.save('batch-check.json',{'passed':True,'source_snapshot_matches_supplied_source':True,'profiles_reached':sorted(seen),'batches':batches,'stable_identity_under_option_shuffle':True,'public_sample_command':cmd,'public_sample_count':len(records)})
print(f'Public sampling passed: all {len(g.TEMPLATES)} profiles reached in {len(batches)} five-question batches; canonical owned identities stable.')
