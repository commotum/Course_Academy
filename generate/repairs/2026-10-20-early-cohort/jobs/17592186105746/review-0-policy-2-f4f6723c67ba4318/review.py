import os,sys,json,hashlib,importlib.util,re,subprocess,shutil
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
PKG=JOB/'workspace'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed',PKG/'17592186105746.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=S.symbols('x y')
def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def expr(s):
 s=s.strip().rstrip('.').replace('&','').replace(' ','').replace(r'\,','')
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
 s=re.sub(r'(\d|\))(?=[xy])',r'\1*',s)
 return S.sympify(s,locals={'x':x,'y':y})
def normalize(s):
 s=s.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\in','\\in').replace('\\\\,','\\,').replace('\\\\infty','\\infty')
 return re.sub(r'\s+','',s)
def equations(q):
 b=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)[1]
 rows=[]
 for row in b.split(r'\\'):
  lhs,rhs=row.split('=');rows.append([expr(lhs).coeff(x),expr(lhs).coeff(y),expr(rhs)])
 return S.Matrix(rows)
def mats(text):
 return [S.Matrix([[expr(v) for v in row.split('&')] for row in b.split(r'\\')]) for b in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def solution_valid(v,a):
 if v=='No solution':return a[:,:2].rank()!=a.rank()
 ms=mats(v)
 if len(ms)!=2 or ms[1].shape!=(2,1):return False
 vv=ms[1];return a[:,:2].rank()==a.rank() and all(S.simplify(z)==0 for z in a[:,:2]*vv-a[:,2]) and any(z.has(y) for z in vv)
def correct_index(r):
 f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'];aid=c[-1] if isinstance(c,list) else c[':answer/id']
 return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==aid)
def profile(r):return tuple(str(z) for z in equations(r['question'])[:,:2])
def mathcheck(r):
 q=r['question'];a=equations(q);f=q[':question/answer-fields'][0];banks=[solution_valid(c[':answer/value'],a) for c in f[':answer-field/choices']];idx=correct_index(r)
 ms=[m for m in mats(q[':question/worked-solution']) if m.shape==(2,3)]
 initial=ms[0]==a
 rows=all(m.rref()[0]==a.rref()[0] for m in ms)
 last=ms[-1];ref=last[1,0]==0 and last[1,1]==0 and last[0,0]!=0
 # Each displayed reduced equation and solved system must describe the same set.
 scalar=[]
 for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S):
  if 'bmatrix' in b or ':=' in b:continue
  rr=[]
  try:
   for row in b.split(r'\\'):
    lhs,rhs=row.split('=');v=expr(lhs)-expr(rhs);rr.append([v.coeff(x),v.coeff(y),-v.subs({x:0,y:0})])
   z=S.Matrix(rr);scalar.append(z.rref()[0]==a.rref()[0])
  except (ValueError,TypeError,S.SympifyError):pass
 return {'id':q[':question/id'],'generation':r['generation'],'matrix':a.tolist(),'valid_bank_indices':[i for i,v in enumerate(banks) if v],'key_index':idx,'initial_matrix_matches':initial,'matrix_chains_row_equivalent':rows,'final_ref':ref,'reduced_scalar_checks':scalar,'passed':banks==[i==idx for i in range(5)] and initial and rows and ref and all(scalar)}
