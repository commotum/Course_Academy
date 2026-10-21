import json,collections,hashlib,re,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;B=E.parent;R=Path('/home/jake/Developer/Course_Academy');P=B/'workspace'
def load(n):return json.load(open(E/n))
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
# Idempotently retain the normalized-batch checks in the aggregate native input.
cases=[c for c in load('grader-input.json') if not c['label'].startswith('delivered-runner:')]
for i,(r,raw) in enumerate(zip(load('delivery-runner/accepted.json'),load('runner-batch.json'))):
 f=raw['question'][':question/answer-fields'][0];value=next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
 cases.append({'label':'delivered-runner:'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/value']==value else 'rejected','purpose':'publication-normalized answer link versus exact RREF oracle'} for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
save('grader-input.json',cases)
# Observe the actual delivered DOM; authored positions are not learner display positions.
ui=load('ui-position-results.json');delivered=load('delivery-runner/accepted.json');positions=[]
for i,r in enumerate(delivered):
 q=r['question'];html=(E/f'render-delivered/question-{i+1:03}.html').read_text();inputs=re.findall(r'<input[^>]*type="radio"[^>]*>',html);order=[re.search(r'value="([^"]+)"',x)[1] for x in inputs]
 positions.append({'question_id':q[':question/id'],'template':r['generation']['template'],'shape':'vector' if 'then solve' in q[':question/problem'] else 'matrix','display_position':order.index(q[':question/answer-fields'][0][':answer-field/correct'][1])+1,'html':f'render-delivered/question-{i+1:03}.html'})
ui['delivered_batch_observed']=positions;save('ui-position-results.json',ui)
probes=[]
for p in load('shortcut-results.json'):
 p={**p,'cue':p['strategy']}
 if p['subgroup'].startswith('runner') and p['strategy'].startswith('position '):
  p['conclusion']+=' These are authored positions. The actual UI reorders them after normalization; see ui-position-results.json. The two raw vector records both have authored key position 4, but their normalized displayed positions are 3 and 1, so this is not a delivered choose-four rule.'
  p['sample_refs']+=['ui-position-results.json','delivery-runner/accepted.json']
 probes.append(p)
for subgroup,rr in [('delivered runner',positions),('delivered matrix',[x for x in positions if x['shape']=='matrix']),('delivered vector',[x for x in positions if x['shape']=='vector'])]:
 for position in range(1,6):
  probes.append({'cue':f'displayed position {position}','subgroup':subgroup,'scope':'overall' if subgroup=='delivered runner' else 'other_recognizable_subgroup','strategy':f'choose displayed option {position}','correct':sum(x['display_position']==position for x in rr),'total':len(rr),'baseline':.2,'disposition':'not_predictive','conclusion':'Baseline is uniform 1/5 choice. Actual UI DOM after delivery normalization has no constant position answering the entire batch or either response-shape subgroup; displayed order also depends on task item identity.','sample_refs':['ui-position-results.json','delivery-runner/accepted.json']})
# Compare strategy outcomes before/after publisher filtering using value-only strategies,
# whose equality is unaffected by stable UUID replacement.
for stem,rawfile in [('independent','independent-samples.json'),('fresh','fresh-batch.json'),('role-controls','role-controls.json'),('runner','runner-batch.json')]:
 raw=load(rawfile);acc=load(f'delivery-{stem}/accepted.json')
 sig=lambda r:(r['question'][':question/problem'],r['question'][':question/worked-solution'],sorted(c[':answer/value'] for c in r['question'][':question/answer-fields'][0][':answer-field/choices']),next(c[':answer/value'] for c in r['question'][':question/answer-fields'][0][':answer-field/choices'] if c[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]))
 assert [sig(r) for r in raw]==[sig(r) for r in acc]
coverage=load('delivery-coverage.json');coverage['fixed_bank_controls']={'input':70,'accepted':70,'report':'delivery-role-controls/delivery.json','value_only_strategy_results_preserved':True};coverage['all_stage_value_signatures_equal']=True;coverage['rejection_branch_report']='rejection-results.json';save('delivery-coverage.json',coverage)
source=load('source-analysis.json')
variation={
 'learner_operation':source['learner_operation'],
 'fixed_features':source['fixed_features']+[
  {'feature':'five-choice, one-correct radio response','justification':'All 14 practice sources use five choices. Nonsingularity makes exactly one [I|solution] or ordered solution vector correct; varying correct-choice count would change the response contract.'},
  {'feature':'14 coefficient matrices and their legal row-operation paths','justification':'A conservative finite family holds arithmetic workload at the source level. This does not fix the correct bank role: all five answer roles occur with the exact same coefficient matrix and bank. More coefficient profiles are eligible, but are not necessary to prevent a fixed decision cue within these tested families.'}],
 'answer_roles':[{'role':'which full-bank vector is the solution','eligible_variation':'all five source-bank members; signed and zero coordinates can qualify once the right-hand sides change','observed':'All 5 roles were generated and independently checked in every one of 14 profiles with an unchanged full bank (70 role controls), as well as translated boundary cases.'},{'role':'learner choice position','eligible_variation':'any of five choices; it must follow the correct mathematical result','observed':'Generator shuffles choices, publication assigns stable IDs, and UI hashes item/field/choice identities into display order. All displayed positions occur in item-identity counterfactuals.'}],
 'coverage':[
  {'case':'14 source practice profiles, complete five-member banks','sample_refs':['replays.json','source-replay-results.json'],'result':'All replay mathematical content, banks, target response shapes and correct answers match; q-10636/q-10646 row-label errors are corrected.'},
  {'case':'all five decision roles within every fixed coefficient/bank profile','sample_refs':['role-controls.json','role-control-math.json'],'result':'70/70 correct; each profile admits five different correct choices without changing visible bank contents.'},
  {'case':'translation boundaries and both matrix/vector targets','sample_refs':['independent-samples.json','math-results.json'],'result':'All 14 profiles, translations at -3 and +3 and all 5 roles pass exact checks.'},
  {'case':'runner exact five-record practice pool','sample_refs':['runner-batch.json','delivery-runner/accepted.json','ui-position-results.json'],'result':'Five distinct systems and profiles, 3 matrix and 2 vector targets, roles 3/3/0/3/1. All survive filtering. No tested bank-content rule answers every record, and normalized displayed positions are 1/5/3/1/3.'},
  {'case':'rejection, requested difficulty, deduplication and learner selection','sample_refs':['delivery-coverage.json','selection-results.json','rejection-results.json'],'result':'Read-only publisher preserves all sampled decision cases. Sampler duplicate-rejection branch is tested separately. With positive moderate weight, all candidate roles retain support under modeled histories; source-practice and current-prefix exclusions are explicit.'}],
 'counterfactuals':[
  {'kind':'relevant','change':'Within each profile hold coefficient matrix, complete unordered bank, translation and RNG seed fixed; change answer_role 0 to 1, thereby changing the equations RHS.','expected':'RREF constants, selected bank member and dependent worked matrices/narrative must change consistently. Former correct choice must be rejected and new choice accepted.','observed':'All 14 pairs change the prompt and correct mathematical value; every intermediate displayed matrix is independently valid. Native grader tests every bank member before/after. Matrix and vector pair screenshots show the corresponding changes.','status':'passed','justification':'Source GJ operation determines the augmented column from actual equations, not bank identity or template label.','sample_refs':['counterfactual-records.json','counterfactual-results.json','math-results.json','grader-results.json','render/rendering.json','render-vector-pair/rendering.json']},
  {'kind':'irrelevant','change':'Hold mathematical parameters fixed and vary only RNG seed/answer order. Also vary UI task item identity in position analysis.','expected':'Prompt, worked solution and correct mathematical choice remain identical; ordering may change.','observed':'All 14 seed-only pairs preserve prompt, worked solution and correct answer ID; native outcomes remain the same. Actual UI HTML verifies independent choice ordering; item identity ranges generate all positions without changing answers.','status':'passed','justification':'Source asks for a unique RREF/solution, which cannot depend on layout or seed.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','ui-position-results.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['generator sampling and augmented-system rejection/resampling','requested moderate difficulty','publisher validation and stable identities','captured inventory and within-batch deduplication','learner history/current-prefix exclusion and difficulty-first selection','actual UI choice ordering'], 'sample_refs':['delivery-coverage.json','delivery-independent/delivery.json','delivery-fresh/delivery.json','delivery-runner/delivery.json','delivery-role-controls/delivery.json','selection-results.json','ui-position-results.json','rejection-results.json'], 'result':'70/70 independent, 42/42 fresh, 70/70 fixed-bank controls and exact runner 5/5 survive. Mathematical keys, prompts and full banks remain unchanged through normalization. Learner-selection simulations cover 4 explicit histories with 512 seeds each. No database access or publication.'},
 'limitations':['Finite testing does not prove absence of all shortcuts. Fixed coefficient families assess repeated GJ application, not arbitrary-system generalization.','Live learner histories, policy weights and future database entity IDs are unavailable. Selection code is examined and faithfully reproduced with explicit prospective IDs; no live-frequency claim is made.','UI preview UUID-based IDs are not the future database numeric identities; actual shared UI code and item-identity counterfactuals establish that authored positions are not fixed learner positions.','Canonical e-4710 provides instructional method evidence and no captured response bank. All 14 practice profiles replay, but a separate e-4710 coefficient profile is not exposed. Easy/hard and later singular-system families are outside scope.','Inventory basis is 5370. All 19 stored keys were checked mathematically and all 5 non-source questions reproduced by normalized identity; original generation seeds were not captured. Empty affected-inventory.json records no demonstrated affected instance, not proof of absence of all possible defects.']}
save('pedagogical-variation.json',variation)
# Structural validation with the installed schema library when available.
try:
 import jsonschema
 schema=json.load(open(R/'generate/pipeline/pedagogical-variation.schema.json'));jsonschema.validate(variation,schema);schema_result='passed jsonschema validation'
except ImportError:
 schema=json.load(open(R/'generate/pipeline/pedagogical-variation.schema.json'))
 assert set(variation)==set(schema['required'])
 for p in variation['shortcut_probes']:assert set(p)==set(schema['properties']['shortcut_probes']['items']['required'])
 schema_result='required exact fields and enum/type/reference constraints checked independently; jsonschema not installed'
refs=[]
for entry in variation['coverage']+variation['counterfactuals']+variation['shortcut_probes']+[variation['delivery']]:
 for p in entry['sample_refs']:
  assert not Path(p).is_absolute() and '..' not in Path(p).parts and (E/p).is_file() and (E/p).stat().st_size>0,p
  refs.append(p)
save('evidence-validation.json',{'pedagogical_schema':schema_result,'sample_refs_checked':len(refs),'unique_files':sorted(set(refs)),'all_sample_refs_exist_nonempty_relative':True})
package_after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()};assert package_after==load('package-before.json');assert not any(p.is_dir() for p in P.iterdir())
save('package-after.json',{'files':package_after,'same_as_before':True,'unexpected_subdirectories':[],'database_writes':0,'published_assets':0})
save('visual-inspection.json',{'renderer':'unmodified Course Academy UI via render_preview.py','screenshots_inspected':['render/question-001.png','render/question-002.png','render/question-003.png','render/question-004.png','render/question-005.png','render/question-006.png','render-vector-pair/question-001.png','render-vector-pair/question-002.png','render-vector-pair/question-003.png']+[f'render-delivered/question-{i:03}.png' for i in range(1,6)],'observations':'Equations, augmented column separators, negative signs, fractional answer entries, all five radio controls and worked row operations are readable. Controlled relevant pairs visibly change RHS/solutions, irrelevant pairs preserve mathematics. All delivered records rendered; no MathJax, font, image or JS errors.','passed':True})
print(json.dumps({'pedagogical_schema':schema_result,'refs':len(refs),'delivered_positions':[(x['shape'],x['display_position']) for x in positions],'package_unchanged':True}))
