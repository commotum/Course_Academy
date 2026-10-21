import sys,json,pathlib,collections,random,re,hashlib,shutil
sys.dont_write_bytecode=True
import math_helper as v
R=v.R;g=v.g;s=v.s;W=v.W
write=v.write
samples=json.load(open(R/'samples.json'));batch=json.load(open(R/'runner-batch.json'))
# Strict printed-solution comparison to original sources, with only documented corrections.
source_report=[]
for q,r in zip(json.load(open(R/'source-cases.json')),json.load(open(R/'source-replays.json'))):
 raw=q[':question/worked-solution'];sid=q.get(':question/math-academy-id')
 if sid=='q-74695':raw=raw.replace('x+ky=2','x+ky=-2').replace('x+ky &=2','x+ky &=-2')
 if sid=='q-42021':raw=raw.replace('1 & 2 & -3','1 & 2 & 3').replace('1-2y=3','x+2y=3').replace('1-2y &=3','x+2y &=3')
 if sid=='q-74691':raw=raw.replace('2x+2y=4','2x-2y=4').replace('$y$,.','$y$.')
 raw=g.normalize_prose(raw)
 raw=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',lambda m:g.matrix([[t.strip() for t in row.split('&')] for row in m[1].split(r'\\')]),raw,flags=re.S)
 def wording(z):return re.sub(r'\s+','',g.normalize_system_braces(z)).replace('&','')
 # Canonical generic "as follows" punctuation differs; record rather than hide it.
 matched=wording(raw)==wording(r['question'][':question/worked-solution'])
 source_report.append({'source_id':q[':question/id'],'profile':sid,'solution_wording_matches':matched,'canonical_punctuation_only':sid=='e-4712' and wording(raw).replace('formasfollows','form,asfollows')==wording(r['question'][':question/worked-solution'])})
write('solution-fidelity.json',source_report)
# Explicit zero roots in each affected family, with and without an observed bank.
boundaries=[]
for level,t,p,profile in [('moderate','inconsistent_shift',dict(a=1,b=2,c=1,d=2,u=1,v=4,e=3),'q-42059'),('moderate','inconsistent_scaled_shift',dict(a=1,b=2,c=1,d=2,u=2,v=4,e=3),'q-131728'),('hard','dependent_fractional',dict(a=2,b=2,c=4,d=3,u=1,v=3,e=6),'q-131731'),('hard','dependent_negative',dict(a=1,b=2,c=1,d=-2,u=-1,v=-4,e=-2),'q-42021')]:
 for pr in [None,profile]:
  r=g.generate(level,seed=681757,template=t,parameters=p,profile=pr);assert v.audit(r)['root']=='0';boundaries.append(r)
write('boundary-records.json',boundaries)
# Controlled relevant/irrelevant pair chosen independently; include old root as actual distractor.
p=dict(a=1,b=2,c=1,d=2,u=1,v=3,e=3)
for seed in range(681703,681730):
 cf=[g.generate('moderate',seed=seed,template='inconsistent_shift',parameters=z) for z in [p,dict(p,v=1),dict(p,e=4),dict(p,v=4)]]
 if any(a[':answer/value']=='k=1' for a in cf[1]['question'][':question/answer-fields'][0][':answer-field/choices']):break
assert [v.audit(r)['root'] for r in cf]==['1','3','1','0']
write('counterfactual-records.json',cf);write('counterfactual-results.json',{'seed':seed,'roots':['1','3','1','0'],'expected':['1','3','1','0'],'passed':True,'grader_input':'grader-input.json','render_input':'render-records.json','old_k1_present_in_changed_bank':True})
# Rejection/resampling is independent of bank rank. Retain every candidate and accepted record.
res=[];resrecords=[]
for level,t in [('easy','inconsistent_easy'),('moderate','inconsistent_shift'),('hard','dependent_fractional')]:
 rng=random.Random(681857);counts=collections.Counter()
 for i in range(18):
  p0=g.sample(level,t,rng)
  try:
   r=g.generate(level,seed=681900+i,template=t,parameters=p0);a=v.audit(r);status='accepted';counts['accepted']+=1;counts['zero_roots']+=a['root']=='0';resrecords.append(r)
  except ValueError as e:status=str(e);counts['rejected:'+status]+=1
  res.append(dict(level=level,template=t,index=i,parameters=p0,result=status))
 res.append({'template':t,'summary':dict(counts)})
