import json,collections,pathlib,sys,re,hashlib
from fractions import Fraction as F
import review as t
E=t.E;J=t.J
save=t.save

def sign(v):return (v>0)-(v<0)
def correct(r):return r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
def signature(a):return tuple(sign(v) for v in t.matrix(a[':answer/value'])[0][1:])
def sign_strategy(r):
 # Inspect only signs of first displayed equation and signs of choice top rows.
 # Does not calculate any quotient, inspect other equations or inspect metadata/key.
 row=t.equations(r['question'][':question/problem'])[0];want=tuple(sign(v)*sign(row[0]) for v in row[1:])
 candidates=[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if signature(a)==want]
 return candidates[0] if len(candidates)==1 else None

def measure(rs):
 answers=[]
 for r in rs:
  pred=sign_strategy(r);f=r['question'][':question/answer-fields'][0];m=[t.matrix(a[':answer/value']) for a in f[':answer-field/choices']]
  answers.append({'id':r['question'][':question/id'],'success':pred==correct(r),'prediction':pred,'correct':correct(r),'same_absolute_bank':len({tuple(abs(x) for row in v for x in row) for v in m})==1,'correct_position':next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct(r)),'first_pivot_sign':sign(t.equations(r['question'][':question/problem'])[0][0]),'plan':r.get('generation',{}).get('parameters',{}).get('plan')})
 return {'count':len(rs),'successes':sum(a['success'] for a in answers),'same_absolute_bank':sum(a['same_absolute_bank'] for a in answers),'position_counts':dict(collections.Counter(a['correct_position'] for a in answers)),'conditional':{s:{'count':sum(a['first_pivot_sign']==s for a in answers),'successes':sum(a['success'] for a in answers if a['first_pivot_sign']==s)} for s in (-1,1)},'results':answers}
if __name__=='__main__':
 sets={n:json.loads((E/f).read_text()) for n,f in [('batch','batch.json'),('fresh','fresh-easy.json'),('delivered_batch','delivery-batch/accepted.json'),('delivered_fresh','delivery-fresh/accepted.json')]}
 results={k:measure(v) for k,v in sets.items()};save('shortcut-results.json',{'command':str(t.PY)+' '+str(E/'probes.py'),'algorithm':'Read only signs of first equation; multiply each b,c,d sign by sign of x; select unique matching sign triple. No magnitude arithmetic, pivot scaling or row elimination.','sets':results})
 # Check all captured non-source records, keeping originals intact. No claim of current-generator provenance.
 inv=json.loads((J/'source/inventory.json').read_text());src=json.loads((J/'source/source.json').read_text());originals={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']};originals.add(src['material']['kp'][':knowledge-point/canonical-example'][':question/id'])
 stored=[]
 for q in inv['questions']:
  if q[':question/id'] in originals:continue
  f=q[':question/answer-fields'][0];cq=f.get(':answer-field/correct');pass # Full captured non-source records retained below.
  stored.append(q)
 save('stored-records.json',stored)
 # Captured inventory omits generation metadata for every record. Cannot satisfy exact replay provenance.
 save('affected-inventory.json',{'affected_questions':[]})
 save('inventory-assessment.json',{'basis':inv['basis'],'original_source_questions_excluded':len(originals),'non_source_records_inspected':len(stored),'limitation':'All captured inventory records omit generation metadata. Non-source status alone does not establish origin from this generator. No affected generated record with exact seed/metadata replay demonstrated. Empty affected list is not a verified absence of historical defects.','stored_records_file':'stored-records.json'})
 # Source replay command fails to reproduce supplied source 693512da, strict regression acceptance.
 missing=json.load(open(E/'source-replay-results.json'))['missing'];save('strict-regressions.json',{'source_coverage':{'expected':16,'actual':15,'missing':missing,'passed':not missing},'decision_independence':{'expected':'Sign-only strategy must not answer every delivered item because numerical pivot normalization is assessed.','success':results['delivered_batch']['successes'],'total':results['delivered_batch']['count'],'passed':results['delivered_batch']['successes']<results['delivered_batch']['count']}})
 # Read-only learner selection reproduction: all accepted records easy, so within-band weighted selection uniform.
 accepted=sets['delivered_batch'];counts=collections.Counter();seen_draws=[]
 for i in range(100):
  seed=f'independent-review-913771/{i}';digest=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);picked=sorted(accepted,key=lambda r:r['question'][':question/id'])[int(u*len(accepted))];counts[picked['question'][':question/id']]+=1
 fresh_sequences=[]
 for i in range(5):
  pool=sorted(accepted,key=lambda r:r['question'][':question/id']);seq=[]
  while pool:
   seed=f'fresh-learner-{i}/prefix-{len(seq)}';d=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);seq.append(pool.pop(int(u*len(pool)))['question'][':question/id'])
  fresh_sequences.append(seq)
 save('selection-analysis.json',{'source':'engine/rust/question_selection.rs select, seen_before_task','implementation':'Faithful read-only SHA256 within-band draws; actual entity order unavailable, UUID ordering used as a permutation. Since all five candidates have the defect, ordering, weights and prior exclusions cannot remove it from any nonempty subset.','stages':{'generator':{'fresh':96,'rejected':0,'rule':'prompt-parameter tuple uniqueness; max 100 attempts per result'},'requested_difficulty':'easy, all five survive','deduplication':{'batch_in':5,'batch_accepted':5,'fresh_in':96,'fresh_accepted':96},'learner_selection':'For any positive easy weight, sample uniformly in easy band; zero easy weight makes this isolated pool unavailable, not repaired.'},'draw_count':100,'counts':dict(counts),'without_replacement_sequences':fresh_sequences,'shortcut_success_rate':1.0,'limits':['Captured basis 5370 only; no live learner history/policy available.','Existing source questions may enter mixed inventory pools; claim is conditional on selecting a generated survivor.','No publication or DB writes.']})
 save('package-after.json',t.package_hashes());assert json.load(open(E/'package-before.json'))==t.package_hashes()
 print(json.dumps({k:{a:b for a,b in v.items() if a!='results'} for k,v in results.items()},indent=2))
