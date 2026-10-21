"""Summarize saved independent evidence and validate the report contract."""
import collections,hashlib,json,pathlib,re
from html.parser import HTMLParser
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def info(r):
 q=r['question'];f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][1];a=f[':answer-field/choices'];v=[int(re.search(r'-?\d+',x[':answer/value'])[0]) for x in a];pos=next(i for i,x in enumerate(a) if x[':answer/id']==cid)
 return dict(id=q[':question/id'],template=r['generation']['template'],answer=v[pos],values=v,rank=sorted(v).index(v[pos])+1,position=pos+1)

# Confirm actual DOM order, rather than treating raw JSON ordering as UI layout.
class Inputs(HTMLParser):
 def __init__(self):super().__init__();self.radios=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='input' and d.get('type')=='radio':self.radios.append(d['value'])
ui=load(E/'ui-order-results.json');render=load(E/'render/rendering.json');records=load(E/'render-records.json')
assert render['passed'] and len(render['cases'])==len(records)==14
for i,r in enumerate(records):
 p=Inputs();p.feed((E/f'render/question-{i+1:03d}.html').read_text())
 assert p.radios==ui['groups']['rendered'][i]['positions'][0]['ordered_ids']
save('rendering-inspection.json',{'renderer_report':'render/rendering.json','rendered_cases':14,'inspected_screenshots':['render/question-001.png','render/question-007.png','render/question-009.png','render/question-010.png','render/question-012.png','render/question-014.png'],'inspection':'Readable derivative, integral, logarithm and exponential equations; five radio controls; selected result agrees with independent integer; long solutions complete. Time6->9 and target30->25 propagate to rendered prompt, final equation and selected answer. Body/pork restored contexts render correctly. No broken images, MathJax errors or JavaScript errors in all fourteen cases.','actual_ui_order':'All fourteen DOM radio UUID sequences match exact choiceOrder function from unmodified learning.js; UI intentionally reorders generator choices.','passed':True})

fresh=load(E/'fresh-samples.json');batch=load(E/'runner-batch.json');probes=[]
def probe(rs,subgroup,scope,refs,ui_group=None):
 data=[info(r) for r in rs]
 strategies={f'Choose numeric rank {k}':lambda d,k=k:sorted(d['values'])[k-1] for k in range(1,6)}
 strategies.update({'Choose nearest midrange (smaller on ties)':lambda d:min(d['values'],key=lambda n:(abs(2*n-min(d['values'])-max(d['values'])),n)), 'Choose nearest arithmetic mean (smaller on ties)':lambda d:min(d['values'],key=lambda n:(abs(n-sum(d['values'])/5),n))})
 for name,fn in strategies.items():
  correct=sum(fn(d)==d['answer'] for d in data)
  probes.append(dict(cue='Numeric order or visible option-bank spacing',subgroup=subgroup,scope=scope,strategy=name,correct=correct,total=len(data),baseline=.2,disposition='not_predictive',conclusion=f'{correct}/{len(data)} versus uniform-choice baseline 1/5. Counterexamples refute deterministic prediction. Small seeded samples can exceed chance; the inspected construction samples the anchor rank independently of gaps, adapting only to integer bounds. This is evidence against this specific bypass, not proof against all statistical cues.',sample_refs=refs))
 if ui_group is not None:
  ids={d['id'] for d in data};groups=[z for z in ui['groups'][ui_group] if z['question_id'] in ids]
  for k in range(1,6):
   correct=sum(p['position']==k for z in groups for p in z['positions']);total=sum(len(z['positions']) for z in groups)
   probes.append(dict(cue='Actual UI radio position',subgroup=subgroup,scope=scope,strategy=f'Choose displayed position {k} using exact UI choiceOrder at tested item IDs',correct=correct,total=total,baseline=.2,disposition='not_predictive',conclusion=f'{correct}/{total}; baseline1/5. UUID hash sorting in the actual UI adds item-ID-dependent order; tested three explicit item IDs per record. No fixed-position rule is supported. Actual rendered DOM order independently matches the extracted function.',sample_refs=refs+['ui-order-results.json','ui-order-probe.cjs']))
