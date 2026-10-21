import pathlib,json,sys,importlib.util,shutil,subprocess,hashlib,collections
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';O=J/'review-1-policy-2-800c03f7bd804ec6'
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
def mod(p):
 s=importlib.util.spec_from_file_location('tested',p/'17592186068842.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=mod(P)
records=[];groups=[];pairs=[]
# Three visible-bank groups per profile, independent seed and factor extremes.
for t,base in [('simple_quotient',{}),('exp_quotient',{'base':2,'a':1}),('exp_quotient',{'base':5,'a':5}),('sqrt_quotient',{'a':1}),('sqrt_quotient',{'a':5})]:
 for seed in [6021,6022]:
  ns=[2,4] if t=='sqrt_quotient' else list(range(1,5))
  rs=[m.generate_easy(seed,t,parameters={**base,'n':n}) for n in ns]
  fields=[r['question'][':question/answer-fields'][0] for r in rs];banks=[sorted(c[':answer/value'] for c in f[':answer-field/choices']) for f in fields];keys=[next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]) for f in fields]
  assert all(b==banks[0] for b in banks) and len(set(keys))==len(ns)
  groups.append({'template':t,'seed':seed,'fixed':base,'powers':ns,'same_visible_bank':True,'keys':keys,'question_ids':[r['question'][':question/id'] for r in rs]});records+=rs
  if seed==6021:pairs+=rs[:2]
records += [m.generate_easy(17,'simple_quotient',parameters={'n':1}),m.generate_easy(2404317989,'exp_quotient',parameters={'base':4,'a':3,'n':4}),m.generate_easy(2404317989,'exp_quotient',parameters={'base':4,'a':4,'n':4})]
# Irrelevant shuffling controlled while profile is fixed: find a different order.
a=m.generate_easy(6021,'simple_quotient',parameters={'n':2});fa=a['question'][':question/answer-fields'][0]
for seed in range(6023,6035):
 b=m.generate_easy(seed,'simple_quotient',parameters={'n':2});fb=b['question'][':question/answer-fields'][0]
 if b['generation']['bank_profile']==a['generation']['bank_profile'] and fa[':answer-field/choices']!=fb[':answer-field/choices']:break
pairs += [a,b]
save('revision-records.json',records);save('same-bank-groups.json',groups);save('revision-counterfactual-records.json',pairs)
# Author checks run exclusively in evidence copies. Identical test code against
# the precise historical failing runtime and the current runtime.
logs=[]
for name,src in [('current',P),('failure0',J/'review-0-policy-2-cf4efc99db03c94a/relocated'),('failure1',O/'relocated')]:
 dst=R/('preflight-'+name)
 for f in json.loads((P/'package.json').read_text())['files']:
  (dst/f).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/f if (src/f).exists() else P/f,dst/f)
 (dst/'checks').mkdir(exist_ok=True);(dst/'evidence/revision-2/before').mkdir(parents=True,exist_ok=True)
 shutil.copyfile(O/'bank_shortcut.py',dst/'evidence/revision-2/before/bank_shortcut.py')
 for f in ['repair_regression.py','bank_signature_regression.py','visible_math.py','radical_regression.py']:shutil.copyfile(P/'checks'/f,dst/'checks'/f)
 tests=['repair_regression.py','bank_signature_regression.py','radical_regression.py'] if name=='current' else ['repair_regression.py'] if name=='failure0' else ['bank_signature_regression.py','radical_regression.py']
 for f in tests:
  cp=subprocess.run([sys.executable,str(dst/'checks'/f)],text=True,capture_output=True)
  logs.append({'target':name,'script':f,'command':[sys.executable,str(dst/'checks'/f)],'script_sha256':hashlib.sha256((dst/'checks'/f).read_bytes()).hexdigest(),'exit':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
  save('retained-regression-verification.json',logs)
assert all(l['exit']==0 if l['target']=='current' else l['exit']!=0 for l in logs)
print('Retained tests: current pass; corresponding historical runtimes fail.',[(l['target'],l['script'],l['exit']) for l in logs])
# Keep just current cases plus a small unchanged regression sample from review.py.
ind=json.load(open(R/'independent-records.json'));save('independent-records.json',ind+records+pairs)
save('easy-records.json',[r for r in ind if r['question'][':question/difficulty']==':question.difficulty/easy']+records)
save('render-extra.json',pairs+records[-3:])
(R/'session-state.md').write_text('All ten captured complete source banks replay. Focused same-bank groups pass for quotient powers 1–4 and radical powers 2/4. Author retained tests pass current and fail precise historical defective runtimes; independent visible math, native grader, delivery and UI pending.\n')
