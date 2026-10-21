import sys,json,pathlib,copy,subprocess,hashlib,collections,platform,shutil
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;B=E.parent;W=B/'workspace';sys.path.insert(0,str(W));import generator as g
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_publish import stable_identities
# Import helpers without rerunning audit.
# Parse prompt/banks independently again.
import re,itertools
def matrix(t):return [[int(v.strip()) for v in row.split('&')] for row in re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S)[1].split('\\\\')]
def coords(t):return [[int(a)-1,int(b)-1] for a,b in re.findall(r'a\}?_\{([1-4])([1-4])\}',t)]
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
source=json.load(open(E/'source-replay.json'));p=copy.deepcopy(source[0]['parameters']);p['bank'][0]=[[0,1]]+p['bank'][0]
try:g.generate('moderate',8801,parameters=p);error='ACCEPTED'
except ValueError as ex:error=str(ex)
save('nonminimum-case.json',{'basis_source_id':source[0]['source_id'],'seed':8801,'parameters':p,'sole_valid_offered_choice':0,'source_rule_expected':'accepted, a12+a21+a43 produces REF; global minimality is not required','actual_error':error})
# Reproduce captured non-source questions using explicit parameters; no original seed assertion.
s=json.load(open(B/'source/source.json'));ids={q[':question/id'] for q in s['material']['kp'][':knowledge-point/questions']};inv=json.load(open(B/'source/inventory.json'));reproduced=[];affected=[];status=[];attempted=[]
for q in inv['questions']:
 if q[':question/id'] in ids:continue
 p={'matrix':matrix(q[':question/problem']),'bank':[coords(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]}
 try:r=g.generate('moderate',0,parameters=p)
 except ValueError as ex:status.append({'id':q[':question/id'],'error':str(ex)});continue
 r['question']=stable_identities(r['question'],g.KP_UUID)
 attempted.append(r)
 match=r['question'][':question/id']==q[':question/id'];status.append({'id':q[':question/id'],'reproduced_id':r['question'][':question/id'],'identity_matches':match,'captured_original_seed':'absent; seed=0 with exact explicit captured parameters','prompt_matches':q[':question/problem']==r['question'][':question/problem'],'solution_matches':q[':question/worked-solution']==r['question'][':question/worked-solution']})
 if match:
  reproduced.append(r);affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Prompt adds global fewest-replacements optimization absent from source operation-selection task.','reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python focused.py (generate moderate, seed=0, explicit captured matrix and bank)','evidence_path':'generated-records.json'})
save('inventory-attempt-records.json',attempted);save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':affected});save('inventory-reproduction.json',{'basis':inv['basis'],'non_source_questions':status,'source_originals_excluded':len(ids),'limits':'All 20 captured prompts inspected; 5 non-source identities reconstructed using explicit parameters. Captured inventory does not contain historical generation metadata, so original seeds are unknown; current generation metadata records seed=0 and exact explicit parameters. No claim about later inventory.'})
# Package relocation under evidence with pycache disabled.
rel=E/'relocated';rel.mkdir(exist_ok=True)
for n in ['generator.py','catalogue.json','math_format.py','package.json']:shutil.copyfile(W/n,rel/n)
a=subprocess.run([sys.executable,str(W/'generator.py'),'--difficulty','moderate','--seed','702311','--count','5'],capture_output=True,text=True)
b=subprocess.run([sys.executable,str(rel/'generator.py'),'--difficulty','moderate','--seed','702311','--count','5'],capture_output=True,text=True,cwd=E)
save('cli-records.json',json.loads(a.stdout));tests=[]
for args in [['--difficulty','easy'],['--difficulty','moderate','--count','0']]:
 r=subprocess.run([sys.executable,str(W/'generator.py')]+args,capture_output=True,text=True);tests.append({'args':args,'exit_code':r.returncode,'stderr':r.stderr})
save('packaging-results.json',{'python_actual':platform.python_version(),'python_declared':json.load(open(W/'package.json'))['dependencies']['python'],'runtime_packages':{},'relocation_identical':a.returncode==b.returncode==0 and json.loads(a.stdout)==json.loads(b.stdout),'cli_replay_identical':json.loads(a.stdout)[0]==json.load(open(E/'independent-samples.json'))[0],'invalid_cli_cases':tests,'external_outputs':'stdout JSON only; no assets, catalogue resolved by __file__, no package writes','hashes_unchanged':json.load(open(E/'package-before.json'))=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()}})
print(json.dumps({'nonminimum_case_error':error,'inventory_reproduced':len(reproduced),'inventory_status':status,'packaging':json.load(open(E/'packaging-results.json'))}))
