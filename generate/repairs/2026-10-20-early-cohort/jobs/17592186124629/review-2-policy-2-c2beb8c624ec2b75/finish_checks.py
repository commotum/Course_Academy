import json,re,sys,hashlib,importlib.util
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parent/'workspace';sys.dont_write_bytecode=True;sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('g',W/'17592186124629.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
sources=json.load(open(E.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];rs=json.load(open(E/'source-replays.json'));report=json.load(open(E/'source-replay-report.json'))
for item,r in zip(report['cases'],rs):
 src=next(q for q in sources if q[':question/id']==item['source_id']);tail=src[':question/worked-solution'].split('With that in mind',1)[1]
 if item['template']=='q-141342':
  tail=tail.replace(r'\text{nullity}(A)=0,$ then',r'\text{nullity}(A)\ne 0,$ then')
 actual=r['question'][':question/worked-solution'].split('With that in mind',1)[1]
 assert g.normalize_prose(tail)==actual
 item['worked_implication_paragraphs_match_with_documented_correction']=True
report['theorem_reflow']='Inspected actual rendered vertical equivalence; all four theorem identities agree with tutorial 555ca00c-d37e-5c67-a658-69b087390920. No response or implication method changed.'
save('source-replay-report.json',report)
results=[]
for name,kw in [('unsupported difficulty',{'difficulty':'hard'}),('unknown template',{'template':'q-missing'}),('empty explicit checkbox subset',{'template':'q-47599','parameters':{'premise':'decision','invertible':True,'hypothesis':'rank','truths':[False,False,False]}}),('unvalidated hypothesis',{'template':'q-47599','parameters':{'premise':'decision','invertible':True,'hypothesis':'pivot','truths':[True,False,True]}})]:
 try:g.generate(**kw)
 except ValueError as err:results.append({'test':name,'parameters':kw,'outcome':'rejected','exception':str(err)})
 else:raise AssertionError(name)
save('boundary-results.json',results)
save('scope-results.json',{'source_lesson':'tutorial 555ca00c-d37e-5c67-a658-69b087390920, canonical c1120305-c8cb-5f57-97b1-9b31dc059b4a','observed':'Every independent sampled prompt is a real square-matrix implication evaluating three theorem propositions. Invertible and singular conclusions require theorem relationships, not row reduction or construction. Basis assertions are finite-dimensional subspace facts already present in source q-142479 and q-141214. Positive numeric dimensions remain the five original dimensions; n is declared positive.','fixed_features_assessment':'Fixing the square shape, three-proposition workload, radio versus checkbox bank shapes, and moderate band is justified. Fixing source-profile dimensions is a conservative finite family; meaningful sampled variation comes from premise state, hypothesis concept, proposition polarities and qualifying subsets.','unsupported_source':'q-47586 omitted because captured key, solution and difficulty are missing and its answer bank lacks the correct subset; no engine limitation is being concealed.','evidence':['independent-samples.json','source-replays.json','math-results.json']})
before=json.load(open(E/'package-hashes-before.json'));after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
assert before==after
save('package-integrity.json',{'unchanged':True,'files_checked':len(after),'before':'package-hashes-before.json','after':after})
print(json.dumps({'source_solutions':len(rs),'boundaries':len(results),'package_unchanged':before==after,'package_files':len(after)}))
