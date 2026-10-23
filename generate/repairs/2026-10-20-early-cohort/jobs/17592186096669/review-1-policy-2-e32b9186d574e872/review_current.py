from review_lib import *
save('package-before.json',hashpkg())
spec=importlib.util.spec_from_file_location('current',PACKAGE/'17592186096669.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('previous',JOB/'review-0-policy-2-8b996ed7d80a08a9/relocated/17592186096669.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
source=load(JOB/'source/source.json');sq={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
replays=[];replay_info=[]
for p,q in sq.items():
 if p not in g.PARAMETERS:
  replay_info.append({'profile':p,'status':'unsupported','reason':'Source lacks correct link, worked solution and difficulty; preserved gap.'});continue
 r=g.generate(profile=p,scale=1,seed=82067);m=inspect(r)
 assert equations(q)==equations(r['question'])
 assert [vec(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']]==[vec(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]
 replays.append(r);replay_info.append({'profile':p,'status':'passed','source_id':q[':question/id'],'math':m})
save('replays.json',replays);save('source-replay.json',replay_info)
normal=[g.generate(seed=s,profile=p) for p in g.PARAMETERS for s in (82067,82069,82073,82079,82081)]
controlled=[g.generate(seed=82067,profile=p,target=t,signs=(1,1,1),shifts=(0,0,0)) for p in g.PARAMETERS for t in range(5)]
# Low/high explicit scales; same validated workload extension from old package.
boundaries=[g.generate(seed=82067,profile=p,scale=9) for p in ('q-20450','q-129455')]
base=g.generate(seed=82067,profile='q-129453',target=1,signs=(1,1,1),shifts=(0,0,0))
changed=g.generate(seed=82067,profile='q-129453',target=2,signs=(1,1,1),shifts=(0,0,0))
qsave=g.QUESTIONS['q-129453'];g.QUESTIONS['q-129453']=copy.deepcopy(qsave)
g.QUESTIONS['q-129453'][':question/problem']=qsave[':question/problem'].replace('{x}_{1}','x').replace('{x}_{2}','y').replace('{x}_{3}','z')
renamed=g.generate(seed=82067,profile='q-129453',target=1,signs=(1,1,1),shifts=(0,0,0));g.QUESTIONS['q-129453']=qsave
pairs=[base,changed,renamed];pi=[inspect(r) for r in pairs]
assert pi[0]['bank']==pi[1]['bank'] and pi[0]['solution']!=pi[1]['solution']
assert pi[0]['solution']==pi[2]['solution'] and pi[0]['bank']==pi[2]['bank']
assert base['question'][':question/problem']!=renamed['question'][':question/problem']
assert base['question'][':question/worked-solution']!=renamed['question'][':question/worked-solution']
save('counterfactual-records.json',pairs);save('counterfactual-results.json',{'relevant':'Same bank and LHS, change target 1 to 2: RHS changes force (-? see exact solutions) reconsideration','irrelevant':'Rename indexed variables to xyz consistently; vector answer preserved','math':pi})
batch=load(JOB/'samples.json')
for n,rs in [('samples',normal),('controlled',controlled),('boundaries',boundaries),('batch',batch)]:save(n+'.json',rs)
results={n:[inspect(r) for r in rs] for n,rs in [('samples',normal),('controlled',controlled),('boundaries',boundaries),('batch',batch)]};save('math-results.json',results)
# Concrete prior failures must fail independently, and the current role family must defeat the old rule.
oldcase=old.generate(profile='q-129453',seed=73421,scale=4);newcase=g.generate(profile='q-129453',seed=73421,scale=4)
def sole_positive_middle(r):
 m=inspect(r);idx=[i for i,v in enumerate(m['bank']) if sp.Rational(v[1])>0];return len(idx)==1 and idx[0]==m['correct_index']
assert sole_positive_middle(oldcase) and not sole_positive_middle(newcase)
try:old.generate(profile='q-20450',scale=1);oldmissing=False
except ValueError:oldmissing=True
assert oldmissing
save('prior-counterexamples.json',{'old_record':oldcase,'current_record':newcase,'old_shortcut_reproduced':True,'current_exact_old_command_defeats_shortcut':True,'old_q20450_rejected':oldmissing,'current_q20450_complete_bank_replay':True})
# Preserve a runnable strict regression that fails on the old implementation.
allrecords=replays+normal+controlled+boundaries+batch+pairs+[oldcase,newcase]
cases=[]
for i,r in enumerate(allrecords):
 info=inspect(r);f=r['question'][':question/answer-fields'][0]
 cases.append({'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if j==info['correct_index'] else 'rejected','purpose':'Independently solve visible equations and test every option'} for j,c in enumerate(f[':answer-field/choices'])]})
save('grader-input.json',cases)
save('render-records.json',[replays[0],*pairs,*batch,*boundaries])
inv=load(JOB/'source/inventory.json');ids={q[':question/id'] for q in sq.values()}
assert all(q[':question/id'] in ids for q in inv['questions'])
save('inventory-review.json',{'basis':inv['basis'],'count':len(inv['questions']),'generated_records':0,'original_ids':[q[':question/id'] for q in inv['questions']],'conclusion':'Verified every inventory ID is an original instructional source. No generated stored records eligible for this repair. No generated history omitted by retirement filtering.'});save('affected-inventory.json',{'affected_questions':[]})
save('scope-results.json',{'method':'Independent equation solution and source workload comparison; code inspection confirms unchanged coefficient triples and two substitution stages.','normal_count':len(normal),'profiles':list(g.PARAMETERS),'representations':['xyz','indexed','angle','column'],'rational_denominators':sorted({int(sp.Rational(v).q) for m in results['samples'] for v in m['solution']}),'extensions':'Correct role sampled independently; signs and small integer shifts change eligible assignments without new prerequisites. Explicit legacy scales checked separately; normal scale is 1.','unsupported':'Incomplete q-20451, unchanged source gap.'})
(ROOT/'session-state.md').write_text('Source reverified before package inspection. All 12 complete source banks replay. Independent exact math passes 60 normal, 60 controlled, 5 batch, 2 boundary and 3 counterfactual records. Prior two failures reproduced on old package; exact shortcut defeated on current. Native grader and rendering inputs ready. Inventory: 13 original sources, zero generated.\n')
print(json.dumps({'replays':len(replays),'normal':len(normal),'controlled':len(controlled),'batch':len(batch),'native_cases':len(cases),'math':'passed'}))
