#!/usr/bin/env python3
"""Reproducible source-specific author checks. Run with the pinned Python."""
import argparse
import collections
import hashlib
import functools
import json
from pathlib import Path
import random
import re

import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import generator as g

HERE = Path(__file__).resolve().parent
OUT = HERE/'evidence'
X = g.X


def save(name, value):
    (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')


@functools.lru_cache(maxsize=20000)
def tex_expr(text):
    """Parse only this source's small arithmetic TeX grammar, independently of g."""
    text = text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').strip()
    def group(pos):
        assert text[pos]=='{', (text,pos)
        depth=1;j=pos+1
        while depth:
            if text[j]=='{':depth+=1
            if text[j]=='}':depth-=1
            j+=1
        return text[pos+1:j-1],j
    out='';i=0
    while i<len(text):
        if text.startswith(r'\frac',i):
            a,j=group(i+5);b,i=group(j)
            out+='(('+str(tex_expr(a))+')/('+str(tex_expr(b))+'))'
        elif text.startswith(r'\sqrt',i):
            a,i=group(i+5);out+='(('+str(tex_expr(a))+')**(1/2))'
        elif text[i]=='{':
            a,i=group(i);out+='('+str(tex_expr(a))+')'
        else:out+=text[i];i+=1
    return parse_expr(out,local_dict={'x':X,'C':s.Symbol('C'),'sqrt':s.sqrt},
                      transformations=standard_transformations+(implicit_multiplication_application,convert_xor))


def field(record):
    return record['question'][':question/answer-fields'][0]


def key(record):
    f=field(record);aid=f[':answer-field/correct'][1]
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)


def integrand(record):
    prompt=record['question'][':question/problem']
    text=re.search(r'\\int (.*?)\\,\\mathrm\{d\}x',prompt).group(1)
    if 'f(x)' in text:
        f=re.search(r'Given \$f\(x\)=(.*?)\$',prompt).group(1)
        text=text.replace('f(x)','('+f+')')
    return tex_expr(text)


def check_math(record):
    f=field(record);function=integrand(record)
    valid=[]
    for a in f[':answer-field/choices']:
        derivative=s.diff(tex_expr(a[':answer/value']),X)
        if s.simplify(derivative-function)==0:valid.append(a[':answer/id'])
    assert valid==[f[':answer-field/correct'][1]], (record['generation'],valid)
    sol=record['question'][':question/worked-solution']
    final=sol.split('&=')[-1].split(r'\end{aligned}')[0].removesuffix('.')
    assert s.simplify(tex_expr(final)-tex_expr(key(record))-(s.Symbol('C') if len(valid)==1 and f[':answer-field/type'].endswith('/blank') else 0))==0
    # The solution's reduced integral must equal the actual served integrand.
    power_form=re.search(r'\\int \\left\((.*?)\\right\)\\,\\mathrm\{d\}x',sol)
    assert power_form and s.simplify(tex_expr(power_form.group(1))-function)==0
    return s.srepr(function)


def grader_checks(record, old=None):
    f=field(record)
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],
                 'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
                 'purpose':'differentiate rendered candidate independently; exactly one match'}
                for a in f[':answer-field/choices']]
    else:
        p=record['generation']['parameters'];a,b=p['a'],p['b']
        checks=[{'submitted':value,'expected':outcome,'purpose':purpose} for value,outcome,purpose in [
            (key(record),'accepted','canonical source-shaped blank'),
            (f'({a}*x^2-({b}))/x','accepted','independently formed equivalent rational expression'),
            (f'{a}*x+({b})/x','rejected','reciprocal integration sign error'),
            (key(record)+'+C','rejected','blank excludes the already supplied integration constant'),
            ('0','rejected','unrelated expression')]]
    if old is not None and f[':answer-field/type'].endswith('/radio'):
        old_value=key(old)
        previous=next(a for a in f[':answer-field/choices'] if a[':answer/value']==old_value)
        checks.append({'submitted_answer_id':previous[':answer/id'],'expected':'rejected','purpose':'counterfactual rejects previously correct bank member'})
    return {'label':str(record['question'][':question/id']), 'record':record,'checks':checks}


