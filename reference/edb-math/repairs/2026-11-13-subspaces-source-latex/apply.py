"""Publish the consolidated repair with CAS, native validation and full readback."""
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher, StaleBasis, KP_PULL, dumps, kw, file_lock, jsonable
from capture.scripts.database.commit import Committer
from capture.scripts.storage import atomic_json
from prepare import entities, update

manifest = json.loads((HERE / 'proposal.json').read_text())
assert json.loads((HERE / 'render-verification.json').read_text())['passed']
assert json.loads((HERE / 'tutorial-audit.json').read_text())['passed']
for path, digest in manifest['source_sha256'].items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
proposals = manifest['proposals']
publisher = Publisher.from_environment(source=':agent/codex')
client = publisher.client
work = HERE / 'publication'
committer = Committer(publisher.config, client, work)
query = '[:find (pull ?t [:db/id :topic/title :topic/math-academy-id {:topic/knowledge-points ' + KP_PULL + '}]) :in $ ?t :where [?t :topic/id _]]'
topic_id = 17592186051046
question_ids = sorted({p['entity'] for p in proposals if p['attribute'].startswith(':question/')})

with file_lock(Path(publisher.config.request_directory) / 'api.lock'):
    for attempt in range(5):
        request = committer.pending()
        try:
            if not request:
                status = client.status()
                basis = status['basis']
                before = jsonable(client.query(query, [topic_id], work, 'before', basis)[0][0])
                for proposal in proposals:
                    matches = [e for e in entities(before) if e[':db/id'] == proposal['entity'] and proposal['attribute'] in e]
                    assert matches and all(e[proposal['attribute']] == proposal['before'] for e in matches), 'Content changed since source review'
                atomic_json(work / 'before.json', before)
                batch = {'source': publisher.config.source,
                         'forms': [[kw('db/cas'), p['entity'], kw(p['attribute']), p['before'], p['after']] for p in proposals]
                                  + [[kw('db/ensure'), q, kw('question/validate')] for q in question_ids],
                         'assertions': [[p['entity'], kw(p['attribute']), p['after']] for p in proposals],
                         'retractions': [[p['entity'], kw(p['attribute']), p['before']] for p in proposals]}
                snapshot = {'basis': basis, 'lineage': status['lineage'],
                    'attributes': client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]', [], work, 'attributes', basis),
                    'idents': client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], work, 'idents', basis)}
                committer.preview(batch, snapshot)
                request = committer.save_request(batch, snapshot, hashlib.sha256(dumps(manifest).encode()).hexdigest())
            receipt = committer.submit(request)
            proof = committer.verify_receipt(request, receipt)
            basis_after = receipt[':edb/db-after-t']
            after = jsonable(client.query(query, [topic_id], work, 'after', basis_after)[0][0])
            expected = json.loads((work / 'before.json').read_text())
            update(expected, proposals)
            # Pull's cardinality-many order is not semantically significant.
            def canonical(v):
                if isinstance(v, dict):
                    return {k: canonical(x) for k, x in sorted(v.items())}
                if isinstance(v, list):
                    return sorted((canonical(x) for x in v), key=lambda x: json.dumps(x, sort_keys=True))
                return v
            assert canonical(after) == canonical(expected), 'Unexpected post-commit content difference'
            atomic_json(work / 'after.json', after)
            verification = {'passed': True, 'committed': True, 'topic': topic_id,
                'basis_before': request['basis'], 'basis_after': basis_after,
                'questions_repaired': len(question_ids), 'attributes_repaired': len(proposals),
                'full_topic_readback_matches_expected': True,
                'answer_ids_correct_links_and_all_other_attributes_unchanged': True,
                'request_key': request['request_key'], **proof}
            atomic_json(HERE / 'verification.json', verification)
            committer.retire(request, 'verified', verification)
            print(json.dumps(verification, indent=2))
            break
        except StaleBasis:
            if request:
                committer.retire(request, 'rejected_stale_basis', {'reason': 'Confirmed stale basis; re-read exact content'})
    else:
        raise RuntimeError('Database kept advancing; repair not committed')
