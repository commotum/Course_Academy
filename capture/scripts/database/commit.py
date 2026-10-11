"""Exact durable requests, bounded retries, and source-aware receipt validation."""
from __future__ import annotations
import hashlib
import json
import uuid
from pathlib import Path
from .client import StaleBasis
from .edn import dumps, loads, kw, Keyword
from .prepare import ALLOWED
from ..storage import atomic_json, atomic_text, read_json

class VerificationError(ValueError):
    pass


def connection_identity(config):
    # Keep secrets out of evidence files while binding retries to the original connection.
    return {'database': str(config.database), 'endpoint': str(config.endpoint),
            'math_root': str(Path(config.math_root).resolve()),
            'connection_sha256': hashlib.sha256(str(config.postgres_url or '').encode()).hexdigest()}


def validate_report(report, batch, snapshot, *, committed=False):
    if committed and report.get(':edb/committed') is not True:
        raise VerificationError('EDB did not confirm a commit')
    names = {r[0]: str(r[1]).lstrip(':') for r in snapshot.get('attributes', [])}
    attr_types = {str(r[1]).lstrip(':'): str(r[2]) for r in snapshot.get('attributes', [])}
    idents = {str(ident): eid for eid, ident in snapshot.get('idents', [])}
    source = idents.get(batch['source'])
    if source is None:
        raise VerificationError('Transaction source entity does not exist: ' + batch['source'])
    tempids = report.get(':edb/tempids', {})
    def entity(value):
        if isinstance(value, str):
            return tempids.get(value, idents.get(value, value))
        return value
    def value(attr, v):
        return entity(v) if attr_types.get(attr) == ':db.type/ref' else v
    def expected(rows):
        return {(entity(e), str(a).lstrip(':'), dumps(value(str(a).lstrip(':'), v))) for e,a,v in rows}
    assertions, retractions = expected(batch['assertions']), expected(batch['retractions'])
    observed_add, observed_retract = set(), set()
    for datom in report.get(':edb/tx-data', []):
        if len(datom) != 6 or type(datom[-1]) is not bool:
            raise VerificationError('Malformed source-aware datom in EDB receipt')
        eid, aid, val, tx, fact_source, added = datom
        attr = names.get(aid)
        if fact_source != source:
            raise VerificationError('Receipt fact attribution differs from the requested source')
        if attr == 'db/txInstant':
            if not added:
                raise VerificationError('Receipt unexpectedly retracts a timestamp')
            continue
        if attr not in ALLOWED:
            raise VerificationError('Receipt changes a protected learner/engine or unknown attribute: ' + str(attr))
        triple = (eid, attr, dumps(val))
        (observed_add if added else observed_retract).add(triple)
    if observed_add != assertions or observed_retract != retractions:
        raise VerificationError('Receipt facts differ from the complete prepared content changes')
    return {'source_eid': source, 'assertions': len(observed_add), 'retractions': len(observed_retract),
            'learner_and_engine_facts_unchanged': True}


class Committer:
    def __init__(self, config, client, directory):
        self.config, self.client, self.directory = config, client, Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.intent_path = self.directory / 'request.json'

    def pending(self):
        return read_json(self.intent_path)

    def preview(self, batch, snapshot):
        atomic_text(self.directory / 'transaction.edn', dumps(batch['forms']) + '\n')
        result = self.client.command('with', '--file', self.directory / 'transaction.edn', '--source', batch['source'])
        atomic_text(self.directory / 'preview.edn', result)
        report = loads(result)
        if report.get(':edb/db-before-t') != snapshot['basis']:
            raise StaleBasis('Database advanced during preparation')
        validate_report(report, batch, snapshot)
        return report

    def save_request(self, batch, snapshot, content_hash):
        if self.pending():
            raise ValueError('A prior exact request must be recovered before creating another')
        transaction = (self.directory / 'transaction.edn').read_text()
        request = {**connection_identity(self.config), 'basis': snapshot['basis'], 'source': batch['source'],
                   'request_key': 'capture-' + str(uuid.uuid4()), 'transaction': transaction,
                   'transaction_sha256': hashlib.sha256(transaction.encode()).hexdigest(),
                   'content_sha256': content_hash, 'batch_edn': dumps(batch), 'snapshot_edn': dumps(snapshot)}
        (self.directory / 'receipt.edn').unlink(missing_ok=True)
        (self.directory / 'receipt-request.json').unlink(missing_ok=True)
        atomic_json(self.intent_path, request)
        return request

    def submit(self, request):
        if any(request[k] != v for k,v in connection_identity(self.config).items()):
            raise ValueError('Pending request belongs to another database connection; retaining it unchanged')
        if hashlib.sha256(request['transaction'].encode()).hexdigest() != request['transaction_sha256']:
            raise ValueError('Saved request integrity check failed')
        tx_path = self.directory / 'transaction.edn'
        atomic_text(tx_path, request['transaction'])
        receipt_path = self.directory / 'receipt.edn'
        envelope = read_json(self.directory / 'receipt-request.json')
        if envelope and envelope.get('request_key') == request['request_key'] and envelope.get('transaction_sha256') == request['transaction_sha256']:
            try:
                receipt = loads(envelope['receipt_edn'])
                if receipt.get(':edb/committed') is True:
                    return receipt
            except (ValueError, IndexError, KeyError):
                pass
        # Retrying this complete saved request resolves a timeout even after basis advances.
        result = self.client.command('transact', '--file', tx_path, '--endpoint', request['endpoint'],
            '--request-key', request['request_key'], '--basis', request['basis'], '--source', request['source'], '--timeout-ms', 180000)
        atomic_text(receipt_path, result)
        atomic_json(self.directory / 'receipt-request.json', {'request_key': request['request_key'],
            'transaction_sha256': request['transaction_sha256'], 'receipt_edn': result})
        receipt = loads(result)
        if receipt.get(':edb/committed') is not True:
            raise VerificationError('Unknown submission outcome; retain and retry the exact request')
        return receipt

    def verify_receipt(self, request, receipt):
        if receipt.get(':edb/db-before-t') != request['basis']:
            raise VerificationError('Receipt basis differs from the original request')
        return validate_report(receipt, loads(request['batch_edn']), loads(request['snapshot_edn']), committed=True)

    def retire(self, request, status, details):
        """Only a confirmed rejection or fully verified commit can retire intent."""
        if status not in ('verified', 'rejected_stale_basis', 'confirmed_needs_reconciliation'):
            raise ValueError('Cannot retire an unresolved request')
        archive = self.directory / 'requests' / request['request_key']
        archive.mkdir(parents=True, exist_ok=True)
        atomic_json(archive / 'request.json', request)
        for name in ('receipt.edn', 'preview.edn', 'transaction.edn'):
            path = self.directory / name
            if path.exists():
                atomic_text(archive / name, path.read_text())
        atomic_json(archive / 'result.json', {'status': status, **details})
        # Receipt first: a crash before deleting the intent triggers an exact replay.
        (self.directory / 'receipt.edn').unlink(missing_ok=True)
        (self.directory / 'receipt-request.json').unlink(missing_ok=True)
        self.intent_path.unlink()
        from ..storage import _sync_directory
        _sync_directory(self.directory)
