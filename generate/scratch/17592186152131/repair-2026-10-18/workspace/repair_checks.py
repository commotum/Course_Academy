#!/usr/bin/env python3
"""Targeted review-3 repair checks; no database access or publication.
Run: python repair_checks.py build
     python repair_checks.py delivered
"""
import collections
from fractions import Fraction
import json
from pathlib import Path
import re
import sys

import generator as g
import validate as v

E = Path(__file__).resolve().parent / 'evidence' / 'repair-3'
E.mkdir(parents=True, exist_ok=True)
v.E = E

def save(name, obj):
    v.save(name, obj)

def load(name):
    return json.loads((E / name).read_text())

def choices(r):
    return r['question'][':question/answer-fields'][0][':answer-field/choices']

def units(r):
    return [(i, v.parse(c[':answer/value'])) for i,c in enumerate(choices(r))
            if re.search(r'\^\{1/',c[':answer/value'])]

def strategy(r, name):
    # Exact original strategy extended naturally to multiple matching options:
    # first decimal candidate, otherwise first maximum-base candidate.
    u = units(r)
    decimal = [i for i,_ in u if '.' in choices(r)[i][':answer/value'].split('^')[0]]
    if name == 'reported-decimal-else-larger':
        return decimal[0] if decimal else max(u,key=lambda a:a[1][0])[0]
    if name == 'larger-unit-base': return max(u,key=lambda a:a[1][0])[0]
    if name == 'smaller-unit-base': return min(u,key=lambda a:a[1][0])[0]
    if name == 'first-numerator-1': return u[0][0]
    if name == 'last-numerator-1': return u[-1][0]
    if name == 'decimal-first' and decimal: return decimal[0]
    if name == 'smallest-unit-denominator': return min(u,key=lambda a:1/a[1][1])[0]
    if name == 'largest-unit-denominator': return max(u,key=lambda a:1/a[1][1])[0]
    if name in ('most-frequent-base/half-power','least-frequent-base/half-power'):
        vals=[v.parse(c[':answer/value']) for c in choices(r)]
        freq=collections.Counter(b for b,p in vals)
        eligible=[i for i,(b,p) in enumerate(vals) if p==Fraction(1,2)]
        if eligible:
            select=max if name.startswith('most') else min
            return select(eligible,key=lambda i:freq[vals[i][0]])
    return None

PROBES = ('reported-decimal-else-larger','larger-unit-base','smaller-unit-base',
          'first-numerator-1','last-numerator-1','decimal-first',
          'smallest-unit-denominator','largest-unit-denominator',
          'most-frequent-base/half-power','least-frequent-base/half-power')

