"""Regression for the review-3 singleton-row shortcut; no database writes."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import generator as G

OUT = Path(__file__).with_name('evidence') / 'singleton-repair'
OUT.mkdir(parents=True, exist_ok=True)
records = []
groups = []
for profile, exponents in [('P', (2,3,4,5,6)), ('R', (3,7))]:
    for n in exponents:
        for sign in (-1,1):
            group = []
            for row,col in ((0,1),(1,0),(1,1),(2,0),(2,1)):
                i = G.instance(profile,n,sign,4,offset=-2,second_offset=2,
                               omitted_row=row,omitted_col=col)
                record = G.build(i)
                integrand, correct, banks, key = G.mathematics(i)
                derivative = lambda terms: [(F(c)*F(p),F(p)-1) for c,p in terms]
                assert derivative(correct) == [(F(c),F(p)) for c,p in integrand]
                assert sum(derivative(b) == derivative(correct) for b in banks) == 1
                assert len(banks) == 5 and banks[key] == correct
                counts = Counter(b[0][0] for b in banks)
                singleton_correct = counts[correct[0][0]] == 1
                assert singleton_correct == (row == 0)
                group.append(singleton_correct)
                records.append(record)
            assert sum(group) == 1
            groups.append({'profile':profile,'exponent':n,'sign':sign,
                           'singleton_correct':sum(group),'omission_cases':len(group),
                           'eliminate_singleton_expected_success':'(4/5)*(1/4) = 1/5'})
try:
    G.instance('P',3,-1,4,offset=-2,second_offset=2,omitted_row=0,omitted_col=0)
except ValueError:
    pass
else:
    raise AssertionError('Must retain the correct choice')
sample = G.generate(count=600,seed=20261020)
for profile in ('P','R'):
    omissions = {tuple(r['generation']['parameters'][key] for key in ('omitted_row','omitted_col'))
                 for r in sample if r['generation']['template']==profile}
    assert omissions == {(0,1),(1,0),(1,1),(2,0),(2,1)}
(OUT/'records.json').write_text(json.dumps(records))
(OUT/'regression.json').write_text(json.dumps({'passed':True,'records':len(records),
    'groups':groups,'sample_count':len(sample),
    'limits':'Targets the demonstrated singleton cue. Independent review must recheck other cues and learner selection.'},indent=2))
cases=[]
for r in records:
    f=r['question'][':question/answer-fields'][0]
    correct=f[':answer-field/correct'][1]
    cases.append({'label':r['question'][':question/id'],'record':r,'checks':[
        {'field_index':0,'submitted_answer_id':a[':answer/id'],
         'expected':'accepted' if a[':answer/id']==correct else 'rejected'}
        for a in f[':answer-field/choices']]})
(OUT/'grader-input.json').write_text(json.dumps(cases))
print(json.dumps({'passed':True,'records':len(records),'groups':len(groups),'sample_count':len(sample)}))
