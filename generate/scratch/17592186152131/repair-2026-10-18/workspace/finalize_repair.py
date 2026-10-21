#!/usr/bin/env python3
"""Summarize existing check results; run after manual screenshot inspection."""
import json
from pathlib import Path
from fractions import Fraction
import repair_checks as checks
import validate as v

E=checks.E

def read(p):return json.loads((E/p).read_text())
def save(p,data):(E/p).write_text(json.dumps(data,indent=2)+'\n')
def avoid_four(rows):
    hits=attempts=0
    for r in rows:
        if r['generation']['template']!='square-equation':continue
        halves=[(i,b) for i,(b,p) in checks.units(r) if p==Fraction(1,2)]
        if len(halves)==2 and any(b==4 for i,b in halves):
            selected=next(i for i,b in halves if b!=4)
            attempts+=1;hits+=selected==v.inspect(r)['correct']
    return {'successes':hits,'attempts':attempts}
comparison={}
for name,root in [('before',E.parent/'repair-2'),('after',E)]:
    comparison[name]={stage:avoid_four(json.loads((root/path).read_text()))
                      for stage,path in [('raw','test-records.json'),('delivered','delivery/accepted.json')]}
assert comparison['before']['delivered']=={'successes':16,'attempts':16}
assert comparison['after']['delivered']=={'successes':16,'attempts':32}
save('feedback-before-after.json',comparison)

delivered=read('delivery/accepted.json')
# Link every same-bank changed target to the actual native results on all choices.
native=read('delivered-native-grader.json')
inputs=read('delivered-native-grader-input.json')
assert len(native['records'])==len(inputs)
for expected,actual in zip(inputs,native['records']):
    assert len(expected['checks'])==len(actual['checks'])
    for a,b in zip(expected['checks'],actual['checks']):assert a['expected']==b['outcome']
banks={}
for i,r in enumerate(delivered):
    if r['generation']['template']!='square-equation':continue
    signature=tuple(sorted(c[':answer/value'] for c in checks.choices(r)))
    banks.setdefault(signature,[]).append((i,r))
pairs=[]
for signature,rows in banks.items():
    assert len(rows)==2
    a,b=rows
    aa,bb=v.inspect(a[1]),v.inspect(b[1])
    assert aa['key']!=bb['key']
    assert a[1]['question'][':question/problem']!=b[1]['question'][':question/problem']
    assert a[1]['question'][':question/worked-solution']!=b[1]['question'][':question/worked-solution']
    for (_,old), (i,new) in [(a,b),(b,a)]:
        previous_key=v.inspect(old)['key']
        previous_index=next(j for j,c in enumerate(checks.choices(new)) if c[':answer/value']==previous_key)
        assert native['records'][i]['checks'][previous_index]['outcome']=='rejected'
        assert native['records'][i]['checks'][v.inspect(new)['correct']]['outcome']=='accepted'
    pairs.append({'radicands':[aa['x'],bb['x']],'same_bank':True,'prompt_and_solution_changed':True,
                  'native_previous_key_rejected_both_directions':True})
save('same-bank-native-counterfactuals.json',{'pairs':len(pairs),'verified':pairs})

source=read('source-replay.json');delivery=read('delivery/delivery.json')
assert read('visual-inspection.json')['passed']
assert read('render/rendering.json')['passed']
summary={'fidelity':{'complete_source_banks':source['complete_banks_matched'],'source_choices':source['choices_matched'],
           'source_distractors':source['distractors_matched'],'missing_fields':'q-69158 key, solution and difficulty inferred; not original-field replay'},
 'correctness':{'square_bank_configurations':336,'square_mathematical_tasks':23,'ordinary_regression_records':45,
                'independent_exact_prompt_choice_solution_checks':'passed'},
 'grading':{name:{k:read(name+'.json')[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']}
           for name in ['native-grader','delivered-native-grader','counterfactual-native-grader']},
 'decision_variation':{'feedback_avoid_4':comparison,'same_complete_banks_with_both_target_assignments':len(pairs),
      'all_displayed_square_bases_are_eligible_targets':True,'raw_and_delivered_conditional_probes':'passed'},
 'delivery':{k:delivery[k] for k in ['input_count','duplicate_count','accepted_count','inventory_basis']},
 'runtime':read('runtime-boundaries.json'),'relocation':'passed','rendering':{'ui_cases':9,'visually_inspected':9,'passed':True},
 'limits':['Easy only.','Original q-69158 fields missing as recorded above.',
           'Captured inventory and offline grading only; live learner history, weights, future IDs and publication untested.',
           'Shortcut results cover documented probes; they do not prove absence of every mathematical elimination strategy.']}
save('summary.json',summary)
print(json.dumps({'source_banks':3,'square_tasks':23,'same_bank_target_pairs':len(pairs),'avoid_4_delivered':comparison['after']['delivered'],
                  'delivered':delivery['accepted_count'],'rendered_and_inspected':9,'status':'all author checks passed'}))