if __name__=='__main__':
 hashes={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-before.json',hashes)
 src=json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']
 replay=[];replay_records=[]
 for s in src:
  sid=s[':question/math-academy-id'];d=s[':question/difficulty'][':db/ident'].split('/')[-1]
  try:r=g.generate(d,7331,sid,{'rhs_scale':1})
  except Exception as e:replay.append({'source_id':s[':question/id'],'template':sid,'passed':False,'error':str(e)});continue
  replay_records.append(r);q=r['question'];f=q[':question/answer-fields'][0];sf=s[':question/answer-fields'][0]
  prompt=normalize(q[':question/problem'])==normalize(s[':question/problem']);bank=sorted(normalize(c[':answer/value']) for c in f[':answer-field/choices'])==sorted(normalize(c[':answer/value']) for c in sf[':answer-field/choices'])
  ci=correct_index(r);si=next(i for i,c in enumerate(sf[':answer-field/choices']) if c[':answer/id']==sf[':answer-field/correct'][':answer/id'])
  expected=s[':question/worked-solution'];corrections=[]
  if sid=='q-42159':expected=expected.replace(r'1 & 7 & 4 \\ 6 & 42 & -24',r'1 & 7 & 4 \\ 6 & 42 & 24');corrections.append('initial matrix +24 agrees with prompt and elimination')
  if sid=='q-130924':expected=expected.replace(r'-3 & 10 & 6',r'-3 & 12 & 6');corrections.append('initial matrix 12 agrees with prompt and elimination')
  sol=normalize(expected)==normalize(q[':question/worked-solution']);key=normalize(f[':answer-field/choices'][ci][':answer/value'])==normalize(sf[':answer-field/correct'][':answer/value'])
  replay.append({'source_id':s[':question/id'],'template':sid,'passed':prompt and bank and key and sol,'prompt_matches':prompt,'full_bank_matches':bank,'key_matches':key,'original_key_position':si,'replay_key_position':ci,'corrected_solution_matches':sol,'corrections':corrections})
 save('source-replay-records.json',replay_records);save('source-replay.json',replay)
 # Complete small declared finite construction domain, rather than random large audit.
 records=[g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],7331,sid,{'rhs_scale':t}) for sid,q in g.CASES.items() for t in [-4,-3,-2,-1,1,2,3,4]]
 save('domain-records.json',records);save('easy-records.json',[r for r in records if r['question'][':question/difficulty'].endswith('/easy')]);batch=json.load(open(JOB/'samples.json'));save('batch-records.json',batch)
 checks=[mathcheck(r) for r in records+batch];save('math-results.json',checks)
 pairs=[g.generate('easy',7331,'q-73750',{'rhs_scale':1}),g.generate('easy',7331,'q-73750',{'rhs_scale':2}),g.generate('easy',7331,'q-42157',{'rhs_scale':1}),g.generate('easy',7331,'q-42157',{'rhs_scale':2})]
 save('counterfactual-records.json',pairs)
 save('counterfactual-results.json',{'relevant':{'change':'q-73750 scale 1 to 2; same coefficient matrix; double both constants','before_key':pairs[0]['question'][':question/answer-fields'][0][':answer-field/choices'][correct_index(pairs[0])][':answer/value'],'after_key':pairs[1]['question'][':question/answer-fields'][0][':answer-field/choices'][correct_index(pairs[1])][':answer/value'],'before':mathcheck(pairs[0]),'after':mathcheck(pairs[1])},'irrelevant':{'change':'q-42157 double both RHS values; nonzero contradictory residual doubles, preserving No solution','before':mathcheck(pairs[2]),'after':mathcheck(pairs[3])},'missing_role':{'change':'Hold first row x-6y=2 and second coefficients -4x+24y fixed; change second RHS from -10 to -8','expected':'No solution changes to x=2+6y, y free','observed':'No generator parameter for second RHS or consistency; q-42157 stays inconsistent for every allowed scale.'}})
 grade=[]
 for i,r in enumerate(records+batch+pairs):
  f=r['question'][':question/answer-fields'][0];idx=correct_index(r)
  grade.append({'label':f'independent {i} {r["generation"]["template"]} {r["generation"]["parameters"]}','record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if j==idx else 'rejected','purpose':'independently solved complete five-choice bank'} for j,c in enumerate(f[':answer-field/choices'])]})
 save('grader-input.json',grade)
 # Record invalid-boundary behavior and deterministic batch replay.
 invalid=[]
 for params in [{'rhs_scale':0},{'rhs_scale':5},{'rhs_scale':-5}]:
  try:g.generate('easy',7331,'q-42157',params);invalid.append({'parameters':params,'rejected':False})
  except ValueError as e:invalid.append({'parameters':params,'rejected':True,'error':str(e)})
 save('packaging-results.json',{'python':sys.version.split()[0],'sympy':S.__version__,'manifest_dependencies':json.load(open(PKG/'package.json'))['dependencies'],'deterministic_batch':g.batch('easy',5,7331)==g.batch('easy',5,7331),'invalid_boundary':invalid,'runtime_imports':['stdlib','sympy'],'source_files_loaded':['17592186105746/source.json'],'command':f'{sys.executable} {ROOT}/review.py'})
 save('session-state.json',{'source_account':'saved before package inspection','source_replay':{'passed':sum(c['passed'] for c in replay),'total':len(replay)},'math':{'passed':sum(c['passed'] for c in checks),'total':len(checks)}})
 (ROOT/'session-state.md').write_text('Source account completed before package inspection. Independent replay and finite-domain mathematical checks saved. Next: delivery, real grader, rendering, shortcut and inventory evidence.\n')
 print(json.dumps({'source_replay_failures':[c for c in replay if not c['passed']],'math_failures':[c for c in checks if not c['passed']],'record_count':len(records)},default=str))
