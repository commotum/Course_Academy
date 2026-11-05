"""Read-only generator registration audit; retain queries and one as-of basis.

Run from the repository root with .venv/bin/python <this file>.
No preview, transaction, package execution, or publication is performed.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_publish import Publisher
from capture.scripts.database.edn import dumps, loads, kw

OUT = Path(__file__).resolve().parent
QUERIES = {
    'current': (False, '''[:find (pull ?kp [:db/id :knowledge-point/id :knowledge-point/title
      {:topic/_knowledge-points [:db/id :topic/title]}
      {:knowledge-point/question-generator [:db/id :question-generator/id :question-generator/script]}])
      :where [?kp :knowledge-point/question-generator _]]''', []),
    'registration-history': (True, '''[:find ?kp ?generator ?tx ?source ?added ?instant
      :where [?kp :knowledge-point/question-generator ?generator ?tx ?source ?added]
             [?tx :db/txInstant ?instant]]''', []),
    'script-history': (True, '''[:find ?generator ?script ?tx ?source ?added ?instant
      :where [?generator :question-generator/script ?script ?tx ?source ?added]
             [?tx :db/txInstant ?instant]]''', []),
    'generator-identities': (True, '''[:find ?generator ?id ?tx ?source ?added
      :where [?generator :question-generator/id ?id ?tx ?source ?added]]''', []),
    'schema': (False, '''[:find (pull ?a [:db/id :db/ident :db/noHistory
      {:db/cardinality [:db/ident]}]) :in $ [?ident ...] :where [?a :db/ident ?ident]]''',
      [list(map(kw, ['knowledge-point/question-generator', 'question-generator/script',
                    'question-generator/id', 'question/retired']))]),
}


def main():
    publisher = Publisher.from_environment()
    client = publisher.client
    status = client.status()
    (OUT / 'capture.json').write_text(json.dumps({**status,
        'math_root': str(publisher.config.math_root), 'edb_bin': str(publisher.config.edb_bin)}, indent=2)+'\n')

    def read(item):
        name, (history, query, inputs) = item
        directory = OUT / 'evidence'
        directory.mkdir(exist_ok=True)
        qpath, ipath = directory / (name+'-query.edn'), directory / (name+'-inputs.edn')
        qpath.write_text(query)
        ipath.write_text(dumps(inputs))
        args = ['--file', qpath, '--inputs', ipath, '--as-of', status['basis']]
        if history:
            args.append('--history')
        result = client.command('query', *args, timeout=210)
        (directory / (name+'.edn')).write_text(result)
        rows = loads(result)
        (directory / (name+'.json')).write_text(json.dumps(rows, default=str, indent=2)+'\n')
        return name, len(rows)

    with ThreadPoolExecutor(max_workers=3) as pool:
        for name, size in pool.map(read, QUERIES.items()):
            print(name, size, flush=True)


if __name__ == '__main__':
    main()
