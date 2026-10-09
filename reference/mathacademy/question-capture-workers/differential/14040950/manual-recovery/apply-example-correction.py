"""Reviewed scalar-only example correction; exact receipt and readback audit."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[6]/'scripts/question_capture'))
from capture import arguments
from core import atomic_json,build_content_transaction
from database import Database,StaleBasis
from edn import dumps,kw,loads
from provenance import mathematical_correction_records

ROOT=Path('/home/jake/Developer/Course_Academy')
activity=ROOT/'reference/mathacademy/question-capture-workers/differential/14040950'
work=ROOT/'reference/mathacademy/mathematical-corrections/e-21715'
review=json.loads((work/'review.json').read_text());original=review['original_content'];corrected=review['corrected_content']
args=arguments(['import-saved','--output',str(activity.parent),'--content',str(activity/'content.json')])
args.capture_root=[ROOT/'reference/mathacademy/question-capture',*[(ROOT/'reference/mathacademy/question-capture-workers'/n) for n in ['linear','multivariable','differential']]]
db=Database(args)
for attempt in range(3):
    intent_path=work/'commit-intent.json'
    if intent_path.exists():
        intent=json.loads(intent_path.read_text());basis=intent['basis'];tx_path=work/'transaction.edn'
    else:
        basis=db.basis();old=db.questions(['e-21715'],work,'before',basis)['e-21715']
        assert old[':question/problem']==original['problem']
        assert old[':question/worked-solution']==original['worked_solution']
        nohistory=db.query('[:find ?value :in $ ?ident :where [?attribute :db/ident ?ident] [?attribute :db/noHistory ?value]]',[kw('question/worked-solution')],work,'no-history',basis)
        assert not any(row[0] is True for row in nohistory)
        assert not old.get(':question/answer-fields')
        tx=[{kw('db/id'):old[':db/id'],kw('question/worked-solution'):corrected['worked_solution'],kw('db/ensure'):[kw('question/validate')]}]
        tx_path=work/'transaction.edn';tx_path.write_text(dumps(tx)+'\n')
        preview_text=db.command('with','--file',tx_path);(work/'preview.edn').write_text(preview_text);preview=loads(preview_text)
        if preview[':edb/db-before-t']!=basis:continue
        attributes=db.attributes(work,basis)
        retractions=[[old[':db/id'],kw('question/worked-solution'),original['worked_solution']]]
        db.validate_datoms(preview,attributes,retractions)
        reconciliation={'retractions':retractions,'immutable_answers':[],'immutable_fields':[]}
        (work/'reconciliation.edn').write_text(dumps(reconciliation)+'\n')
        digest=hashlib.sha256(tx_path.read_bytes()).hexdigest()
        intent={'database':args.database,'endpoint':args.endpoint,'basis':basis,'sha256':digest,
                'content_sha256':hashlib.sha256(json.dumps(corrected,sort_keys=True).encode()).hexdigest(),
                'request_key':'ma-mathematical-correction-e-21715-'+str(basis)+'-'+digest,
                'reconciliation_sha256':hashlib.sha256((work/'reconciliation.edn').read_bytes()).hexdigest()}
        atomic_json(intent_path,intent)
    try:receipt=db._commit(intent,tx_path,work)
    except StaleBasis:continue
    break
else:raise RuntimeError('Three bounded stale-basis attempts exhausted')
assert receipt[':edb/db-before-t']==basis
attributes=db.attributes(work,basis);frozen=loads((work/'reconciliation.edn').read_text())
db.validate_datoms(receipt,attributes,frozen['retractions'])
after=receipt[':edb/db-after-t'];current=db.questions(['e-21715'],work,'after',after)['e-21715']
before=db.questions(['e-21715'],work,'original-retained',basis)['e-21715']
assert before[':question/worked-solution']==original['worked_solution']
assert current[':question/worked-solution']==corrected['worked_solution']
assert current[':question/problem']==original['problem']
assert current[':question/id']==before[':question/id']
assert current.get(':question/answer-fields',[])==before.get(':question/answer-fields',[])
for key in set(before)|set(current):
    if key!=':question/worked-solution':assert current.get(key)==before.get(key),(key,current.get(key),before.get(key))
verification={'committed':True,'basis_before':basis,'basis_after':after,'mathematical_check_passed':True,
    'historical_original_question_retained':True,'answer_fields_unchanged':True,
    'learner_and_engine_facts_unchanged':True,'verification_method':'committed_content_datoms_and_exact_question_readback',
    'review_sha256':hashlib.sha256((work/'review.json').read_bytes()).hexdigest(),
    'transaction_sha256':hashlib.sha256(tx_path.read_bytes()).hexdigest()}
atomic_json(work/'verification.json',verification)
assert len(mathematical_correction_records(ROOT/'reference/mathacademy',{'e-21715'}))==2
content=json.loads((activity/'content.json').read_text())
noop=db.import_content(content,activity/'manual-recovery/source-reimport-check',apply=False)
assert noop.get('already_complete') and noop['database_writes']==0
verification['original_source_reimport_is_noop']=True
atomic_json(work/'verification.json',verification)
print(json.dumps(verification,indent=2))
