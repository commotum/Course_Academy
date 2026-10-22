"""Write review outcome and validate its evidence references. No package mutations."""
import pathlib,json,hashlib,subprocess,os,sys,shutil
E=pathlib.Path(__file__).resolve().parent;B=E.parent;W=B/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy');P=B/'review-1-policy-2-45a9ed86924bfc07';PY=R/'.venv/bin/python'
load=lambda n:json.loads((E/n).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
# Reproduce the retained original undeclared-import defect with a runnable local copy.
legacy=E/'legacy-original';legacy.mkdir(exist_ok=True);(legacy/'17592186184172').mkdir(exist_ok=True)
for src,dest in [(W/'evidence/original-generator.py',legacy/'17592186184172.py'),(W/'17592186184172/source.json',legacy/'17592186184172/source.json')]:shutil.copyfile(src,dest)
assert (legacy/'17592186184172.py').read_bytes()==(P/'legacy/17592186184172.py').read_bytes()
cmd=[str(PY),str(E/'standalone_discovery.py'),str(legacy/'17592186184172.py')];p=subprocess.run(cmd,capture_output=True,text=True,cwd=E,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':''});assert p.returncode!=0 and 'StopIteration' in p.stderr
save('legacy-import-retest.json',{'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'old_source_sha256':hashlib.sha256((legacy/'17592186184172.py').read_bytes()).hexdigest(),'matches_prior_failing_source':True,'current_closure':'packaging-results.json validates current manifest-only moderate/hard execution without repository import discovery.'})
analysis=load('source-analysis.json')
checks={
 'source_replay':{'status':'passed','evidence_paths':['source-analysis.json','source-replay-results.json','replay-records.json'],'details':'All 15 supported source prompts, complete answer banks and worked solutions replay exactly. Missing canonical bank is explicitly documented.'},
 'math':{'status':'passed','evidence_paths':['math-results.json','delivered-math-results.json','counterfactual-results.json'],'details':'Independent prompt-derived exact math found no mismatch in 131 raw and 107 normalized delivered evaluations, including all five runner records and boundary cases.'},
 'variety':{'status':'passed','evidence_paths':['retained-regression.json','current-profile/profile-omission-results.json','fresh-cli-results.json','shortcut-results.json','delivery-moderate/delivery.json','delivery-hard/delivery.json','batch-assessment.json'],'details':'Retained test fails old code and passes revision. All eight moderate and seven hard profiles survive delivery; every delivered control profile has multiple truth subsets. Exact five-record batch assessed separately.'},
 'scope':{'status':'passed','evidence_paths':['scope-assessment.json','source-analysis.json','rejection-results.json'],'details':'Unchanged constructors preserve the three-statement rank/nullity theorem task and source response banks. Unsupported easy difficulty and invalid boundary parameters are rejected.'},
 'grading':{'status':'passed','evidence_paths':['native-input.json','native-report.json','counterfactual-results.json'],'details':'Native learner grader passed 1320 response checks: 498 accepted, 822 rejected, zero unresolved. Every offered response was checked against independently derived truth; no free-entry fields exist.'},
 'rendering':{'status':'passed','evidence_paths':['render-all/rendering.json','render-all/input.json','visual-inspection.json'],'details':'Actual UI rendered ten cases. Screenshots inspected for every runner record, both relevant/irrelevant pairs and a hard vector profile; mathematics, selections and explanations agree.'},
 'packaging':{'status':'passed','evidence_paths':['packaging-results.json','determinism.json','legacy-import-retest.json','runtime-change.json','package-integrity.json'],'details':'Manifest-only relocation and deterministic replay pass. Installed Python 3.13.5 and SymPy 1.14.0 match exact dependency declarations. Original import failure reproduced; package files remain unchanged.'},
 'decision_variation':{'status':'passed','evidence_paths':['pedagogical-variation.json','counterfactual-results.json','shortcut-results.json','selection-results.json','batch-assessment.json'],'details':'Same-claim count change flips correct response and actual grading; dimension-preserving coordinate change preserves response. Conditional template and position/action probes show alternatives after delivery; exact batch has no tested constant full-response shortcut. Learner-selection analysis is conditional on captured inventory and stated history/weight scenarios.'}
}
result={'verdict':'accepted','summary':'The seeded profile shuffle resolves the retained omission. All eight checks pass; no remaining defect was demonstrated. Package unchanged.','source_analysis':{k:analysis[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs']},'checks':checks,'findings':[]};result['source_analysis']['evidence_paths']=['source-analysis.json','reuse-provenance.json','scope-assessment.json'];save('result.json',result)
# Validate schema with a small standard-library validator for the supplied schema subset.
schema=json.loads((R/'generate/pipeline/pedagogical-variation.schema.json').read_text());variation=load('pedagogical-variation.json')
def validate(x,s,path='$'):
 types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}
 if 'type' in s:assert isinstance(x,types[s['type']]) and not (s['type'] in ['integer','number'] and isinstance(x,bool)),(path,'type')
 if 'enum' in s:assert x in s['enum'],(path,'enum')
 if isinstance(x,dict):
  assert all(k in x for k in s.get('required',[])),(path,'missing')
  if s.get('additionalProperties') is False:assert set(x)<=set(s.get('properties',{})),(path,'extra')
  for k,v in x.items():
   if k in s.get('properties',{}):validate(v,s['properties'][k],path+'.'+k)
 if isinstance(x,list):
  assert len(x)>=s.get('minItems',0),(path,'minItems')
  for i,v in enumerate(x):validate(v,s.get('items',{}),path+f'[{i}]')
 if isinstance(x,str):assert len(x)>=s.get('minLength',0),(path,'minLength')
 if isinstance(x,(int,float)) and not isinstance(x,bool):assert x>=s.get('minimum',float('-inf')) and x<=s.get('maximum',float('inf')),(path,'bounds')
validate(variation,schema)
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['sample_refs','evidence_paths']:refs.extend(v)
   else:walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(variation);walk(result)
for ref in refs:
 p=pathlib.Path(ref);assert not p.is_absolute() and '..' not in p.parts and (E/p).is_file() and (E/p).stat().st_size>0,ref
assert set(checks)==set(['source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'])
assert {'relevant','irrelevant'}<={p['kind'] for p in variation['counterfactuals']}
assert any(p['scope']!='overall' for p in variation['shortcut_probes'])
assert all(c['status']=='passed' and c['evidence_paths'] for c in checks.values())
assert not load('math-results.json')['failures'] and not load('delivered-math-results.json')['failures']
assert load('render-all/rendering.json')['passed'] and len(load('render-all/rendering.json')['cases'])==10
before=load('package-before.json');after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert before==after
save('evidence-contract-validation.json',{'passed':True,'schema':str(R/'generate/pipeline/pedagogical-variation.schema.json'),'schema_sha256':hashlib.sha256((R/'generate/pipeline/pedagogical-variation.schema.json').read_bytes()).hexdigest(),'relative_nonempty_evidence_paths':len(set(refs)),'eight_checks':list(checks),'package_unchanged':True,'result_sha256':hashlib.sha256((E/'result.json').read_bytes()).hexdigest()})
(E/'commands.md').write_text('Run from evidence_root. All command output and artifacts are local.\n\n```sh\nexport PYTHONDONTWRITEBYTECODE=1\nPY=/home/jake/Developer/Course_Academy/.venv/bin/python\nREPO=/home/jake/Developer/Course_Academy\nJOB="$PWD/.."\n"$PY" reproduce_profile_omission.py --assert-coverage\n"$PY" review_tests.py\nfor band in moderate hard; do\n  "$PY" "$REPO/generate/pipeline/check_delivery.py" --input "delivery-input-$band.json" --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty "$band" --output "delivery-$band" --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math\ndone\n"$PY" "$REPO/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty moderate --output delivery-batch --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math\n"$PY" prepare_native.py\n"$REPO/generate/runs/current/check-engine" native-input.json native-report.json\n"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render-all --limit 10 --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math\n"$PY" assess_revision.py\n"$PY" complete_report.py\n```\n\nThe original-import reproduction command and failure are retained in legacy-import-retest.json. The old-versus-current profile regression commands and seeds are in retained-regression.json. Scripts copied from prior review retain provenance in reuse-provenance.json; no author validation oracle was used.\n')
(E/'session-state.md').write_text('Review complete: accepted, all eight checks passed, no findings. result.json and evidence-contract-validation.json saved. Retained old omission and original import failures reproduced; current package closure and revised profile coverage pass. Fifteen source replays;131 raw and107 delivered math evaluations;1320 native responses;10 visually inspected UI cases; captured inventory basis5447 contains only original sources. All package files unchanged. No database writes or assets published.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:c['status'] for k,c in checks.items()},'evidence_paths_verified':len(set(refs)),'package_unchanged':before==after}))
