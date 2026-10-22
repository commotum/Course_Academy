import pathlib,json,hashlib,sys,subprocess
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');W=J/'workspace';sys.dont_write_bytecode=True
sys.path.insert(0,str(E/'deps'));import sympy as S

def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
def load(n):return json.loads((E/n).read_text())
x,C=S.symbols('x C');z=(2*x**5+C)/(5*x**2);assert S.simplify(S.diff(z,x)+2*z/x-2*x**2)==0
save('canonical-results.json',{'source_id':'047ea3c1-8ebf-5e26-9f28-c5a87e7cf997','source_stages':['n=-1, z=y^2','z\'+2z/x=2x^2','I=x^2','x^2*z=2*x^5/5+C1','y^2=(2*x^5+C)/(5*x^2)'],'independent_linear_residual':str(S.simplify(S.diff(z,x)+2*z/x-2*x**2)),'response_contract_gap':'Canonical example has no answer field or bank, so no manufactured radio replay is claimed. Ten complete practice cases replay separately.'})
after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};save('package-after.json',after);assert after==load('package-before.json')
save('review-bindings.json',{'policy_version':2,'package_hash':'a5a78975059440751ce7ad7285e2b0a0af31608d88e9db1d5ee3958a27345ce4','batch_hash':'973fa49add1c41540c8b30f1118774cdd875605e673a65ca1e9af14dff54d1c6','source_hash':'b5a1f569b76f9f537b98d0dc874f7abdd6d4b0c1df0740a9e6764f49f1453de4','inventory_hash':'905c1dcb2ef8e5bf0a30bb668aeb2b699a372dfd143f5c52679110ecfc1e7425','engine_hash':'dc1e0a8583ca33c6028bc0a641128ecc8e7896742189dd42b292170c9726bad9','prior_source_analysis_confirmed':True,'package_files_unchanged':len(after),'actual_sha256':{n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in {'source':J/'source/source.json','inventory':J/'source/inventory.json','batch':J/'samples.json','entrypoint':W/'17592186147454.py','selector':R/'engine/rust/question_selection.rs'}.items()},'retained_findings':['1388ffc008aaf44c1904','0d445813c431c607edbe'],'preflight':'Both retained findings inspected; copied author check passes current revision and fails old implementation; independent old/current witnesses and tests retained.'})
save('regression-check-execution.json',{'current':{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python author-check/repair_check.py','exit_code':0,'output':'author-check-execution.log','result':'author-check/evidence/regression-results.json'},'old':{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python old-author-check/repair_check.py','exit_code':1,'output':'old-author-check-execution.log','assertion':'Retained C-2u^(5/2) shortcut persists'},'independent_restriction_witness':'retained-regression-results.json: old rejects q109029 shift=1, current emits it, and ordinary fresh seeds emit it three times.','isolation':'All self-writing author checks executed in copies under evidence_root, never in package_root.'})
sa=load('source-analysis.json');sa['evidence_paths']=['source-analysis.json','source-confirmation.json','canonical-results.json','prior-source-gap-results.json'];save('source-analysis.json',sa)
checks={
'source_replay':{'status':'passed','evidence_paths':['source-analysis.json','source-confirmation.json','source-replays.json','source-replay-results.json','canonical-results.json','prior-source-gap-results.json'],'details':'All ten complete source prompts, 50 choices, keys and worked solutions replay after TeX sizing normalization. Canonical solution independently verified; missing canonical answer bank and incomplete/incorrect q106074 explicitly excluded with evidence.'},
'math':{'status':'passed','evidence_paths':['independent_math.py','review-current.py','resume-math.py','math-records.json','math-results.json','math-execution.log'],'details':'90 records checked using independently parsed displayed ODEs and every choice. Exactly one solution per bank matches the key; new displayed z and final formula verified. Explicit positive-base branch conditions applied. Initial reviewer parser sizing-command failures were corrected and all cases rerun.'},
'variety':{'status':'passed','evidence_paths':['controlled-records.json','ordinary-records.json','retained-regression-results.json','delivery-coverage.json','regression-check-execution.json'],'details':'All ten supported profiles permit five correct-formula assignments in fixed banks, varied p magnitude and forcing sign. Excluded autonomous family restored in normal generation. Retained old failure witnesses reproduced before current checks.'},
'scope':{'status':'passed','evidence_paths':['source-analysis.json','scope-results.json','math-records.json'],'details':'Signed small coefficients preserve elementary Bernoulli reduction, integrating factors, inverse powers, source difficulty and five-choice radio workload. No demonstrated drift.'},
'grading':{'status':'passed','evidence_paths':['grader-input.json','grader-report.json','grader-execution.json','counterfactual-pairs.json'],'details':'Actual native learning::grade_field tested 102 complete banks: 102 accepted choices, 408 rejected choices, no unresolved checks and zero database writes. Radio-only source contract; no free-entry equivalence claim.'},
'rendering':{'status':'passed','evidence_paths':['render/rendering.json','render-inspection.json','render/inspection-1.png','render/inspection-2.png','render/inspection-3.png','render-records.json'],'details':'Actual unmodified UI rendered 12 records; screenshots visually inspected for all five runner items, relevant coefficient pairs and hard fractional-power cases. No reported or observed math/control/layout failure.'},
'packaging':{'status':'passed','evidence_paths':['packaging-results.json','relocation-records.json','package-before.json','package-after.json','review-bindings.json'],'details':'Exact installed dependency strings match manifest; seeded CLI relocation/determinism and malformed parameter rejection passed. Package hashes unchanged; reviewer output confined to evidence_root.'},
'decision_variation':{'status':'passed','evidence_paths':['pedagogical-variation.json','variation-current.py','counterfactual-pairs.json','shortcut-results.json','delivery-coverage.json','selection-results.json','delivery-batch/accepted.json','affected-inventory.json','generated-records.json','inventory-results.json'],'details':'Every visible formula can qualify within each controlled profile; relevant and irrelevant counterfactuals follow displayed math and native grading. Old q109154 cue 0/12 current vs 12/12 old. Exact batch: 5 profiles, both forcing signs, 5/5 delivery acceptance, source-bank memory 0/5 and first actual UI position 2/5. Actual delivery filtering and captured-inventory selector rules examined with modeled histories. One historical old-version affected item reproduced separately; no current generator defect demonstrated.'}}
report={'verdict':'accepted','summary':'The revision resolves both retained failures. Independent math, native grading, actual UI, delivery and decision-variation checks pass; package unchanged. One historical old-version inventory item remains recorded as affected.','source_analysis':{k:sa[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':checks,'findings':[]};save('result.json',report)
# Validate the exact required pedagogical shape and every cited relative sample path.
try:
 import jsonschema
 jsonschema.Draft202012Validator(json.loads((R/'generate/pipeline/pedagogical-variation.schema.json').read_text())).validate(load('pedagogical-variation.json'))
 schema='jsonschema Draft202012Validator'
except ImportError:
 ped=load('pedagogical-variation.json');required=['learner_operation','fixed_features','answer_roles','coverage','counterfactuals','shortcut_probes','delivery','limitations'];assert sorted(ped)==sorted(required)
 for v in ped['fixed_features']:assert set(v)=={'feature','justification'}
 for v in ped['answer_roles']:assert set(v)=={'role','eligible_variation','observed'}
 for v in ped['counterfactuals']:assert set(v)=={'kind','change','expected','observed','status','justification','sample_refs'};assert v['kind'] in ['relevant','irrelevant'];assert v['status'] in ['passed','failed','not_applicable']
 for v in ped['shortcut_probes']:
  assert set(v)=={'cue','subgroup','scope','strategy','correct','total','baseline','disposition','conclusion','sample_refs'}
  assert type(v['correct'])==type(v['total'])==int and 0<=v['correct']<=v['total'] and 0<=v['baseline']<=1
  assert v['scope'] in ['overall','within_template','other_recognizable_subgroup'] and v['disposition'] in ['not_predictive','intended_skill','defect']
 assert set(ped['delivery'])=={'stages_examined','sample_refs','result'}
 schema='Explicit exact-field/type/enum assertions matching supplied schema; jsonschema unavailable'
paths=[]
def walk(o):
 if isinstance(o,dict):
  for k,v in o.items():
   if k in ['evidence_paths','sample_refs']:paths.extend(v)
   else:walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
walk(report);walk(load('pedagogical-variation.json'))
for p in paths:
 path=pathlib.Path(p);assert not path.is_absolute() and '..' not in path.parts;assert (E/path).is_file() and (E/path).stat().st_size>0,p
assert len(checks)==8 and all(v['status']=='passed' and v['evidence_paths'] for v in checks.values())
assert {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}==after
save('contract-check.json',{'passed':True,'pedagogical_schema':schema,'nonempty_relative_evidence_references_checked':len(paths),'eight_checks':list(checks),'package_files_unchanged':len(after),'findings':0})
(E/'session-state.md').write_text('Review complete: accepted current revision. All eight checks pass; source independently confirmed; 90 math records, 102 native banks, 12 actual UI records, 77 delivered records. Package hashes unchanged. Historical old-version inventory member reproduced and recorded in affected-inventory.json. Final result: result.json; evidence contract: contract-check.json.\n')
print(json.dumps(load('contract-check.json')))
