#!/usr/bin/env python3
"""Read-only review. Run with context Python -B audit.py; all writes beside this script."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,pathlib,platform,re,shutil,subprocess,collections
E=pathlib.Path(__file__).resolve().parent
JOB=E.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PKG=JOB/'workspace'
PY=REPO/'.venv/bin/python'
def save(n,x):
 p=E/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n');return p
def read(p):return json.loads(pathlib.Path(p).read_text())
def hashes():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PKG.rglob('*')) if p.is_file()}
spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186059768.py')
sys.path.insert(0,str(PKG));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def matrix(text,captured=False):
 if captured and text.startswith('\\\\'):text=text.replace('\\\\','\\')
 ms=[]
 for env,body in re.findall(r'\\begin\{(array|bmatrix)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}',text,re.S):
  ms.append([[int(v.strip()) for v in row.split('&')] for row in body.split('\\\\') if row.strip()])
 return ms

def equation_blocks(text):
 return [[r.replace('&','').strip() for r in body.split('\\\\') if r.strip()] for body in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)]
def linear(s,n):
 s=re.sub(r'\s+','',s);out=[0]*(n+1)
 assert re.fullmatch(r'[+\-0-9xyz]+',s),s
 for term in re.findall(r'[+-]?[^+-]+',s):
  if term[-1] in 'xyz':
   j='xyz'.index(term[-1]);num=term[:-1]; out[j]+=int(num) if num not in ('','+','-') else (-1 if num=='-' else 1)
  else:out[-1]+=int(term)
 return out

def expected(rows):
 n=3 if any('z' in r for r in rows) else 2
 out=[]
 for r in rows:
  a,b=r.split('=');lhs,rhs=linear(a,n),linear(b,n)
  out.append([lhs[i]-rhs[i] for i in range(n)]+[rhs[-1]-lhs[-1]])
 return out

def field(r):return r['question'][':question/answer-fields'][0]
def correct_id(f):
 c=f[':answer-field/correct'];return c[':answer/id'] if isinstance(c,dict) else c[1]
def correct_matrix(r):
 f=field(r);return matrix(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct_id(f)))[0]
def sign(m):return [[(v>0)-(v<0) for v in row] for row in m]
def check_math(r):
 q=r['question']; f=field(r); m=expected(equation_blocks(q[':question/problem'])[0]);assert correct_matrix(r)==m
 bank=[matrix(a[':answer/value'])[0] for a in f[':answer-field/choices']]
 assert len(bank)==5 and bank.count(m)==1 and len({str(v) for v in bank})==5
 sol=q[':question/worked-solution'];assert matrix(sol)==[[row[:-1] for row in m],m]
 for rows in equation_blocks(sol):assert expected(rows)==m
 return {'id':q[':question/id'],'profile':r['generation']['template'],'expected':m,'passed':True}

def sign_strategy(r):
 # Template can be recognized by surface equation layout. No coefficients are calculated.
 profile=r['generation']['template'];target=SIGNATURES[profile]
 candidates=[a for a in field(r)[':answer-field/choices'] if sign(matrix(a[':answer/value'])[0])==target]
 return len(candidates)==1 and candidates[0][':answer/id']==correct_id(field(r)),len(candidates)
def negative_corner(r):
 choices=[a for a in field(r)[':answer-field/choices'] if matrix(a[':answer/value'])[0][-1][-1]<0]
 return len(choices)==1 and choices[0][':answer/id']==correct_id(field(r))

def main():
 before=hashes();save('package-before.json',before)
 source=read(JOB/'source/source.json'); batch=read(JOB/'samples.json');save('runner-batch.json',batch)
 runtime={'python':platform.python_version(),'manifest':read(PKG/'package.json')['dependencies'],'third_party_runtime_imports':[],'command':str(PY)+' -B audit.py'};save('runtime.json',runtime)
 global SIGNATURES
 SIGNATURES={};replays=[];replay_results=[];missing=[]
 for src in source['material']['kp'][':knowledge-point/questions']:
  name=src[':question/math-academy-id'];difficulty=src[':question/difficulty'][':db/ident'].split('/')[-1]
  params={str(n):n for n in sorted({int(x) for x in re.findall(r'\d+',src[':question/problem']+src[':question/worked-solution']) if int(x)>1})}
  if name not in g.PROFILES:
   try:g.generate(difficulty,941713201,profile=name,parameters=params)
   except Exception as ex:err=type(ex).__name__+': '+str(ex)
   missing.append({'source_id':src[':question/id'],'profile':name,'difficulty':difficulty,'parameters':params,'observed':err});continue
  r=g.generate(difficulty,941713201,profile=name,parameters=params);check_math(r);replays.append(r)
  f=src[':question/answer-fields'][0];bank=[matrix(a[':answer/value'],True)[0] for a in f[':answer-field/choices']]
  assert bank==[matrix(a[':answer/value'])[0] for a in field(r)[':answer-field/choices']]
  assert correct_matrix(r)==matrix(f[':answer-field/correct'][':answer/value'],True)[0]
  assert re.sub(r'\s+','',src[':question/problem'])==re.sub(r'\s+','',r['question'][':question/problem'])
  replay_results.append({'source_id':src[':question/id'],'profile':name,'matched_choices':5,'math':'passed','prompt':'whitespace normalized exact'})
  SIGNATURES[name]=sign(correct_matrix(r))
 save('source-replays.json',replays);save('source-replay-results.json',{'replayed':replay_results,'unresolved_missing_profiles':missing,'canonical_example':'No parameterized canonical replay interface; source canonical inspected independently.'})
 records=[];boundaries=[];rejections=[]
 for idx,(name,src) in enumerate(g.PROFILES.items()):
  level=src[':question/difficulty'][':db/ident'].split('/')[-1]
  for offset in range(12):records.append(g.generate(level,941713211+idx*103+offset,profile=name))
  keys=[str(n) for n in g.slots(src)]
  for vals in ([2,24]+list(range(3,24)),[24,2]+list(range(23,2,-1))):
   params=dict(zip(keys,vals));r=g.generate(level,941713311,profile=name,parameters=params);records.append(r);boundaries.append({'profile':name,'parameters':params,'accepted':True})
  params={str(n):n for n in g.slots(src)}
  for kind,mutate in [('below-bound',1),('above-bound',25),('negative-sign',-int(keys[0]))]:
   p={**params,keys[0]:mutate}
   try:g.generate(level,941713311,profile=name,parameters=p); outcome='accepted'
   except Exception as ex:outcome=type(ex).__name__+': '+str(ex)
   rejections.append({'profile':name,'parameters':p,'case':kind,'outcome':outcome})
  if len(keys)>1:
   p={k:2 for k in keys}
   try:g.generate(level,941713311,profile=name,parameters=p);outcome='accepted'
   except Exception as ex:outcome=type(ex).__name__+': '+str(ex)
   rejections.append({'profile':name,'parameters':p,'case':'equal-magnitude','outcome':outcome})
 save('independent-samples.json',records);save('independent-easy.json',[r for r in records if r['generation']['template'] in ['q-20361','q-1052','q-129122','q-129124','q-71722']]);save('independent-moderate.json',[r for r in records if r['question'][':question/difficulty'].endswith('/moderate')]);save('boundaries.json',{'accepted':boundaries,'rejection_cases':rejections,'resampling':'No generator retry loop. random.sample enforces distinct 2..24 values; explicit invalid parameters assert.'})
 save('math-results.json',{'records':[check_math(r) for r in replays+records+batch],'independent_method':'integer linear-term parsing of displayed prompt; full bank and two solution matrices checked','count':len(replays+records+batch)})
 # Controlled dependency pairs, generated through the real API.
 base_params={'2':2,'3':3,'4':4,'5':5,'6':6}
 base=g.generate('easy',941713401,profile='q-1052',parameters=base_params)
 related=g.generate('easy',941713401,profile='q-1052',parameters={**base_params,'6':24})
 irrelevant=copy.deepcopy(base);irrelevant['question'][':question/problem']=irrelevant['question'][':question/problem'].replace('6+y','y+6')
 irrelevant['review_fixture']={'change':'Only commutative term order in second equation; no generator repair; original key and solution retained'}
 pairs=[base,related,irrelevant]
 for r in pairs:check_math(r)
 assert correct_matrix(base)!=correct_matrix(related) and correct_matrix(base)==correct_matrix(irrelevant)
 save('counterfactual-records.json',pairs)
 save('counterfactual-results.json',{'relevant':{'change':'q-1052 literal 6 -> 24, same seed and all other parameters','before':correct_matrix(base),'after':correct_matrix(related),'prompt_solution_math':'passed'},'irrelevant':{'change':'6+y -> y+6 in displayed second equation','before':correct_matrix(base),'after':correct_matrix(irrelevant),'prompt_solution_math':'passed'},'sign_counterfactual':{'parameters':{**base_params,'6':-6},'expected':'same algebraic method with RHS sign reversed; bank and explanation recomputed','observed':'generator AssertionError: parameters must be >=2; this answer-bearing sign cannot vary'}})
 # Native grader: all choices per supported source and independent records + exact batch + pairs.
 cases=[]
 for k,r in enumerate(replays+records+batch+pairs):
  f=field(r);cases.append({'label':f'math-checked-{k}-{r["generation"]["template"]}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct_id(f) else 'rejected','purpose':'independent displayed-equation matrix match' if a[':answer/id']==correct_id(f) else 'plausible source-profile distractor'} for a in f[':answer-field/choices']]})
 save('grader-input.json',cases)
 # All captured generated records: replay original metadata, compare complete mathematical contents and IDs.
 inv=read(JOB/'source/inventory.json');old=read(PKG/'17592186059768/reference/replenishment/basis-2204/generated.json');old_by_id={r['question'][':question/id']:r for r in old}
 generated=[];affected=[];invcases=[]
 for q in inv['questions']:
  if ':question/math-academy-id' in q:continue
  r=old_by_id[q[':question/id']];meta=r['generation'];now=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],meta['seed'],profile=meta['template'],parameters=meta['parameters'])
  assert r['question'][':question/id']==q[':question/id']
  expected_q=copy.deepcopy(q);expected_q.pop(':db/id',None)
  # Captured enum maps versus serialized strings do not change mathematical records.
  assert expected(equation_blocks(q[':question/problem'])[0])==correct_matrix(now)
  stored_bank=[matrix(a[':answer/value'])[0] for a in q[':question/answer-fields'][0][':answer-field/choices']]
  assert sorted(map(str,stored_bank))==sorted(str(matrix(a[':answer/value'])[0]) for a in field(now)[':answer-field/choices'])
  assert {a[':answer/id'] for a in field(r)[':answer-field/choices']}=={a[':answer/id'] for a in q[':question/answer-fields'][0][':answer-field/choices']}
  assert matrix(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])[0]==correct_matrix(now)
  def portable(v):
   if isinstance(v,list):return [portable(x) for x in v]
   if isinstance(v,dict):
    if ':db/ident' in v:return v[':db/ident']
    return {k:portable(x) for k,x in v.items() if k!=':db/id'}
   return v
  current_id=now['question'][':question/id'];now['question']=portable(q)
  f=field(now);f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  now['generation']=copy.deepcopy(meta);now['inventory_reproduction']={'entity_id':q[':db/id'],'original_metadata_path':'workspace/17592186059768/reference/replenishment/basis-2204/generated.json','current_generator_version':'1.0.1','stored_id_and_complete_bank_match':True,'current_normalized_generator_id':current_id,'note':'v1.0.0 stored identity retained from original metadata record; current v1.0.1 reconstructs equal mathematical prompt/bank with newer identity'}
  generated.append(now);success,unique=sign_strategy(now)
  invcases.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'template':meta['template'],'sign_mask_success':success,'unique_candidates':unique,'negative_corner_success':negative_corner(now)})
  if success:
   affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':f'{meta["template"]}: memorized source sign mask uniquely identifies correct matrix without coefficient collection; fixed sign topology','reproduction':f'{PY} -B {E}/audit.py (replays seed {meta["seed"]}, profile {meta["template"]}, parameters {json.dumps(meta["parameters"],sort_keys=True)})','evidence_path':'generated-records.json'})
 save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inv['basis'],'original_source_questions_excluded':10,'generated_tested':len(generated),'results':invcases,'limits':'Captured inventory has no generation metadata; exact original metadata recovered from package reference generated.json, validated against stored ID, full bank and mathematical system. No original source question is marked generated.'})
 # Read-only relocation, no package writes.
 reloc=E/'relocated-package'
 if not reloc.exists():shutil.copytree(PKG,reloc)
 cmd=[str(PY),'-B',str(reloc/'17592186059768.py'),'--difficulty','easy','--seed','941713501','--count','3']
 run=subprocess.run(cmd,cwd=E,capture_output=True,text=True);save('relocation-command.json',{'command':cmd,'cwd':str(E),'returncode':run.returncode,'stderr':run.stderr});assert run.returncode==0
 relocated=json.loads(run.stdout);save('relocation-records.json',relocated)
 original=[g.generate('easy',941713501+i) for i in range(3)];assert relocated==original
 save('replay-results.json',{'deterministic_seed_replay':all(g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],profile=r['generation']['template'])==r for r in records if r['generation']['seed']!=941713311),'relocation_equal':True,'external_output':'JSON only; no generated assets or external writes; imported with bytecode disabled'})
 subprocess.run([str(PY),'-B',str(E/'reproduce_inventory.py')],cwd=E,check=True,capture_output=True,text=True)
 after=hashes();save('package-integrity.json',{'unchanged':before==after,'files':len(before),'before':'package-before.json','after_hashes':after});assert before==after
 save('shortcut-signatures.json',SIGNATURES)
 print(json.dumps({'supported_replays':len(replays),'missing_source_profiles':missing,'sample_count':len(records),'math_checked':len(replays+records+batch),'affected_inventory':len(affected),'package_unchanged':before==after},indent=2))
 (E/'session-state.md').write_text('Source account saved before package inspection. Independent audit.py completed source replay, math, boundaries, controlled pairs, inventory reproduction and relocation. Missing three moderate source profiles; investigating fixed-sign shortcuts. Native grader, delivery, UI rendering and final reports pending. All package hashes unchanged.\n')
if __name__=='__main__':main()
