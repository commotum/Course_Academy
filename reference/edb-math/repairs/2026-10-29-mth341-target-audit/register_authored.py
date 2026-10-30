"""Register narrowly reviewed committed authoring from immutable11666 EDN evidence.
This writes provenance files only; it never opens a database connection.
"""
import collections,copy,hashlib,json,os,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R/'scripts'),str(R/'scripts/question_capture')]
from migrate_learner_history import loads
from provenance import mathematical_correction_records
read=lambda p:json.loads(Path(p).read_text());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
BASIS=11666;D=H/'final-live'
def cached(prefix):
 records={}
 for path in sorted(D.glob(prefix+'-*-t'+str(BASIS)+'.edn')):
  stem=path.name[len(prefix)+1:].split('-t')[0]
  if not stem.isdigit():continue
  for row in loads(path.read_text()):
   o=row[0];records[o[':db/id']]=o
 assert records,(prefix,'missing fixed readback');return records
questions=cached('questions');fields=cached('fields');owners={q[':db/id']:q[':db/id']for q in questions.values()}
for q in questions.values():
 q[':question/answer-fields']=[copy.deepcopy(fields[f[':db/id']])for f in q.get(':question/answer-fields',[])]
 for f in q[':question/answer-fields']:
  owners[f[':db/id']]=q[':db/id']
  for a in f[':answer-field/choices']:owners[a[':db/id']]=q[':db/id']
classified=read(H/'correction-classification-ledger.json')['entries'];selected=collections.defaultdict(list);tutorials=[]
for item in classified:
 if item['category']=='source-presentation-and-control-restoration':continue
 if item['entity']in owners:selected[owners[item['entity']]].append(item)
 else:
  assert item['attribute']=='tutorial/content',item;tutorials.append(item)
word={p['entity']for p in read(H/'group-3-wording-delta/proposals.json')};banks={'q-140766','q-141192'};proof_files={
'group-1':['completion-evidence.json','mathematical-corrections.json','scalar-versus-set-restorations.json','math-verification.json','supplemental-math-verification.json','row-operation-verification.json','theorem-bank-verification.json'],
'group-2':['completion-evidence.json','mathematical-correction-evidence.json','family-algebra-audit-after.json','inverse-key-verification.json','solution-chain-verification.json'],
'group-3':['completion-evidence.json','authored-math-proof.json','plane-math-verification.json','cross-math-verification.json','geometry-evidence.json']}
manifest=[];out=[]
for eid,items in sorted(selected.items()):
 q=questions[eid];mid=q.get(':question/math-academy-id');assert mid,('Selected source correction has no MA identity',eid)
 group=items[0]['group'];batch=H/'group-3-wording-delta'if eid in word else H/('commit-'+group);verify=read(batch/'verification.json');assert verify['committed']and verify['only_exact_reviewed_datoms_changed']and verify['exact_readback'];commit_t=verify['basis_t']
 checks=[H/group/name for name in proof_files[group]if(H/group/name).exists()]
 if eid in word:checks+=[H/'group-3-wording-delta/evidence.json',H/'group-3-wording-delta/render-verification.json']
 proof={'question':eid,'source_id':mid,'classifications':items,'readback_basis_t':BASIS,'commit_basis_t':commit_t,'commit_verification':str((batch/'verification.json').relative_to(R)),'proof_files':[{'path':str(p.relative_to(R)),'sha256':sha(p)}for p in checks],'prior_primary_batch_proof':str((H/('commit-'+group)/'verification.json').relative_to(R))if eid in word else None}
 manifest.append(proof)
