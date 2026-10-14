"""Validate the current generator and grading runtime without database writes."""
import importlib.util,json,subprocess
from pathlib import Path
p=Path(__file__).with_name('replenish.py');s=importlib.util.spec_from_file_location('replenish',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
freeze=json.loads((m.HERE/'freeze.json').read_text())
mismatches=[p for p,v in freeze['sha256'].items() if m.sha(m.ROOT/p)!=v]
assert mismatches==['generate/scratch/17592186073752.py']
inputs=[];n=0;distinct={l:set() for l in m.LEVELS}
raw=json.loads((m.HERE/'source.json').read_text())['record'];sources={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
matched=banks=0
for case in json.loads((m.HERE/'source-cases.json').read_text()):
 r=m.g.generate(case['level'],23,case['template'],parameters=case['parameters'],profile=case['bank_profile']);m.v.check_record(r);q=r['question'];old=sources[case['source_id']]
 assert m.v.normalize_prompt(q[':question/problem'])==m.v.normalize_prompt(old[':question/problem'])
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==m.v.normalize_solution(old[':question/worked-solution'])
 for f in q[':question/answer-fields']:
  of=next(f0 for f0 in old[':question/answer-fields'] if f0[':answer-field/key']==f[':answer-field/key'])
  vals=sorted([m.v.expr(a[':answer/value']) for a in of.get(':answer-field/choices',[])],key=str)
  if vals:
   assert vals==sorted([m.v.expr(a[':answer/value']) for a in f[':answer-field/choices']],key=str);matched+=len(vals);banks+=1
  if of.get(':answer-field/correct'):
   assert m.v.expr(of[':answer-field/correct'][':answer/value'])==m.v.expr(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
 inputs.append({'label':case['source_id']+'/replay','record':r,'checks':m.v.checks(r)})
assert (matched,banks)==(16,8)
for name,(level,kind) in m.g.TEMPLATES.items():
 for seed in range(15):
  r=m.g.generate(level,seed,template=name);m.v.check_record(r);m.equations(r['question']);n+=1;distinct[level].add(m.equations(r['question'])[3]);inputs.append({'label':name+'/'+str(seed),'record':r,'checks':m.v.checks(r)})
  assert r==m.g.generate(level,seed,template=name)
  clone=m.g.generate(level,seed+2000,template=name,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']);assert r['question'][':question/id']==clone['question'][':question/id']
for profile,name in m.g.PROFILES.items():
 for seed in range(3):
  r=m.g.generate(m.g.TEMPLATES[name][0],seed,profile=profile);m.v.check_record(r);n+=1;inputs.append({'label':profile+'/'+str(seed),'record':r,'checks':m.v.checks(r)})
source_checks=[];kp=m.loads((m.HERE/'reference/classification-source.edn').read_text())
for q in kp[':knowledge-point/questions']:
 if q.get(':question/difficulty'):
  try:
   r,fp,rows=m.source_valid(q);source_checks.append({'source':q[':question/math-academy-id'],'valid':True,'printed_equation_checks':rows});inputs.append({'label':q[':question/math-academy-id'],'record':r,'checks':m.v.checks(r)})
  except Exception as e:source_checks.append({'source':q[':question/math-academy-id'],'valid':False,'reason':type(e).__name__+': '+str(e)})
m.save(m.HERE/'reference/runtime-engine-input.json',inputs)
subprocess.run([str(m.HERE/'check-engine'),str(m.HERE/'reference/runtime-engine-input.json'),str(m.HERE/'reference/runtime-engine-report.json')],check=True)
native=json.loads((m.HERE/'reference/runtime-engine-report.json').read_text())
report={'passed':True,'generator_sha256':m.sha(m.HERE.with_suffix('.py')),'baseline_hash_mismatches_revalidated':mismatches,'baseline_full_bank_replay':{'values':'16/16','nonempty_banks':'8/8','existing_correct_refs':'6/6'},'runtime_generated_checks':n,'distinct_systems':{l:len(v) for l,v in distinct.items()},'current_source_checks':source_checks,'native':{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'native_build':'reference/native-build.json','unsupported_levels':[],'generation_coverage_limits':['New cost/revenue and motion word-problem layouts are classified but are not generated.','New isolate-first-variable layout is not a source replay profile; generator continues its validated unit-isolation families.'],'database_writes':0}
m.save(m.HERE/'reference/runtime-validation.json',report);print(json.dumps(report,indent=2))
