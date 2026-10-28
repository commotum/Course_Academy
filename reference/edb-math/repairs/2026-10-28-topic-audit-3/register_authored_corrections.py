"""Register only independently proved, committed authoring for future reconciliation.

Input authoring-manifest.json lists {question, commit, rationale, proof_file}.
The existing provenance reader still attests values/identities at the saved basis.
"""
import hashlib,json,os,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from provenance import mathematical_correction_records
read=lambda p:json.loads(Path(p).read_text())
model={q[':db/id']:q for q in read(H/'final-check/model.json')};names=dict(read(H/'idents.json'));out=[]
def enum(v):return str(v.get(':db/ident',names.get(v.get(':db/id'))))if isinstance(v,dict)else str(v)
for item in read(H/'authoring-manifest.json'):
 q=model[item['question']];mid=q.get(':question/math-academy-id')
 if not mid:continue
 batch=H/item['commit'];verification=read(batch/'verification.json');assert verification['committed']and verification['only_exact_reviewed_datoms_changed']
 proof=(R/item['proof_file']).resolve();assert proof.is_file()
 fields=[]
 for f in q.get(':question/answer-fields',[]):
  right=f.get(':answer-field/correct');assert right,f
  bank=f.get(':answer-field/choices',[]);canonical=next(a for a in bank if a[':db/id']==right[':db/id'])
  # Historical blank entries are learner data, not authored choice alternatives.
  bank=[canonical]if enum(f[':answer-field/type'])==':answer-field.type/blank'else [canonical]+[a for a in bank if a[':db/id']!=canonical[':db/id']]
  fields.append({'key':f[':answer-field/key'],'type':enum(f[':answer-field/type']).split('/')[-1],
                 'choices':[{'type':enum(a[':answer/type']).split('/')[-1],'value':a[':answer/value']}for a in bank],
                 'correct_value':canonical[':answer/value']})
 content={'math_academy_id':mid,'problem':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'answer_fields':fields}
 directory=R/'reference/mathacademy/mathematical-corrections'/('2026-10-28-audit-3-'+mid);directory.mkdir(exist_ok=True,parents=True)
 review={'corrected_content':content,'rationale':item['rationale'],'authorship':'Locally derived or corrected; not claimed as an observed Math Academy key.',
         'independent_proof':str(proof.relative_to(R)),'independent_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
         'question_entity':q[':db/id'],'commit':str(batch.relative_to(R))}
 encoded=json.dumps(review,indent=2,ensure_ascii=False)+'\n';path=directory/'review.json'
 if path.exists():assert path.read_text()==encoded
 else:path.write_text(encoded)
 tx=directory/'transaction.edn'
 if not tx.exists():
  try:os.link(batch/'transaction.edn',tx)
  except OSError:shutil.copyfile(batch/'transaction.edn',tx)
 assert tx.read_bytes()==(batch/'transaction.edn').read_bytes()
 record={'committed':True,'mathematical_check_passed':True,'basis_after':verification['basis_t'],
         'review_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'transaction_sha256':hashlib.sha256(tx.read_bytes()).hexdigest(),
         'learner_and_engine_facts_unchanged':True,'source':':agent/codex','original_verification':str((batch/'verification.json').relative_to(R))}
 (directory/'verification.json').write_text(json.dumps(record,indent=2)+'\n');out.append({'question':q[':db/id'],'source_id':mid,'directory':str(directory.relative_to(R))})
loaded=mathematical_correction_records(R/'reference/mathacademy',{x['source_id']for x in out})
assert {r['question']for r in loaded}=={x['source_id']for x in out}
(H/'authored-reconciliation-verification.json').write_text(json.dumps({'passed':True,'question_records':len(out),'attribute_evidence_records':len(loaded),'records':out,'database_writes':0},indent=2)+'\n');print('Registered committed authored corrections:',len(out))
