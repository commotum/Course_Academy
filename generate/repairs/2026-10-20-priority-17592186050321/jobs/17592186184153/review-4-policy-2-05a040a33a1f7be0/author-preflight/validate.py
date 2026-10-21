#!/usr/bin/env python3
"""Author checks; run with the job Python. SymPy is test-only, not runtime."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import tempfile
import sys
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import generator as G
from math_format import normalize_tex, normalize_prose, validate_generated_record

OUT = Path('evidence')
OUT.mkdir(exist_ok=True)
V = {v: S.Symbol(v, positive=True) for v in ('x', 'y', 't')}
V['C'] = S.Symbol('C')
TRANS = standard_transformations + (implicit_multiplication_application,)


def tex(text):
    """Independent parser for the source's limited arithmetic TeX (no generator formatter)."""
    text = text.replace(r'\left', '').replace(r'\right', '').replace(r'\,', '').replace(r'\cdot', '*')
    pos = 0
    def group():
        nonlocal pos
        while pos < len(text) and text[pos].isspace(): pos += 1
        if text[pos] != '{':
            char = text[pos]; pos += 1; return char
        pos += 1
        return walk('}')
    def walk(stop=None):
        nonlocal pos
        out = ''
        while pos < len(text):
            if stop and text[pos] == stop:
                pos += 1; return out
            if text.startswith(r'\frac', pos) or text.startswith(r'\dfrac', pos):
                pos += 5 if text.startswith(r'\frac',pos) else 6
                a, b = group(), group()
                out += f'(({a})/({b}))'
            elif text.startswith(r'\sqrt', pos):
                pos += 5; degree = '2'
                if text[pos] == '[':
                    end = text.index(']', pos); degree = text[pos+1:end]; pos = end+1
                a = group(); out += f'(({a})**(1/({degree})))'
            elif text[pos] == '{':
                out += '(' + group() + ')'
            elif text[pos] == '^':
                out += '**'; pos += 1
            else:
                out += text[pos]; pos += 1
        assert stop is None, text
        return out
    return parse_expr(walk(),local_dict=V, transformations=TRANS)


def poly(terms, v):
    return sum(S.Rational(c) * V[v]**S.Rational(p) for c,p in terms)


def correct_value(r):
    f = r['question'][':question/answer-fields'][0]
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])


def semantic(r):
    i=r['generation']['parameters']
    return (i['profile'], i['n'], i['s'], i['k'])


def verify(r):
    validate_generated_record(r)
    i = r['generation']['parameters']; v = i['variable']; x = V[v]
    p = -S.Rational(i['n'], 2) if i['profile']=='R' else S.Integer(i['n'])
    integrand = i['s']*x**p+i['k']
    correct = S.integrate(integrand,x)
    actual = tex(correct_value(r))
    assert S.simplify(S.diff(actual,x)-integrand)==0
    assert S.simplify(actual-V['C']-correct)==0 if i['profile']!='B' else S.simplify(actual-correct)==0
    q = r['question']; prompt=q[':question/problem']
    if i['profile']=='B':
        supplied = re.search(r"y'\(t\)=(.*?)\$",prompt)[1]
        assert '+\\,C' in prompt and '+C' not in correct_value(r)
    elif i['profile']=='P':
        supplied = re.search(r'\\left\((.*?)\\right\)',prompt)[1]
    else:
        supplied=re.search(r'of \$(.*?)\$',prompt)[1]
    assert S.simplify(tex(supplied)-integrand)==0
    final=q[':question/worked-solution'].split('&=')[-1].split(r'\end')[0].strip()
    assert S.simplify(tex(final)-correct-V['C'])==0
    f=q[':question/answer-fields'][0]
    values=[tex(a[':answer/value']) for a in f[':answer-field/choices']]
    # Distinct full expressions; exactly one general antiderivative.
    for j,a in enumerate(values):
        for b in values[:j]: assert S.simplify(a-b)!=0
    qualifies=[S.simplify(S.diff(a,x)-integrand)==0 for a in values]
    assert sum(qualifies)==1
    if i['profile']!='B': assert all(a.has(V['C']) for a in values)
    return integrand, correct


