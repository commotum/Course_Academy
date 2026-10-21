from audit import *
from collections import Counter,defaultdict
src=json.loads(Path('source-analysis.json').read_text());ss=json.loads(Path('selection-results.json').read_text());mapping=json.loads(Path('selection-map.json').read_text());accepted=json.loads(Path('delivery-independent/accepted.json').read_text())+json.loads(Path('delivery-runner/accepted.json').read_text());byuuid={r['question'][':question/id']:r for r in accepted}
stage=[];selected=[]
for draw in ss['draws']:
 ct=Counter();sign=Counter();origin=Counter()
 for qid,count in draw['selection_counts'].items():
  meta=mapping[qid];ct[meta['template']]+=count;origin[meta['kind']]+=count
  if meta['a'] is not None:sign['positive' if meta['a']>0 else 'negative']+=count
  if draw['scenario']=='all captured bank previously seen':selected.extend([byuuid[meta['uuid']]]*count)
 stage.append({'scenario':draw['scenario'],'candidate_count':draw['candidate_count'],'template_draw_counts':dict(ct),'generated_coefficient_sign_draws':dict(sign),'origin_draws':dict(origin),'distinct_selected':len(draw['selection_counts'])})
save('selection-coverage.json',stage);save('selected-delivered-records.json',selected)
# Importing the audit module does not execute or alter package code.
# Reuse deterministic surface strategies from decision_audit without its sampling side effects.
ns={};script=Path('decision_audit.py').read_text();snippet=script[script.index('def probe('):script.index('probes=probe(')];exec('from collections import defaultdict\n'+snippet,globals(),ns)
new=ns['probe'](selected,'native selection; captured inventory seen','selected-delivered-records.json');probes=json.loads(Path('shortcut-results.json').read_text())+new;save('shortcut-results.json',probes)
counts=json.loads(Path('coverage.json').read_text())
variation={'learner_operation':src['learner_operation'],'fixed_features':[
 {'feature':'Outer function is square root or reciprocal square root; inner polynomial degree at most two','justification':'Lesson e-182, q-48730 and q-342680 establish this chain-rule depth; sum term only in q-20181.'},
 {'feature':'Finite real slope and simple square radicand for evaluated questions','justification':'Source slopes all evaluate at positive square radicands. Avoiding undefined roots preserves the stated derivative task and arithmetic workload.'},
 {'feature':'One correct expression in a five-option radio or equivalent-expression blank','justification':'Captured field contracts; zero-total radio bank must be rejected to keep five distinct choices.'},
 {'feature':'Derivative-only quadratic template forces c=0','justification':'No defensible instructional reason found. Author cites q-342680 shape, but the central lesson e-182 uses 1-x^2 with a nonzero constant and no linear term. This fixed assignment fails review.'}],
 'answer_roles':[
 {'role':'inner coefficient sign and magnitude','eligible_variation':'Either sign and bounded magnitudes without changing chain-rule method','observed':'Both coefficient signs in every sampled template; details in coverage.json.'},
 {'role':'outer derivative sign and exponent','eligible_variation':'Square root and reciprocal square root follow +1/2 versus -1/2 rules','observed':'Same inner 6x-3 pair changes derivative from -3/(6x-3)^(3/2) to 3/sqrt(6x-3).'},
 {'role':'evaluated slope sign/zero and target point','eligible_variation':'Hold curve fixed and vary valid x0; positive, zero, negative all legitimate','observed':'-x^2+10x at targets 2,5,8 gives 3/4,0,-3/4. Both quadratic blank samplers include negative, zero, positive in fresh samples.'},
 {'role':'which displayed choice is correct','eligible_variation':'Every displayed position and eligible scalar rank; no source answer position is essential','observed':'Rank and displayed-position counts vary. No perfect incidental cue found in tested raw, filtered or selected groups.'},
 {'role':'constant-versus-linear term in quadratic radicand','eligible_variation':'Canonical 1-x^2 and practice x^2-6x both require one polynomial derivative and one chain-rule multiplication','observed':'Generator forbids nonzero quadratic constants outside constant-quadratic slope template; canonical derivative cannot be generated.'}],
 'coverage':[{'case':t,'sample_refs':['samples.json','coverage.json'],'result':json.dumps(v)} for t,v in counts.items()]+[
 {'case':'runner requested moderate batch','sample_refs':['runner-batch.json','delivery-runner/accepted.json'],'result':'All 5 pass shared delivery; 3 radio and 2 reciprocal blank records.'},
 {'case':'canonical quadratic constant derivative','sample_refs':['restriction-results.json'],'result':'FAIL: explicit a=-1,b=0,c=1 rejected before rendering.'}],
 'counterfactuals':[
 {'kind':'relevant','change':'Hold -x^2+10x fixed; change target 2 to 5 to 8','expected':'Slope changes 3/4 to 0 to -3/4; former answers stop grading correct','observed':'Matching prompts, substitutions, rendered answers and native accepted canonical/equivalent entries; six cross-target responses rejected.','status':'passed','justification':'q-342792 and q-342789 require evaluating the derivative at a specified point. Targets 5 and 8 are explicit same-method controls outside normal t bound.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-results.json','render-all/rendering.json','visual-inspection.json']},
 {'kind':'relevant','change':'Hold a=-4, root family and display seed fixed; shift constant 3 to 7','expected':'Inner derivative stays -4; denominator, prompt and solution change together','observed':'2/sqrt((-4x+3)^3) changes to 2/sqrt((-4x+7)^3); actual canonical and scaled equivalents accepted, matching visible solutions.','status':'passed','justification':'Inner constant affects composition value, not inner derivative, exactly the separation taught in e-182.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','visual-inspection.json']},
 {'kind':'relevant','change':'Hold inner 6x-3 fixed; swap root versus reciprocal root','expected':'Reconsider outer power and sign; derivative changes','observed':'-3/(6x-3)^(3/2) versus 3/sqrt(6x-3), correct radio IDs accepted and four wrong choices rejected for each.','status':'passed','justification':'q-48730 versus q-107303 requires different outer power derivatives.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-all/rendering.json']},
 {'kind':'irrelevant','change':'Reverse the same radio choices without altering math, key or explanation','expected':'Correct mathematical value and native accepted choice UUID remain; screen position changes','observed':'Response 3/sqrt(6x-3) unchanged; choices reversed, actual grader accepts same UUID and rejects the other four; renderer passes.','status':'passed','justification':'Choice ordering does not enter the chain rule or source mathematical task.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','visual-inspection.json']},
 {'kind':'relevant','change':'Use canonical e-182 constant-quadratic radicand 1-x^2 in derivative template','expected':'Generate -x/sqrt(1-x^2) with original chain-rule stages','observed':'ValueError: Observed quadratic scope has two nonconstant terms and c=0','status':'failed','justification':'e-182 is the central radical chain-rule lesson example. Its constant assignment is not an extra prerequisite.','sample_refs':['restriction-results.json','source-analysis.json']}],
 'shortcut_probes':[{k:v for k,v in p.items() if k!='stage'} for p in probes],
 'delivery':{'stages_examined':['Whole-bank rejection and deterministic resampling','Requested difficulty: mixed audit rejected as expected; matching moderate subset used','Actual prepare_records validation, normalization, captured inventory and within-batch deduplication','Native usable-response validation with current practice exclusions checked for applicability','Native difficulty-weighted selection under explicit weights/history scenarios'], 'sample_refs':['resampling-results.json','rejection-results.json','samples-moderate.json','delivery-independent/delivery.json','delivery-independent/accepted.json','delivery-runner/delivery.json','delivery-runner/accepted.json','selection-input.json','selection-results.json','selection-coverage.json','selection-provenance.json','selected-delivered-records.json'], 'result':'At basis 3951, independent moderate 60 -> 58 after deduplication; runner 5 -> 5. Seed 72676 resamples a zero-sum collapsed bank once while preserving chosen role 3. Native response validation excludes captured q-48846 (missing key). All 63 unpublished moderate records are selected at least once in 512 fresh-history scenario draws after captured inventory is marked seen. Other scenarios and legacy first-ID behavior are recorded. No shortcut perfect in tested generated subgroups, before or after delivery/selection; canonical restriction persists.'},
 'limitations':['Finite tests cannot establish absence of every shortcut.','Actual policy weights and learner history absent; selection scenarios are explicit conditional checks, not live forecasts.','Unpublished database IDs synthetic; future IDs can alter seeded order. Captured inventory may change after basis 3951.','Installed native rlib lacks current validate_practice_question wrapper; native validate_response_question plus inspection of absent free/multistep/example markers reproduces applicable candidate checks for these records.','Math answer tests use independent prompt parsing and SymPy differentiation; branch-sensitive equivalents checked on exact real-domain points, not a formal proof for every possible parameter.','Grading failure remains: valid equivalent fractional-power reciprocal derivative is unresolved.']}
