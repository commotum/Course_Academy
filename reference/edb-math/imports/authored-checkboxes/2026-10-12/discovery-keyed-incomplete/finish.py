"""Read-only history verification and durable post-commit handoff."""
import json
from pathlib import Path
import prepare as migration

OUT=migration.OUT
edb=migration.edb

def read(path):return json.loads(path.read_text())
def save(path,value):edb.atomic_json(path,value)

def main():
    receipt=read(OUT/'commit-receipt.json')
    verification=read(OUT/'verification.json')
    assert receipt['committed'] and verification['committed'] and verification['passed']
    snapshot=edb.loads((OUT/'snapshot.edn').read_text())
    ids=sorted(q[':db/id'] for q, in snapshot['questions'])
    edb.OUT=OUT/'post-commit';edb.OUT.mkdir(exist_ok=True)
    historical=edb.batches('[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',ids,'historical-questions',snapshot['basis'],64)
    normalize=lambda rows:{q[':db/id']:migration.plain(q) for q, in rows}
    assert normalize(historical)==normalize(snapshot['questions'])
    kps=sorted({k[':db/id'] for q, in snapshot['questions'] for k in q[':knowledge-point/_questions']})
    topics=edb.batches('[:find (pull ?kp [:db/id {[:topic/_knowledge-points :limit nil] [:db/id :topic/title :topic/math-academy-id]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',kps,'committed-topics',receipt['basis_after'],64)
    assert normalize(topics)==normalize(snapshot['topics'])
    generators=[str(p.relative_to(migration.ROOT)) for p in (migration.ROOT/'generate/scratch').glob('*.py') if p.stem in {str(k) for k in kps}]
    checks=dict(passed=True,committed_basis=receipt['basis_after'],historical_basis=snapshot['basis'],historical_questions_unchanged=len(ids),topic_memberships_preserved=len(kps),affected_generator_files=generators)
    save(OUT/'post-commit/verification.json',checks)
    verification.update(historical_snapshot_preserved=True,topic_memberships_preserved=True,post_commit_verification=str(OUT/'post-commit/verification.json'),affected_generator_files=generators)
    save(OUT/'verification.json',verification)
    audit=migration.AUDIT
    status=read(audit/'status.json')
    status.update(state='keyed_group_committed_verified',transactions_prepared=True,previewed=True,committed=True,database_writes=2,committed_basis=receipt['basis_after'],confirmed_conversion_ids=ids,confirmed_solution_corrections=7,commit_receipt=str(OUT/'commit-receipt.json'),verification=str(OUT/'verification.json'),source=receipt['source'],preserved_concurrent_repairs=[dict(question=17592186134302,ma_id='q-40639',detached_unkeyed_duplicate_field=17592186131851)])
    save(audit/'status.json',status)
    queue=read(audit/'next-queue.json')
    queue.update(confirmed_conversion_ids=ids,commit_basis=receipt['basis_after'],commit_receipt=str(OUT/'commit-receipt.json'),database_writes=2)
    save(audit/'next-queue.json',queue)
    text=(audit/'README.md').read_text()
    text=text.replace('**No database writes.** The evaluated group was subsequently prepared and natively previewed at basis 1846; see the prepared package linked below.', '**The evaluated group is now committed and verified.** Conversions committed at basis 1854, followed by seven separate solution corrections at basis 1855. Each group was freshly captured, natively previewed, committed and verified before the next. Source: `:agent/gpt-6.1-sol-high`.')
    text=text.replace('These are reviewable proposed repairs, not transactions.', 'All seven corrections were committed separately at basis 1855; existing keys are preserved.')
    text=text.replace('Prepared package:', 'Committed package:').replace('No transaction has been submitted.', 'Both groups are confirmed and verified; see the package receipt. A concurrent removal of q-40639’s obsolete unkeyed duplicate was preserved. Historical counts above describe the original audit.')
    (audit/'README.md').write_text(text)
    print(json.dumps(checks),flush=True)

if __name__=='__main__':main()