# Freeze the proof ledger before its hashes are put into the individual records.
proofpath=H/'authored-proof-manifest.json';proofpath.write_text(json.dumps({'basis_t':BASIS,'question_records':manifest,'tutorial_records':tutorials,'scope':'Authored completions and independently proved source mathematical corrections/restorations only; excludes pure font/layout changes.'},default=str,indent=2)+'\n')
for proof in manifest:
 eid=proof['question'];q=questions[eid];mid=proof['source_id'];batch=R/Path(proof['commit_verification']).parent;verify=read(batch/'verification.json');commit_t=verify['basis_t'];fs=[]
 for f in q[':question/answer-fields']:
  right=f[':answer-field/correct'][':db/id'];canonical=next(a for a in f[':answer-field/choices']if a[':db/id']==right);kind=str(f[':answer-field/type'][':db/ident']).split('/')[-1];bank=[canonical]if kind=='blank'else[canonical]+[a for a in f[':answer-field/choices']if a[':db/id']!=right];field={'key':f[':answer-field/key'],'type':kind,'choices':[{'type':str(a[':answer/type'][':db/ident']).split('/')[-1],'value':a[':answer/value']}for a in bank],'correct_value':canonical[':answer/value']}
  if mid in banks:field['protect_choices']=True
  fs.append(field)
 content={'math_academy_id':mid,'problem':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'answer_fields':fs};directory=R/'reference/mathacademy/mathematical-corrections'/('2026-10-29-mth341-'+mid);directory.mkdir(parents=True,exist_ok=True)
 review={'corrected_content':content,'rationale':'Committed authored completion or independently proved mathematical source correction/restoration; retain against reimport of the original source mistake. See per-question proof manifest for exact classifications and proofs.','authorship':'Locally derived or corrected; not claimed as an observed Math Academy key.','independent_proof':str(proofpath.relative_to(R)),'independent_proof_sha256':sha(proofpath),'question_entity':eid,'commit':str(batch.relative_to(R)),'commit_basis_t':commit_t,'readback_basis_t':BASIS,'readback_source':'Fixed actual question/field EDN cache under '+str(D.relative_to(R)),'prior_primary_batch_proof':proof['prior_primary_batch_proof']}
 encoded=json.dumps(review,default=str,ensure_ascii=False,indent=2)+'\n';path=directory/'review.json'
 if path.exists():assert path.read_text()==encoded,('Existing authoring record differs',path)
 else:path.write_text(encoded)
 tx=directory/'transaction.edn'
 if not tx.exists():
  try:os.link(batch/'transaction.edn',tx)
  except OSError:shutil.copyfile(batch/'transaction.edn',tx)
 assert tx.read_bytes()==(batch/'transaction.edn').read_bytes()
 record={'committed':True,'mathematical_check_passed':True,'basis_after':commit_t,'readback_basis_t':BASIS,'review_sha256':sha(path),'transaction_sha256':sha(tx),'learner_and_engine_facts_unchanged':True,'source':':agent/codex','original_verification':str((batch/'verification.json').relative_to(R)),'exact_readback':True,'proof_manifest_sha256':sha(proofpath)}
 (directory/'verification.json').write_text(json.dumps(record,indent=2)+'\n');out.append({'question':eid,'source_id':mid,'directory':str(directory.relative_to(R)),'basis_after':commit_t,'readback_basis_t':BASIS,'protect_choices':mid in banks})
loaded=mathematical_correction_records(R/'reference/mathacademy',{x['source_id']for x in out});assert {r['question']for r in loaded}=={x['source_id']for x in out};protected=[r for r in loaded if r['attribute']=='answer-field/choices'];assert {r['question']for r in protected}==banks
report={'passed':True,'question_records':len(out),'attribute_evidence_records':len(loaded),'guarded_complete_banks':len(protected),'readback_basis_t':BASIS,'basis_after_is_actual_chosen_commit_t':True,'records':out,'tutorials_separately_attributed':'Existing capture.scripts.database.prepare.Preparation.lesson branch; see tutorial-source-guard-verification.json','database_writes':0};(H/'authored-reconciliation-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Registered',len(out),'committed authored question records;',len(loaded),'attribute evidence records;',len(protected),'complete-bank guards; no database operations')
