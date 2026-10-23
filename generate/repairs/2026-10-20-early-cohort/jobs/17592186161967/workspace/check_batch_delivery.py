"""Compare visible current CLI decision cases after shared delivery filtering."""
import collections,json
from check_batch_repair import OUT,probe
raw=json.loads((OUT/'small-sample.json').read_text())
accepted=json.loads((OUT/'small-delivery/accepted.json').read_text())
def split(rows):
 groups=collections.defaultdict(list)
 for r in rows:
  b=r['generation']['batch'];groups[(b['seed'],b['count'])].append(r)
 return groups
before,after=split(raw),split(accepted)
assert before.keys()==after.keys()
reports=[]
for key,rows in after.items():
 assert len(rows)==len(before[key])==key[1]
 report=probe(rows)
 reports.append({'seed':key[0],'count':key[1],'raw':probe(before[key]),'delivered':report})
all_rows=accepted+json.loads((OUT/'delivery/accepted.json').read_text())
from check_repair import inspect,mats
stats={'profiles':set(),'coordinates':set(),'sign_pairs':set(),'semantic_instances':set(),'correct_positions':set()}
for r in all_rows:
 bank,ci=inspect(r);A,B=mats(r['question'][':question/problem'])
 stats['semantic_instances'].add(str((A,B)))
 stats['sign_pairs'].add(tuple(1 if x>0 else -1 for x in bank[ci]))
 stats['profiles'].add(r['generation']['bank_profile'])
 stats['correct_positions'].add(ci)
 p=next(i for i in range(3) if A[i]==B[i]);c=next(c for c in range(3) if A[p][c] and all(B[i][c]==0 for i in range(3) if i!=p))
 stats['coordinates'].add((p,c))
assert len(stats['profiles'])==10 and len(stats['sign_pairs'])==4
summary={k:(len(v) if k=='semantic_instances' else sorted(v)) for k,v in stats.items()}
result={'status':'pass','sample_survivors':len(accepted),'batch_survivors':5,'coverage':summary,'batches':reports,
 'selection_limit':'Shared delivery covers captured inventory basis 5580. Learner history and future inventory changes are not simulated. Existing selection.rs chooses a seeded uniform member of the selected difficulty; it does not enforce per-learner sign-case sequencing.'}
(OUT/'post-delivery-report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','sample_survivors':len(accepted),'coverage':summary}))
