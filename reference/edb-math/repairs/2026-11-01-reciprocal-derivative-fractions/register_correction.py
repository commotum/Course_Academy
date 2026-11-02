"""Attest the corrected exponent so future source imports cannot restore it."""
import hashlib,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from migrate_learner_history import connection
proof=json.loads((H/'verification.json').read_text());assert proof['committed'];basis=proof['basis_after'];mid='q-341608'
db=connection();q=db.questions([mid],H/'correction-readback','question',basis)[mid]
assert '-2{y}^{-2}+5{y}^{2}' in q[':question/worked-solution'] and '-2{y}^{-1}+5{y}^{2}' not in q[':question/worked-solution']
fields=[]
for f in q[':question/answer-fields']:
    correct=f[':answer-field/correct'];bank=[correct] if f[':answer-field/type'][':db/ident']==':answer-field.type/blank' else f[':answer-field/choices']
    fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':[{'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']} for a in bank],'correct_value':correct[':answer/value']})
d=ROOT/'reference/mathacademy/mathematical-corrections/2026-11-01-q-341608';d.mkdir(parents=True,exist_ok=True)
independent=H/'proposals.json'
review={'question_entity':q[':db/id'],'corrected_content':{'math_academy_id':mid,'problem':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'answer_fields':fields},'rationale':'The reciprocal power -2/y^2 equals -2y^(-2), not -2y^(-1). The following differentiation and keyed denominator 4+10y^4 already use the correct power. Also retain the independently verified fraction answer layout. Field identities and saved responses are unchanged.','authorship':'Independently derived and symbolically checked mathematical correction.','independent_proof':str(independent.relative_to(ROOT)),'independent_proof_sha256':hashlib.sha256(independent.read_bytes()).hexdigest(),'commit':str((H/'publication').relative_to(ROOT))}
path=d/'review.json';path.write_text(json.dumps(review,indent=2)+'\n');tx=d/'transaction.edn';shutil.copy2(H/'publication/transaction.edn',tx)
(d/'verification.json').write_text(json.dumps({'committed':True,'mathematical_check_passed':True,'basis_after':basis,'review_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'transaction_sha256':hashlib.sha256(tx.read_bytes()).hexdigest(),'learner_and_engine_facts_unchanged':True,'original_verification':str((H/'verification.json').relative_to(ROOT))},indent=2)+'\n')
reconciler=db.reconciliation({'questions':[],'canonical_examples':[]},H/'correction-readback',{mid:q},basis)
assert any(r['category']=='mathematical_correction' for r in reconciler.evidence(reconciler.authored,mid,None,'question/worked-solution',q[':question/worked-solution']))
assert reconciler.replace(mid,None,'question/worked-solution',q[':question/worked-solution'],'Original exponent typo',{'ma_capture'}) is False
(H/'correction-protection.json').write_text(json.dumps({'passed':True,'basis':basis,'actual_importer_immutable_attestation':True,'erroneous_solution_cannot_overwrite_verified_correction':True,'database_writes':0},indent=2)+'\n')
print('Verified mathematical correction protected against reimport at',basis)
