import sys,json,pathlib,collections,re,hashlib,subprocess
sys.dont_write_bytecode=True
from review_checks import R,J,P,PREV,REPO,PY,g,save,hashes,tex,semantic,family
load=lambda p:json.load(open(R/p))
# Replay the actual generator with passive proposal instrumentation (same RNG and output).
original=g.sample_parameters; proposals=[]
def traced(rng):
 p=original(rng); proposals.append(p.copy());return p
try:
 g.sample_parameters=traced
 actual=g.generate(count=40,seed=731905)
finally:g.sample_parameters=original
assert actual==load('sample-records.json')
seen=set();trace=[]
for i,p in enumerate(proposals):
 t,case,_=g.number(p); accepted=t not in seen;seen.add(t)
 trace.append({'attempt':i+1,'parameters':p,'tex':t,'case':case,'accepted':accepted,'rejection':None if accepted else 'repeated printed number'})
# Bounded failure: deliberately repeat the same valid instance for a count-2 request.
calls=0
def constant(rng):
 global calls
 calls+=1;return {'family':'radical','n':-2}
try:
 g.sample_parameters=constant
 try:g.generate(count=2,seed=731908);raise AssertionError('must reject exhausted support')
 except ValueError as e:failure=str(e)
finally:g.sample_parameters=original
assert calls==1000 and 'exceeds' in failure
save('sampling-trace.json',{'command':str(PY)+' -B finish_review.py','seed':731905,'count':40,'proposals':trace,'before_rejection_counts':dict(collections.Counter(x['case'] for x in trace)),'after_rejection_counts':dict(collections.Counter(x['case'] for x in trace if x['accepted'])),'identical_to_uninstrumented':True,'nonempty_policy_rejected':0,'nonempty_policy_reason':'Every supported membership mask includes C. Full semantic check of sampled outputs confirms at least one true value.','exhaustion_boundary':{'seed':731908,'count':2,'forced_parameters':{'family':'radical','n':-2},'proposal_calls':calls,'expected':'ValueError after max(1000,count*100) attempts','observed':failure,'passed':True}})
# Inspect 100% conditional cues with mathematical grounds, rather than aggregate balance.
a=load('pedagogical-variation.json')
for p in a['shortcut_probes']:
 if p['correct']==p['total'] and p['disposition']=='not_predictive':
  if '/integer' in p['subgroup'] and 'batch' in p['subgroup']:
   p['conclusion']+=' Apparent 100% subgroup is one delivered positive integer (14), whose all-five answer follows directly from being a natural number. Integer representation does not determine the full fresh-source family: both positive and negative integers are present there. One homogeneous batch subgroup is insufficient to infer a family-wide formatting rule.'
  elif 'radical' in p['subgroup']:
   p['conclusion']+=' This small subgroup must be read with controlled positive-square, positive-nonsquare, zero and negative-root cases. Those vary decisions within the same visible root notation; sign/nonreality is intended mathematical evidence.'
