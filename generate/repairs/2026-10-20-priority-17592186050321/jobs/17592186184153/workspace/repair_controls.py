"""Resolve the observed n=5 sampling gap and inspect synthetic learner selection.
All controls retain the same integrand per sign/order; only wrong divisor roles change.
"""
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import random
import sys
import generator as G
import repair_validate as R
import validate as T
OUT=Path('evidence/repair')

def prepare():
    rs=[]
    for s in (-1,1):
        for order in (False,True):
            for ds in ((2,3),(2,8),(7,8)):
                i=G.instance('P',5,s,-4,'x',order,factors=[str(F(6,d)) for d in ds],omitted_row=1,omitted_col=2)
                r=G.build(i,random.Random(42));T.verify(r);rs.append(r)
    R.save('rank-controls.json',rs)
    R.save('rank-controls-grader-input.json',[T.make_checks(r,'n5 divisor rank control') for r in rs])
    print(json.dumps({'controls':len(rs),'reason':'Fresh random n=5 subgroup had only magnitude rank zero after matching constant; test all three ranks with the integrand fixed.'}))

def after():
    controls=json.loads((OUT/'rank-controls-delivery/accepted.json').read_text())
    assert len(controls)==12
    probe=R.conditional(controls)
    assert set(probe['groups']['all']['magnitude_ranks_after_constant'])=={0,1,2}
    R.save('rank-controls-shortcuts.json',probe)
    # Demonstrate controlled invariance of the correct response while incidental ranks change.
    groups={}
    for s in (-1,1):
        for order in (False,True):
            group=[r for r in controls if r['generation']['parameters']['s']==s and r['generation']['parameters']['constant_first']==order]
            assert len({T.correct_value(r) for r in group})==1
            ids={r['question'][':question/id'] for r in group}
            ranks={t['magnitude_rank_after_constant'] for t in probe['trials'] if t['id'] in ids}
            assert ranks=={0,1,2}
            groups[f's={s},order={order}']={'records':len(group),'constant_matched_correct_ranks':sorted(ranks),'same_prompt_solution_key':len({json.dumps([r['question'][':question/problem'],r['question'][':question/worked-solution'],T.correct_value(r)]) for r in group})==1}
    delivered=json.loads((OUT/'delivery/accepted.json').read_text())
    lookup={r['question'][':question/id']:r for r in delivered+controls}
    ids=sorted(lookup)
    draws=[]
    for j in range(1024):
        digest=hashlib.sha256(f'course-academy/question-selection/v1/author-repair-{j}'.encode()).digest()
        u=(int.from_bytes(digest[8:16],'big')>>11)/(2**53)
        draws.append(lookup[ids[int(u*len(ids))]])
    selected_ids={r['question'][':question/id'] for r in draws}
    selected=[lookup[q] for q in ids if q in selected_ids]
    controls_selected=[r for r in selected if r['question'][':question/id'] in {c['question'][':question/id'] for c in controls}]
    assert len(controls_selected)>0
    R.save('selection-records.json',selected)
    R.save('shortcut-selection.json',R.conditional(selected))
    R.save('coverage-selection.json',T.coverage(selected))
    R.save('selection.json',{'rule':'question_selection.rs select() lines 125-197: one positive-weight moderate band, SHA256 uniform(8)',
             'pool':len(ids),'normal_delivered':len(delivered),'targeted_controls_delivered':len(controls),
             'draws':len(draws),'unique_selected':len(selected),'templates':dict(Counter(r['generation']['template'] for r in draws)),
             'selected_control_records':len(controls_selected),
             'semantics_delivered':len({T.semantic(r) for r in lookup.values()}),'semantics_selected':len({T.semantic(r) for r in selected}),
             'limits':['Uses synthetic sorted UUID order instead of unavailable database entity IDs; validates uniform within-band membership, not actual live draws.',
                       'Learner history, zero moderate weight, database identity collisions and concurrent inventory changes are unavailable offline.',
                       'Without a difficulty policy the selector returns the first database ID; live ordering is not inferred.',
                       'Targeted controls are validation inputs admitted by the same generator domain, not forced sampling quotas.']})
    R.save('rank-controls-results.json',{'groups':groups,'passes':True,'interpretation':'The eight n=5 fresh normal records alone all had constant-matched magnitude rank zero. Twelve delivered controls with the same method and fixed integrands show every rank for each sign/order; the observed correlation is not a domain invariant. No claim of forced empirical balance.'})
    print(json.dumps({'controls':len(controls),'ranks':[0,1,2],'selected_controls':len(controls_selected),'selection_pool':len(ids)}))

if __name__=='__main__':after() if '--after-delivery' in sys.argv else prepare()
