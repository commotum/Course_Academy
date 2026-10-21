"""Retained finding 74d7bc6e85b704fc3ba0: native grading of visible +C scaffolds.

No runtime edits or service/database access. Independent derivative witnesses
read the displayed ODE and scaffold; the real application grades all responses.
"""
from audit_support import *

E.mkdir(exist_ok=True)
records = [g.generate('easy', 1504545805, 'q-126765', {'h': h}) for h in range(-4, 5)]
exact = next(r for r in records if r['generation']['parameters']['h'] == 3)
retained = json.loads((E/'before-input.json').read_text())[0]['record']
assert exact['question'][':question/problem'] == retained['question'][':question/problem']
assert correct(exact) == correct(retained)
assert exact['generation'] == retained['generation']

def checks_for(r):
    prompt = r['question'][':question/problem']
    assert r'\sin(\boxed{\text{expression}}+C)' in prompt
    assert 'Expression: {{field-1}}' in prompt
    assert r'-\pi/2<\theta<\pi/2' in prompt
    ode = re.search(r"\$y'=(.*?)\$", prompt)[1]
    rhs = expr(ode.replace(r'\sqrt', r'*\sqrt'))
    forcing = simplify(rhs/S.sqrt(1-y*y))
    key = expr(correct(r))
    assert simplify(S.diff(key, x)-forcing) == 0
    # Numerical values are derived from the rendered key, not generation metadata.
    valid = [key, S.expand(key), key+1, key-S.Rational(2,3), key+S.pi]
    invalid = [2*key, key+x, key**2, S.Integer(0)]
    cases = []
    for accepted, values in [(True, valid), (False, invalid)]:
        for value in values:
            same_derivative = simplify(S.diff(value, x)-forcing) == 0
            assert bool(same_derivative) == accepted, str(value)
            cases.append({'submitted': str(value).replace('**','^'),
                          'expected': 'accepted' if accepted else 'rejected',
                          'purpose': 'Independent displayed-ODE derivative witness; constants reparameterize C and its local branch'})
    cases.append({'submitted': '('+correct(r)+')+x/x', 'expected': 'unresolved',
                  'purpose': 'Extra domain restriction must not be silently accepted'})
    return cases

save('sine-records.json', records)
delivery = E/'delivery-sine'
cmd = [sys.executable, str(ROOT/'generate/pipeline/check_delivery.py'), '--input', str(E/'sine-records.json'),
       '--source', str(JOB/'source/source.json'), '--inventory', str(JOB/'source/inventory.json'),
       '--difficulty', 'easy', '--output', str(delivery), '--asset-root', str(E),
       '--math-root', '/media/jake/SSD/EDB/math']
p = subprocess.run(cmd, capture_output=True, text=True)
(E/'sine-delivery-console.txt').write_text(p.stdout+p.stderr)
assert p.returncode == 0, p.stdout+p.stderr
accepted = json.loads((delivery/'accepted.json').read_text())
assert len(accepted) == len(records), 'Changed family coverage lost in delivery'
delivered_exact = next(r for r in accepted if r['generation']['parameters']['h'] == 3)
assert delivered_exact['question'] == retained['question']
assert delivered_exact['question'][':question/id'] == 'a5b2a220-0459-5dce-b547-6284c446511b'
cases = [{'label': stage+' '+str(r['generation']['parameters']), 'record': r, 'checks': checks_for(r)}
         for stage, rs in [('raw',records),('delivered',accepted)] for r in rs]
# Preserve both literal entries from the independent review, not just equivalents
# serialized by SymPy, plus the explicitly requested derivative-distinct negative.
cases.append({'label':'exact retained delivered counterexample', 'record':retained, 'checks':[
    {'submitted':'x^2-6*x','expected':'accepted'},
    {'submitted':'(x-3)^2+1','expected':'accepted'},
    {'submitted':'2*(x-3)^2','expected':'rejected'}]})
save('sine-grader-input.json', cases)
grade = [str(ROOT/'generate/runs/current/check-engine'), str(E/'sine-grader-input.json'), str(E/'sine-grader-report.json')]
p = subprocess.run(grade, capture_output=True, text=True)
(E/'sine-grader-console.txt').write_text(p.stdout+p.stderr)
assert p.returncode == 0, p.stdout+p.stderr
# A canonical record demonstrates the stored-ID reproduction explicitly.
save('sine-reproduction.json', {'finding':'74d7bc6e85b704fc3ba0', 'template':'q-126765',
     'seed':1504545805, 'parameters':{'h':3}, 'question_id':delivered_exact['question'][':question/id'], 'raw_question_id':exact['question'][':question/id'],
     'visible_key':correct(exact), 'matches_review_record':True, 'commands':[cmd,grade],
     'raw_h': [r['generation']['parameters']['h'] for r in records],
     'delivered_h': [r['generation']['parameters']['h'] for r in accepted],
     'proof':'All accepted fragments have derivative equal to the rendered ODE forcing. Their constant differences are absorbed by C -> C-d; the local branch condition is expressed in the full sine argument. All rejected fragments have a different derivative.',
     'shortcut':'Constant offsets and expanded/factored spelling are irrelevant evidence; derivative changes are relevant. Both preserve their expected outcomes after the real delivery filter.',
     'domain_limit':'x/x adds a restriction and remains an explicit unresolved comparison, never accepted.',
     'native_checks':sum(len(c['checks']) for c in cases), 'status':'passed'})
print(p.stdout.strip())
print('All nine shifts, exact review entries and delivery controls passed.')
