import sys
sys.dont_write_bytecode=True
import json,pathlib,importlib.util,re,collections,hashlib,shutil,subprocess,platform
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def write(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def loadmod(path):
 spec=importlib.util.spec_from_file_location('review_generator',path); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod); return mod
manifest=json.load(open(PKG/'package.json'))
hashes={x:hashlib.sha256((PKG/x).read_bytes()).hexdigest() for x in ['package.json']+manifest['files']};write('package-before.json',hashes)
m=loadmod(PKG/manifest['entrypoint']);source=json.load(open(JOB/'source/source.json')); inv=json.load(open(JOB/'source/inventory.json'));batch=json.load(open(JOB/'samples.json'));write('batch.json',batch)
t=sp.Symbol('t',real=True)
def key(q):
 v=q[':question/answer-fields'][0].get(':answer-field/correct')
 return v.get(':answer/id') if isinstance(v,dict) else (v[1] if v else None)
def pars(q):
 text=q[':question/problem']; ns=[sp.Rational(x) for x in re.findall(r'\$([0-9]+(?:\.[0-9]+)?)',text)]
 V,q0,c,r,rout=ns[:5]; assert r==rout
 if r'\text{g/L}' in text:c/=1000
 return V,q0,c,r,ns[5] if len(ns)>5 else None
EX=re.compile(r'Q\(t\)=([+-]?\d+(?:\.\d+)?)([+-])(\d+(?:\.\d+)?)?(?:\{e\}|e)\^\{(-?)t/([0-9.]+)\}')
def ex(value):
 a=EX.fullmatch(value)
 if not a:raise ValueError('unsupported independently parsed expression '+value)
 E,sgn,A,neg,tau=a.groups();E=sp.Rational(E); A=sp.Rational(A or 1)*(1 if sgn=='+' else -1); rate=sp.Rational(1)/sp.Rational(tau)*(1 if neg else -1)
 return E,A,rate

def shortcut(q):
 # Uses only the visible choice bank. Does not inspect prompt, solution, key or metadata.
 opts=q[':question/answer-fields'][0][':answer-field/choices']; triples=[ex(x[':answer/value']) for x in opts]
 leading=collections.Counter(x[0] for x in triples);initials=collections.Counter(x[0]+x[1] for x in triples)
 dup=[e for e,n in leading.items() if n==2];modal=[v for v,n in initials.items() if n==4]
 if len(dup)!=1 or len(modal)!=1:return None
 picks=[o[':answer/id'] for o,(e,a,k) in zip(opts,triples) if e==dup[0] and e+a==modal[0]]
 return picks[0] if len(picks)==1 else None

samples=[]
for level,count in [('easy',60),('moderate',12),('hard',3)]:
 for seed in range(81031,81031+count):samples.append(m.generate(level,seed))
