from audit_helpers import *
import author_regression as ar
from shortcut_probe import probe
old=json.load(open(ROOT.parent/'review-0-policy-2-707c0c642d91a260/batch-records.json'))
save('old-failing-batch.json',old)
new=json.load(open('batch-records.json'))
exact=g.generate('easy',3173462203,'slope_sqrt_radio',parameters={'a':7,'b':37,'t':-4})
save('exact-counterexample-current.json',[exact])
try:ar.check(old); negative=False
except AssertionError:negative=True
positive=ar.check(new); forced=ar.check([exact]);sample=ar.check(json.load(open('independent-samples.json')))
save('regression-results.json',{'author_script_sha256':hashlib.sha256((PKG/'checks/regression.py').read_bytes()).hexdigest(),'adaptation':'Only output destination redirected; check(records) function unchanged. Independently selected current 47-record sample rather than repeating author seeds.','negative_control_failed_as_required':negative,'old_results':[probe(r) for r in old if probe(r) is not None],'batch':positive,'forced':forced,'samples':sample})
assert negative
print('negative control rejected; current exact witness, batch and independent radios pass original spacing check')
