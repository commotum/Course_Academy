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
  r=g.generate(level,seed=822157,template=t,parameters=p,profile=pr);assert v.audit(r)['root']=='0';boundaries.append(r)
write('boundary-records.json',boundaries)
# Controlled relevant/irrelevant pair chosen independently; include old root as actual distractor.
p=dict(a=1,b=2,c=1,d=2,u=1,v=3,e=3)
for seed in range(822101,822130):
 cf=[g.generate('moderate',seed=seed,template='inconsistent_shift',parameters=z) for z in [p,dict(p,v=1),dict(p,e=4),dict(p,v=4)]]
 if any(a[':answer/value']=='k=1' for a in cf[1]['question'][':question/answer-fields'][0][':answer-field/choices']):break
assert [v.audit(r)['root'] for r in cf]==['1','3','1','0']
write('counterfactual-records.json',cf);write('counterfactual-results.json',{'seed':seed,'roots':['1','3','1','0'],'expected':['1','3','1','0'],'passed':True,'grader_input':'grader-input.json','render_input':'render-records.json','old_k1_present_in_changed_bank':True})
# Rejection/resampling is independent of bank rank. Retain every candidate and accepted record.
res=[];resrecords=[]
for level,t in [('easy','inconsistent_easy'),('moderate','inconsistent_shift'),('hard','dependent_fractional')]:
 rng=random.Random(822257);counts=collections.Counter()
 for i in range(18):
  p0=g.sample(level,t,rng)
  try:
   r=g.generate(level,seed=822300+i,template=t,parameters=p0);a=v.audit(r);status='accepted';counts['accepted']+=1;counts['zero_roots']+=a['root']=='0';resrecords.append(r)
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

write('supplement-math-results.json',[v.audit(r) for r in boundaries+cf+resrecords])
print('supplement complete')
