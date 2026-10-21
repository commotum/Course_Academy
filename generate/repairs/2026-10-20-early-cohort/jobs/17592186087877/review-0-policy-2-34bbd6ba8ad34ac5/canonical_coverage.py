"""Strict canonical-source regression, using every reachable easy Q at P=2.

Other easy a values cannot match P=2. For constant_cos both signs of b
produce the same cosine, so b=1..4 is complete. The other Q slot is n=1..4.
Moderate/hard templates have nonconstant P (nonzero a/k, degree >=2).
"""
import sys
import audit as A

target=A.V+2*A.Y-2*A.S.exp(-2*A.X)
records=[]
for t in ['constant_cos','scaled_constant_power','signed_constant_power']:
    for v in range(1,5):
        p={'a':'2','b':v} if t=='constant_cos' else {'a':'2','n':v}
        records.append(A.G.generate('easy',seed=19073,template=t,parameters=p))
A.save('canonical-candidates.json',records)
matches=[r['question'][':question/id'] for r in records
         if A.S.simplify(A.normalized(A.prompt_equation(r)[1])-target)==0]
report={'source_id':'1e3c0253-226d-596c-a831-7c68ec76b21c','source_ma_id':'e-21741',
        'expected_equation':'dy/dx + 2y = 2 exp(-2x)',
        'expected_integrating_factor':'exp(2x)',
        'expected_final_equation':'d(y exp(2x))/dx = exp(2x) * 2 exp(-2x)',
        'candidate_count':len(records),'matching_ids':matches,'passed':bool(matches),
        'coverage_argument':__doc__,
        'rule_to_change':'Add a same-method constant-P exponential-forcing source family, with independent small parameters for P and Q, preserving the transformation-only task.'}
A.save('canonical-coverage-results.json',report)
print('PASS' if matches else 'FAIL: canonical source equation is unreachable')
sys.exit(0 if matches else 1)
