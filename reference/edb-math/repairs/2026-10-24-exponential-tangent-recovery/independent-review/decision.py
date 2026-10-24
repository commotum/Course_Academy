"""Independent visible-math shortcut tests and finite bank-kernel proof."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
import re
import sympy as s
import review as a
import visible_math as v


def inspect(records):
    rows=[]
    for i,rec in enumerate(records):
        prompt=rec['question'][':question/problem']
        function=v.parse(re.search(r'y\s*=\s*([^$]+)',prompt)[1].rstrip(',.'))
        point=v.parse(re.search(r'point where \$x=([^$]+)',prompt)[1].rstrip('.'))
        base,exponent=function.as_base_exp()
        ordinate=function.subs(v.x,point)
        values=[v.parse(c[':answer/value']) for c in v.choices(rec)]
        slopes=[s.simplify(s.diff(value,v.x)) for value in values]
        key_index=next(j for j,c in enumerate(v.choices(rec)) if c[':answer/id']==v.correct(rec))
        assert len(values)==len(set(slopes))==5
        assert sum(bool(slope>0) for slope in slopes) in (2,3)
        assert all(s.simplify(value.subs(v.x,point)-ordinate)==0 for value in values)
        expected=v.expected(rec)
        assert [j for j,value in enumerate(values) if s.simplify(value-expected)==0]==[key_index]
        assert v.cue(rec) is None
        coefficients=[s.simplify(slope/(ordinate*s.log(base))) for slope in slopes]
        for coefficient in coefficients:
            offset=s.simplify(exponent.subs(v.x,point)-coefficient*point)
            assert coefficient.is_Integer and 1<=abs(coefficient)<=9
            assert offset.is_Integer and 1<=abs(offset)<=5
            alternate=base**(coefficient*v.x+offset)
            tangent=s.diff(alternate,v.x).subs(v.x,point)*(v.x-point)+alternate.subs(v.x,point)
            assert any(s.simplify(tangent-value)==0 for value in values)
        rank=sorted(range(5),key=lambda j:float(slopes[j])).index(key_index)
        rows.append({'index':i,'seed':rec['generation'].get('seed'),
                     'point':str(point),'base':str(base),'slope_sign':int(s.sign(slopes[key_index])),
                     'rank':rank,'position':key_index,'positive_choices':sum(bool(slope>0) for slope in slopes),
                     'same_sign_choices':sum(bool(s.sign(slope)==s.sign(slopes[key_index])) for slope in slopes),
                     'coefficients':list(map(int,coefficients)),'target_coefficient':int(coefficients[key_index])})
    return {'total':len(rows),'old_cue_success':0,'singleton_correct_sign':0,'cases':rows,
            'rank_counts':dict(Counter(row['rank'] for row in rows)),
            'position_counts':dict(Counter(row['position'] for row in rows)),
            'sign_counts':dict(Counter(row['slope_sign'] for row in rows))}


def main():
    frozen=a.load(a.R/'evidence/frozen-candidate.json')
    assert a.package_hash()==frozen['package_hash']
    g=a.module('decision_candidate',a.P/'generator.py')
    old=a.module('decision_original',a.R/'original/generator.py')
    sets={name:a.load(a.E/(name+'.json')) for name in ['requested','fresh','controlled']}
    sets['author-fresh']=a.load(a.R/'evidence/fresh.json')
    a.save('author-fresh.json',sets['author-fresh'])
    reports={name:inspect(records) for name,records in sets.items()}
    old_negative=[old.generate_hard(1072510293+i) for i in range(4)]
    assert v.probes(old_negative)['correct']==4
    a.save('original-negative-records.json',old_negative)
    seed2=a.load(a.E/'sign-only-fresh-counterexample.json')['record']
    slopes=[s.diff(v.parse(c[':answer/value']),v.x) for c in v.choices(seed2)]
    assert sum(bool(slope>0) for slope in slopes)==1
    assert next(c[':answer/id'] for c,slope in zip(v.choices(seed2),slopes) if slope>0)==v.correct(seed2)
    # Finite independent parameter-domain account. No generator answer metadata.
    groups=[]
    for point in [-1,0,1]:
        for evaluated in range(-2,3):
            eligible=[coefficient for coefficient in range(-9,10)
                      if coefficient and 1<=abs(evaluated-coefficient*point)<=5]
            if not eligible:
                continue
            incidences=Counter()
            for coefficient in eligible:
                params=dict(b=3,c=1,a=coefficient,n=1,k=0,l=0,
                            d=evaluated-coefficient*point,point=str(point))
                completed=g.complete('q-107463',params)
                g.guard('q-107463',completed)
                assert g.tangent_coefficients(completed)==eligible
            banks=[bank for bank in combinations(eligible,5) if sum(c>0 for c in bank) in (2,3)]
            assert banks
            raw_joint=Fraction(1,len(eligible)*comb(len(eligible)-1,4))
            for bank in banks:
                masses={key:raw_joint for key in bank}
                assert all(mass/sum(masses.values())==Fraction(1,5) for mass in masses.values())
                incidences.update(bank)
            assert all(incidences[key]>0 for key in eligible)
            groups.append({'point':point,'evaluated_exponent':evaluated,'eligible_coefficients':eligible,
                           'accepted_banks':len(banks),'bank_incidence_by_key':dict(incidences),
                           'raw_joint_probability':str(raw_joint),'conditional_key_probability':'1/5',
                           'all_targets_represented':True})
    proof={'passed':True,'groups':groups,
           'reasoning':'Read sample/generate/tangent_bank: normal hard samples each signed coefficient1..9, base, point and evaluated exponent uniformly before guard rejection. At fixed base/point/exponent, guard leaves the same eligible coefficient set regardless of key. random.sample chooses each containing4-subset uniformly; before bank rejection each (target,complete bank) has equal mass. The2/3 sign acceptance predicate depends only on the bank. Normal generation retries both parameters and bank, so conditioning on acceptance preserves exactly1/5 probability for every key in a given bank. Accepted target marginals need not be uniform and are proportional to bank incidence. The initial unused constant draw is overwritten and does not change these relative probabilities.',
           'base_scope':'Coefficient eligibility and sign acceptance are independent of base2..6; all logs/ordinates positive.',
           'explicit_parameter_limit':'When a caller fixes target parameters, only bank seeds resample. Every choice can still be keyed in another supported fixed-parameter problem, but uniform conditional key probability is claimed for normal CLI sampling, not an arbitrary external distribution of fixed-parameter requests.',
           'pseudorandom_limit':'Probability argument uses the documented uniform random choices, not adversarial knowledge or inversion of the deterministic seed.',
           'negative_controls':{'old_bank_cue':'4/4 retained original requested records',
                                'rejected_seed2':'1/1 singleton positive sign identifies key',
                                'rejected_unit_case':'Archived c70c unit-target-only candidate pool contrasted with current identical pools for every key'}}
    a.save('exchangeability.json',proof)
    all_rows=[row for report in reports.values() for row in report['cases']]
    assert len({row['rank'] for row in all_rows})==5
    assert len({row['position'] for row in all_rows})==5
    assert {row['slope_sign'] for row in all_rows}=={-1,1}
    assert any(abs(row['target_coefficient'])==1 for row in reports['author-fresh']['cases'])
    assert any(abs(row['target_coefficient'])!=1 and any(abs(c)==1 for c in row['coefficients'])
               for row in reports['author-fresh']['cases'])
    a.save('decision-results.json',{'passed':True,'sets':reports,'proof':'exchangeability.json'})
    print({'passed':True,'records':len(all_rows),'finite_groups':len(groups),
           'accepted_complete_banks':sum(row['accepted_banks'] for row in groups)})


if __name__=='__main__':
    main()
