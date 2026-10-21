import runpy
x=runpy.run_path('inventory-audit.py')
g=x['g'];save=x['save'];load=x['load'];info=x['info'];E=x['E'];J=x['J'];P=x['P'];num=x['num'];samples=x['samples'];batch=x['batch'];cf=x['cf']
import math,re,json,hashlib,collections
p=dict(ambient=10,initial=50,observed=40,target=30,time=5)
mc=[g.generate('moderate',84179,'bath',parameters=p),g.generate('moderate',84179,'bath',parameters={**p,'target':25})]
cf=cf+mc;save('counterfactual-records.json',cf);save('render-counterfactuals.json',cf)
c=load(E/'counterfactual-results.json');c['target']={'change':'Hold ambient, initial and observed temperatures and observation time fixed; target30 ->25','before':info(mc[0]),'after':info(mc[1]),'expected':[12,17],'passed':[info(r)['answer'] for r in mc]==[12,17]};save('counterfactual-results.json',c)
cases=load(E/'grader-input.json')
for r in mc:
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 cases.append({'label':'target counterfactual','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'independent logarithmic target-time computation or distractor'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases)
# Solution and prompt dependency checks independent of generation metadata.
checks=[]
for r in samples+batch+cf:
 s=r['question'][':question/problem'];sol=r['question'][':question/worked-solution'];ans=info(r)['answer'];level=r['question'][':question/difficulty'].split('/')[-1]
 if level=='easy':
  k,A=re.search(r'=-([\d.]+)\(T-(\d+)\)',s).groups();A=int(A);I=int(re.search(r'initial temperature.*?\$\{(\d+)',s).group(1));t=int(re.search(r'after \$(\d+)\$ minutes',s).group(1));D=I-A
  expected=math.floor(A+D*math.exp(-float(k)*t)+.5)
  deps=[f'K & ={D}',f'T(t)={A}+{D}{{e}}^{{-{k}t}}',f'T({t})={A}+{D}{{e}}^{{-{k}\\cdot {t}}}',f'≈{{{expected}}}']
 else:
  vs=[int(v) for v in re.findall(r'\$\{(\d+)\}\^\{∘\}[CF]',s)]
  if r['generation']['template']=='tea':I,O,Z,A=vs[:4]
  else:I,A,O,Z=vs[:4]
  t=int(re.search(r'After \$(\d+)\$ minutes',s).group(1));D=I-A;expected=math.floor(t*math.log((Z-A)/D)/math.log((O-A)/D)+.5)
  deps=[f'K & ={D}',f'T(t)={A}+{D}{{e}}^{{-kt}}',f'T({t})={O}',f'T({{t}}_{{1}}) & ={Z}',f'≈{expected}']
 checks.append({'id':info(r)['id'],'expected':expected,'stored':ans,'dependency_fragments':deps,'passed':expected==ans and all(d in sol for d in deps)})
save('solution-dependencies.json',checks)
# Delivered cohorts, plus selection using Rust's exact stable band draw.
def recs_inv():
 inv=load(J/'source/inventory.json');return [{'question':q} for q in inv['questions']]
sets={'raw_easy':[r for r in samples if r['question'][':question/difficulty'].endswith('/easy')],'delivered_easy':load(E/'delivery-fresh/accepted.json'),'raw_batch':batch,'delivered_batch':load(E/'delivery-batch/accepted.json')}
stages={n:{'count':len(rs),'median_success':sum(info(r)['rank']==3 for r in rs),'templates':dict(collections.Counter(r['generation']['template'] for r in rs))} for n,rs in sets.items()}
inv=recs_inv();bandinfo={}
for band in ['easy','moderate','hard']:
 rs=[r for r in inv if r['question'][':question/difficulty'][':db/ident'].endswith('/'+band)];bandinfo[band]={'count':len(rs),'rank_strategy_correct':sum(info(r)['rank']==(3 if band=='easy' else 4) for r in rs),'strategy':'median' if band=='easy' else 'second-largest'}
# Conditional on easy being drawn, each actual candidate has equal probability.
# Exercise deterministic selection and seen-prefix removal on captured entity IDs.
easy=sorted([q for q in load(J/'source/inventory.json')['questions'] if q[':question/difficulty'][':db/ident'].endswith('/easy')],key=lambda q:q[':db/id']); draws=[]
for i in range(12):
 digest=hashlib.sha256(f'course-academy/question-selection/v1/independent-{i}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 pool=easy if i<6 else easy[1:];q=pool[int(u*len(pool))];draws.append({'seed':f'independent-{i}','conditional_band':'easy','seen_exclusion':[] if i<6 else [easy[0][':db/id']],'selected_entity':q[':db/id'],'selected_question':q[':question/id']})
save('delivery-selection.json',{'stages':stages,'inventory_basis':5392,'captured_inventory_bands':bandinfo,'selection_rule':'question_selection.rs select: sorted unique fresh IDs; difficulty band chosen by positive weights then uniform within band; unknown fallback only when no weighted rated band remains; previous tasks excluded by seen_before_task and prefix by caller.','conditional_selection_reproduction':draws,'new_batch_selection':'Every nonempty subset of the five newly accepted easy records remains 100% median-answerable, regardless of IDs or selection seed.','resampling':'Whole bank collision/domain validation rejects the entire instance up to 1000 times, after the template is selected. Conditional on acceptance the two-below/two-above invariant cannot change.','limitations':['No live learner history or policy weights supplied; these are conditional eligible-band conclusions, not a prediction of a named learner session.','Preparation file absent; helper uses actual shared prepare_records against captured basis5392. Future inventory changes can alter deduplication.'],'difficulty_negative_test':'Mixed easy/moderate fresh-samples input rejected by actual check_delivery before prepare_records; requested easy subset accepted50/50.'})
save('review-summary-data.json',{'solution_checks':len(checks),'solution_failures':[z for z in checks if not z['passed']],'cf':[info(r) for r in cf],'delivery':stages})
print('Supplemental math failures:',[z for z in checks if not z['passed']])