save('pedagogical-variation.json',variation)
# Verify exact report schema using its supported JSON Schema keyword subset.
schema=json.loads((REPO/'generate/pipeline/pedagogical-variation.schema.json').read_text())
def validate(v,sch,path='$'):
 typ=sch.get('type');types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}
 if typ:assert isinstance(v,types[typ]),(path,typ)
 if 'enum' in sch:assert v in sch['enum'],path
 if isinstance(v,dict):
  assert all(k in v for k in sch.get('required',[])),path
  if sch.get('additionalProperties') is False:assert set(v)<=set(sch.get('properties',{})),path
  for k,a in v.items():
   if k in sch.get('properties',{}):validate(a,sch['properties'][k],path+'.'+k)
 if isinstance(v,list):
  assert len(v)>=sch.get('minItems',0),path
  for i,a in enumerate(v):validate(a,sch.get('items',{}),path+f'[{i}]')
 if isinstance(v,str):assert len(v)>=sch.get('minLength',0),path
 if isinstance(v,(int,float)):
  assert v>=sch.get('minimum',-float('inf')) and v<=sch.get('maximum',float('inf')),path
validate(variation,schema)
def refs(v):
 if isinstance(v,dict):
  for k,a in v.items():
   if k=='sample_refs':
    for f in a:assert not Path(f).is_absolute() and (ROOT/f).is_file() and (ROOT/f).stat().st_size>0,f
   else:refs(a)
 elif isinstance(v,list):
  for a in v:refs(a)