def source_checks():
    original=json.loads(Path('source-data.json').read_text())
    replay=G.replay_sources()
    expected={
        'q-2159':(V['x']**S.Rational(1,2)-3,'x'),
        'q-29828':(V['x']**S.Rational(5,2)+V['x']**S.Rational(-5,2),'x'),
        'q-113781':(V['x']**S.Rational(1,4)-V['x']**5,'x'),
        'q-71169':(V['x']**S.Rational(-3,2)+4,'x'),
        'q-71173':(2+V['y']**-5,'y'),
        'q-133291':(V['t']**2-2,'t'),
        'q-71167':(5-V['x']**3,'x')}
    banks, matched, math = 0,0,0
    for q,r in zip(original,replay):
        ref=q[':question/math-academy-id']; g=r['generation']; integrand,v=expected[ref]
        assert S.simplify(poly(g['answer_terms'],v).diff(V[v])-integrand)==0; math+=1
        if r.get('math_only'): continue
        validate_generated_record(r)
        f=q[':question/answer-fields'][0]; rf=r['question'][':question/answer-fields'][0]
        assert [normalize_tex(a[':answer/value']) for a in f[':answer-field/choices']]==[a[':answer/value'] for a in rf[':answer-field/choices']]
        assert S.simplify(tex(correct_value(r)).diff(V[v])-integrand)==0
        if ':answer-field/correct' in f:
            assert normalize_tex(f[':answer-field/correct'][':answer/value'])==correct_value(r)
        if ref!='q-133291': assert r['question'][':question/problem']==normalize_prose(q[':question/problem'])
        if ':question/worked-solution' in q:
            expected_worked = q[':question/worked-solution'] + ('\n\n' + G.BLANK_EXPLANATION if ref=='q-133291' else '')
            assert r['question'][':question/worked-solution']==normalize_prose(expected_worked)
        banks+=1; matched+=len(f[':answer-field/choices'])
    # Reconstruct complete supported banks from generalized recipes, not source literals.
    for i, ref in [(G.instance('P',3,-1,5,bank='source'), 'q-71167'), (G.instance('R',3,1,4,constant_first=False,bank='source'),'q-71169'), (G.instance('B',2,1,-2,'t',False),'q-133291')]:
        r=G.build(i); verify(r)
        q=next(q for q in original if q[':question/math-academy-id']==ref)
        actual=[tex(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
        orig=[tex(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
        assert len(actual)==len(orig)
        assert all(sum(S.simplify(a-b)==0 for b in actual)==1 for a in orig)
    report={'source_questions':len(original),'math_replays':math,'complete_captured_fields':banks,'matched_choices':matched,'total_choices':21,
            'complete_radio_banks':'4/4 captured, 2/2 parameterized moderate',
            'missing_fields':['q-71173','q-113781'],'missing_solutions_reconstructed':['q-2159','q-29828'],
            'prompt_correction':'q-133291 derivative restored from source solution', 'passes':True}
    (OUT/'fidelity.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'source-replay.json').write_text(json.dumps(replay,indent=2)+'\n')
    return report


def make_checks(r, label):
    f=r['question'][':question/answer-fields'][0]
    if f[':answer-field/type'].endswith('/blank'):
        i=r['generation']['parameters']; x=V[i['variable']]
        expr=S.integrate(i['s']*x**i['n']+i['k'],x)
        equivalents=[str(expr),str(S.factor(expr))]
        checks=[{'submitted':s.replace('**','^'),'expected':'accepted','purpose':'independent equivalent polynomial'} for s in equivalents]
        checks += [{'submitted':str(expr+x).replace('**','^'),'expected':'rejected','purpose':'incorrect constant-term integral'},
                   {'submitted':str(i['s']*x**i['n']+i['k']).replace('**','^'),'expected':'rejected','purpose':'copy integrand'}]
    else:
        checks=[{'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
                 'purpose':'complete bank choice'} for a in f[':answer-field/choices']]
    return {'label':label, 'record':r, 'checks':checks}


def coverage(records):
    report={}
    for profile in ('P','R','B'):
        rs=[r for r in records if r['generation']['template']==profile]
        items=[r['generation']['parameters'] for r in rs]
        report[profile]={'records':len(rs),'semantic_instances':len({semantic(r) for r in rs}),
          'n':sorted({i['n'] for i in items}),'s':sorted({i['s'] for i in items}),'k':sorted({i['k'] for i in items}),
          'constant_first':sorted({i['constant_first'] for i in items}),'variables':sorted({i['variable'] for i in items})}
        if profile!='B':
            report[profile]['bank_assignments']={'factors':sorted({f for i in items for f in i['factors']}),
              'omitted_cells':sorted({(i['omitted_row'],i['omitted_col']) for i in items}),
              'offset_signs':sorted({1 if i['offset']>0 else -1 for i in items})}
            if profile == 'R': assert len(report[profile]['bank_assignments']['factors'])==6
            else:
                report[profile]['bank_assignments']['divisors'] = sorted({(Fraction(i['n']+1)/Fraction(f)).numerator for i in items for f in i['factors']})
                assert report[profile]['bank_assignments']['divisors'] == list(range(2,10))
            assert len(report[profile]['bank_assignments']['omitted_cells'])==4
            assert report[profile]['bank_assignments']['offset_signs']==[-1,1]
        if profile=='B': continue
        groups=defaultdict(list)
        for r in rs:
            i=r['generation']['parameters']
            groups[f"s={i['s']}, ksign={1 if i['k']>0 else -1}, constant_first={i['constant_first']}"].append(r)
        for n in sorted({r['generation']['parameters']['n'] for r in rs}):
            groups['n='+str(n)] = [r for r in rs if r['generation']['parameters']['n']==n]
        group_reports={}
        for name, group in [('all',rs),*sorted(groups.items())]:
            positions=[]; shortest=longest=0; exponent_alone=[]; constant_alone=[]; coefficient_alone=[]; rank_success=Counter(); magnitude_rank_success=Counter(); bank_cells=Counter()
            for r in group:
                i=r['generation']['parameters']; f=r['question'][':question/answer-fields'][0]; choices=f[':answer-field/choices']; target=f[':answer-field/correct'][1]
                positions.append(next(j for j,a in enumerate(choices) if a[':answer/id']==target))
                lengths=[len(a[':answer/value']) for a in choices]; ci=positions[-1]
                shortest+=int(lengths.index(min(lengths))==ci); longest+=int(lengths.index(max(lengths))==ci)
                for rank in range(5):
                    rank_success[rank] += int(sorted(range(5), key=lambda j:lengths[j])[rank] == ci)
                # Multiplicative error assignments can put the correct power coefficient at every magnitude rank.
                fs=[1,*map(Fraction,i['factors'])]
                magnitude_rank_success[sorted(fs).index(1)] += 1
                bank_cells[(i['omitted_row'],i['omitted_col'])] += 1
                x=V[i['variable']]; c=tex(correct_value(r))-V['C']
                # How many options survive checking just one summand's coefficient/exponent?
                constant_alone.append(sum(S.expand(tex(a[':answer/value'])-V['C']).coeff(x,1)==i['k'] for a in choices))
                p=-S.Rational(i['n'],2) if profile=='R' else S.Integer(i['n'])
                a=S.Rational(i['s'])/(p+1)
                coefficient_alone.append(sum(S.expand(tex(ch[':answer/value'])-V['C']).coeff(x**(p+1))==a for ch in choices))
                exponent_alone.append(sum(any(term.as_powers_dict().get(x)==p+1 for term in S.Add.make_args(S.expand(tex(a[':answer/value'])-V['C']))) for a in choices))
            counts=Counter(positions)
            group_reports[name]={'attempts':len(group),'position_counts':dict(counts),'best_fixed_position_success':max(counts.values()),
              'baseline_random_position':0.2, 'shortest_success':shortest,'longest_success':longest,
              'length_rank_success':dict(rank_success),'correct_coefficient_magnitude_rank':dict(magnitude_rank_success),'omitted_cells':{str(k):v for k,v in bank_cells.items()},
              'nonconstant_integral_alone_candidate_counts':dict(Counter(coefficient_alone)), 'constant_rule_alone_candidate_counts':dict(Counter(constant_alone)), 'exponent_increment_alone_candidate_counts':dict(Counter(exponent_alone))}
            assert len(counts)>1, (profile,name,'fixed answer position')
            assert max(rank_success.values())<len(group), (profile,name,'length rank predictor')
            if name=='all' or name.startswith('n='): assert len(magnitude_rank_success)>1, (profile,name,'coefficient magnitude predictor')
            assert shortest<len(group) and longest<len(group), (profile,name,'length predictor')
            assert min(constant_alone)>=2 and min(coefficient_alone)>=2 and min(exponent_alone)>=2, (profile,name,'single-rule cue')
        report[profile]['shortcut_probes']=group_reports
    return report


def controlled():
    pairs=[]; native=[]
    for profile in ('P','R','B'):
        v='t' if profile=='B' else 'x'
        base=G.instance(profile,3,1,4,v,True)
        r=G.build(base,random.Random(5)); verify(r)
        for key,value in [('n',5),('s',-1),('k',-4),('constant_first',False)]:
            changed=base|{key:value}
            if profile=='P' and key=='n':
                changed['factors']=[str(Fraction(value+1,d)) for d in (2,8)]
            other=G.build(changed,random.Random(5)); verify(other)
            if key=='constant_first':
                assert S.simplify(tex(correct_value(r))-tex(correct_value(other)))==0
            else:
                assert S.simplify(tex(correct_value(r))-tex(correct_value(other)))!=0
            assert r['question'][':question/problem']!=other['question'][':question/problem']
            assert r['question'][':question/worked-solution']!=other['question'][':question/worked-solution']
            if profile=='B' and key!='constant_first':
                item=make_checks(other,f'counterfactual {profile} {key}')
                item['checks'].append({'submitted':correct_value(r),'expected':'rejected','purpose':'stale base response after relevant change'})
                native.append(item)
            else: native.append(make_checks(other,f'counterfactual {profile} {key}'))
            pairs.append({'profile':profile,'change':key,'base':r,'changed':other,'predicted':'preserve response' if key=='constant_first' else 'change response'})
        if profile!='B':
            renamed=G.build(base|{'variable':'y'},random.Random(5)); verify(renamed)
            assert S.simplify(tex(correct_value(r)).subs(V['x'],V['y'])-tex(correct_value(renamed)))==0
            pairs.append({'profile':profile,'change':'rename variable','base':r,'changed':renamed,'predicted':'preserve under variable substitution'})
            native.append(make_checks(renamed,'irrelevant variable rename '+profile))
        if profile!='B':
            factor_changes = ([{'factors':['2','4/3']},{'factors':['4/7','1/2']}] if profile=='P' else [{'factors':['2','3']},{'factors':['1/3','1/2']}])
            for change in (*factor_changes,{'offset':-2},{'omitted_row':0,'omitted_col':1}):
                other=G.build(base|change,random.Random(5)); verify(other)
                assert correct_value(r)==correct_value(other)
                assert {a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']} != {a[':answer/value'] for a in other['question'][':question/answer-fields'][0][':answer-field/choices']}
                pairs.append({'profile':profile,'change':change,'base':r,'changed':other,'predicted':'preserve key; change distractor-role assignments'})
                native.append(make_checks(other,'bank assignment '+profile+' '+str(change)))
        # Reordering options cannot change the mathematical key.
        shuffled=G.build(base,random.Random(17)); assert correct_value(r)==correct_value(shuffled)
        native.extend([make_checks(r,'controlled base '+profile),make_checks(shuffled,'option reorder '+profile)])
    return pairs,native


def prepare():
    source=source_checks()
    pairs,native=controlled()
    # Explicit boundaries first, independent of random coverage.
    boundaries=[]
    for profile in ('P','R','B'):
        for n in ((3,7) if profile=='R' else (2,6)):
            for s in (-1,1):
                for k in (-6,-1,1,6):
                    r=G.build(G.instance(profile,n,s,k,'t' if profile=='B' else 'x',k>0),random.Random(n+k+s)); verify(r); boundaries.append(r)
    # Normal sample resolves coverage of interior exponents, constants, and position/subgroup cues.
    records=G.generate(count=240,seed=20261020)
    for r in records: verify(r)
    cov=coverage(records)
    for p,c in cov.items():
        assert c['n']==([3,5,7] if p=='R' else [2,3,4,5,6])
        assert c['s']==[-1,1] and c['k']==[*range(-6,0),*range(1,7)] and c['constant_first']==[False,True]
    # Native cases: source bank radios/blank plus every boundary, controls, and a small normal regression.
    for r in G.replay_sources():
        if r.get('math_only'):continue
        f=r['question'][':question/answer-fields'][0]
        if f[':answer-field/type'].endswith('/blank'):
            native.append({'label':'source blank','record':r,'checks':[{'submitted':'t*(t^2/3-2)','expected':'accepted','purpose':'factored equivalent'}, {'submitted':'t^3-2t','expected':'rejected','purpose':'missing division'}]})
        else: native.append(make_checks(r,'source '+r['generation']['source_refs'][0]))
    native.extend(make_checks(r,'boundary '+str(j)) for j,r in enumerate(boundaries))
    native.extend(make_checks(r,'normal regression '+str(j)) for j,r in enumerate(records[:9]))
    (OUT/'grader-input.json').write_text(json.dumps(native,indent=2)+'\n')
    (OUT/'test-records.json').write_text(json.dumps(records,indent=2)+'\n')
    (OUT/'counterfactuals.json').write_text(json.dumps(pairs,indent=2)+'\n')
    (OUT/'boundaries.json').write_text(json.dumps(boundaries,indent=2)+'\n')
    report={'fidelity':source,'correctness':{'source_math':7,'boundaries':len(boundaries),'normal':len(records),'controlled_pairs':len(pairs),'failures':0},
            'generation_rejection':{'policy':'invalid explicit parameters raise ValueError; sampled domain guarantees distinct complete banks','normal_resamples':0},
            'before_delivery':cov}
    # deterministic run, declared runtime-only relocation and rejected bands.
    sample=G.generate(count=5,seed=84153)
    assert sample==G.generate(count=5,seed=84153)
    (OUT/'sample.json').write_text(json.dumps(sample,indent=2)+'\n')
    for band in ('easy','hard'):
        try:G.generate(band,1,0)
        except ValueError:pass
        else:raise AssertionError(band)
    with tempfile.TemporaryDirectory(prefix='sum-rule-relocate-', dir=OUT.resolve()) as directory:
        for f in json.loads(Path('package.json').read_text())['files']:shutil.copy(f,directory)
        result=subprocess.run([sys.executable,'generator.py','--difficulty','moderate','--count','5','--seed','84153','--format','json'],cwd=directory,capture_output=True,text=True,check=True)
        assert json.loads(result.stdout)==G.generate(count=5,seed=84153)
    report['runtime']={'deterministic':True,'relocation':True,'unsupported_bands_rejected':['easy','hard'],'dependencies':'standard library only'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'source':source,'correctness':report['correctness'],'normal_semantic_instances':len({semantic(r) for r in records})}))


def after():
    report=json.loads((OUT/'validation.json').read_text())
    records=json.loads((OUT/'delivery/accepted.json').read_text())
    report['after_delivery']=coverage(records)
    for r in records:verify(r)
    # Read-only reproduction of select() for the positive moderate-band pool.
    # Common band weights do not affect membership within a single band.
    qids=sorted({r['question'][':question/id'] for r in records})
    draws=[]
    for j in range(1024):
        digest=hashlib.sha256(f'course-academy/question-selection/v1/author-{j}'.encode()).digest()
        uniform=(int.from_bytes(digest[8:16],'big')>>11)/(2**53)
        draws.append(qids[int(uniform*len(qids))])
    lookup={r['question'][':question/id']:r for r in records}
    selection=Counter(lookup[q]['generation']['template'] for q in draws)
    report['selection']={'implementation':'question_selection.rs select(), within one positive-weight moderate band',
                         'pool':len(qids),'draws':len(draws),'template_counts':dict(selection),
                         'limits':['Synthetic sorted UUID identities stand in for database entity IDs; reproduces uniform within-band rule, not exact live draws.',
                                   'Learner history, zero band weights, concurrent inventory changes and database identity collisions are unavailable offline.',
                                   'No-policy selector uses first database ID; its live candidate ordering cannot be inferred offline.']}
    report['grading']=json.loads((OUT/'grading.json').read_text())|{'records':'See grading.json for per-case details'}
    # Keep report bounded; actual full grading remains separate.
    report['grading'].pop('records',None)
    report['decision_variation']={'passes':True,'controlled_pairs':22,'answer_bearing_slots':['signed constant','signed power','power exponent','correct option position'],
       'cue_probes':'Within profile and every sign/constant-sign/order subgroup, no tested position or answer-length rank strategy always succeeds. Coefficient magnitude ranks vary per profile and exponent; small cross-groups can repeat a rank by chance, and controlled factor changes provide explicit counterexamples. Checking only one summand retains multiple candidates.',
       'scope':'Finite moderate P/R/B families. No claim about untested arbitrary strategies or unsupported bands.'}
    (OUT/'pedagogical-variation.json').write_text(json.dumps(report,indent=2)+'\n')
    # Render both signs and orders for each served template, plus two original radios for side-by-side review.
    reps=[]
    for p in ('P','R','B'):
        for s,order in ((1,True),(-1,False)):
            reps.append(next(r for r in records if r['generation']['template']==p and r['generation']['parameters']['s']==s and r['generation']['parameters']['constant_first']==order))
    reps.extend(r for r in G.replay_sources() if r.get('generation',{}).get('source_refs') in [['q-71167'],['q-71169']])
    (OUT/'render-records.json').write_text(json.dumps(reps,indent=2)+'\n')
    print(json.dumps({'accepted':len(records),'semantic_instances':len({semantic(r) for r in records}),'selection_templates':dict(selection),'render_records':len(reps)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--after-delivery',action='store_true');a=p.parse_args()
    after() if a.after_delivery else prepare()
