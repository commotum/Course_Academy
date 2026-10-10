#!/usr/bin/env python3
"""Submit prepared MA JSON lesson batches with stable retry keys and receipts."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0, '/home/jake/Developer/Course_Academy/scripts/question_capture')
from edn import loads, kw

BINARY = '/home/jake/Developer/EDB/target/release/edb'


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path('/media/jake/SSD/EDB/math/imports/math-academy/lessons'))
    args = parser.parse_args()
    directory = args.directory.resolve()
    manifest_path = directory / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    assert manifest['source'] == ':org/Math-Academy'
    env = os.environ.copy()
    env['EDB_POSTGRES_URL'] = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"
    def command(arguments):
        return subprocess.run([BINARY] + arguments, env=env, text=True, capture_output=True)
    source_query = directory / 'source-query.edn'
    source_query.write_text('[:find ?e :where [?e :db/ident :org/Math-Academy]]\n')
    source_result = command(['query', '--database', 'math', '--file', str(source_query)])
    if source_result.returncode:
        raise RuntimeError(source_result.stderr)
    rows = loads(source_result.stdout)
    assert len(rows) == 1
    source_id = rows[0][0]
    status = command(['status', '--database', 'math'])
    if status.returncode:
        raise RuntimeError(status.stderr)
    basis = int(re.search(r'basis_t=(\d+)', status.stdout)[1])
    manifest.setdefault('basis_before', basis)
    save(manifest_path, manifest)
    receipts = directory / 'receipts'
    receipts.mkdir(exist_ok=True)
    for number, batch in enumerate(manifest['batches'], 1):
        if 'committed_basis' in batch:
            print(f'Already committed {batch["file"]} at basis {batch["committed_basis"]}.', flush=True)
            continue
        batch.setdefault('basis_before', basis)
        save(manifest_path, manifest)
        print(f'Transacting {number}/{len(manifest["batches"])}: {batch["file"]} ({len(batch["topics"])} lessons).', flush=True)
        result = command(['transact', '--database', 'math', '--endpoint', '/tmp/edb-math/writer.sock',
                          '--request-key', batch['request_key'], '--source', manifest['source'],
                          '--basis', str(batch['basis_before']), '--file', str(directory / batch['file']),
                          '--timeout-ms', '180000'])
        receipt_path = receipts / batch['file']
        receipt_path.write_text(result.stdout)
        (receipts / (batch['file'] + '.stderr')).write_text(result.stderr)
        if result.returncode:
            batch['last_error'] = result.stderr
            save(manifest_path, manifest)
            print('Stopped at ' + batch['file'] + ': ' + result.stderr[:2500], flush=True)
            print('The exact request key and basis are saved; rerun with the same unchanged batch to resolve any unknown outcome.', flush=True)
            raise SystemExit(result.returncode)
        receipt = loads(result.stdout)
        assert receipt[kw('edb/committed')] is True
        datoms = receipt[kw('edb/tx-data')]
        assert all(d[4] == source_id for d in datoms), 'Unexpected transaction source'
        basis = receipt[kw('edb/basis-t')]
        batch['committed_basis'] = basis
        batch['committed_datoms'] = len(datoms)
        batch.pop('last_error', None)
        manifest['last_committed_basis'] = basis
        save(manifest_path, manifest)
        print(f'Committed basis {basis}; {len(datoms)} datoms, all source :org/Math-Academy.', flush=True)
    manifest['complete'] = True
    save(manifest_path, manifest)
    print(f'Completed {manifest["totals"]["lessons"]} lessons. Final basis: {basis}.', flush=True)


if __name__ == '__main__':
    main()
