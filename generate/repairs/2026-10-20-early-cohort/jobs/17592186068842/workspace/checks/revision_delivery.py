"""Build/check the affected delivery sample and grade new controlled records."""
import collections,json,pathlib,subprocess,sys
sys.dont_write_bytecode=True
from bank_signature_regression import E,ROOT,g,check_group,visible_bank,correct,attack,a
load=lambda p:json.loads(p.read_text())
save=lambda p,v:p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
if len(sys.argv)==1:
 rs=load(E/'regression-records.json')+load(E/'radical-records.json')
 save(E/'delivery-input.json',load(ROOT/'evidence/delivery-input.json')+rs)
 cases=[]
 for i,r in enumerate(rs):
  f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
  cases.append({'label':'same-bank/'+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'Independent visible-equation and solution-stage witness in bank_signature_regression.py'} for c in f[':answer-field/choices']]})
 save(E/'grader-input.json',cases)
 subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(E/'grader-input.json'),str(E/'grader-report.json')],check=True,capture_output=True,text=True)
 print('affected delivery input:',len(load(E/'delivery-input.json')),'records; native additional choices:',len(rs)*5)
else:
 pools={'raw':load(E/'delivery-input.json'),'accepted':load(E/'delivery/accepted.json'),'replacement_batch':load(ROOT/'evidence/delivery-batch/accepted.json')}
 results={}
 for name,rs in pools.items():
  rows=[]
  for t in ('simple_quotient','exp_quotient'):
   sub=[r for r in rs if r['generation']['template']==t]
   profiles=sorted({r['generation']['bank_profile'] for r in sub})
   for profile in profiles:
    group=[r for r in sub if r['generation']['bank_profile']==profile]
    tests={label:sum(attack(r,fn) for r in group) for label,fn in [('modal',a.choose),('shortest_repeated_lhs',a.power_sign_shortest)]}
    assert tests['shortest_repeated_lhs']==0
    assert tests['modal']<len(group) or len(group)==1 # a single chance hit is not a rule
    rows.append({'template':t,'profile':profile,'records':len(group),'attack_successes':tests})
  groups=[]
  if name!='replacement_batch':
   for t,p in [('simple_quotient',{}),('exp_quotient',{'base':2,'a':1}),('exp_quotient',{'base':5,'a':5})]:
    for seed in (0,1):
     wanted=[g.generate_easy(seed,t,parameters={**p,'n':n}) for n in range(1,5)]
     # Match all learner-visible content, not UUIDs rewritten by publication.
     actual=[]
     for w in wanted:
      matches=[r for r in rs if r['question'][':question/problem']==w['question'][':question/problem'] and visible_bank(r)==visible_bank(w)]
      assert matches, 'controlled decision case lost in delivery'
      # Delivery may retain a duplicate from another seed; answer order is irrelevant
      # to the stronger identical-bank / four-different-keys witness.
      actual.append(matches[0])
     assert len({correct(r) for r in actual})==4 and len({tuple(visible_bank(r)) for r in actual})==1
     groups.append({'template':t,'held_fixed':p,'seed':seed,'same_visible_bank':True,'distinct_correct_equations':4})
  radical_groups=[]
  if name!='replacement_batch':
   for coefficient in (1,5):
    wanted=[g.generate_easy(17,'sqrt_quotient',parameters={'a':coefficient,'n':n}) for n in (2,4)]
    actual=[]
    for w in wanted:
     matches=[r for r in rs if r['question'][':question/problem']==w['question'][':question/problem'] and visible_bank(r)==visible_bank(w)]
     assert matches, 'controlled radical target lost in delivery'
     actual.append(matches[0])
    assert len({correct(r) for r in actual})==2 and len({tuple(visible_bank(r)) for r in actual})==1
    radical_groups.append({'a':coefficient,'same_visible_bank':True,'distinct_correct_equations':2})
  results[name]={'records':len(rs),'quotient_probes':rows,'controlled_groups':groups,'radical_controlled_groups':radical_groups}
 save(E/'delivery-shortcuts.json',{'passed':True,'pools':results,'interpretation':'No deterministic rule of the same visible bank identifies which of its four eligible equations is correct. Modal guessing may hit a case by chance; reported per-profile counts include these hits. Uniform guess baseline 1/5; after identifying unseparated row using lesson skill, 1/4.','selection_limits':'Actual delivery uses captured inventory basis only. No live history/weights supplied; prior evidence/delivery-selection.json describes read-only selector analysis. Every retained full four-power group survives; conditional personalized selection was not executed.'})
 print('post-delivery same-bank counterfactuals pass in raw and accepted pools; 6 groups each')
