"""Read-only provenance trace for the six solution exponent labels."""
import json
import os
import subprocess
from pathlib import Path

from scripts.database.edn import dumps, loads

HERE = Path(__file__).resolve().parent
BASIS = json.loads((HERE / 'snapshot.json').read_text())['basis']
IDS = [17592186184843, 17592186265944, 17592186378650,
       17592186388125, 17592186348090, 17592186379372]
ENV = {**os.environ, 'EDB_POSTGRES_URL': 'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
BIN = '/home/jake/Developer/EDB/target/release/edb'


def query(name, expression, inputs, history=False):
    q = HERE / f'{name}-query.edn'
    i = HERE / f'{name}-inputs.edn'
    q.write_text(expression)
    i.write_text(dumps(inputs))
    command = [BIN, 'query', '--database', 'math', '--as-of', str(BASIS),
               '--file', str(q), '--inputs', str(i), '--max-value-bytes', '1073741824']
    if history:
        command.append('--history')
    output = subprocess.check_output(command, env=ENV, text=True, timeout=150)
    (HERE / f'{name}.edn').write_text(output)
    rows = loads(output)
    (HERE / f'{name}.json').write_text(json.dumps(rows, indent=2, default=str) + '\n')
    return rows


history = query('solution-history', '''[:find ?e ?v ?tx ?source ?added
 :in $ [?e ...]
 :where [?e :question/worked-solution ?v ?tx ?source ?added]]''', [IDS], True)
txs = sorted({row[2] for row in history})
sources = sorted({row[3] for row in history})
query('transaction-instants', '[:find ?tx ?instant :in $ [?tx ...] :where [?tx :db/txInstant ?instant]]', [txs])
query('sources', '[:find ?s ?ident :in $ [?s ...] :where [?s :db/ident ?ident]]', [sources])
print(json.dumps({'basis': BASIS, 'history_events': len(history), 'transactions': txs, 'sources': sources}))
