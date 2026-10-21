from auditlib import *
rs=json.load(open(E/'delivery-easy/accepted.json'))+json.load(open(E/'delivery-moderate/accepted.json'))+json.load(open(E/'delivery-batch/accepted.json'))
cases=[]
for i,r in enumerate(rs):
 f=field(r)
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':correct(r),'expected':'accepted'},{'submitted':'0','expected':'rejected'}]
  if r['generation']['template']!='q-126765':
   _,(_,ordinate)=prompt_data(r);checks.append({'submitted':str(ordinate).replace('**','^').replace('log(','ln(').replace('E','e'),'expected':'rejected','purpose':'Shortcut: copy the printed initial ordinate instead of integrating'})
 cases.append({'label':'delivered '+str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
batch=json.load(open(E/'delivery-batch/accepted.json'));r=next(r for r in batch if r['generation']['template']=='q-126765')
save('sine-minimal-record.json',[r])
strict={'label':'delivered exact-batch sine valid constant shift','record':r,'checks':[{'submitted':'x^2-6*x','expected':'accepted','purpose':'Equivalent sine solution family because C is arbitrary'},{'submitted':'(x-3)^2+1','expected':'accepted','purpose':'Constant shift absorbed into C'}]}
save('delivered-sine-strict-input.json',[strict])
obs=copy.deepcopy(strict)
for c in obs['checks']:c['expected']='rejected';c['purpose']='Observe known defect; strict ACCEPTED assertions remain in delivered-sine-strict-input.json'
cases.append(obs);save('delivered-grader-input.json',cases)
cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'delivered-grader-input.json'),str(E/'delivered-grader-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True);(E/'delivered-grader-console.txt').write_text(p.stdout+p.stderr)
save('delivered-grader-execution.json',{'command':cmd,'exit':p.returncode,'checks':sum(len(c['checks']) for c in cases),'result':'Observation validates ordinary keys/wrongs after actual normalization, and reproduces known rejection of two valid entries; does not establish grading pass.'});assert p.returncode==0,p.stderr
print(p.stdout.strip())
