import copy
import json
from pathlib import Path
import re
import sys
import unittest
sys.dont_write_bytecode = True
import os
E = Path(__file__).resolve().parent
W = Path(os.environ.get("REVIEW_GENERATOR_ROOT", str(E.parent/"workspace")))
sys.path.insert(0, str(W))
import generator

def matrix(text):
    body = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)[1]
    return [[int(v.strip()) for v in row.split('&')] for row in body.split('\\\\')]

def coords(text):
    return [[int(i)-1, int(j)-1] for i,j in re.findall(r'a\}?_\{([1-4])([1-4])\}', text)]

def ref_after(m, cells):
    # Independent witness: all entries before each surviving pivot vanish;
    # each pivot column is zero in every lower row, and no internal zero row.
    a = copy.deepcopy(m)
    for i,j in cells: a[i][j] = 0
    zero_seen = False
    for i,row in enumerate(a):
        nonzero = [j for j,v in enumerate(row) if v != 0]
        if not nonzero:
            zero_seen = True
        else:
            if zero_seen: return False
            pivot = nonzero[0]
            if any(any(v != 0 for v in lower[:pivot+1]) for lower in a[i+1:]): return False
    return True

def check_record(r):
    q = r['question']; m = matrix(q[':question/problem'])
    f = q[':question/answer-fields'][0]; choices=f[':answer-field/choices']
    valid = [a[':answer/id'] for a in choices if ref_after(m, coords(a[':answer/value']))]
    assert valid == [f[':answer-field/correct'][1]], valid
    assert not any(x in q[':question/problem'].lower() for x in ['fewest','minimum'])
    selected = next(a for a in choices if a[':answer/id']==valid[0])
    solution=q[':question/worked-solution']
    assert coords(solution.split(':')[0]) == coords(selected[':answer/value'])
    rendered = re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',solution,re.S)
    assert len(rendered)==2
    transformed = copy.deepcopy(m)
    for i,j in coords(selected[':answer/value']): transformed[i][j]=0
    assert matrix('\\begin{bmatrix}'+rendered[-1]+'\\end{bmatrix}')==transformed
    return valid[0]

class SourceContract(unittest.TestCase):
    def test_complete_q73149_bank_accepts_already_zero_distractor(self):
        case=next(x for x in json.loads((E/'source-replay.json').read_text()) if x['source_id']=='5da4a360-a207-5df6-9d38-99e7b8b5a765')
        r=generator.generate('moderate',9100,parameters=case['parameters'])
        check_record(r)
        bank=[coords(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
        self.assertEqual(bank,case['parameters']['bank'])
        self.assertIn([[1,0],[2,0]],bank)
    def test_valid_offered_operation_need_not_be_globally_minimum(self):
        case=json.loads((E/'nonminimum-case.json').read_text())
        p=case['parameters']; self.assertTrue(ref_after(p['matrix'],[[1,0],[3,2]]))
        r=generator.generate('moderate',case['seed'],parameters=p);check_record(r)
        q=r['question'];f=q[':question/answer-fields'][0]
        selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        self.assertEqual(coords(selected[':answer/value']),[[0,1],[1,0],[3,2]])
        self.assertNotIn('minimum',q[':question/worked-solution'].lower())
    def test_prompt_does_not_add_optimization(self):
        check_record(generator.generate('moderate',702311))

if __name__=='__main__': unittest.main()
