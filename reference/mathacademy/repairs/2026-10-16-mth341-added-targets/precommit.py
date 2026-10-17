"""Read-only freshness and answer-history guard for the reviewed display repair."""
import hashlib,json,sys,threading
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import kw
assert not (HERE/'commit-intent.json').exists(), 'Retain and reconcile an existing exact request first'
changes=json.loads((HERE/'changes.json').read_text())
client=EDBClient(Config(account='linear'),threading.Event())
status=client.status()
snapshot=json.loads((ROOT/'reference/mathacademy/audits/2026-10-16-mth341-added-targets/snapshot.json').read_text())
assert status['lineage']==snapshot['lineage']
fields=client.query('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]',
    [[[c['entity'],kw(c['attribute'])] for c in changes]],HERE,'before-current',status['basis'])
actual={(e,str(a)):v for e,a,v in fields}
assert actual=={(c['entity'],c['attribute']):c['before'] for c in changes}
answers=[c['entity'] for c in changes if c['attribute']==':answer/value']
refs=client.query('[:find ?a ?item :in $ [?a ...] :where [?item :task-item/responses ?a]]',
    [answers],HERE,'answer-usage',status['basis'])
assert not refs, refs
record={**status,'original_snapshot_basis':snapshot['basis'],'fields_compared':len(actual),
    'all_fields_unchanged_since_snapshot':True,'changed_answer_values':len(answers),
    'response_references':0,'transaction_sha256':hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()}
(HERE/'precommit-safety.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