a['delivery']['stages_examined'][0]='actual generator proposal trace before/after unique-TeX rejection, bounded exhaustion test, nonempty-checkbox wrapper'
a['delivery']['sample_refs'].append('sampling-trace.json')
a['delivery']['result']+=' Actual generator trace: '+str(len(trace))+' proposals -> 40 records; duplicate rejection cannot remove all five supported masks in this test. Deliberate repeated sqrt(-2) proposal fails at the documented bounded limit.'
save('pedagogical-variation.json',a)
# Exact binding of old failing bytes back to prior independent audit snapshot.
old=hashes(PREV/'relocated-package');old_saved=load('repair-verification.json')['provenance']['failing_package_hashes'];assert old==old_saved
prior_baseline=json.load(open(PREV/'package-before.json'))
old_match=all(old.get(name)==digest for name,digest in prior_baseline.items());assert old_match
r=load('repair-verification.json');r['provenance']['failing_bytes_match_previous_independent_baseline']=old_match;save('repair-verification.json',r)
# Actual screenshot observations, made by reviewer after viewing images.
save('visual-inspection.json',{'renderer':'render/rendering.json','rendered_count':15,'inspected':['render/question-001.png']+['render/question-'+str(i).zfill(3)+'.png' for i in range(6,16)],'observations':'Actual UI checkbox fields, three distinct source radio banks, fractions, square roots, hierarchy image, worked solutions and membership exclusions are readable, with no clipping/overlap seen. sqrt(4)->sqrt(2)->sqrt(-2) changes five->two->one checked memberships. sqrt(-2)->sqrt(-4) preserves C while visible imaginary coefficient changes sqrt(2)->2. -7/3 and 7/3 keep Q,R,C; 6/3 checks all five. Runner sqrt(-83) displays exact sqrt(83)i and C only. Source -18 radio selects Z,Q,R,C rather than all five. No reported math/image/JavaScript errors.'})
# Verify complete evidence contract with the supplied schema, including references.
schema=json.load(open(REPO/'generate/pipeline/pedagogical-variation.schema.json'))
# Use system Python's installed jsonschema only for reviewer artifact validation.
code="import json,jsonschema;jsonschema.validate(json.load(open('pedagogical-variation.json')),json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json')));print('schema passed')"
c=subprocess.run(['python3','-B','-c',code],capture_output=True,text=True,check=True)
refs=[]
def walk(x):
 if isinstance(x,dict):
  if 'sample_refs' in x:refs.extend(x['sample_refs'])
  for y in x.values():walk(y)
 elif isinstance(x,list):
  for y in x:walk(y)
walk(a)
for p in refs:
 path=pathlib.Path(p);assert not path.is_absolute() and '..' not in path.parts and (R/path).is_file() and (R/path).stat().st_size>0,p
now=hashes(P);before=load('package-before.json');assert before==now
save('package-after.json',{'files':now,'unchanged':before==now})
save('evidence-validation.json',{'pedagogical_variation_schema':'passed','method':'jsonschema validates official schema','schema_command':c.args,'sample_ref_count':len(refs),'all_sample_refs_nonempty_and_relative':True,'package_unchanged':True,'prior_failing_package_binding_confirmed':old_match})
commands='''Review commands run from evidence_root. All reviewer scripts/results and package copies stay here. No publication or database access.\n\n```sh\npython3 -B confirm_source.py\n/home/jake/Developer/Course_Academy/.venv/bin/python -B review_checks.py\n/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json\n/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input sample-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --asset-root ../workspace --math-root /media/jake/SSD/EDB/math\n/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math\n/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root ../workspace --math-root /media/jake/SSD/EDB/math --limit 15\n/home/jake/Developer/Course_Academy/.venv/bin/python -B variation_review.py\n/home/jake/Developer/Course_Academy/.venv/bin/python -B finish_review.py\n```\n\nFresh sample seed 731905 (40 records); controlled seed 731907; full negative bounded domain seed 731906; relocation seed 942137. Retained independent source_acceptance.py runs automatically against earlier failing bound bytes and current package. The author's named preflight runs against evidence_root/preflight-package so all its output remains here.\n'''
(R/'commands.md').write_text(commands)
(R/'session-state.md').write_text('All eight review checks complete and passing within documented limits. Retained independent regression fails against previous bound package and passes current. 221 exact math records including 144 negative radicands; native grader 1112 accepts/1108 rejects; actual UI renders 15, screenshots inspected. Fresh sample 40->38 delivery preserves all masks; runner batch5->4 has C=1,N=2,R=1. Conditional cue, count and all positional-subset probes found no incidental bypass. Five controlled pairs verified by actual grader and rendered math. Selection faithfully examined with explicit policy/history conditions. Inventory inspected for retained defects; no affected stored instances. Evidence schema and relative paths pass; package recursively unchanged. Ready for accepted final report.\n')
print(json.dumps({'schema':'passed','package_unchanged':True,'proposal_count':len(trace),'conditional_probes':sum(x['scope']!='overall' for x in a['shortcut_probes']),'evidence_paths_checked':len(refs)}))