def inspect(records):
    groups=collections.defaultdict(list)
    semantic=set()
    for r in records:
        family=r['generation']['template'];p=r['generation']['parameters']
        function=check_math(r);semantic.add((family,function))
        subgroup=family
        if family=='radical':subgroup += ':sqrt-product' if p['target'] in (0,3,4) else ':reciprocal-product'
        groups[subgroup].append(r)
    result={'records':len(records),'semantic_integrands_by_family':len(semantic),'groups':{}}
    for label,rs in groups.items():
        params=[r['generation']['parameters'] for r in rs]
        data={'count':len(rs),'coefficient_sign_pairs':sorted({('+' if p['a']>0 else '-')+('+' if p['b']>0 else '-') for p in params}),
              'a_values':sorted({p['a'] for p in params}),'b_values':sorted({p['b'] for p in params}),
              'p_values':sorted({p['p'] for p in params}) if label=='quotient' else [],
              'degree_values':sorted({p['degree'] for p in params}) if label=='blank' else [],
              'target_counts':dict(collections.Counter(p['target'] for p in params))}
        if label!='blank':
            scores=collections.Counter();positions=collections.Counter()
            static_high=collections.Counter();static_low=collections.Counter()
            for r in rs:
                f=field(r);choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
                k=next(i for i,a in enumerate(choices) if a[':answer/id']==correct);positions[k]+=1
                values=[tex_expr(a[':answer/value']).subs(s.Symbol('C'),0) for a in choices]
                exponents=[max(t.as_powers_dict().get(X,0) for t in s.Add.make_args(v)) for v in values]
                leading=[v.expand().coeff(X**e) for v,e in zip(values,exponents)]
                heuristics={'first':0,'last':4,
                    'shortest':min(range(5),key=lambda j:len(choices[j][':answer/value'])),
                    'longest':max(range(5),key=lambda j:len(choices[j][':answer/value'])),
                    'median_leading_coefficient':sorted(range(5),key=lambda j:leading[j])[2],
                    'largest_static_exponent':max(range(5),key=lambda j:exponents[j]),
                    'smallest_static_exponent':min(range(5),key=lambda j:exponents[j])}
                if label.startswith('radical'):
                    high_power=[j for j,e in enumerate(exponents) if e==s.Rational(5,2)]
                    assert len(high_power)==3
                    heuristics['source_median_among_high_power_candidates']=sorted(high_power,key=lambda j:leading[j])[1]
                for name,j in heuristics.items():scores[name]+=int(j==k)
            n=len(rs)
            data['correct_positions']=dict(positions)
            data['probes']={name:{'successes':v,'attempts':n,'rate':round(v/n,4),'uniform_choice_baseline':0.2} for name,v in scores.items()}
            data['best_fixed_source_candidate']={'successes':max(data['target_counts'].values()),'attempts':n,
                'role_count_in_subgroup':len(data['target_counts'])}
            assert len(data['target_counts'])>1 and len(positions)>1
            assert all(v<n for v in scores.values()), ('perfect incidental predictor',label,scores)
        result['groups'][label]=data
    return result


