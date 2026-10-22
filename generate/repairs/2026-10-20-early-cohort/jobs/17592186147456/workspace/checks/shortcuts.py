"""Within-family cue checks, before/after delivery, plus normal-sampler coverage."""
import random
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate as v

before=v.json.loads((v.E/'records.json').read_text())
after=[]
for band in ('easy','moderate'):
    after+=v.json.loads((v.E/f'delivery-{band}/accepted.json').read_text())
assert v.coverage(before)==v.coverage(after),'Delivery lost a decision case'
reports={}; normal=[]
for t,(level,_) in v.g.CASES.items():
    group=[r for r in after if r['generation']['template']==t]
    masks={tuple(v.flags(r['question'])) for r in group}
    expected=set(v.feasible_cases(t))
    assert masks==expected
    # The same x-function family, row labels and coefficient vector must yield
    # different answer subsets, not just different equations or UUIDs.
    fixed=[r for r in group if r['generation']['parameters']['left_scales']==[2,3,4] and r['generation']['parameters']['right_scales']==[3,4,5]]
    assert {tuple(v.flags(r['question'])) for r in fixed}==expected
    assert len({sum(m) for m in masks})>1,'Choice count fixed within family'
    mutable=[i for i in range(3) if len({m[i] for m in expected})>1]
    for i in mutable:assert {m[i] for m in masks}=={False,True}
    # Test the ordinary seeded path, without explicit decisions or coefficients.
    seen={};seeds=[]
    for seed in range(64):
        r=v.g.generate(level,seed,t)
        visible=tuple(v.independent_truth(e) for e in v.prompt_equations(r['question'][':question/problem']))
        assert tuple(v.flags(r['question']))==visible
        assert visible in expected
        if visible not in seen:seen[visible]=r;seeds.append(seed)
        if set(seen)==expected:break
    assert set(seen)==expected,('Normal sampling missed decisions',t)
    normal+=list(seen.values())
    radio_positions=sorted({next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/value']==v.correct_value(r['question'][':question/answer-fields'][0])) for r in group}) if '-radio' in group[0]['generation']['bank_profile'] else None
    reports[t]={'decision_cases':len(masks),'mutable_rows':mutable,'counts':sorted({sum(m) for m in masks}),'radio_correct_positions':radio_positions,'normal_seeds_covering_all_cases':seeds,'normal_draws':seed+1,'coefficient_and_template_cue_counterexamples':True}
v.save(v.E/'normal-sampler-records.json',normal)
v.save(v.E/'coverage-after.json',v.coverage(after))
v.save(v.E/'shortcut-report.json',{'status':'passed','before':len(before),'accepted':len(after),'families':reports,'selection_limits':'Captured delivery/inventory filters exercised. Rust selection chooses band then uniform eligible item, independent of correct labels; learner history and configured live weights unavailable. Generator has no case rejection: feasible cases chosen directly, explicit None preserves empty ordinary subsets. Fixed nonpower rejections are mathematical evidence, not an incidental cue. This audit does not prove absence of all cognitive strategies.'})
print('Within-template labels, counts, positions and coefficient cues: passed; normal sampler covered all cases')
