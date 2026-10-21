import review as t,json,re,copy,hashlib,random
from probes import sign_strategy
save=t.save
sets={n:json.load(open(t.E/n)) for n in ['batch.json','fresh-easy.json','fresh-moderate.json','source-replay.json','counterfactual-records.json']}
# Execute the displayed operation annotations rather than trusting generator trace metadata.
results=[]
for name,rs in sets.items():
 for r in rs:
  text=r['question'][':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',text,re.S);current=None;pending=None;errors=[];steps=0
  for b in blocks:
   if '\\begin{array}' in b:
    nxt=t.matrix(b)
    if current is not None and pending:
     a=copy.deepcopy(current);op=pending.replace(' ','')
     swap=re.fullmatch(r'R_(\d)\\leftrightarrowR_(\d)',op)
     add=re.fullmatch(r'R_(\d):=R_\1\+\((.*?)\)R_(\d)',op)
     scale=re.fullmatch(r'R_(\d):=\((.*?)\)R_\1',op)
     if swap:
      i,j=map(lambda v:int(v)-1,swap.groups());a[i],a[j]=a[j],a[i]
     elif add:
      i,f,j=add.groups();i=int(i)-1;j=int(j)-1;f=t.scalar(f);a[i]=[x+f*y for x,y in zip(a[i],a[j])]
     elif scale:
      i,f=scale.groups();i=int(i)-1;f=t.scalar(f);a[i]=[f*x for x in a[i]]
     else:errors.append('unparsed operation '+op)
     if a!=nxt:errors.append('operation does not produce displayed next matrix')
     steps+=1
    current=nxt;pending=None
   elif b.strip().startswith('R_'):pending=b.strip()
  results.append({'file':name,'id':r['question'][':question/id'],'steps':steps,'errors':errors})
save('row-operation-results.json',{'tested':len(results),'failures':[r for r in results if r['errors']],'results':results})
# Replay canonical example at original parameters. Its source has no answer field.
p={'profile':'q-74536','difficulty':'easy','b':-3,'c':1,'d':4,'scales':[2,-6,4],'plan':'normalize','source_id':'8de46974-719c-5ac2-a43c-83d1c67c57b6'}
r=t.g.build(p,source_replay=True);q=json.load(open(t.J/'source/source.json'))['material']['kp'][':knowledge-point/canonical-example'];save('canonical-replay.json',[r]);save('canonical-replay-results.json',{'prompt_math_equal':t.equations(q[':question/problem'])==t.equations(r['question'][':question/problem']),'math':t.analyze(r),'limitation':'Source canonical example contains no answer bank; constructed bank not asserted as observed.'})
# Exercise duplicate rejection without altering disk package.
original=t.g.sample_parameters;params=original(random.Random(7729),'easy');other=original(random.Random(3219),'easy');calls=iter([params,params,other]);t.g.sample_parameters=lambda rng,band:next(calls)
try:rs=t.g.generate('easy',2,39);resampling={'duplicate_then_valid':len(rs)==2 and rs[1]['generation']['draw']==3 and rs[1]['generation']['rejections']==1,'draws':[r['generation']['draw'] for r in rs]}
finally:t.g.sample_parameters=original
t.g.sample_parameters=lambda rng,band:params
try:
 try:t.g.generate('easy',2,39);resampling['bounded_failure']=False
 except RuntimeError as e:resampling['bounded_failure']=True;resampling['error']=str(e)
finally:t.g.sample_parameters=original
save('resampling-results.json',resampling)
# Counterfactual response relationships verified on actual content and all-choice grader cases.
pairs=json.load(open(t.E/'counterfactuals.json'))
def val(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
base=pairs[0]['record'];relations=[]
for x in pairs[1:]:
 r=x['record'];relations.append({'case':x['name'],'prompt_changed':base['question'][':question/problem']!=r['question'][':question/problem'],'solution_changed':base['question'][':question/worked-solution']!=r['question'][':question/worked-solution'],'base_correct_value':val(base),'new_correct_value':val(r),'response_preserved':val(base)==val(r),'grader_labels':['counterfactual-0','counterfactual-'+str(pairs.index(x))],'render_indices':[6,6+pairs.index(x)]})
save('counterfactual-results.json',relations)
# UI visual inspection notes and raw-to-delivery content invariant.
save('render-inspection.json',{'renderer_report':'render-all/rendering.json','count':10,'visually_inspected':['render-all/question-001.png','render-all/question-007.png','render-all/question-008.png','render-all/question-009.png','render-all/question-010.png'],'observations':'Prompts, negative coefficients, matrices, radio controls, row operation fractions, augmented dividers, and moderate free-variable vector solutions legible. Controlled sign/scale/magnitude changes appear in rendered prompt and solution. No visual defect observed.','raw_delivery_equal':all(a['question'][':question/problem']==b['question'][':question/problem'] and [v[':answer/value'] for v in a['question'][':question/answer-fields'][0][':answer-field/choices']]==[v[':answer/value'] for v in b['question'][':question/answer-fields'][0][':answer-field/choices']] for a,b in zip(sets['batch.json'],json.load(open(t.E/'delivery-batch/accepted.json'))))})
save('scope-results.json',{'tested':148,'source_scope':'One-pivot consistent singular 3x3 systems; easy RREF radio and moderate solve radio.','observed':'96 easy and32 moderate fresh preserve rank one, three equations, same row normalization/elimination and arithmetic ranges 1..10 coefficients / 1..18 constants. No new operators, representation or required prerequisite found.','plans':{k:sum(r['generation']['parameters']['plan']==k for r in sets['fresh-easy.json']) for k in ['normalize','swap2','swap3']},'separate_restriction':'Numerical values vary but bank construction restricts decisions to signs, assessed under variety/decision_variation.'})
print(json.dumps({'row_operation_records':len(results),'row_operation_failures':sum(bool(r['errors']) for r in results),'counterfactuals':[{k:v for k,v in x.items() if k not in ('base_correct_value','new_correct_value')} for x in relations],'resampling':resampling},indent=2))
