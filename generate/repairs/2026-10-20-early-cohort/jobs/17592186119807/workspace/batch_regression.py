"""Retained reviewer finite-pool acceptance test; inspect visible choices and key.
Run: <context-python> batch_regression.py
Positive control: <context-python> batch_regression.py --records controlled-records.json
"""
import json,re,pathlib,argparse,sys
from fractions import Fraction
p=argparse.ArgumentParser();p.add_argument('--records',default='evidence/delivery-batch/accepted.json');a=p.parse_args()
rs=json.loads((pathlib.Path(__file__).resolve().parent/a.records).read_text())
def n(x):return Fraction(re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'\1/\2',re.sub(r'\s+','',x)))
def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
sub=[r for r in rs if any(n(c[':answer/value'])<=0 for c in r['question'][':question/answer-fields'][0][':answer-field/choices'] if c[':answer/type']==':answer.type/math')]
assert sub,'Test needs the recognizable nonpositive numeric-bank subgroup'
assert any(key(r)!='No solution' for r in sub), ('BATCH SHORTCUT: choose No solution for a bank containing a nonpositive numeric option: '+str(len(sub))+'/'+str(len(sub))+'. See batch-sign-reproduction.json for complete records and exact seeds/parameters.')
print('PASS: nonpositive numeric-bank subgroup contains a counterexample to the shortcut')
