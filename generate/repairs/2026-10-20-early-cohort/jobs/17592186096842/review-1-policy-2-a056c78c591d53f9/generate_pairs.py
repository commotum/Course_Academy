"""Recreate controlled pairs and exact renderer inputs after audit.py."""
from audit_helpers import *
cf=json.load(open(ROOT/'counterfactual-records.json'))[:5]
for t in [-4,-3]:
    cf.append(g.generate('easy',seed=3173462203,template='slope_sqrt_radio',parameters={'a':7,'b':37,'t':t}))
save('counterfactual-records.json',cf)
records=cf+json.load(open(ROOT/'batch-records.json'))+[r for r in json.load(open(ROOT/'independent-samples.json')) if r['generation']['template']=='reciprocal_radio'][:1]
save('render-records.json',records)
save('render-extra-records.json',records[6:])
save('independent-easy.json',[r for r in json.load(open(ROOT/'independent-samples.json')) if r['question'][':question/difficulty'].endswith('/easy')])
