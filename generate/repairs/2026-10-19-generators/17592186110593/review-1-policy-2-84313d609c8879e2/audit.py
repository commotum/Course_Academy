import os,sys,json,pathlib,hashlib,subprocess,re,shutil,collections,random,math
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
R=pathlib.Path('/home/jake/Developer/Course_Academy')
J=R/'generate/repairs/2026-10-19-generators/17592186110593'
W=J/'workspace'
P=R/'.venv/bin/python'
def save(n,v): (E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def fingerprint():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(W.rglob('*')) if p.is_file()}
save('package-before.json',fingerprint())
sys.path.insert(0,str(W));import generator as g
# Pure independent mathematical parsing. No generator parameters/role_value used.
import sympy as S

def group(t,i,left='(',right=')'):
 assert t[i]==left,(t,i)
 depth=1;j=i+1
 while depth:
  if t[j]==left:depth+=1
  elif t[j]==right:depth-=1
  j+=1
 return t[i+1:j-1],j

def tex(t):
 t=t.split('=',1)[-1].strip().replace('⁡','').replace(r'\left','').replace(r'\right','').replace('{log}',r'\log')
 def convert(t):
  o='';i=0
  while i<len(t):
   if t.startswith(r'\frac',i):
    a,j=group(t,i+5,'{','}');b,j=group(t,j,'{','}');o+='(('+convert(a)+')/('+convert(b)+'))';i=j
   elif t.startswith(r'\log',i):
    j=i+4;assert t[j]=='_';j+=1
    if t[j]=='{':b,j=group(t,j,'{','}')
    else:b=t[j];j+=1
    while t[j].isspace():j+=1
    a,j=group(t,j);o+='log(('+convert(a)+'),('+convert(b)+'))';i=j
   else:o+=t[i];i+=1
  return o.replace('{','(').replace('}',')')
 t=convert(t)
 t=re.sub(r'(\d)(?=log)',r'\1*',t)
 return S.sympify(t,locals={'log':S.log})

def prompt(r):
 t=r['question'][':question/problem']
 t=t.replace(' ','').replace('${','$').replace('}^','^')
 m=re.search(r'\$(\d+)\^\{x([+-]\d+)?\}=(\d+)',t)
 assert m, t
 b,s,n=int(m[1]),int(m[2] or 0),int(m[3])
 return b,n,s

def fid(r):return r['question'][':question/answer-fields'][0]
def key(r):
 c=fid(r)[':answer-field/correct']
 return c[':answer/id'] if isinstance(c,dict) else c[1]
def choices(r):return fid(r)[':answer-field/choices']
def answer(r):return next(c[':answer/value'] for c in choices(r) if c[':answer/id']==key(r))

def mathcheck(records,name):
 failures=[];details=[]
 for i,r in enumerate(records):
  b,n,s=prompt(r);expected=S.log(n)/S.log(b)-s
  cs=choices(r);values=[tex(c[':answer/value']) for c in cs]
  good=[c[':answer/id'] for c,v in zip(cs,values) if abs(complex(S.N(v-expected,75)))<1e-60]
  final=re.findall(r'(?:solution is|obtain the exact solution)[\s\S]*?\$x=([^$]+)\$',r['question'][':question/worked-solution'])
  if good!=[key(r)]:failures.append({'index':i,'problem':r['question'][':question/problem'],'good':good,'stored':key(r)})
  if final and abs(complex(S.N(tex(final[-1])-expected,75)))>1e-60:failures.append({'index':i,'reason':'solution final mismatch'})
  # Normal generator solution must show exact inversion and offset, independently from metadata.
  if 'source_replay' not in r.get('generation',{}):
   sol=r['question'][':question/worked-solution']
   inv='x'+(f'{s:+}' if s else '')+rf'=\log_{{{b}}}({n})'
   if inv not in sol:failures.append({'index':i,'reason':'missing/corrupt inversion','expected':inv})
  details.append({'index':i,'prompt_parameters':[b,n,s],'correct_value':answer(r),'matching_choices':good,'final_expression_checked':bool(final)})
 return {'set':name,'count':len(records),'precision':75,'failures':failures,'cases':details}

seeds=[104729,271828,314159,161803,65537,8675309,20261019,433494437]
samples=[]
for seed in seeds:samples+=g.generate('easy',40,seed)
save('samples.json',samples)
batch=json.load(open(J/'samples.json'));save('runner-batch.json',batch)
replays=[g.replay_source(i) for i in g.SOURCE_IDS];save('source-replays.json',replays)
source=json.load(open(J/'source/source.json'))['material']['kp']
replay=[]
for original,r in zip(source[':knowledge-point/questions'],replays):
 of=original[':question/answer-fields'][0];rf=fid(r)
 old={c[':answer/id']:c[':answer/value'] for c in of[':answer-field/choices']}
 new={c[':answer/id']:c[':answer/value'] for c in choices(r)}
 same_ids=old.keys()==new.keys()
 same_values=same_ids and all(S.simplify(tex(old[k])-tex(new[k]))==0 for k in old)
 # Independent whitespace/capture-TeX normalization for prompt and narrative.
 def norm(t):return re.sub(r'\s+','',t.replace('⁡','').replace('{log}',r'\log').replace(r'\left','').replace(r'\right',''))
 replay.append({'source_id':original[':question/math-academy-id'],'question_id':original[':question/id'],'bank_ids_identical':same_ids,'all_five_values_equivalent':same_values,'key_identical':of[':answer-field/correct'][':answer/id']==key(r),'prompt_equivalent':norm(original[':question/problem'])==norm(r['question'][':question/problem']),'worked_solution_equivalent':norm(original[':question/worked-solution'])==norm(r['question'][':question/worked-solution']),'field_type':rf[':answer-field/type'],'field_key':rf[':answer-field/key']})
