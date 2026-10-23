"""Independent read-only generator audit. Run with the job's Python interpreter."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys, json, re, importlib.util, pathlib, hashlib, collections, subprocess
sys.dont_write_bytecode=True
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name,value):
 (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
spec=importlib.util.spec_from_file_location('reviewed_generator',JOB/'workspace/17592186229165.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
x=S.Symbol('x',real=True)
def texparse(t):
 t=t.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\alpha','a').replace(r'\beta','b')
 def group(pos):
  assert t[pos]=='{',t[pos:]
  depth=1;end=pos+1
  while depth:
   depth+=(t[end]=='{')-(t[end]=='}');end+=1
  return t[pos+1:end-1],end
 while r'\frac' in t:
  p=t.index(r'\frac');a,e=group(p+5);b,e2=group(e)
  t=t[:p]+'(('+str(texparse(a))+')/('+str(texparse(b))+'))'+t[e2:]
 t=t.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(t,local_dict={'x':x,'e':S.E,'a':S.Symbol('a'),'b':S.Symbol('b')},transformations=standard_transformations+(implicit_multiplication_application,))
def answers(r):return [a[':answer/value'] for a in r['question'][':question/answer-fields'][0].get(':answer-field/choices',[])]
def params_from_prompt(r):
 text=r['question'][':question/problem']
 eq=text.split('$$')[1].split(r',\,')[0]
 lhs,rhs=eq.split('=');coeff=lhs.split('′}')[1].replace('y','');hc=texparse(coeff+'1' if coeff in ['+','-'] else coeff)
 v=int(re.search(r'y\(0\)=(-?\d+)',text)[1])
 return -hc,texparse(rhs),v
def checkmath(r):
 h,forcing,v=params_from_prompt(r)
 rows=[]
 for ans in answers(r):
  y=texparse(ans)
  rows.append({'answer':ans,'ode_residual':str(S.simplify(S.diff(y,x)-h*y-forcing)),'initial_residual':str(S.simplify(y.subs(x,0)-v))})
 # Last displayed solution must independently match the answer bank.
 last=re.findall(r'\$\$\s*(.*?)\s*\$\$',r['question'][':question/worked-solution'],re.S)[-1]
 ylast=texparse(last.split('=',1)[1]);final_ok=all(S.simplify(ylast-texparse(a))==0 for a in answers(r))
 return {'id':r['question'][':question/id'],'parameters_from_prompt':{'h':str(h),'forcing':str(forcing),'v':v},'answers':rows,'final_solution_matches':final_ok,'passed':final_ok and all(z['ode_residual']=='0' and z['initial_residual']=='0' for z in rows)}

source=load(JOB/'source/source.json')['material']['kp']
# Independent parameter table reconstructed from supplied question statements.
table=[(6,2,8,1),(3,3,9,2),(5,2,6,4),(4,-1,5,-1),(3,-2,7,0),(1,4,2,10),(-2,-3,-5,8),(-2,-2,8,-1),(4,4,-2,1),(5,5,15,1),(2,2,-10,0),(-3,-3,12,1),(3,1,8,1),(1,1,7,4),(5,5,4,-1)]
replays=[];replay_results=[]
for q,vals in zip(source[':knowledge-point/questions'],table):
 p=dict(zip(('h','k','f','v'),vals));level='easy' if p['h']!=p['k'] else 'moderate';name=q[':question/math-academy-id']
 r=G.generate(level,seed=941,parameters=p,profile='raw:'+name);replays.append(r)
 old=[a[':answer/value'] for a in q[':question/answer-fields'][0].get(':answer-field/choices',[])]
 replay_results.append({'source_id':q[':question/id'],'profile':name,'parameters':p,'prompt_equal':q[':question/problem']==r['question'][':question/problem'],'solution_equal':q.get(':question/worked-solution')==r['question'].get(':question/worked-solution'),'complete_bank_equal':sorted(old)==sorted(answers(r)),'designation_equal':not old or q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']==answers(r)[-1],'original_bank':old,'generated_bank':answers(r)})
save('source-replays.json',replays);save('source-replay-results.json',replay_results)
batch=load(JOB/'samples.json');save('runner-batch.json',batch)
sample=[]
for level in ['easy','moderate','hard']:
 for seed in range(230021,230025):sample.append(G.generate(level,seed=seed))
save('independent-samples.json',sample)
# Controlled relevant changes: initial coefficient cancellation, forcing coefficient, exponent.
base=dict(h=2,k=3,f=4,v=1)
pair_specs=[('base','easy',base,None),('initial-cancels','easy',dict(base,v=4),None),('forcing-sign','easy',dict(base,f=-4),None),('exponent-change','easy',dict(base,k=1),None),('irrelevant-profile','easy',base,'q-332906'),('irrelevant-seed','easy',base,None),('resonance','moderate',dict(base,k=2),None)]
pairs=[G.generate(level,seed=771 if name=='irrelevant-seed' else 770,parameters=p,profile=profile) for name,level,p,profile in pair_specs]
save('counterfactual-records.json',pairs)
boundaries=[G.generate('easy',parameters=dict(h=-6,k=6,f=-15,v=10)),G.generate('easy',parameters=dict(h=6,k=-6,f=15,v=-10)),G.generate('moderate',parameters=dict(h=-6,k=-6,f=15,v=0))]
save('boundary-records.json',boundaries)
math_records=batch+sample+pairs+boundaries+[r for r in replays if answers(r)]
math_result=[checkmath(r) for r in math_records]
save('math-results.json',math_result)
assert all(z['passed'] for z in math_result)
assert all(all(z[k] for k in ['prompt_equal','solution_equal','complete_bank_equal','designation_equal']) for z in replay_results)

def expected_tex(r):
 p=r['generation']['parameters'];h=p['h'];v=p['v'];parts=[(p['k'],p['f'])]+([(p['k2'],p['f2'])] if 'k2' in p else [])
 c=[S.Rational(f,k-h) if k!=h else S.Integer(f) for k,f in parts];a=v-sum(z for (k,f),z in zip(parts,c) if k!=h)
 y=a*S.exp(h*x)+sum(z*(x if k==h else 1)*S.exp(k*x) for (k,f),z in zip(parts,c))
 return y
grading=[]
for i,r in enumerate(batch+pairs+boundaries+sample[::8]+[z for z in replays if answers(z)]):
 y=expected_tex(r)
 equivalent=S.latex(S.factor(y))
 checks=[{'submitted':equivalent,'expected':'accepted','purpose':'Independent symbolic solution, refactored where possible'}, {'submitted':S.latex(y+S.exp(r['generation']['parameters']['h']*x)),'expected':'rejected','purpose':'Correct ODE but incorrect initial value'}, {'submitted':'0','expected':'rejected','purpose':'Ignore nonzero forcing'}, {'submitted':S.latex(y+1),'expected':'rejected','purpose':'Add erroneous constant'}]
 if r in pairs:
  checks.append({'submitted':S.latex(expected_tex(pairs[0])),'expected':'accepted' if S.simplify(y-expected_tex(pairs[0]))==0 else 'rejected','purpose':'Controlled pair: original answer must track relevant evidence and ignore profile/seed'})
 grading.append({'label':f'independent-{i}','record':r,'checks':checks})
save('grader-input.json',grading)
save('render-records.json',batch+pairs+[sample[8],sample[8],sample[9]])
# Runtime and input-boundary packaging tests.
guards=[]
bad=[dict(h=2,k=2,f=4,v=1),dict(h=0,k=3,f=4,v=1),dict(h=2,k=3,f=0,v=1),dict(h=2,k=3,f=16,v=1),dict(h=2,k=3,f=4,v=11),dict(h=2,k=3,f=True,v=1)]
for p in bad:
 try:G.generate('easy',parameters=p);guards.append({'parameters':p,'rejected':False})
 except ValueError as e:guards.append({'parameters':p,'rejected':True,'error':str(e)})
deterministic=all(G.generate('easy',seed=z)==G.generate('easy',seed=z) for z in [0,67031,-1,2**63])
save('runtime-results.json',{'python':sys.version.split()[0],'packages':{'sympy':S.__version__},'manifest_dependencies':load(JOB/'workspace/package.json')['dependencies'],'deterministic_replay':deterministic,'guards':guards,'resampling':'No loop or rejection after random sampling. sample() draws directly from valid per-template bounds; explicit inputs pass param_guard before construction.','command':str(sys.executable)+' '+str(ROOT/'audit.py')})
print(json.dumps({'source_cases':len(replays),'source_failures':[z for z in replay_results if not all(z[k] for k in ['prompt_equal','solution_equal','complete_bank_equal','designation_equal'])],'math_cases':len(math_result),'grader_records':len(grading),'sample_count':len(sample),'guards_passed':all(z['rejected'] for z in guards)},indent=2))
