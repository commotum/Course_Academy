"""Independent tests of changed banks; read-only imports and evidence-only writes.
Run: PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python revision_checks.py
"""
import json,pathlib,sys,importlib.util,collections,subprocess,shutil,hashlib
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';OLD=J/'review-0-policy-2-cf4efc99db03c94a/relocated'
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
def mod(p):
 s=importlib.util.spec_from_file_location('tested',p/'17592186068842.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=mod(P);old=mod(OLD)
# Small focused domain: both new profiles, all four quotient powers, base/slope boundaries.
records=[]
for t in ['simple_quotient','exp_quotient']:
 for n in range(1,5):
  for seed in [0,1]:
   p={'n':n} if t=='simple_quotient' else {'n':n,'base':2 if n%2 else 5,'a':1 if n%2 else 5}
   records.append(m.generate_easy(seed,t,parameters=p))
# Prior exact witnesses (old batch parameters retained, as well as current batch).
records += [m.generate_easy(17,'simple_quotient',parameters={'n':1}),m.generate_easy(2404317989,'exp_quotient',parameters={'base':4,'a':3,'n':4})]
for n in [2,4]:
 for a in [1,5]:records.append(m.generate_easy(61093,'sqrt_quotient',parameters={'n':n,'a':a}))
save('revision-records.json',records)
# New relevant pairs exercise flips of a shared displayed candidate, not just metadata.
pairs=[];labels=[]
for t,seed in [('simple_quotient',0),('exp_quotient',1),('sqrt_quotient',9106)]:
 p={'n':1} if t=='simple_quotient' else {'base':3,'a':2,'n':1} if t=='exp_quotient' else {'a':2,'n':2}
 q={**p,'n':p['n']+1 if t!='sqrt_quotient' else 4}
 pairs += [m.generate_easy(seed,t,parameters=p),m.generate_easy(seed,t,parameters=q)];labels += [t+'/before',t+'/relevant']
# Seed changes only position in a fixed new profile.
pairs += [m.generate_easy(0,'simple_quotient',parameters={'n':1}),m.generate_easy(5,'simple_quotient',parameters={'n':1})];labels += ['irrelevant/before','irrelevant/after']
save('revision-counterfactual-records.json',pairs);save('revision-counterfactual-labels.json',labels)
# Execute author's retained preflight, safely relocated, and demonstrate it fails on old target.
logs=[]
for name,src in [('current',P),('previous',OLD)]:
 dst=R/('preflight-'+name);(dst/'checks').mkdir(parents=True,exist_ok=True);(dst/'evidence').mkdir(exist_ok=True)
 for f in json.load(open(P/'package.json'))['files']:
  (dst/f).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/f if (src/f).exists() else P/f,dst/f)
 for f in ['repair_regression.py','visible_math.py']:shutil.copyfile(P/'checks'/f,dst/'checks'/f)
 cp=subprocess.run([sys.executable,str(dst/'checks/repair_regression.py')],capture_output=True,text=True)
 logs.append({'target':name,'command':[sys.executable,str(dst/'checks/repair_regression.py')],'script_sha256':hashlib.sha256((dst/'checks/repair_regression.py').read_bytes()).hexdigest(),'exit':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
save('retained-regression-verification.json',logs)
assert logs[0]['exit']==0 and logs[1]['exit']!=0
# All supported easy profiles used as delivery inputs, not only the changed subset.
raw=json.load(open(R/'independent-records.json'));easy=[r for r in raw if r['question'][':question/difficulty']==':question.difficulty/easy']+records
save('easy-records.json',easy)
# Complete records for mathematical and native-grader checking; author results are not reused.
ind=json.load(open(R/'independent-records.json'));save('independent-records.json',ind+records+pairs)
save('render-extra.json',records[:2]+[records[8],records[9],records[-4]]+pairs)
(R/'session-state.md').write_text('Source replay rerun: all 10 complete banks match. 33 boundary/fresh records generated. Added 22 focused changed-bank cases, 8 revised counterfactual records. Retained author check runs in relocated evidence copy: fails original target on unique fractionless defect and passes current. Next independent visible math, native grading, delivery, UI, and prompt-blind changed-bank probe.\n')
print('revision records',len(records),'counterfactuals',len(pairs),'retained regression old/current',logs[1]['exit'],logs[0]['exit'])
