"""Independent visible-record coverage after the real delivery filter."""
import json, collections
from pathlib import Path
from math_witness import inspect, equations
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence'
def load(p):return json.loads((OUT/p).read_text())
def bank_groups(records):
    groups=collections.defaultdict(list)
    for r in records:
        i=inspect(r)
        # Group by visible coefficient expressions, vector shape and ordered values.
        q=r['question']; shape='angle' if q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'].startswith('⟨') else 'column'
        lhs=tuple(str(e-e.subs({v:0 for v in e.free_symbols})) for e in equations(q))
        groups[(lhs,shape,str(i['bank']))].append(i)
    return groups
before=bank_groups(load('controlled.json'));after=bank_groups(load('delivery-controlled/accepted.json'))
assert set(before)==set(after)
for k,rows in after.items():
    assert len(rows)==5 and {r['correct_index'] for r in rows}==set(range(5))
# The same bank can be keyed to every option: any deterministic bank-only rule,
# including all review predicates and rank/tie/count heuristics, scores at most 1/5.
report={'controlled':{'before':sum(map(len,before.values())),'after':sum(map(len,after.values())),'groups':len(after),'every_fixed_bank_correct_indices':[0,1,2,3,4],'max_bank_only_success_per_group':'1/5'},'normal':{},'batch':{}}
for label in ('normal','batch'):
    rows=load(label+'.json');survivors=load('delivery-'+label+'/accepted.json')
    report[label]={'before':len(rows),'after':len(survivors),'before_positions':dict(collections.Counter(inspect(r)['correct_index'] for r in rows)),'after_positions':dict(collections.Counter(inspect(r)['correct_index'] for r in survivors)),'semantic_systems':len({tuple(inspect(r)['equations']) for r in survivors})}
    assert len(survivors)>0
report['selection']={'inspection':'engine/rust/question_selection.rs::seen_before_task/select','facts':['Seen questions and current prefix are excluded upstream; rated band selection then uses configured weights and hash choice.','All candidates here are easy; a positive easy weight allows selection. No configured distribution chooses first sorted candidate.','Selection does not inspect coordinate signs, equality or role assignments.'],'limits':['Live learner history and policy were not supplied. Arbitrary history exclusions may remove tested counterfactual partners; no claim of per-learner balance or universal shortcut absence.']}
(OUT/'delivery-probes.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
