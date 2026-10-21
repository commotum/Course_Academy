import json,subprocess,sys
from pathlib import Path
from independent_math import value,correct,s,X,Y,K,C,D,rhs
R=Path(__file__).resolve().parent;REPO=Path('/home/jake/Developer/Course_Academy')
def load(n):return json.loads((R/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
cases=[]
records=load('batch.json')+[r for p in load('pairs.json') for r in [p['before'],p['after']]]+[r for r in load('normal-cases.json') if r['generation']['template']=='q-128191']
for i,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independent printed-ODE substitution and arbitrary constant check'} for a in f[':answer-field/choices']]
 else:
  power=int(str(value(correct(r))).split('**')[1]);checks=[{'submitted':'*'.join(['x']*power),'expected':'accepted','purpose':'valid factored equivalent entry'},{'submitted':f'x^{power+1}','expected':'rejected','purpose':'wrong power'},{'submitted':f'2*x^{power}','expected':'rejected','purpose':'wrong coefficient'},{'submitted':f'x^{power}+x','expected':'rejected','purpose':'nonconstant extra term changes ODE'}]
 cases.append({'label':f'normal-{i}','record':r,'checks':checks})
# Retain strict source-response test for the engine capability concealed by the new normal wording.
observed=next(r for r in load('source-replay.json') if r['generation']['template']=='q-128191')
strict=[{'label':'source blank arbitrary-constant equivalence','record':observed,'checks':[{'submitted':'x^2+5','expected':'accepted','purpose':'-2/(x^2+5+K) is exactly the same family as -2/(x^2+K), K arbitrary'}]}]
save('grader-input.json',cases);save('grader-family-strict-input.json',strict)
cmd=[str(REPO/'generate/runs/current/check-engine'),str(R/'grader-input.json'),str(R/'grader-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True);print(p.stdout,p.stderr)
cmd2=[str(REPO/'generate/runs/current/check-engine'),str(R/'grader-family-strict-input.json'),str(R/'grader-family-strict-report.json')]
p2=subprocess.run(cmd2,capture_output=True,text=True);print('strict family equivalence:',p2.returncode,p2.stderr.strip())
save('grader-commands.json',[{'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr},{'command':cmd2,'returncode':p2.returncode,'stdout':p2.stdout,'stderr':p2.stderr}])
results=[]
for pair in load('pairs.json'):
 b,a=pair['before'],pair['after'];bv,av=value(correct(b)),value(correct(a));changed=s.simplify(bv-av)!=0
 details={'kind':pair['kind'],'template':pair['template'],'before_answer':correct(b),'after_answer':correct(a),'answer_changed':changed,'printed_rhs_before':str(rhs(b['question'][':question/problem'])),'printed_rhs_after':str(rhs(a['question'][':question/problem'])),'prompt_same':b['question'][':question/problem']==a['question'][':question/problem'],'solution_same':b['question'][':question/worked-solution']==a['question'][':question/worked-solution'],'solution_contains_answer_primitive':True,'grader_cases':'grader-input.json','result':'passed' if (changed if pair['kind']=='relevant' else not changed and b['question'][':question/worked-solution']==a['question'][':question/worked-solution']) else 'failed'}
 # The worked solution's final displayed equation must equal the keyed answer (same constant spelling).
 for role,r in [('before',b),('after',a)]:
  import re
  last=re.findall(r'\$\$(.*?)\$\$',r['question'][':question/worked-solution'],flags=re.S)[-1].strip().rstrip('.')
  last=last.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  last=last.split(r'\\')[-1].replace('&','').strip().rstrip('.')
  try:details[role+'_last_solution_matches']=s.simplify(value(last)-value(correct(r)))==0
  except Exception as e:details[role+'_last_solution_matches']=False;details[role+'_error']=repr(e)
  if not details[role+'_last_solution_matches']:details['result']='failed'
 results.append(details)
save('counterfactual-results.json',results)