refs(variation)
save('evidence-contract-results.json',{'schema':'generate/pipeline/pedagogical-variation.schema.json','schema_valid':True,'all_sample_refs_nonempty_relative_files':True,'shortcut_probe_count':len(probes),'conditional_probe_count':sum(p['scope']!='overall' for p in probes)})
after={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};before=json.loads(Path('package-hashes-before.json').read_text());save('package-integrity-results.json',{'unchanged':before==after,'files_before':len(before),'files_after':len(after),'changed':[k for k in set(before)|set(after) if before.get(k)!=after.get(k)]});assert before==after
Path('commands.txt').write_text(Path('commands.txt').read_text()+'python3 collect_native.py # collecting harness; original harness independent defect below\n'+json.dumps(json.loads(Path('selection-command.json').read_text()))+'\n./selection\n'+PY+' -B finish_tests.py\n'+PY+' -B make_report.py\n'+str(REPO/'generate/runs/current/check-engine')+' grading-defect-input.json grading-defect-results.json # expected exit 1\n')
Path('session-state.md').write_text('Review complete: revise. 182 prompt-derived math checks pass; 17 practice sources replayed with q-107303 power-rule-stage omission. Canonical e-182 blocked by quadratic c=0 restriction. Actual original native grader reproduces failure on valid power-form equivalent for runner seed 4221317821; collecting native harness totals 44 accepted, 82 rejected, 3 unresolved over 129 submissions. All 19 UI renders pass; 11 screenshots inspected. Shared delivery: 60 moderate -> 58 and runner 5 -> 5. Native selection conditional scenarios and shortcut probes saved. Relocation/determinism/dependencies pass. Package hashes unchanged. pedagogical-variation.json schema and sample_refs validated. Final report: review.json.\n')
print('variation schema verified; probes',len(probes),'package unchanged',before==after)
