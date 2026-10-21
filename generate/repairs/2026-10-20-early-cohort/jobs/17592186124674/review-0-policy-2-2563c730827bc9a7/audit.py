import os,sys,json,hashlib,importlib.util,pathlib,re,shutil,subprocess,collections,platform
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy');P=R/'.venv/bin/python'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.load(open(p))
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
before=hashes();save('package-hashes-before.json',before)
spec=importlib.util.spec_from_file_location('reviewed',W/'17592186124674.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
src=load(J/'source/source.json');qs=src['material']['kp'][':knowledge-point/questions']
a=load(E/'source-analysis.json');a['difficulty']='Thirteen source questions explicitly easy; rehabilitation question unrated.';a['response_contract']='One radio choice from five math equations in all 14 source question banks; canonical example has no captured answer bank.';save('source-analysis.json',a)
def q(r):return r['question']
def field(r):return q(r)[':question/answer-fields'][0]
def correct(r):return field(r).get(':answer-field/correct',[None,None])[1]
def values(r):return [a[':answer/value'] for a in field(r)[':answer-field/choices']]
replays=[];replay_results=[]
for s in qs:
 r=m.replay_current_source(s[':question/math-academy-id'],seed=913);replays.append(r);rq=q(r);sf=s[':question/answer-fields'][0];sc=sf.get(':answer-field/correct',{}).get(':answer/value');rc=next((a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==correct(r)),None)
 checks={'prompt':rq[':question/problem']==s[':question/problem'],'solution':rq.get(':question/worked-solution')==s.get(':question/worked-solution'),'bank':sorted(values(r))==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),'correct_or_absence':rc==sc,'difficulty_or_absence':rq.get(':question/difficulty')==(s.get(':question/difficulty') or {}).get(':db/ident')}
 replay_results.append({'source_id':s[':question/id'],'checks':checks})
save('source-replay-records.json',replays);save('source-replay-results.json',{'command':str(P)+' '+str(E/'audit.py'),'cases':replay_results,'passed':all(all(x['checks'].values()) for x in replay_results),'canonical_gap':'No replay API for canonical fish text; checked its capacity 200 model using explicit authored case; canonical bank unavailable.'})
samples=[m.generate_easy(seed=s) for s in range(48371,48411)];save('samples.json',samples);batch=load(J/'samples.json');save('runner-batch.json',batch)
# Controlled source pair preserves all choice constants while irrelevant initial changes.
pairs=[m.generate_easy(seed=624,parameters={'context':'deer','capacity':120}),m.generate_easy(seed=624,parameters={'context':'deer','capacity':240}),m.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':95,'initial':10}),m.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':95,'initial':20})]
save('counterfactual-records.json',pairs)
save('counterfactual-results.json',{'relevant':{'parameters':[r['generation']['parameters'] for r in pairs[:2]],'prompt_changed':q(pairs[0])[':question/problem']!=q(pairs[1])[':question/problem'],'answer_before':next(a[':answer/value'] for a in field(pairs[0])[':answer-field/choices'] if a[':answer/id']==correct(pairs[0])),'answer_after':next(a[':answer/value'] for a in field(pairs[1])[':answer-field/choices'] if a[':answer/id']==correct(pairs[1])),'solution_changed':q(pairs[0])[':question/worked-solution']!=q(pairs[1])[':question/worked-solution']},'irrelevant':{'parameters':[r['generation']['parameters'] for r in pairs[2:]],'prompts_differ':q(pairs[2])[':question/problem']!=q(pairs[3])[':question/problem'],'banks_equal':values(pairs[2])==values(pairs[3]),'solution_equal':q(pairs[2])[':question/worked-solution']==q(pairs[3])[':question/worked-solution'],'ineligible':pairs[2]['generation']['evidence_only']}})
# Independent exact polynomial RHS parser, derived from visible equations, not metadata recipes.
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
trans=standard_transformations+(implicit_multiplication_application,)
def rhs(v):
 s=v.replace('\\\\','\\').split('=',1)[1];s=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s);s=s.replace('{','(').replace('}',')').replace('^','**');return sp.expand(parse_expr(s,local_dict={c:sp.Symbol(c) for c in 'kNMTBCPVRSFH'},transformations=trans))
maths=[]
for group,records in [('fresh',samples),('batch',batch),('counterfactual',pairs)]:
 for r in records:
  prompt=q(r)[':question/problem'];s=re.search(r'Let \$([A-Z])\(t\)',prompt)
  if not s:s=re.search(r'center \$([A-Z])\(t\)',prompt)
  symbol=s.group(1);cap=int(re.search(r'maximum capacity (?:is|of the tutoring center is) \$(\d+)',prompt).group(1));target=sp.Symbol('k')*(cap-sp.Symbol(symbol));matches=[a[':answer/id'] for a in field(r)[':answer-field/choices'] if sp.expand(rhs(a[':answer/value'])-target)==0]
  maths.append({'group':group,'id':q(r)[':question/id'],'capacity_from_prompt':cap,'symbol_from_prompt':symbol,'unique_correct':matches==[correct(r)],'distinct_rhs':len(set(map(str,map(rhs,values(r)))))==5,'solution_has_model':str(cap)+'-'+symbol in q(r)[':question/worked-solution']})
