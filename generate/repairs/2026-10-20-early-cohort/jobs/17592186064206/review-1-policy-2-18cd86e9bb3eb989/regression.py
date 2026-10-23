"""Strict acceptance regression: current package is expected to FAIL.
Run with the repository venv Python. Accepts prospective candidate files.
"""
import argparse, json, pathlib, sys
sys.dont_write_bytecode=True
import audit
p=argparse.ArgumentParser()
p.add_argument('--package',default=str(audit.JOB/'workspace'))
p.add_argument('--candidate-records',default=str(audit.ROOT/'delivery-batch/accepted.json'))
p.add_argument('--output',default='regression-results.json')
a=p.parse_args();m=audit.load(a.package)
tests=[]
try:
    r=m.generate(seed=8301,parameters=[3,5,2])
    tests.append({'test':'canonical positive-slope parameters [3,5,2] supported','passed':True,'record':r})
except Exception as e:
    tests.append({'test':'canonical positive-slope parameters [3,5,2] supported','passed':False,'error':repr(e)})
records=audit.read(a.candidate_records);probe=audit.probe(records)
tests.append({'test':'candidate batch cannot all be answered from bank-only cue','passed':probe['correct']<probe['total'],'input':a.candidate_records,'probe':probe})
sample=[m.generate(seed=i) for i in range(46391,46431)]
probe=audit.probe(sample)
tests.append({'test':'fresh sample cannot all be answered from bank-only cue','passed':probe['correct']<probe['total'],'seeds':[46391,46430],'probe':probe})
audit.save(a.output,tests)
print(json.dumps([{'test':t['test'],'passed':t['passed']} for t in tests]))
sys.exit(0 if all(t['passed'] for t in tests) else 1)