def prepare(source_path):
    source=json.loads(Path(source_path).read_text())
    source_qs=source['material']['kp'][':knowledge-point/questions']
    specs=[('q-49059',('quotient',1,7,4,0,3)),('q-49063',('radical',1,2,4,0,3)),
           ('q-167635',('blank',1,2,4,0,3)),('q-167587',('blank',1,2,4,0,3)),('q-167617',('blank',2,-4,4,0,2))]
    replays=[];replay_report=[]
    for name,args in specs:
        q=next(q for q in source_qs if q.get(':question/math-academy-id')==name)
        r=g.generate(*args);replays.append(r);check_math(r)
        sf=q[':question/answer-fields'][0]
        original=[tex_expr(a[':answer/value']) for a in sf[':answer-field/choices']]
        generated=[tex_expr(a[':answer/value']) for a in field(r)[':answer-field/choices']]
        matches=[[j for j,v in enumerate(generated) if s.simplify(v-o)==0] for o in original]
        assert all(len(js)==1 for js in matches) and len(original)==len(generated)
        assert s.simplify(tex_expr(sf[':answer-field/correct'][':answer/value'])-tex_expr(key(r)))==0
        replay_report.append({'source_id':q[':question/id'],'math_academy_id':name,
            'original_difficulty':q[':question/difficulty'][':db/ident'],
            'matched_choices':len(matches),'total_choices':len(original),'correct_designation_matches':True,
            'complete_bank':True,'prompt_context_repair':args[0]=='blank',
            'source_answer_values':[a[':answer/value'] for a in sf[':answer-field/choices']],
            'generated_answer_values':[a[':answer/value'] for a in field(r)[':answer-field/choices']]})
    save('source-replay.json',{'cases':replay_report,'complete_banks':5,'radio_choices_matched':10,'blank_choices_matched':3,
          'limits':'Three blank prompts restored from explicit solution functions; not literal source prompt reproduction. All moderate source banks included.'})
    save('source-records.json',replays)
    rng=random.Random(9041);controlled=[];counter=[];checks=[]
    # All permitted role assignments and boundary feature categories, not huge seed sweeps.
    for family in ('quotient','radical'):
        for a,b in ((1,1),(3,-4),(-2,4),(-3,-1)):
            for p in ([3,4,5] if family=='quotient' else [4]):
                old=None
                for target in range(5):
                    order=list(range(5));rng.shuffle(order)
                    r=g.generate(family,a,b,p,target,order=order)
                    controlled.append(r);checks.append(grader_checks(r,old))
                    if old is not None:
                        assert field(r)[':answer-field/choices']!=field(old)[':answer-field/choices'] # IDs are owned by new prompt
                        assert set(a[':answer/value'] for a in field(r)[':answer-field/choices'])==set(a[':answer/value'] for a in field(old)[':answer-field/choices'])
                        assert s.simplify(tex_expr(key(r))-tex_expr(key(old)))!=0
                        assert s.simplify(integrand(r)-integrand(old))!=0
                        counter.append({'kind':'changed-key-same-bank','before':old['question'][':question/id'],'after':r['question'][':question/id']})
                    old=r
    for degree in (2,3):
        for a,b in ((1,1),(4,-8),(-1,8),(-4,-1)):
            r=g.generate('blank',a,b,degree=degree);controlled.append(r);checks.append(grader_checks(r))
    # Exhaust the repaired structural slot, rather than enlarging random sweeps.
    assert len(g.QUOTIENT_PAIRINGS) == 14
    for p in (3,4,5):
        for pairing in g.QUOTIENT_PAIRINGS:
            old = None
            for target in range(5):
                order=list(range(5));rng.shuffle(order)
                r=g.generate('quotient',2,3,p,target,order=order,reciprocal_exponents=pairing)
                controlled.append(r);checks.append(grader_checks(r))
                # Same denominator and same bank, changed numerator/primitive role.
                if pairing[target] == -1:
                    if old is not None:
                        assert set(a[':answer/value'] for a in field(r)[':answer-field/choices']) == set(a[':answer/value'] for a in field(old)[':answer-field/choices'])
                        assert key(r) != key(old) and integrand(r) != integrand(old)
                        assert r['question'][':question/worked-solution'] != old['question'][':question/worked-solution']
                        checks.append(grader_checks(r,old))
                        counter.append({'kind':'changed-polynomial-role-same-denominator-and-bank',
                                        'before':old['question'][':question/id'],'after':r['question'][':question/id']})
                    old=r
    blank=g.generate('blank',2,4,degree=2)
    changed=g.generate('blank',2,-4,degree=2)
    irrelevant=g.generate('blank',2,4,degree=3)
    assert key(blank)!=key(changed) and key(blank)==key(irrelevant)
    counter += [{'kind':'blank-relevant-sign','before':blank,'after':changed},
                {'kind':'blank-irrelevant-degree','before':blank,'after':irrelevant}]
    for r in (blank,changed,irrelevant):
        controlled.append(r);checks.append(grader_checks(r))
    for family in ('quotient','radical'):
        r=g.generate(family,1,2,target=3);other=g.generate(family,1,2,target=3,order=list(reversed(range(5))))
        assert key(r)==key(other) and r['question'][':question/id']==other['question'][':question/id']
        checks.extend([grader_checks(r),grader_checks(other)])
        counter.append({'kind':'choice-order-preserves-answer','before':r,'after':other})
    rejection={}
    normal=g.sample(160,20261020,audit=rejection)
    save('generator-rejection.json',rejection)
    assert normal==g.sample(160,20261020)
    for r in replays+normal:checks.append(grader_checks(r))
    all_records=controlled+normal
    math_instances={check_math(r) for r in all_records}
    # Duplicates intentionally test shared filtering as well as irrelevant order changes.
    save('test-records.json',all_records+replays+[normal[0]])
    save('normal-records.json',normal)
    save('counterfactuals.json',counter)
    save('grader-input.json',checks)
    save('math-and-fidelity.json',{'passed':True,'source_banks':len(replays),'controlled_records':len(controlled),
        'normal_records':len(normal),'distinct_mathematical_integrands':len(math_instances),
        'differentiation_check':'Every rendered candidate independently parsed and differentiated; exactly one matches the rendered prompt.',
        'solution_check':'Final expression and expanded integral parsed from worked solution and matched independently.',
        'determinism':True,'counterfactuals':len(counter),'generator_rejection':'Only duplicate mathematical prompt rejection; no role or sign case rejected.',
        'source_sha256':hashlib.sha256(Path(source_path).read_bytes()).hexdigest()})
    save('coverage-before.json',{'normal':inspect(normal),'combined':inspect(all_records)})
    # Render each source family, both radical forms, and a negative result.
    previews=[replays[0],replays[1],replays[4],g.generate('radical',-2,3,target=2),
              g.generate('quotient',2,3,target=0,reciprocal_exponents=(-3,-2,-1,-1,-1)),
              g.generate('quotient',2,3,target=3,reciprocal_exponents=(-1,-2,-1,-3,-1)),
              g.generate('quotient',2,3,target=4,reciprocal_exponents=g.SOURCE_RECIPROCALS)]
    save('render-records.json',previews)
    print(json.dumps({'source_banks':5,'matched_source_choices':13,'controlled':len(controlled),'normal':len(normal),
                      'independent_math_checks':len(all_records),'grader_records':len(checks),'counterfactuals':len(counter)}))


