"""Content-only recovery at activity boundaries. Never calls a browser or model."""
import hashlib
import json
import logging
import re
from pathlib import Path

from core import ROOT, atomic_json, journal
from database import StaleBasis
from edn import loads
from native_comparison import availability
from retry_policy import completion_outcome

MAX_ATTEMPTS = 20
PACKAGE = Path(__file__).parent


def read_json(path):
    return json.loads(path.read_text()) if path.exists() else {}


def confirmed_completion(state):
    kind = state.get('task_type','lesson')
    if not state.get('activity_complete') or not state.get(kind+'_complete'):
        return False
    completion = state.get('completion','')
    if kind in ('lesson','review'):
        if completion_outcome(completion, kind) is None:
            return False
    elif kind == 'assessment':
        count = state.get('assessment_question_count')
        status = state.get('test_submission_status')
        suffix = '(?:questions|answered)' if status == 'expired' else 'questions'
        if (status not in ('completed','expired') or not count or
                status == 'expired' and not re.search(r'\bexpired\b',completion,re.I) or
                not re.search(r'\bof\s+'+str(count)+r'\s+'+suffix+r'\b',completion,re.I)):
            return False
    elif kind == 'multistep':
        if 'completed the task' not in completion.lower():
            return False
    elif kind == 'diagnostic':
        from diagnostic import completed_url
        if (not state.get('diagnostic_id') or not state.get('diagnostic_question_count') or
                not completed_url(state, state.get('diagnostic_completion_url','')) or
                completion != 'Diagnostic completed: '+state['diagnostic_completion_url']):
            return False
    else:
        return False
    return True


def eligible(directory, state, content):
    if (not confirmed_completion(state) or not state.get('history_complete') or
            not content.get('content_only') or content.get('task_id') != state.get('task_id') or
            content.get('task_type','lesson') != state.get('task_type','lesson')):
        return False
    questions = {q['math_academy_id']:q for q in content.get('questions',[])}
    records = state.get('questions',{})
    if not records or len(questions) != len(content['questions']) or set(questions) != set(records):
        return False
    if state.get('task_type') == 'assessment' and len(records) != state.get('assessment_question_count'):
        return False
    if state.get('task_type') == 'diagnostic' and (
            len(records) != state.get('diagnostic_question_count') or
            set(state.get('diagnostic_question_order',[])) != set(records) or
            content.get('question_order') != state.get('diagnostic_question_order')):
        return False
    if state.get('task_type') == 'multistep' and (
            set(state.get('multistep_question_order',[])) != set(records) or
            content.get('question_order') != state.get('multistep_question_order')):
        return False
    if any(not r.get('finalized') or r.get('content') != questions[mid] or
           not r.get('history',{}).get('worked_solution') or
           r['history']['worked_solution'] != questions[mid].get('worked_solution') for mid,r in records.items()):
        return False
    metadata = read_json(directory/'activity-metadata.json')
    if (not isinstance(metadata,list) or len(metadata) != len(records) or
            {q['id'].replace('question-','q-') for q in metadata} != set(records)):
        return False
    examples = list(state.get('examples',{}).values())
    if sorted(examples,key=lambda q:q['math_academy_id']) != sorted(content.get('canonical_examples',[]),key=lambda q:q['math_academy_id']):
        return False
    return True


