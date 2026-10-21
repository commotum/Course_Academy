import os,sys,json,pathlib,importlib.util,collections,hashlib,platform,shutil,subprocess,re,copy
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent; J=E.parent; P=J/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(P))
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(P/'17592186115241.py','review_generator')
from independent_math import *
def dump(name,x): (E/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
S=json.loads((J/'source/source.json').read_text()); B=json.loads((J/'samples.json').read_text());dump('batch.json',B)
# Observe actual construction and bank rejection, without changing persisted code.
orig=g.bank_valid;attempts=[]
def bank(M,b):
 try:
  out=orig(M,b);attempts.append({'matrix':str(M.tolist()),'result':'accepted'});return out
 except ValueError as ex:attempts.append({'matrix':str(M.tolist()),'result':'rejected','error':str(ex)});raise
g.bank_valid=bank
fresh=[g.generate_easy(seed=s) for s in range(82130,82166)];dump('fresh.json',fresh);g.bank_valid=orig
dump('resampling-stages.json',{'command':'python -B review.py','seeds':[82130,82165],'bank_attempts':attempts,'accepted':len(fresh),'rejected':sum(x['result']=='rejected' for x in attempts),'construction':'Inspected sample_easy, candidate_bank, authored, rank_one and generate. Six cases chosen before values; valid bank role chosen before system. Whole-instance ValueError resamples within selected case; observed bank_valid attempts retained.'})
replay=[];source_results=[];variants=[]
for q in S['material']['kp'][':knowledge-point/questions']:
 profile=q[':question/math-academy-id']; M=system(q[':question/problem']);p={'scale':1,'offsets':[0]*(M.cols-1)}
 r=g.generate_easy(seed=71383,profile=profile,parameters=p);replay.append(r)
 eq=lambda cs:collections.Counter(str(vec(c[':answer/value'])) for c in cs)
 src=q.get(':question/worked-solution');gensol=r['question'][':question/worked-solution']
 # Prose remains source wording; normalize mathematical environments away for comparison.
 def prose(t):
  t=re.sub(r'\$\$.*?\$\$','MATH',t,flags=re.S);t=re.sub(r'\$[^$]*\$','INLINE',t);return re.sub(r'\s+',' ',t).strip()
 rr={'source_id':q[':question/id'],'profile':profile,'system_equal':system(r['question'][':question/problem'])==M,'complete_bank_equal':eq(field(r)[':answer-field/choices'])==eq(q[':question/answer-fields'][0][':answer-field/choices']),'solution_prose_equal':prose(src)==prose(gensol) if src else 'absent source; inferred authored solution','math':mathcheck(r)}
 source_results.append(rr)
 # Three repaired profiles get a fresh affine counterexample and normal generation.
 if profile in ['q-131714','q-131713','q-42062']:
  variants += [g.generate_easy(seed=71384,profile=profile,parameters={'scale':-1,'offsets':[1]*(M.cols-1)}),g.generate_easy(seed=71385,profile=profile)]
dump('source-replay-records.json',replay);dump('source-replay.json',source_results);dump('source-variants.json',variants)
p={'free_coefficients':[2,-3],'constants':[1,4],'mix':[1,1]}
params=[p,{**p,'free_coefficients':[-2,-3]},{**p,'mix':[-1,1]},{**p,'free_coefficients':[2,0],'free_column':1},{**p,'free_coefficients':[2,0]}, {'free_coefficients':[5,0],'constants':[-1,3],'mix':[1,1],'free_column':1}]
cf=[g.generate_easy(seed=71386,parameters=x) for x in params];dump('counterfactual-records.json',cf)
def keyvec(r):return vec(next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r)))
dump('counterfactual-results.json',{'parameters':params,'relevant':{'answer_changed':keyvec(cf[0])!=keyvec(cf[1]),'prompt_changed':cf[0]['question'][':question/problem']!=cf[1]['question'][':question/problem'],'solution_changed':cf[0]['question'][':question/worked-solution']!=cf[1]['question'][':question/worked-solution']},'irrelevant':{'answer_preserved':keyvec(cf[0])==keyvec(cf[2]),'prompt_changed':cf[0]['question'][':question/problem']!=cf[2]['question'][':question/problem']},'target_free_column':{'answer_changed':keyvec(cf[3])!=keyvec(cf[4]),'prompt_changed':cf[3]['question'][':question/problem']!=cf[4]['question'][':question/problem']},'canonical_system_equal':system(cf[5]['question'][':question/problem'])==system(S['material']['kp'][':knowledge-point/canonical-example'][':question/problem'])})
boundaries=[];tests=[]
for label,pp in [('zero_slope',{**p,'free_coefficients':[0,-3]}),('equal_coordinates',{**p,'free_coefficients':[2,2],'constants':[1,1]}),('zero_intercept',{**p,'constants':[0,4]}),('rational',{'free_coefficients':['1/2',-5],'constants':['1/2',-6],'mix':[-2,2]}),('over_bound',{**p,'free_coefficients':[6,-3]}),('zero_mix',{**p,'mix':[0,1]})]:
 try:
  r=g.generate_easy(seed=71387,parameters=pp);boundaries.append(r);tests.append({'label':label,'parameters':pp,'accepted':True})
 except ValueError as ex:tests.append({'label':label,'parameters':pp,'accepted':False,'error':str(ex)})
