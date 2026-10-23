import sys,json,pathlib,importlib.util,hashlib,re,collections
from fractions import Fraction
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('target',root.parent/'workspace/17592186059776.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def load(p):return json.loads((root/p).read_text())
def save(p,o):(root/p).write_text(json.dumps(o,indent=2))
def shortcut(r):
 f=r['question'][':question/answer-fields'][0]; vals=[]
 for a in f[':answer-field/choices']:
  body=re.search(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}',a[':answer/value'],re.S)[1];vals.append(Fraction(body.split(r'\\')[1].split('&')[2].strip()))
 chosen=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if v==sorted(vals)[1]]
 return chosen==[f[':answer-field/correct'][1]]
def stats(rs):return {'count':len(rs),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'second_smallest_hits':sum(shortcut(r) for r in rs),'solution_signs':dict(collections.Counter('zero' if g.matrices(r['question'][':question/worked-solution'])[-1][1,2]==0 else 'negative' if g.matrices(r['question'][':question/worked-solution'])[-1][1,2]<0 else 'positive' for r in rs))}
orig=g.generate;attempts=[]
def traced(*a,**kw):
 r=orig(*a,**kw);attempts.append(r);return r
g.generate=traced;out=g.batch('easy',40,918273);assert out==load('control.json');save('sampler-attempts.json',attempts)
stages={p:stats(load(p)) for p in ['batch.json','control.json','delivery-batch/accepted.json','delivery-control/accepted.json']}
stages['sampler-attempts.json']=stats(attempts)
# Faithful same-band index selection from question_selection.rs: SHA256 bytes 8..16.
# Synthetic IDs in stable input order; no claim of actual postpublication entity IDs or learner history.
selection=[]
for file in ['delivery-batch/accepted.json','delivery-control/accepted.json']:
 rs=load(file)
 for seen in [0,1,2]:
  pool=rs[seen:];chosen=[]
  for n in range(128):
   seed='independent-review-'+str(n);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);chosen.append(pool[int(u*len(pool))])
  selection.append({'input':file,'fixture_seen_prefix':seen,'seed_prefix':'independent-review-','seeds':128,'stats':stats(chosen),'reachable_unique_questions':len({r['question'][':question/id'] for r in chosen})})
save('delivery-analysis.json',{'stages':stages,'sampler_rejection':'No random rejection branch. Finite shuffled parameter list; batch rejects repeated solution fingerprints. All 40 control outputs are easy.','selection_rules':{'source':'engine/rust/question_selection.rs select and seen_before_task; engine/rust/learning.rs validate_practice_question','eligibility':'Exclude prior task/prefix IDs, retired, canonical examples and unusable practice. Captured inventory contains ten originals, no generated records and no retired originals.','same_band':'Within a positive-weight easy band, hash-derived draw is uniform over fresh sorted unique entity IDs. Numerical rank is not used for selection.','fixture_limit':'Captured inventory lacks learner history and active policy weights; synthetic order verifies same-band draws, not a future learner schedule. We do not know postpublication entity IDs. Zero easy weight would suppress all candidates, not repair their pedagogy.'},'selection_fixture':selection,'ui_order':'ui/learning.js choiceOrder lines 690-693 hashes item seed and answer UUID. Authored positions are not delivered invariants. Numerical ranks survive any order.','inventory':'Captured basis 5576; no generated stored instances. No publication preparation exists; check_delivery reproduced filtering read-only.','limits':['Concurrent inventory or unknown learner history may change which record is served. Conditional rank rule holds for every member of each affected family, hence any retained subset.']})
print(json.dumps(stages))
