import sys,json,importlib.util,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;JOB=OUT.parent;PY='/home/jake/Developer/Course_Academy/.venv/bin/python'
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2)+'\n')
c=load(OUT/'staged-package/checks/repair_checks.py','author_checks')
old=load(JOB/'review-0-policy-2-0c69632c0ac42ce3/relocated/17592186078583.py','old')
cur=load(JOB/'workspace/17592186078583.py','cur')
results=[];witnesses=[]
for label,g in [('old',old),('current',cur)]:
 try:r=g.generate('easy',90271,template='q-106877',profile='q-106877',parameters={'S':70});cake='Fahrenheit' in r['question'][':question/problem']
 except Exception as e:cake=False;err=str(e)
 r=g.generate('moderate',92601,template='q-106883');witnesses.append(r)
 shortest=c.shortest_correct(r)
 # Exact retained predicate is absence of the unique-shortest answer cue.
 cue_pass=not shortest;cue_error='Exact shortest counterexample persists' if shortest else None
 results.append({'generator':label,'cake_acceptance':cake,'cake_error':err if not cake else None,'turkey_parameters':r['generation']['parameters'],'unique_shortest_correct':shortest,'author_cue_check_pass':cue_pass,'cue_error':cue_error if not cue_pass else None})
assert results[0]['cake_acceptance'] is False and results[0]['unique_shortest_correct'] is True
assert results[1]['cake_acceptance'] is True and results[1]['unique_shortest_correct'] is False
# cue_summary additionally needs more than one position: run with independent controls to avoid singleton-only rejection.
for label,g in [('old',old),('current',cur)]:
 rows=[g.generate('moderate',seed,template='q-106883') for seed in range(92601,92609)]
 try:v=c.cue_summary(rows);passed=True;detail=v
 except AssertionError as e:passed=False;detail=str(e)
 results.append({'generator':label,'author_conditional_check_8_seeds_pass':passed,'detail':detail})
assert not results[-2]['author_conditional_check_8_seeds_pass'] and results[-1]['author_conditional_check_8_seeds_pass']
save('retained-finding-verification.json',{'commands':[PY+' regression_verification.py',PY+' staged-package/checks/repair_checks.py'],'preflight_claim':'passed: source_banks=10, sample_records=85, counterfactuals=25; independently rerun on byte-identical staged copy','results':results})
save('retained-witness-records.json',witnesses)
# Fresh controlled cases: relevant ambient and irrelevant initial changes in changed moderate banks, plus restored cake.
cf=[];summary=[]
for level,t,p in [('easy','q-106877',{'S':64}),('moderate','q-106883',{'S':64,'I':159}),('moderate','q-106934',{'S':64,'I':181})]:
 a=cur.generate(level,107071,template=t,parameters=p);b=cur.generate(level,107071,template=t,parameters={**p,'S':p['S']+1});rows=[a,b]
 def value(r):
  f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 assert value(a)!=value(b) and a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
 item={'template':t,'relevant_response_changed':True,'relevant_solution_changed':True}
 if 'I'in p:
  ccc=cur.generate(level,107071,template=t,parameters={**p,'I':p['I']+1});rows.append(ccc);assert value(a)==value(ccc) and a['question'][':question/worked-solution']==ccc['question'][':question/worked-solution'];item['irrelevant_response_and_solution_preserved']=True
 cf.extend(rows);summary.append(item)
save('changed-counterfactual-records.json',cf);save('changed-counterfactual-results.json',summary)
# Exercise unmodified acceptance scripts with exact original parameters.
for case in ['cake','shortest']:
 x=subprocess.run([PY,str(OUT/'reproduce_failures.py'),case],text=True,capture_output=True);(OUT/f'retained-{case}.txt').write_text(x.stdout+x.stderr);assert x.returncode==0
print(json.dumps(results))
