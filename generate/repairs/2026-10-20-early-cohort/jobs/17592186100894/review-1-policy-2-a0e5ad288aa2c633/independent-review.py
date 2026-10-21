from auditlib import *
import collections, shutil

def require(v,msg):
 if not v: raise AssertionError(msg)

source=json.load(open(JOB/'source/source.json'))
orig={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
replays=[]; replay_results=[]
for i,(mid,q) in enumerate(orig.items()):
 if mid=='q-104058': continue
 r=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],seed=492731+i,template=mid,replay=True)
 replays.append(r); sf=q[':question/answer-fields'][0]
 replay_results.append({'template':mid,'source_id':q[':question/id'],'bank_equal':collections.Counter(g.normalize_tex(a[':answer/value']) for a in sf[':answer-field/choices'])==collections.Counter(a[':answer/value'] for a in field(r)[':answer-field/choices']),'key_equal':correct(r)==g.normalize_tex(sf[':answer-field/correct'][':answer/value']),'prompt_equal':r['question'][':question/problem']==g.normalize_prose(q[':question/problem']),'solution_equal':r['question'][':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])})
save('source-replay-records.json',replays)
save('source-replay.json',{'results':replay_results,'excluded':{'q-104058':'At (1,1), coefficient of derivative is zero but RHS is 2; valid documented exclusion.'},'canonical':'Read canonical worked solution as instructional evidence; no captured field or complete bank. No independent replay family asserted.','corrections':g.REPAIRS,'new_corrections':'q-126765 equation restored from worked solution, nonconstant local sine branch specified; q-128199 replaces unavailable part 6 reference. Verified against source.'})
require(all(v['bank_equal'] and v['key_equal'] for v in replay_results),'source bank/key mismatch')

# Fresh seed, exact prior counterexample, constant/coefficient boundaries, signed branches.
trig=[g.generate('easy',847003,'q-104065',{'h':1})]
trig += [g.generate('easy',492793+i*5+j,'q-104065',{'h':[-4,1,4][i],'a':a,'c':c}) for i,a in enumerate((2,4,6)) for j,c in enumerate(('-pi^2','-1','0','1','pi^2'))]
rad=[g.generate('moderate',493011+i,'q-128199',{'h':1,'b':b}) for i,b in enumerate((-2,-1,1,2))]
native=[g.generate(g.level(m),493099+i,m,{'h':h}) for i,m in enumerate(('q-355559','q-355577','q-355582','q-350957')) for h in (-4,4)]
reg=[g.generate(g.level(m),493300+i,m,{'h':h}) for i,(m,h) in enumerate([('q-355560',-4),('q-104064',4),('q-104056',1)])]
cf=[g.generate('easy',493451,'q-104065',{'h':1,'a':4,'c':c}) for c in ('0','1')]
cf += [g.generate('easy',493451,'q-104065',{'h':1,'a':6,'c':'0'})]
irrelevant=copy.deepcopy(cf[0]); irrelevant['question'][':question/problem']=irrelevant['question'][':question/problem'].replace('Find','Determine');field(irrelevant)[':answer-field/choices'].reverse()
cf.append(irrelevant)
samples=trig+rad+native+reg
batch=json.load(open(E/'batch.json'))
save('samples.json',samples);save('counterfactual-records.json',cf)
checks=[]
for r in samples+cf+batch:
 try: result=math_check(r)
 except Exception as exc: result={'template':r['generation']['template'],'parameters':r['generation']['parameters'],'error':repr(exc)}
 checks.append(result)
save('math-results.json',checks)
print('Math:',len(checks),'failures:',[(c['template'],c.get('error',c.get('IC'))) for c in checks if not c.get('passed') or c.get('valid_choice_count')!=1],flush=True)

# The sine profile is a general solution fragment, not an IVP.
sines=[g.generate('easy',493501+i,'q-126765',{'h':h}) for i,h in enumerate((-4,1))]
sine_checks=[]
for r in sines:
 h=r['generation']['parameters']['h']; v=expr(correct(r)); C=S.Symbol('C',real=True)
 p=r['question'][':question/problem']; sol=r['question'][':question/worked-solution']
 sine_checks.append({'parameters':r['generation']['parameters'],'fragment':str(v),'expected_fragment':str((x-h)**2),'fragment_correct':simplify(v-(x-h)**2)==0,'local_branch_derivative':str(simplify(S.diff(S.sin(v+C),x)-2*(x-h)*S.cos(v+C))),'prompt':p,'solution':sol})
save('sine-records.json',sines);save('sine-checks.json',sine_checks)

# Strict native grader in ONE invocation: retained failure checks plus new cases and cross-keys.
cases=json.load(open(E/'retained-grader-input.json'))
for n,r in enumerate(samples+cf+batch+sines):
 f=field(r); checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
 else:
  v=correct(r); alt=str(expr(v)).replace('**','^').replace('log(','ln(').replace('E','e')
  checks=[{'submitted':v,'expected':'accepted'},{'submitted':alt,'expected':'accepted','purpose':'Equivalent plain algebra'},{'submitted':'0','expected':'rejected'},{'submitted':'('+v+')+1','expected':'rejected'}]
  if r['generation']['template']=='q-128199': checks.append({'submitted':'-('+v+')','expected':'rejected','purpose':'Opposite branch'})
 # Cross answer matching by exact expression when present; otherwise fixture adds wrong choice to test native grading.
 cases.append({'label':'fresh '+str(n)+' '+r['generation']['template']+' '+str(r['generation']['parameters']),'record':r,'checks':checks})
for i,j in [(0,1),(1,0),(0,2),(2,0)]:
 r=copy.deepcopy(cf[i]); f=field(r); a=copy.deepcopy(field(cf[j])[':answer-field/choices'][next(k for k,v in enumerate(field(cf[j])[':answer-field/choices']) if v[':answer/id']==field(cf[j])[':answer-field/correct'][1])]); a[':answer/id']=str(__import__('uuid').uuid5(__import__('uuid').NAMESPACE_DNS,'review-cross-'+str(i)+str(j)));f[':answer-field/choices'].append(a)
 cases.append({'label':'counterfactual cross '+str(i)+str(j),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'rejected','purpose':'Relevant ODE/IC change requires different response'}]})
save('grader-input.json',cases)
p=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')],capture_output=True,text=True)
(E/'grader-console.txt').write_text(p.stdout+p.stderr)
save('grader-execution.json',{'exit':p.returncode,'cases':len(cases),'checks':sum(len(c['checks']) for c in cases),'command':[str(ROOT/'generate/runs/current/check-engine'),'grader-input.json','grader-report.json']})
print('Grader:',p.returncode,p.stdout[-500:],p.stderr[-500:],flush=True)

# Native input formatting cannot replace real package runtime checks.
runtime=[]
for label,kw in [('bad shift',{'parameters':{'h':5}}),('boolean shift',{'parameters':{'h':True}}),('bad trig coefficient',{'template':'q-104065','parameters':{'h':1,'a':0,'c':'0'}}),('bad radical branch',{'difficulty':'moderate','template':'q-128199','parameters':{'h':1,'b':0}}),('unknown parameter',{'parameters':{'h':1,'bogus':2}}),('hard',{'difficulty':'hard'})]:
 try:g.generate(**kw); runtime.append({'label':label,'rejected':False})
 except Exception as exc:runtime.append({'label':label,'rejected':True,'message':str(exc)})
save('runtime-results.json',{'rejections':runtime,'deterministic':trig[0]==g.generate('easy',847003,'q-104065',{'h':1}),'python':platform.python_version(),'sympy':S.__version__})
save('render-records.json',batch+cf+rad[:1]+sines+[native[0]])
(E/'session-state.md').write_text('Source replay milestone: 25 complete banks/keys matched; documented invalid IVP excluded. Fresh targeted records, exact batch and counterfactuals saved. Math and strict native results saved; see console for failures. Delivery/render/package checks pending.\n')
