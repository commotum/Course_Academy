"""Retire demonstrated generated defects without detaching their KP.

Never retract question/answer entities, source questions, or learner history.
Uses the existing guarded preview/submission transport and exact-request recovery.
"""
from pathlib import Path
import uuid

from generator_publish import GeneratorCommitter, StaleBasis, digest, dumps, loads, kw, file_lock
from inventory_jobs import save

POOL_REPAIR_POLICY_VERSION = 2


def generated_proof(row, evidence_root):
    ref=row.get('evidence_path')
    if not isinstance(ref,str) or not ref or Path(ref).is_absolute() or '..' in Path(ref).parts:return False
    path=(Path(evidence_root)/ref).resolve()
    if not path.is_relative_to(Path(evidence_root).resolve()) or not path.is_file():return False
    import json
    try:data=json.loads(path.read_text())
    except (OSError,ValueError):return False
    wanted=str(row.get('question_id'))
    def visit(value):
        if isinstance(value,dict):
            if isinstance(value.get('question'),dict) and value.get('generation') and str(value['question'].get(':question/id'))==wanted:return True
            return any(visit(v) for v in value.values())
        if isinstance(value,list):return any(visit(v) for v in value)
        return False
    return bool(row.get('finding') and row.get('reproduction') and visit(data))


def eligible(question):
    if question.get(':question/math-academy-id'):return False,'original_source'
    if question.get(':knowledge-point/_canonical-example'):return False,'canonical_example'
    if question.get(':question/retired'):return False,'already_retired'
    # Retirement excludes future practice only. Saved task-items, question
    # content, answers, bank membership and grading remain unchanged, including
    # a question already served to another learner or kept in a saved task.
    return True,None


def repair_pool(publisher, kp, reports, directory):
    import json
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    requested={};unresolved=[]
    for report in reports:
        report=Path(report)
        for row in json.loads(report.read_text()).get('affected_questions',[]):
            if not generated_proof(row,report.parent):
                unresolved.append({'question':row,'reason':'Missing reproducible generated-record evidence'});continue
            try:
                qid=str(uuid.UUID(str(row['question_id'])))
                if type(row['entity_id']) is not int or row['entity_id']<=0:raise ValueError('Invalid entity ID')
                eid=row['entity_id']
            except (ValueError,KeyError,TypeError):
                unresolved.append({'question':row,'reason':'Exact question UUID and entity ID are required'});continue
            requested[eid]=qid
    # Several reviews may report the same question. A later incomplete copy
    # does not invalidate the exact generated-record proof already supplied for
    # that same UUID/entity pair. Keep other unproven claims unresolved.
    def duplicate_of_proved(issue):
        row=issue.get('question')
        if not isinstance(row,dict) or type(row.get('entity_id')) is not int:return False
        try:return requested.get(row['entity_id'])==str(uuid.UUID(str(row['question_id'])))
        except (ValueError,KeyError,TypeError):return False
    duplicate_reports=[issue for issue in unresolved if duplicate_of_proved(issue)]
    unresolved=[issue for issue in unresolved if not duplicate_of_proved(issue)]
    client=publisher.client;committer=GeneratorCommitter(publisher.config,client,directory)
    lock=Path(publisher.config.request_directory)/'api.lock'
    with file_lock(lock):
        for attempt in range(3):
            pending=committer.pending()
            protected=[];already_absent=[]
            if pending:
                snapshot=loads(pending['snapshot_edn']);batch=loads(pending['batch_edn'])
                if any(str(a)==':knowledge-point/questions' for _,a,_ in batch['retractions']):
                    raise ValueError('Legacy bank-detachment request requires exact-outcome reconciliation and ownership repair; retained unchanged')
                removed=[int(e) for e,a,v in batch['assertions'] if str(a)==':question/retired' and v is True]
            else:
                status=client.status();basis=status['basis']
                if not requested:
                    result={'retired':[],'unresolved':unresolved,'protected':[],'basis':basis};save(directory/'verification.json',result);return result
                query='[:find (pull ?q [:db/id :question/id :question/math-academy-id :question/retired {:task-item/_content [:db/id]} {:knowledge-point/_canonical-example [:db/id]}]) :in $ ?kp [?q ...] :where [?kp :knowledge-point/questions ?q]]'
                rows=client.query(query,[int(kp),list(requested)],directory,'candidates',basis)
                already_absent=sorted(set(requested)-{question[':db/id'] for [question] in rows})
                removed=[];retired_before={}
                for [question] in rows:
                    eid=question[':db/id']
                    if str(question[':question/id'])!=requested[eid]:raise ValueError('Pool question identity changed')
                    ok,why=eligible(question)
                    if ok:
                        removed.append(eid);retired_before[eid]=question.get(':question/retired')
                    else:
                        protected.append({'question':eid,'reason':why})
                        if why!='already_retired':unresolved.append({'question':eid,'reason':why+' requires a separate content repair'})
                if not removed:
                    result={'retired':[],'already_absent':already_absent,'duplicate_reports':duplicate_reports,
                            'unresolved':unresolved,'protected':protected,'basis':basis};save(directory/'verification.json',result);return result
                attributes=client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],directory,'attributes',basis)
                idents=client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],directory,'idents',basis)
                snapshot={'basis':basis,'lineage':status['lineage'],'attributes':attributes,'idents':idents}
                batch={'source':publisher.config.source,
                    'assertions':[[eid,kw('question/retired'),True] for eid in removed],
                    'retractions':[[eid,kw('question/retired'),False] for eid in removed if retired_before[eid] is False],
                    'forms':[[kw('db/cas'),eid,kw('question/retired'),retired_before[eid],True] for eid in removed]+[[kw('db/ensure'),int(kp),kw('knowledge-point/validate')]]}
                save(directory/'protected.json',protected)
                try:committer.preview(batch,snapshot)
                except StaleBasis:continue
                pending=committer.save_request(batch,snapshot,digest(batch))
            try:receipt=committer.submit(pending)
            except StaleBasis:
                committer.retire(pending,'rejected_stale_basis',{'reason':'Concurrent learner/database change; recheck retirement eligibility'})
                continue
            proof=committer.verify_receipt(pending,receipt);after=receipt[':edb/db-after-t']
            rows=client.query('[:find ?q :in $ ?kp [?q ...] :where [?kp :knowledge-point/questions ?q]]',[int(kp),removed],directory,'membership-readback',after)
            if {r[0] for r in rows}!=set(removed):raise ValueError('Retirement detached question bank ownership')
            rows=client.query('[:find ?q :in $ [?q ...] :where [?q :question/retired true]]',[removed],directory,'retirement-readback',after)
            if {r[0] for r in rows}!=set(removed):raise ValueError('Questions were not retired from fresh practice')
            rows=client.query('[:find ?q ?id :in $ [?q ...] :where [?q :question/id ?id]]',[removed],directory,'entities-preserved',after)
            if {r[0] for r in rows}!=set(removed):raise ValueError('Question entities were not preserved')
            result={'retired':removed,'already_absent':already_absent,'duplicate_reports':duplicate_reports,
                    'unresolved':unresolved,'protected':protected,'basis':after,**proof}
            save(directory/'verification.json',result);committer.retire(pending,'verified',result);return result
    raise RuntimeError('Pool repair repeatedly raced database changes; saved evidence retained')
