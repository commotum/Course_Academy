"""Attest that a fixed complete readback remains valid after known later commits."""
import collections,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads
read=lambda p:json.loads(p.read_text());db=connection();D=H/'presentation-delta';D.mkdir(exist_ok=True)
base=read(H/'prepublication-check/basis.json')['basis_t'];target=read(H/'final-check/basis.json')['basis_t'];assert base<=target
attestation=read(H/'group-2/final-presentation-readback/verification.json');assert attestation['passed']and attestation['basis']==base and attestation['model_sha256']==hashlib.sha256((H/'prepublication-check/model.json').read_bytes()).hexdigest()
query=D/'query.edn';query.write_text('[:find ?e ?a ?v ?tx ?source ?added :where [?e ?a ?v ?tx ?source ?added]]\n')
result=db.command('query','--file',query,'--as-of',target,'--since',base,'--history','--max-results','100000');(D/'datoms.edn').write_text(result);rows=loads(result)
attrs={':question/problem',':question/worked-solution',':question/answer-fields',':question/difficulty',':question/math-academy-id',':answer-field/key',':answer-field/display-key',':answer-field/type',':answer-field/correct',':answer-field/choices',':answer/value',':answer/type',':answer/feedback',':tutorial/content',':tutorial/title'}
names=dict(read(H/'idents.json'));attribute_ids={eid for eid,name in names.items()if name in attrs}
protected=set()
def visit(v):
 if isinstance(v,list):
  for x in v:visit(x)
 elif isinstance(v,dict):
  if ':db/id'in v:protected.add(v[':db/id'])
  for x in v.values():visit(x)
for name in ['prepublication-check','final-check']:visit(read(H/name/'model.json'));protected.update(x['entity']for x in read(H/name/'render-input.json'))
key=lambda d:json.dumps(d,default=str,separators=(',',':'))
relevant=lambda d:d[0]in protected and d[1]in attribute_ids
actual=collections.Counter(key(d)for d in rows if relevant(d));expected=collections.Counter();later=[]
for name in read(H/'commits.json'):
 v=read(H/name/'verification.json')
 if base<v['basis_t']<=target:
  receipt=loads((H/name/'receipt.edn').read_text());expected.update(key(d)for d in receipt[':edb/tx-data']if relevant(d));later.append(name)
assert actual==expected,{'unexpected':list((actual-expected).elements()),'missing':list((expected-actual).elements())}
report={'passed':True,'base_t':base,'target_t':target,'complete_readback':'group-2/final-presentation-readback','later_verified_content_batches':later,'presentation_datoms_after_base':sum(actual.values()),'unexpected_presentation_changes':0,'database_writes':0};(H/'presentation-delta-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
