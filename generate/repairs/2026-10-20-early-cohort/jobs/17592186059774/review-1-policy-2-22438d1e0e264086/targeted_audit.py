"""Independent revision review. Run with job Python; writes only beside this script."""
from independent import *
import itertools

source=json.load(open(JOB/'source/source.json'))
sq=source['material']['kp'][':knowledge-point/questions']
replays=[]; replay_report=[]
for q in sq:
    sid=q[':question/math-academy-id']; r=g.replay(sid); a=analyze(r)
    f=q[':question/answer-fields'][0]; rf=r['question'][':question/answer-fields'][0]
    assert mats(q[':question/problem'])==mats(r['question'][':question/problem'])
    assert target(q[':question/problem'])==target(r['question'][':question/problem'])
    assert [op(v[':answer/value'].replace(r'\\frac',r'\frac')) for v in f[':answer-field/choices']]==[op(v[':answer/value']) for v in rf[':answer-field/choices']]
    if f.get(':answer-field/correct'):
        assert op(f[':answer-field/correct'][':answer/value'])==op(a['correct'])
    replays.append(r);replay_report.append({'profile':sid,'source_id':q[':question/id'],'all_five_choices_match':True,'analysis':a,'source_solution_result_matches':mats(q.get(':question/worked-solution',''))[-1:]==mats(r['question'][':question/worked-solution'])[-1:]})
save('source-replays.json',replays);save('source-replay-results.json',replay_report)

# Independent eligibility from visible source operations, not generator eligibility.
q=next(q for q in sq if q[':question/math-academy-id']=='q-72858')
t,c=target(q[':question/problem']); eligible=[]
for j,v in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):
    o=op(v[':answer/value'])
    if (o[0]=='swap' and t in o[1:]) or (o[0]=='linear' and o[1]==t and o[2][t]==1 and sum(x!=0 for i,x in enumerate(o[2]) if i!=t)==1):eligible.append(j)
assert eligible==[0,1]
fresh=[]
for w in eligible:
    for rr in range(3):
        for cc in range(3):
            rows=[0,1,2];rows[t],rows[rr]=rows[rr],rows[t]
            cols=[0,1,2];cols[c],cols[cc]=cols[cc],cols[c]
            r=g.generate(seed=921701+rr*3+cc,template='q-72858',parameters={'winner':w,'rows':rows,'cols':cols})
            assert analyze(r)['target']==f'{rr+1}{cc+1}';fresh.append(r)
    for rows in itertools.permutations(range(3)):
        r=g.generate(seed=670811,template='q-72858',parameters={'winner':w,'rows':list(rows)})
        analyze(r);fresh.append(r)
    # Explicit small-boundary signed columns and zero donor for swap.
    for sign in [-1,1]:
        m=[[9,-9,12*sign],[0,1,12*sign],[-9,9,sign if w==0 else 0]]
        if w==1:m[0][2]=11*sign
        fresh.append(g.generate(seed=10291,template='q-72858',parameters={'winner':w,'matrix':m}))
random_controls=g.batch('hard',12,972501)
fresh+=random_controls

# A small deterministic control from every unchanged sampled profile, using earlier
# independent records only after the construction code and source equality checks.
old=json.load(open(ROOT/'reused/independent-samples.json')); controls=[]; seen=set()
for r in old:
    sid=r['generation']['bank_profile']
    if sid in seen:continue
    seen.add(sid);new=g.generate(seed=r['generation']['seed'],parameters=r['generation']['parameters'])
    assert new['question']==r['question'];analyze(new);controls.append(new)
fresh+=controls
save('fresh-samples.json',fresh)
save('unchanged-control-results.json',{'profiles':sorted(seen),'question_equality':True,'records':controls,'reuse_basis':'revision-diff.json; version-only executable change and exact equality of all ten prior source records'})
save('runner-batch.json',json.load(open(JOB/'samples.json')))
batch=json.load(open(ROOT/'runner-batch.json'))

base={'source':'q-72858','rows':[0,1,2],'cols':[0,1,2],'order':[0,1,2,3,4]}
# Change decisive donor evidence while keeping target value, bank and all other
# columns fixed. A subtraction winner and swap winner must exchange correctness.
params=[dict(base,winner=0,matrix=[[2,1,3],[6,4,3],[1,2,3]]),
        dict(base,winner=1,matrix=[[2,1,4],[6,4,3],[1,2,0]]),
        dict(base,winner=0,matrix=[[-9,8,3],[6,4,3],[1,2,3]])]
cf=[g.generate(seed=921733,parameters=p) for p in params]
ca=[analyze(r) for r in cf]
assert op(ca[0]['correct'])!=op(ca[1]['correct']) and op(ca[0]['correct'])==op(ca[2]['correct'])
assert len(set(r['question'][':question/problem'] for r in cf))==3
assert len(set(r['question'][':question/worked-solution'] for r in cf))==3
# Identical visible matrix/bank, only target a21 -> a23 changes.
tp=[g.generate(seed=921733,parameters=dict(base,winner=0,matrix=[[4,1,3],[3,4,3],[0,2,2]],cols=[2,1,0])),
    g.generate(seed=921733,parameters=dict(base,winner=1,matrix=[[3,1,4],[3,4,3],[2,2,0]]))]
