"""Persist generator verification independently of question publication.

The pipeline validates the verifier's report and files before calling this
module. These checks bind that decision to the final package, engine and every
difficulty's sampled questions; they do not make pedagogical judgments.
"""
from copy import deepcopy
import hashlib
import json
import re


BANDS = ('easy', 'moderate', 'hard')


class ApprovalError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _hash(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def _binding_valid(binding, identity, policy_version, engine_hash):
    if (not isinstance(binding, dict)
            or binding.get('policy_version') != policy_version
            or binding.get('package_hash') != identity.get('package_sha256')
            or not _hash(binding.get('package_hash'))
            or not _hash(binding.get('source_hash'))
            or not _hash(binding.get('engine_hash'))
            or binding.get('engine_hash') != engine_hash):
        return False
    batches = binding.get('verification_batches')
    return (isinstance(batches, dict) and set(batches) == set(BANDS)
            and all(isinstance(batch, dict) and _hash(batch.get('batch_hash'))
                    and isinstance(batch.get('count'), int) and not isinstance(batch['count'], bool)
                    and batch['count'] > 0 and isinstance(batch.get('seed'), int)
                    and not isinstance(batch['seed'], bool) and isinstance(batch.get('assets'), dict)
                    and all(isinstance(path, str) and _hash(value) for path, value in batch['assets'].items())
                    for batch in batches.values()))


def make_approval(identity, review, binding, review_path, publication, published_band,
                  policy_version, *, publication_batch_hash=None):
    """Create one all-band approval, without inventing publication receipts.

    ``publication_batch_hash`` identifies the actual published questions. It
    may differ from a newly sampled verification batch during catch-up review.
    """
    if not isinstance(binding, dict) or not _binding_valid(binding, identity, policy_version, binding.get('engine_hash')):
        raise ValueError('Generator approval requires complete final all-band input bindings')
    if not isinstance(review, dict) or review.get('verdict') != 'accepted':
        raise ValueError('Generator approval requires an accepted review')
    reports = review.get('band_verification')
    if not isinstance(reports, dict) or set(reports) != set(BANDS):
        raise ValueError('Generator approval requires verification of easy, moderate and hard')
    if (published_band not in BANDS or not isinstance(publication, dict)
            or publication.get('passed') is not True):
        raise ValueError('Generator approval requires the actual verified publication receipt')
    if publication_batch_hash is None:
        publication_batch_hash = binding.get('batch_hash')
    if not _hash(publication_batch_hash):
        raise ValueError('Generator approval requires the actual published batch identity')
    if not isinstance(review_path, str) or not review_path:
        raise ValueError('Generator approval requires a saved review path')
    review_hash = _digest(review)
    bands = {}
    for band in BANDS:
        report = reports[band]
        batch = binding['verification_batches'][band]
        if (not isinstance(report, dict) or report.get('status') != 'passed'
                or report.get('batch_sha256') != batch['batch_hash']
                or not isinstance(report.get('evidence_paths'), list) or not report['evidence_paths']
                or any(not isinstance(path, str) or not path.strip() for path in report['evidence_paths'])):
            raise ValueError('Generator approval requires final passing evidence for ' + band)
        bands[band] = {
            'review_policy_version': policy_version,
            'review_sha256': review_hash,
            'batch_sha256': batch['batch_hash'],
            'engine_sha256': binding['engine_hash'],
            'evidence': review_path,
            'evidence_paths': deepcopy(report['evidence_paths']),
        }
    return {
        'format': 2,
        'identity': deepcopy(identity),
        'verification_binding': deepcopy(binding),
        'bands': bands,
        'publication': {
            'difficulty': published_band,
            'batch_sha256': publication_batch_hash,
            'receipt': deepcopy(publication),
        },
    }


def approved_band(value, identity, band, policy_version, engine_hash):
    """Resolve eligibility from recorded verification, never publication scope."""
    if not isinstance(value, dict) or value.get('identity') != identity:
        raise ApprovalError('source_changed', 'Registered package approval does not match current instructional source')
    bands = value.get('bands')
    if not isinstance(bands, dict):
        raise ApprovalError('approval_invalid', 'Registered generator approval is incomplete')
    if band not in bands:
        raise ApprovalError('approval_band_missing', 'Registered package has not been reviewed for ' + band)
    approval = bands[band]
    # Old single-band records remain evidence of their original scope only.
    # They cannot satisfy the new all-band policy or be upgraded by relabeling.
    if (value.get('format') == 1 or not isinstance(approval, dict)
            or approval.get('review_policy_version') != policy_version):
        raise ApprovalError('approval_policy_stale', 'Registered package needs an independent review under the current policy')
    if value.get('format') != 2:
        raise ApprovalError('approval_invalid', 'Registered generator approval format is not supported')
    binding = value.get('verification_binding')
    if isinstance(binding, dict) and binding.get('engine_hash') != engine_hash:
        raise ApprovalError('approval_engine_changed', 'Registered package needs verification against the current answer engine')
    if not _binding_valid(binding, identity, policy_version, engine_hash) or set(bands) != set(BANDS):
        raise ApprovalError('approval_invalid', 'Registered generator approval has incomplete all-band input bindings')
    publication = value.get('publication')
    if (not isinstance(publication, dict) or publication.get('difficulty') not in BANDS
            or not _hash(publication.get('batch_sha256'))
            or not isinstance(publication.get('receipt'), dict)
            or publication['receipt'].get('passed') is not True):
        raise ApprovalError('approval_invalid', 'Registered generator has no verified publication receipt')
    review_hashes, evidence_roots = set(), set()
    for name in BANDS:
        record = bands[name]
        if (not isinstance(record, dict) or record.get('review_policy_version') != policy_version
                or not _hash(record.get('review_sha256'))
                or record.get('batch_sha256') != binding['verification_batches'][name]['batch_hash']
                or record.get('engine_sha256') != engine_hash
                or not isinstance(record.get('evidence'), str) or not record['evidence']
                or not isinstance(record.get('evidence_paths'), list) or not record['evidence_paths']
                or any(not isinstance(path, str) or not path.strip() for path in record['evidence_paths'])
                or 'publication' in record):
            raise ApprovalError('approval_invalid', 'Registered generator approval has invalid verification for ' + name)
        review_hashes.add(record['review_sha256'])
        evidence_roots.add(record['evidence'])
    if len(review_hashes) != 1 or len(evidence_roots) != 1:
        raise ApprovalError('approval_invalid', 'Generator bands must share one final verification session')
    return {'identity': deepcopy(identity), 'difficulty': band, 'approval': deepcopy(approval)}
