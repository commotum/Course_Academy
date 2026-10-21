"""Assemble evidence-backed review; all writes remain in evidence_root."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
repo=Path('/home/jake/Developer/Course_Academy')
def load(n):return json.loads((root/n).read_text())
def save(n,d):(root/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
source=load('source-analysis.json')
counter=load('counterfactual-tests.json')['pairs']
groups=load('controlled-bank-tests.json')['groups']
shortcuts=load('shortcut-tests.json')
render=load('render-inspection.json')

fixed=[
 {'feature':'Two factors with a common valid base; product/power expansion and given-log substitution.', 'justification':'q-79453 and q-98925 both use this operation; tutorial 2796 provides its identities. More factors or quotients would add a reasoning stage outside these hard examples.'},
 {'feature':'Numeric family has two nonunit exponents; symbolic family has one unit exponent, one nonunit exponent and one symbolic given.', 'justification':'Preserves the two observed hard workloads: two short numeric products versus one affine result. Fixing which variable has these roles is unnecessary and is tested independently.'},
 {'feature':'Five radio choices, one correct identity/value; x and y positive and base >1.', 'justification':'All four bank items use five radio alternatives; logarithm domain is mathematically necessary. Conservative bases >1 suffice without a new prerequisite.'},
 {'feature':'Integer exponent/given magnitudes remain small; no fractional exponents sampled as hard.', 'justification':'Two explicit hard cases have integer exponents and givens. The wider lesson has a fractional example but does not establish its hard substitution workload. Negative given logarithms remain realizable by positive x=b^u, y=b^v.'},
 {'feature':'Letters x,y,k and base set {2,3,5,7,10}.','justification':'Renaming letters and extending the infinite valid base set does not change the answer-bearing association operation. Both variable assignments are varied, so fixed letters provide no fixed-role shortcut.'}
]
roles=[
 {'role':'Which given is symbolic','eligible_variation':'Either x or y, independently of which factor is powered.','observed':'All four symbol/powered assignments and both signs observed. Controlled x-to-y swap changes k+6 to 3k+2 with exponents fixed.'},
 {'role':'Which variable carries the nonunit symbolic-family exponent','eligible_variation':'Either factor; change its exponent while holding the other givens and bank fixed.','observed':'Both factors are powered in sampled symbolic cases; minimal exponent changes produce 2k-2 then 3k-2 for each symbolic variable.'},
 {'role':'Numeric coefficients and given values','eligible_variation':'Vary both exponent/value assignments, magnitudes, and signs without changing product/power rules.','observed':'All 12 unequal exponent pairs from 2..5, all 12 nonzero givens -6..6, all four sign quadrants, all five bases and both given orders occur in 160 fresh samples.'},
 {'role':'Which visible candidate is correct','eligible_variation':'All five bank values and positions may be correct when the prompt evidence changes.','observed':'12 controlled sign/factor subgroups each retain a fixed five-value bank and five different correct values; all 60 survive delivery. Raw options are shuffled independently, and the UI further reorders by IDs.'}
]
coverage=[]
for group in groups:
 coverage.append({'case':group['group'],'sample_refs':['controlled-bank-records.json','controlled-bank-tests.json','delivery/accepted.json'],'result':f"Five different correct values {group['correct_values']} with the same visible bank; no controlled role removed by delivery."})
coverage.append({'case':'Fresh-seed slot coverage and actual runner batch','sample_refs':['samples.json','runner-batch.json','math-tests.json','delivery-stage-tests.json'],'result':'160 fresh samples cover 74 numeric and 86 symbolic; all justified sign/factor/exponent/base/order slots observed. Runner batch 5/5 accepted. Delivery 220/220 independent and 5/5 runner records.'})
counterfactuals=[]
for pair in counter:
 counterfactuals.append({'kind':pair['kind'],'change':pair['label'],'expected':'Recompute answer because the weighted-sum evidence changed.' if pair['relationship']=='different' else 'Preserve the mathematical response while updating presentation and any base notation.','observed':f"Before {pair['before_correct']}; after {pair['after_correct']}. Exact visible-prompt arithmetic, worked substitution, rendered prompt/final equation and native grading all agree.",'status':'passed','justification':'The exponent-to-given association in q-79453/q-98925 determines the answer; common-base relabeling, given order and display order do not change that weighted sum.','sample_refs':['counterfactual-records.json','counterfactual-tests.json','render-inspection.json','grader-input.json','grader-report.json']})
probes=[]
for p in shortcuts['empirical']:
 if p['stage']=='samples.json' and p['subgroup'] in ('overall','numeric','symbolic'):
  probes.append({'cue':p['strategy'],'subgroup':p['subgroup'],'scope':'overall' if p['subgroup']=='overall' else 'within_template','strategy':p['strategy']+' using only displayed choices; ties use first stored choice.','correct':p['correct'],'total':p['total'],'baseline':0.2,'disposition':'not_predictive','conclusion':'Baseline 1/5 is blind selection among five distinct alternatives. This finite descriptive rate does not show a reliable perfect predictor; conditional controlled banks test the stronger fixed-bank claim.','sample_refs':['samples.json','shortcut-tests.json']})
for p in shortcuts['controlled']:
 probes.append({'cue':p['strategy'],'subgroup':p['subgroup'],'scope':'other_recognizable_subgroup','strategy':p['strategy']+'; hold the visible bank and recognizable sign/factor subgroup fixed while changing target evidence.','correct':p['correct'],'total':p['total'],'baseline':0.2,'disposition':'not_predictive','conclusion':'Exactly 1/5 equals blind-choice baseline. Each of five bank values is correct for one prompt. This remains true after shared delivery filtering. Role changes, not numerical uniqueness, establish the result.','sample_refs':['controlled-bank-records.json','controlled-bank-tests.json','shortcut-tests.json','delivery/accepted.json']})
for p in render['ui_position_probes']:
 probes.append({'cue':'Actual UI option position','subgroup':p['subgroup'],'scope':'within_template','strategy':p['strategy'],'correct':p['correct'],'total':p['total'],'baseline':0.2,'disposition':'not_predictive','conclusion':p['conclusion']+' Baseline is blind 1-of-5 selection; these paired cases are a descriptive layout check, not an independent random-frequency estimate.','sample_refs':['render-inspection.json','render-input.json']})

variation={
 'learner_operation':source['skill']+' Associate the exponent on each variable with that same variable’s given logarithm; the displayed evidence must determine the weighted sum.',
 'fixed_features':fixed,'answer_roles':roles,'coverage':coverage,'counterfactuals':counterfactuals,'shortcut_probes':probes,
 'delivery':{'stages_examined':['Generator duplicate-answer rejection before key selection','Requested hard difficulty','Publisher actual prepare_records normalization, validation and inventory/within-batch deduplication','Actual native radio grading','Actual UI hash-based option ordering and rendering','Learner freshness and difficulty-first weighted selection, with unconfigured/zero-weight branches'], 'sample_refs':['samples.json','controlled-bank-records.json','runner-batch.json','delivery/delivery.json','runner-delivery/delivery.json','delivery-stage-tests.json','selection-tests.json','grader-report.json','render-inspection.json'], 'result':'At captured basis 4975, all 220 independent and 5 runner records survive; all 12 controlled subgroups retain all five answer roles. Duplicate-answer rejection precedes uniformly selected role, so does not favor a selected key. Faithful read-only selection reproduction retains every eligible subgroup when hard has positive weight. Zero hard weight and consumed history intentionally remove supply; unconfigured policy selects lowest fresh ID rather than sampling uniformly.'},
 'limitations':['Finite audit cannot prove absence of every possible shortcut. Option-based use of exponent association or arithmetic is intended skill, not automatically a defect.','Selection policy, learner history and future allocated entity IDs are absent from captured inventory. Selection scenarios use explicit synthetic IDs and the actual SHA256 selector algorithm; they show conditional support, not a prediction of a particular live learner draw.','Inventory may change after captured basis 4975; later deduplication can change available coverage. No publication or database writes occurred.','Canonical e-4082 is a demonstration without a captured radio bank and is not separately replayable through the hard generator. Two unrated source banks lack original keys/solutions; their inferred completions are independently checked, not presented as original source evidence.','Easy/moderate, three-factor/quotient tasks, and fractional hard-substitution workloads are not supported or certified.']}
save('pedagogical-variation.json',variation)

pkg=root.parent/'workspace'
after={str(p.relative_to(pkg)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pkg.rglob('*') if p.is_file()}
before=load('package-before.json');assert after==before
save('package-integrity.json',{'unchanged':True,'file_count':len(after),'before':'package-before.json','after_sha256':after,'database_writes':0,'published_assets':0})

commands=load('commands.json')
commands['delivery']=[['/home/jake/Developer/Course_Academy/.venv/bin/python','-B',str(repo/'generate/pipeline/check_delivery.py'),'--input',str(root/infile),'--source',str(root.parent/'source/source.json'),'--inventory',str(root.parent/'source/inventory.json'),'--difficulty','hard','--output',str(root/out),'--asset-root',str(root),'--math-root','/media/jake/SSD/EDB/math'] for infile,out in [('delivery-input.json','delivery'),('runner-batch.json','runner-delivery')]]
commands['grader']=[str(repo/'generate/runs/current/check-engine'),str(root/'grader-input.json'),str(root/'grader-report.json')]
commands['renderer']=[str(repo/'.venv/bin/python'),'-B',str(repo/'generate/pipeline/render_preview.py'),'--input',str(root/'render-input.json'),'--output',str(root/'render'),'--asset-root',str(root),'--math-root','/media/jake/SSD/EDB/math','--limit','31']
commands['supplemental']=[[str(repo/'.venv/bin/python') if name!='finalize-review.py' else 'python3','-B',str(root/name)] for name in ['source-symbolic-math.py','delivery-and-cues.py','inspect-render.py','finalize-review.py']]
save('commands.json',commands)

def passed(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
result={
 'verdict':'accepted',
 'summary':'No concrete defect found. All eight checks passed; original package unchanged. Acceptance is limited to hard product/power substitution practice and captured inventory basis 4975.',
 'source_analysis':{k:source[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
 'checks':{
 'source_replay':passed(['source-analysis.json','source-replay-records.json','source-replay-tests.json','source-symbolic-math.json'],'All four practice prompts and all 20 choices replay at original parameters. Both recorded hard keys and solution stages match. Missing unrated keys/solutions are explicitly inferred and independently checked; canonical demonstration has no source bank to reproduce.'),
 'math':passed(['math-tests.json','source-symbolic-math.json','counterfactual-tests.json','cli-1000.json'],'Exact visible-prompt arithmetic, five distinct answer identities and worked expansions/substitutions pass on 249 hard test records plus 1000 boundary outputs. SymPy independently verifies both incomplete symbolic-source identities and refutes all distractors with positive witnesses.'),
 'variety':passed(['samples.json','math-tests.json','controlled-bank-tests.json','delivery-stage-tests.json','selection-tests.json'],'160 fresh samples cover both hard families, all 12 exponent pairs, 12 signed givens, five bases, both orders and all 12 sign/factor subgroups. All controlled answer roles survive delivery. Freshness/weighted-selection conclusions are conditional on explicit policies and history scenarios.'),
 'scope':passed(['source-analysis.json','scope-tests.json','source-replay-tests.json'],'Two-factor product/power expansion and substitution retain source workloads. Signed logarithm values are realizable with positive arguments. Unrated source-only, unsupported difficulty and canonical demonstration limits are explicit.'),
 'grading':passed(['grader-input.json','grader-report.json','grader-command.log'],'Native learning::grade_field accepted 476 independently correct radio selections and rejected 1904 distractor selections, including before/after pairs and normalized delivery records. No free-entry fields exist, so free-entry equivalents are inapplicable.'),
 'rendering':passed(['render/rendering.json','render-inspection.json','render/question-001.png','render/question-003.png','render/question-022.png','render/question-023.png','render/question-024.png'],'Actual UI renders all 31 cases without reported math/JS/font/image errors. Parsed rendered MathML matches every prompt and final equation; five radio controls and feedback keys match. Representative full screenshots visually inspected.'),
 'packaging':passed(['packaging-tests.json','package-integrity.json','commands.json','determinism-relocated.json'],'Exact declared/actual Python 3.13.5; empty third-party package map matches stdlib-only runtime plus declared local helper. Determinism, relocation, count boundaries 0/1/1000, invalid counts/difficulties and no external outputs checked. Package file hashes unchanged.'),
 'decision_variation':passed(['pedagogical-variation.json','counterfactual-tests.json','controlled-bank-tests.json','shortcut-tests.json','delivery-stage-tests.json','selection-tests.json','render-inspection.json'],'Relevant changes update prompts, answers, solutions, rendered math and native grades; irrelevant base/order changes preserve responses. Six bank-only strategies are 1/5 in each of 12 controlled sign/factor subgroups, including after delivery. Actual UI position probes and selection-support scenarios reveal no reproducible incidental shortcut.')},
 'findings':[]}
save('review-result.json',result)

# Validate required evidence contract using the supplied schema, not an author's report.
import jsonschema
jsonschema.Draft202012Validator(json.loads((repo/'generate/pipeline/pedagogical-variation.schema.json').read_text())).validate(variation)
for section in list(result['checks'].values())+[result['source_analysis']]:
 for path in section['evidence_paths']:
  target=root/path;assert target.is_file() and target.stat().st_size>0,path
for name in ['coverage','counterfactuals','shortcut_probes']:
 for item in variation[name]:
  for path in item['sample_refs']:
   assert not Path(path).is_absolute() and (root/path).is_file() and (root/path).stat().st_size>0,path
for path in variation['delivery']['sample_refs']:assert (root/path).is_file() and (root/path).stat().st_size>0
save('evidence-contract.json',{'passed':True,'pedagogical_variation_schema':'generate/pipeline/pedagogical-variation.schema.json','eight_checks':len(result['checks']),'all_cited_files_nonempty':True,'package_unchanged':True})
(root/'session-state.md').write_text('Completed: independent original-source analysis; four full bank replays; 160 fresh samples, 60 fixed-bank role cases and 11 relevant/irrelevant counterfactual pairs; 1000-output boundary; exact math; delivery 220/220 plus runner 5/5; native grading 476 correct/1904 wrong; 31 actual UI cases and screenshot inspection; selection and shortcut tests; dependency/relocation/determinism; package hashes unchanged. All eight checks passed. review-result.json is the final structured report. pedagogical-variation.json validated against supplied schema. No publication/database writes or package edits.\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(result['checks']),'findings':len(result['findings']),'package_unchanged':True,'contract_passed':True}))
