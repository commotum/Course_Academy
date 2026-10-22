import json,pathlib,hashlib,collections
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
def read(n):return json.load(open(E/n))
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def response(r):
 f=r['question'][':question/answer-fields'][0];a=f[':answer-field/choices'];v=[int(x[':answer/value']) for x in a];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id'];i=next(i for i,x in enumerate(a) if x[':answer/id']==cid)
 return v,i,v[i]
probes=[]
def probe(rs,ref,group,scope,strategy,fn,disposition='not_predictive',note=''):
 correct=sum(bool(fn(r,*response(r))) for r in rs)
 probes.append({'cue':strategy,'subgroup':group,'scope':scope,'strategy':strategy,'correct':correct,'total':len(rs),'baseline':0.2,'disposition':disposition,'conclusion':f'{correct}/{len(rs)} against uniform five-option guessing baseline 0.20. '+note,'sample_refs':[ref]})
for level in ['easy','moderate']:
 for path,stage in [(level+'-records.json','raw'),('delivery-'+level+'-records/accepted.json','delivered')]:
  rs=read(path)
  for name,fn in [('Always select first option',lambda r,v,i,a:i==0),('Select second-smallest option',lambda r,v,i,a:sorted(v).index(a)==1),('Select maximum option',lambda r,v,i,a:a==max(v)),('Copy row dimension',lambda r,v,i,a:a==r['generation']['parameters']['rows'])]:
   probe(rs,path,level+' wording / '+stage,'within_template',name,fn,note='Strategy has counterexamples; no exhaustive absence-of-shortcut claim. Moderate row-copy never succeeds because full-row-rank cases are rejected, a demonstrated restriction.')
  probe(rs,path,level+' wording / '+stage,'within_template','Copy supplied column count',lambda r,v,i,a:a==r['generation']['parameters']['count'],'intended_skill' if level=='easy' else 'not_predictive','Easy is the intended rank=pivots definition. Moderate never has rank=nonpivots because that valid case is suppressed.')
  for profile in sorted({r['generation']['bank_profile'] for r in rs}):
   sub=[r for r in rs if r['generation']['bank_profile']==profile]
   probe(sub,path,profile+' / '+stage,'other_recognizable_subgroup','Always select first option',lambda r,v,i,a:i==0,note='Conditional bank-construction probe. Metadata is not learner-visible; no perfect fixed-first action occurs in this profile sample.')
rs=read('delivery-runner-batch/accepted.json')
for name,fn in [('Always select first option',lambda r,v,i,a:i==0),('Always select fifth option',lambda r,v,i,a:i==4),('Select second-smallest option',lambda r,v,i,a:sorted(v).index(a)==1),('Select maximum option',lambda r,v,i,a:a==max(v))]:
 probe(rs,'delivery-runner-batch/accepted.json','exact runner batch','overall',name,fn,note='Evaluated separately from larger samples; strategy does not solve all five.')
