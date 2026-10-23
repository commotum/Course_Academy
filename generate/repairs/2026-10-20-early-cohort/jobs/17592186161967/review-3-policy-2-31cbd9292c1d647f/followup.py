import ast,sys,pathlib,json,collections,importlib.util,hashlib
sys.dont_write_bytecode=True
from helpers import mats,ops,check
R=pathlib.Path(__file__).resolve().parent;J=R.parent;PKG=J/'workspace'
s=importlib.util.spec_from_file_location('subject',PKG/'17592186161967.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
a=ast.parse((R/'review.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ['bank','analyze','metrics']],type_ignores=[]),'analysis-functions','exec'))
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,default=int)+'\n')
assert json.load(open('relocated.log'))==g.batch('easy',5,1278010737)==json.load(open('batch.json'))
cli=[];summaries=[]
for seed,count in [(49217,12),(10983,5),(483,2),(904,3)]:
 rr=g.batch('easy',count,seed);cli+=rr;summaries.append({'seed':seed,'count':count,'metrics':metrics(rr)})
 assert g.batch('easy',count,seed)==rr
save('fresh-cli.json',cli);save('fresh-cli-results.json',summaries)
# Exact first retained minimal record; complete records for negative control evidence.
s=importlib.util.spec_from_file_location('old',R/'control-old-bank/17592186161967.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
base={'A':[[1,2,3],[2,5,4],[-3,7,8]],'pivot':0,'column':0,'ks':[0,-2,3]}
save('negative-bank-records.json',[old.generate(seed=472,bank_profile='q-42531',parameters=base)])
save('negative-batch-records.json',json.load(open(J/'review-1-policy-2-fa94c3c9d1dc4929/batch.json')))
assert json.load(open('control-old-batch/evidence/batch-repair/prospective.json'))==json.load(open('negative-batch-records.json'))
post={};sel={}
for name in ['batch','fresh']:
 rr=json.load(open(R/f'delivery-{name}/accepted.json'));post[name]=metrics(rr);draws=[]
 for i in range(40):
  seed=f'independent-review-3-{i}';d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();ix=int(((int.from_bytes(d[8:16],'big')>>11)/(1<<53))*len(rr));z=analyze(rr[ix]);draws.append({'seed':seed,'candidate_rank':ix,'question_id':z['id'],'shortcut_success':z['success']})
 sel[name]={'eligible_count':len(rr),'draws':draws,'shortcut_successes':sum(x['shortcut_success'] for x in draws)}
sel['captured_basis']=5580;sel['rules']='question_selection.rs select sorts unique entity IDs; positive easy weight makes easy pool uniformly selectable via SHA256 offset 8. Empty learner history modeled; all 5 delivered batch members remain eligible. No weights: first eligible; zero easy weight: none of this rated pool. Seen/current-prefix questions are removed upstream. Entity order unknown before publication, so file-rank model shows one possible ordering; uniform reachability and both sign counterexamples hold for every permutation.'
sel['limits']='No live database/policy or learner history. A learner who has already exhausted some cases can have an unbalanced remaining pool; that does not invalidate the complete captured candidate pool. Original inventory is ten source questions, no generated records, eligible or retired.'
save('selection.json',sel);save('post-delivery-shortcuts.json',post)
p=json.load(open('packaging.json'));p.pop('relocation_pending');p['relocation_equal']=True;p['runner_batch_exact_replay']=True
save('packaging.json',p)
save('scope-review.json',{'source':'source-analysis.json','observed':'All source profiles retain the 3x3 two row-addition, five-choice easy response. All nine pivot/column coordinates tested; pivot magnitude 3 and target magnitude 12 boundary. No unsupported source family removed. Swap-magnitude banks need unequal magnitudes; unit perturbation needs at least one magnitude >1 for distinct choices. Moderate/hard rejected. Batch construction selects a magnitude shape for small pools but all profiles remain accessible in larger pools and direct sampling.','reused_previous':'../review-1-policy-2-fa94c3c9d1dc4929/scope-review.json','new_review':'Batch filtering changes signs/profile mixture, not mathematical operations, coefficient limits, or workload.'})
(R/'session-state.md').write_text('Completed 111 independent math cases, 10 complete source replays, source canonical, controlled target/sign/irrelevant pairs, both retained negative and positive controls, runner batch exact replay and relocation. Delivery: batch 5/5; direct fresh 8/40 unique survivors. Current batch shortcut 2/5 vs historical 5/5. Fresh CLI boundary batches sampled; native grading and rendering in progress.\n')
print(json.dumps({'fresh_cli':[(x['seed'],x['count'],x['metrics']['groups']) for x in summaries],'post_delivery':{k:v['groups'] for k,v in post.items()}}))