write('samples.json',samples);write('easy-samples.json',samples[:60])
# Controlled pairs: change answer-bearing initial mass and rate, then irrelevant nouns.
base={'V':500,'r':25,'c':'0.02','q0':7,'context':'coolant'}
pairs=[('base',base),('initial_mass',dict(base,q0=13)),('flow',dict(base,r=20)),('context',dict(base,context='dye'))]
cf=[m.generate('easy',99173,parameters=p) for label,p in pairs];write('counterfactual-records.json',cf)
write('counterfactual-inputs.json',{'command':f'{sys.executable} {ROOT}/review_checks.py','seed':99173,'cases':dict(pairs),'expected':{'base':'10-3 exp(-t/20)','initial_mass':'10+3 exp(-t/20)','flow':'10-3 exp(-t/25)','context':'10-3 exp(-t/20)'}})
mathres=[];grading=[]
for group,records in [('sample',samples),('batch',batch),('counterfactual',cf)]:
 for i,rec in enumerate(records):
  q=rec['question'];V,q0,c,r,time=pars(q); E=V*c;k=r/V; expected=E+(q0-E)*sp.exp(-k*t);opts=q[':question/answer-fields'][0][':answer-field/choices'];truth=[]
  for o in opts:
   if time is None:
    e,a,rate=ex(o[':answer/value']);f=e+a*sp.exp(-rate*t)
    good=sp.simplify(sp.diff(f,t)-(r*c-r*f/V))==0 and f.subs(t,0)==q0
   else:
    n=sp.Rational(re.match(r'([0-9.]+)',o[':answer/value'])[1]); good=abs(float(n)-float(expected.subs(t,time)))<.005
   if good:truth.append(o[':answer/id'])
  # Parse the final function printed in worked solution, rather than trusting generation parameters.
  sol=q[':question/worked-solution']; matches=EX.findall(sol)
  final=EX.search(sol[sol.rfind('Therefore, we obtain'):]) if 'Therefore, we obtain' in sol else None
  eqs=list(EX.finditer(sol)); solgood=False
  if eqs:
   se,sa,sk=ex(eqs[-1][0]);solgood=sp.simplify(se+sa*sp.exp(-sk*t)-expected)==0
  passed=truth==[key(q)] and solgood
  mathres.append({'group':group,'index':i,'seed':rec['generation']['seed'],'id':q[':question/id'],'parameters_from_prompt':[str(x) if x is not None else None for x in (V,q0,c,r,time)],'unique_correct':truth==[key(q)],'solution_final_matches':solgood,'passed':passed})
  checks=[{'field_index':0,'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/id'] in truth else 'rejected','purpose':'independent ODE/initial-value or numerical oracle, all five radio choices'} for o in opts]
  if time is None:
   pick=shortcut(q)
   if pick:checks.append({'field_index':0,'submitted_answer_id':pick,'expected':'accepted','purpose':'bank-only repeated constant plus modal initial-value shortcut; no prompt used'})
  grading.append({'label':f'{group}-{i}','record':rec,'checks':checks})
write('math-results.json',{'cases':mathres,'passed':all(x['passed'] for x in mathres)})
write('grader-input.json',grading)
# Replay every captured source question, including the missing profiles and current changed attributes.
replays=[];source_results=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 sid=str(q[':db/id']);level='moderate' if 'rounded' in q[':question/problem'] else 'easy'
 try:
  rec=m.generate(level,61829,template='source_'+sid);replays.append(rec);rq=rec['question']
  norm=lambda x:re.sub(r'\s+','',x).replace('{e}','e')
  bank=lambda x:sorted(norm(a[':answer/value']) for a in x[':question/answer-fields'][0][':answer-field/choices'])
  fields=[':question/worked-solution',':question/difficulty']
  differences=[f for f in fields if rq.get(f)!=q.get(f) and not (f==':question/difficulty' and rq.get(f)==q.get(f,{}).get(':db/ident'))]
  if bank(rq)!=bank(q):differences.append('complete bank')
  if bool(key(rq))!=bool(key(q)):differences.append('correct-link presence')
  source_results.append({'source_id':q[':question/id'],'entity_id':sid,'level':level,'replay_id':rq[':question/id'],'differences':differences,'prompt_bytes_match':rq[':question/problem']==q[':question/problem'],'passed':not differences})
 except ValueError as e:source_results.append({'source_id':q[':question/id'],'entity_id':sid,'level':level,'error':str(e),'passed':False})
write('source-replay-records.json',replays);write('source-replay.json',{'cases':source_results,'canonical':'No canonical bank captured; canonical math independently derived in source-analysis.json.','passed':all(x['passed'] for x in source_results)})
# Source-independent shortcut measurements, separated by signs, contextual subgroup and delivered batch.
def measure(records,label):
 qs=[r['question'] for r in records];picks=[shortcut(q) for q in qs]
 return {'label':label,'correct':sum(p==key(q) for p,q in zip(picks,qs)),'total':len(qs),'abstained':picks.count(None),'baseline':.2,'ids':[q[':question/id'] for q in qs]}
easy=samples[:60]; probe=[measure(easy,'raw easy'),measure(batch,'exact runner batch')]
for sign in ['increasing','decreasing']:
 rs=[r for r in easy if (pars(r['question'])[1]<pars(r['question'])[0]*pars(r['question'])[2])==(sign=='increasing')];probe.append(measure(rs,sign))
