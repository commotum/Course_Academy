"""Commit the seven reviewed OSU transactions with persisted exact retry intents."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import threading
import uuid

sys.path.insert(0, '/home/jake/Developer/Course_Academy/capture')
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import dumps, loads
from scripts.storage import atomic_json, atomic_text, file_lock

STAGE = Path('/tmp/osu-commit-2026-10-10')
PREP = Path('/home/jake/Developer/Course_Academy/reference/edb-math/imports/oregon-state/2026-10-10')
OUT = PREP/'commit'
OUT.mkdir(parents=True,exist_ok=True)
config = Config()
client = EDBClient(config,threading.Event())
manifest = json.loads((PREP/'prepared-manifest.json').read_text())
state = json.loads((PREP/'db/state.json').read_text())
assert state['basis'] == manifest['basis_read'] == 187
timestamp_attr = next(row[0] for row in state['attributes'] if row[1] == ':db/txInstant')
shutil.copytree(PREP/'db', STAGE/'db', dirs_exist_ok=True)

def save_edn(name, text):
    atomic_text(OUT/name,text)
    atomic_text(STAGE/name,text)
def save_json(name,value):
    atomic_json(OUT/name,value)
    atomic_json(STAGE/name,value)
def material(report):
    return {(e,a,dumps(v),s,added) for e,a,v,tx,s,added in report[':edb/tx-data'] if a != timestamp_attr}
def check(report, index, expected):
    assert report.get(':edb/committed') is True, 'Receipt does not confirm commit'
    assert report[':edb/db-before-t'] == 187+index-1
    assert report[':edb/db-after-t'] == 187+index
    assert material(report) == material(expected), 'Committed facts differ from reviewed preview'
    timestamps = [d for d in report[':edb/tx-data'] if d[1] == timestamp_attr]
    assert len(timestamps) == 1 and timestamps[0][5] is True
    assert {d[4] for d in report[':edb/tx-data']} == {d[4] for d in expected[':edb/tx-data']}, 'Source differs'

# Verify every installed EDN before any mutation. Exact submitted bytes are saved.
for entry in manifest['transactions']:
    path = config.math_root/entry['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], str(path)

with file_lock(config.database_lock):
    summaries = []
    for index,entry in enumerate(manifest['transactions'],1):
        receipt_path = OUT/f'stage{index}-commit.edn'
        request_path = OUT/f'stage{index}-request.json'
        transaction_path = OUT/f'stage{index}-transaction.edn'
        expected = loads((PREP/f'preview/stage{index}-preview.edn').read_text())
        if receipt_path.exists():
            text = receipt_path.read_text()
            report = loads(text)
            check(report,index,expected)
        else:
            if request_path.exists():
                request = json.loads(request_path.read_text())
                assert request['sha256'] == entry['sha256'] and request['source'] == entry['source']
                assert request['basis'] == 187+index-1
                assert request['database'] == config.database and request['endpoint'] == config.endpoint
            else:
                basis = client.basis()
                assert basis == 187+index-1, f'Database advanced to {basis}; review before submitting next stage'
                transaction = (config.math_root/entry['path']).read_text()
                atomic_text(transaction_path,transaction)
                request = {'request_key':'osu-migration-'+str(uuid.uuid4()),'basis':basis,
                           'database':config.database,'endpoint':config.endpoint,'source':entry['source'],
                           'sha256':entry['sha256'],'file':str(transaction_path)}
                atomic_json(request_path,request)
            assert hashlib.sha256(transaction_path.read_bytes()).hexdigest() == request['sha256']
            # A transport timeout retries the exact key, basis, source, and bytes.
            for attempt in range(3):
                try:
                    text = client.command('transact','--file',transaction_path,
                         '--endpoint',request['endpoint'],'--request-key',request['request_key'],
                         '--basis',request['basis'],'--source',request['source'],'--timeout-ms',180000)
                    break
                except subprocess.TimeoutExpired:
                    if attempt == 2:raise
                    print(f'Stage {index}: response timed out; recovering exact saved request',flush=True)
            save_edn(receipt_path.name,text)
            report = loads(text)
            check(report,index,expected)
        save_edn(receipt_path.name,text)
        summaries.append({'stage':index,'file':entry['path'],'source':entry['source'],
                          'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],
                          'material_datoms':len(material(report)),'receipt_matches_reviewed_preview':True})
        save_json('commit-progress.json',{'committed_stages':summaries})
        print(f"Committed stage {index}/7: {entry['path']} ({report[':edb/db-before-t']} -> {report[':edb/db-after-t']})",flush=True)
    final_basis = client.basis()
    assert final_basis == 194, f'Unexpected basis {final_basis}'
    save_json('final-basis.json',{'basis':final_basis})

    identities = loads((PREP/'pull-identities.edn').read_text())
    rows = client.query('[:find ?attribute ?identity (pull ?e [*]) :in $ [[?attribute ?identity]] :where [?e ?attribute ?identity]]',
                        [identities],OUT,'final-entities',final_basis)
    found = {(str(a),str(i)):v for a,i,v in rows}
    assert len(found) == len(identities), 'Missing final entities'
    pulled = [[identity,found[(str(identity[0]),str(identity[1]))]] for identity in identities]
    save_edn('final-pull1.edn',dumps(pulled)+'\n')
    eids = [row[1][':db/id'] for row in pulled]
    # Also read current fact attribution, beyond checking receipts.
    source_rows = client.query('[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]',
                                [eids],OUT,'final-facts',final_basis)
    save_edn('final-facts.edn',dumps(source_rows)+'\n')
    print(f'Read back {len(pulled)} entities and {len(source_rows)} source-attributed facts at basis {final_basis}',flush=True)
    save_json('result.json',{'committed':True,'basis_before':187,'basis_after':final_basis,
                           'transactions':summaries,'entities_read_back':len(pulled),
                           'source_attributed_facts_read_back':len(source_rows)})
