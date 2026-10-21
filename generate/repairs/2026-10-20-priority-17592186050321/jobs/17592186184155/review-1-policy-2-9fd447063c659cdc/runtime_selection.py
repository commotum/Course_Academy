from audit import *
manifest=json.loads((W/'package.json').read_text());clone=E/'relocated-package';clone.mkdir(exist_ok=True)
for f in ['package.json']+manifest['files']:shutil.copy2(W/f,clone/f)
cwd=E/'runtime-cwd';cwd.mkdir(exist_ok=True)
args=['--seed','995317','--count','5','--difficulty','hard','--format','json']
logs=[]
def run(path,args):
 cmd=[PY,'-B','-I',str(path/'generator.py')]+args
 # -I omits script directory, so use -B plus a cleared PYTHONPATH instead; valid standalone imports require script directory.
 cmd=[PY,'-B',str(path/'generator.py')]+args
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONPATH':'','PYTHONDONTWRITEBYTECODE':'1'})
 logs.append({'command':cmd,'cwd':str(cwd),'returncode':r.returncode,'stderr':r.stderr,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()})
 return r
first=run(W,args);again=run(W,args);reloc=run(clone,args)
assert first.returncode==again.returncode==reloc.returncode==0
assert first.stdout==again.stdout==reloc.stdout
save('runtime-samples.json',json.loads(first.stdout))
assert all(check(r) for r in json.loads(first.stdout))
for name in ['q-2250','q-29830','q-113848','q-113850']:
 a=run(W,['--replay-source',name]);b=run(clone,['--replay-source',name]);assert a.returncode==b.returncode==0 and a.stdout==b.stdout
for args2,expect in [(['--count','0'],0),(['--count','-1'],2),(['--difficulty','easy'],2),(['--difficulty','moderate'],2),(['--count','2','--difficulty','unclassified'],0)]:
 r=run(clone,args2);assert r.returncode==expect
 if expect==0:
  assert isinstance(json.loads(r.stdout),list)
  assert all(x['question'][':question/difficulty']==':question.difficulty/hard' for x in json.loads(r.stdout))
assert not list(cwd.iterdir())
imports={}
import ast
for f in manifest['files']:
 if f.endswith('.py'):
  tree=ast.parse((clone/f).read_text());mods=[]
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):mods.extend(x.name.split('.')[0] for x in node.names)
   elif isinstance(node,ast.ImportFrom) and node.module:mods.append(node.module.split('.')[0])
  imports[f]=sorted(set(mods))
  assert all(x in sys.stdlib_module_names or x=='math_format' for x in mods)
assert manifest['dependencies']=={'python':'.'.join(map(str,sys.version_info[:3])),'packages':{}}
# Isolated invalid parameter probes: real sampling never draws these.
rejections=[]
base={'profile':'negative_fractional','order':[0,1,2],'states':[[0,1,1],[1,0,1],[1,1,0],[1,1,1]]}
for name,t in [('log-exponent',[[1,-1],[1,3],[1,-2]]),('zero-coefficient',[[0,'-4/3'],[1,3],[1,-2]]),('unsupported-even-root',[[1,'-3/2'],[1,3],[1,-2]]),('out-of-range-power',[[1,'-4/3'],[1,8],[1,-2]])]:
 try:g.generate(78,parameters=t,design=base);raise RuntimeError('accepted invalid '+name)
 except AssertionError:rejections.append(name)
# Exhaust the five-of-eight binary design domain; no numeric values are rejected.
valid=[];allbanks=list(itertools.combinations(itertools.product((0,1),repeat=3),5))
for bank in allbanks:
 if all(sum(row[j] for row in bank) in (2,3) for j in range(3)):valid.append(bank)
assert valid
save('runtime-results.json',{'commands':logs,'determinism':True,'relocation':True,'external_output':'stdout only, empty working directory after all launches','dependencies_installed':manifest['dependencies'],'imports':imports,'invalid_cases_rejected':rejections,'sample_design':{'candidate_banks':len(allbanks),'accepted_banks':len(valid),'pivot':'uniform randrange(5), after answer-neutral column-balance rejection','parameter_rejection':'none: parameter sampling occurs after design acceptance; all candidate banks allow each candidate to be true','cutoff':10000},'package_unchanged':hash_package()==json.loads((E/'package-before.json').read_text())})
# Read-only faithful reproduction of the inspected selection.rs select(): all delivered
# candidates are hard, so nonzero hard weight means uniform selection of fresh hard rows.
rs=json.loads((E/'delivery-sampled/accepted.json').read_text());rb=json.loads((E/'delivery-batch/accepted.json').read_text())
def selection(rs,seeds,weights,fresh=True):
 if weights is None:return [0 for _ in seeds]
 if weights[2]<=0:return []
 pool=list(range(len(rs)))
 if not fresh:pool=pool[len(pool)//2:]
 chosen=[]
 for seed in seeds:
  d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53)
  chosen.append(pool[int(u*len(pool))])
 return chosen
result=[];selected=[]
for label,rr in [('sampled',rs),('runner',rb)]:
 for name,weights,fresh in [('hard-only',[0,0,1],True),('mixed',[2,3,4],True),('freshness-half',[0,0,1],False),('zero-hard',[1,1,0],True),('unconfigured',None,True)]:
  chosen=selection(rr,[f'independent-review-{i}' for i in range(1000)],weights,fresh)
  profiles=collections.Counter(rr[i]['generation']['template'] for i in chosen)
  positions=collections.Counter(str(qparts(rr[i])[2]) for i in chosen)
  result.append({'input':label,'policy_case':name,'weights':weights,'selected':len(chosen),'distinct':len(set(chosen)),'profiles':profiles,'positions':positions})
  if label=='sampled' and name=='hard-only':selected=[rr[i] for i in chosen]
save('selection-samples.json',selected)
save('selection-results.json',{'command':f'{PY} runtime_selection.py','source_file':str(REPO/'engine/rust/question_selection.rs'),'source_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'inspected_lines':'seen_before_task 110-129; select 135-217','results':result,'captured_basis':5277,'limits':['No database read/write: synthetic monotonically assigned candidate entity IDs fix order for a faithful conditional selection reproduction; actual database IDs can change seeded ordering, not uniform support.','Actual learner history and policy are not supplied; freshness-half is a controlled history example. Zero hard weight excludes these records; unconfigured policy always takes the first candidate.','Inventory can change after capture; conclusions apply to captured delivery plus the explicitly modeled policy cases.']})
# Selection shortcut coverage still uses actual accepted records.
from decision_tests import probes
save('selection-shortcut-results.json',{'results':probes(selected,'learner-selection-hard-only'),'command':f'{PY} runtime_selection.py'})
print(json.dumps({'package_unchanged':hash_package()==json.loads((E/'package-before.json').read_text()),'runtime_commands':len(logs),'binary_banks':len(valid),'selection':result}))
