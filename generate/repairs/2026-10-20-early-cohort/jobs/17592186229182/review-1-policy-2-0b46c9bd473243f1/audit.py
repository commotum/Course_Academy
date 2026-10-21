import os,sys,json,pathlib,importlib.util,hashlib,subprocess,shutil,re,collections
sys.dont_write_bytecode=True
ROOT=pathlib.Path('/home/jake/Developer/Course_Academy')
JOB=ROOT/'generate/repairs/2026-10-20-early-cohort/jobs/17592186229182'
PKG=JOB/'workspace'; OUT=pathlib.Path(__file__).resolve().parent
def save(n,x): (OUT/n).write_text(json.dumps(x,indent=2,default=str))
spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186229182.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as s
def digest_package():
 return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PKG.rglob('*')) if p.is_file()}
save('package-before.json',digest_package())
source=json.load(open(JOB/'source/source.json'))['material']['kp']
batch=json.load(open(JOB/'samples.json'));save('batch.json',batch)
records=[g.generate('easy',seed) for seed in range(92031,92071)]
records += [g.generate(level,seed,template=m['source_id']) for level in ['moderate','hard'] for m in g.M.values() if m['level']==level for seed in [2203,5783]]
save('samples.json',records)
def correct(r):
 f=r['question'][':question/answer-fields'][0]
 key=f.get(':answer-field/correct',[None,None])[1]
 return next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key),None)
def math_check(r):
 # Independently parse physical givens from learner-facing prompt, not metadata.
 p=r['question'][':question/problem'];nums=re.findall(r'\$([^$]+)\$',p)
 vals=[]
 for x in nums[:5]:
  vals.append(s.Rational(re.match(r'[\d.]+',x)[0]))
 V,q,c,ri,ro=vals; t=s.Symbol('t'); delta=ri-ro
 Q=c*(V+delta*t)+(q-c*V)*(V/(V+delta*t))**(ro/delta)
 residual=s.simplify(s.diff(Q,t)-(c*ri-ro*Q/(V+delta*t)))
 assert residual==0 and s.simplify(Q.subs(t,0)-q)==0
 if 'α + β' in p or '\\alpha + \\beta' in p: answer=q
 elif '\\alpha -' in p: answer=2*c*V-q
 else:
  T=s.Rational(re.search(r'\$(\d+)\$ minutes after pumping',p).group(0).split('$')[1])
  from decimal import Decimal,ROUND_HALF_UP
  answer=Decimal(str(s.N(Q.subs(t,T),40))).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
 got=correct(r); actual=s.Rational(got.split('\\,')[0])
 return {'id':r['question'][':question/id'],'seed':r['generation']['seed'],'expected':str(answer),'actual':str(actual),'passed':actual==s.Rational(str(answer)),'ode_residual':str(residual)}
math=[]
for r in records+batch:
 try: math.append(math_check(r))
 except Exception as e: math.append({'id':r['question'][':question/id'],'error':repr(e)})
save('math.json',math)
replays=[];replay_checks=[]
for q in source[':knowledge-point/questions']:
 ma=q[':question/math-academy-id']; item={'source_id':q[':question/id'],'template':ma}
 if ma not in g.M: item.update(passed=False,error='No source template/profile in executable generator')
 else:
  m=g.M[ma];r=g.generate(m['level'],1943,template=ma,parameters=m['parameters'],profile='observed:'+ma);replays.append(r)
  rq=r['question'];f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
  def norm(x):return re.sub(r'\s+','',x).replace('\\\\','\\')
  sb=sorted(norm(a[':answer/value']) for a in f[':answer-field/choices']);rb=sorted(norm(a[':answer/value']) for a in rf[':answer-field/choices'])
  item.update(prompt_match=norm(q[':question/problem'])==norm(rq[':question/problem']),bank_match=sb==rb,source_bank=sb,replay_bank=rb,source_has_key=':answer-field/correct' in f,replay_has_key=':answer-field/correct' in rf,source_has_solution=':question/worked-solution' in q,replay_has_solution=':question/worked-solution' in rq,source_difficulty=q.get(':question/difficulty'),replay_difficulty=rq.get(':question/difficulty'))
  item['passed']=item['prompt_match'] and item['bank_match'] and item['source_has_key']==item['replay_has_key'] and item['source_has_solution']==item['replay_has_solution']
 replay_checks.append(item)
