# Complete evidence for the demonstrated sampling gap; do not touch package.
import sys
sys.dont_write_bytecode=True
import json,re,hashlib
from pathlib import Path
from fractions import Fraction
from collections import Counter
E=Path(__file__).resolve().parent
P=Path('/home/jake/Developer/Course_Academy/generate/scratch/17592186152131/repair-2026-10-18/pipeline/workspace')
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
# Reuse the reviewer's exact-math functions without re-executing sampler setup.
ns={'__file__':str(E/'audit.py')};exec((E/'audit.py').read_text().split('batch=json.loads')[0],ns)
raw=json.loads((E/'shortcut-raw.json').read_text());rs=json.loads((E/'shortcut-results.json').read_text())
checks=Counter();failure=[]
for i,r in enumerate(raw):
 try:ns['inspect'](r);checks.update([r['generation']['template']])
 except Exception as e:failure.append({'index':i,'error':str(e)})
assert not failure
math=json.loads((E/'math-results.json').read_text());math['expanded_sampling_check']={'records':len(raw),'templates':checks,'failures':failure};save('math-results.json',math)
cases=[];grader=json.loads((E/'grader-input.json').read_text())
for i in rs['accepted']['indices']:
 r=json.loads((E/'shortcut-accepted.json').read_text())[i] if False else raw[i]
 # All zero-duplicate independent trial batches preserve array ordering.
 q=r['question'];f=q[':question/answer-fields'][0];choice=next(a for a in f[':answer-field/choices'] if a[':answer/value']=='{2}^{1/2}')
 expected='accepted' if re.search(r'\\sqrt\{2\}',q[':question/problem']) else 'rejected'
 cases.append({'flattened_index':i,'trial_seed':461003+i//5,'batch_index':i%5,'expected_shortcut_result':expected,'record':r})
 grader.append({'label':f'shortcut seed={461003+i//5} index={i%5}','record':r,'checks':[{'field_index':0,'submitted_answer_id':choice[':answer/id'],'expected':expected,'purpose':'Answer-bank-only choose2^(1/2) strategy; expected outcome independently reads radical rather than key metadata.'}]})
save('shortcut-cases.json',cases);save('grader-input.json',grader)
# Compact slot coverage and scope interpretation.
samples=json.loads((E/'samples.json').read_text());accepted=json.loads((E/'delivery/accepted.json').read_text());batch=json.loads((E/'runner-batch.json').read_text());cf=json.loads((E/'counterfactual-records.json').read_text())
def coverage(records):
 return {'count':len(records),'templates':dict(Counter(r['generation']['template'] for r in records)),
 'profiles':dict(Counter(r['generation']['profile'] for r in records)),
 'indices':sorted({r['generation']['parameters']['n'] for r in records}),
 'radicands':sorted({str(r['generation']['parameters']['x']) for r in records},key=Fraction),
 'decision_cases':dict(Counter(r['generation']['decision_case'] for r in records)),
 'square_foil_indices':dict(Counter(str(r['generation']['foil_index']) for r in records if r['generation']['template']=='square-equation')),
 'square_directions':dict(Counter(str(r['generation']['base_direction']) for r in records if r['generation']['template']=='square-equation')),
 'square_inverted_base':dict(Counter(str(r['generation']['inverted_base']) for r in records if r['generation']['template']=='square-equation')),
 'indexed_bank_profiles':len({json.dumps(r['generation']['indexed_bank'],sort_keys=True) for r in records if r['generation']['indexed_bank']})}
save('coverage-results.json',{'raw':coverage(samples),'delivery':coverage(accepted),'runner':coverage(batch),'expanded_shortcut_trials':coverage(raw),'source_family_coverage':'All three supplied question forms and complete source banks replay. Ordinary indexed practice uses new grid bank; square practice uses alternate-base/index bank. Canonical e-4959 operation checked separately; no fabricated canonical bank.',
 'scope_judgment':'Positive decimals are unobserved radicand values but do not require decimal arithmetic: the radicand is copied as a token. The tutorial identity applies to general x. No inverse conversions, powered radicands, negative or variable expressions, extra response fields or evaluation added.',
 'limits':'Finite supported family excludes indexed x=n and (2,4), and larger numbers. No claim that all legitimate radicals are covered. Excluded degenerate legacy bank parameters are a conservative numeric family restriction, not evidence by itself of an incidental deterministic key.'})
# Preserve initial independent source analysis, with transparent scope clarification.
a=json.loads((E/'source-analysis.json').read_text());a['post_test_scope_clarification']='Initial account used positive integer as a conservative observed-domain invariant. That is not an essential mathematical constraint: tutorial3293 states the rule for general x. Copying positive decimal radicands introduces no additional reasoning or evaluation. This clarification distinguishes original observation from final scope judgment and does not revise the independently identified learner operation.';save('source-analysis.json',a)
# Package preservation and declaration check.
old=json.loads((E/'package-before.json').read_text());now={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()};assert old==now
pack=json.loads((E/'packaging-results.json').read_text());pack['after']=now;pack['package_unchanged']=True;save('packaging-results.json',pack)
print(json.dumps({'exact_math_expansion':len(raw),'failures':failure,'native_grader_records':len(grader),'shortcut_cases':len(cases),'example_success':next({'seed':x['trial_seed'],'index':x['batch_index']} for x in cases if x['expected_shortcut_result']=='accepted'),'example_failure':next({'seed':x['trial_seed'],'index':x['batch_index']} for x in cases if x['expected_shortcut_result']=='rejected'),'package_unchanged':True}))
