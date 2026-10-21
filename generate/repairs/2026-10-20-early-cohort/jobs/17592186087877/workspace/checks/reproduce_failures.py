"""Strict regression: exits 1 when the easy bank alone reveals its key.

Run: /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_failures.py
The ODE, solutions, metadata and stored keys are hidden from the predictor.
"""
import sys
import audit as A

records=[A.G.generate('easy',seed=8173,template='signed_constant_power',
    parameters={'a':a,'n':2}) for a in ['1','-1']]
A.save('minimal-failing-records.json',records)
outcomes=[]
for r in records:
    predicted=A.shortcut(r)
    outcomes.append({'question_id':r['question'][':question/id'],
        'prediction':predicted,'stored_key':A.key(r),'success':predicted==A.key(r)})
report={'test':'An answer-bank-only double-exponent cue must not identify the correct factor in both opposite-sign cases.',
        'outcomes':outcomes,'passed':not all(x['success'] for x in outcomes),
        'rule_to_change':'All easy templates share [I,1/I,I^2,x,x^2]; I is uniquely recoverable without the ODE. Break that fixed bank-to-key association across legitimate cases; keep the ODE skill, five complete options and unique correctness.'}
A.save('minimal-failure-results.json',report)
print('FAIL: bank-only cue identifies both answers' if not report['passed'] else 'PASS: cue no longer identifies both answers')
sys.exit(0 if report['passed'] else 1)
