#!/usr/bin/env python3
"""Conditional cue probes for the repaired quotient banks, from served records.

Run before/after the shared delivery filter. Neither constructs nor grades keys.
Native grader cases use the actual cue's predicted answer UUID and math-checked key.
"""
import collections
import hashlib
import json
from pathlib import Path
import re
import validate as v

OUT = Path(__file__).resolve().parent/'evidence'


def probe(records):
    groups=collections.defaultdict(list)
    for r in records:
        if r['generation']['template']!='quotient':continue
        prompt=r['question'][':question/problem']
        denominator=int(re.search(r'}\{x\^\{(\d+)\}\}',prompt).group(1))
        p=r['generation']['parameters']['p']
        for group in ('all',f'denominator={denominator}',f'denominator={denominator}:p={p}'):
            groups[group].append(r)
    result={};cases=[]
    for group,rs in groups.items():
        scores=collections.Counter();targets=collections.Counter();pairings=set();polynomial_degrees=set()
        for r in rs:
            f=v.field(r);choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
            params=r['generation']['parameters'];targets[params['target']]+=1
            pairings.add(tuple(params['reciprocal_exponents']))
            values=[v.tex_expr(a[':answer/value']).subs(v.s.Symbol('C'),0).expand() for a in choices]
            exponents=[max(t.as_powers_dict().get(v.X,0) for t in v.s.Add.make_args(value)) for value in values]
            leading=[value.coeff(v.X**e) for value,e in zip(values,exponents)]
            # This is exactly the review's regex-based visible-exponent strategy.
            visible=[max([int(n) for n in re.findall(r'x\^\{(\d+)\}',a[':answer/value'])]+[1]) for a in choices]
            strategies={'largest_visible_exponent':max(range(5),key=lambda j:visible[j]),
                        'smallest_visible_exponent':min(range(5),key=lambda j:visible[j]),
                        'largest_polynomial_exponent':max(range(5),key=lambda j:exponents[j]),
                        'smallest_polynomial_exponent':min(range(5),key=lambda j:exponents[j]),
                        'largest_leading_coefficient':max(range(5),key=lambda j:leading[j]),
                        'smallest_leading_coefficient':min(range(5),key=lambda j:leading[j]),
                        'median_leading_coefficient':sorted(range(5),key=lambda j:leading[j])[2],
                        'first':0,'last':4,
                        'shortest':min(range(5),key=lambda j:len(choices[j][':answer/value'])),
                        'longest':max(range(5),key=lambda j:len(choices[j][':answer/value']))}
            for name,j in strategies.items():
                ok=choices[j][':answer/id']==correct;scores[name]+=int(ok)
                if group=='denominator=4' and name=='largest_visible_exponent':
                    cases.append({'label':'review shortcut '+r['question'][':question/id'], 'record':r,
                       'checks':[{'submitted_answer_id':choices[j][':answer/id'],
                                  'expected':'accepted' if ok else 'rejected',
                                  'purpose':'actual grader outcome for review largest-visible-exponent strategy'}]})
            polynomial_degrees.add(int(exponents[next(j for j,a in enumerate(choices) if a[':answer/id']==correct)]))
        result[group]={'records':len(rs),'target_counts':dict(targets),'pairing_count':len(pairings),
           'correct_polynomial_degrees':sorted(polynomial_degrees),
           'probes':{name:{'successes':score,'attempts':len(rs),'uniform_baseline':0.2} for name,score in scores.items()},
           'best_fixed_candidate':{'successes':max(targets.values()),'attempts':len(rs)}}
    return result,cases


def selection(records):
    # Conditional reproduction of question_selection.rs with all fresh candidates
    # moderate and positively weighted. Real database ID ordering is unavailable.
    ordered=sorted(records,key=lambda r:r['question'][':question/id']);n=len(ordered)
    # One representative deterministic draw per supplied candidate: this tests the
    # downstream uniform-index step, without suggesting these are live histories.
    selected=[]
    for index in range(n):
        digest=hashlib.sha256(f'course-academy/question-selection/v1/repair-{index}'.encode()).digest()
        uniform=(int.from_bytes(digest[8:16],'big') >> 11)/float(1<<53)
        selected.append(ordered[int(uniform*n)])
    return selected


def main():
    datasets={name:json.loads((OUT/path).read_text()) for name,path in {
       'before-controlled-and-normal':'test-records.json', 'before-normal':'normal-records.json',
       'after-controlled-and-normal':'delivery/accepted.json', 'after-normal':'delivery-normal/accepted.json'}.items()}
    datasets['after-conditional-selection']=selection(datasets['after-controlled-and-normal'])
    report={};cases=[]
    for name,rs in datasets.items():
        report[name],more=probe(rs);cases+=more
        for group,data in report[name].items():
            # Small random subgroups may be perfect by chance. Complete structural
            # cases must defeat every tested static cue in every denominator/p cell.
            if name in ('before-controlled-and-normal','after-controlled-and-normal'):
                # Source roles 1 and 2 have the identical polynomial component.
                # Delivery may deduplicate their exchanged reciprocal assignments.
                # Require every mathematical component, not both internal labels.
                assert {1 if t==2 else t for t in data['target_counts']}=={0,1,3,4},(name,group,data)
                assert all(p['successes']<p['attempts'] for p in data['probes'].values()),(name,group,data)
    raw=report['before-controlled-and-normal']['all']
    assert raw['pairing_count']==14
    fixed=[r for r in datasets['before-controlled-and-normal'] if r['generation']['template']=='quotient'
           and tuple(r['generation']['parameters'][k] for k in ('a','b','p'))==(2,3,4)]
    banks={tuple(sorted(a[':answer/value'] for a in v.field(r)[':answer-field/choices'])) for r in fixed}
    assert len(banks)==7
    v.save('conditional-shortcuts.json',{'passed':True,'datasets':report,
       'fixed_parameters':{'a':2,'b':3,'p':4,'distinct_unordered_banks':len(banks),
                           'internal_assignments':14,'note':'Exchanging identical polynomial components is not semantic variety.'},
       'scope':'All 14 reciprocal assignments x 5 targets x 3 p values, plus boundary and sampler regression.',
       'limitations':['No finite cue suite proves absence of every possible strategy.',
                     'Actual learner history, policy and database ID ordering are unavailable.',
                     'Reciprocal-exponent matching to the prompt is legitimate power-rule reasoning.']})
    v.save('shortcut-grader-input.json',cases)
    print(json.dumps({name:{k:report[name][k]['probes']['largest_visible_exponent']
         for k in ('all','denominator=4') if k in report[name]} for name in report}))


if __name__=='__main__':main()
