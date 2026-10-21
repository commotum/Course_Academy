"""Independent focused checks for the newly added shared-bank construction."""
from audit import *
from reproduce_shortcut import select

g=module(W/'17592186059770.py')
records=[];reports=[]
profiles=list(g.EASY_SOURCES)
for profile,seed in [(p,613423+i*211) for i,p in enumerate(profiles)]+[(None,721957),(None,928139)]:
 rs=g.generate_batch('easy',5,seed,profile=profile)
 assert len(rs)==5 and rs==g.generate_batch('easy',5,seed,profile=profile)
 groups=collections.defaultdict(list)
 for r in rs:
  qcheck(r)
  key=tuple(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
  groups[key].append(r)
 outcomes=[]
 for key,group in groups.items():
  targets=[visible(r['question']) for r in group]
  assert len(set(map(str,targets)))==len(group)>=2
  # This proof checks visible bank equality, not author role metadata.
  assert len({r['question'][':question/problem'] for r in group})==len(group)
  successes=sum(select(r)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in group)
  assert successes<len(group)
  outcomes.append({'count':len(group),'distinct_visible_targets':len(set(map(str,targets))),'bank_only_best_possible':1,'prior_selector_correct':successes})
 start=len(records);records.extend(rs);reports.append({'profile':profile,'seed':seed,'record_indices':list(range(start,len(records))),'groups':outcomes})
# Pin the branch newly used by q-129137: shared constants must actually be
# ambiguous for two choices, so it cannot be replaced by copying the RHS alone.
q129=[r for r in records if r['generation']['bank_profile']=='q-129137' and r['generation']['batch']['decision_case']=='shared_constants']
assert q129
for r in q129:
 cs=[mat(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
 assert len({tuple(m[i][-1] for i in range(2)) for m in cs if len(m)==2 and len(m[0])==3})<3
save('fresh-batches.json',records);save('changed-batch-results.json',{'command':f'{PY} -B {E}/changed_batch.py','cases':reports,'shared_constants_records':len(q129),'visible_bank_proof':'Same full ordered answer bank, at least two distinct displayed targets per group; hence a deterministic bank-only choice cannot answer all group members.'})
# Counterexamples from the prior failed batch are still supported, while a
# changed prompt can select every eligible matrix in the exact same bank.
old=load(J/'review-1-policy-2-33e5a98244ac977f/batch.json')
retained=[]
for r in old:
 m=r['generation'];new=g.generate('easy',m['seed'])
 assert new['question']==r['question'];assert select(new)==new['question'][':question/answer-fields'][0][':answer-field/correct'][1]
 retained.append(new)
save('prior-counterexamples-current.json',retained)
# Explicit strict regression fails on the old bad batch, passes on current.
oldpath=E/'retained-failed-batch.json';save(oldpath.name,load(J/'review-1-policy-2-33e5a98244ac977f/delivery-batch/accepted.json'))
before=command([PY,'-B',E/'reproduce_shortcut.py',oldpath]);assert before['exit']!=0
save('prior-shortcut-failure-run.json',before);save('prior-shortcut-failure-results.json',load(E/'shortcut-regression.json'))
after=command([PY,'-B',E/'reproduce_shortcut.py',E/'delivery-batch/accepted.json']);assert after['exit']==0
save('current-shortcut-run.json',after)
native=[]
for i,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0];expected=visible(r['question'])
 native.append({'label':f'fresh-changed-batch-{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if mat(a[':answer/value'])==expected else 'rejected','purpose':'visible-matrix oracle, fresh shared-bank construction'} for a in f[':answer-field/choices']]})
save('fresh-native-input.json',native)
run=command([R/'generate/runs/current/check-engine',E/'fresh-native-input.json',E/'fresh-native-report.json']);save('fresh-native-run.json',run);assert run['exit']==0
print(json.dumps({'records':len(records),'banks':sum(len(x['groups']) for x in reports),'old_regression_exit':before['exit'],'current_regression_exit':after['exit'],'native_exit':run['exit']}))