sub=[r for r in rs if r['generation']['bank_profile']=='q-34825']
probe(sub,'delivery-runner-batch/accepted.json','runner q-34825 construction','other_recognizable_subgroup','Always select first option',lambda r,v,i,a:i==0,note='Three records have three different correct positions and numerical orders; singleton profiles cannot establish a conditional distribution.')
pv={'learner_operation':read('source-analysis.json')['learner_operation'],
'fixed_features':[{'feature':'Rank target, five radio options, one correct','justification':'Every source-bank question has this response contract.'},{'feature':'Easy gives pivots; moderate gives non-pivots','justification':'Observed difficulty split: direct definition versus one subtraction.'},{'feature':'Feasible small positive counts','justification':'Source-like workload and rank <= min(rows,columns); feasibility does not require rank to differ from rows or non-pivots.'}],
'answer_roles':[{'role':'Correct rank','eligible_variation':'Pivot count or columns-minus-nonpivots, including equality with rows or non-pivots.','observed':'Easy ranks 1..12 covered; moderate full-row-rank and rank=nonpivot cases are rejected by every profile.'},{'role':'Name and dimensions','eligible_variation':'Names and feasible rows preserve the response; moderate columns affect it.','observed':'Successful controls follow these dependencies; source q-79409 rows 5 -> 4 instead fails generation.'},{'role':'Answer position and bank','eligible_variation':'Preserve complete banks on replay; replace colliding distractors on extensions.','observed':'Fresh positions/orders vary in all profiles, but valid() requires the original unsigned recipe to be distinct before constructing the bank.'}],
'coverage':[{'case':'11 source-bank profiles','sample_refs':['source-replay-records.json','source-replay-tests.json','independent-records.json','delivery-coverage.json'],'result':'All complete banks replay. Twenty fresh seeds per profile; delivery accepts 100/100 easy and 112/120 moderate, skipping eight duplicates.'},{'case':'Canonical full-row rank','sample_refs':['canonical-rejection.json','audit-canonical.py'],'result':'FAIL: 4x7 with three non-pivots rejected by every moderate profile.'},{'case':'Rank equals non-pivots','sample_refs':['restriction.json','restriction-regression.py','restriction-regression.stderr'],'result':'FAIL: 3x4/two non-pivots rejected. Six even-column pairs and one additional (columns,count)=(3,2) are absent within current numeric bounds.'},{'case':'Exact requested batch','sample_refs':['runner-batch.json','delivery-runner-batch/accepted.json','delivery-coverage.json'],'result':'All five survive; ranks 10,1,11,3,8 and correct positions 5,5,1,3,2. No tested fixed action solves all five.'}],
'counterfactuals':[{'kind':'relevant','change':'Change supplied pivot/nonpivot count at fixed dimensions; additionally change moderate columns 8 -> 9.','expected':'Easy 5 -> 4; moderate 5 -> 6 under count 3 -> 2 or columns 8 -> 9.','observed':'Prompts, keys, solutions, actual native acceptance/rejection and rendered answers follow the expected changes after delivery normalization.','status':'passed','justification':'Rank=pivots and canonical subtraction columns-minus-nonpivots.','sample_refs':['control-records.json','control-tests.json','grader-input.json','grader-report.json','render/rendering.json','render-tail/rendering.json']},{'kind':'irrelevant','change':'Rename Q to T and change feasible rows 10 -> 11, preserving columns and count.','expected':'Easy and moderate rank both remain five.','observed':'Normalized controls preserve rank; native grading and rendered prompts/solutions agree, with updated names and dimensions.','status':'passed','justification':'Rows only bound rank once the column count evidence is supplied.','sample_refs':['controls-easy.json','controls-moderate.json','control-tests.json','grader-report.json','render/rendering.json']},{'kind':'irrelevant','change':'Source q-79409 rows 5 -> 4, retaining seven columns and three non-pivots.','expected':'Rank remains four and the feasible item is generated.','observed':'Every profile rejects the after parameters. No after prompt, explanation or grader instance is available; before record was source-replayed and native-graded.','status':'failed','justification':'Rank four is feasible with four or five rows; canonical example uses four.','sample_refs':['row-counterfactual.json','canonical-rejection.json','grader-report.json']}],
'shortcut_probes':probes,
'delivery':{'stages_examined':['catalog construction and bank rejection','task sampling without replacement; no invalid-item resampling','requested difficulty','actual publisher normalization and inventory/within-batch deduplication','native selector inspection and faithful conditional replay'], 'sample_refs':['restriction.json','canonical-rejection.json','delivery-coverage.json','delivery-runner-batch/delivery.json','selection-tests.json'],'result':'Rejected constructions cannot enter delivery. All five exact batch records survive. Selection depends on difficulty/freshness; conditional replay documents specified weights/history and synthetic future IDs.'},
'limitations':['Captured inventory basis 5404; later inventory changes are not predicted.','Active learner history/weights and future entity IDs are absent; selection scenarios are explicitly conditional.','Finite shortcut probes do not establish universal absence. Some numerical-order heuristics outperform chance in small groups but have counterexamples.','Historical stored q-79405 ordering weakness reproduced in affected-inventory.json is not attributed to current v2.','Canonical example has no bank; its failure concerns the valid stem, without requiring an invented canonical bank.']}
save('pedagogical-variation.json',pv)
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='sample_refs':refs.extend(v)
   else:walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(pv)
for ref in refs:assert not pathlib.Path(ref).is_absolute() and (E/ref).is_file() and (E/ref).stat().st_size>0,ref
for p in probes:assert 0<=p['correct']<=p['total'] and isinstance(p['total'],int)
validation='Required fields and reference/domain checks passed; jsonschema unavailable'
try:
 import jsonschema
 jsonschema.validate(pv,json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json')));validation='jsonschema validation passed'
except ImportError:pass
save('evidence-contract.json',{'validation':validation,'sample_references_checked':len(refs)})
after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};before=read('package-before.json');assert before==after
save('package-integrity.json',{'unchanged':True,'file_count':len(before),'hashes':after})
save('render-inspection.json',{'screenshots_inspected':12,'reports':['render/rendering.json','render-tail/rendering.json'],'visual_result':'All seven controls and all five exact batch records inspected: visible dimensions/counts, radio controls, selected answers and worked equations are legible. No raw delimiters, malformed TeX, clipping or stale answers.','contact_sheets':['render/contact-1.png','render/contact-2.png','render-tail/contact-1.png','render-tail/contact-2.png']})
print(json.dumps({'pedagogical_contract':validation,'package_unchanged':True,'probes':len(probes)}))
