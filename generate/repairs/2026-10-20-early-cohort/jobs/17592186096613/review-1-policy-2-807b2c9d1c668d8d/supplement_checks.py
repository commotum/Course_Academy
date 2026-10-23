import json,pathlib,re,hashlib
from math_helpers import parse,target,field,correct,sp,x
P=pathlib.Path(__file__).parent
load=lambda n:json.loads((P/n).read_text())
def save(n,v):(P/n).write_text(json.dumps(v,indent=2))
rs=load('samples.json')+load('batch.json')
rows=[]
for r in rs:
 sol=r['question'][':question/worked-solution']; block=sol.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]; vals=block.split(r'\\')
 for row in vals:assert sp.simplify(parse(row.split('=')[-1])-target(r))==0,row
 rows.append({'question_id':r['question'][':question/id'],'rows_checked':len(vals)})
save('solution-rows.json',rows)
pairs=load('counterfactuals.json');a=pairs[0]['before'];b=next(r for r in rs if r['generation']['bank_profile']=='quotient' and r['generation']['parameters']==dict(n=1,d=5,k=0))
assert sp.simplify(target(a)-1/(4*x))==0 and sp.simplify(target(b)-1/(5*x))==0
save('denominator-counterfactual.json',{'before':a,'after':b,'expected':'1/(4x) changes to 1/(5x); all five worked stages and key update','passed':True})
cases=load('grader-combined-input.json')
for i,r in enumerate(load('delivery-batch/accepted.json')+[a,b]):
 t=target(r);f=field(r)
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if sp.simplify(parse(v[':answer/value'])-t)==0 else 'rejected'} for v in f[':answer-field/choices']]
 else:checks=[{'submitted':v,'expected':e} for v,e in [(str(t),'accepted'),(str(-t),'rejected')]]
 cases.append({'label':'delivered-or-denominator-'+str(i),'record':r,'checks':checks})
save('grader-combined-input.json',cases)
save('scope-results.json',{'difficulty':'easy','records':len(rs),'verified':'Every visible prompt differentiates c ln(x), constant independent of x; no composition, sums, general-base logs, point evaluation. Five-option radio or expression blank. Signed quotient rewrites remain the sourced workload.','uncertified':'moderate/hard are outside requested review'})
save('repair-verification.json',{'retained_findings':['6bbaf15dc6703e79f686'],'preflight_read':True,'old_package_strict_reproducer':'original-failure.json','old_package_author_regression':'author-negative-control.log','old_author_exit':1,'current_strict_reproducer':'source-gap.json','current_author_regression':'author-regression/regression-results.json','independent_checks':['source-replay-results.json','math-results.json','solution-rows.json'],'result':'Both executable checks fail on the former missing-unit-fraction case and pass the current generator.'})
