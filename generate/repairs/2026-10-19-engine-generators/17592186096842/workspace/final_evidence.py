"""Validate filtered controls and prepare final native/UI evidence."""
import json,collections,hashlib
import sympy as sp
import generator as g
from validate import independent,grading,key,field,save,coverage
from validation_math import displayed,equal
accepted=[];cf=[];roles=[]
for band in ['easy','moderate','hard']:
 accepted+=json.load(open('evidence/delivery-'+band+'/accepted.json'))
 cf+=json.load(open('evidence/delivery-counterfactual-'+band+'/accepted.json'))
 roles+=json.load(open('evidence/delivery-roles-'+band+'/accepted.json'))
# All five bank assignments must remain represented in every radio layout.
counts=collections.defaultdict(set)
for r in roles:counts[r['generation']['template']].add(r['generation']['bank_assignment'])
assert len(counts)==8 and all(v==set(range(5)) for v in counts.values())
# Controlled curve and target response changes survive normalization/deduplication.
controlled=[r for r in cf if r['generation']['template']=='slope_sqrt_quadratic_blank']
assert len(controlled)==3
answers=[displayed(key(r)[':answer/value']) for r in controlled]
assert set(sp.sign(v) for v in answers)=={-1,0,1}
lin=[r for r in cf if r['generation']['template']=='slope_sqrt_linear_blank']
assert len(lin)==2 and not equal(displayed(key(lin[0])[':answer/value']),displayed(key(lin[1])[':answer/value']))
# Source duplicate q-342802 at t=2 is already present in inventory; its reflected
# case survives. The raw control and native grader prove both source and new case.
recip=[r for r in cf if r['generation']['template']=='slope_reciprocal_blank']
assert len(recip)==1 and recip[0]['generation']['parameters']['t']==-6
sample=json.load(open('evidence/delivery-sample/accepted.json'));assert len(sample)==5
one_per_layout={}
for r in accepted:one_per_layout.setdefault(r['generation']['template'],r)
cases=[]
for i,r in enumerate(cf+roles+list(one_per_layout.values())+sample):cases.append(grading(r,independent(r),'post-delivery '+str(i)))
save('post-delivery-grader-input.json',cases)
# Explicit controlled response/counterfactual evidence after actual filtering.
save('pedagogical-variation.json',{
 'learner_operation':'decompose radical composition; differentiate outer and inner; multiply; evaluate requested point; apply sum rule only in sum family',
 'fixed_feature_reasons':'instructional-account.md',
 'source_fidelity':'17 inputs; 8/8 complete radio banks (40/40 choices); blank histories retained separately; q-48846 missing fields repaired explicitly',
 'mathematics':'180 parsed-rendered records plus source/counterfactual/control/rejection cases independently differentiated; every displayed solution equation checked',
 'decision_variation':'122 semantic function/exponent/point/cubic tuples in the normal probe set; answer ranks and signs vary within each radio layout; zero slopes served in appropriate blanks',
 'shortcut_checks':{'before':'pedagogical-variation-before.json','after':'pedagogical-variation-after.json','selection':'pedagogical-variation-selection.json','fixed_data_bank_controls':'role-controls.json','all_five_roles_survive_for_layouts':len(counts)},
 'controlled_evidence':{'raw_counterfactual_records':37,'surviving_counterfactual_records':len(cf),'quadratic_fixed_curve_answers':[str(v) for v in answers],'linear_fixed_curve_target_cases':len(lin),'reciprocal_source_duplicate':'positive/negative pair tested with actual grader; original t=2 duplicate already in source inventory, t=-6 survives','irrelevant_spacing':'mathematical response preserved; actual native check in grader-input.json'},
 'generator_rejection':'rejection-probe.json (seed 1168, zero radio bank rejected, chosen role preserved)',
 'selection_limits':'See delivery-audit.json; synthetic IDs reproduce configured uniform within-band support only. Actual learner history, future inventory, live entity ordering and legacy unconfigured first-entity policy cannot be certified offline.',
 'grading_limits':'Equivalent reciprocal fractional-power notation produces unresolved domain differences in the actual engine (grader-domain-report.json); canonical radicals and same-domain equivalents pass. No engine or database changes.',
 'normal_bank_extension':'Contiguous integer coefficient ladder; role chosen before compatible evidence, all five answers rendered identically. Historical source banks are restricted to source replay.'})
source=json.load(open('evidence/source-records.json'))
zero=next(r for r in source if r['generation']['replay_source_id']=='q-342789')
sumcase=next(r for r in accepted if r['generation']['template']=='slope_sum_radio' and r['generation']['parameters']['k']<0)
hard=next(r for r in accepted if r['generation']['template']=='slope_sqrt_quadratic_radio' and r['generation']['parameters']['a']<0)
blank=next(r for r in accepted if r['generation']['template']=='sqrt_quadratic_blank' and r['generation']['parameters']['a']<0)
save('final-render-records.json',[sample[0],sample[1],zero,sumcase,hard,blank])
manifest=json.load(open('package.json'))
save('runtime-hashes.json',{name:hashlib.sha256(open(name,'rb').read()).hexdigest() for name in ['package.json']+manifest['files']})
print(json.dumps({'post_delivery_grader_cases':len(cases),'all_bank_roles_retained':40,'counterfactuals_retained':len(cf),'final_render_count':6}))
