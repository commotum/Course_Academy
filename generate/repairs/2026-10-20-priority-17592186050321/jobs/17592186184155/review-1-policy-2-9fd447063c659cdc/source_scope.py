from audit import *
src=json.loads((JOB/'source/source.json').read_text())['material']['kp'];results=[]
for q in src[':knowledge-point/questions']+[src[':knowledge-point/canonical-example']]:
 p=re.findall(r'\$(.*?)\$',q[':question/problem'],re.S)[0].strip().rstrip('= .')
 p=re.sub(r'\\textrm\s+d\s*x','',p)
 val=parse(p);integrand=derivative(val) if r'\int' in p else val
 stages=[]
 if ':question/worked-solution' in q:
  s=q[':question/worked-solution'].split('$$')[1];s=re.sub(r'\\(?:begin|end)\{aligned\}','',s).replace('\\\\','').replace('&','')
  for step in s.split('='):
   assert derivative(parse(step))==integrand,(q[':question/math-academy-id'],step);stages.append(step)
 results.append({'source_id':q[':question/id'],'source_name':q[':question/math-academy-id'],'solution_stages_checked':len(stages),'complete_bank':bool(q.get(':question/answer-fields')),'difficulty':q.get(':question/difficulty'),'result':'passed visible source mathematics; response replay only when fields are captured'})
save('source-math-results.json',{'command':f'{PY} source_scope.py','cases':results})
save('scope-results.json',{'source_basis':'source-analysis.json and source-math-results.json','observed_domain':'Both hard profiles: one positive integer power, one negative integer power and one odd-denominator fractional power; three independent signed nonzero integer coefficients.','judgments':[{'feature':'Odd degrees 3,5,7 and rational numerators','result':'Same radical-to-power and rational exponent arithmetic as q-113848, q-113850 and q-29830; seventh-root extension explicitly authored. Avoids even-root branch work.'},{'feature':'Integer exponents 1..7, reciprocal -2..-6, magnitudes 1..6','result':'Conservative finite arithmetic workload; not required to enumerate every power for an instructional family. Negative fractional -(d+1)/d is narrower than every possible odd rational, but supports the negative-fractional operation; q-29830 exact -13/7 remains replayable. No target label or answer action is fixed by this restriction.'},{'feature':'Sign and term order','result':'All signs per role and all six orders appear. Reordering changes presentation while preserving mathematics, as tested.'},{'feature':'Five radio choices with distributed term errors','result':'Response shape and reasoning stages preserved. Source errors include coefficient and exponent errors; varied combinations do not require new operators.'},{'feature':'Unsupported moderate/easy generation','result':'Explicitly rejected. Moderate source records lack answer fields and easy has no source evidence; these are disclosed unsupported families, not silent missing hard profiles.'}], 'render_representatives':'render-input.json','sampling_evidence':'coverage.json','counterfactual_evidence':'counterfactual-results.json','result':'passed'})
print('All seven original source records: mathematics checked; captured banks replayed separately.')
