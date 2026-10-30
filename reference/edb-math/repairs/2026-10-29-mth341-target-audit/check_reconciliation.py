"""Read-only real importer attestation and stale-source regression check."""
import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
from provenance import field_value
D=H/'reconciliation-readback';D.mkdir(exist_ok=True);db=connection();basis=db.basis()
ids=['q-140766','q-141192','q-47586','q-33160','q-280352','e-13158']
current=db.questions(ids,D,'current',basis);assert set(current)==set(ids)
reconciler=db.reconciliation({'questions':[],'canonical_examples':[]},D,current,basis)
proof=[]
for mid in ids:
 q=current[mid]
 for attr in ['question/problem','question/worked-solution']:
  if attr=='question/problem'and mid=='e-13158':continue
  exact=[r for r in reconciler.evidence(reconciler.authored,mid,None,attr,q[':'+attr])if r['category']=='mathematical_correction']
  assert exact,(mid,attr,'No real immutable-basis attestation')
  assert reconciler.replace(mid,None,attr,q[':'+attr],'Stale original mathematical source error',{'ma_capture'})is False
 proof.append({'source_id':mid,'immutable_basis_and_identity_attested':True,'incorrect_source_scalar_replacement_prevented':True})
baseline=json.loads((H/'group-1/current.json').read_text())
for mid in ['q-140766','q-141192']:
 oldq=next(q for q in baseline['questions']if q.get(':question/math-academy-id')==mid)
 f=current[mid][':question/answer-fields'][0];oldf=next(x for x in oldq[':question/answer-fields']if x[':db/id']==f[':db/id']);bank=oldf[':answer-field/choices'];right=next(a for a in bank if a[':db/id']==oldf[':answer-field/correct'][':db/id'])
 def kind(v):return v[':db/ident'].split('/')[-1]
 incoming={'key':f[':answer-field/key'],'type':kind(f[':answer-field/type']),'choices':[{'type':kind(a[':answer/type']),'value':a[':answer/value']}for a in bank],'correct_value':right[':answer/value']}
 assert any(r['category']=='mathematical_correction'for r in reconciler.evidence(reconciler.authored,mid,f[':answer-field/key'],'answer-field/choices',field_value(f,'answer-field/choices')))
 assert reconciler.field_action(mid,f,incoming)=='retain'
 proof.append({'source_id':mid,'stale_complete_choice_bank_prevented':True,'exact_typed_bank_attested':True})
result={'passed':True,'basis_t':basis,'tests':proof,'decisions':reconciler.decisions,'attested_evidence_records':len(reconciler.authored),'database_writes':0}
(H/'reconciliation-protection-verification.json').write_text(json.dumps(result,indent=2,default=str)+'\n');print('Actual importer immutable readback/protection passed:',len(proof),'checks at',basis)