ta=[analyze(r) for r in tp]
assert mats(tp[0]['question'][':question/problem'])==mats(tp[1]['question'][':question/problem'])
assert [v[':answer/value'] for v in tp[0]['question'][':question/answer-fields'][0][':answer-field/choices']]==[v[':answer/value'] for v in tp[1]['question'][':question/answer-fields'][0][':answer-field/choices']]
assert ta[0]['target']=='21' and ta[1]['target']=='23' and ta[0]['correct']!=ta[1]['correct']
save('counterfactual-records.json',cf+tp)
save('counterfactual-results.json',{'parameters':params,'relevant':ca[:2],'irrelevant':[ca[0],ca[2]],'target_change':ta,'assertions':'Visible prompts, all five independently applied choices and final solution matrices agree. Native and renderer checks pending.'})

checked={n:[analyze(r) for r in rs] for n,rs in [('fresh',fresh),('batch',batch),('counterfactual',cf+tp),('source',replays)]}
save('math-results.json',checked)
reject=[]
for label,args in [('unsupported easy',{'difficulty':'easy'}),('unsupported moderate',{'difficulty':'moderate'}),
    *[(f'ineligible self-scaling/unrelated winner {w}',{'parameters':dict(base,winner=w)}) for w in [2,3,4]],
    ('ambiguous subtraction and swap',{'parameters':dict(base,winner=0,matrix=[[2,1,3],[6,4,3],[1,2,0]])}),
    ('initial zero target',{'parameters':dict(base,winner=0,matrix=[[2,1,0],[6,4,0],[1,2,3]])}),
    ('duplicate row permutation',{'parameters':dict(base,rows=[0,0,2])}),
    ('duplicate option order',{'parameters':dict(base,order=[0,1,2,3,3])})]:
    try:g.generate(**args)
    except ValueError as e:reject.append({'case':label,'args':args,'result':'rejected','message':str(e)})
    else:raise AssertionError(('unexpected acceptance',label))
save('rejection-results.json',reject)

grader=[]
for r in batch+replays+cf+tp+fresh[:2]:
    a=analyze(r);vs=r['question'][':question/answer-fields'][0][':answer-field/choices']
    grader.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if j==a['position'] else 'rejected','purpose':'Independent exact Fraction evaluation of every visible operation'} for j,v in enumerate(vs)]})
save('grader-input.json',grader)
save('render-records.json',batch+cf+tp+[next(r for r in replays if r['generation']['bank_profile']=='q-72858')])

# Replay persisted parameters and relocate into evidence without package writes.
assert all(g.generate(seed=r['generation']['seed'],parameters=r['generation']['parameters'])['question']==r['question'] for r in fresh+batch+cf+tp)
assert g.batch('hard',5,6715009)==g.batch('hard',5,6715009)
copy=ROOT/'relocated';copy.mkdir(exist_ok=True)
for name in json.load(open(PKG/'package.json'))['files']+['package.json']:shutil.copy2(PKG/name,copy/name)
command=[sys.executable,str(copy/'generator.py'),'--count','5','--seed','986321']
pr=subprocess.run(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
assert pr.returncode==0 and json.loads(pr.stdout)==g.batch('hard',5,986321) and pr.stderr==''
save('relocated-records.json',json.loads(pr.stdout))
versions={'python':platform.python_version(),'packages':{x:importlib.metadata.version(x) for x in ['sympy','mpmath']}}
assert versions==json.load(open(PKG/'package.json'))['dependencies']
save('packaging-results.json',{'versions':versions,'manifest_matches':True,'replay_records':len(fresh+batch+cf+tp),'batch_determinism':True,'relocation_command':command,'relocation_stdout_json_only':True,'external_output':'No assets or external outputs used by generator; actual UI renderer will verify math displays.'})
save('coverage.json',{'restored_profile':'q-72858','independently_eligible_winners':eligible,'winner_counts':dict(collections.Counter(r['generation']['parameters']['winner'] for r in fresh if r['generation']['bank_profile']=='q-72858')),'target_counts':dict(collections.Counter(a['target'] for a in checked['fresh'] if a['profile']=='q-72858')),'rejection_attempt_counts':dict(collections.Counter(r['generation']['rejection_attempts'] for r in fresh)),'random_batch_seed':972501,'random_profiles':dict(collections.Counter(r['generation']['bank_profile'] for r in random_controls)),'commands':['PYTHONDONTWRITEBYTECODE=1 '+sys.executable+' targeted_audit.py'],'prior_unaffected_evidence':'reused/independent-samples.json; revision-diff.json'})
(ROOT/'session-state.md').write_text('Retained author regression confirmed to fail on old package and pass on current relocated copy. Independent 11-bank replay, restored-profile winners/targets/permutations/boundaries, small unchanged-profile controls, exact batch math, explicit counterfactuals, rejection and relocation checks completed. Native grading, delivery, render and decision summary pending. All writes under evidence_root.\n')
print(json.dumps({'source_replays':len(replays),'fresh_records':len(fresh),'current_batch':len(batch),'counterfactuals':len(cf+tp),'rejected':len(reject),'grader_cases':len(grader)}))
