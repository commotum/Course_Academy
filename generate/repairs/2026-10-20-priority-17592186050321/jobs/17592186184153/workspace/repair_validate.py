"""Targeted feedback regression; retains the original author evidence separately.
Run prepare, shared check_delivery, then --after-delivery; commands in repair log.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import generator as G
import validate as T

OUT=Path('evidence/repair'); OUT.mkdir(exist_ok=True)
T.OUT=OUT

def save(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n')

def field(r): return r['question'][':question/answer-fields'][0]

def choices(r): return field(r)[':answer-field/choices']

def independent_coefficients(r):
    """Read actual displayed choices, not bank metadata, with test-only parser."""
    i=r['generation']['parameters']; x=T.V[i['variable']]
    p=-T.S.Rational(i['n'],2) if i['profile']=='R' else T.S.Integer(i['n'])
    rows=[]
    for a in choices(r):
        value=T.S.expand(T.tex(a[':answer/value'])-T.V['C'])
        linear=value.coeff(x,1); power=value-linear*x
        coefficient=abs(power.as_coeff_Mul()[0])
        num,den=coefficient.as_numer_denom()
        rows.append({'id':a[':answer/id'],'linear':str(linear),'coefficient':str(coefficient),
                     'unit_single_digit':bool(num==1 and den<10),
                     'coefficient_numerator':int(num),'coefficient_denominator':int(den),
                     'power':str(power)})
    return rows

def conditional(records):
    trials=[]
    for r in records:
        i=r['generation']['parameters']
        if i['profile']!='P': continue
        rows=independent_coefficients(r)
        matched=[row for row in rows if row['linear']==str(i['k'])]
        cue=[row for row in matched if row['unit_single_digit']]
        target=field(r)[':answer-field/correct'][1]
        # Also test raw length/coefficient rank after matching the constant.
        ranked=sorted(matched,key=lambda row:F(row['coefficient']))
        actual_rank=next(j for j,row in enumerate(ranked) if row['id']==target)
        length_rank=sorted(matched,key=lambda row:len(next(a[':answer/value'] for a in choices(r) if a[':answer/id']==row['id'])))
        actual_length_rank=next(j for j,row in enumerate(length_rank) if row['id']==target)
        trials.append({'id':r['question'][':question/id'],'n':i['n'],'s':i['s'],
                       'constant_first':i['constant_first'],'ksign':1 if i['k']>0 else -1,
                       'cue_candidates':len(cue),'constant_candidates':len(matched),
                       'cue_unique_correct':len(cue)==1 and cue[0]['id']==target,
                       'magnitude_rank_after_constant':actual_rank,'length_rank_after_constant':actual_length_rank,
                       'rows':rows})
        assert len(cue)==len(matched)>=2
    groups=defaultdict(list)
    for t in trials:
        groups['all'].append(t); groups['n='+str(t['n'])].append(t)
        groups[f"n={t['n']},s={t['s']},order={t['constant_first']}"].append(t)
    summary={}
    for name,ts in groups.items():
        summary[name]={'attempts':len(ts),'unique_correct':sum(t['cue_unique_correct'] for t in ts),
                       'candidate_counts':dict(Counter(t['cue_candidates'] for t in ts)),
                       'magnitude_ranks_after_constant':dict(Counter(t['magnitude_rank_after_constant'] for t in ts)),
                       'length_ranks_after_constant':dict(Counter(t['length_rank_after_constant'] for t in ts))}
    affected=[t for t in trials if t['n'] in (4,6)]
    return {'strategy':'Match printed constant, choose sole unit-numerator one-digit denominator power fraction (review 1)',
            'affected_attempts':len(affected),'affected_unique_correct':sum(t['cue_unique_correct'] for t in affected),
            'groups':summary,'trials':trials,'passes':True}

def exhaustive():
    counts=Counter(); ranks=defaultdict(Counter); matching_ranks=defaultdict(Counter)
    for n in range(2,7):
        for ds in combinations([d for d in range(2,10) if d!=n+1],2):
            factors=[str(F(n+1,d)) for d in ds]
            for row in (0,1):
                for col in (1,2):
                    for s in (-1,1):
                        i=G.instance('P',n,s,4,factors=factors,omitted_row=row,omitted_col=col)
                        integrand,answer,banks,ci=G.mathematics(i)
                        # Independent rational polynomial differentiation, without SymPy or generator formatter.
                        expected={F(0):F(4),F(n):F(s)}
                        hits=[]
                        for terms in banks:
                            derivative={}
                            for c,p in terms:
                                c,p=F(c),F(p)
                                derivative[p-1]=derivative.get(p-1,F(0))+c*p
                            hits.append(derivative==expected)
                            assert all(abs(F(c)).numerator==1 and 2<=F(c).denominator<=9 for c,p in terms if F(p)==n+1)
                        assert hits==[j==ci for j in range(5)]
                        matched=[terms for terms in banks if F(terms[0][0])==4]
                        assert len(matched)>=2 and len({F(t[1][0]) for t in matched})==len(matched)
                        mags=sorted({abs(F(t[1][0])) for t in banks})
                        ranks[n][mags.index(F(1,n+1))]+=1
                        matching_ranks[n][sorted(abs(F(t[1][0])) for t in matched).index(F(1,n+1))]+=1
                        counts[n]+=1
                        # Parsing one record per divisor pair also checks actual printed bank.
                        if row==1 and col==2 and s==1:
                            r=G.build(i,random.Random(n)); T.verify(r)
    assert all(len(c)>1 for c in ranks.values())
    assert all(set(c)=={0,1,2} for c in matching_ranks.values())
    return {'records_checked_exactly':sum(counts.values()),'counts_per_exponent':dict(counts),
            'rendered_banks_independently_parsed':105,'divisor_pairs_per_exponent':21,
            'both_signs':True,'all_four_omitted_cells':True,
            'correct_coefficient_magnitude_ranks':{n:dict(c) for n,c in ranks.items()},
            'correct_ranks_after_matching_constant':{n:dict(c) for n,c in matching_ranks.items()},
            'unique_typography_cue':0,'passes':True}

def runtime():
    manifest=json.loads(Path('package.json').read_text())
    assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{}}
    a=G.generate(count=5,seed=84153); assert a==G.generate(count=5,seed=84153)
    save('sample.json',a)
    with tempfile.TemporaryDirectory(prefix='sum-rule-repair-',dir=OUT.resolve()) as directory:
        for f in manifest['files']:shutil.copy(f,directory)
        result=subprocess.run([sys.executable,'generator.py','--difficulty','moderate','--count','5','--seed','84153','--format','json'],cwd=directory,capture_output=True,text=True,check=True)
        assert json.loads(result.stdout)==a
    # Explicit unsupported assignments cannot bypass the new grid restriction.
    bad=0
    for n in (4,6):
        for factors in (['1/2','2'],['1','2'],['2','2']):
            try:G.build(dict(profile='P',n=n,s=1,k=4,variable='x',constant_first=True,bank='grid',offset=1,factors=factors,omitted_row=1,omitted_col=2))
            except ValueError:bad+=1
            else:raise AssertionError((n,factors))
    for band in ('easy','hard'):
        try:G.generate(band,1,0)
        except ValueError:pass
        else:raise AssertionError(band)
    return {'determinism':True,'relocation':True,'invalid_banks_rejected':bad,'dependencies':manifest['dependencies'],'passes':True}

def prepare():
    fidelity=T.source_checks()
    domain=exhaustive()
    pairs,native=T.controlled()
    boundaries=[]
    for n in (2,6):
        for s in (-1,1):
            for k in (-6,-1,1,6):
                r=G.build(G.instance('P',n,s,k),random.Random(n+k+s));T.verify(r);boundaries.append(r)
    records=G.generate(count=240,seed=86184906)
    # Feedback-affected P checked completely. Small R/B regression preserves earlier independent evidence.
    affected=[r for r in records if r['generation']['template']=='P']
    regression=[next(r for r in records if r['generation']['template']==p and r['generation']['parameters']['n']==n)
                for p,ns in [('R',(3,5,7)),('B',(2,3,4,5,6))] for n in ns]
    for r in affected+regression:T.verify(r)
    for r in boundaries+affected+regression:native.append(T.make_checks(r,'repair regression '+r['question'][':question/id']))
    for r in G.replay_sources():
        if r.get('math_only'):continue
        if field(r)[':answer-field/type'].endswith('/blank'):
            native.append({'label':'source blank','record':r,'checks':[{'submitted':'t*(t^2/3-2)','expected':'accepted','purpose':'equivalent'},{'submitted':'t^3-2t','expected':'rejected','purpose':'missing division'}]})
        else:native.append(T.make_checks(r,'source '+r['generation']['source_refs'][0]))
    # Grader counterfactuals reject stale mathematical responses even when UUIDs change.
    # Existing controls cover changed exponent/sign/constant/order and irrelevant bank assignments.
    save('grader-input.json',native)
    save('records.json',records);save('boundaries.json',boundaries);save('counterfactuals.json',pairs)
    save('exhaustive.json',domain);save('shortcut-before.json',conditional(records))
    cov=T.coverage(records);save('coverage-before.json',cov)
    report={'fidelity':fidelity,'exhaustive':domain,'runtime':runtime(),
            'independent_rendered_math':{'polynomial_normal':len(affected),'polynomial_boundaries':len(boundaries),'reciprocal_blank_regression':len(regression),'controlled_pairs':len(pairs)},
            'generation_rejection':{'resamples':0,'reason':'Distinct divisors and nonzero distinct constant rows guarantee complete distinct banks; invalid explicit assignments raise ValueError.'},
            'seed':86184906,'count':240,'passes':True}
    save('validation.json',report)
    print(json.dumps({'fidelity':fidelity,'exhaustive':sum(domain['counts_per_exponent'].values()),'normal_P':len(affected),'regression':len(regression),'controls':len(pairs)}))

def after():
    raw=json.loads((OUT/'records.json').read_text()); accepted=json.loads((OUT/'delivery/accepted.json').read_text())
    save('shortcut-after.json',conditional(accepted));save('coverage-after.json',T.coverage(accepted))
    native=[]
    for r in accepted:
        if r['generation']['template']=='P':native.append(T.make_checks(r,'delivered repaired P '+r['question'][':question/id']))
    save('delivered-grader-input.json',native)
    # Controlled n=4->6 pair holds every parameter except exponent/factors fixed.
    # Keep competing divisors fixed, so factors change only as derived metadata.
    render=[]
    for s,order in ((1,True),(-1,False)):
        for n in (4,6):
            i=G.instance('P',n,s,-2,'t',order,factors=[str(F(n+1,d)) for d in (3,8)],omitted_row=0,omitted_col=2)
            r=G.build(i,random.Random(19));T.verify(r);render.append(r)
    render.extend(next(r for r in accepted if r['generation']['template']==p) for p in ('R','B'))
    save('render-records.json',render)
    # Reuse previous read-only selector evidence: selection code and band unchanged.
    summary={'before':len(raw),'after':len(accepted),'semantic_before':len({T.semantic(r) for r in raw}),
             'semantic_after':len({T.semantic(r) for r in accepted}),
             'delivery_report':'delivery/delivery.json','selection':'All accepted records moderate; earlier within-positive-band uniform selection model remains applicable. No database/learner history access; no claim about live order or draws.',
             'passes':True}
    assert {T.semantic(r) for r in raw}=={T.semantic(r) for r in accepted}
    save('delivery-summary.json',summary);print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--after-delivery',action='store_true');a=p.parse_args()
    after() if a.after_delivery else prepare()
