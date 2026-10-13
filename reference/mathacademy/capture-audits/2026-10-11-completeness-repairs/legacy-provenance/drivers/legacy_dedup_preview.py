import json, threading, time, hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from scripts.storage import read_json, atomic_json, file_lock
from scripts.config import Config
from scripts.legacy_recovery import aggregate_source_repairs
from scripts.database.client import EDBClient, QUESTION_PULL
from scripts.database.prepare import ALLOWED
from scripts.database.pipeline import DatabasePipeline
from scripts.database.images import ImageLibrary
from scripts.database.edn import kw, loads

root=Path('reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance')
mids=['q-136291','q-181303','q-41957','q-51054']; config=Config()
package=aggregate_source_repairs(root,read_json(root/'database-structural-repair-candidates.json')['prepared'],mids,'structural')
directory=Path(package['directory']); content=read_json(directory/'content.json'); evidence=read_json(directory/'source-evidence.json')
questions=[ImageLibrary(config.math_root,directory).question(q) for q in content['questions']]
client=EDBClient(config,threading.Event());proof=root/'duplicate-field-repair-preview'/str(time.time_ns());proof.mkdir(parents=True)
typed=lambda a:(a[':answer/type'][':db/ident'].rsplit('/',1)[-1],a[':answer/value'])
with file_lock(config.database_lock):
    before=client.status();old={row[0][':question/math-academy-id']:row[0] for row in client.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?mid ...] :where [?q :question/math-academy-id ?mid]]',[mids],proof,'before',before['basis'])}
    assert set(old)==set(mids);rows=[];entity_ids=set();answer_ids=set();field_ids=set();allowed_retractions=set()
    for q in questions:
        mid=q['math_academy_id'];held=old[mid];binding=next(b for b in evidence['bindings'] if b['id']==mid)
        raw=read_json(Path(binding['directory'])/'state.json')['questions'][mid]['before'];dom=BeautifulSoup(raw['html'],'html.parser')
        assert len(raw['fields'])==len(q['answer_fields'])==1
        assert raw['fields'][0]['type']==q['answer_fields'][0]['type']=='radio'
        tables=dom.select('.questionWidget-choicesTable');assert len(tables)==1
        circles=tables[0].select('.questionWidget-choiceLetterCircle')
        assert len(circles)==len(raw['fields'][0]['choices'])==len(q['answer_fields'][0]['choices'])==5
        assert [c.get('id') for c in circles]==['questionWidget-choiceLetterCircle-'+mid.removeprefix('q-')+'-'+str(c['option']) for c in raw['fields'][0]['choices']]
        incoming=q['answer_fields'][0];wanted={(c['type'],c['value']) for c in incoming['choices']};correct=(incoming['correct_type'],incoming['correct_value'])
        matches=[f for f in held[':question/answer-fields'] if f[':answer-field/key']==incoming['key'] and f[':answer-field/type'][':db/ident'].endswith('/radio') and {typed(c) for c in f[':answer-field/choices']}==wanted and f.get(':answer-field/correct') and typed(f[':answer-field/correct'])==correct]
        assert len(matches)==1;retained=matches[0];removed=[f for f in held[':question/answer-fields'] if f[':db/id']!=retained[':db/id']]
        assert len(removed)==1
        entity_ids.add(held[':db/id'])
        for f in held[':question/answer-fields']:
            field_ids.add(f[':db/id']);entity_ids.add(f[':db/id'])
            for a in f[':answer-field/choices']:
                entity_ids.add(a[':db/id']);answer_ids.add(a[':db/id']);assert not a.get(':task-item/_responses')
            if f.get(':answer-field/correct'):entity_ids.add(f[':answer-field/correct'][':db/id']);answer_ids.add(f[':answer-field/correct'][':db/id'])
        allowed_retractions.add((held[':db/id'],removed[0][':db/id']))
        rows.append({'id':mid,'question_uuid':str(held[':question/id']),'original_physical_field_count':1,'original_circle_ids':[c.get('id') for c in circles],'original_html_sha256':hashlib.sha256(raw['html'].encode()).hexdigest(),'retained_exact_source_field_eid':retained[':db/id'],'retained_exact_source_field_uuid':str(retained[':answer-field/id']),'retained_field':retained,'removed_question_link_field_eids':[f[':db/id'] for f in removed],'removed_field_entities_retained':removed,'source_hash':binding['source_hash']})
    attrs=[kw(':'+a) for a in ALLOWED if a.startswith(('question/','answer-field/','answer/')) and not a.endswith('/id')]
    sources=client.query('[:find ?e ?a ?source :in $ [?e ...] [?a ...] :where [?e ?a _ _ ?s] [?s :db/ident ?source]]',[sorted(entity_ids),attrs],proof,'all-active-authored-sources',before['basis'])
    assert sources and {str(row[-1]) for row in sources}=={':org/Math-Academy'}
    owners=client.query('[:find ?answer ?item :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',[sorted(answer_ids)],proof,'all-answer-response-owners',before['basis']);assert not owners
    client.query('[:find (pull ?f [* {:answer-field/type [:db/id :db/ident]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',[sorted(field_ids)],proof,'all-retained-field-entities',before['basis'])
    client.query('[:find (pull ?a [* {:answer/type [:db/id :db/ident]}]) :in $ [?a ...] :where [?a :answer/id _]]',[sorted(answer_ids)],proof,'all-retained-answer-entities',before['basis'])
    result=DatabasePipeline(config,threading.Event()).process(directory,apply=False);assert result['status']=='previewed' and not result.get('omissions')
    transaction=loads((directory/'database/transaction.edn').read_text());actual_retractions=set()
    for edit in transaction:
        if isinstance(edit,dict):
            assert edit[kw(':db/id')] in {q[':db/id'] for q in old.values()}
            assert set(edit)-{kw(':db/id'),kw(':db/ensure')}<=set(map(kw,(':question/problem',':question/worked-solution')))
        else:
            assert len(edit)==4 and str(edit[0])==':db/retract' and str(edit[2])==':question/answer-fields'
            assert (edit[1],edit[3]) in allowed_retractions;actual_retractions.add((edit[1],edit[3]))
    assert actual_retractions==allowed_retractions
    output={'package':package,'before':before,'preview':result,'questions':rows,'active_fact_sources':sources,'all_answer_native_response_owners':owners,'readback_directory':str(proof),'transaction_edits':len(transaction),'database_writes':0,'checks':{'one_original_physical_radio_field_per_question':True,'unique_existing_full_source_signature_match':True,'all_old_and_new_field_answers_unowned':True,'all_authored_active_sources_MA':True,'only_question_text_and_four_exact_obsolete_field_link_retractions':True}}
    atomic_json(proof/'preview-proof.json',json.loads(json.dumps(output,default=str)));atomic_json(root/'duplicate-field-repair-preview.json',json.loads(json.dumps(output,default=str)))
    print(json.dumps({'directory':str(directory),'proof':str(proof),'questions':mids,'transaction_edits':len(transaction),'status':result['status']}))
