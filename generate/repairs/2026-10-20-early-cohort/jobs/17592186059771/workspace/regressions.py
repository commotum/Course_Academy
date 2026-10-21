"""Strict repair acceptance tests. No runtime file writes or service access."""
import sys
sys.dont_write_bytecode = True
import itertools
from validation_helpers import *

OUT = E/'evidence'
OUT.mkdir(exist_ok=True)
def save(n,x): (OUT/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
source = json.loads((J/'source/source.json').read_text())
source_q = source['material']['kp'][':knowledge-point/questions']
results=[]
def check(label, passed, **details):
    results.append({'case':label,'passed':bool(passed),**details})

replays=[]
for q in source_q:
    sid=q[':question/math-academy-id']; d=q[':question/difficulty'][':db/ident'].split('/')[-1]
    try:
        if d=='hard': r=hard.replay(sid,991)
        elif d=='easy': r=g.generate(d,991,sid,easy.CASES[sid])
        else: r=g.generate(d,991,sid)
        replays.append(r)
        bank=lambda question: sorted(str(mat(a[':answer/value'])) for a in question[':question/answer-fields'][0][':answer-field/choices'])
        check(sid+' complete source bank', bank(q)==bank(r['question']) and mat(key(q)[':answer/value'])==mat(key(r['question'])[':answer/value']) and mat(q[':question/problem'])==mat(r['question'][':question/problem']),source_id=q[':question/id'])
    except Exception as e:
        check(sid+' complete source bank',False,error=repr(e),source_id=q[':question/id'])

canonical=g.generate('moderate',991,'e-4693')
original=source['material']['kp'][':knowledge-point/canonical-example']
check('canonical worked example preserves no invented answer bank',
      canonical['question'][':question/problem']==g.normalize_prose(original[':question/problem'])
      and canonical['question'][':question/worked-solution']==g.normalize_prose(original[':question/worked-solution'])
      and canonical['question'][':question/answer-fields']==[])

# Exact review seeds: witness relationships from visible delivered operations.
hard_records=[g.generate('hard',seed) for seed in range(72011,72071)]
relationships=[]
for r in hard_records:
    op=ops(r['question'][':question/problem'])
    relationships.append('shared-target' if op[0][1]==op[1][1] else 'shared-donor')
check('both hard source-supported role families from exact review seeds',set(relationships)=={'shared-target','shared-donor'},counts=dict(collections.Counter(relationships)))

# Hold entries and candidate bank fixed; every candidate must be eligible as key.
m=[[1,2,3],[4,5,7],[-2,6,8]]
pairs=[[2,1],[2,-1],[-2,1],[-2,-1],[1,2]]
controls=[]
for case,roles in [('shared-target',[(0,1),(0,2)]),('shared-donor',[(0,1),(2,1)])]:
    group=[]
    for coefficients in pairs:
        p={'matrix':m,'operations':[[t,d,k] for (t,d),k in zip(roles,coefficients)],'candidate_pairs':pairs,'name':'C'}
        r=g.generate('hard',614,parameters=p);group.append(r);controls.append(r)
        visible=ops(r['question'][':question/problem'])
        check(case+' respects explicit requested operations '+str(coefficients),[(t,d,int(k)) for _,t,d,k in visible]==[tuple(o) for o in p['operations']])
    banks=[sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']) for r in group]
    check(case+' each bank member becomes key with fixed data',all(b==banks[0] for b in banks) and len({key(r['question'])[':answer/value'] for r in group})==5)
    check(case+' factor changes update prompt and explanation',len({r['question'][':question/problem'] for r in group})==5 and len({r['question'][':question/worked-solution'] for r in group})==5)
    # Irrelevant notation, and order of these commuting operations, preserve result.
    p=copy.deepcopy(group[0]['generation']['parameters'])
    for change in ['name','reverse']:
        variant=copy.deepcopy(p)
        if change=='name': variant['name']='B'
        else:
            variant['operations'].reverse(); variant['candidate_pairs']=[list(reversed(pair)) for pair in pairs]
        r=g.generate('hard',614,parameters=variant);controls.append(r)
        check(case+' invariant under '+change,key(r['question'])[':answer/value']==key(group[0]['question'])[':answer/value'] and r['generation']['mathematical_fingerprint']==group[0]['generation']['mathematical_fingerprint'])

# All six row assignments in each relationship: no source row is frozen.
role_records=[]
for case in ['shared-target','shared-donor']:
    for anchor,x,y in itertools.permutations(range(3)):
        roles=[(anchor,x),(anchor,y)] if case=='shared-target' else [(x,anchor),(y,anchor)]
        p={'matrix':m,'operations':[[t,d,k] for (t,d),k in zip(roles,pairs[0])],'candidate_pairs':pairs,'name':'C'}
        role_records.append(g.generate('hard',614,parameters=p))
controls+=role_records
# Old parameter calls translate to exactly the same mathematical prompt and bank.
legacy={'matrix':m,'target':0,'donors':[1,2],'coefficients':[2,1],'candidate_pairs':pairs,'name':'C'}
l=g.generate('hard',614,parameters=legacy)
check('legacy same-target API preserves explicit equivalent',l==controls[0])
# The review supplied legacy fields PLUS explicit operations; explicit operations must win.
explicit={**legacy,'operations':[[0,1,2],[2,1,1]]}
r=g.generate('hard',614,parameters=explicit);controls.append(r)
check('review explicit-operation counterexample not ignored',calc(r['question'])==[[9,12,17],[4,5,7],[2,11,15]])

# Small regression sample for unchanged easy/moderate behavior, plus delivered count.
easy_records=[g.generate('easy',seed) for seed in range(72011,72029)]
moderate_records=[g.generate('moderate',seed) for seed in range(72011,72017)]
batch=[g.generate('easy',20261021+i) for i in range(5)]
all_records=hard_records+replays+controls+easy_records+moderate_records+batch
math_results=[verify(r) for r in all_records]
flags=['key_correct','unique_correct','five_unique','solution_final_correct']
check('independent visible mathematics, complete banks and final solutions',all(all(x[k] for k in flags) for x in math_results),count=len(math_results),failures=[x for x in math_results if not all(x[k] for k in flags)])
# Independent intermediate matrices must reflect the first, then both operations.
for r in hard_records+controls:
    q=r['question']; mm=matrixes(q[':question/worked-solution']); op=ops(q[':question/problem']); original=mat(q[':question/problem']); after=copy.deepcopy(original)
    _,t,d,k=op[0];after[t]=[a+k*b for a,b in zip(after[t],after[d])]
    check('hard intermediate '+q[':question/id'],len(mm)==3 and mm[0]==original and mm[1]==after and mm[2]==calc(q))
for parameters in [
    {'matrix':m,'operations':[[0,1,2],[1,2,1]],'candidate_pairs':pairs,'name':'C'},
    {'matrix':m,'operations':[[0,0,2],[0,2,1]],'candidate_pairs':pairs,'name':'C'},
    {'matrix':m,'operations':[[0,1,0],[2,1,1]],'candidate_pairs':pairs,'name':'C'}]:
    try:g.generate('hard',1,parameters=parameters); rejected=False
    except ValueError:rejected=True
    check('invalid hard operation request rejected '+str(parameters['operations']),rejected)

save('source-replays.json',replays)
save('hard-records.json',hard_records+controls)
save('easy-records.json',easy_records+batch)
save('moderate-records.json',moderate_records)
save('control-records.json',controls)
save('batch-records.json',batch)
save('math-results.json',math_results)
save('regression-results.json',{'command':sys.executable+' -B regressions.py','findings':['55fe1d6b85c6baba6cb2','420f6a55dfa2869218de'],'checks':results,'passed':all(x['passed'] for x in results)})
# Grader cases derive outcomes independently from the visible prompt, including all wrong choices.
gcases=[]
for i,r in enumerate(replays+controls+batch+[hard_records[0],hard_records[1]]):
    q=r['question'];expected=calc(q)
    gcases.append({'label':str(i)+': '+q[':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if mat(a[':answer/value'])==expected else 'rejected','purpose':'Independent visible row-operation arithmetic; every choice tested'} for a in q[':question/answer-fields'][0][':answer-field/choices']]})
save('grader-input.json',gcases)
# Two missing replays and both hard operation relationships cover all changed rendering paths.
save('render-records.json',[next(r for r in replays if r['generation']['profile']==sid) for sid in ['q-10251','q-10243']]+[controls[0],controls[7]])
fail=[x for x in results if not x['passed']]
print(json.dumps({'checks':len(results),'math_records':len(math_results),'hard_relationships':dict(collections.Counter(relationships)),'source_banks':len(replays),'failures':fail},default=str))
sys.exit(bool(fail))