def audit(records, stage):
    groups=collections.defaultdict(list)
    for r in records:
        a=v.inspect(r)
        groups[r['generation']['template']].append((r,a))
    report={'records':len(records),'semantic_instances':len({(a['x'],a['n']) for rows in groups.values() for r,a in rows}),
            'blind_radio_baseline':0.2,'groups':{}, 'attempts':[]}
    for template,rows in groups.items():
        subgroups={'all':rows}
        for dtype in ('integer','decimal'):
            part=[(r,a) for r,a in rows if a['decimal']==(dtype=='decimal')]
            if part: subgroups[dtype]=part
        if template=='square-equation':
            assert all(r['generation']['profile']=='square-index-confusion' for r,a in rows)
            assert {r['generation']['foil_index'] for r,a in rows}=={1,3,4,5}
            assert {a['case'] for r,a in rows}=={'x<n','x=n','x>n'}
            for foil in (1,3,4,5):
                subgroups[f'foil-{foil}']=[(r,a) for r,a in rows if r['generation']['foil_index']==foil]
                for dtype in ('integer','decimal'):
                    subgroups[f'{dtype}/foil-{foil}']=[(r,a) for r,a in rows if r['generation']['foil_index']==foil and a['decimal']==(dtype=='decimal')]
            for direction in (-1,1):
                subgroups[f'base-direction-{direction}']=[(r,a) for r,a in rows if r['generation']['base_direction']==direction]
            for r,a in rows:
                u=units(r)
                same=[i for i,(b,p) in u if b==Fraction(a['x'])]
                assert len(same)==2 and a['correct'] in same
                # Every decimal-base and maximum-base candidate strategy has
                # at least two indistinguishable bases when it could be right.
                surf=[i for i,(b,p) in u if '.' in choices(r)[i][':answer/value'].split('^')[0]]
                if not surf:
                    largest=max(b for i,(b,p) in u)
                    surf=[i for i,(b,p) in u if b==largest]
                assert surf!=[a['correct']]
            assert {a['position'] for r,a in rows}==set(range(5))
        entry={}
        for label,part in subgroups.items():
            if not part: continue
            n=len(part)
            item={'count':n,'cases':dict(collections.Counter(a['case'] for r,a in part)),
                  'positions':dict(collections.Counter(a['position'] for r,a in part)),
                  'ranks':dict(collections.Counter(a['rank'] for r,a in part)),
                  'foil_indices':dict(collections.Counter(r['generation'].get('foil_index') for r,a in part)),
                  'probes':{}}
            for name in PROBES:
                attempts=[(r,a,strategy(r,name)) for r,a in part if strategy(r,name) is not None]
                hits=sum(i==a['correct'] for r,a,i in attempts)
                item['probes'][name]={'successes':hits,'attempts':len(attempts)}
                if template=='square-equation' and name in ('reported-decimal-else-larger','larger-unit-base','smaller-unit-base','first-numerator-1','last-numerator-1','decimal-first','most-frequent-base/half-power','least-frequent-base/half-power') and attempts:
                    assert hits<len(attempts),(stage,template,label,name,hits,len(attempts))
            item['best_fixed_position']=max(collections.Counter(a['position'] for r,a in part).values())
            item['best_fixed_numeric_rank']=max(collections.Counter(a['rank'] for r,a in part).values())
            if template=='square-equation':
                assert item['best_fixed_position']<n
                assert item['best_fixed_numeric_rank']<n
            entry[label]=item
        report['groups'][template]=entry
        if template=='square-equation':
            for r,a in rows:
                selected=strategy(r,'reported-decimal-else-larger')
                report['attempts'].append({'question_id':r['question'][':question/id'],'prompt':r['question'][':question/problem'],
                    'foil_index':r['generation']['foil_index'],'selected':choices(r)[selected][':answer/value'],
                    'key':a['key'],'success':selected==a['correct']})
    return report

def conditional_bases(records):
    """Read the complete served bank, without relying on generator metadata."""
    rows=[r for r in records if r['generation']['template']=='square-equation']
    banks=collections.defaultdict(list)
    for r in rows:
        signature=tuple(sorted(c[':answer/value'] for c in choices(r)))
        banks[signature].append(r)
    paired=[]
    for signature, part in banks.items():
        half={b for b,p in map(v.parse,signature) if p==Fraction(1,2)}
        targets={Fraction(v.inspect(r)['x']) for r in part}
        assert targets==half,(signature,targets,half)
        paired.append({'bank':signature,'eligible_targets':sorted(map(str,half)),
                       'observed_targets':sorted(map(str,targets))})
    avoids={}
    all_bases={b for r in rows for _,(b,p) in units(r)}
    for base in sorted(all_bases):
        # Answer-only conditional shortcut: avoid this base in a two-base bank.
        applicable=[]
        for r in rows:
            halves=[(i,b) for i,(b,p) in units(r) if p==Fraction(1,2)]
            if any(b==base for i,b in halves):
                selected=next(i for i,b in halves if b!=base)
                applicable.append((r,selected))
        hits=sum(i==v.inspect(r)['correct'] for r,i in applicable)
        assert 0<hits<len(applicable),(base,hits,len(applicable))
        avoids[str(base)]={'successes':hits,'attempts':len(applicable)}
    return {'same_bank_groups':len(banks),'all_complete_banks_have_both_targets':True,
            'avoid_base_probes':avoids,'bank_pairs':paired}

