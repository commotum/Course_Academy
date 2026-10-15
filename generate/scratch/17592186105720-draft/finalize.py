"""Review assembly, final inexpensive API checks, baseline preservation and freeze."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('frozen_final_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=[]
for level in g.SUPPORTED_LEVELS:
 ts=['easy_integer']if level=='easy'else[t for t,v in g.TEMPLATES.items()if v['level']==level]
 for t in ts:
  for pp in [g.domain(t)[0],g.domain(t)[-1]]:
   for profile in ['normal']+([]if t=='easy_integer'else['source']):review.append(g.generate(level,23,t,parameters=pp,profile=profile))
# Original and two changed/endpoint variants for every profile are reviewable.
allrows=[]
for t,v in g.TEMPLATES.items():
 raw=g.generate(v['level'],template=t,parameters=v['parameters'],profile='source');normal=g.generate(v['level'],template=t,parameters=v['parameters'],profile='normal');raw['generation']['review_role']='original MA evidence';normal['generation']['review_role']='normal original-parameter presentation / documented repair';allrows.extend([raw,normal])
for r in review:
 r['generation']['review_role']='generated variant; '+('authored missing-level easy'if r['generation']['template']=='easy_integer'else 'source-family '+r['generation']['bank_profile']);allrows.append(r)
(D/'review.json').write_text(json.dumps(allrows,indent=2))
parts=['# Original MA evidence and generated variants\n\nRaw evidence is ineligible; every normal question has one fixed complete worked solution. Source IDs, parameters and profiles are review metadata, not learner content.']
for r in allrows:
 m=r['generation'];parts.append('## '+m['review_role']+' — '+m['template']+' / '+m['bank_profile']+' / '+json.dumps(m['parameters'])+'\n\n'+g.markdown(r))
(D/'review.md').write_text('\n\n'.join(parts)+'\n')
coverage={}
for level in g.SUPPORTED_LEVELS:
 observed={g.generate(level,i)['generation']['template']for i in range(120)};expected={'easy_integer'}if level=='easy'else{t for t,v in g.TEMPLATES.items()if v['level']==level};assert observed==expected;coverage[level]=sorted(observed)
 for seed in [0,1,79]:
  rows=g.batch(level,6,seed);assert len({r['generation']['parameter_fingerprint']for r in rows})==6
for f in [g.generate_easy,g.generate_moderate,g.generate_hard]:assert f(0)['knowledge_point']['db_id']==g.KP_ID
for bad in [dict(level='easy',seed=True),dict(level=True),dict(level='easy',template=True),dict(level='easy',template='easy_integer',parameters={'n':2.0}),dict(level='hard',template='q-103375',parameters={'n':2}),dict(level='hard',template='q-49067',parameters={'n':16})]:
 try:g.generate(**bad)
 except(ValueError,TypeError):pass
 else:raise AssertionError('invalid API input admitted '+str(bad))
for level,count in [('easy',47),('moderate',231),('hard',31)]:
 try:g.batch(level,count)
 except ValueError:pass
 else:raise AssertionError('finite capacity overflow was not rejected')
base=D.with_name('17592186105720');before=json.loads((D/'registered-baseline.json').read_text());actual={str(z.relative_to(Path.cwd()))for z in [base.with_suffix('.py'),*[z for z in base.rglob('*')if z.is_file()]]};assert actual==set(before);assert all(h(Path(path))==sha for path,sha in before.items())
limitations=json.loads((D/'engine-limitations.json').read_text());validation=json.loads((D/'validation.json').read_text());validation.update({'default_family_coverage':coverage,'api_postchecks':'strict types, individual entrypoints, finite exhaustion, deduplicated seeded batches passed','native_math_diagnostic':{'cases':limitations['mathematical_cases'],'initial_mismatch_totals':limitations['initial_mismatch_totals'],'report':'native-math-report.json','limitations':'engine-limitations.json'},'registered_baseline_files_unchanged':len(before),'status':'bounded mathematical and fidelity checks passed; radio grading supported; freeform arbitrary-constant limitations remain documented'})
(D/'validation.json').write_text(json.dumps(validation,indent=2))
paths=[D.with_suffix('.py'),D/'templates.json',D/'source.json',D/'topic.json',D/'lesson.json',D/'math_format.py',D/'parser.py',D/'check-engine',D/'validate.py',D/'audit-native-math.py',D/'finalize.py']
freeze={'version':g.VERSION,'python':sys.version.split()[0],'sympy':g.sp.__version__,'files':{str(p.relative_to(Path.cwd())):h(p)for p in paths},'registered_baseline_preserved_files':len(before),'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage']};(D/'freeze.json').write_text(json.dumps(freeze,indent=2));print(json.dumps(freeze,indent=2))