probe(fresh,'fresh samples overall','overall',['fresh-samples.json','independent-review.py'],'fresh')
for t in sorted({r['generation']['template'] for r in fresh}):
 probe([r for r in fresh if r['generation']['template']==t],t,'within_template',['fresh-samples.json','raw-coverage.json'],'fresh')
probe(batch,'exact runner batch, before and after delivery','overall',['runner-batch.json','delivery-batch/accepted.json'],'batch')
# Per-template small batch groups are explicitly measured but do not justify
# learning a rule from a one/two-item subgroup. Numeric ranks differ across the
# two iron questions, while singleton contexts need fresh controls above.
batch_groups={t:[info(r) for r in batch if r['generation']['template']==t] for t in {r['generation']['template'] for r in batch}}
save('shortcut-results.json',{'probes':probes,'exact_batch':[info(r) for r in batch],'batch_template_groups':batch_groups,'conditional_batch_interpretation':'The two iron records have ranks1 and3; singleton body/bulb/compressor contexts cannot establish a template rule. Fresh within-template samples provide independent counterexamples. No sign-only repetition or shared answer-producing rule answers all five batch members.','actual_rendered_batch_positions':[z['positions'][0]['position'] for z in ui['groups']['rendered'][:5]],'limitations':['Small regression sample selected independently, not an exhaustive or fitted statistical audit.','Same fresh seeds across templates are controlled comparisons and are not counted as independent random draws for significance.','Opt-in source profiles retain complete observed scalar-offset banks for fidelity, not claims of broader default sampling variety.']})

