"""Read-only review of the remaining historical strong candidates."""
import concurrent.futures
import hashlib
import importlib.util
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PRIOR = ROOT / 'reference/edb-math/imports/authored-checkboxes'
AUDIT = ROOT / 'generate/reports/checkbox-discovery-2026-10-12'
spec = importlib.util.spec_from_file_location('checkbox_reference', PRIOR / '2026-10-12/finder-easy/prepare.py')
edb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edb)
edb.DB.args.capture_only = True
edb.OUT = OUT

def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, default=str) + '\n')

def main():
    assert not (OUT / 'snapshot.json').exists(), 'Preserve completed captures'
    completed = set()
    evidence = []
    for date, name in [('2026-10-11','topic-3215'), ('2026-10-12','finder-easy'), ('2026-10-12','finder-remaining')]:
        directory = PRIOR / date / name
        verification = json.loads((directory / 'verification.json').read_text())
        assert verification.get('committed') and (verification.get('passed') or verification.get('verified'))
        plan = json.loads((directory / 'plan.json').read_text())
        completed.update(q['id'] for q in plan['questions'])
        evidence.append(str(directory / 'verification.json'))
    for name in ['discovery-direct', 'discovery-next']:
        directory = PRIOR / '2026-10-12' / name
        receipts = json.loads((directory / 'commit-receipt.json').read_text())
        assert receipts['committed']
        for receipt in receipts['batches']:
            assert receipt['committed']
            batch = directory / ('batch-%02d' % receipt['batch'])
            request = json.loads((batch / 'prepared-request.json').read_text())
            assert request['request_key'] == receipt['request_key']
            plan = json.loads((batch / 'plan.json').read_text())
            assert len(plan['questions']) == receipt['counts']['questions']
            completed.update(q['id'] for q in plan['questions'])
        evidence.append(str(directory / 'commit-receipt.json'))
    directory = PRIOR / '2026-10-12' / 'discovery-keyed-incomplete'
    if (directory / 'commit-receipt.json').exists():
        receipts = json.loads((directory / 'commit-receipt.json').read_text())
        verification = json.loads((directory / 'verification.json').read_text())
        assert receipts['committed'] and verification['passed'] and verification['committed']
        receipt = next(r for r in receipts['batches'] if r['batch'] == 1)
        assert receipt['committed']
        batch = Path(receipt['directory'])
        request = json.loads((batch / 'prepared-request.json').read_text())
        plan = json.loads((batch / 'plan.json').read_text())
        assert request['request_key'] == receipt['request_key']
        assert request['sha256'] == receipt['transaction_sha256']
        assert len(plan['questions']) == receipt['counts']['questions']
        completed.update(q['id'] for q in plan['questions'])
        evidence.append(str(directory / 'commit-receipt.json'))
    report = json.loads((AUDIT / 'report.json').read_text())
    retained = {17592186329885}
    rows = [q for q in report['strong_candidates'] if q['id'] not in completed | retained]
    ids = sorted(q['id'] for q in rows)
    status = edb.DB.command('status')
    basis = int(re.search(r'\bbasis_t=(\d+)', status)[1])
    assert 'lineage=' + report['lineage'] in status
    save('capture-start.json', dict(basis=basis,lineage=report['lineage'],historical_basis=report['basis'],selected_ids=ids,confirmed_completed_ids=sorted(completed),retained_radio_ids=sorted(retained),receipt_evidence=evidence,database_writes=0))
    save('historical-candidates.json', rows)
    pattern = edb.QUESTION.replace(':knowledge-point/title]', ':knowledge-point/title {[:topic/_knowledge-points :limit nil] [:db/id :topic/title :topic/math-academy-id]}]')
    questions = edb.batches('[:find (pull ?q '+pattern+') :in $ [?q ...] :where [?q :question/id _]]',ids,'questions',basis,64)
    assert {q[':db/id'] for q, in questions} == set(ids)
    items = edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',ids,'items',basis,128)
    fields = sorted({f[':db/id'] for q, in questions for f in q.get(':question/answer-fields',[])})
    answers = sorted({a[':db/id'] for q, in questions for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])})
    users = edb.batches('[:find ?a (pull ?item '+edb.ITEM+') :in $ [?a ...] :where [?item :task-item/responses ?a]]',answers,'response-users',basis,256)
    field_owners = edb.batches('[:find ?f (pull ?f [{[:question/_answer-fields :limit nil] [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',fields,'field-owners',basis,128)
    answer_owners = edb.batches('[:find ?a (pull ?a [{[:answer-field/_choices :limit nil] [:db/id]}]) :in $ [?a ...] :where [?a :answer/id _]]',answers,'answer-owners',basis,256)
    snapshot = dict(basis=basis,lineage=report['lineage'],questions=questions,items=items,response_users=users,field_owners=field_owners,answer_owners=answer_owners)
    (OUT/'snapshot.edn').write_text(edb.dumps(snapshot)+'\n')
    save('snapshot.json',snapshot)
    manifest = dict(state='captured_for_review',basis=basis,lineage=report['lineage'],historical_candidates=len(ids),confirmed_prior_conversions=len(completed),presentations=len(items),response_links=len(users),snapshot_sha256=hashlib.sha256((OUT/'snapshot.edn').read_bytes()).hexdigest(),database_writes=0,scope='Remaining historical strong candidates; excludes confirmed conversions and previously retained ordered radio. Not a new database-wide discovery.')
    save('status.json',manifest)
    print(json.dumps(manifest),flush=True)

if __name__ == '__main__':
    main()