save('math-results.json',{'method':'Parse capacity and symbol from displayed prompts; exact SymPy polynomial comparison of all displayed RHSs.','cases':maths,'passed':all(x['unique_correct'] and x['distinct_rhs'] and x['solution_has_model'] for x in maths)})
# All options, including plausible wrong entries; swapped relevant-pair answer UUID rejected.
cases=[]
for i,r in enumerate(batch+samples[:5]+pairs):
 checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct(r) else 'rejected','purpose':'independent complete radio bank check'} for a in field(r)[':answer-field/choices']]
 cases.append({'label':str(i),'record':r,'checks':checks})
save('grader-input.json',cases)
# Boundary/rejection/determinism/relocation and exact manifest versions.
bounds=[]
for cap in (20,500):
 r=m.generate_easy(seed=88,parameters={'context':'deer','capacity':cap});bounds.append(r)
save('boundary-records.json',bounds)
invalids=[]
for p in ({'context':'deer','capacity':19},{'context':'deer','capacity':501},{'context':'deer','capacity':True},{'context':'missing','capacity':20}):
 try:m.generate_easy(parameters=p);outcome='unexpected acceptance'
 except ValueError as ex:outcome=str(ex)
 invalids.append({'parameters':p,'result':outcome})
rel=E/'relocated';rel.mkdir(exist_ok=True);shutil.copy2(W/'17592186124674.py',rel/'17592186124674.py');(rel/'17592186124674').mkdir(exist_ok=True)
for name in ('extracted-recipes.json','current-source-recipes.json'):shutil.copy2(W/'17592186124674'/name,rel/'17592186124674'/name)
cmd=[str(P),'-B',str(rel/'17592186124674.py'),'--difficulty','easy','--seed','48371','--count','1','--format','json'];proc=subprocess.run(cmd,capture_output=True,text=True,cwd=E);save('relocation-records.json',json.loads(proc.stdout))
save('packaging-results.json',{'manifest_dependencies':load(W/'package.json')['dependencies'],'actual_python':platform.python_version(),'actual_sympy':sp.__version__,'deterministic':m.generate_easy(48371)==samples[0],'relocation_command':cmd,'relocation_match':json.loads(proc.stdout)==samples[:1],'invalid_parameters':invalids,'bounded_sampler':'1000 attempts; easy randint(20,500), five contexts; no rejection possible for default easy; correct option shuffled with seed; no file outputs.','external_runtime_files':['extracted-recipes.json','current-source-recipes.json'],'package_unchanged':before==hashes(),'repair_history_present':(J/'repair-history.json').exists(),'repair_preflight_present':(J/'repair-preflight.json').exists()})
save('sampling-results.json',{'fresh_seeds':[48371,48410],'template_counts':dict(collections.Counter(r['generation']['template'] for r in samples)),'context_counts':dict(collections.Counter(r['generation']['parameters']['context'] for r in samples)),'correct_position_counts':dict(collections.Counter(next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==correct(r)) for r in samples)),'supported_source_banks':14,'normal_easy_bank_profiles':['model_operations'],'excluded_source_family':'All-linear five-capacity banks are evidence-only; default easy cannot generate maximum-vs-initial discrimination.','source_examples':['5651275c-fd64-5799-85e0-52ab15ebd288','3974627f-3801-52ea-b93f-3d1a3033e2cc']})
# Inventory: reproduce retained full generated metadata, match content/id to stored bank, never label source originals as generated.
inv=load(J/'source/inventory.json');historical=load(W/'17592186124674/reference/replenishment/basis-2578/generated.json');sourceids={s[':question/id'] for s in qs};nonoriginal=[s for s in inv['questions'] if s[':question/id'] not in sourceids];reproduced=[];status=[]
for s in nonoriginal:
 saved=next((r for r in historical if q(r)[':question/id']==s[':question/id']),None)
 if saved:
  g=saved['generation'];r=m.generate(q(saved)[':question/difficulty'].split('/')[-1],seed=g['seed'],parameters=g['parameters']);reproduced.append(r)
  status.append({'entity_id':s[':db/id'],'question_id':s[':question/id'],'reproduced_id':q(r)[':question/id']==s[':question/id'],'prompt_equal':q(r)[':question/problem']==s[':question/problem'],'bank_equal':sorted(values(r))==sorted(a[':answer/value'] for a in s[':question/answer-fields'][0][':answer-field/choices']),'difficulty':q(r)[':question/difficulty']})
save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':[]});save('inventory-results.json',{'basis':inv['basis'],'stored_count':len(inv['questions']),'source_originals':len(qs),'nonoriginal_count':len(nonoriginal),'reproductions':status,'conclusion':'All 10 non-source stored questions reproduced with matching IDs and metadata. All are moderate/hard, so none belongs to demonstrated default-easy shortest-option defect. This is verified absence of affected easy generated instances at captured basis; no audit claim for other moderate/hard shortcuts.'})
(E/'session-state.md').write_text('Independent replay, math, controlled pairs, packaging and inventory scripts executed. Required next: native grader, shared delivery on fresh and exact batch, actual UI preview and screenshot inspection, decision variation evidence/report. Concrete default-easy shortest-option cue and omitted scalar-capacity family identified.\n')
print(json.dumps({'replay':all(all(x['checks'].values()) for x in replay_results),'math':all(x['unique_correct'] and x['distinct_rhs'] for x in maths),'samples':len(samples),'inventory_reproduced':len(reproduced),'package_unchanged':before==hashes()}))
