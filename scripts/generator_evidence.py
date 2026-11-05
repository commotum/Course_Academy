"""Identity and integrity checks for offline generator tools, not pedagogical proof."""
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FORMATS = {
    'course-academy-native-grading-v1': 'grading',
    'course-academy-rendering-v1': 'rendering',
    'course-academy-delivery-v1': 'delivery',
}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def record_sha256(record):
    """Fingerprint the actual record, including solution, response and metadata."""
    return hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def batch_sha256(records):
    # Matches the runner's existing digest; do not change approval identities.
    return hashlib.sha256(json.dumps(records, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def implementation_hashes(paths, root=ROOT):
    """Hash local transitive Python imports, including lazily imported topic guards.

    This records code provenance, not proof that every imported branch executed.
    Restrict traversal to repository Python sources; never import/execute them.
    """
    root = Path(root).resolve()
    pending, found = [Path(p).resolve() for p in paths], {}
    while pending:
        path = pending.pop()
        if not path.is_relative_to(root) or not path.is_file():
            continue
        name = str(path.relative_to(root))
        if name in found:
            continue
        found[name] = sha256_file(path)
        if path.suffix != '.py':
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                modules = [node.module]
            for module in modules:
                candidate = root / (module.replace('.', '/') + '.py')
                if candidate.is_file():
                    pending.append(candidate)
    return dict(sorted(found.items()))


def _local(path, root, label):
    if not isinstance(path, (str, Path)) or not str(path):
        raise ValueError(f'{label} must be a local relative evidence path')
    path = Path(path)
    root = Path(root).resolve()
    if path.is_absolute() or '..' in path.parts:
        raise ValueError(f'{label} must be a local relative evidence path')
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError(f'{label} is missing or escapes the evidence directory')
    return resolved


def _hash(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def validate_tool_report(path, evidence_root, *, engine_sha256=None):
    """Return a recognized, input-bound passing report; None for other evidence.

    The reviewer still judges sufficiency, valid equivalents, visual meaning and
    instructional intent. A success here certifies only these mechanical claims.
    """
    path = Path(path).resolve()
    root = Path(evidence_root).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Tool report escapes evidence directory')
    try:
        report = json.loads(path.read_text())
    except (UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(report, dict) or report.get('format') not in FORMATS:
        return None
    kind = FORMATS[report['format']]
    if report.get('passed') is not True:
        raise ValueError(f'{kind} tool report is not passed')
    source = _local(report.get('input_file', ''), path.parent, f'{kind} input_file')
    if not source.is_relative_to(root) or report.get('input_sha256') != sha256_file(source):
        raise ValueError(f'{kind} input hash mismatch')
    data = json.loads(source.read_text())
    if not isinstance(data, list) or not data:
        raise ValueError(f'{kind} requires nonempty input records')
    records = [row.get('record') for row in data] if kind == 'grading' else data
    expected = [record_sha256(row) for row in records]
    if report.get('record_sha256') != expected:
        raise ValueError(f'{kind} record fingerprints differ from its input')
    if not isinstance(report.get('implementation_sha256'), dict) or not report['implementation_sha256']:
        raise ValueError(f'{kind} implementation identities are missing')
    if any(not _hash(v) for v in report['implementation_sha256'].values()):
        raise ValueError(f'{kind} implementation identity is invalid')
    for name, identity in report['implementation_sha256'].items():
        current = ROOT / name
        if current.is_file() and current.resolve().is_relative_to(ROOT) and sha256_file(current) != identity:
            raise ValueError(f'{kind} implementation changed: {name}')
    checked = report.get('checked_record_sha256')
    if not isinstance(checked, list) or not checked or not set(checked) <= set(expected):
        raise ValueError(f'{kind} checked record coverage is empty or mismatched')
    if kind == 'grading':
        if not _hash(report.get('engine_sha256')) or (engine_sha256 is not None and report['engine_sha256'] != engine_sha256):
            raise ValueError('grading engine identity differs from the final review')
        rows = report.get('records')
        if not isinstance(rows, list) or len(rows) != len(data):
            raise ValueError('grading record coverage is incomplete')
        totals = {'accepted': 0, 'rejected': 0, 'unresolved': 0}
        for index, (row, original) in enumerate(zip(rows, data)):
            checks = row.get('checks')
            if row.get('record_sha256') != expected[index] or not isinstance(checks, list) or not checks:
                raise ValueError('grading requires checked actual records')
            if len(checks) != len(original.get('checks', [])):
                raise ValueError('grading check coverage differs from input')
            for check, requested in zip(checks, original['checks']):
                outcome = check.get('outcome')
                if outcome not in totals or outcome != requested.get('expected'):
                    raise ValueError('grading outcome differs from its expected result')
                if check.get('field_index') != requested.get('field_index', 0) or check.get('submitted_input') != requested.get('submitted_answer_id', requested.get('submitted')):
                    raise ValueError('grading response differs from its tested input')
                totals[outcome] += 1
        if totals['unresolved'] or report.get('documented_unresolved_checks') != 0:
            raise ValueError('unresolved grading is not a successful acceptance check')
        for outcome in ('accepted', 'rejected'):
            if report.get(outcome + '_checks') != totals[outcome]:
                raise ValueError('grading counts differ from actual checks')
    elif kind == 'rendering':
        rows = report.get('cases')
        if not isinstance(rows, list) or not rows:
            raise ValueError('rendering has no observed cases')
        for row in rows:
            if row.get('passed') is not True or row.get('record_sha256') not in checked:
                raise ValueError('rendering case failed or has mismatched input')
            if row.get('state') not in ('active', 'completed'):
                raise ValueError('rendering state is missing')
            viewport = row.get('viewport', {})
            if any(type(viewport.get(k)) is not int or viewport[k] <= 0 for k in ('width', 'height')):
                raise ValueError('rendering viewport is missing')
            _local(row.get('screenshot', ''), path.parent, 'rendering screenshot')
    else:
        if report.get('batch_sha256') != batch_sha256(records):
            raise ValueError('delivery batch identity mismatch')
        accepted_file = _local(report.get('accepted_file', ''), path.parent, 'delivery accepted_file')
        if report.get('accepted_sha256') != sha256_file(accepted_file):
            raise ValueError('delivery accepted file hash mismatch')
        accepted = json.loads(accepted_file.read_text())
        if report.get('accepted_record_sha256') != [record_sha256(row) for row in accepted]:
            raise ValueError('delivery accepted record identities mismatch')
        if report.get('input_count') != len(records) or report.get('accepted_count') != len(accepted):
            raise ValueError('delivery counts differ from actual records')
        for name in ('source', 'inventory'):
            capture = report.get('captured_inputs', {}).get(name, {})
            captured = _local(capture.get('file'), path.parent, 'delivery ' + name)
            if capture.get('sha256') != sha256_file(captured):
                raise ValueError('delivery captured ' + name + ' hash mismatch')
    return report
