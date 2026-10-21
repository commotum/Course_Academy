"""Verify relocated package and probe saved visible output before/after delivery."""
import ast,collections,hashlib,json,os,pathlib,re,shutil,subprocess,sys
P=pathlib.Path(__file__).resolve().parents[1];E=P/'evidence'
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def info(r):
 f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];ns=[int(re.search(r'-?\d+',a[':answer/value'])[0]) for a in cs];i=next(i for i,a in enumerate(cs) if a[':answer/id']==f[':answer-field/correct'][1]);return ns,i

def probes(records):
 out={}
 for template in sorted({r['generation']['template'] for r in records}):
  rs=[r for r in records if r['generation']['template']==template];counts=collections.Counter()
  for r in rs:
   ns,i=info(r);ordered=sorted(ns);correct=ns[i];avg=sum(ns)/5;mid=(min(ns)+max(ns))/2
   for rank in range(1,6):counts[f'rank_{rank}']+=correct==ordered[rank-1]
   for pos in range(1,6):counts[f'position_{pos}']+=i==pos-1
   for name,target in [('nearest_mean',avg),('nearest_midrange',mid)]:
    predicted=min(range(5),key=lambda j:(abs(ns[j]-target),j));counts[name]+=predicted==i
   for parity in [0,1]:
    choices=[j for j,n in enumerate(ns) if n%2==parity]
    if len(choices)==1:counts[f'only_{"even" if parity==0 else "odd"}']+=choices[0]==i
  assert max(counts.values())<len(rs),(template,counts)
  out[template]=dict(attempts=len(rs),successes=dict(counts),baseline=0.2,semantic_instances=len({json.dumps(r['generation']['parameters'],sort_keys=True) for r in rs}))
 return out
before=load(E/'fresh-samples.json');after=sum([load(E/f'delivery-{level}/accepted.json') for level in ['easy','moderate','hard']],[])
raw=probes(before);survivors=probes(after);assert raw==survivors
counts=collections.Counter(r['generation']['attempts'] for r in before)
semantic={(r['question'][':question/difficulty'],json.dumps(r['generation']['parameters'],sort_keys=True),('F' if r['generation']['template'] in ['cake','exhaust','outside'] else 'C')) for r in before}
save('pedagogical-variation.json',dict(learner_operation='Separate, integrate, apply the initial condition, then evaluate; moderate additionally calibrates k and inverts for elapsed time.',fixed_reasons='Cooling from above, positive rate, consistent units, integer rounding and one-of-five response follow the source skill and contract. Rank and position have no instructional significance.',before_delivery=raw,after_delivery=survivors,generator_attempts=dict(counts),normal_records=len(before),semantic_instances=len(semantic),counterfactuals='counterfactual-results.json; historical-counterexamples-current.json',selection='Shared prepare_records filters accept 84 easy,60 moderate,12 hard, plus all five regenerated runner items. Rust question_selection.rs:125-199 deduplicates candidates, selects a difficulty band by configured weights, and selects uniformly within that band using a seed hash. It does not inspect answer rank. No live history or policy snapshot was available; weighted end-to-end learner selection is untested.',limitations=['Finite sampled shortcut probes do not prove absence of every possible heuristic.','Explicit observed profiles retain their original complete banks, including ranks; they are never selected by normal generation.','Scalar error offsets have unresolved source misconception intent. Authored banks preserve the computation and response contract.']))
manifest=load(P/'package.json');assert set(manifest)=={'entrypoint','files','dependencies','default_difficulty'}
assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':__import__('sympy').__version__}}
assert 'package.json' not in manifest['files']
rel=E/'relocated';rel.mkdir(exist_ok=True)
hashes={}
for name in manifest['files']:
 path=P/name;assert path.is_file() and not path.is_symlink() and not pathlib.Path(name).is_absolute() and '..' not in pathlib.Path(name).parts
 dest=rel/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest);hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
 if name.endswith('.py'):ast.parse(path.read_text())
cmd=[sys.executable,'-B',str(rel/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','1403253416','--format','json']
env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'relocated-assets'),'PYTHONDONTWRITEBYTECODE':'1'}
a=subprocess.run(cmd,cwd='/tmp',env=env,capture_output=True,text=True,check=True)
b=subprocess.run(cmd,cwd='/tmp',env=env,capture_output=True,text=True,check=True)
assert a.stdout==b.stdout
records=json.loads(a.stdout);assert len(records)==5
save('relocated-records.json',records)
save('packaging.json',dict(passed=True,command=cmd,cwd='/tmp',deterministic=True,dependencies=manifest['dependencies'],runtime_sha256=hashes,runtime_files=len(hashes),source_snapshot_changed='Updated obsolete runtime snapshot from supplied unchanged source evidence; replay compared against authoritative source file, with original canonical/body counterexamples retained. No original counterexample was invalidated by changing source evidence.',assets='No generated assets or runtime output files. Output-dir environment supported vacuously.'))
# Ensure grader and render reports actually passed; count responses, not metadata promises.
gr=load(E/'grader-report.json');assert gr['database_writes']==0 and gr['documented_unresolved_checks']==0
assert gr['accepted_checks']+gr['rejected_checks']==sum(len(c['checks']) for c in load(E/'grader-input.json'))
render=load(E/'render/rendering.json');assert render['passed'] and len(render['cases'])==4
save('final-checks.json',dict(passed=True,package=hashes,shortcut_templates=len(raw),semantic_instances=len(semantic),native_accepted=gr['accepted_checks'],native_rejected=gr['rejected_checks'],rendered=len(render['cases'])))
print(json.dumps(dict(passed=True,shortcut_templates=len(raw),semantic_instances=len(semantic),native_accepted=gr['accepted_checks'],native_rejected=gr['rejected_checks'],rendered=len(render['cases']),files=len(hashes))))
