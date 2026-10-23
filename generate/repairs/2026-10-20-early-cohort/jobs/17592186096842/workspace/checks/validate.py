from audit_helpers import *
OUT=PKG/'evidence'
def write(n,d): (OUT/n).write_text(json.dumps(d,indent=2,default=str))
def eq(a,b):return s.simplify(s.powdenest(a,force=True)-s.powdenest(b,force=True))==0
replays=g.replay_sources();write('source-replays.json',replays)
source=json.load(open(PKG.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in source}
replay_results=[]
for r in replays:
 q=byid[r['generation']['replay_source_id']];f=q[':question/answer-fields'][0]
 radio=f[':answer-field/type'][':db/ident'].endswith('/radio')
 before=[a[':answer/value'] for a in f[':answer-field/choices']];after=[a[':answer/value'] for a in field(r)[':answer-field/choices']]
 ok=not radio or len(before)==len(after) and all(sum(eq(latex(a),latex(b)) for b in after)==1 for a in before)
 assert ok,(q[':question/id'],before,after)
 replay_results.append({'source_id':q[':question/id'],'complete_bank_match':ok,'choices':len(before) if radio else None,'capture_matches_current_source':r['generation']['source_capture'][':question/answer-fields']==q[':question/answer-fields']})
write('source-replay-results.json',replay_results)
cf=[]
# Same function, three eligible targets, positive/zero/negative derivative.
for t in [1,5,9]:cf.append(g.generate('easy',999,'slope_sqrt_quadratic_blank',parameters={'a':-1,'b':10,'c':0,'t':t}))
assert [expected(r) for r in cf]==[s.Rational(4,3),0,-s.Rational(4,3)]
# Same linear function; relevant target changes 4/3 to 4/5.
for t in [0,2]:cf.append(g.generate('easy',999,'slope_sqrt_radio',parameters={'a':8,'b':9,'t':t}))
assert [expected(r) for r in cf[3:]]==[s.Rational(4,3),s.Rational(4,5)]
# Different banks and positions must preserve function, answer and solution.
for seed in [610,611]:cf.append(g.generate('easy',seed,'slope_sqrt_radio',parameters={'a':4,'b':9,'t':0}))
assert correct(cf[-1])==correct(cf[-2])
assert cf[-1]['question'][':question/worked-solution']==cf[-2]['question'][':question/worked-solution']
assert field(cf[-1])[':answer-field/choices']!=field(cf[-2])[':answer-field/choices']
write('counterfactual-records.json',cf)
canonical=g.generate('hard',990,'sqrt_quadratic_blank',parameters={'a':-1,'b':0,'c':1})
write('canonical-record.json',[canonical])
samples=json.load(open(OUT/'radio-sample.json'))
# All generated radio banks are independently checked; no stale expected fixtures.
records=replays+samples+json.load(open(OUT/'prospective-batch.json'))+cf+[canonical]
results=[];cases=[]
for n,r in enumerate(records):
 ans=expected(r);f=field(r);choices=f[':answer-field/choices'];v=latex(correct(r))
 assert eq(v,ans),(r['question'][':question/id'],str(ans),str(v))
 assert sum(eq(latex(a[':answer/value']),ans) for a in choices)==1
 checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if eq(latex(a[':answer/value']),ans) else 'rejected'} for a in choices]
 else:
  checks=[{'submitted':str(ans).replace('**','^'),'expected':'accepted'}, {'submitted':s.latex(ans),'expected':'accepted'}, {'submitted':str(ans+1).replace('**','^'),'expected':'rejected'}]
 cases.append({'label':str(n)+'-'+r['generation']['template'],'record':r,'checks':checks})
 results.append({'id':r['question'][':question/id'],'independent_answer':str(ans),'correct_count':1})
write('math-results.json',results);write('grader-input.json',cases)
# Replay from declared files alone after relocation, and compare deterministic CLI.
manifest=json.load(open(PKG/'package.json'));rel=OUT/'relocated-package';rel.mkdir(exist_ok=True)
for name in manifest['files']:
 dest=rel/name;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(PKG/name,dest)
cmd=[sys.executable,'-B',str(rel/'generator.py'),'--difficulty','easy','--seed','3173462200','--count','5','--format','json']
run=subprocess.run(cmd,check=True,text=True,capture_output=True,cwd=OUT,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'assets')})
assert json.loads(run.stdout)==json.load(open(OUT/'prospective-batch.json'))
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':s.__version__}}
write('validation-results.json',{'source_replays':len(replays),'radio_source_banks':sum(x['choices'] is not None for x in replay_results),'math_records':len(records),'grader_checks':sum(len(c['checks']) for c in cases),'counterfactuals':'target changes and irrelevant bank changes verified','relocation_and_determinism':True,'dependencies':manifest['dependencies'],'max_parameter_attempts':max(r['generation']['attempts'] for r in samples),'source_capture_note':'q-342787 capture predates an additional historical blank submission; complete current source is retained outside runtime; canonical answer unchanged.'})
# Exact witness and a reciprocal symbolic radio exercise the changed choices.
render=[json.load(open(OUT/'exact-counterexample-current.json'))[0], next(r for r in samples if r['generation']['template']=='reciprocal_radio'),next(r for r in samples if r['generation']['template']=='slope_sum_radio')]
write('render-records.json',render)
print(json.dumps({'source_replays':len(replays),'math_records':len(records),'grader_checks':sum(len(c['checks']) for c in cases),'relocation':True}))
