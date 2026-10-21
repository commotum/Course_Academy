import sys,os,json,re,hashlib,importlib.util,collections,pathlib,platform,shutil,subprocess
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
E=pathlib.Path(__file__).resolve().parent
JOB=E.parent; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PKG=JOB/'workspace'
def dump(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def hashes(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file()}
dump('package-before.json',hashes(PKG))
sys.path.insert(0,str(PKG))
spec=importlib.util.spec_from_file_location('review_generator',PKG/'17592186115241.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
S=json.load(open(JOB/'source/source.json')); B=json.load(open(JOB/'samples.json'));dump('batch.json',B)
v=sp.symbols('x y z w'); trans=standard_transformations+(implicit_multiplication_application,)
def expr(t):
 t=t.replace('−','-').replace(' ', '').strip().rstrip('.,')
 t=re.sub(r'\{x\}_\{([1-4])\}',lambda m:str(v[int(m[1])-1]),t)
 t=re.sub(r'x_\{([1-4])\}',lambda m:str(v[int(m[1])-1]),t)
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 return sp.expand(parse_expr(t,local_dict=dict(zip(map(str,v),v)),transformations=trans))
def rawfix(t):return t.replace('\\\\','\\') if r'\\begin' in t else t

def vec(t):
 t=rawfix(t)
 m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',t,re.S)
 if not m:return None
 return tuple(expr(a) for a in m[1].split(r'\\'))
def system(t):
 m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',rawfix(t),re.S)
 rows=[]
 n=3 if ('z' in t or '{x}_{3}' in t) else 2
 for line in m[1].split(r'\\'):
  left,right=line.replace('&','').split('='); e=expr(left)-expr(right)
  rows.append([e.coeff(a) for a in v[:n]]+[-e.subs(dict.fromkeys(v,0))])
 return sp.Matrix(rows)
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);ref=f[':answer-field/correct'];return ref[-1] if isinstance(ref,list) else ref[':answer/id']
def mathcheck(r):
 q=r['question']; M=system(q[':question/problem']); n=M.cols-1;R,piv=M.rref(); A=M[:,:-1];b=M[:,-1]; assertions=[]
 assertions.append(('consistent_one_free',n not in piv and n-len(piv)==1))
 valid=[]; bank=[]
 for c in field(r)[':answer-field/choices']:
  vv=vec(c[':answer/value']);bank.append(vv)
  if vv is None:continue
  syms=set().union(*(a.free_symbols for a in vv));dim=len(vv)==n
  works=dim and all(sp.simplify(a)==0 for a in A*sp.Matrix(vv)-b)
  # all solution sets have one parameter and a nonzero direction; rejects an isolated point
  full=works and len(syms)==1 and any(sp.diff(a,next(iter(syms)))!=0 for a in vv)
  if full:valid.append(c[':answer/id'])
 assertions.append(('unique_full_solution_and_key',valid==[correct(r)]))
 stages=[]
 for m in re.finditer(r'\\begin\{(array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{\1\}',q[':question/worked-solution'],re.S):
  try:
   a=sp.Matrix([[expr(c) for c in row.split('&')] for row in m[2].split(r'\\')])
   if a.shape==M.shape:stages.append(a)
  except Exception:pass
 assertions.append(('solution_stages_row_equivalent',bool(stages) and all(a.rref()[0]==R for a in stages)))
 return {'id':q[':question/id'],'matrix':str(M.tolist()),'rank':len(piv),'free_columns':[j for j in range(n) if j not in piv],'assertions':dict(assertions),'pass':all(a[1] for a in assertions),'stages':len(stages)}
def shortcut(r):
 cs=field(r)[':answer-field/choices']; vectors=[vec(c[':answer/value']) for c in cs]
 if any(x is None or len(x)<3 for x in vectors):return {'applicable':False,'id':r['question'][':question/id']}
 # Pure printed-component matching; no algebra, equations, parameter metadata or key used to choose.
 # Normalize whitespace only; expressions are already consistently formatted in these banks.
 strings=[re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',rawfix(c[':answer/value']),re.S) for c in cs]
 if not all(strings):return {'applicable':False,'id':r['question'][':question/id']}
 rows=[[a.strip() for a in x[1].split(r'\\')] for x in strings]
 modes=[];freq=[]
 for j in [0,1]:
  f=collections.Counter(x[j] for x in rows); freq.append(dict(f));mx=max(f.values()); modes.append([a for a,b in f.items() if b==mx])
 candidates=[i for i,row in enumerate(rows) if all(row[j] in modes[j] for j in [0,1])]
 unique_modes=all(len(a)==1 for a in modes)
 selected=cs[candidates[0]][':answer/id'] if len(candidates)==1 else None
 return {'id':r['question'][':question/id'],'applicable':True,'unique_modes':unique_modes,'component_counts':freq,'candidate_positions':[i+1 for i in candidates], 'selected_answer_id':selected,'correct':selected==correct(r),'correct_position':next(i+1 for i,c in enumerate(cs) if c[':answer/id']==correct(r))}
def main():
 # Independently selected seed range, one modest regression sample.
 
 records=[g.generate_easy(seed=i) for i in range(90101,90161)]
 dump('fresh.json',records)
 # Source replay covers every declared source, full banks at identity parameters.
 replays=[]; replay_report=[]; unsupported=[]
 for q in S['material']['kp'][':knowledge-point/questions']:
  profile=q[':question/math-academy-id'];M=system(q[':question/problem'])
  if profile not in g.BASE:
   try:g.generate_easy(seed=90101,profile=profile);error='unexpectedly accepted'
   except Exception as ex:error=type(ex).__name__+': '+str(ex)
   unsupported.append({'id':q[':question/id'],'profile':profile,'error':error});continue
  r=g.generate_easy(seed=90101,profile=profile,parameters={'scale':1,'offsets':[0]*(M.cols-1)})
  replays.append(r)
  source_bank=collections.Counter(str(vec(c[':answer/value'])) for c in q[':question/answer-fields'][0][':answer-field/choices'])
  generated_bank=collections.Counter(str(vec(c[':answer/value'])) for c in field(r)[':answer-field/choices'])
  replay_report.append({'source_id':q[':question/id'],'profile':profile,'prompt_system_equal':system(r['question'][':question/problem'])==M,'complete_bank_equal':source_bank==generated_bank,'source_has_solution':bool(q.get(':question/worked-solution')),'math':mathcheck(r)})
 dump('source-replay-records.json',replays);dump('source-replay.json',{'command':'PYTHONDONTWRITEBYTECODE=1 '+str(REPO/'.venv/bin/python')+' audit.py','supported':replay_report,'unsupported_current_sources':unsupported,'canonical':'No source profile or target/free-variable slot implements the canonical y-free, z-constant system.'})
 # Controlled relevant/irrelevant changes, same seed and most parameters fixed.
 p={'free_coefficients':[2,-3],'constants':[1,4],'mix':[1,1]}
 pa={**p,'free_coefficients':[-2,-3]};pi={**p,'mix':[-1,1]}
 cf=[g.generate_easy(seed=90217,parameters=pp) for pp in [p,pa,pi]];dump('counterfactual-records.json',cf)
 def keyed_vec(r):return next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))
 dump('counterfactual-results.json',{'command':'audit.py, explicit parameters in counterfactual-records.json','relevant':{'change':'first RREF free coefficient 2 to -2','before':keyed_vec(cf[0]),'after':keyed_vec(cf[1]),'answer_changed':keyed_vec(cf[0])!=keyed_vec(cf[1]),'prompt_changed':cf[0]['question'][':question/problem']!=cf[1]['question'][':question/problem'],'solution_changed':cf[0]['question'][':question/worked-solution']!=cf[1]['question'][':question/worked-solution']},'irrelevant':{'change':'row mixing multiplier 1 to -1','before':keyed_vec(cf[0]),'after':keyed_vec(cf[2]),'answer_preserved':keyed_vec(cf[0])==keyed_vec(cf[2]),'prompt_changed':cf[0]['question'][':question/problem']!=cf[2]['question'][':question/problem']}})
 # Rational boundary, invalid explicit inputs, zero-slope restriction and whole-instance rejection.
 boundary=[];rejects=[]
 for pp in [{'free_coefficients':['1/2',-5],'constants':['1/2',-6],'mix':[-2,2]}, {'scale':'-5/2','offsets':[10,-10,10]}]:
  try:
   r=g.generate_easy(seed=90301,parameters=pp,**({'profile':'q-131715'} if 'scale' in pp else {}));boundary.append(r)
  except Exception as ex:rejects.append({'parameters':pp,'unexpected_error':str(ex)})
 for label,pp in [('zero_slope',{**p,'free_coefficients':[0,-3]}),('over_bound',{**p,'free_coefficients':[6,-3]}),('collision',{**p,'constants':[0,4]}),('zero_mix',{**p,'mix':[0,1]})]:
  try:g.generate_easy(seed=90301,parameters=pp);rejects.append({'case':label,'parameters':pp,'accepted':True})
  except Exception as ex:rejects.append({'case':label,'parameters':pp,'accepted':False,'error':str(ex)})
 dump('boundary-records.json',boundary);dump('rejection-tests.json',rejects)
 allrec=B+records+replays+cf+boundary
 mathresults=[mathcheck(r) for r in allrec];dump('math-results.json',{'count':len(mathresults),'failed':[r for r in mathresults if not r['pass']],'cases':mathresults})
 dump('shortcut-results.json',{name:[shortcut(r) for r in recs] for name,recs in [('batch',B),('fresh',records),('source_profiles',replays),('counterfactuals',cf)]})
 # Real native radio grading: independently checked entire five-option banks, includes paired stale choices.
 grade=[]
 for i,r in enumerate(B+replays+cf+boundary):
  f=field(r);grade.append({'label':str(i)+': '+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'independent symbolic full-set verification; all bank choices'} for c in f[':answer-field/choices']]})
 dump('grader-input.json',grade)
 # Rendering includes source profiles, exact batch and both kinds of controlled pairs.
 dump('render-records.json',B+replays+cf+boundary)
 # Determinism/dependencies and relocation smoke test (copy package only inside evidence).
 replay_equal=records[0]==g.generate_easy(seed=90101)
 versions={'python':platform.python_version(),'packages':{'sympy':sp.__version__}}
 manifest=json.load(open(PKG/'package.json'))
 # Minimal runtime closure relocated; declared resources include bundled source data, not the whole historical evidence tree.
 rel=E/'relocated';rel.mkdir(exist_ok=True)
 for name in ['17592186115241.py','math_format.py']:shutil.copyfile(PKG/name,rel/name)
 (rel/'17592186115241').mkdir(exist_ok=True);shutil.copyfile(PKG/'17592186115241/source.json',rel/'17592186115241/source.json')
 cp=subprocess.run([sys.executable,str(rel/'17592186115241.py'),'--difficulty','easy','--seed','90101','--count','1','--format','json'],cwd=E,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 rel_result=json.loads(cp.stdout) if cp.returncode==0 else None
 dump('packaging.json',{'runtime':versions,'declared':manifest['dependencies'],'exact_match':versions==manifest['dependencies'],'deterministic':replay_equal,'relocation_command':cp.args,'relocation_exit':cp.returncode,'relocation_stderr':cp.stderr,'relocation_same_record':rel_result==[records[0]],'external_outputs':'none; stdout JSON; no images or database calls in entrypoint','package_unchanged':hashes(PKG)==json.load(open(E/'package-before.json'))})
 (E/'session-state.md').write_text('Completed source reconstruction, package inspection, 60 fresh easy samples, 11 complete source-bank replays, 3 controlled counterfactual records, boundaries/rejections, independent prompt-based math and shortcut tests, dependency/determinism/relocation checks. Native grading, delivery, UI screenshots and inventory replay pending. Run with PYTHONDONTWRITEBYTECODE=1; no package writes.\n')
 print(json.dumps({'fresh':len(records),'replays':len(replays),'unsupported':unsupported,'math_count':len(mathresults),'math_failures':len([r for r in mathresults if not r['pass']]),'shortcut':{name:{'total':len(rr),'unique_mode_decisions':sum(shortcut(r).get('unique_modes',False) for r in rr),'correct':sum(shortcut(r).get('correct',False) for r in rr)} for name,rr in [('batch',B),('fresh',records)]},'packaging':json.load(open(E/'packaging.json'))},indent=2))

if __name__=="__main__":main()