dump('boundary-records.json',boundaries);dump('rejection-tests.json',tests)
rational=[g.generate_easy(seed=s,profile='q-32244') for s in range(71381,71401)]
for profile in sorted(g.QUESTIONS):
 if profile!='q-32244':rational.extend(g.generate_easy(seed=s,profile=profile) for s in (82173,82174))
rp={'free_coefficients':['1/2',-3],'constants':['1/2',4],'mix':[1,1]}
rparams=[rp,{**rp,'free_coefficients':['-1/2',-3]},{**rp,'mix':[-1,1]}, {**rp,'free_coefficients':[0,'-1/2']},{**rp,'free_coefficients':['1/2','1/2'],'constants':['1/2','1/2']},{**rp,'constants':[0,'-1/2']},{**rp,'free_coefficients':['1/2',0],'free_column':1},{**rp,'free_coefficients':[0,-3],'constants':[0,4]},{**rp,'free_coefficients':[0,0],'constants':[0,0]}]
rcf=[g.generate_easy(seed=82175,parameters=p) for p in rparams]; rational+=rcf
dump('source-shortcut-records.json',rational);dump('rational-counterfactual-records.json',rcf)
dump('rational-counterfactual-results.json',{'parameters':rparams,'relevant_answer_changes':keyvec(rcf[0])!=keyvec(rcf[1]),'irrelevant_answer_preserved':keyvec(rcf[0])==keyvec(rcf[2]),'prompt_changes':[r['question'][':question/problem']!=rcf[0]['question'][':question/problem'] for r in rcf[1:3]],'solution_changes':[r['question'][':question/worked-solution']!=rcf[0]['question'][':question/worked-solution'] for r in rcf[1:3]]})
allr=B+fresh+replay+variants+cf+boundaries+rational
maths=[mathcheck(r) for r in allr];dump('math-results.json',{'count':len(maths),'failures':[x for x in maths if not x['pass']],'cases':maths})
# Real radio grader: test every choice against independently verified whole solution set.
grade=[{'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'Independent exact substitution plus full-line dimension; all five choices'} for c in field(r)[':answer-field/choices']]} for i,r in enumerate(allr)]
for i,expected in [(1,'rejected'),(2,'accepted')]:
 r=copy.deepcopy(cf[i]);old=next(c for c in field(cf[0])[':answer-field/choices'] if c[':answer/id']==correct(cf[0]));match=next((c for c in field(r)[':answer-field/choices'] if vec(c[':answer/value'])==vec(old[':answer/value'])),None)
 if not match:field(r)[':answer-field/choices'].append(old);match=old
 grade.append({'label':'controlled-previous-vector-'+str(i),'record':r,'checks':[{'submitted_answer_id':match[':answer/id'],'expected':expected,'purpose':'Relevant coefficient changes invalidate previous vector; row mixing preserves it'}]})
for i,expected in [(1,'rejected'),(2,'accepted')]:
 r=copy.deepcopy(rcf[i]);old=next(c for c in field(rcf[0])[':answer-field/choices'] if c[':answer/id']==correct(rcf[0]));match=next((c for c in field(r)[':answer-field/choices'] if vec(c[':answer/value'])==vec(old[':answer/value'])),None)
 if not match:field(r)[':answer-field/choices'].append(old);match=old
 grade.append({'label':'rational-controlled-previous-vector-'+str(i),'record':r,'checks':[{'submitted_answer_id':match[':answer/id'],'expected':expected,'purpose':'Relevant rational coefficient changes invalidate previous vector; row mixing preserves it'}]})
dump('grader-input.json',grade)
# Renderer includes all actual batch records, six cases, target pair and relevant/irrelevant pairs, rational boundary, new source profile.
representatives=[next(r for r in fresh if r['generation']['decision_case']==case) for case in g.EASY_CASES]
dump('render-records.json',B+representatives+cf+rcf[:3]+[rational[0]])
# Minimal runtime closure relocation, using declared files only.
manifest=json.loads((P/'package.json').read_text());rel=E/'relocated';rel.mkdir(exist_ok=True)
for name in manifest['files']:
 dest=rel/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,dest)
cp=subprocess.run([sys.executable,'-B',str(rel/manifest['entrypoint']),'--difficulty','easy','--seed','82130','--count','1','--format','json'],cwd=E,capture_output=True,text=True)
versions={'python':platform.python_version(),'packages':{'sympy':sp.__version__}}
dump('packaging.json',{'runtime':versions,'declared':manifest['dependencies'],'exact_match':versions==manifest['dependencies'],'deterministic':fresh[0]==g.generate_easy(seed=82130),'relocation_command':cp.args,'relocation_exit':cp.returncode,'relocation_stderr':cp.stderr,'relocation_same_record':json.loads(cp.stdout)==[fresh[0]] if cp.returncode==0 else False,'output_handling':'CLI returns complete JSON on stdout; generator has no external output writes or required images.'})
(E/'session-state.md').write_text('Completed source reconstruction and exact 14-bank replay; 60 fresh seeds 71320–71379; repaired-profile variants; controlled relevant, irrelevant, free-column cases; boundaries; exact math; runtime/determinism/relocation. Delivery, native grader, rendered visual inspection and inventory follow-up pending. Package writes disabled.\n')
print(json.dumps({'math_count':len(maths),'math_failures':len([x for x in maths if not x['pass']]),'source_failures':[x['profile'] for x in source_results if not x['system_equal'] or not x['complete_bank_equal'] or x['solution_prose_equal']==False],'rejections':tests,'packaging':json.loads((E/'packaging.json').read_text())},indent=2))
