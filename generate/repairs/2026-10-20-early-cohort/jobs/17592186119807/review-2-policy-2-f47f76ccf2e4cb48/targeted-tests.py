import json,pathlib,sys,subprocess,collections,re,itertools
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
text=(E/'review.py').read_text();exec(text.split('before=hashes();')[0]);exec(text[text.index('def num(s):'):text.index('source=load(J/')])
g=module(P/'17592186119807.py','targeted_generator')
# Small fresh sample at requested count; trace both role rejection and whole-pool acceptance.
traces=[]
for seed in (104729,20261021):
 attempted=[];original=g.generate
 def traced(*args,**kwargs):
  r=original(*args,**kwargs);attempted.append(r);return r
 g.generate=traced
 try:rs=g.batch('moderate',5,seed)
 finally:g.generate=original
 for r in rs:check(r)
 assert rs==g.batch('moderate',5,seed)
 save(f'trace-{seed}-attempts.json',attempted);save(f'fresh-batch-{seed}.json',rs)
 def counts(records):
  out=collections.Counter()
  for r in records:
   nums=[num(a[':answer/value']) for a in choices(r) if a[':answer/type']==':answer.type/math']
   out[str((any(n<=0 for n in nums),truth(r)!='No solution'))]+=1
  return dict(out)
 assert len(counts(rs))==4
 traces.append({'seed':seed,'attempt_count':len(attempted),'retained':len(rs),'attempt_cases':counts(attempted),'retained_cases':counts(rs),'deterministic':True,'attempts_file':f'trace-{seed}-attempts.json','records_file':f'fresh-batch-{seed}.json','limits':'Counts aggregate role rejection, duplicate-system rejection and whole-pool retries. Top-level runner seed unavailable; exact batch is separately replayed per item.'})
save('resampling-results.json',{'command':str(PY)+' targeted-tests.py','traces':traces})
# Original failing record and controlled changes at fixed source and seed.
p={'translation':-2,'residual':'1','rank':4,'gaps':[4,4,4]};seed=5888234723018271144
bad=g.generate('moderate',seed,'q-105166',p)
good=g.generate('moderate',seed,'q-105166',dict(p,residual='0'))
# Irrelevant distractor signs: same correct sum and vectors but all-positive vs mixed bank.
p2={'translation':1,'residual':'0','rank':1,'gaps':[5,5,5]}
pos=g.generate('moderate',104729,'q-105165',p2)
neg=g.generate('moderate',104729,'q-105165',dict(p2,rank=4))
assert truth(bad)=='No solution' and truth(good)=='-4'
assert vectors(bad)[:2]==vectors(good)[:2] and sum(a!=b for a,b in zip(vectors(bad)[2],vectors(good)[2]))==1
assert [(a[':answer/value'],a[':answer/type']) for a in choices(bad)]==[(a[':answer/value'],a[':answer/type']) for a in choices(good)]
assert truth(pos)==truth(neg)=='10' and vectors(pos)==vectors(neg)
assert pos['question'][':question/worked-solution']==neg['question'][':question/worked-solution']
assert min(num(a[':answer/value']) for a in choices(pos) if a[':answer/type']==':answer.type/math')>0
assert min(num(a[':answer/value']) for a in choices(neg) if a[':answer/type']==':answer.type/math')<=0
pairs=[bad,good,pos,neg]
for r in pairs:check(r)
save('sign-counterfactual-records.json',pairs)
save('sign-counterfactual-results.json',{'command':str(PY)+' targeted-tests.py','relevant':'Original q-105166 failing record retained. Change only decisive RHS residual1->0, holding bank fixed: No solution -> -4.','irrelevant':'q-105165 at t1: change only bank rank1->4, making positive-only bank mixed-sign; vectors, solution and answer10 unchanged.','records':'sign-counterfactual-records.json','passed':True})
# Strict regression must fail original batch and pass current batch and controls.
checks=[]
for name,records,expected in [('original',J/'review-1-policy-2-bc476fa1f6e925b4/delivery-batch/accepted.json',False),('current',E/'delivery-batch/accepted.json',True),('control',E/'sign-counterfactual-records.json',True)]:
 cmd=[str(PY),str(E/'batch_regression.py'),'--records',str(records)];r=subprocess.run(cmd,capture_output=True,text=True)
 assert (r.returncode==0)==expected
 if not expected:assert '3/3' in r.stderr
 checks.append({'case':name,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'expected_pass':expected})
save('retained-sign-regression.json',checks)
# Add these new controlled instances to the one native-grader invocation and actual UI.
cases=load(E/'grader-input.json')
for i,r in enumerate(pairs):cases.append({'label':f'sign-pair-{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if canon(a[':answer/value'])==truth(r) else 'rejected','purpose':'Independent Fraction oracle; sign/consistency controlled pair'} for a in choices(r)]})
save('grader-input.json',cases);save('render-records.json',load(E/'render-records.json')+pairs)
(E/'session-state.md').write_text('Source replay14/14 and independent math157 pass. Shared delivery raw138->136 and exact5->5. New sign batch fixes old3/3 cue; strict original-fails/current-passes tests retained. Fresh requested-size traces and relevant/irrelevant sign pairs saved. Native/UI final run pending (17 records). Package remains unchanged.\n')
print(json.dumps({'traces':traces,'pairs':4,'strict_regressions':3,'grader_records':len(cases)}))
