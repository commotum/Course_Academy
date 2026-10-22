"""Independent revision review. Run with the context Python from evidence_root.
No writes to the candidate package; inputs are frozen job captures.
"""
import sys
sys.dont_write_bytecode=True
import json,re,hashlib,importlib.util,copy,platform,shutil,subprocess,os,random
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parent;JOB=ROOT.parent;REPO=Path('/home/jake/Developer/Course_Academy');PKG=JOB/'workspace';PY=REPO/'.venv/bin/python'
def save(n,d):
 p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.load(open(p))
def module(p,name='candidate'):
 spec=importlib.util.spec_from_file_location(name,p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
g=module(PKG/'17592186119805.py')
def scalar(s):
 s=str(s).strip().replace('\\\\frac','\\frac').replace(' ','');m=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',s)
 return (-1 if m[1] else 1)*Fraction(int(m[2]),int(m[3])) if m else Fraction(s)
def value(v):return v if v=='No solution' else scalar(v)
def mats(s):return [[scalar(x) for x in re.split(r'\\\\',v)] for v in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def choices(q):return q[':question/answer-fields'][0][':answer-field/choices']
def key(q):
 f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a[':answer/value'] for a in choices(q) if a[':answer/id']==cid)
def solve(q):
 text=q[':question/problem'];a,u,*bs=mats(text);m=re.search(r'if \$(\d+)',text);c=int(m[1]) if m else 1
 sign=-1 if re.search(r'\{a\}_\{1\}-[a-z]',text) else 1;b=bs[0] if bs else [Fraction(0)]*len(a)
 residual=[sign*(x-c*y) for x,y in zip(b,a)];ratios={x/y for x,y in zip(residual,u) if y}
 ans=next(iter(ratios)) if len(ratios)==1 and all(y or x==0 for x,y in zip(residual,u)) else 'No solution'
 return ans,residual,(a,u,b,c,sign)
def verify(r):
 q=r['question'];ans,res,(a,u,b,c,sign)=solve(q);assert value(key(q))==ans,(q[':question/id'],key(q),str(ans))
 bank=[value(x[':answer/value']) for x in choices(q)];assert len(bank)==len(set(bank))==5 and bank.count(ans)==1
 assert q[':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'
 sm=mats(q[':question/worked-solution']);expected=[a,u,b,u,a,b,u,res] if sign==-1 else [a,u,b,u,b,a,u,res]
 if ans=='No solution':
  pivot=next(i for i,x in enumerate(u) if x);t=res[pivot]/u[pivot];expected += [u,[t*x for x in u],res]
  assert 'Therefore, there is no $' in q[':question/worked-solution']
 else:
  letter=re.search(r'Find \$([a-z])',q[':question/problem'])[1];m=re.search(re.escape('$'+letter+'=')+r'(.*?)\.\$',q[':question/worked-solution']);assert m and scalar(m[1])==ans
 assert sm==expected,(q[':question/id'],'solution matrices')
 return ans

def predict(q,strategy):
 nums=sorted(value(a[':answer/value']) for a in choices(q) if a[':answer/value']!='No solution');letter=re.search(r'Find \$([a-z])',q[':question/problem'])[1]
 if strategy=='old-label-bank':
  if '=0$' in q[':question/problem']:return 'No solution'
  if letter=='l' and len(nums)==4:return next((x for x in nums if x<0),None)
  if letter=='l':return nums[-2]
  if letter=='h':return nums[-1]
  if letter=='m':return nums[0]
  if letter=='k':return nums[1]
  if letter=='j':return next((x for x in nums if x>0),None)
  return None
 if strategy=='No solution':return 'No solution'
 if strategy.startswith('position-'):return value(choices(q)[int(strategy[-1])][':answer/value'])
 if strategy.startswith('rank-'):return nums[min(int(strategy[-1]),len(nums)-1)]
 if strategy=='negative-nearest-zero':return max((x for x in nums if x<0),default=None)
 if strategy=='closest-zero':return min(nums,key=lambda x:(abs(x),x))
 if strategy=='literal-minus-two':return Fraction(-2) if Fraction(-2) in nums else None
 raise ValueError(strategy)
STRATEGIES=['old-label-bank','No solution','negative-nearest-zero','closest-zero','literal-minus-two']+['position-'+str(i) for i in range(5)]+['rank-'+str(i) for i in range(5)]
def stats(records):
 groups={'overall':records}
 for r in records:
  q=r['question'];sid=r['generation']['bank_profile'];text=q[':question/problem'];label=re.search(r'Find \$([a-z])',text)[1]
  groups.setdefault('profile:'+sid,[]).append(r);groups.setdefault('label:'+label,[]).append(r)
  groups.setdefault('target:'+('zero' if '=0$' in text else 'explicit'),[]).append(r)
  groups.setdefault('bank:'+('with-No-solution' if len([a for a in choices(q) if a[':answer/value']=='No solution']) else 'numeric-only'),[]).append(r)
 out=[]
 for name,rs in groups.items():
  for strategy in STRATEGIES:
   out.append({'subgroup':name,'strategy':strategy,'correct':sum(predict(r['question'],strategy)==solve(r['question'])[0] for r in rs),'total':len(rs),'baseline':0.2,'ids':[r['question'][':question/id'] for r in rs]})
 return out

if __name__=='__main__':
 source=load(JOB/'source/source.json');seedlist=[730001+99991*i for i in range(16)];records=[]
 for level,sids in g.LEVELS.items():
  for sid in sids:
   for seed in seedlist:records.append(g.generate(level,seed,sid))
 batch=load(JOB/'samples.json');save('normal-records.json',records);save('runner-batch.json',batch)
 save('sampling-inputs.json',{'command':str(PY)+' revision-audit.py','seeds':seedlist,'per_profile':16,'profiles':g.LEVELS})
 # Full source replay, independent of package CASES and source-data.json.
 replay=[];replayed=[]
 for q in source['material']['kp'][':knowledge-point/questions']:
  sid=q[':question/math-academy-id']
  if not q.get(':question/difficulty'):
   replay.append({'source_id':q[':question/id'],'status':'source_gap','reason':'Unrated q-34250 lacks key and solution; independent implied answer 4, missing authored response/difficulty cannot be recovered.'});continue
  text=q[':question/problem'];a,u,*bs=mats(text);c=1 if sid=='q-34241' else int(re.search(r'if \$(\d+)',text)[1]);level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  p={'a':list(map(int,a)),'u':list(map(int,u)),'c':c,'s':None if not bs else str(solve(q)[0]),'letter':re.search(r'Find \$([a-z])',text)[1]}
  r=g.generate(level,961031,sid,p);verify(r);replayed.append(r)
  bank_equal=[value(a[':answer/value']) for a in choices(q)]==[value(a[':answer/value']) for a in choices(r['question'])]
  prompt_equal=mats(text)==mats(r['question'][':question/problem']);solution_equal=mats(q[':question/worked-solution'])==mats(r['question'][':question/worked-solution'])
  # Wording is identical apart from fraction escaping and whitespace; source canonical bold styling need not be emitted.
  norm=lambda t:re.sub(r'\s+','',t.replace('\\\\frac','\\frac'))
  wording_equal=norm(text)==norm(r['question'][':question/problem']) and norm(q[':question/worked-solution'])==norm(r['question'][':question/worked-solution'])
  assert bank_equal and prompt_equal and solution_equal and wording_equal,sid
  replay.append({'source_id':q[':question/id'],'profile':sid,'status':'passed','complete_bank_equal':bank_equal,'prompt_vectors_equal':prompt_equal,'solution_matrices_equal':solution_equal,'wording_equal_after_whitespace_and_fraction_normalization':wording_equal})
 canonical=source['material']['kp'][':knowledge-point/canonical-example'];cp={'a':[-1,2,1],'u':[4,0,-2],'c':3,'s':4,'letter':'s','bank':['4','-4','0','2','No solution']}
 cr=g.generate('easy',961031,'q-34051',cp);verify(cr);assert mats(canonical[':question/problem'])==mats(cr['question'][':question/problem']);assert mats(canonical[':question/worked-solution'])==mats(cr['question'][':question/worked-solution']);replayed.append(cr)
 save('source-replay-records.json',replayed);save('source-replay-results.json',{'cases':replay,'canonical':{'id':canonical[':question/id'],'parameters':cp,'mathematical_prompt_and_solution_replay':True,'bank':'Authored independent bank; source canonical has no captured answer-field.'}})
 # Controlled pairs and all eligible correct bank roles; unmodified generator renders every record.
 pairs=[];pair_results=[];role_records=[]
 for sid in g.PROFILES:
  level='moderate' if sid in g.LEVELS['moderate'] else 'easy';base=copy.deepcopy(g.CASES[sid]);bank=g.source_bank(sid)
  for v in bank:
   p=copy.deepcopy(base);p['bank']=bank
   if level=='easy':p['s']=str(scalar(v)) if v!='No solution' else None
   elif v!='No solution':
    s=scalar(v);p['a']=[-s.numerator*(i+1) for i in range(len(base['a']))];p['u']=[p['c']*s.denominator*(i+1) for i in range(len(base['u']))]
   if level=='easy' and v=='No solution':continue
   r=g.generate(level,961033,sid,p);assert verify(r)==value(v);role_records.append(r)
 # Held bank, a, c, profile and label; change one coordinate of u to reverse consistency.
 mp=copy.deepcopy(g.CASES['q-34570']);before=g.generate('moderate',961037,'q-34570',mp);afterp=copy.deepcopy(mp);afterp['u'][0]=1;after=g.generate('moderate',961037,'q-34570',afterp)
 pairs += [before,after];assert verify(before)=='No solution' and verify(after)==-6
 pair_results.append({'kind':'relevant','indices':[0,1],'change':'u[0]: 3 -> 1, all other parameters and full visible bank held fixed','expected':['No solution','-6'],'observed':[key(before['question']),key(after['question'])],'prompts_changed':before['question'][':question/problem']!=after['question'][':question/problem'],'solutions_changed':before['question'][':question/worked-solution']!=after['question'][':question/worked-solution'],'passed':True})
 # For each explicit target profile change scalar and b together with fixed visible bank.
 for sid in g.LEVELS['easy']:
  p=copy.deepcopy(g.CASES[sid]);p['bank']=g.source_bank(sid);b=g.generate('easy',961039,sid,p);orig=verify(b);v=next(v for v in p['bank'] if v!='No solution' and scalar(v)!=orig);p2=copy.deepcopy(p);p2['s']=str(scalar(v));a=g.generate('easy',961039,sid,p2);assert verify(a)==scalar(v)
  ix=len(pairs);pairs += [b,a];pair_results.append({'kind':'relevant','profile':sid,'indices':[ix,ix+1],'change':'Change target b through new scalar; a,u,c,label and full bank fixed','expected':[str(orig),str(scalar(v))],'observed':[key(b['question']),key(a['question'])],'passed':True})
 # Irrelevant translations of the known vector compensated in b preserve residual and answer.
 p=copy.deepcopy(g.CASES['q-34249']);b=g.generate('easy',961041,'q-34249',p);p2=copy.deepcopy(p);p2['a'][0]+=1;a=g.generate('easy',961041,'q-34249',p2);ix=len(pairs);pairs += [b,a];assert verify(b)==verify(a)==-2
 assert solve(b['question'])[1]==solve(a['question'])[1];pair_results.append({'kind':'irrelevant','indices':[ix,ix+1],'change':'a1[0] 9 -> 10 and b[0] 45 -> 50, unchanged residual and bank','expected':['-2','-2'],'observed':[key(b['question']),key(a['question'])],'passed':True})
 # Cosmetic unknown label change preserves all scalar values.
 p3=copy.deepcopy(p);p3['letter']='x';c=g.generate('easy',961041,'q-34249',p3);ix=len(pairs);pairs += [b,c];assert verify(c)==-2;pair_results.append({'kind':'irrelevant','indices':[ix,ix+1],'change':'l -> x only','expected':['-2','-2'],'observed':[key(b['question']),key(c['question'])],'passed':True})
 save('counterfactual-records.json',pairs);save('counterfactual-results.json',pair_results);save('role-records.json',role_records)
 # Strict rejection of original c=2 defect and nearby invalid inputs; retain acceptance controls.
 rejected=[]
 for name,sid,p in [('original subtraction c2','q-34241',dict(copy.deepcopy(g.CASES['q-34241']),c=2)),('subtraction c3','q-34241',dict(copy.deepcopy(g.CASES['q-34241']),c=3)),('zero u','q-34570',dict(copy.deepcopy(g.CASES['q-34570']),u=[0,0])),('dimension mismatch','q-34570',dict(copy.deepcopy(g.CASES['q-34570']),u=[1,2,3])),('invalid bank','q-34249',dict(copy.deepcopy(g.CASES['q-34249']),bank=['1','1','1','1','1']))]:
  try:r=g.generate('moderate' if sid=='q-34570' else 'easy',64193,sid,p)
  except (ValueError,AssertionError) as e:rejected.append({'case':name,'parameters':p,'passed':True,'exception':type(e).__name__,'message':str(e)})
  else:rejected.append({'case':name,'parameters':p,'passed':False,'record':r})
 save('rejection-results.json',rejected);assert all(x['passed'] for x in rejected)
 math=[]
 for r in records+batch+replayed+pairs+role_records:
  ans=verify(r);math.append({'id':r['question'][':question/id'],'independent_answer':str(ans),'stored_answer':key(r['question']),'passed':True})
 save('math-results.json',{'checked':len(math),'passed':True,'cases':math})
 coverage=[]
 for sid in g.PROFILES:
  rs=[r for r in records if r['generation']['bank_profile']==sid];ans=[verify(r) for r in rs]
  coverage.append({'profile':sid,'count':len(rs),'answers':sorted(set(map(str,ans))),'dimensions':sorted({len(mats(r['question'][':question/problem'])[0]) for r in rs}),'correct_positions':sorted({next(i for i,a in enumerate(choices(r['question'])) if value(a[':answer/value'])==verify(r)) for r in rs}),'first_informative_coordinates':sorted({next(i for i,x in enumerate(mats(r['question'][':question/problem'])[1]) if x) for r in rs}),'labels':sorted({r['generation']['parameters']['letter'] for r in rs})})
 save('coverage.json',{'profiles':coverage,'normal_shortcuts':stats(records),'exact_batch_shortcuts':stats(batch),'batch_answers':[str(verify(r)) for r in batch],'sampling_rule_inspection':'Bank selected/translated independently before uniform eligible correct role; numeric roles for easy, numeric and No solution for moderate; coordinate roles generated anew; dedup in batch uses mathematical fingerprint.'})
 save('scope-results.json',{'counts':{'normal':len(records),'runner_batch':len(batch)},'dimensions':sorted({len(mats(r['question'][':question/problem'])[0]) for r in records}),'response':'one five-choice radio field','operations':'one-coefficient isolation and component comparison, no new operators or multi-unknown systems','easy_consistency':'Easy source examples all unique scalar; normal sampler preserves that focused difficulty. No solution remains a plausible bank distractor. Moderate varies consistency.','rational_moderate':'Existing q-73923 bank includes 10/3; its translated/reflected values use the same rational arithmetic; integer coordinates retained.','gaps':['q-34250 lacks authored key/solution/rating; not counted as a reproduced full source.'],'passed':True})
 for level in g.LEVELS:save('normal-'+level+'.json',[r for r in records if r['question'][':question/difficulty']==':question.difficulty/'+level])
 # Reproduce current runner metadata exactly (the batch seed drives one continuous stream, parameters are captured).
 assert all(g.generate('easy',r['generation']['seed'],r['generation']['bank_profile'],r['generation']['parameters'])==r for r in batch)
 assert g.batch('easy',5,2406259497)==batch
 # Runtime relocation uses manifest file list only, output entirely under evidence.
 d=ROOT/'relocated';d.mkdir(exist_ok=True);manifest=load(PKG/'package.json')
 for n in manifest['files']:shutil.copy2(PKG/n,d/n)
 cmd=[str(PY),str(d/manifest['entrypoint']),'--difficulty','easy','--count','7','--seed','9027613','--output',str(ROOT/'relocated-records.json')];run=subprocess.run(cmd,capture_output=True,text=True,cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});assert run.returncode==0,run.stderr
 assert load(ROOT/'relocated-records.json')==g.batch('easy',7,9027613);assert g.batch('easy',7,9027613)==g.batch('easy',7,9027613)
 save('packaging-results.json',{'command':cmd,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'versions':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'declared':manifest['dependencies'],'versions_match':manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'relocation_matches':True,'deterministic':True,'runner_batch_exact_replay':True,'runtime_imports':'standard library and sympy; source-data.json is included; no generated assets or external output dependencies'})
 # A compact UI set: exact runner batch and both members of relevant/irrelevant controlled pairs.
 render=batch+pairs[:2]+pairs[2:4]+pairs[-4:];save('render-records.json',render)
 (ROOT/'session-state.md').write_text('Independent revision sampling, full rated-source replay, canonical math replay, controlled counterfactuals, all bank roles, strict rejection, arithmetic, scope and packaging checks completed. Author checks fail on frozen original and pass on current copy. Pending shared delivery, native grading, UI screenshots, inventory and report.\n')
 print(json.dumps({'normal':len(records),'math_checked':len(math),'full_sources':len(replay)-1,'pairs':len(pair_results),'role_records':len(role_records),'batch_answers':[str(verify(r)) for r in batch],'normal_profiles':coverage},indent=2))