for context in sorted(set(r['generation']['parameters']['context'] for r in easy)):
 probe.append(measure([r for r in easy if r['generation']['parameters']['context']==context],context))
write('shortcut-results.json',{'strategy':'Ignore question. Find the sole leading constant occurring in two choices. Compute constant plus signed exponential coefficient at t=0 for each choice; find the value occurring four times. Choose the member of the repeated-constant pair whose value equals that mode.','probes':probe})
# Parameter rejection and deterministic replay, runtime contract and relocation.
rejections=[]
for label,params in [('zero flow',dict(base,r=0)),('zero volume',dict(base,V=0)),('invalid context',dict(base,context='alien')),('equilibrium',dict(base,q0=10)),('zero concentration',dict(base,c=0)),('outside source arithmetic',dict(base,V=299))]:
 try:m.generate('easy',99173,parameters=params);ok=False;err='accepted'
 except (ValueError,ZeroDivisionError) as e:ok=True;err=str(e)
 rejections.append({'case':label,'parameters':params,'rejected':ok,'error':err})
rel=ROOT/'relocated';rel.mkdir(exist_ok=True);shutil.copy2(PKG/manifest['entrypoint'],rel/manifest['entrypoint']);(rel/'17592186229181').mkdir(exist_ok=True);shutil.copy2(PKG/'17592186229181/masks.json',rel/'17592186229181/masks.json')
relmod=loadmod(rel/manifest['entrypoint']); relocation=relmod.generate('easy',81031)==easy[0]
write('packaging.json',{'actual_versions':{'python':platform.python_version(),'packages':{'sympy':sp.__version__}},'declared_dependencies':manifest['dependencies'],'versions_match':manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':sp.__version__}},'deterministic':m.generate('easy',81031)==easy[0],'relocated_with_runtime_files':relocation,'runtime_files':['17592186229181.py','17592186229181/masks.json'],'rejections':rejections,'external_outputs':'Generator returns records/stdout only; no plotting or asset subprocess code.','repair_history_exists':(JOB/'repair-history.json').exists(),'repair_preflight_exists':(JOB/'repair-preflight.json').exists()})
# Inventory applicability: inspect all captured records, retain source vs generated distinction.
invres=[];affected=[];reproduced=[]
for q in inv['questions']:
 gid=q.get(':question/generation'); info={'id':q[':question/id'],'entity_id':q[':db/id'],'is_captured_source':any(s[':question/id']==q[':question/id'] for s in source['material']['kp'][':knowledge-point/questions']),'keys':list(q),'generation':gid}
 if 'Which expression' in q[':question/problem']:
  try:pick=shortcut(q);info['bank_shortcut_matches']=pick is not None and pick==key(q)
  except ValueError as e:info['error']=str(e)
 invres.append(info)
write('inventory-audit.json',{'basis':inv['basis'],'cases':invres,'conclusion':'All captured expression banks are original source, not method_bank generated instances; no already-stored instance of the demonstrated easy method_bank shortcut established. Numeric generated entries do not have this expression-bank cue.','limitations':'This conclusion applies to this precise cue and captured basis; no live database inspected.'});write('affected-inventory.json',{'affected_questions':affected})
# Render entire runner batch and controlled pairs; include sampled positive and negative branches and numeric level.
render=batch+cf+[next(r for r in easy if pars(r['question'])[1]>pars(r['question'])[0]*pars(r['question'])[2]),samples[60],samples[-1]]
write('render-input.json',render)
(ROOT/'session-state.md').write_text('Independent source analysis saved before author inspection. Completed sample math, full source replay, bank-only shortcut, runtime/rejection/relocation and captured inventory tests. See review_checks.py and JSON evidence. Pending shared delivery, native grader and actual UI render.\n')
print(json.dumps({'math_pass':all(x['passed'] for x in mathres),'math_cases':len(mathres),'math_failures':[x for x in mathres if not x['passed']][:2],'source_replay_failures':[x for x in source_results if not x['passed']],'shortcut':probe,'packaging_relocation':relocation},indent=2))