save('source-replays.json',replays);save('source-replay-results.json',replay_checks)
base={'V':640,'q0':17,'c':'0.05','rin':16,'rout':24}
pair=[g.generate('easy',619,parameters=p) for p in [base,dict(base,q0=18),dict(base,V=800)]]
save('counterfactual-records.json',pair)
save('counterfactual-results.json',{'base':correct(pair[0]),'relevant_q0_18':correct(pair[1]),'irrelevant_V_800':correct(pair[2]),'prompt_changes':[r['question'][':question/problem'] for r in pair],'solution_changes':[r['question'][':question/worked-solution'] for r in pair]})
rejections=[]
tests=[('positive transient source', 'moderate','q-336746',{'V':240,'q0':9,'c':'0.025','rin':16,'rout':24},None),('positive transient integer','easy','q-336439',{'V':240,'q0':15,'c':'0.05','rin':16,'rout':24},None),('zero transient','easy','q-336439',{'V':640,'q0':32,'c':'0.05','rin':16,'rout':24},None),('fractional source initial mass','hard','q-339400',{'V':320,'q0':'2.2','c':'0.05','rin':8,'rout':4,'T':5},None),('equal rates invalid','easy','q-336439',dict(base,rout=16),None),('negative volume invalid','easy','q-336439',dict(base,V=-640),None)]
for name,level,template,p,profile in tests:
 try:r=g.generate(level,619,template=template,parameters=p,profile=profile);result='accepted'
 except Exception as e:result=type(e).__name__+': '+str(e)
 rejections.append(dict(case=name,level=level,template=template,parameters=p,profile=profile,result=result))
save('rejection-tests.json',rejections)
cases=[]
for label,r in [(f'sample-{i}',r) for i,r in enumerate(records+batch+pair)]:
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 cases.append({'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'Independently verified correct value' if a[':answer/id']==key else 'Wrong operation distractor'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases)
def probes(rs):
 easy=[r for r in rs if r['question'].get(':question/difficulty')==':question.difficulty/easy'];ranks=[];pos=[]
 for r in easy:
  f=r['question'][':question/answer-fields'][0];v=[s.Rational(a[':answer/value']) for a in f[':answer-field/choices']];a=s.Rational(correct(r));ranks.append(sorted(v).index(a)+1);pos.append(v.index(a)+1)
 return {'n':len(easy),'rank_counts':dict(collections.Counter(ranks)),'position_counts':dict(collections.Counter(pos)),'answer_values':dict(collections.Counter(correct(r) for r in easy)),'always_smallest_correct':ranks.count(1),'always_second_smallest_correct':ranks.count(2),'bottom_two_correct':sum(x<=2 for x in ranks)}
save('coverage.json',{'sample':probes(records),'batch':probes(batch),'all_templates':dict(collections.Counter(r['generation']['template'] for r in records))})
save('render-records.json',batch[:2]+[records[40],records[44]]+pair)
runtime={'python':sys.version.split()[0],'sympy':s.__version__,'manifest':json.load(open(PKG/'package.json'))['dependencies'],'deterministic':records[0]==g.generate('easy',92031),'source_count':len(source[':knowledge-point/questions'])}
# Relocate a read-only snapshot into evidence; package paths are never altered.
rel=OUT/'relocated';shutil.copytree(PKG,rel,dirs_exist_ok=True)
cmd=[sys.executable,str(rel/'17592186229182.py'),'--difficulty','easy','--seed','92031','--format','json']
run=subprocess.run(cmd,cwd=OUT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
runtime.update(relocation_command=cmd,relocation_exit=run.returncode,relocation_match=run.returncode==0 and json.loads(run.stdout)[0]==records[0]);save('runtime.json',runtime)
save('package-after.json',digest_package())
assert digest_package()==json.load(open(OUT/'package-before.json'))
(OUT/'session-state.md').write_text('Independent sampling, math, source replay, explicit rejection cases, counterfactuals, native grader inputs, runtime and relocation checks completed. Pending delivery, native grader execution, renderer, inventory reproduction, final report. Package unchanged.\n')
print(json.dumps({'records':len(records),'math_failures':[x for x in math if not x.get('passed')],'source_failures':[x['template'] for x in replay_checks if not x['passed']],'runtime':runtime,'coverage':probes(records)},default=str))
