"""Strict failing acceptance cases; no package or database writes.

Run: .venv/bin/python regression.py source
     .venv/bin/python regression.py batch
"""
import json,sys
from audit import E,P,load_generator,correct
def source():
    g=load_generator()
    # Source has an unambiguous I-only key and a complete worked solution.
    r=g.generate(template='q-142367',replay=True)
    f=r['question'][':question/answer-fields'][0]
    assert correct(f)=='I only'
    assert len(f[':answer-field/choices'])==5
def batch():
    rows=json.load(open(E/'delivery-batch/accepted.json'))
    sub=[r for r in rows if len(r['question'][':question/answer-fields'])==3]
    def cue_succeeds(r):
        return all((correct(f)=='true')==('invertible' in f[':answer-field/key']) for f in r['question'][':question/answer-fields'])
    assert len(sub)>=2
    assert not all(cue_succeeds(r) for r in sub), 'Select only the invertibility claim answers all recurring three-option checkbox items without inspecting the given.'
if __name__=='__main__':
    {'source':source,'batch':batch}[sys.argv[1]]()