# Banks deliberately hold all displayed evidence except equation and dependent solution fixed.
banks={'direct':[(2,3,0),(2,5,0),(7,3,0),(7,5,0),(7,11,0)],'shifted':[(2,3,1),(2,3,-1),(7,3,2),(7,5,-2),(2,5,3)]}
controlled=[]
for name,roles in banks.items():
 for selected in range(5):controlled.append(g.build(roles,selected,order=[2,4,0,3,1],seed=91027))
controlled.append(g.build(banks['shifted'],0,order=[1,3,0,4,2],seed=91028))
# Canonical example: same original values, no captured answer bank exists.
canonical=g.build([(2,3,-1),(2,3,1),(3,5,-1),(3,5,2),(2,7,3)],0,seed=91029)
controlled.append(canonical)
save('controlled.json',controlled)
save('source-replay-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 repo/.venv/bin/python evidence_root/audit.py','replays':replay,'canonical':{'source_id':'e-4067','generated':canonical,'expected':'log_2(3)-1','source_answer_bank_absent':True}})
math_results=[mathcheck(a,n) for a,n in [(samples,'fresh seeds'),(batch,'runner batch'),(replays,'source replay'),(controlled,'controlled and canonical')]]
save('math-results.json',math_results)
# Test deterministic API/CLI and declared runtime from a relocated manifest-only package.
rel=E/'relocated';rel.mkdir(exist_ok=True)
manifest=json.load(open(W/'package.json'))
for name in manifest['files']+['package.json']:shutil.copyfile(W/name,rel/name)
commands=[]
for args in [['--seed','104729','--count','40'],['--count','0'],['--count','-1'],['--count','1001'],['--difficulty','moderate']]:
 cmd=[str(P),str(rel/'generator.py'),*args];out=subprocess.run(cmd,cwd=E,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 item={'argv':cmd,'exit_code':out.returncode,'stderr':out.stderr,'stdout_sha256':hashlib.sha256(out.stdout.encode()).hexdigest()}
 if out.returncode==0:item['records']=json.loads(out.stdout)
 commands.append(item)
large=g.generate('easy',1000,98593);save('boundary-1000.json',large)
save('packaging-results.json',{'manifest':manifest,'actual_python':sys.version.split()[0],'runtime_matches':sys.version.split()[0]==manifest['dependencies']['python'],'determinism':samples[:40]==g.generate('easy',40,104729),'relocation_matches':commands[0]['records']==json.loads(json.dumps(samples[:40])),'count_zero':commands[1]['records']==[],'invalid_requests_rejected':all(x['exit_code']!=0 for x in commands[2:]),'commands':commands,'max_count_returned':len(large),'max_count_unique_equations':len({prompt(r) for r in large}),'package_before':'package-before.json'})
# Native grader: all choices, not just stored key; independent numerical/symbolic prompt check supplies expectations.
grader=[]
for label,rs in [('fresh',samples),('runner',batch),('source',replays),('controlled',controlled)]:
 for i,r in enumerate(rs):
  b,n,s=prompt(r);v=S.log(n)/S.log(b)-s
  checks=[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if abs(complex(S.N(tex(c[':answer/value'])-v,75)))<1e-60 else 'rejected','purpose':'Independently evaluate option against equation, including distractors'} for c in choices(r)]
  grader.append({'label':f'{label}-{i}','record':r,'checks':checks})
save('grader-input.json',grader)
# Render source banks, relevant controlled pairs, irrelevant reorder, canonical and runner representatives.
render=replays+controlled[:2]+controlled[5:7]+controlled[10:]+batch[:2]
save('render-input.json',render)
save('test-plan.json',{'command':f'PYTHONDONTWRITEBYTECODE=1 {P} {E}/audit.py','seeds':seeds,'count_per_seed':40,'controlled_banks':banks,'controlled_order':[2,4,0,3,1],'boundary_seed':98593,'mathematical_oracle':'Parse prompt b^(x+s)=n and all TeX options independently; SymPy log(n)/log(b)-s; 75-digit comparison, plus source-bank exact expression comparisons.','sample_files':['samples.json','runner-batch.json','source-replays.json','controlled.json','boundary-1000.json']})
(E/'session-state.md').write_text('Completed: independent source analysis, 320 fresh samples, all four full source-bank replays, canonical example, 12 controlled instances, max-count/relocation/rejection checks and independent math checks. Next: native grader, actual UI renderer, delivery/selection coverage and conditional shortcuts. All package imports disable bytecode.\n')
print(json.dumps({'sample_count':len(samples),'math_failures':[(x['set'],len(x['failures'])) for x in math_results],'replay':replay,'packaging':{k:v for k,v in json.load(open(E/'packaging-results.json')).items() if k not in ['commands','manifest']}}))
