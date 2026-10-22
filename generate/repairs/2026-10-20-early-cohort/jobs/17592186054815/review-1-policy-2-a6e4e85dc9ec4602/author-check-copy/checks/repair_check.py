"""Retained source omissions/bank mutation regressions plus construction-family tests."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,random,re,subprocess
W=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(W))
import generator as g
from oracle import verify,correct_value,enum,mask
E=W/'evidence';E.mkdir(exist_ok=True)

def save(name,value): (E/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
# Execute the retained strict review regression, supplemented with independent keys.
subprocess.run([sys.executable,'-B',str(W/'checks/source_acceptance.py'),'--output',str(E/'source-acceptance-result.json')],check=True)
source=json.loads((W/'source_cases.json').read_text())[':knowledge-point/questions']
replays=g.replay_sources();by_sid={r['generation']['source_question_ids'][0]:r for r in replays}
assert set(by_sid)=={q[':question/id'] for q in source}
results=[]
for q in source:
    r=by_sid[q[':question/id']];verify(r)
    for old,new in zip(q[':question/answer-fields'],r['question'][':question/answer-fields']):
        assert enum(old[':answer-field/type'])==new[':answer-field/type']
        assert [a[':answer/value'] for a in old[':answer-field/choices']]==[a[':answer/value'] for a in new[':answer-field/choices']]
        if old.get(':answer-field/correct'): assert correct_value(old)==correct_value(new)
    results.append({'source_id':q[':question/id'],'fields':len(r['question'][':question/answer-fields']),'verified':True,'source_missing_solution':not bool(q.get(':question/worked-solution'))})
# Original q-104686 exact counterexample must remain callable through generate.
q=next(q for q in source if q[':question/id']=='c620ed83-c013-5ff0-8983-14697bd50f1b')
r=g.generate('Q0+',[g.number('integer',0),g.number('sqrt',1,20),g.number('sqrt',-1,25),g.number('fraction',1,2)],replay=q)
assert correct_value(r['question'][':question/answer-fields'][0])=='I and IV only'
controlled=[]
for t in g.TARGETS:
    for response in ('radio','checkbox'):
        masks=range(16) if t in ('Q0-','Z0+') or (t=='Q0+' and response=='radio') else (1,14)
        for m in masks:
            _,ns,_=g.sample(random.Random(700+m),t,m)
            r=g.generate(t,ns,response=response,seed=822,index=m)
            verify(r);assert mask(r)==m
            controlled.append(r)
# All source canonical decision distinctions, through both response contracts.
ns=[g.number('sqrt',-1,3),g.number('decimal',-2),g.number('integer',0),g.number('sqrt',-1,4)]
canonical=[g.generate('Q-',ns,response=mode,seed=77) for mode in ('checkbox','radio')]
assert all(mask(r)==10 for r in canonical)
for r in canonical:verify(r)
# Same visible data under changed targets; irrelevant within-class magnitude change.
ns=[g.number('integer',0),g.number('sqrt',1,2),g.number('fraction',1,2),g.number('integer',-3)]
pairs=[]
for response in ('checkbox','radio'):
    rs=[g.generate(t,ns,response=response,seed=12) for t in ('Q0+','R0+','Q0-','Q-','Z0+')]
    altered=list(ns);altered[2]=g.number('fraction',3,4)
    rs.append(g.generate('Q0+',altered,response=response,seed=12))
    assert [mask(r) for r in rs]==[5,7,9,8,1,5]
    for r in rs:verify(r)
    pairs+=rs
fresh=g.batch('easy',28,1442108295)
for r in fresh:verify(r)
save('source-replay-checks.json',results);save('replay-records.json',replays)
save('controlled-records.json',controlled);save('counterfactual-records.json',pairs);save('canonical-records.json',canonical)
save('fresh-records.json',fresh);save('batch-records.json',fresh[:5])
allrecords=replays+controlled+pairs+canonical+fresh
checks=[]
for i,r in enumerate(allrecords):
    expected=verify(r);cs=[]
    for j,(f,v) in enumerate(zip(r['question'][':question/answer-fields'],expected)):
        for a in f[':answer-field/choices']:
            cs.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==v else 'rejected','purpose':'visible mathematical witness; correct and every offered incorrect response'})
    checks.append({'label':f'math-{i}','record':r,'checks':cs})
save('grader-input.json',checks)
save('delivery-input.json',controlled+pairs+fresh)
# Representative UI: all restored source radio cases, captured four-field checkbox,
# explicit source None, new empty-set radio and fresh authored checkbox/radio.
render=[by_sid[s] for s in ('59f3318f-8861-5823-9f55-694de5f640be','891fa895-d529-5c21-9765-4d2a287c7001','c620ed83-c013-5ff0-8983-14697bd50f1b','c2a941ac-46f5-56a9-b5ba-03889446453a')]
render += [next(r for r in controlled if r['generation']['response_contract']==mode and mask(r)==0) for mode in ('radio','checkbox')]
save('render-records.json',render)
summary={'source_cases':len(replays),'captured_correct_keys':sum(bool(f.get(':answer-field/correct')) for q in source for f in q[':question/answer-fields']),'controlled':len(controlled),'fresh':len(fresh),'counterfactuals':len(pairs),'independent_math_records':len(allrecords),'native_grader_checks_prepared':sum(len(c['checks']) for c in checks),'passed':True}
save('repair-checks.json',summary);print(json.dumps(summary))
