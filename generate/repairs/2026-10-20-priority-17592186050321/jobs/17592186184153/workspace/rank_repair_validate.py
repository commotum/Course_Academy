"""Review-2 targeted repair checks; job Python -B, then --after-delivery.

Reuses the retained independent TeX parser, exact checks and grader cases.
No publishing or database operations. Current evidence: evidence/repair-3.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
from itertools import permutations, combinations
import json
from math import comb
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import generator as G
import validate as T

OUT = Path('evidence/repair-3')
OUT.mkdir(exist_ok=True)
T.OUT = OUT


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def field(r):
    return r['question'][':question/answer-fields'][0]


def displayed(r):
    """Extract both coefficients from actual answer text, without bank metadata."""
    i = r['generation']['parameters']
    x = T.V[i['variable']]
    p = -T.S.Rational(i['n'], 2) if i['profile'] == 'R' else T.S.Integer(i['n'])
    rows = []
    for a in field(r)[':answer-field/choices']:
        value = T.S.expand(T.tex(a[':answer/value']) - T.V['C'])
        rows.append(dict(id=a[':answer/id'], linear=str(value.coeff(x, 1)),
                         power=str(value.coeff(x**(p+1))), length=len(a[':answer/value'])))
    return rows


def probes(records):
    trials = []
    for r in records:
        i = r['generation']['parameters']
        if i['profile'] == 'B':
            continue
        rows = displayed(r)
        target = field(r)[':answer-field/correct'][1]
        correct = next(row for row in rows if row['id'] == target)
        constant_matched = [row for row in rows if row['linear'] == str(i['k'])]
        coefficient_matched = [row for row in rows if row['power'] == correct['power']]
        assert len(constant_matched) == 2 and len(coefficient_matched) >= 2
        assert len({row['length'] for row in constant_matched}) == 1
        # Relevant structural number types cannot distinguish the two options.
        assert len({F(row['power']).denominator==1 for row in constant_matched})==1
        assert len({abs(F(row['power']))<1 for row in constant_matched})==1
        frequency = Counter(row['power'] for row in rows)
        strategies = {
            'constant_then_max_magnitude': max(constant_matched, key=lambda z: abs(F(z['power']))),
            'constant_then_min_magnitude': min(constant_matched, key=lambda z: abs(F(z['power']))),
            'constant_then_median_or_first': sorted(constant_matched,key=lambda z:abs(F(z['power'])))[1] if len(constant_matched)==3 else constant_matched[0],
            'constant_then_most_frequent_power': max(constant_matched, key=lambda z: frequency[z['power']]),
            'constant_then_least_frequent_power': min(constant_matched, key=lambda z: frequency[z['power']]),
            'constant_then_shortest': min(constant_matched, key=lambda z: z['length']),
            'constant_then_longest': max(constant_matched, key=lambda z: z['length']),
        }
        polynomial = i['profile'] == 'P'
        if polynomial:
            assert len(constant_matched) == 2
            assert len({row['length'] for row in constant_matched}) == 1
            assert all(abs(F(row['power'])).numerator == 1 and 2 <= abs(F(row['power'])).denominator <= 9 for row in rows)
        elif i['n']==3:
            assert all(abs(F(row['power'])).denominator==1 and 1<=abs(F(row['power']))<=6 for row in rows)
        else:
            assert all(abs(F(row['power'])).numerator==2 and abs(F(row['power'])).denominator in (3,5,7,9) for row in rows)
        trials.append(dict(id=r['question'][':question/id'], profile=i['profile'], n=i['n'],
                           s=i['s'], ksign=1 if i['k'] > 0 else -1, order=i['constant_first'],
                           position=rows.index(correct), constant_candidates=len(constant_matched),
                           power_candidates=len(coefficient_matched),
                           magnitude_rank=sorted({abs(F(z['power'])) for z in constant_matched}).index(abs(F(correct['power']))),
                           correct_power_frequency=frequency[correct['power']],
                           conditional_length_tie=len({row['length'] for row in constant_matched}) == 1,
                           cue_selected={k:v['id'] for k,v in strategies.items()},
                           wins={k:v['id']==target for k,v in strategies.items()},
                           raw_length_rank=sorted(range(5),key=lambda j:rows[j]['length']).index(rows.index(correct))))
    groups = defaultdict(list)
    for t in trials:
        keys=[t['profile'], f"{t['profile']}:n={t['n']}",
              f"{t['profile']}:s={t['s']}:ksign={t['ksign']}:order={t['order']}",
              f"{t['profile']}:n={t['n']}:s={t['s']}:order={t['order']}"]
        for k in keys:
            groups[k].append(t)
    summary = {}
    for name, ts in groups.items():
        wins = {key:sum(t['wins'][key] for t in ts) for key in ts[0]['wins']}
        summary[name] = dict(attempts=len(ts), conditional_baseline=sum(1/t['constant_candidates'] for t in ts)/len(ts),
                             wins=wins, positions=dict(Counter(t['position'] for t in ts)),
                             length_ranks=dict(Counter(t['raw_length_rank'] for t in ts)),
                             magnitude_ranks=dict(Counter(t['magnitude_rank'] for t in ts)),
                             power_frequencies=dict(Counter(t['correct_power_frequency'] for t in ts)))
        # On sufficiently populated exponent groups, assess the reported cue
        # against its exact conditional .5 null (not an arbitrary balance quota).
        if name.startswith('P:n=') and ':s=' not in name:
            w=wins['constant_then_max_magnitude']; n=len(ts)
            summary[name]['max_rank_two_sided_binomial_p']=min(1, 2*sum(comb(n,j) for j in range(min(w,n-w)+1))/2**n)
            assert summary[name]['max_rank_two_sided_binomial_p'] > .01
    return dict(strategy='After integrating constant, choose by coefficient magnitude/frequency/length; first displayed tie.',
                baseline='Uniform among constant-matched options; polynomial exactly 1/2.',
                groups=summary, trials=trials)


def coverage(records):
    result={}
    for profile in ('P','R','B'):
        rs=[r for r in records if r['generation']['template']==profile]
        items=[r['generation']['parameters'] for r in rs]
        c=dict(records=len(rs), semantics=len({T.semantic(r) for r in rs}),
               n=sorted({i['n'] for i in items}), s=sorted({i['s'] for i in items}),
               k=sorted({i['k'] for i in items}), order=sorted({i['constant_first'] for i in items}),
               variables=sorted({i['variable'] for i in items}))
        assert c['n']==([3,7] if profile=='R' else [2,3,4,5,6])
        assert c['s']==[-1,1] and c['order']==[False,True]
        assert c['k']==[*range(-6,0),*range(1,7)]
        if profile=='P':
            c['divisors']=sorted({int(F(i['n']+1)/F(i['factors'][0])) for i in items})
            c['omissions']=sorted({(i['omitted_row'],i['omitted_col']) for i in items})
            c['constant_ranks']=dict(Counter(int(i['offset']<0)+int(i['second_offset']<0) for i in items))
            c['wrong_coefficient_side']=dict(Counter('above' if F(i['factors'][0])>1 else 'below' for i in items))
            assert c['divisors']==list(range(2,10)) and len(c['omissions'])==4
            assert set(c['constant_ranks'])=={0,1,2}
        if profile=='R':
            c['omissions']=sorted({(i['omitted_row'],i['omitted_col']) for i in items})
            assert len(c['omissions'])==4
        if profile!='B':
            c['correct_positions']=dict(Counter(next(j for j,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==field(r)[':answer-field/correct'][1]) for r in rs))
            assert set(c['correct_positions'])==set(range(5))
        result[profile]=c
    result['semantic_instances']=len({T.semantic(r) for r in records})
    return result


def exact_domain():
    counts=Counter(); printed=[]; probability={}
    for n in range(2,7):
        ds=[d for d in range(2,10) if d!=n+1]
        # Two-sided role choice is independent of k, sign/order and omission.
        probability[n]={'above_divisors':[d for d in ds if d<n+1],
                        'below_divisors':[d for d in ds if d>n+1],
                        'side_probability':'1/2 each', 'maximum_strategy_expected_success':'1/2'}
        assert all(probability[n][key] for key in ('above_divisors','below_divisors'))
        for d in ds:
            for row in (1,2):
                for col in (0,1):
                    for s in (-1,1):
                        for offsets in ((-2,-1),(-1,1),(1,2)):
                            i=G.instance('P',n,s,4,offset=offsets[0],second_offset=offsets[1],factors=[str(F(n+1,d))],omitted_row=row,omitted_col=col)
                            _, answer, banks, ci=G.mathematics(i)
                            assert len(banks)==5
                            hits=[]
                            for terms in banks:
                                derivative={F(p)-1:F(c)*F(p) for c,p in terms}
                                hits.append(derivative=={F(0):F(4),F(n):F(s)})
                            assert hits==[j==ci for j in range(5)]
                            assert len({tuple((str(c),str(p)) for c,p in terms) for terms in banks})==5
                            assert sum(F(b[0][0])==4 for b in banks)==2
                            assert sum(F(b[1][0])==F(s,n+1) for b in banks) in (2,3)
                            counts[n]+=1
                            if row==1 and col==0 and s==1 and offsets==(-1,1):
                                r=G.build(i,random.Random(d));T.verify(r);printed.append(r)
    # Offset compatibility and constant ranks at every boundary, without expanding
    # unrelated exponent/sign combinations.
    offset_cases=0
    for k in (*range(-6,0),*range(1,7)):
        ranks=set()
        for a,b in permutations([d for d in (-3,-2,-1,1,2,3) if k+d!=0],2):
            i=G.instance('P',2,1,k,offset=a,second_offset=b)
            assert len({k,k+a,k+b})==3 and all((k,k+a,k+b))
            ranks.add(int(a<0)+int(b<0));offset_cases+=1
        assert ranks=={0,1,2}
    reciprocal_banks=0
    for n in (3,7):
        for factor in G.factor_domain('R',n):
            for row,col in ((1,0),(1,1),(2,0),(2,1)):
                for s in (-1,1):
                    i=G.instance('R',n,s,4,factors=[factor],omitted_row=row,omitted_col=col)
                    _,_,banks,ci=G.mathematics(i)
                    target={F(0):F(4),F(-n,2):F(s)}
                    assert [dict((F(p)-1,F(c)*F(p)) for c,p in b)==target for b in banks]==[j==ci for j in range(5)]
                    reciprocal_banks+=1
                    if row==1 and col==0 and s==1:
                        T.verify(G.build(i,random.Random(5)))
    save('exact-domain.json',dict(exact_banks=sum(counts.values()),per_exponent=dict(counts),independently_parsed_banks=len(printed)+8,offset_assignments=offset_cases,analytical_sampling=probability,reciprocal_banks=reciprocal_banks,reciprocal_sampling='First choose wrong coefficient side with probability 1/2. Correct frequency 2 or 3 independently, each probability 1/2.',passes=True))


def controls():
    pairs=[]; records=[]
    # Identical integrands: change only magnitude side and omission frequency.
    for n in range(2,7):
        for s,order in ((1,True),(-1,False)):
            for col in (0,1):
                base=G.instance('P',n,s,4,constant_first=order,offset=-1,second_offset=1,factors=[str(F(n+1,2))],omitted_col=col)
                a=G.build(base,random.Random(5));b=G.build(base|{'factors':[str(F(n+1,9))]},random.Random(5))
                for r in (a,b):T.verify(r)
                assert T.correct_value(a)==T.correct_value(b)
                assert a['question'][':question/problem']==b['question'][':question/problem']
                assert a['question'][':question/worked-solution']==b['question'][':question/worked-solution']
                records.extend((a,b));pairs.append(dict(change='wrong coefficient above/below',base=a,changed=b,predicted='same prompt/solution/key; opposite conditional rank'))
    base=G.instance('P',3,1,4,offset=-1,second_offset=1,factors=['2'])
    a=G.build(base,random.Random(5));T.verify(a)
    for change in ({'n':5,'factors':['3']},{'s':-1},{'k':-4},{'constant_first':False},{'variable':'y'}):
        b=G.build(base|change,random.Random(5));T.verify(b)
        if set(change)&{'n','s','k'}:
            assert T.S.simplify(T.tex(T.correct_value(a))-T.tex(T.correct_value(b)))!=0
        elif 'constant_first' in change:
            assert T.S.simplify(T.tex(T.correct_value(a))-T.tex(T.correct_value(b)))==0
        else:
            assert T.S.simplify(T.tex(T.correct_value(a)).subs(T.V['x'],T.V['y'])-T.tex(T.correct_value(b)))==0
        records.append(b);pairs.append(dict(change=change,base=a,changed=b))
    reordered=G.build(base,random.Random(17))
    assert T.correct_value(a)==T.correct_value(reordered)
    records.extend((a,reordered))
    for n in (3,7):
        for s,order in ((1,True),(-1,False)):
            for col in (0,1):
                below=next(f for f in G.factor_domain('R',n) if f<1)
                above=next(f for f in G.factor_domain('R',n) if f>1)
                i=G.instance('R',n,s,4,constant_first=order,offset=-1,second_offset=1,factors=[str(below)],omitted_col=col)
                a=G.build(i,random.Random(5));b=G.build(i|{'factors':[str(above)]},random.Random(5))
                for r in (a,b):T.verify(r)
                assert T.correct_value(a)==T.correct_value(b)
                assert a['question'][':question/problem']==b['question'][':question/problem']
                assert a['question'][':question/worked-solution']==b['question'][':question/worked-solution']
                records.extend((a,b));pairs.append(dict(change='R competitor side, prompt/solution/key preserved',base=a,changed=b))
    save('controls.json',records);save('counterfactuals.json',pairs)
    return records


def runtime():
    manifest=json.loads(Path('package.json').read_text())
    assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{}}
    a=G.generate(count=5,seed=84153);assert a==G.generate(count=5,seed=84153)
    save('sample.json',a)
    with tempfile.TemporaryDirectory(prefix='rank-repair-',dir=OUT.resolve()) as directory:
        for f in manifest['files']:shutil.copy(f,directory)
        cmd=[sys.executable,'-B','generator.py','--difficulty','moderate','--count','5','--seed','84153','--format','json']
        p=subprocess.run(cmd,cwd=directory,text=True,capture_output=True,check=True)
        assert json.loads(p.stdout)==a
    for band in ('easy','hard'):
        try:G.generate(band,1,0)
        except ValueError:pass
        else:raise AssertionError(band)
    invalid=[{'second_offset':1,'offset':1},{'second_offset':-4},{'omitted_row':0},{'omitted_col':2},{'factors':['1']},{'factors':['2','4/3']}]
    for change in invalid:
        try:G.instance('P',3,1,4,**change)
        except ValueError:pass
        else:raise AssertionError(change)
    try:G.instance('R',5,1,4)
    except ValueError:pass
    else:raise AssertionError('excluded R5 extension')
    return dict(version=G.VERSION,python=sys.version.split()[0],determinism=True,relocation=True,invalid_assignments_rejected=len(invalid)+1,unsupported_bands=['easy','hard'],unsupported_extension='R exponent 5; original source replay unaffected')


def probabilities():
    """Exact probability of the reported cues, including uniformly shuffled ties."""
    report={}
    for profile,ns in (('P',range(2,7)),('R',(3,7))):
        for n in ns:
            wins=Counter();mass=F(0)
            domain=G.factor_domain(profile,n)
            for side in (-1,1):
                fs=[f for f in domain if (f>1)==(side>0)]
                for factor in fs:
                    for row,col in ((1,0),(1,1),(2,0),(2,1)):
                        i=G.instance(profile,n,1,4,offset=-1,second_offset=1,factors=[factor],omitted_row=row,omitted_col=col)
                        _,answer,banks,ci=G.mathematics(i)
                        a=F(answer[1][0]);matched=[b for b in banks if F(b[0][0])==4]
                        freq=Counter(F(b[1][0]) for b in banks)
                        weight=F(1,2*len(fs)*4);mass+=weight
                        for name,key in (('max_magnitude',lambda b:abs(F(b[1][0]))),('min_magnitude',lambda b:-abs(F(b[1][0]))),('most_frequent',lambda b:freq[F(b[1][0])]),('least_frequent',lambda b:-freq[F(b[1][0])])):
                            best=max(map(key,matched));eligible=[b for b in matched if key(b)==best]
                            wins[name]+=weight*F(sum(F(b[1][0])==a for b in eligible),len(eligible))
            assert mass==1 and set(wins.values())=={F(1,2)}
            report[f'{profile}:n={n}']={key:str(value) for key,value in wins.items()}
    save('sampler-probabilities.json',dict(exact=True,conditional_baseline='1/2',groups=report,
                                        reason='Side sampled first, then compatible values; omission column independent; shuffled ties uniform.',
                                        limits='Statement concerns these four strategies, not arbitrary use of the mathematical values.'))
    print(json.dumps(report))


def prepare(resample=False):
    fidelity=json.loads((OUT/'fidelity.json').read_text()) if resample else T.source_checks()
    source=json.loads(Path('../source/source.json').read_text())
    assert source['material']['kp'][':knowledge-point/questions']==json.loads(Path('source-data.json').read_text())
    if resample:
        controlled=json.loads((OUT/'controls.json').read_text())
        boundaries=json.loads((OUT/'boundaries.json').read_text())
    else:
        exact_domain()
        controlled=controls()
        boundaries=[]
        for n in (2,6):
            for s in (-1,1):
                for k in (-6,-1,1,6):
                    r=G.build(G.instance('P',n,s,k),random.Random(23));T.verify(r);boundaries.append(r)
    records=G.generate(count=480,seed=94172863)
    affected=[r for r in records if r['generation']['template']=='P']
    reciprocal=[r for r in records if r['generation']['template']=='R']
    regression=[r for r in records if r['generation']['template']=='B'][:4]
    for r in affected+reciprocal+regression:T.verify(r)
    cov=coverage(records);probe=probes(records)
    save('records.json',records);save('coverage-raw.json',cov);save('shortcuts-raw.json',probe)
    save('boundaries.json',boundaries)
    grader=[]
    for r in G.replay_sources():
        if r.get('math_only'):continue
        if field(r)[':answer-field/type'].endswith('/blank'):
            grader.append(dict(label='source blank',record=r,checks=[dict(submitted='t*(t^2/3-2)',expected='accepted'),dict(submitted='t^3-2t',expected='rejected')]))
        else:grader.append(T.make_checks(r,'source bank'))
    grader.extend(T.make_checks(r,'boundary/control/regression') for r in boundaries+controlled+regression)
    save('grader-input.json',grader)
    report=dict(fidelity=fidelity,source_snapshot_matches=True,affected_normal_math_checks=len(affected),affected_reciprocal_math_checks=len(reciprocal),small_regression=len(regression),boundaries=len(boundaries),controls=len(controlled),runtime=runtime(),generator_rejection='No resampling: compatible offset/divisor domains construct distinct banks. Explicit invalid assignments raise ValueError.')
    save('validation.json',report)
    print(json.dumps(report))


def after():
    rs=json.loads((OUT/'delivery/accepted.json').read_text())
    cov=coverage(rs);probe=probes(rs)
    save('coverage-delivered.json',cov);save('shortcuts-delivered.json',probe)
    controls_delivered=json.loads((OUT/'controls-delivery/accepted.json').read_text())
    save('controls-shortcuts-delivered.json',probes(controls_delivered))
    raw=json.loads((OUT/'records.json').read_text())
    assert {T.semantic(r) for r in rs}=={T.semantic(r) for r in raw}
    grader=[]
    byid={r['question'][':question/id']:r for r in rs}
    for t in probe['trials']:
        r=byid[t['id']]
        case=T.make_checks(r,'delivered '+t['profile']+' complete bank')
        case['checks'].extend(dict(submitted_answer_id=aid,expected='accepted' if t['wins'][strategy] else 'rejected',purpose=strategy) for strategy,aid in t['cue_selected'].items())
        grader.append(case)
    save('delivered-grader-input.json',grader)
    ids=sorted(byid);draws=[]
    for j in range(1024):
        digest=hashlib.sha256(f'course-academy/question-selection/v1/author-rank-repair-{j}'.encode()).digest()
        u=(int.from_bytes(digest[8:16],'big')>>11)/2**53
        draws.append(ids[int(u*len(ids))])
    selected=[byid[q] for q in ids if q in set(draws)]
    save('coverage-selection.json',coverage(selected));save('shortcuts-selection.json',probes(selected))
    save('selection.json',dict(pool=len(ids),draws=len(draws),unique_selected=len(selected),semantics=len({T.semantic(r) for r in selected}),
                              rule='question_selection.rs select(): positive moderate band, SHA256 uniform(8)',
                              limits=['Synthetic sorted UUID order substitutes for unavailable database entity IDs; membership and within-band distribution only.',
                                      'Live learner history, zero moderate policy weight, database identity collisions and concurrent inventory changes unavailable offline.',
                                      'Without difficulty policy select() returns first database ID; live order is unknown.'],controls_added_to_normal_pool=False))
    reps=[]
    for side in (True,False):
        reps.append(next(r for r in rs if r['generation']['template']=='P' and r['generation']['parameters']['n']==2 and (F(r['generation']['parameters']['factors'][0])>1)==side))
    reps.append(next(r for r in rs if r['generation']['template']=='P' and r['generation']['parameters']['n']==6))
    reps.extend(next(r for r in rs if r['generation']['template']=='R' and r['generation']['parameters']['n']==n) for n in (3,7))
    reps.append(next(r for r in rs if r['generation']['template']=='B'))
    save('render-records.json',reps)
    print(json.dumps(dict(raw=len(raw),delivered=len(rs),raw_P=sum(r['generation']['template']=='P' for r in raw),delivered_P=probe['groups']['P']['attempts'],quadratic=probe['groups']['P:n=2'],semantics=cov['semantic_instances'],selected=len(selected),render_records=len(reps))))


if __name__=='__main__':
    if '--probabilities' in sys.argv:probabilities()
    elif '--after-delivery' in sys.argv:after()
    else:prepare('--resample' in sys.argv)
