import sys,os,pathlib,json,re,hashlib,importlib.util,collections,platform,subprocess,shutil
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy');P=R/'.venv/bin/python'
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=module(W/'17592186124674.py','current')
def q(r):return r['question']
def f(r):return q(r)[':question/answer-fields'][0]
def opts(r):return f(r)[':answer-field/choices']
def key(r):return f(r).get(':answer-field/correct',[None,None])[1]
def val(r):return next(c[':answer/value'] for c in opts(r) if c[':answer/id']==key(r))
def clean(x):return re.sub(r'\s+','',x.replace('\\\\','\\'))
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
trans=standard_transformations+(implicit_multiplication_application,)
def rhs(v):
 x=v.replace('\\\\','\\').split('=',1)[1];x=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',x)
 return sp.expand(parse_expr(x.replace('{','(').replace('}',')').replace('^','**'),local_dict={c:sp.Symbol(c) for c in 'kNMTBCPVRSFH'},transformations=trans))
def facts(r):
 prompt=q(r)[':question/problem'];s=re.search(r'\$([A-Z])\(t\)\$',prompt)[1];a=int(re.search(r'maximum.+?is \$(\d+)\$',prompt)[1]);X=sp.Symbol(s);k=sp.Symbol('k')
 eq=[rhs(c[':answer/value']) for c in opts(r)];matches=[c[':answer/id'] for c,e in zip(opts(r),eq) if sp.expand(e-k*(a-X))==0]
 linear=[i for i,x in enumerate(eq) if sp.degree(x,X)==1 and x.coeff(X)==-k and x.subs(X,0)/k>0]
 idx=next(i for i,c in enumerate(opts(r)) if c[':answer/id']==key(r));caps={i:int(eq[i].subs(X,0)/k) for i in linear};lens=[len(clean(c[':answer/value'])) for c in opts(r)]
 assert matches==[key(r)] and len(set(eq))==5,(q(r)[':question/id'],matches)
 assert str(a)+'-'+s in clean(q(r)[':question/worked-solution'])
 return {'id':q(r)[':question/id'],'capacity':a,'symbol':s,'template':r['generation']['template'],'kind':'mixed' if len(linear)==2 else 'capacities','position':idx,'rank':sorted(caps.values()).index(a),'linear_count':len(linear),'lengths':lens,'shortest_first':idx==min(range(5),key=lens.__getitem__),'unique_shortest':lens.count(min(lens))==1 and lens[idx]==min(lens),'longest_first':idx==max(range(5),key=lens.__getitem__),'minimum_capacity':caps[idx]==min(caps.values()),'maximum_capacity':caps[idx]==max(caps.values()),'middle_linear_capacity':idx==sorted(linear,key=lambda i:caps[i])[len(linear)//2]}
# Original source fidelity is checked on all complete banks, before extensions.
src=load(J/'source/source.json');sources=src['material']['kp'][':knowledge-point/questions'];replays=[];replay=[]
expected=[('P',70),('R',85),('N',150),('T',95),('M',60),('F',100),('S',500),('P',240),('B',50),('C',1000),('V',90),('V',250),('B',110),('H',75)]
for source,(symbol,cap) in zip(sources,expected):
 r=g.replay_current_source(source[':question/math-academy-id'],seed=927);replays.append(r);sf=source[':question/answer-fields'][0];checks={'prompt':q(r)[':question/problem']==source[':question/problem'],'solution':q(r).get(':question/worked-solution')==source.get(':question/worked-solution'),'complete_bank':sorted(c[':answer/value'] for c in opts(r))==sorted(c[':answer/value'] for c in sf[':answer-field/choices']),'key_or_absence':(val(r) if key(r) else None)==sf.get(':answer-field/correct',{}).get(':answer/value'),'difficulty_or_absence':q(r).get(':question/difficulty')==(source.get(':question/difficulty') or {}).get(':db/ident')}
 target=sp.Symbol('k')*(cap-sp.Symbol(symbol));matches=[c for c in opts(r) if sp.expand(rhs(c[':answer/value'])-target)==0];checks['independent_model']=len(matches)==1 and (not key(r) or matches[0][':answer/id']==key(r));assert all(checks.values()),checks
 replay.append({'source_id':source[':question/id'],'checks':checks})
save('source-replay-records.json',replays);save('source-replay-results.json',{'passed':True,'cases':replay,'gaps':load(E/'source-analysis.json')['source_gaps'],'canonical':'Capacity 200 gives k(200-P); original canonical bank absent, so no bank claim.'})
# Fresh seeds independently selected, unrelated to author check sample.
fresh=[g.generate_easy(seed=s) for s in range(71631,71655)];batch=load(J/'samples.json');save('fresh-records.json',fresh);save('runner-batch.json',batch)
# Counterfactual fixed banks change only equilibrium; irrelevant stock changes preserve response.
pair=[g.generate_easy(seed=9901,template='source_17592186308739',parameters={'capacity':a,'initial':10,'candidates':[95,30,60,100,950]}) for a in (95,60)]
pair.append(g.generate_easy(seed=9901,template='source_17592186308739',parameters={'capacity':60,'initial':20,'candidates':[95,30,60,100,950]}))
seed=next(s for s in range(903,913) if g.generate_easy(seed=s,parameters={'context':'deer','capacity':60})['generation']['bank_kind']=='mixed')
for cap,rank in [(60,0),(95,1)]:pair.append(g.generate_easy(seed=seed,parameters={'context':'deer','capacity':cap,'candidates':[60,95],'target_rank':rank,'linear_indices':[0,1]}))
save('counterfactual-records.json',pair)
def bank(r):return sorted(c[':answer/value'] for c in opts(r))
assert bank(pair[0])==bank(pair[1])==bank(pair[2]) and val(pair[0])!=val(pair[1])==val(pair[2]);assert q(pair[1])[':question/worked-solution']==q(pair[2])[':question/worked-solution']
assert len({tuple(bank(r)) for r in pair[3:]})==1 and len({val(r) for r in pair[3:]})==2
save('counterfactual-results.json',{'passed':True,'command':str(P)+' -B independent_review.py','capacity_pair':'counterfactual-records.json indices 0/1: 95->60; same initial10 and bank','irrelevant_pair':'indices1/2: initial10->20; same bank, key value and solution','mixed_role_pair':'indices3/4: capacity60/95, both positive-linear targets, same bank and context','models':[val(r) for r in pair],'render_and_native_grading':'render-pairs/rendering.json and native-grader-results.json'})
# Retained exact counterexamples, boundary valid/invalid calls.
minimal=g.generate_easy(seed=88,parameters={'context':'deer','capacity':20});fixed=g.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':60,'initial':10});bounds=[minimal,fixed]+[g.generate_easy(seed=89,parameters={'context':'deer','capacity':a}) for a in (99,100,499,500)]+[g.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':a,'initial':1}) for a in (10,5000)]
save('boundary-records.json',bounds)
invalid=[]
for p in [{'context':'deer','capacity':19},{'context':'deer','capacity':501},{'context':'deer','capacity':True},{'context':'absent','capacity':50},{'context':'deer','capacity':60,'candidates':[30,30,60,70,80]},{'context':'deer','capacity':60,'candidates':[30,40,60,70,80],'target_rank':0}]:
 try:g.generate_easy(seed=88,parameters=p);out='UNEXPECTED_ACCEPT'
 except ValueError as ex:out=str(ex)
 invalid.append({'parameters':p,'outcome':out});assert out!='UNEXPECTED_ACCEPT'
