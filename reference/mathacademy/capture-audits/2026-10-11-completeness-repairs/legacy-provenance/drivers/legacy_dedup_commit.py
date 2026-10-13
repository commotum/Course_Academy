import json, hashlib, threading, time
from pathlib import Path
from scripts.config import Config
from scripts.storage import read_json, atomic_json, file_lock
from scripts.legacy_recovery import current_supported_reviews, authoritative_question, source_record
from scripts.database.client import EDBClient, QUESTION_PULL
from scripts.database.prepare import ALLOWED
from scripts.database.pipeline import DatabasePipeline
from scripts.database.images import ImageLibrary
from scripts.database.edn import kw, loads
from scripts.database.text import markdown

root=Path('reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance')
approval=read_json(root/'duplicate-field-repair-preview.json'); package=approval['package'];directory=Path(package['directory'])
content=read_json(directory/'content.json');evidence=read_json(directory/'source-evidence.json');reviewed=current_supported_reviews(root)
assert hashlib.sha256(json.dumps(content,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==evidence['content_sha256']
original_content_hashes={}
for q in content['questions']:
    mid=q['math_academy_id'];binding=next(b for b in evidence['bindings'] if b['id']==mid)
    assert q==authoritative_question(reviewed[mid]['question']) and reviewed[mid]['source_hash']==binding['source_hash']
    assert hashlib.sha256(json.dumps(source_record(Path(binding['directory']),mid),sort_keys=True,ensure_ascii=False).encode()).hexdigest()==binding['source_hash']
    assert hashlib.sha256(Path(binding['state_file']).read_bytes()).hexdigest()==binding['state_sha256']
    path=Path(binding['directory'])/'content.json';original_content_hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
config=Config();client=EDBClient(config,threading.Event());questions=[ImageLibrary(config.math_root,directory).question(q) for q in content['questions']]
mids=package['question_ids'];assert mids==['q-136291','q-181303','q-41957','q-51054']
proof=root/'verified-duplicate-field-readbacks'/str(time.time_ns());proof.mkdir(parents=True)
typed=lambda a:(a[':answer/type'][':db/ident'].rsplit('/',1)[-1],a[':answer/value'])
query='[:find (pull ?q '+QUESTION_PULL+') :in $ [?mid ...] :where [?q :question/math-academy-id ?mid]]'
def pull(name,basis):return {row[0][':question/math-academy-id']:row[0] for row in client.query(query,[mids],proof,name,basis)}
with file_lock(config.database_lock):
    before=client.status();old=pull('before',before['basis']);assert set(old)==set(mids)
    retained={};allowed_retractions=set();ids=set();answer_ids=set();field_ids=set()
    for q in questions:
        mid=q['math_academy_id'];held=old[mid];incoming=q['answer_fields'][0]
        assert len(q['answer_fields'])==1 and len(held[':question/answer-fields'])==2
        wanted={(c['type'],c['value']) for c in incoming['choices']};correct=(incoming['correct_type'],incoming['correct_value'])
        matches=[f for f in held[':question/answer-fields'] if f[':answer-field/key']==incoming['key'] and f[':answer-field/type'][':db/ident'].endswith('/radio') and {typed(c) for c in f[':answer-field/choices']}==wanted and f.get(':answer-field/correct') and typed(f[':answer-field/correct'])==correct]
        assert len(matches)==1;retained[mid]=matches[0]
        expected=next(row for row in approval['questions'] if row['id']==mid)
        assert matches[0][':db/id']==expected['retained_exact_source_field_eid']
        removed=[f for f in held[':question/answer-fields'] if f[':db/id']!=matches[0][':db/id']]
        assert [f[':db/id'] for f in removed]==expected['removed_question_link_field_eids']
        allowed_retractions.add((held[':db/id'],removed[0][':db/id']));ids.add(held[':db/id'])
        for f in held[':question/answer-fields']:
            ids.add(f[':db/id']);field_ids.add(f[':db/id'])
            for a in f[':answer-field/choices']:
                assert not a.get(':task-item/_responses');ids.add(a[':db/id']);answer_ids.add(a[':db/id'])
            if f.get(':answer-field/correct'):ids.add(f[':answer-field/correct'][':db/id']);answer_ids.add(f[':answer-field/correct'][':db/id'])
    attrs=[kw(':'+a) for a in ALLOWED if a.startswith(('question/','answer-field/','answer/')) and not a.endswith('/id')]
    sources=client.query('[:find ?e ?a ?source :in $ [?e ...] [?a ...] :where [?e ?a _ _ ?s] [?s :db/ident ?source]]',[sorted(ids),attrs],proof,'all-active-authored-sources',before['basis']);assert sources and {str(row[-1]) for row in sources}=={':org/Math-Academy'}
    owners=client.query('[:find ?answer ?item :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',[sorted(answer_ids)],proof,'all-answer-response-owners',before['basis']);assert not owners
    field_query='[:find (pull ?f [* {:answer-field/type [:db/id :db/ident]}]) :in $ [?f ...] :where [?f :answer-field/id _]]'
    answer_query='[:find (pull ?a [* {:answer/type [:db/id :db/ident]}]) :in $ [?a ...] :where [?a :answer/id _]]'
    old_fields=client.query(field_query,[sorted(field_ids)],proof,'old-all-field-entities',before['basis']);old_answers=client.query(answer_query,[sorted(answer_ids)],proof,'old-all-answer-entities',before['basis'])
    pipeline=DatabasePipeline(config,threading.Event());preview=pipeline.process(directory,apply=False);assert preview['status']=='previewed' and not preview.get('omissions')
    transaction=loads((directory/'database/transaction.edn').read_text());actual_retractions=set();qids={q[':db/id'] for q in old.values()}
    for edit in transaction:
        if isinstance(edit,dict):assert edit[kw(':db/id')] in qids and set(edit)-{kw(':db/id'),kw(':db/ensure')}<=set(map(kw,(':question/problem',':question/worked-solution')))
        else:
            assert len(edit)==4 and str(edit[0])==':db/retract' and str(edit[2])==':question/answer-fields'
            assert (edit[1],edit[3]) in allowed_retractions;actual_retractions.add((edit[1],edit[3]))
    assert actual_retractions==allowed_retractions
    result=pipeline.process(directory,apply=True);assert result['status']=='verified' and not result.get('omissions')
    after=client.status();new=pull('after',after['basis'])
    for q in questions:
        mid=q['math_academy_id'];prior=old[mid];current=new[mid]
        assert current[':question/id']==prior[':question/id']
        assert current[':question/problem']==markdown(q['problem']) and current[':question/worked-solution']==markdown(q['worked_solution'])
        assert len(current[':question/answer-fields'])==1 and current[':question/answer-fields'][0]==retained[mid]
        mutable={':question/problem',':question/worked-solution',':question/answer-fields'}
        assert {k:v for k,v in prior.items() if k not in mutable}=={k:v for k,v in current.items() if k not in mutable}
    new_fields=client.query(field_query,[sorted(field_ids)],proof,'after-all-retained-field-entities',after['basis']);new_answers=client.query(answer_query,[sorted(answer_ids)],proof,'after-all-retained-answer-entities',after['basis'])
    key=lambda row:row[0][':db/id'];assert sorted(old_fields,key=key)==sorted(new_fields,key=key);assert sorted(old_answers,key=key)==sorted(new_answers,key=key)
    assert all(receipt['learner_and_engine_facts_unchanged'] for receipt in result['receipts'])
    second=pipeline.process(directory,apply=True);assert second['status']=='no_changes' and not second.get('omissions')
    for path,digest in original_content_hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest
    for binding in evidence['bindings']:assert hashlib.sha256(Path(binding['state_file']).read_bytes()).hexdigest()==binding['state_sha256']
    outcome={**package,'status':'verified','before':before,'after':after,'preview':preview,'result':result,'second_prepare':second,'readback_directory':str(proof),'checks':{'question_uuids_stable':True,'unique_source_exact_field_uuid_preserved':True,'all_original_field_and_answer_entities_byte_identical':True,'only_four_obsolete_unowned_question_field_links_removed':True,'source_problem_solution_exact':True,'original_capture_state_and_content_unchanged':True,'learner_engine_facts_unchanged':True,'second_prepare_noop':True}}
    atomic_json(proof/'verification.json',outcome);atomic_json(root/'database-duplicate-field-repair-commits.json',{'commits':[outcome]});print(json.dumps(outcome))