def after_delivery(path, normal_path):
    accepted=json.loads(Path(path).read_text());data=inspect(accepted)
    # Use the separately filtered actual sampler batch; prompt-only matching can
    # count controlled records with the same integrand but a different bank twice.
    normal=json.loads(Path(normal_path).read_text())
    result={'combined':data,'normal_survivors':inspect(normal),
        'selection':{'implementation':'engine/rust/question_selection.rs:122-198',
            'read_only_observation':'All accepted records are moderate. Positive moderate weight gives a uniform deterministic SHA256 draw within the sorted fresh moderate candidates; no candidate-role preference in this function.',
            'limitations':['No database IDs or live learner history available.','Moderate weight zero makes this band ineligible.','Legacy unconfigured policy chooses first ID.','Captured inventory can become stale.']}}
    save('pedagogical-variation.json',result)
    save('filtered-grader-input.json',[grader_checks(r) for r in accepted])
    print(json.dumps({'accepted':len(accepted),'normal_survivors':len(normal),
         'groups':{k:{'n':v['count'],'targets':v['target_counts']} for k,v in data['groups'].items()}}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source');parser.add_argument('--after-delivery');parser.add_argument('--normal-accepted')
    args=parser.parse_args()
    if args.source:prepare(args.source)
    elif args.after_delivery:
        if not args.normal_accepted:parser.error('--normal-accepted is required with --after-delivery')
        after_delivery(args.after_delivery,args.normal_accepted)
    else:parser.error('Specify --source or --after-delivery')