# Independent polynomial validation applies to changed rules and small sample, plus author controlled witnesses.
controlled=load(E/'author-check-rerun/regression-records.json')[3:71]
all_groups={'fresh':fresh,'batch':batch,'pairs':pair,'boundaries':bounds,'controlled':controlled};math=[]
for name,rs in all_groups.items():
 for r in rs:math.append({'group':name,**facts(r)})
save('math-results.json',{'passed':True,'method':'Prompt-derived capacity/symbol; independent exact polynomial checks of every displayed equation, one correct model, five distinct RHSs, solution follows prompt.','cases':math})
# Actual grader receives all choices for exact batch, both pair kinds and representative fresh/boundaries/source banks.
grader=[]
for label,rs in [('batch',batch),('pairs',pair),('fresh',fresh[:4]),('boundaries',bounds),('source',replays)]:
 for i,r in enumerate(rs):
  if not key(r):continue
  grader.append({'label':label+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key(r) else 'rejected','purpose':'Independent model calculation; test all plausible radio alternatives'} for c in opts(r)]})
save('native-grader-input.json',grader)
# Verify prior restriction failure on the original registered generator, without edits or writes.
old=module(R/'generate/scratch/17592186124674.py','original_registered')
try:old.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':60,'initial':10});prior='UNEXPECTED_ACCEPT'
except ValueError as ex:prior=str(ex)
assert prior=='whole observed bank needs bounded integer constants';assert not fixed['generation']['evidence_only'];assert not facts(minimal)['unique_shortest']
save('repair-verification.json',{'preflight':'repair-preflight.json claimed both findings pass; reran the same executable with only output paths adapted.','author_current_result':load(E/'author-check-rerun/regression-results.json'),'prior_shortest':'prior-failure-shortcut.json; author check --records prior-boundary-records.json exits1 on unique_shortest2/2','restriction_prior':prior,'restriction_current':'accepted; k(60-T), learning eligible','normal_capacities_family_present':any(facts(r)['kind']=='capacities' for r in fresh),'strict_tests_retained':True})
# Exact versions, relocation and metadata deterministic replay.
manifest=load(W/'package.json');deps=manifest['dependencies'];assert deps=={'python':platform.python_version(),'packages':{'sympy':sp.__version__}}
rel=E/'relocated';rel.mkdir(exist_ok=True)
for path in manifest['files']:
 dest=rel/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/path,dest)