write('resampling-results.json',res);write('resampling-records.json',resrecords)
# Native submissions derive expected correctness from printed equations rather than generator key.
grader=[]
alltest=batch+[next(z for z in samples if z['generation']['template']==t) for ts in g.TEMPLATES.values() for t in ts]+cf+boundaries+json.load(open(R/'source-replays.json'))
for ix,r in enumerate(alltest):
 root=s.Rational(v.audit(r)['root']);f=r['question'][':question/answer-fields'][0]
 checks=[dict(field_index=0,submitted_answer_id=a[':answer/id'],expected='accepted' if v.expr(a[':answer/value'].split('=')[1])==root else 'rejected',purpose='Independent printed system root and rank; includes previous root as wrong option in relevant pair') for a in f[':answer-field/choices']]
 grader.append({'label':f'independent-{ix}','record':r,'checks':checks})
write('grader-input.json',grader)
q74691=next(r for r in alltest if r['generation']['profile']=='q-74691')
write('render-records.json',batch+cf+[q74691,boundaries[0]])
write('easy-samples.json',[r for r in samples if r['generation']['template']=='inconsistent_easy'])
# Reconfirm previously affected stored generated records using bound old generator and complete saved records.
oldR=R.parent/'review-0-policy-2-7164cf0480f72dae';spec=__import__('importlib.util',fromlist=['x']).spec_from_file_location('old_generator',oldR/'relocated/17592186115242.py');oldg=__import__('importlib.util',fromlist=['x']).module_from_spec(spec);spec.loader.exec_module(oldg)
inv=json.load(open(R.parent/'source/inventory.json'));stored=[];affected=[]
for oldr in json.load(open(oldR/'generated-records.json')):
 gen=oldr['generation'];r=oldg.generate('easy',seed=gen['seed'],template=gen['template'],parameters=gen['parameters'])
 assert all(gen[k]==z for k,z in r['generation'].items())
 q=next(z for z in inv['questions'] if z[':question/id']==r['question'][':question/id']);f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
 assert q[':question/problem']==r['question'][':question/problem'] and q[':question/worked-solution']==r['question'][':question/worked-solution']
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices']) and f[':answer-field/correct'][':answer/id']==rf[':answer-field/correct'][1]
 r['generation']=gen;stored.append(r)
 affected.append(dict(question_id=q[':question/id'],entity_id=q[':db/id'],finding='Historical v2 easy sign-only numeric-extreme shortcut remains in captured inventory; not reproduced by current v3 construction.',reproduction=f'Run job-python -B supplement.py; old generator seed={gen["seed"]}, parameters={gen["parameters"]}',evidence_path='generated-records.json'))
write('generated-records.json',stored);write('affected-inventory.json',{'affected_questions':affected})
write('inventory-audit.json',{'basis':inv['basis'],'total':len(inv['questions']),'original_practice_questions':17,'historical_generated_questions_verified':len(stored),'current_package_in_inventory':0,'provenance':'Replayed prior bound old package; matched question ID, prompt, full solution, bank, key and all runtime metadata against prior complete records and captured inventory. No original source question relabelled generated.','limits':'No live database access; existing five weak v2 items require separate bank remediation, which is outside generator-only repair scope.'})
write('supplement-math-results.json',[v.audit(r) for r in boundaries+cf+resrecords+stored])
# Save a local source image to document visual confirmation of the original flowchart.
shutil.copyfile('/media/jake/SSD/EDB/math/images/f5/f5b808eac6e1d865b13b68ce2a4f7d317560ae3965928e478531fcd2148c2c6b.png',R/'lesson-classification.png')
a=json.load(open(R/'source-analysis.json'));a['gaps']=['No easy-labelled source instances.'];a['image_confirmation']='Visually inspected lesson flowchart: no solution -> inconsistent; solution -> consistent; unique -> independent; not unique -> dependent. Saved lesson-classification.png.';write('source-analysis.json',a)
(R/'session-state.md').write_text('Regression milestone: 18/18 source replays; 75 initial exact math checks; all three strict prior counterexamples fail on old package and pass on current. Eight zero-root profile/default boundaries pass; relevant/irrelevant pair roots 1,3,1,0 saved for actual UI/grader. Historical five weak inventory records independently replayed and retained separately. Delivery/grading/rendering pending.\n')
print(json.dumps({'source_wording':collections.Counter(z['solution_wording_matches'] for z in source_report),'cf_seed':seed,'boundary_records':len(boundaries),'inventory_affected':len(affected),'supplement_math_records':len(boundaries+cf+resrecords+stored)}))
