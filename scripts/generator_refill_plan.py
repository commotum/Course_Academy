"""Bind reviewed survivor obligations to an immutable generator package.

Applicability is the independent reviewer's judgment. This module requires that
judgment, links every retained finding, and prevents silently dropping its checks.
"""
import hashlib
import json
from pathlib import Path

PLAN = 'refill-review-plan.json'
FORMAT = 'course-academy-refill-plan-v1'


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Refill plan requires ' + label)


def _strings(value, label, *, required=False):
    if (not isinstance(value, list) or (required and not value)
            or any(not isinstance(item, str) or not item.strip() for item in value)
            or len(set(value)) != len(value)):
        raise ValueError('Refill plan requires distinct ' + label)


def _rationale(row, label, evidence_root):
    _text(row.get('reason'), label + ' reason')
    _strings(row.get('source_refs'), label + ' source_refs', required=True)
    _strings(row.get('evidence_paths'), label + ' evidence_paths', required=True)
    for name in row['evidence_paths']:
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Refill plan evidence must be review-root relative')
        if evidence_root is not None:
            root = Path(evidence_root).resolve()
            path = (root / relative).resolve()
            if not path.is_relative_to(root) or not path.is_file() or not path.stat().st_size:
                raise ValueError('Refill plan evidence is missing or escapes the review')


def load_refill_plan(root, manifest, *, expected=None):
    """Read a declared plan; an absent plan is allowed only for legacy approvals."""
    from scripts.generator_refill import declared_file
    if PLAN not in manifest['files']:
        if expected is not None:
            raise ValueError('Approved refill plan is missing from the package')
        return None, None
    path = declared_file(root, manifest, PLAN)
    plan = json.loads(path.read_text())
    if not isinstance(plan, dict) or plan.get('format') != FORMAT or plan.get('status') not in ('checks', 'not_applicable'):
        raise ValueError('Invalid refill review plan')
    _rationale(plan, 'applicability', None)
    checks, exemptions = plan.get('checks'), plan.get('finding_exemptions')
    if not isinstance(checks, list) or not isinstance(exemptions, list):
        raise ValueError('Refill plan requires checks and finding_exemptions arrays')
    ids, covered = set(), set()
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError('Refill plan check must be an object')
        _text(check.get('id'), 'check id'); _text(check.get('purpose'), 'check purpose')
        if check['id'] in ids:
            raise ValueError('Duplicate refill check id')
        ids.add(check['id'])
        _strings(check.get('finding_ids'), 'check finding_ids')
        covered.update(check['finding_ids'])
    exempted = set()
    for row in exemptions:
        if not isinstance(row, dict):
            raise ValueError('Refill finding exemption must be an object')
        _text(row.get('id'), 'exempted finding id'); _rationale(row, 'finding exemption', None)
        if row['id'] in exempted or row['id'] in covered:
            raise ValueError('Refill finding has conflicting dispositions')
        exempted.add(row['id'])
    descriptor = 'refill-validation.json'
    if plan['status'] == 'checks':
        if not checks:
            raise ValueError('Applicable refill plan requires executable checks')
        contract = json.loads(declared_file(root, manifest, descriptor).read_text())
        if not isinstance(contract, dict) or contract.get('format') != 'course-academy-refill-check-v1':
            raise ValueError('Refill plan requires a valid declared checker')
        declared_file(root, manifest, contract.get('script'))
        for name in contract.get('files', []):
            declared_file(root, manifest, name)
    elif checks or descriptor in manifest['files']:
        raise ValueError('Nonapplicable refill plan cannot conceal declared checks')
    binding = {'format': FORMAT, 'path': PLAN, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
               'status': plan['status'], 'check_ids': sorted(ids), 'finding_ids': sorted(covered | exempted)}
    if expected is not None and binding != expected:
        raise ValueError('Package refill plan differs from its approved binding')
    return plan, binding


def validate_refill_plan(root, manifest, retained_findings, evidence_root):
    """Required for a new approval; retain evidence independently of runtime files."""
    plan, binding = load_refill_plan(root, manifest)
    if plan is None:
        raise ValueError('New approval requires declared refill-review-plan.json with checks or justified nonapplicability')
    _rationale(plan, 'applicability', evidence_root)
    for row in plan['finding_exemptions']:
        _rationale(row, 'finding exemption', evidence_root)
    required = {row['id'] for row in retained_findings}
    if set(binding['finding_ids']) != required:
        raise ValueError('Refill plan must cover or justify nonapplicability for every retained finding; missing='
                         + repr(sorted(required - set(binding['finding_ids']))) + '; unknown='
                         + repr(sorted(set(binding['finding_ids']) - required)))
    return binding


def validate_check_results(report, binding, fingerprints):
    """Each retained executable obligation examines the actual delivery survivors."""
    if binding is None:
        return
    rows = report.get('check_results')
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError('Refill checker must report its approved check_results')
    if len(rows) != len(binding['check_ids']) or {row.get('id') for row in rows} != set(binding['check_ids']):
        raise ValueError('Refill checker omitted or changed an approved check')
    for row in rows:
        if row.get('status') != 'passed' or row.get('checked_fingerprints') != fingerprints:
            raise ValueError('Each approved refill check must pass on the actual survivors')


def validate_reviewed_refill(root, manifest, retained_findings, evidence_root, *,
                            batches, source, inventory, math_root, repo_root, python, environment):
    """Execute a new approval's applicable checks through real offline delivery."""
    from generate.pipeline.check_delivery import audit
    from scripts.generator_refill import validate_survivors
    binding = validate_refill_plan(root, manifest, retained_findings, evidence_root)
    result = {'plan': binding, 'bands': {}}
    if binding['status'] == 'not_applicable':
        return result
    for band, batch in batches.items():
        directory = Path(evidence_root) / 'refill-checks' / band
        records = json.loads(Path(batch['batch_file']).read_text())
        delivery = audit(records, inventory, source, band, directory / 'delivery',
                         batch.get('assets_directory', Path(batch['batch_file']).parent), math_root)
        delivered = json.loads((directory / 'delivery' / delivery['accepted_file']).read_text())
        report = validate_survivors(delivered, inventory, directory / 'checks', root=root,
            manifest=manifest, band=band, python=python, repo_root=repo_root,
            environment=environment, expected_plan=binding)
        if report['status'] not in ('passed', 'finite-limit'):
            raise ValueError('Refill regression verification needs surviving records or a proven usable finite catalog in ' + band)
        result['bands'][band] = {'batch_sha256': delivery['batch_sha256'],
            'delivered_sha256': delivery['accepted_sha256'], 'plan_sha256': binding['sha256'],
            'delivery': str(directory / 'delivery' / 'delivery.json'),
            'report': str(directory / 'checks' / 'result.json')}
    return result
