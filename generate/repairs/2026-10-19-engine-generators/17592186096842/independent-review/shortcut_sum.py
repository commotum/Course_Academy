from audit import *
import copy
records=[];checks=[];probe=[]
for i in range(20):
 a=[-8,-6,6,8][i%4];t=[-4,-3,3,4][(i//4)%4];r=[3,5][i%2];k=[-2,-1,1,2][(i//5)%4];p={'a':a,'b':r*r-a*t,'t':t,'k':k}
 rec=g.generate('easy',seed=958113+i,template='slope_sum_radio',parameters=p,bank_role=i%5);records.append(rec)
 cubic=s.Integer(3*k*t*t);opts=field(rec)[':answer-field/choices'];pick=min(opts,key=lambda a:abs(untex(a[':answer/value'])-cubic));good=pick[':answer/id']==field(rec)[':answer-field/correct'][1]
 probe.append({'seed':958113+i,'parameters':p,'bank_role':i%5,'cubic_derivative_only':str(cubic),'chosen':pick[':answer/value'],'correct':good,'prompt':rec['question'][':question/problem'],'choices':opts})
 checks.append({'label':'sum shortcut seed '+str(958113+i),'record':rec,'checks':[{'submitted_answer_id':pick[':answer/id'],'expected':'accepted','purpose':'choose numeric option closest to cubic derivative only; never differentiate radical'}]})
save('sum-shortcut-records.json',records);save('sum-shortcut-results.json',{'strategy':'Compute only 3*k*t^2; choose numeric option nearest it. Do not differentiate the radical.','recognizable_subgroup':'slope_sum_radio with |t|>=3 and radicand at t>=9','baseline':.2,'correct':sum(p['correct'] for p in probe),'total':len(probe),'cases':probe,'why_reliable':'A=C+delta with C=3kt^2, delta=a/(2r), r>=3, |t|>=3, |a|<=8. Distractor spacing |A/a|; |delta| < |A/a|/2 because a^2/r<=64/3 while |A|>=27-8/6. Thus the correct option is uniquely closest to C for every eligible role 0..4 in this subgroup. The strategy uses a prerequisite cubic derivative and magnitude comparison, bypassing the radical chain-rule operation.'});save('sum-shortcut-grader-input.json',checks)
save('sum-shortcut-render.json',[records[0],records[-1]])
