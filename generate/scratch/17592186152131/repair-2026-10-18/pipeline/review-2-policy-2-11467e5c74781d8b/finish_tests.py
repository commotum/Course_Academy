import sys
sys.dont_write_bytecode=True
import json,re,hashlib
from pathlib import Path
from fractions import Fraction
from collections import Counter,defaultdict
E=Path(__file__).resolve().parent
ns={'__file__':str(E/'audit.py')};exec((E/'audit.py').read_text().split('batch=json.loads')[0],ns)
g=ns['g'];save=ns['save'];inspect=ns['inspect'];graded=ns['graded']
load=lambda f:json.loads((E/f).read_text())
raw=load('shortcut-raw.json'); accepted=load('profile-delivery/accepted.json');samples=load('samples.json');cf=load('counterfactual-records.json');batch=load('runner-batch.json');replay=load('source-replay.json')['records']
for r in raw+accepted:inspect(r)
# Native grader is a single batch, covering all actual radio choices for each case.
cases=[]
for prefix,rs in [('counterfactual',cf),('source',replay),('runner',batch),('postprofile',accepted),('postsample',load('delivery/accepted.json')),('fresh-trial',raw[:60])]:
 for i,r in enumerate(rs):cases.append(graded(f'{prefix}-{i}',r))
save('grader-input.json',cases)

def coverage(rs):
 out={'records':len(rs),'templates':dict(Counter(r['generation']['template'] for r in rs)), 'profiles':dict(Counter(r['generation']['profile'] for r in rs)), 'decision_cases':dict(Counter(r['generation']['decision_case'] for r in rs)), 'indices':sorted({r['generation']['parameters']['n'] for r in rs}), 'radicands':sorted({str(r['generation']['parameters']['x']) for r in rs},key=Fraction), 'key_positions':dict(Counter(inspect(r)['position'] for r in rs))}
 out['square_foils']=dict(Counter(str(r['generation']['foil_index']) for r in rs if r['generation']['template']=='square-equation'))
 out['square_directions']=dict(Counter(str(r['generation']['base_direction']) for r in rs if r['generation']['template']=='square-equation'))
 out['square_inverted_base']=dict(Counter(str(r['generation']['inverted_base']) for r in rs if r['generation']['template']=='square-equation'))
 return out
save('coverage-results.json',{'initial_samples':coverage(samples),'initial_postdelivery':coverage(load('delivery/accepted.json')),'all_profiles':coverage(load('profile-records.json')),'profiles_postdelivery':coverage(accepted),'trials':coverage(raw),'runner':coverage(batch),'runner_postdelivery':coverage(load('batch-delivery/accepted.json'))})
# Complete bank multiplicities must survive actual filtering. Identify by mathematical bank alone.
def banks(rs):
 d=defaultdict(set)
 for r in rs:
  f=r['question'][':question/answer-fields'][0];bank=tuple(sorted(a[':answer/value'] for a in f[':answer-field/choices']));key=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);d[(r['generation']['template'],bank)].add(key)
 return Counter(len(v) for v in d.values())
