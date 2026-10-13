"""Read-only EDB exports pinned to one basis for the frequency-fraction proposal."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import threading

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[4]
sys.path.insert(0, str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import kw


def main():
    if (FOLDER/'request.json').exists():
        raise ValueError('Keep the exact prepared request and its pinned exports; use a new bundle for a refresh.')
    client = EDBClient(Config(capture_only=True), threading.Event())
    identity = client.status()
    queries = {
        'topics': ('[:find (pull ?t [:db/id :topic/id :topic/math-academy-id :topic/title '
                   '{:topic/next [:db/id :topic/math-academy-id]} '
                   '{:topic/encompasses [:db/id :encompassing/weight :encompassing/rationale '
                   '{:encompassing/topic [:db/id :topic/math-academy-id :topic/title]}]}]) '
                   ':where [?t :topic/id _]]', []),
        'idents': ('[:find (pull ?e [:db/id :db/ident :db/doc]) :where [?e :db/ident ?ident]]', []),
        'schema': ('[:find (pull ?a [*]) :in $ [?ident ...] :where [?a :db/ident ?ident]]',
                   [[kw(s) for s in ('topic/encompasses','encompassing/topic','encompassing/weight',
                                     'encompassing/rationale','encompassing/validate')]])
    }
    def export(name):
        query, inputs = queries[name]
        rows = client.query(query, inputs, FOLDER, name, identity['basis'])
        (FOLDER/(name+'.json')).write_text(json.dumps(rows, indent=2, default=str)+'\n')
        return name, len(rows)
    with ThreadPoolExecutor(max_workers=3) as pool:
        counts = dict(pool.map(export, queries))
    after = client.status()
    assert after['lineage'] == identity['lineage'], 'Database lineage changed during export'
    (FOLDER/'database-identity.json').write_text(json.dumps(identity, indent=2)+'\n')
    (FOLDER/'read-verification.json').write_text(json.dumps({
        'read_basis': identity['basis'], 'after_read_status': after,
        'all_queries_pinned_to_same_basis': True, 'row_counts': counts,
        'database_writes': 0}, indent=2)+'\n')
    print(json.dumps({'identity': identity, 'row_counts': counts}))


if __name__ == '__main__':
    main()
