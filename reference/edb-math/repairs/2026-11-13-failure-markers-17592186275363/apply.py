"""Restore two source-colored failure markers with a guarded content transaction."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher, StaleBasis, dumps, kw, file_lock
from capture.scripts.database.commit import Committer
from capture.scripts.storage import atomic_json

proposal = json.loads((HERE / 'proposal.json').read_text())
assert json.loads((HERE / 'render-verification.json').read_text())['passed']
assert hashlib.sha256((ROOT / proposal['source']).read_bytes()).hexdigest() == proposal['source_sha256']
publisher = Publisher.from_environment(source=':agent/codex')
client = publisher.client
work = HERE / 'publication'
committer = Committer(publisher.config, client, work)
query = '[:find (pull ?q [*]) :in $ ?q :where [?q :question/id _]]'
entity = proposal['entity']
attribute = kw(proposal['attribute'])

with file_lock(Path(publisher.config.request_directory) / 'api.lock'):
    for attempt in range(5):
        request = committer.pending()
        try:
            if not request:
                status = client.status()
                basis = status['basis']
                before = client.query(query, [entity], work, 'before', basis)[0][0]
                assert before[str(attribute)] == proposal['before'], 'Solution changed since source review'
                atomic_json(work / 'before.json', json.loads(json.dumps(before, default=str)))
                batch = {'source': publisher.config.source,
                         'forms': [[kw('db/cas'), entity, attribute, proposal['before'], proposal['after']],
                                   [kw('db/ensure'), entity, kw('question/validate')]],
                         'assertions': [[entity, attribute, proposal['after']]],
                         'retractions': [[entity, attribute, proposal['before']]]}
                snapshot = {'basis': basis, 'lineage': status['lineage'],
                    'attributes': client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]', [], work, 'attributes', basis),
                    'idents': client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], work, 'idents', basis)}
                committer.preview(batch, snapshot)
                request = committer.save_request(batch, snapshot, hashlib.sha256(dumps(proposal).encode()).hexdigest())
            receipt = committer.submit(request)
            proof = committer.verify_receipt(request, receipt)
            basis_after = receipt[':edb/db-after-t']
            after = client.query(query, [entity], work, 'after', basis_after)[0][0]
            expected = json.loads((work / 'before.json').read_text())
            expected[str(attribute)] = proposal['after']
            # JSON normalizes UUID values in the full entity readback.
            assert json.loads(json.dumps(after, default=str)) == expected
            verification = {'passed': True, 'committed': True, 'entity': entity,
                'basis_before': request['basis'], 'basis_after': basis_after,
                'markers_restored': 2, 'question_other_attributes_unchanged': True,
                'request_key': request['request_key'], **proof}
            atomic_json(HERE / 'verification.json', verification)
            committer.retire(request, 'verified', verification)
            print(json.dumps(verification, indent=2))
            break
        except StaleBasis:
            if request:
                committer.retire(request, 'rejected_stale_basis', {'reason': 'Confirmed stale basis; re-read exact solution'})
    else:
        raise RuntimeError('Database kept advancing; repair not committed')
