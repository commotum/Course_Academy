"""Confirm a conditional shortcut using prompt constants and typography only."""
import sys;sys.dont_write_bytecode=True
import json,pathlib,random,collections
from fractions import Fraction as F
from audit_math import extract,tex,field,answer,V,S,verify
R=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'workspace'));import generator as G

def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
def evaluate(records,label):
 rows=[]
 for j,r in enumerate(records):
  if r['generation'].get('template')!='P':continue
  integrand,var=extract(r);x=V[var]
  # Only identify the printed constant, never integrate the nonconstant term.
  constant=S.expand(integrand).coeff(x,0)
  n=max(term.as_powers_dict().get(x,0) for term in S.Add.make_args(integrand))
  if n not in (4,6):continue
  selected=[];details=[]
  for idx,a in enumerate(field(r)[':answer-field/choices']):
   val=S.expand(tex(a[':answer/value'])-V['C']);linear=val.coeff(x,1)
   powerterm=val-linear*x
   coefficient=abs(powerterm.as_coeff_Mul()[0])
   numerator,denominator=coefficient.as_numer_denom()
   eligible=(linear==constant and numerator==1 and denominator<10)
   if eligible:selected.append(idx)
   details.append({'index':idx,'linear':str(linear),'power_coefficient_numerator':str(numerator),'power_coefficient_denominator':str(denominator),'eligible':bool(eligible)})
  win=len(selected)==1 and field(r)[':answer-field/choices'][selected[0]][':answer/id']==answer(r)[':answer/id']
  rows.append({'stage':label,'sample_index':j,'id':r['question'][':question/id'],'printed_exponent':str(n),'printed_constant':str(constant),'selected_indices':selected,'correct':win,'choice_details':details})
 return {'stage':label,'strategy':'For polynomial prompts with printed exponent 4 or 6: retain options whose linear coefficient matches the printed constant; choose the power fraction with numerator 1 and a one-digit denominator. Do not calculate an antiderivative of the power term.','correct':sum(r['correct'] for r in rows),'total':len(rows),'baseline':0.2,'trials':rows}
raw=json.loads((R/'samples.json').read_text());delivered=json.loads((R/'delivery/accepted.json').read_text());holdout=G.generate(count=240,seed=86184906)
save('shortcut-holdout-records.json',holdout)
for r in holdout:
 if r['generation']['template']=='P' and r['generation']['parameters']['n'] in (4,6):verify(r)
results=[evaluate(raw,'discovery raw'),evaluate(delivered,'discovery delivered'),evaluate(holdout,'fresh holdout raw')]
assert all(a['correct']==a['total'] and a['total']>0 for a in results)
proof=[]
for q in (5,7):
 row=[]
 for f in (F(1,3),F(1,2),F(2,3),F(3,2),F(2),F(3)):
  c=F(1,q)*f;row.append({'distractor_factor':str(f),'resulting_coefficient':str(c),'passes_cue':c.numerator==1 and c.denominator<10})
 assert not any(r['passes_cue'] for r in row)
 proof.append({'correct_coefficient':str(F(1,q)),'correct_passes_cue':True,'all_eligible_distractor_coefficients':row})
save('shortcut-confirmation.json',{'results':results,'domain_proof':proof,'pedagogical_assessment':'Demonstrated incidental answer-producing action: the only mathematical step is integrating the constant; no increment/divide operation on x^4 or x^6 is needed. All choices supply the same integrated power already. The learner can recognize exponent 4/6 and the typographic coefficient cue. This bypasses the nonconstant power-rule calculation required by e-371 and q-71167.','controls':'Both source and normal options are independently correct/keyed, so the finding concerns distractor design, not wrong mathematics. Random choice baseline .2; guessing after matching the constant gives 1/2 or 1/3 rather than certainty.'})
# Render examples representing both cue subgroups, directly from fresh samples.
examples=[]
for n in (4,6):examples.append(next(r for r in holdout if r['generation']['template']=='P' and r['generation']['parameters']['n']==n))
save('shortcut-render-records.json',examples)
print(json.dumps([{k:v for k,v in a.items() if k!='trials'} for a in results]))