cmd=[str(P),'-B',str(rel/manifest['entrypoint']),'--difficulty','easy','--seed','71631','--count','1','--format','json'];proc=subprocess.run(cmd,capture_output=True,text=True,cwd=E);assert proc.returncode==0;rel_rs=json.loads(proc.stdout);assert rel_rs==fresh[:1];save('relocation-records.json',rel_rs)
assert all(g.generate_easy(seed=r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'])==r for r in fresh+batch)
save('packaging-results.json',{'dependencies':deps,'exact_runtime_match':True,'deterministic_replay_count':len(fresh+batch),'relocation_command':cmd,'relocation_match':True,'invalid_parameters':invalid,'rejection':'Normal easy constructs a feasible bank directly; no rejection/resampling. Explicit invalid boundaries raise ValueError.','external_outputs':'No generated images or external output paths in runtime; two JSON files resolved relative to __file__.','manifest_files_only':True})
# Matched historical inventory evidence can be reused, but recheck captured IDs and complete records.
inv=load(J/'source/inventory.json');records=load(E/'prior-generated-records.json');sourceids={s[':question/id'] for s in sources};nonoriginal=[x for x in inv['questions'] if x[':question/id'] not in sourceids];checks=[];reproduced=[]
for stored in nonoriginal:
 original=next(r for r in records if q(r)[':question/id']==stored[':question/id']);meta=original['generation'];r=g.generate(q(original)[':question/difficulty'].split('/')[-1],seed=meta['seed'],parameters=meta['parameters']);assert r==original;assert q(r)[':question/problem']==stored[':question/problem'];assert bank(r)==sorted(x[':answer/value'] for x in stored[':question/answer-fields'][0][':answer-field/choices']);reproduced.append(r);checks.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'difficulty':q(r)[':question/difficulty'],'complete_generation_reproduced':True})
save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':[]});save('inventory-results.json',{'basis':inv['basis'],'stored_count':len(inv['questions']),'source_originals':len(sourceids),'generated_reproductions':checks,'result':'Verified no generated easy instances at captured basis; all ten generated records are moderate/hard and reproduce exactly. Original source questions are not marked generated. Broader moderate/hard pedagogical audit is outside this changed-easy review.'})
save('scope-results.json',{'passed':True,'requested':'easy','result':'Changed mixed banks combine source-supported signs/factors with two competing capacities; all-capacity banks require equilibrium discrimination. Same five-radio first-order ODE modeling operation; no solving, integration or fitting. Same source formal-model then substitution explanation.','factory_units':'Normal source factory fixes stock capacity units/day to units in prompt and solution; replay preserves captured text.','sample_files':['fresh-records.json','runner-batch.json','counterfactual-records.json']})
(E/'session-state.md').write_text('Source replay14/14, independent changed-rule math, retained failure checks and current repair, fixed-bank relevant/irrelevant pairs, package relocation/dependencies/determinism and inventory reproduction complete. Next: native grader, delivery/selection, render and inspect, variation/report.\n')
print(json.dumps({'replay':len(replay),'fresh':len(fresh),'math_records':len(math),'native_grader_records':len(grader),'inventory_reproduced':len(reproduced),'fresh_kinds':dict(collections.Counter(facts(r)['kind'] for r in fresh))}))