def build():
    source=json.loads((E.parents[2]/'source/source.json').read_text())
    original=next(value for value in source['material'].values() if isinstance(value,dict) and ':knowledge-point/questions' in value)
    captured=json.loads((v.ROOT/'source_cases.json').read_text())
    assert captured['questions']==original[':knowledge-point/questions']
    assert captured['canonical']==original[':knowledge-point/canonical-example']
    replay=v.source_checks()
    controlled,cross=v.controlled()
    # Unchanged indexed implementation gets a small ordinary regression sample.
    normal=[]
    for seed in (0,1,2,3,4,7,25,92718,1033798965):
        batch=g.generate_batch('easy',5,seed)
        assert batch==g.generate_batch('easy',5,seed)
        assert len({(str(r['generation']['parameters']['x']),r['generation']['parameters']['n']) for r in batch})==5
        normal.extend(batch)
    assert any(r['generation']['parameters']=={'x':4,'n':2} for r in normal)
    save('seeded-records.json',normal)
    sampled_square=[r for r in normal if r['generation']['template']=='square-equation']
    assert {r['generation']['foil_index'] for r in sampled_square}=={1,3,4,5}
    assert {r['generation']['base_direction'] for r in sampled_square}=={-1,1}
    assert {r['generation']['inverted_base'] for r in sampled_square}=={'target','other'}
    save('seeded-coverage.json',{'records':len(normal),'seeds':[0,1,2,3,4,7,25,92718,1033798965],
         'square_records':len(sampled_square),
         'foil_indices':dict(collections.Counter(r['generation']['foil_index'] for r in sampled_square)),
         'base_directions':dict(collections.Counter(r['generation']['base_direction'] for r in sampled_square)),
         'inverted_bases':dict(collections.Counter(r['generation']['inverted_base'] for r in sampled_square)),
         'gap_resolution':'Retained seed 7 for foil denominator 3; added review seed 92718 and seed 25, the first seed in 0..29 reaching square target 4.'})
    square=[g.generate(x,n,'square-equation',foil_index=m,base_direction=d,inverted_base=b,order_seed=1000+16*i+4*j+2*(d==1)+(b=='other'))
            for i,(x,n) in enumerate(g.domain('square-equation')) for j,m in enumerate((1,3,4,5)) for d in g.square_neighbors(x) for b in ('target','other')]
    # Source/boundaries are checked first, before expanding the affected square domain.
    for r in replay+controlled+square+normal:v.inspect(r)
    records=square+normal
    save('test-records.json',records)
    report=audit(records,'raw')
    save('conditional-base-raw.json',conditional_bases(square))
    report['affected_square_instances']=len(square)
    report['affected_square_numeric_instances']=len(g.domain('square-equation'))
    report['sampler']='No rejection loop; profile-specific valid numeric domains, without replacement within each batch; square denominator-case chosen before radicand.'
    report['selection_limits']=['Captured-inventory delivery only. Prior read-only selector review still applies: history/policy unavailable; no actual learner draw is claimed.']
    save('raw-variation.json',report)
    # A bank-only controlled change must preserve both key and solution.
    banks=[g.generate('3.5',2,'square-equation',foil_index=m,inverted_base=b,order_seed=91)
           for m in (1,3,4,5) for b in ('target','other')]
    assert len({v.inspect(r)['key'] for r in banks})==1
    assert len({r['question'][':question/worked-solution'] for r in banks})==1
    assert len({r['question'][':question/problem'] for r in banks})==1
    assert len({r['question'][':question/id'] for r in banks})==8
    roles=[g.generate(7,2,'square-equation',foil_index=3,base_direction=1,inverted_base='target',order_seed=91),
           g.generate(8,2,'square-equation',foil_index=3,base_direction=-1,inverted_base='other',order_seed=91)]
    assert sorted(c[':answer/value'] for c in choices(roles[0]))==sorted(c[':answer/value'] for c in choices(roles[1]))
    assert v.inspect(roles[0])['key']!=v.inspect(roles[1])['key']
    assert roles[0]['question'][':question/problem']!=roles[1]['question'][':question/problem']
    assert roles[0]['question'][':question/worked-solution']!=roles[1]['question'][':question/worked-solution']
    save('bank-counterfactual-records.json',banks+roles)
    save('bank-counterfactual.json',{'irrelevant_bank_changes':{'fixed_prompt':True,'fixed_key':True,'fixed_solution':True,'distinct_banks':8,'foil_indices':[1,3,4,5]},
         'relevant_target_swap':{'same_complete_bank':True,'radicands':[7,8],'keys':[v.inspect(r)['key'] for r in roles],
         'prompt_and_solution_change':True}})
    save('native-grader-input.json',v.grader_cases(replay+controlled+records+banks+roles,'repair3')+cross)
    render=[g.generate(x,2,'square-equation',foil_index=m,base_direction=d,inverted_base=b,order_seed=m)
            for x,m,d,b in ((10,1,-1,'other'),(10,3,1,'target'),('1.5',4,-1,'other'),('3.5',5,1,'target'))]
    render+= [g.generate(2,7,'indexed-what'),g.generate(7,3,'indexed-equation'),replay[1]]
    render += [g.generate(x,2,'square-equation',foil_index=1,base_direction=d,inverted_base=b,order_seed=91)
               for x,d,b in ((3,1,'target'),(4,-1,'other'))]
    save('render-records.json',render)
    save('summary.json',{'source_banks':3,'source_choices':15,'square_instances':len(square),
        'square_numeric_instances':len(g.domain('square-equation')),'regression_records':len(normal),
        'controlled_pairs':6,'bank_counterfactuals':8,'all_independent_math_checks':'passed',
        'determinism':'passed','next':'delivery, native grader, relocation and visual inspection'})
    print(json.dumps(load('summary.json')))

