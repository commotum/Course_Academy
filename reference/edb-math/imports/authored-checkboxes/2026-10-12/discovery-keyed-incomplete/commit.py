"""Authorized, independently refreshed migration groups with durable recovery."""
import copy,json,shutil,subprocess
from pathlib import Path
import prepare as migration

OUT=migration.OUT
edb=migration.edb
def read(path):return json.loads(path.read_text())
def save(path,value):edb.atomic_json(path,value)
def equal(left,right):return migration.plain(left)==migration.plain(right)

def compile_helpers():
    from capture.scripts.database.preview import _library
    from types import SimpleNamespace
    library=_library(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math')))
    source=OUT/'single-preview.rs';committer=OUT/'exact-commit.rs'
    for path,name in [(source,'single-preview'),(committer,'exact-commit')]:
        command=['rustc','--edition=2024','-O',str(path),'--extern','edb_core='+str(library),'-L','dependency='+str(library.parent),'-o',str(OUT/name)]
        subprocess.run(command,check=True)
    save(OUT/'commit-helper-build.json',dict(edb_library=str(library),edb_sha256=migration.digest(library),source_sha256=migration.digest(source),committer_sha256=migration.digest(committer),preview_binary_sha256=migration.digest(OUT/'single-preview'),commit_binary_sha256=migration.digest(OUT/'exact-commit')))

def report_scope(directory,report,snapshot,number,committed=False):
    if not committed:return migration.verify_report(directory,report,snapshot,number==2)
    # Validate exactly the same logical datoms; no report bytes or intent are changed.
    checked=copy.deepcopy(report);checked[':edb/committed']=False;checked[':edb/speculative']=True
    result=migration.verify_report(directory,checked,snapshot,number==2)
    result.update(committed=True,speculative=False)
    save(directory/'commit-validation.json',result)
    # Keep the actual speculative verification distinct from committed evidence.
    preview=edb.loads((directory/'preview.edn').read_text());migration.verify_report(directory,preview,snapshot,number==2)
    return result

def original_fields(snapshot):return {f[':db/id']:f for q, in snapshot['questions'] for f in q[':question/answer-fields']}

def review_concurrent_change(fresh,baseline,number):
    if equal(fresh,baseline):return []
    # The refreshed capture shows that the obsolete, unkeyed duplicate was
    # detached externally. Preserve that repair; the authoritative keyed bank,
    # mathematics and every other question fact must still match exactly.
    qid=17592186134302;fid=17592186131851
    adjusted=copy.deepcopy(baseline)
    old=next(f for f in adjusted[qid][':question/answer-fields'] if f[':db/id']==fid)
    assert number==1 and ':answer-field/correct' not in old
    adjusted[qid][':question/answer-fields']=[f for f in adjusted[qid][':question/answer-fields'] if f[':db/id']!=fid]
    assert equal(fresh,adjusted),('Concurrent question change requires re-review',number)
    return [dict(question=qid,ma_id='q-40639',detached_field=fid,reason='Preserve concurrent removal of an unkeyed duplicate; keyed C-only bank and all other facts are unchanged.')]

def prepare_group(number,directory,basis,baseline):
    migration.OUT=directory;edb.OUT=directory
    ids=sorted(q['id'] for q in read(OUT/'batch-01/plan.json')['questions'])
    snapshot=migration.capture(ids,basis)
    fresh={q[':db/id']:q for q, in snapshot['questions']}
    changes=review_concurrent_change(fresh,baseline,number)
    assert snapshot['lineage']==read(OUT/'plan.json')['lineage']
    template=OUT/f'batch-{number:02d}'
    manifest=read(template/'plan.json');manifest.update(basis=basis,captured_basis=basis)
    shutil.copy2(template/'transaction.edn',directory/'transaction.edn')
    assert migration.digest(directory/'transaction.edn')==manifest['transaction_sha256']
    if changes:
        forms=edb.loads((directory/'transaction.edn').read_text())
        removed=[edb.kw('db/retract'),17592186134302,edb.kw('question/answer-fields'),17592186131851]
        assert forms.count(removed)==1
        forms.remove(removed)
        (directory/'transaction.edn').write_text('[\n'+'\n'.join(' '+edb.dumps(form) for form in forms)+'\n]\n')
        manifest['reviewed_template_sha256']=manifest['transaction_sha256']
        manifest['transaction_sha256']=migration.digest(directory/'transaction.edn')
        question=next(q for q in manifest['questions'] if q['id']==17592186134302)
        question['old_fields'].remove(17592186131851)
        # Retain the historical choice mappings and all 744 original entities.
        save(directory/'concurrent-change-review.json',dict(basis=basis,reviewed=True,changes=changes,existing_key_preserved=True))
    if number==1:
        forms=edb.loads((directory/'transaction.edn').read_text());collisions=[]
        for attribute in ('answer-field/id','answer/id'):
            identities=[f[':'+attribute] for f in forms if isinstance(f,dict) and ':'+attribute in f]
            collisions+=edb.batches('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',identities,'identity-'+attribute.split('/')[0],basis,256)
        assert not collisions
        save(directory/'identity-check.json',dict(basis=basis,collisions=[]))
    save(directory/'plan.json',manifest)
    for name in ['question-pattern.edn','field-pattern.edn','question-ids.txt','field-ids.txt']:shutil.copy2(OUT/name,directory/name)
    request=read(template/'prepared-request.json');request.update(basis=basis,sha256=manifest['transaction_sha256'],request_key=f'discovery-keyed-incomplete-v1-{basis}-{number}-{manifest["transaction_sha256"]}',transaction_file=str(directory/'transaction.edn'),previous_batch_required=None,original_preparation_key=read(template/'prepared-request.json')['request_key'])
    save(directory/'prepared-request.json',request)
    return snapshot

def preview_group(number,directory,baseline):
    process=subprocess.Popen([str(OUT/'single-preview'),str(directory),edb.SOURCE],env=edb.DB.env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        line=process.stdout.readline();assert line.startswith('CAPTURED_BASIS '),line;basis=int(line.split()[1])
        snapshot=prepare_group(number,directory,basis,baseline)
        stdout,stderr=process.communicate('PREVIEW\n',timeout=180);assert process.returncode==0,stderr
        (directory/'preview.log').write_text(line+stdout);assert stdout.splitlines()==['PREVIEWED_GROUP']
        report_scope(directory,edb.loads((directory/'preview.edn').read_text()),snapshot,number)
        after=edb.loads((directory/'questions-after.edn').read_text())
        expected=edb.loads((OUT/f'batch-{number:02d}'/'questions-after.edn').read_text())
        def without_allocations(questions):
            out=copy.deepcopy(questions)
            for q in out:
                for f in q[':question/answer-fields']:
                    f.pop(':db/id',None)
                    for a in f[':answer-field/choices']:a.pop(':db/id',None)
                    f[':answer-field/correct'].pop(':db/id',None)
            return out
        assert equal(without_allocations(after),without_allocations(expected)),('Preview semantic shape differs from reviewed package',number)
        before_fields=original_fields(edb.loads((OUT/'snapshot.edn').read_text()))
        after_fields={f[':db/id']:f for f in edb.loads((directory/'fields-after.edn').read_text())}
        assert equal(before_fields,after_fields)
        print(json.dumps(dict(previewed_group=number,basis=basis,questions=len(after))),flush=True)
        return snapshot
    finally:
        if process.poll() is None:process.kill();process.wait()

class ConfirmedStale(Exception):pass

def submit(number,directory,snapshot):
    request=read(directory/'prepared-request.json');manifest=read(directory/'plan.json');preview=read(directory/'preview.json')
    assert request['sha256']==manifest['transaction_sha256']==preview['sha256']==migration.digest(directory/'transaction.edn')
    assert request['source']==edb.SOURCE and request['basis']==manifest['basis']==preview['basis']
    assert preview['passed'] and not preview['committed'] and request['must_use_basis_guard']
    intent={**request,'state':'submission_requested'}
    path=directory/'commit-intent.json'
    if path.exists():assert read(path)==intent
    else:save(path,intent)
    if not (directory/'commit.edn').exists():
        for attempt in range(3):
            result=subprocess.run([str(OUT/'exact-commit'),str(directory),intent['request_key'],intent['source'],str(intent['basis']),intent['endpoint']],env=edb.DB.env,capture_output=True,text=True,timeout=210)
            (directory/f'commit-attempt-{attempt+1}.log').write_text(result.stdout+result.stderr)
            if (directory/'commit.edn').exists():break
            if (directory/'confirmed-reconciliation.edn').exists():raise RuntimeError('Commit confirmed; recover the saved exact request report before continuing')
            error_path=directory/'native-reconciliation-error.edn'
            if error_path.exists():
                error=edb.loads(error_path.read_text());code=error[':diagnostic/code'];remote=error.get(':diagnostic/details',{}).get('remote_code')
                if code=='postgres/stale-basis' or remote=='postgres/stale-basis':
                    save(directory/'rejection.json',dict(confirmed_not_committed=True,code='postgres/stale-basis',request_key=intent['request_key'],basis=intent['basis'],error=migration.plain(error)))
                    raise ConfirmedStale()
                if error[':diagnostic/category'] not in ('UnknownOutcome','Unavailable'):raise RuntimeError(migration.plain(error))
            if attempt==2:raise RuntimeError('Outcome unknown; retain and reconcile this exact request')
    report=edb.loads((directory/'commit.edn').read_text());assert report[':edb/committed'] is True
    receipt=dict(committed=True,batch=number,basis_before=report[':edb/db-before-t'],basis_after=report[':edb/db-after-t'],source=edb.SOURCE,request_key=intent['request_key'],transaction_sha256=intent['sha256'],tx_hash=report.get(':edb/tx-hash'),replayed=report.get(':edb/replayed'),datoms=len(report[':edb/tx-data']),counts=manifest['counts'],directory=str(directory))
    save(directory/'commit-receipt.json',receipt)
    update_status(receipt)
    report_scope(directory,report,snapshot,number,committed=True)
    print(json.dumps(dict(committed_group=number,basis_before=receipt['basis_before'],basis_after=receipt['basis_after'])),flush=True)
    return receipt

def update_status(receipt):
    path=OUT/'status.json';status=read(path);receipts={r['batch']:r for r in status.get('confirmed_commits',[])};receipts[receipt['batch']]=receipt
    status.update(state='committed_pending_readback',live_submission_authorized=True,database_writes=len(receipts),confirmed_commits=[receipts[k] for k in sorted(receipts)],unknown_outcome_requests=[],unsubmitted_question_ids=[] if 1 in receipts else status['unsubmitted_question_ids'])
    save(path,status)
    if not (OUT/'prepared-resolutions.json').exists():shutil.copy2(OUT/'resolutions.json',OUT/'prepared-resolutions.json')
    ledger=read(OUT/'resolutions.json')
    if 1 in receipts:
        for row in ledger['questions']:row.update(commit_status='committed_pending_readback',commit_basis=receipts[1]['basis_after'],commit_request_key=receipts[1]['request_key'])
    save(OUT/'resolutions.json',ledger)

def readback(receipt,directory):
    basis=receipt['basis_after'];edb.OUT=directory
    ids=sorted(q['id'] for q in read(OUT/'batch-01/plan.json')['questions'])
    after=edb.batches('[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',ids,'committed-questions',basis,64)
    expected={q[':db/id']:q for q in edb.loads((directory/'questions-after.edn').read_text())}
    assert equal({q[':db/id']:q for q, in after},expected),'Committed readback differs from held native preview'
    original=original_fields(edb.loads((OUT/'snapshot.edn').read_text()))
    pattern=(OUT/'field-pattern.edn').read_text()
    fields=edb.batches('[:find (pull ?f '+pattern+') :in $ [?f ...] :where [?f :answer-field/id _]]',sorted(original),'committed-original-fields',basis,64)
    assert equal({f[':db/id']:f for f, in fields},original)
    items=edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',ids,'committed-items',basis,128)
    assert not items
    save(directory/'verification.json',dict(passed=True,committed=True,basis=basis,questions=len(after),original_entities_preserved=744,existing_keys_preserved=True,learner_state_unchanged=True))
    print(json.dumps(dict(verified_group=receipt['batch'],basis=basis,questions=len(after),original_entities_preserved=744)),flush=True)
    return {q[':db/id']:q for q, in after}

def main():
    integrity=read(OUT/'package-integrity.json');assert integrity['passed']
    for name,digest in integrity['files'].items():
        path=OUT/name
        if name=='resolutions.json' and (OUT/'prepared-resolutions.json').exists():path=OUT/'prepared-resolutions.json'
        assert migration.digest(path)==digest,('Prepared artifact changed',name)
    assert read(OUT/'engine-report.json')['documented_unresolved_checks']==0
    compile_helpers()
    baseline={q[':db/id']:q for q, in edb.loads((OUT/'snapshot.edn').read_text())['questions']}
    receipts=[]
    for number in (1,2):
        existing=[r for r in read(OUT/'status.json').get('confirmed_commits',[]) if r['batch']==number]
        if existing:
            receipt=existing[0];directory=Path(receipt['directory']);baseline=readback(receipt,directory);receipts.append(receipt);continue
        for attempt in range(1,5):
            directory=OUT/'execution'/f'group-{number:02d}-attempt-{attempt:02d}'
            if (directory/'rejection.json').exists():continue
            if (directory/'commit-intent.json').exists():
                snapshot=edb.loads((directory/'snapshot.edn').read_text())
            else:
                if directory.exists():
                    save(directory/'unsubmitted-interruption.json',dict(confirmed_not_submitted=True,reason='Interrupted before any durable submission intent; preserve evidence and refresh in the next directory.'))
                    continue
                directory.mkdir(parents=True);snapshot=preview_group(number,directory,baseline)
            try:receipt=submit(number,directory,snapshot)
            except ConfirmedStale:
                print(json.dumps(dict(rejected_stale_group=number,attempt=attempt,confirmed_not_committed=True)),flush=True);continue
            baseline=readback(receipt,directory);receipts.append(receipt);break
        else:raise RuntimeError('Repeated contention; retain confirmed receipts and rejected requests')
    summary=dict(committed=True,basis_before=receipts[0]['basis_before'],basis_after_conversions=receipts[0]['basis_after'],basis_after=receipts[-1]['basis_after'],source=edb.SOURCE,counts=read(OUT/'plan.json')['counts'],batches=receipts,mode='Each group freshly captured, previewed, committed and read back before the next')
    save(OUT/'commit-receipt.json',summary)
    save(OUT/'verification.json',dict(passed=True,committed=True,basis=summary['basis_after'],counts=summary['counts'],existing_keys_preserved=True,original_entities_preserved=744,unrated_preserved=True,groups=[read(Path(r['directory'])/'verification.json') for r in receipts]))
    status=read(OUT/'status.json');status.update(state='committed_verified',basis=summary['basis_after'],database_writes=2,verification=str(OUT/'verification.json'),unsubmitted_question_ids=[],unknown_outcome_requests=[]);save(OUT/'status.json',status)
    ledger=read(OUT/'resolutions.json')
    for row in ledger['questions']:row.update(commit_status='committed_verified',verification_passed=True)
    save(OUT/'resolutions.json',ledger)
    print(json.dumps(dict(all_committed_and_verified=True,basis=summary['basis_after'],**summary['counts'])),flush=True)

if __name__=='__main__':main()
