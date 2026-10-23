"""Executable current-generator regressions for both retained findings.
No runtime edits, services or database writes. Run from any directory.
"""
import json, sys, importlib.util, collections
from pathlib import Path
from math_witness import inspect, equations, vec
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence'; OUT.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('generator',ROOT/'17592186096669.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,v): (OUT/name).write_text(json.dumps(v,indent=2,ensure_ascii=False,default=str))
source=json.loads((ROOT.parent/'source/source.json').read_text())
sq={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
complete={p:q for p,q in sq.items() if q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/correct')}
assert set(complete)==set(g.PARAMETERS)
replays=[]; controlled=[]; normal=[]; reports=[]
for p,q in complete.items():
    r=g.generate(profile=p,scale=1)
    info=inspect(r)
    assert equations(q)==equations(r['question'])
    f=q[':question/answer-fields'][0]
    original=[vec(c[':answer/value']) for c in f[':answer-field/choices']]
    assert original==[vec(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]
    assert tuple(map(str,vec(f[':answer-field/correct'][':answer/value'])))==tuple(info['solution'])
    assert '$=\\begin' not in r['question'][':question/worked-solution']
    replays.append(r)
    # Same exact visible bank and LHSs; only decisive evidence changes.
    group=[g.generate(profile=p,seed=8,target=i,signs=(-1,1,-1),shifts=(2,-2,1)) for i in range(5)]
    observed=[inspect(r) for r in group]
    banks=[v['bank'] for v in observed]
    assert all(b==banks[0] for b in banks)
    assert {v['correct_index'] for v in observed}==set(range(5)),p
    assert len({tuple(v['solution']) for v in observed})==5
    assert len({r['question'][':question/problem'] for r in group})==5
    assert len({r['question'][':question/worked-solution'] for r in group})==5
    assert g.generate(profile=p,seed=987,target=0,signs=(-1,1,-1),shifts=(2,-2,1))['question']==group[0]['question']
    controlled.extend(group)
    # Normal stream cannot silently remain in source replay mode.
    random_group=[g.generate(profile=p,seed=i) for i in (0,1,2,3,4)]
    random_info=[inspect(r) for r in random_group]
    assert len({v['correct_index'] for v in random_info})>1,p
    normal.extend(random_group)
    reports.append({'profile':p,'source_question_id':q[':question/id'],'replay_choices':5,'controlled_correct_positions':[v['correct_index'] for v in observed], 'normal_correct_positions':[v['correct_index'] for v in random_info], 'fixed_bank_only_strategy_max_success':'1/5', 'math':observed})
# Retain both concrete old-scale probes. Show the unique-middle rule is no longer a key rule.
old=json.loads((OUT/'before-shortcut.json').read_text())[0]
i=inspect(old); assert sum(float(v[1])>0 for v in i['bank'])==1 and float(i['solution'][1])>0
exact=g.generate(profile='q-129453',seed=73421,scale=4)
new=inspect(exact)
positives=[j for j,v in enumerate(new['bank']) if float(v[1])>0]
assert len(positives)!=1 or positives[0]!=new['correct_index']
# Exact unchanged old bank supports each of its five keys when RHSs change.
legacy_family=[g.generate(profile='q-129453',seed=73421,scale=4,target=t,signs=(1,1,1),shifts=(0,0,0)) for t in range(5)]
assert all(inspect(r)['bank']==i['bank'] for r in legacy_family)
assert {inspect(r)['correct_index'] for r in legacy_family}==set(range(5))
legacy2=[g.generate(profile='q-10195',seed=73421,scale=3,target=t,signs=(1,1,1),shifts=(0,0,0)) for t in range(5)]
assert {inspect(r)['correct_index'] for r in legacy2}==set(range(5))
all_records=replays+controlled+normal+[exact]+legacy_family+legacy2
cases=[]
for n,r in enumerate(all_records):
    info=inspect(r);f=r['question'][':question/answer-fields'][0]
    cases.append({'label':str(n),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if j==info['correct_index'] else 'rejected','purpose':'Independent solution of visible equations, all choices'} for j,c in enumerate(f[':answer-field/choices'])]})
save('regressions.json',{'passed':True,'source_replay_banks':len(replays),'controlled_records':len(controlled),'normal_records':len(normal),'profiles':reports,'exact_old_probe':i,'exact_new_probe':new,'checks':len(cases)*5})
save('source-replays.json',replays);save('controlled.json',controlled);save('normal.json',normal);save('legacy-counterfactuals.json',legacy_family+legacy2);save('grader-input.json',cases)
save('render-records.json',[replays[-1],controlled[-5],controlled[40],normal[0]])
print(json.dumps({'passed':True,'replay_banks':len(replays),'controlled':len(controlled),'normal':len(normal),'native_checks_prepared':len(cases)*5}))
