"""A valid boundary counterfactual must be generatable with the complete 2x2 radio bank.
Usage: .venv/bin/python reproduce_restriction.py /absolute/path/to/17592186100989.py
Expected to fail on the reviewed package, not to bless the exception.
"""
import sys,importlib.util,json,pathlib
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('candidate',sys.argv[1]);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p={'name':'B','matrix':[['1','-3'],['0','5']],'i':3,'j':2}
before=g.generate_easy(seed=11,profile='all_four',parameters=p)
# Same bank already has all four cells and No such entry; no extra prerequisite required.
after=g.generate_easy(seed=11,profile='all_four',parameters=p|{'i':2})
def answer(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
assert answer(before)=='No such entry'
assert answer(after)=='5'
print('Boundary counterfactual accepted and keys correct.')
