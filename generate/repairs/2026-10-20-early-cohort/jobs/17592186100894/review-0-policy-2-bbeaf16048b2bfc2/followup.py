from auditlib import *
import uuid,collections
samples=json.load(open(E/'samples.json'));batch=json.load(open(E/'batch.json'));excluded=json.load(open(E/'excluded-records.json'))
before=next(r for r in samples if r['generation']['template']=='q-355546' and r['generation']['parameters']['h']==1)
after=copy.deepcopy(before)
after['question'][':question/problem']=after['question'][':question/problem'].replace('y(2)=6','y(2)=7')
f=field(after);f[':answer-field/choices'][0][':answer/value']=correct(before).replace('+7','+8')
assert correct(after)!=correct(before)
after['question'][':question/worked-solution']=r'''Separating the variables and integrating gives

$$y=\int\left(\frac{5}{(x-1)^2}+8(x-1)\right)\,\mathrm{d}x=-\frac{5}{x-1}+4(x-1)^2+C.$$

Apply $y(2)=7$: $-5+4+C=7$, so $C=8$. Thus

$$y=-\frac{5}{x-1}+4(x-1)^2+8.$$'''
after['question'][':question/id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'review-y0-counterfactual'))
after['generation']['review_counterfactual']='Same ODE, h=1 and initial x=2; initial y changed from 6 to 7. Independent review fixture, not package output.'
irrelevant=copy.deepcopy(before);irrelevant['question'][':question/problem']=irrelevant['question'][':question/problem'].replace('Find the particular solution','Determine the particular solution');irrelevant['generation']['review_counterfactual']='Wording-only change; same ODE and IVP.'
# Position permutation with UUID/key preserved tests real grader independently from values.
radio=next(r for r in samples if r['generation']['template']=='q-104064' and r['generation']['parameters']['h']==1);permuted=copy.deepcopy(radio);field(permuted)[':answer-field/choices'].reverse();permuted['generation']['review_counterfactual']='Choice order reversed with identity and key preserved.'
cf=[before,after,irrelevant,radio,permuted];save('counterfactual-records.json',cf)
checks=[]
for label,r in [('before',before),('relevant changed IC',after),('irrelevant wording',irrelevant)]:
 own=correct(r);other=correct(after) if label!='relevant changed IC' else correct(before)
 checks.append({'label':label,'record':r,'checks':[{'submitted':own,'expected':'accepted','purpose':'independently derived antiderivative with IC constant'},{'submitted':other,'expected':'rejected','purpose':'same derivative but wrong initial value'},{'submitted':'0','expected':'rejected','purpose':'plausible constant wrong answer'}]})
for label,r in [('radio before',radio),('radio permuted',permuted)]:
 checks.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field(r)[':answer-field/correct'][1] else 'rejected','purpose':'choice identity tracks mathematical key after irrelevant permutation'} for a in field(r)[':answer-field/choices']]})
# Every sampled source profile once, every exact batch item, and all four excluded profiles.
for r in [*samples[1::3],*batch,*excluded]:
 f=field(r);cases=[]
 if f[':answer-field/type'].endswith('/radio'):
  cases=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete independently checked bank'} for a in f[':answer-field/choices']]
 else:
  v=correct(r);cases=[{'submitted':v,'expected':'accepted','purpose':'canonical expression'},{'submitted':'('+v+')+0','expected':'accepted','purpose':'valid neutral-term equivalent'},{'submitted':'0','expected':'rejected','purpose':'strict wrong constant rejection; excludes engine capability workarounds'},{'submitted':v+'+1','expected':'rejected','purpose':'nearby wrong expression'}]
 checks.append({'label':r['generation']['template']+' h='+str(r['generation']['parameters']['h'])+' id='+r['question'][':question/id'],'record':r,'checks':cases})
save('grader-input.json',checks)
save('counterfactual-math.json',[math_check(r) for r in cf[:3]])
# Render source family representatives, exact batch, controlled pairs and the restored denominator.
render=batch+cf+[next(r for r in samples if r['generation']['template']=='q-355560')]
save('render-records.json',render)
save('inventory-audit.json',{'basis':5372,'question_count':len(json.load(open(JOB/'source/inventory.json'))['questions']),'generated_question_count':sum(1 for q in json.load(open(JOB/'source/inventory.json'))['questions'] if ':question/generation' in q or ':question/generator' in q),'all_inventory_question_ids_are_source_ids':set(q[':question/id'] for q in json.load(open(JOB/'source/inventory.json'))['questions'])==set(q[':question/id'] for q in json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']),'conclusion':'All 26 captured inventory records are original source records. No stored generated records exist in this captured bank; none are relabeled as generated. This is a verified absence at the captured basis, not a claim about later database state.'})
save('affected-inventory.json',{'affected_questions':[]})
print('grader cases',len(checks),'responses',sum(len(c['checks']) for c in checks),'render records',len(render))
