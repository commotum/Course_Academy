from auditlib import *
from collections import Counter

def probe(r):
 if r['generation']['template']!='q-104065':return None
 # Read visible IC and bank; no generator parameter a/c or key used to predict.
 _,(_,ordinate)=prompt_data(r)
 pure=simplify(ordinate/S.pi**2).is_Rational is True
 opts=field(r)[':answer-field/choices'];h=r['generation']['parameters']['h']
 coeffs=[S.expand(explicit(r,a[':answer/value'])-S.log(S.sin(x-h))).coeff(x,2) for a in opts]
 repeated=[v for v,n in Counter(coeffs).items() if n>1]
 eligible=pure and len(repeated)==1
 predicted=None
 if eligible:
  ids=[i for i,v in enumerate(coeffs) if v==repeated[0]]
  lens=[len(opts[i][':answer/value']) for i in ids]
  shortest=[i for i in ids if len(opts[i][':answer/value'])==min(lens)]
  if len(shortest)==1:predicted=opts[shortest[0]][':answer/id']
 return {'question_id':r['question'][':question/id'],'visible_initial_ordinate':str(ordinate),'coefficients':list(map(str,coeffs)),'eligible':eligible,'predicted_id':predicted,'correct':predicted==field(r)[':answer-field/correct'][1] if eligible else None}

stages={};witnesses=[]
for label,path in [('raw','samples.json'),('delivered','delivery-easy/accepted.json'),('batch_raw','batch.json'),('batch_delivered','delivery-batch/accepted.json')]:
 rs=json.load(open(E/path));out=[p for r in rs if (p:=probe(r)) is not None]
 stages[label]={'total_records':len(rs),'trig':len(out),'qualifying':sum(p['eligible'] for p in out),'correct':sum(bool(p['correct']) for p in out),'cases':out}
 if label=='raw':witnesses=[r for r in rs if (p:=probe(r)) and p['eligible']]
save('conditional-shortcut-records.json',witnesses)
minimal=next(r for r in witnesses if r['generation']['seed']==492800)
save('minimal-failure.json',[minimal])
save('conditional-shortcut-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python conditional-shortcut.py','strategy':'When the initial ordinate is a pure rational multiple of pi² (including 0) and exactly one quadratic coefficient is repeated in the answer bank, select the shortest option among those with that repeated coefficient. This uses visible expression shape and repetitions, without integration, differentiation, or substituting the initial point.','baseline':0.2,'stages':stages,'minimal':{'seed':492800,'template':'q-104065','parameters':{'h':1,'a':4,'c':'0'},'record':'minimal-failure.json'},'construction_proof':'Bank starts with two coefficient-a expressions, constants c and c+nonzero integer delta. Remaining pool may add more coefficient-a choices but has constants c+nonzero integers. Every other coefficient is singleton when the observable subgroup condition holds. Pure pi² initial ordinate forces c in {-pi²,0,pi²}; the c expression has no standalone rational offset and is strictly shorter than every c+nonzero integer option with the same coefficient. Thus the rule always selects the key within this recognizable subgroup. This identifies bank construction, not a calculus simplification.','native_grading':'All five complete witness records were included in grader-input.json, all choices tested. Predicted UUID is accepted; four alternatives rejected.','ui_order':'Shape and coefficient multiplicity survive ui/learning.js choiceOrder, so positional shuffling does not remove the cue.','batch_conclusion':'No q-104065 record occurs in the exact batch. This demonstrated generator defect is not asserted as an actual-batch shortcut.'})
render=json.load(open(E/'render-counterfactual-records.json'));render.append(minimal);save('render-counterfactual-records.json',render)
print({k:(v['correct'],v['qualifying'],v['trig']) for k,v in stages.items()})