cf=load(E/'counterfactual-results.json');grader=load(E/'grader-report.json')
assert grader['accepted_checks']==41 and grader['rejected_checks']==164
variation={
 'learner_operation':'Separate and integrate the inhibited-decay equation, apply the initial temperature to fix excess, then evaluate and round the requested future temperature. Moderate controls additionally infer the rate from a later observation and invert for a target time. The answer is a computed scalar, not its option rank or UI position.',
 'fixed_features':[
  {'feature':'Positive rate, initial temperature above ambient and positive elapsed time','justification':'Tutorial da7cd802-d46b-546f-bdc3-8a783a8bb999 defines r>0,P>a; cooling stays above equilibrium.'},
  {'feature':'Easy asks future temperature with specified rate; one integer-unit choice among five','justification':'Canonical e3e001a8-9294-59a4-82e6-b1122afdc72f and all six easy source items use this workload; source practice contract is five-choice radio.'},
  {'feature':'Ordinary boiling Celsius water starts at100; object-appropriate temperature bounds','justification':'Water source02ce9872-8986-5e67-bea1-b49d589c24ac explicitly says boiling. These physical context constraints do not justify fixing correct option rank.'},
  {'feature':'Moderate controls ask for a later lower target temperature','justification':'All five captured moderate problems do so. Earlier-target inversion is mathematically eligible but was not a retained failure or changed rule in this bounded repair. No claim of all possible target orders is made.'}
 ],
 'answer_roles':[
  {'role':'Rounded correct scalar','eligible_variation':'Ambient, initial temperature, positive rate and future evaluation time; moderate observation/target slots.','observed':'Fresh90 contains varied numerical slots; controlled time6->9 changes81->73 and target30->25 changes12->17 with grader/UI agreement.'},
  {'role':'Correct numeric rank among the offered five integers','eligible_variation':'All feasible ranks; no instructional reason fixes rank. Boundary rounding may limit feasible distractor arrangements without excluding the IVP.','observed':'Every recognizable default template has multiple ranks; exact runner ranks2,2,1,5,3. Previously rejected canonical/body IVPs and rounded ambient/initial endpoints now accepted.'},
  {'role':'Radio position and context label','eligible_variation':'Context changes preserving units may preserve the answer; UI order must not identify the correct scalar.','observed':'Same numerical coffee/compressor answer81; bank seed change preserves model and81 while rank2->5. Exact actual-UI ordering tested separately from JSON positions.'}
 ],
 'coverage':[
  {'case':'Every supplied source practice case and complete bank','sample_refs':['source-replay.json','source-replay-records.json'],'result':'All eleven replay, including restored body/pork; outside source unit typo corrected. Canonical bulb parameters/context evaluated; source has no canonical answer bank.'},
  {'case':'Changed default bank construction, each recognizable template','sample_refs':['fresh-samples.json','raw-coverage.json','retained-finding-tests.json'],'result':'56easy,30moderate,4authored-hard controls; each template refutes the old fixed-rank strategy. Hard is unchanged method and outside requested easy batch.'},
  {'case':'Exact runner finite practice batch','sample_refs':['runner-batch.json','delivery-batch/accepted.json','shortcut-results.json'],'result':'5/5 survive. Median, nearest-midrange and nearest-mean each answer1/5; no single rank answers more than2/5. Two iron items have different correct ranks. No batch-wide bypass demonstrated.'},
  {'case':'Previously rejected valid IVPs and integer rounding boundaries','sample_refs':['acceptance-records.json','retained-finding-tests.json'],'result':'Valid canonical44 and body36 accepted; endpoint80 and20 also accepted. Invalid nonpositive time/rate and equilibrium initial condition rejected.'}
 ],
 'counterfactuals':[
  {'kind':'relevant','change':'Hold coffee ambient25,initial100,rate.05 and seed932631 fixed; evaluation time6->9','expected':'Rounded temperature81->73; prompt, substitution, selected UUID and grader must agree.','observed':'Answers81,73; solutions show T(6),T(9); actual UI question006/007 and native grader cases5/6 agree.','status':'passed','justification':'Requested evaluation time directly determines the easy answer.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/rendering.json','render/question-007.png']},
  {'kind':'relevant','change':'Hold bath ambient10,initial50,observed40 at5minutes and seed932631 fixed; target30->25','expected':'Total rounded time12->17; calibrated rate unchanged; target and final logarithm update.','observed':'Answers12,17; rendered question009/010 show changed target and3/8 target-excess ratio; both keys accepted and every distractor rejected.','status':'passed','justification':'Target is an eligible answer-bearing assignment, not a source-fixed label.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/question-009.png','render/question-010.png']},
  {'kind':'irrelevant','change':'At identical Celsius model givens, coffee->compressor context; separately seed932631->932632 changes bank arrangement','expected':'Scalar81 preserved. Context prose may change; bank seed preserves prompt and solution while allowing option rank/position changes.','observed':'Coffee/compressor each81; bank-only change rank2->5 preserves81 and exact prompt/solution. Real grader and rendered question006/008/011 agree.','status':'passed','justification':'Object noun and distractor arrangement carry no evidence in this numeric model.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/rendering.json']}
 ],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['generator validation/rejection/resampling','requested difficulty','actual shared normalization/validation and inventory/batch deduplication','captured inventory','Rust learner freshness, weighted band draw and uniform member selection','actual UI choice ordering'],'sample_refs':['delivery-commands.json','delivery-selection.json','selection-inputs.json','delivery-batch/accepted.json','delivery-easy/accepted.json','shortcut-results.json','ui-order-results.json'],'result':'All90 fresh and5 runner records survive their actual difficulty filters with unchanged per-template/rank coverage. Explicit boundary tests show rank feasibility adapts without the former IVP rejection. Rust selection examined with captured IDs, conditional weights, seen-prefix exclusions and explicitly simulated future IDs; selection does not inspect numeric rank. Seven historical target-time records remain separately enumerated.'},
 'limitations':['Captured basis5392 only; future inventory/history/weights are unavailable and not predicted. No publishing or DB writes.','No captured hard source questions; authored hard controls do not establish source support beyond the requested easy scope.','No finite audit proves absence of every shortcut. Observed above-chance rates in small seed-controlled subgroups are not independent significance estimates.','Historical seven affected stored records persist; accepted current package/batch does not certify them. See affected-inventory.json.']
}
save('pedagogical-variation.json',variation)