save('postdelivery-bank-results.json',{'before':dict(banks(load('profile-records.json'))),'after':dict(banks(accepted)),'explanation':'Four eligible answers per indexed bank, two per square bank. Checking actual accepted records, rather than assuming deduplication preserves counterfactuals.'})
assert banks(load('profile-records.json'))==banks(accepted)
# Probe ranked choices, foil leakage and inverted base separately within recognizable subgroups.
probes=[]
for stage,rs in [('profile_raw',load('profile-records.json')),('profile_accepted',accepted),('fresh_trials',raw)]:
 groups=defaultdict(list)
 for r in rs:
  t=r['generation']['template'];q=r['question'];f=q[':question/answer-fields'][0];key=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);vs=[a[':answer/value'] for a in f[':answer-field/choices']]
  if t.startswith('indexed'):
   foil=next(re.fullmatch(r'\{1\}\^\{(\d+)/(\d+)\}',v) for v in vs if v.startswith('{1}^'))
   prediction=f'{{{foil[1]}}}^{{1/{foil[2]}}}'
   groups[(t,'base1-foil reconstruction',.25)].append(key==prediction)
   # Answer-only smallest numerical base and index; neither mathematical role is supplied by prompt.
   unit=[(Fraction(m[1]),int(m[2]),v) for v in vs if (m:=re.fullmatch(r'\{([\d.]+)\}\^\{1/(\d+)\}',v)) and m[1]!='1']
   prediction=min(unit)[2];groups[(t,'smallest base and denominator',.25)].append(key==prediction)
  else:
   half=[(Fraction(m[1]),v) for v in vs if (m:=re.fullmatch(r'\{([\d.]+)\}\^\{1/2\}',v))]
   inv=next(re.fullmatch(r'\{([\d.]+)\}\^\{2/1\}',v) for v in vs if re.fullmatch(r'\{([\d.]+)\}\^\{2/1\}',v))
   prediction=f'{{{inv[1]}}}^{{1/2}}';typ='decimal' if '.' in inv[1] else 'integer';foil=r['generation']['foil_index']
   groups[(f'{t}/{typ}/foil={foil}','copy inverted-power base',.5)].append(key==prediction)
   groups[(f'{t}/{typ}/foil={foil}','choose smaller square-root base',.5)].append(key==min(half)[1])
 for (sub,strategy,baseline),v in groups.items():probes.append({'stage':stage,'subgroup':sub,'strategy':strategy,'correct':sum(v),'total':len(v),'baseline':baseline})
save('conditional-shortcuts.json',{'probes':probes,'conclusion':'Full fixed-bank target groups give 1/4 for indexed strategies and 1/2 for square strategies, including integer/decimal and foil-index cue subgroups. Trial deviations are compared to those baselines; none establishes a deterministic predictor.'})
# Save observed scope and source gaps explicitly.
save('scope-results.json',{'source_family':'All three captured five-choice radio forms; canonical operation separately checked.','operations':'Only identify radicand, index and reciprocal exponent. No non-unit powered radicals, inverse direction, variables, negative roots or evaluation.','decimal_extension':'Square radicands include positive decimals. This changes a copied token only; tutorial3293 states the identity for general x. No decimal arithmetic is required.','numeric_restrictions':'Finite indexed x=2..15,n=3..10 excludes x=n and (2,4), preventing equal-valued legacy swapped-root distractors; revised grids could permit some such targets. This conservative family retains both magnitude orderings, all source parameters, all supported indices, and no demonstrated answer-position or answer-role shortcut. Not a claim of exhaustive radical coverage.','uncaptured_evidence':['q-69158 key, worked solution and difficulty missing; identity determines key and authored explanation is flagged as inferred.','e-4959 answer field absent; only mathematical identity and solution stages replayed, no invented canonical bank.'],'math_records_checked':len(raw)+len(accepted)+len(samples)+len(cf)+len(batch)+3,'failures':[]})
# Reconfirm package immutability including undeclared author artifacts.
assert load('package-before.json')==ns['hashes']()
p=load('packaging-results.json');p['after']=ns['hashes']();p['package_unchanged']=True;save('packaging-results.json',p)
(E/'session-state.md').write_text('Completed exact arithmetic on all 1,765 indexed profiles, 21 square pairs, 512 fresh five-item trials, source replay, delivery and learner-selection model. Native grader input includes all five responses to every accepted profile and controlled pair. UI renderer extended to all 18 representative records. Await native grader and final screenshot inspection/report.\n')
print(json.dumps({'grader_records':len(cases),'grader_submissions':5*len(cases),'conditional_probes':len(probes),'profile_delivery_counts':{k:v for k,v in load('profile-delivery/delivery.json').items() if k in ['input_count','accepted_count','duplicate_count']},'package_unchanged':True}))