def version():
    """Only effective importer/comparison changes reset ordinary retries."""
    digest = hashlib.sha256()
    paths = [PACKAGE/name for name in ('core.py','database.py','edb_transport.py','edn.py',
                                      'provenance.py','math_notation.py','native_comparison.py','import_repair.py')]
    # The checker runs an installed executable, not its Rust source files.
    # Unbuilt edits and changes to sweep bookkeeping cannot fix old imports.
    # availability() below hashes the actual executable when it changes.
    for path in paths:
        if path.exists():
            digest.update(str(path.relative_to(ROOT)).encode())
            digest.update(path.read_bytes())
    digest.update(repr(availability()).encode())
    # These are the durable authoring inputs used by Reconciler. Changes are
    # genuine new evidence, unlike database basis changes on every live task.
    evidence = ROOT/'reference/mathacademy'
    names = ['factorials-13831129/'+name for name in ('authored-worked-solutions.json',
        'completion-review.json','review.json','content.json','transaction.edn','verification.json',
        'completion-transaction.edn','completion-verification.json','worked-solutions-transaction.edn',
        'worked-solutions-verification.json')]
    names += ['history-question-import-2026-10-04/'+name for name in
        ('import-ready/questions.json','import-ready/database-import/transaction.edn',
         'import-ready/database-import/verification.json','format-audit/repairs.json',
         'format-audit/database-repair/transaction.edn','format-audit/database-repair/verification.json')]
    for name in names:
        path = evidence/name
        if path.is_file():
            digest.update(name.encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def retry_key(directory, state, generation, args, prior_evidence=()):
    digest = hashlib.sha256((generation+str(bool(args.preview))+args.database+args.endpoint).encode())
    # Do not include mutable import flags, deferrals or timestamps: recording a
    # failure must not itself authorize another attempt on the next invocation.
    evidence = {k:state.get(k) for k in ('task_id','task_type','activity_complete','history_complete',
                'completion','questions','examples','kps','assessment_question_count','test_submission_status')}
    digest.update(json.dumps(evidence,sort_keys=True).encode())
    digest.update(json.dumps(prior_evidence,sort_keys=True).encode())
    names = ['content.json','activity-metadata.json','assets/manifest.json','answer-source-reviews.json',
             'edb-import/commit-intent.json','edb-import/commit.edn',
             'edb-import/transaction.edn','edb-import/reconciliation.edn']
    from provenance import field_layout_retry_evidence
    digest.update(json.dumps(field_layout_retry_evidence(directory),sort_keys=True).encode())
    names += [str(p.relative_to(directory)) for p in sorted(directory.glob('example-*.json'))]
    for name in names:
        path = directory/name
        digest.update(name.encode())
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def verified(directory, content):
    proof = read_json(directory/'edb-import/verification.json')
    current = hashlib.sha256(json.dumps(content,sort_keys=True,default=str).encode()).hexdigest()
    if proof.get('content_sha256') and proof['content_sha256'] != current:
        return False
    if not (proof.get('already_complete') and proof.get('database_writes') == 0 or
            proof.get('committed') and proof.get('reimport_is_noop') and
            proof.get('learner_and_engine_facts_unchanged')):
        return False
    receipts = directory/'edb-import'
    archive = proof.get('receipt_archive')
    if archive:
        # The one-time canonical-example payload migration archived committed
        # intents. Its audited hash transition is recorded on the verification,
        # not inferred from a missing receipt or a checkpoint flag.
        if archive != 'committed-before-capture-format-migration' or not proof.get('content_sha256'):
            return False
        receipts = receipts/archive
    if proof.get('committed'):
        receipt = receipts/'commit.edn'
        if not receipt.exists() or loads(receipt.read_text()).get(':edb/committed') is not True:
            return False
        if archive:
            committed = loads(receipt.read_text())
            if (committed.get(':edb/db-before-t') != proof.get('basis_before') or
                    committed.get(':edb/db-after-t') != proof.get('basis_after')):
                return False
    intent = read_json(receipts/'commit-intent.json')
    if archive and not intent:
        return False
    if intent:
        attested = proof.get('original_content_sha256') if archive else current
        if attested != intent.get('content_sha256'):
            return False
        if archive:
            historical = json.loads(json.dumps(content))
            for question in historical.get('questions',[]):
                question['is_example'] = False
            for example in historical.get('canonical_examples',[]):
                example['is_example'] = True
            if hashlib.sha256(json.dumps(historical,sort_keys=True,default=str).encode()).hexdigest() != attested:
                return False
        for name,key in [('transaction.edn','sha256'),('reconciliation.edn','reconciliation_sha256')]:
            path = receipts/name
            if intent.get(key) and (not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != intent[key]):
                return False
        receipt = receipts/'commit.edn'
        if not receipt.exists() or loads(receipt.read_text()).get(':edb/committed') is not True:
            return False
    return True


def complete(args, directory, state, result):
    flag = 'preview_complete' if args.preview else 'import_complete'
    changed = not state.get(flag) or bool(state.get('deferred_error'))
    if not changed:
        return
    state[flag] = True
    if flag == 'import_complete':
        state.pop('import_deferred',None)
    if state.get('history_complete') or state.get('deferred_error',{}).get('phase') in ('import','queue-after'):
        state.pop('deferred_error',None)
    atomic_json(directory/'state.json',state)
    journal(args.state_dir/'journal.jsonl','content_previewed' if args.preview else 'content_imported',
            task_id=state['task_id'], directory=str(directory), **result)


def sweep(db, args, *, trigger, exclude=(), repair_budget=None):
    """At most 20 attempts; one per capture and evidence/version/mode key.

    repair_budget limits model diagnoses, not ordinary saved-content retries.
    Budget-postponed repairs remain eligible at later boundaries.
    Persist started *before* importing, and the final key afterwards so newly
    created intent artifacts cannot cause an unchanged failure to loop. Only
    Database.import_content may recover, preview, plan, commit or verify.
    """
    if getattr(args,'dry_run',False) or getattr(args,'capture_only',False):
        return []
    sources = sorted(args.output.glob('*/state.json'))
    states = []
    for source in sources:
        try:
            state = read_json(source)
            if (state.get('task_type') in ('assessment','diagnostic') and
                    (state.get('assessment_started') or state.get('diagnostic_started') or state.get('diagnostic_start_intent')) and
                    not confirmed_completion(state)):
                logging.info('Saved import sweep deferred until assessment completion')
                return []
            states.append((source.parent,state))
        except (ValueError,OSError) as error:
            logging.warning('Cannot inspect saved capture %s: %s',source,error)
    excluded = {Path(p).resolve() for p in exclude}
    ledger_path = args.state_dir/'saved-import-attempts.json'
    try:
        ledger = read_json(ledger_path)
        generation = version()
    except (ValueError,OSError) as error:
        logging.warning('Saved import retry bookkeeping needs inspection: %s',error)
        return []
    # Prior verified MA evidence for the same IDs can resolve an unknown-origin
    # case. Unrelated newly captured questions must not reset its retry bound.
    prior = {}
    for directory,state in states:
        try:
            proof = read_json(directory/'edb-import/verification.json')
            if proof.get('committed') and proof.get('reimport_is_noop'):
                for mid,record in state.get('questions',{}).items():
                    prior.setdefault(mid,[]).append({'directory':str(directory),'record':record,'proof':proof})
                for mid,example in state.get('examples',{}).items():
                    prior.setdefault(mid,[]).append({'directory':str(directory),'example':example,'proof':proof})
        except (ValueError,OSError,AttributeError) as error:
            logging.warning('Cannot inspect prior MA evidence %s: %s',directory,error)
    outcomes = []
    remaining_repairs = repair_budget
    repair_postponed = False
    def can_repair():
        nonlocal remaining_repairs, repair_postponed
        if remaining_repairs is None:
            return True
        if remaining_repairs <= 0:
            repair_postponed = True
            return False
        remaining_repairs -= 1
        return True
    for directory,state in states:
        if directory.resolve() in excluded:
            continue
        stop = getattr(args,'stop_event',None)
        if stop is not None and stop.is_set():
            raise KeyboardInterrupt('Stopped before saved import')
        try:
            content = read_json(directory/'content.json')
            if not eligible(directory,state,content):
                continue
            if verified(directory,content):
                complete(args,directory,state,read_json(directory/'edb-import/verification.json'))
                continue
            identity = str(directory.resolve())
            related = [r for q in content['questions']+content.get('canonical_examples',[])
                       for r in prior.get(q['math_academy_id'],[]) if Path(r['directory']) != directory]
            key = retry_key(directory,state,generation,args,related)
            previous = ledger.get(identity,{})
            if (previous.get('key') == key and
                    previous.get('status') != 'contention_pending' and
                    (previous.get('status') != 'repair_pending' or remaining_repairs == 0)):
                continue
            if len(outcomes) >= MAX_ATTEMPTS:
                break
            ledger[identity] = {'key':key, 'status':'started', 'trigger':trigger}
            atomic_json(ledger_path,ledger)
            repair_postponed = False
            try:
                from import_repair import import_with_repair
                result = import_with_repair(db,content,directory,state,args,revisit=False,can_repair=can_repair)
                if not (result.get('previewed') or result.get('committed') or result.get('already_complete')):
                    raise ValueError('Pending commit intent retained; preview cannot recover a commit')
                complete(args,directory,state,result)
                status, error_text = 'complete', None
            except Exception as error:
                status = ('contention_pending' if isinstance(error,StaleBasis) else
                          'repair_pending' if repair_postponed else 'deferred')
                error_text = str(error)
                state['deferred_error'] = {'phase':'import','message':str(error)}
                atomic_json(directory/'state.json',state)
                journal(args.state_dir/'journal.jsonl','saved_import_deferred',task_id=state['task_id'],
                        directory=str(directory),trigger=trigger,error_type=type(error).__name__,message=str(error))
                if status == 'contention_pending':
                    logging.info('Saved import %s will retry database contention at the next sweep',directory)
                elif repair_postponed:
                    logging.info('Saved import %s is queued for repair after live capture resumes',directory)
                else:
                    logging.warning('Saved import %s remains deferred: %s',directory,error)
            ledger[identity] = {'key':retry_key(directory,state,generation,args,related), 'status':status,
                                'trigger':trigger, 'error':error_text}
            atomic_json(ledger_path,ledger)
            outcomes.append({'directory':str(directory),'status':status,'error':error_text})
        except (ValueError,OSError,KeyError,TypeError) as error:
            logging.warning('Cannot inspect saved import %s: %s',directory,error)
    return outcomes