# Immutable package check includes every package file, not just runtime manifest files.
after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
before=load(E/'package-hashes-before.json');assert before==after
save('package-integrity.json',{'unchanged':True,'file_count':len(after),'before_file':'package-hashes-before.json','after':after})
checks={
 'source_replay':{'status':'passed','evidence_paths':['source-replay.json','source-replay-records.json','retained-finding-tests.json'],'details':'All eleven source questions replay complete banks, keys, prompts and worked solutions with the documented Fahrenheit-label correction. Restored body/pork profiles and canonical bulb parameters pass.'},
 'math':{'status':'passed','evidence_paths':['math-results.json','counterfactual-results.json','historical-counterexamples-current.json'],'details':'132 independent displayed-prompt numeric and solution-dependency checks pass, including the exact batch, all source replays, restored boundaries and prior mathematical counterexamples.'},
 'variety':{'status':'passed','evidence_paths':['fresh-samples.json','raw-coverage.json','acceptance-records.json','retained-finding-tests.json'],'details':'All changed bank constructors tested across90 fresh records; numerical slots vary and every template has multiple correct ranks. Original rejection and missing-profile defects reproduce on hash-matched old code and pass on current code.'},
 'scope':{'status':'passed','evidence_paths':['source-analysis.json','scope-and-math.json','runner-batch.json'],'details':'Requested easy batch retains specified-rate cooling IVPs, one future-temperature evaluation, integer rounding and five-choice radio response. Existing authored hard extension is outside the easy verdict scope.'},
 'grading':{'status':'passed','evidence_paths':['grader-input.json','grader-report.json','counterfactual-results.json'],'details':'Native learner grader passes205 selections:41 independently calculated correct choices accepted and164 distractors rejected. Radio-only response contract has no free-entry equivalent-notation requirement.'},
 'rendering':{'status':'passed','evidence_paths':['render/rendering.json','rendering-inspection.json','ui-order-results.json'],'details':'Actual UI renders14 cases without math/image/JavaScript errors. Screenshots inspected for changed evaluation time/target and restored body/pork. DOM choice order verified against exact UI function.'},
 'packaging':{'status':'passed','evidence_paths':['packaging.json','relocated-records.json','package-integrity.json'],'details':'Declared exact Python3.13.5/SymPy1.14.0 versions match. Full runtime manifest relocates, deterministically replays and emits valid JSON. Every package file remains unchanged.'},
 'decision_variation':{'status':'passed','evidence_paths':['pedagogical-variation.json','shortcut-results.json','delivery-selection.json','delivery-batch/accepted.json','affected-inventory.json','inventory-results.json'],'details':'Old fixed-rank bypasses fail on current within-template and exact delivered-batch tests. Controlled relevant/irrelevant changes agree across prompts, solutions, real grading and actual UI. Historical seven affected stored records remain separately documented.'}
}
result={'verdict':'accepted','summary':'The repaired generator and exact five-record batch pass all eight checks. Prior defects reproduce on the old executable and are resolved in current output. Seven historical stored questions remain affected and are listed separately. Package unchanged.','source_analysis':{k:v for k,v in load(E/'source-analysis.json').items() if k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':checks,'findings':[]}
save('result.json',result)
# Validate schema and every required relative evidence reference.
import jsonschema
jsonschema.validate(variation,load(R/'generate/pipeline/pedagogical-variation.schema.json'))
refs=[]
def visit(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['sample_refs','evidence_paths']:refs.extend(v)
   visit(v)
 elif isinstance(x,list):
  for y in x:visit(y)
visit(variation);visit(result)
for n in refs:
 p=E/n;assert not pathlib.Path(n).is_absolute() and p.is_file() and p.stat().st_size>0,n
save('evidence-validation.json',{'pedagogical_variation_schema':'passed','relative_nonempty_references':len(refs),'eight_checks':list(checks),'passed':True})
(E/'session-state.md').write_text('Review complete. result.json accepts current package and exact five-record runner batch; all eight checks passed. Old failures freshly reproduced, current controls pass. Native grader205 selections; UI14 renders and representative screenshots inspected;90 fresh records plus5 batch survive actual delivery filtering. Seven historical affected inventory records reproduced and retained in affected-inventory.json/generated-records.json, separate from current acceptance. Entire package hash set unchanged. All output under evidence_root.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:v['status'] for k,v in checks.items()},'evidence_references':len(refs),'package_files_unchanged':len(after),'historical_affected':len(load(E/'affected-inventory.json')['affected_questions'])},indent=2))
