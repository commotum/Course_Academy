import copy,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parent;W=Path('/tmp/generator-live-pipeline/workspace');sys.path.insert(0,str(W));import generator
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_evidence import record_sha256
load=lambda p:json.loads(Path(p).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n')
def parse(record):
 q=record['question'];m=re.search(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',q[':question/problem'],re.S)
 a=[[int(t.strip()) for t in row.split('&')] for row in m[1].split(r'\\')]
 i,j=map(int,re.search(r'find \$a_\{([12])([12])\}',q[':question/problem']).groups());v=a[i-1][j-1]
 f=q[':question/answer-fields'][0];key=f[':answer-field/choices'][0][':answer/value']
 conclusion=re.search(r'\$a_\{([12])([12])\}=(-?\d+)\$',q[':question/worked-solution'])
 assert int(key)==v and tuple(map(int,conclusion.groups()))==(i,j,v)
 return a,i,j,v
pairs=[];native=[]
for band in ['easy','moderate','hard']:
 base=load(R/f'delivery-{band}/accepted.json')[0];a,i,j,v=parse(base)
 for kind in ['relevant','irrelevant']:
  changed=copy.deepcopy(a)
  if kind=='relevant':x,y=i-1,j-1
  else:x,y=i%2,j%2
  changed[x][y]+=1
  generated=generator.generate(changed,i-1,j-1,band)
  ca,ci,cj,cv=parse(generated);expected=v+1 if kind=='relevant' else v
  assert cv==expected
  name=f'counterfactual-{band}-{kind}.json';save(name,[generated])
  pairs.append({'band':band,'kind':kind,'source_record_sha256':record_sha256(base),'changed_record_sha256':record_sha256(generated),'change':f'Increment row {x+1}, column {y+1} with all other givens and target fixed.','expected':str(expected),'observed':str(cv),'status':'passed','sample_refs':[f'delivery-{band}/accepted.json',name]})
  native.append({'label':f'{band}-{kind}','record':generated,'checks':[{'field_index':0,'submitted':str(cv),'expected':'accepted','purpose':'Independent changed displayed-cell lookup matches regenerated key and solution.'},{'field_index':0,'submitted':f'{cv}/1','expected':'accepted','control':'equivalent','purpose':'Equivalent integer-valued fraction; no form restriction.'},{'field_index':0,'submitted':str(cv+1),'expected':'rejected','control':'wrong','purpose':f'Exact integer blank has value {cv}, so distinct integer {cv+1} is wrong.'}]})
save('counterfactual-results.json',{'pairs':pairs,'method':'Actually invoke the current package generate function with one controlled cell change; independently parse displayed matrices, targets, solutions and keys. Native grader checks the six changed records separately.'})
save('counterfactual-grading-input.json',native)
# Preselected visible strategies never inspect target/key to choose an answer.
# We read a_ij only when scoring the resulting prediction, not in these strategies.
def predict(a,strategy):
 flat=[v for row in a for v in row]
 if strategy=='upper-right':return a[0][1]
 if strategy=='minimum':return min(flat)
 if strategy=='unique-negative':
  ns=[v for v in flat if v<0]
  return ns[0] if len(ns)==1 else None
 raise ValueError(strategy)
probe_sets=[]
for band in ['easy','moderate','hard']:
 ordinary=load(R/'ordinary-probe-records.json')
 selected=[x for x in ordinary if x['question'][':question/difficulty']==':question.difficulty/'+band]
 save(f'ordinary-probes-{band}.json',selected)
 final=load(R/f'delivery-{band}/accepted.json')
 for label,records in [('final-delivered',final),('ordinary-fresh',selected)]:
  for strategy in ['upper-right','minimum','unique-negative']:
   rows=[]
   for record in records:
    a,i,j,v=parse(record);prediction=predict(a,strategy)
    if prediction is None:continue
    rows.append({'record_sha256':record_sha256(record),'prediction':prediction,'actual':v,'correct':prediction==v,'guessing_baseline':sum(x==v for row in a for x in row)/4})
   probe_sets.append({'band':band,'set':label,'strategy':strategy,'correct':sum(x['correct'] for x in rows),'total':len(rows),'baseline':sum(x['guessing_baseline'] for x in rows)/len(rows) if rows else None,'cases':rows,'claim':'diagnostic'})
save('cue-probes.json',{'allowed_information':'Displayed matrix only, no target, key, metadata, seed, answer catalog or solution. Unique-negative subgroup is selected by counting negative displayed cells. Target/key is used only to score predictions after selecting them.','bypassed_work':'All strategies omit the requested subscript and its row/column interpretation; unique-negative uses sign recognition as a possible cue instead.','results':probe_sets,'limits':'Small final batches and 200 fresh ordinary cases per band are diagnostic, not confirmation of a defect or universal absence of shortcuts. No per-batch balance quota follows.'})
print(json.dumps({'counterfactuals':len(pairs),'probe_results':[{k:row[k] for k in ['band','set','strategy','correct','total']} for row in probe_sets]}))
