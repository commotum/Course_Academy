"""Correct the copied final sine-transform LHS, preserving authentic evidence and keys."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from capture import arguments
from core import atomic_json
from database import Database,StaleBasis
from edn import dumps,kw,loads
from provenance import mathematical_correction_records
WORK=Path(__file__).resolve().parent;SOURCE=ROOT/'reference/mathacademy/question-capture-workers/differential/14074297';AUDIT=ROOT/'.local/question_capture-fleet/de-smoothness-typo-14074297';MID='q-340850'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
state=json.loads((SOURCE/'state.json').read_text());assert all(state.get(k) for k in ['activity_complete','history_complete','import_complete'])
content=json.loads((SOURCE/'content.json').read_text());original=next(q for q in content['questions'] if q['math_academy_id']==MID);corrected=copy.deepcopy(original)
wrong='L{{t}^{2}{e}^{4t}}={{field-4}}';right=r'L{{t}^{2}\operatorname{sin}⁡4t}={{field-4}}'
assert original['problem'].count(wrong)==1 and original['knowledge_point_id']=='6373d849-f5c6-50d2-ad4f-72f77a1a8c92'
corrected['problem']=original['problem'].replace(wrong,right)
assert r'\operatorname{sin}⁡4t' in original['worked_solution']
assert r'\frac{24{s}^{2}-128}{({s}^{2}+16)^{3}}' in original['worked_solution']
if '{t}^{2}{e}^{4t}' in original['worked_solution']:
 assert original['worked_solution'].count('{t}^{2}{e}^{4t}')==1
 corrected['worked_solution']=original['worked_solution'].replace('{t}^{2}{e}^{4t}',r'{t}^{2}\operatorname{sin}⁡4t')
assert original['answer_fields']==corrected['answer_fields']
assert [f['correct_value'] for f in original['answer_fields']]==[r'{F}^{″}(s)',r'\frac{4}{{s}^{2}+16}',r'\frac{24{s}^{2}-128}{({s}^{2}+16)^{3}}',r'\frac{24{s}^{2}-128}{({s}^{2}+16)^{3}}']
after_source=json.loads((SOURCE/'q-340850-after.json').read_text());history=json.loads((SOURCE/'history-q-340850.json').read_text())
assert after_source['worked_solution']==history['worked_solution']==original['worked_solution']
assert after_source['result'] in ('Correct','PartialCredit','Incorrect')
source_paths=[p for p in SOURCE.rglob('*') if p.is_file() and not p.is_relative_to(SOURCE/'solver-session')]
hashes={str(p):sha(p) for p in source_paths}
review_path=WORK/'review.json'
review={'question':MID,'source_capture':str(SOURCE),'original_content':original,'corrected_content':corrected,
 'rationale':'Correct the sole copied exponential in the final conclusion to sin(4t), as uniquely established by the original objective, given sine transform, defined f(t), three accepted stages, unchanged complete final choices, canonical e21838 and authentic graded analogous q341222. Preserve source and authentic final grade; no fields, choices, accepted keys or identities change.',
 'authorized_scope':'Explicitly authorized second and final source investigation/recovery plus guarded content-only study correction.',
 'source_sha256':hashes,'source_grade':after_source['result'],'mathematical_check':json.loads((AUDIT/'review.json').read_text())['mathematical_check'],
 'source_recovery_proof_sha256':sha(AUDIT/'proof.json')}
if review_path.exists():assert json.loads(review_path.read_text())==review
else:atomic_json(review_path,review)
args=arguments(['import-saved','--content',str(SOURCE/'content.json'),'--output',str(SOURCE.parent),'--edb-bin','/home/jake/Developer/EDB/target/release/edb','--database','course-academy-v2','--endpoint','/tmp/course-academy-edb-v2/writer.sock'])
args.capture_root=[ROOT/'reference/mathacademy/question-capture',*[ROOT/'reference/mathacademy/question-capture-workers'/w for w in ['linear','multivariable','differential']]]
db=Database(args);tx_path=WORK/'transaction.edn';intent_path=WORK/'commit-intent.json'
changed={':question/'+a.replace('_','-'):(original[a],corrected[a]) for a in ['problem','worked_solution'] if original[a]!=corrected[a]}
assert ':question/problem' in changed
for attempt in range(2):
 basis=db.basis();before=db.questions([MID],WORK,'before',basis)[MID]
 if intent_path.exists():
  intent=json.loads(intent_path.read_text());assert intent['sha256']==sha(tx_path) and intent['review_sha256']==sha(review_path)
  basis=intent['basis'];before=db.questions([MID],WORK,'before',basis)[MID]
 else:
  assert all(before[a]==old for a,(old,new) in changed.items())
  nohistory=db.query('[:find ?ident :in $ [?ident ...] :where [?a :db/ident ?ident] [?a :db/noHistory true]]',[[kw(a) for a in ['question/problem','question/worked-solution','question/answer-fields','question/version','answer-field/correct','answer/value']]],WORK,'history-retention',basis);assert not nohistory
  tx=[{kw('db/id'):before[':db/id'],**{kw(a):new for a,(old,new) in changed.items()},kw('db/ensure'):[kw('question/validate')]}]
  tx_path.write_text(dumps(tx)+'\n');preview_text=db.command('with','--file',tx_path);(WORK/'preview.edn').write_text(preview_text);preview=loads(preview_text)
  if preview[':edb/db-before-t']!=basis:continue
  guards={'retractions':[[before[':db/id'],kw(a),old] for a,(old,new) in changed.items()],
   'immutable_answers':sorted({c[':db/id'] for f in before[':question/answer-fields'] for c in f[':answer-field/choices']}),
   'immutable_fields':[[f[':db/id'],kw(a)] for f in before[':question/answer-fields'] for a in ['answer-field/id','answer-field/key','answer-field/type','answer-field/correct','answer-field/choices']]}
  attrs=db.attributes(WORK,basis);db.validate_datoms(preview,attrs,**guards);names=dict(attrs)
  datoms=[d for d in preview[':edb/tx-data'] if names[d[1]]!=':db/txInstant'];assert len(datoms)==2*len(changed) and all(d[0]==before[':db/id'] and names[d[1]] in changed for d in datoms)
  (WORK/'guards.edn').write_text(dumps(guards)+'\n');intent={'database':args.database,'endpoint':args.endpoint,'basis':basis,'sha256':sha(tx_path),'review_sha256':sha(review_path),'guards_sha256':sha(WORK/'guards.edn'),'request_key':'ma-mathematical-correction-q-340850-sine-final-'+str(basis)+'-'+sha(tx_path)};atomic_json(intent_path,intent)
 try:receipt=db._commit(intent,tx_path,WORK)
 except StaleBasis:
  intent_path.unlink();continue
 break
else:raise RuntimeError('Two bounded stale-basis previews exhausted')
assert receipt[':edb/committed'] and receipt[':edb/db-before-t']==basis
attrs=db.attributes(WORK,basis);guards=loads((WORK/'guards.edn').read_text());db.validate_datoms(receipt,attrs,**guards);names=dict(attrs)
datoms=[d for d in receipt[':edb/tx-data'] if names[d[1]]!=':db/txInstant'];assert len(datoms)==2*len(changed) and all(d[0]==before[':db/id'] and names[d[1]] in changed for d in datoms)
after_basis=receipt[':edb/db-after-t'];current=db.questions([MID],WORK,'after',after_basis)[MID]
assert all(current[a]==new for a,(old,new) in changed.items())
assert {k:v for k,v in before.items() if k not in changed}=={k:v for k,v in current.items() if k not in changed}
assert db.questions([MID],WORK,'historical-original',basis)[MID]==before
verification={'committed':True,'basis_before':basis,'basis_after':after_basis,'mathematical_check_passed':True,'review_sha256':sha(review_path),'transaction_sha256':sha(tx_path),'historical_original_question_retained':True,'answer_fields_choices_and_answer_identities_unchanged':True,'learner_and_engine_facts_unchanged':True,'source_grade':after_source['result'],'receipt':str(WORK/'commit.edn'),'receipt_content_datom_count':len(datoms),'changed_attributes':sorted(changed)};atomic_json(WORK/'verification.json',verification)
assert len(mathematical_correction_records(ROOT/'reference/mathacademy',{MID}))==6
noop=db.import_content({**content,'questions':[original],'canonical_examples':[]},WORK/'original-source-reimport',apply=False);assert noop.get('already_complete') and noop['database_writes']==0
assert all(sha(Path(p))==h for p,h in hashes.items())
verification.update(original_source_reimport_is_noop=True,original_source_reimport_preview=noop,original_source_sha256_unchanged=True);atomic_json(WORK/'verification.json',verification)
print(json.dumps(verification,indent=2))
