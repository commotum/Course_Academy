#!/usr/bin/env python3
"""Check decision coverage and simple cue strategies before/after real delivery."""
import json
from collections import Counter,defaultdict
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from repair_check import expected,validate,symbol
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence'

def ui_hash(text):
    # learning.js choiceOrder (lines 690-701), for numeric content/item IDs.
    n=2166136261
    for c in text: n=((n^ord(c))*16777619)&0xffffffff
    return n

def analyze(records):
    groups=defaultdict(list); masks=set(); banks=defaultdict(set);semantic=set()
    ui_positions=defaultdict(lambda:defaultdict(Counter)); strategies=defaultdict(Counter)
    for r in records:
        want=validate(r,not r['generation'].get('replay_only'))
        fields=r['question'][':question/answer-fields'];p=r['generation']['profile'];b=r['generation']['bank_profile']
        semantic.add((r['question'][':question/problem'],tuple(f[':answer-field/key'] for f in fields),tuple(want)))
        if fields[0][':answer-field/type'].endswith('/checkbox'):
            response=tuple(i for i,(f,w) in enumerate(zip(fields,want)) if w=='true')
            ordinary=tuple(w for f,w in zip(fields,want) if symbol(f[':answer-field/key']))
            masks.add(ordinary);size=sum(w=='true' for w in ordinary)
            correct_positions=response
        else:
            response=want[0];size=len(__import__('repair_check').selected(response))
            correct_positions=tuple(i for i,a in enumerate(fields[0][':answer-field/choices']) if a[':answer/value']==response)
            banks[b].add(response)
            f=fields[0]
            for item_id in (1,2,3):
                ordered=sorted(f[':answer-field/choices'],key=lambda a:ui_hash(f"{item_id}:{f[':answer-field/id']}:{a[':answer/id']}"))
                index=next(i for i,a in enumerate(ordered) if a[':answer/value']==response)
                ui_positions[(p,b)][item_id][index+1]+=1
        ordinary_subset={i for i,v in enumerate(ordinary) if v=='true'} if fields[0][':answer-field/type'].endswith('/checkbox') else __import__('repair_check').selected(response)
        for label,guess in [('first only',{0}),('last only',{3}),('first two',{0,1}),('last two',{2,3}),('all four',set(range(4))),('none',set())]:
            strategies[(p,b)][label]+=int(ordinary_subset==guess)
        groups[(p,b)].append((str(response),correct_positions,size))
    stats={}
    for (p,b),rows in sorted(groups.items()):
        responses=Counter(row[0] for row in rows);positions=Counter(str(row[1]) for row in rows);counts=Counter(row[2] for row in rows)
        assert len(responses)>1,(p,b,'constant final response')
        stats[p+'/'+b]={'n':len(rows),'responses':dict(responses),
            'best_constant_response':{'successes':max(responses.values()),'attempts':len(rows)},
            'best_fixed_position_strategy':{'successes':max(positions.values()),'attempts':len(rows)},
            'ordinary_correct_counts':dict(counts),
            'fixed_roman_label_or_checkbox_position_strategy_successes':dict(strategies[(p,b)]),
            'ui_radio_correct_ordinals_for_item_ids_1_2_3':{str(k):dict(v) for k,v in ui_positions[(p,b)].items()}}
    assert len(masks)==16
    import generator as g
    for b,bank in g.RADIO_BANKS.items(): assert banks[b]==set(bank),(b,banks[b])
    return {'record_count':len(records),'semantic_instances':len(semantic),'checkbox_truth_patterns':len(masks),
        'radio_choice_outcomes':{b:sorted(v) for b,v in banks.items()},'within_template_cues':stats,
        'interpretation':'All template/profile groups have varying final responses. Fixed-position strategy is compared with the empirical best constant-response baseline. No tested strategy is universally successful; symbol semantics (e.g. C contains every real target) are intended lesson rules. Finite radio banks limit feasible subsets, so partial bank-derived information is not claimed eliminated.'}

before=json.loads((OUT/'delivery-input.json').read_text());after=json.loads((OUT/'delivery/accepted.json').read_text())
result={'before':analyze(before),'after':analyze(after),'delivery':json.loads((OUT/'delivery/delivery.json').read_text()),
    'generator_rejection':'No truth-based resampling: choose feasible bank subset first, then compatible candidates. Only within-batch identical question IDs resample; unique content checked by delivery.',
    'selection_limits':'Current learning.rs:149-171 rejects all-false checkbox fields, retired/free/multistep questions. These new records have explicit true checkbox or one radio answer, no retirement, free fields or multistep layout. question_selection.rs groups by difficulty and draws within easy when easy has positive weight. Live policy, learner history and reservations were not supplied; no claim about actual per-learner exposure. Cached native eligibility discrepancy from prior review is not counted as source-rule verification.'}
(OUT/'pedagogical-variation.json').write_text(json.dumps(result,indent=2)+'\n')
# Six noninterchangeable response layouts/repair cases for the unmodified UI.
samples=json.loads((OUT/'samples.json').read_text());selected=[]
for b,p in [('radio-0','root'),('radio-1','decimal'),('radio-2','universal'),('radio-10','universal')]:
    selected.append(next(r for r in samples if r['generation']['bank_profile']==b and r['generation']['profile']==p))
selected.append(json.loads((OUT/'retained-counterexamples.json').read_text())[1])
selected.append(json.loads((OUT/'source-replays.json').read_text())[3])
(OUT/'render-records.json').write_text(json.dumps(selected,indent=2)+'\n')
print(json.dumps({'before':len(before),'after':len(after),'truth_patterns_before_after':[result['before']['checkbox_truth_patterns'],result['after']['checkbox_truth_patterns']],'radio_bank_outcomes':{b:len(v) for b,v in result['after']['radio_choice_outcomes'].items()},'subgroups':len(result['after']['within_template_cues']),'render_records':len(selected)}))