def delivered():
    records=load('delivery/accepted.json')
    report=audit(records,'delivered')
    save('delivered-variation.json',report)
    save('conditional-base-delivered.json',conditional_bases(records))
    raw=load('test-records.json')
    keys=lambda rows:{(str(r['generation']['parameters']['x']),r['generation']['parameters']['n'],r['generation'].get('foil_index'),r['generation'].get('base_direction'),r['generation'].get('inverted_base')) for r in rows if r['generation']['template']=='square-equation'}
    assert keys(raw)==keys(records),'Delivery removed an affected square case'
    attempts=[]
    for i,r in enumerate(records):
        if r['generation']['template']!='square-equation':continue
        selected=strategy(r,'reported-decimal-else-larger')
        correct=v.inspect(r)['correct']
        attempts.append({'label':f'reported-strategy-delivered-{i}','record':r,'checks':[
            {'submitted_answer_id':choices(r)[selected][':answer/id'],
             'expected':'accepted' if selected==correct else 'rejected','purpose':'Native reproduction of reported surface shortcut after repair'}]})
        halves=[(j,b) for j,(b,p) in units(r) if p==Fraction(1,2)]
        if any(b==4 for j,b in halves):
            avoid_four=next(j for j,b in halves if b!=4)
            attempts.append({'label':f'avoid-4-delivered-{i}','record':r,'checks':[
                {'submitted_answer_id':choices(r)[avoid_four][':answer/id'],
                 'expected':'accepted' if avoid_four==correct else 'rejected',
                 'purpose':'Feedback conditional avoid-4 strategy after shared delivery'}]})
    bank_delivered=load('bank-counterfactual-delivery/accepted.json')
    assert len(bank_delivered)==10
    role_rows=[r for r in bank_delivered if r['generation']['parameters']['x'] in (7,8)]
    assert len(role_rows)==2
    by_x={r['generation']['parameters']['x']:r for r in role_rows}
    old_key=v.inspect(by_x[7])['key']
    wrong=next(c for c in choices(by_x[8]) if c[':answer/value']==old_key)
    target_case={'label':'same-square-bank-target-swap-rejects-former-key','record':by_x[8],
                'checks':[{'submitted_answer_id':wrong[':answer/id'],'expected':'rejected','purpose':'Only target radicand changes; previous key is now a distractor'}]}
    save('delivered-native-grader-input.json',v.grader_cases(records+bank_delivered,'repair3-delivered')+attempts+[target_case])
    save('delivery-comparison.json',{'raw_count':len(raw),'accepted_count':len(records),
        'square_bank_instances_before':len(keys(raw)),'square_bank_instances_after':len(keys(records)),
        'square_domain_preserved':True,'limits':'No learner history/configured policy provided; actual draw and live database identity collisions untested.'})
    print(json.dumps(load('delivery-comparison.json')))

if __name__=='__main__':
    if sys.argv[1]=='build':build()
    elif sys.argv[1]=='delivered':delivered()
    else:raise SystemExit('Use build or delivered')
