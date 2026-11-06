"""Bounded checks of actual publication survivors; no database operations.

An optional package checker adds reviewed semantic regressions. The native
fallback checks the actual response controls, not generator-declared metadata.
Finite exhaustion requires an enforced, package-bound complete catalog.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from scripts.generator_packages import package_digest
from scripts.generator_publish import answer_id, content_fingerprint, enum, validate_question, normalized_question


def _read(path):
    return json.loads(Path(path).read_text())


def _write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n')


def declared_file(root, manifest, name):
    if not isinstance(name, str) or name not in manifest['files']:
        raise ValueError('Refill contract file must be declared in the package: ' + str(name))
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Refill contract file must be package relative')
    path = Path(root)
    for part in relative.parts:
        path /= part
        if path.is_symlink():
            raise ValueError('Refill contract file cannot use symlinks')
    path = path.resolve()
    if not path.is_relative_to(Path(root).resolve()) or not path.is_file():
        raise ValueError('Refill contract file is missing or escapes the package')
    return path


def finite_catalog(root, manifest, band):
    if 'generation-limits.json' not in manifest['files']:
        return None
    limits = _read(declared_file(root, manifest, 'generation-limits.json'))
    catalogs = limits.get('finite_catalogs', {})
    if not isinstance(catalogs, dict) or any(key not in ('easy', 'moderate', 'hard') for key in catalogs):
        raise ValueError('finite_catalogs must map supported difficulty bands to declared record files')
    if band not in catalogs:
        return None
    path = declared_file(root, manifest, catalogs[band])
    records = _read(path)
    if not isinstance(records, list) or not records:
        raise ValueError('A finite catalog requires a nonempty complete record list')
    fingerprints = []
    for record in records:
        validate_question(record['question'])
        if enum(record['question'].get(':question/difficulty')) != ':question.difficulty/' + band:
            raise ValueError('Finite catalog has a record in the wrong band')
        fingerprints.append(content_fingerprint(record['question']))
    if len(set(fingerprints)) != len(fingerprints):
        raise ValueError('Finite catalog contains duplicate questions')
    return {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'fingerprints': sorted(fingerprints)}


def check_catalog_membership(root, manifest, band, records):
    catalog = finite_catalog(root, manifest, band)
    if catalog is not None and any(content_fingerprint(row['question']) not in catalog['fingerprints'] for row in records):
        raise ValueError('Generated question is outside the declared finite catalog')
    return catalog


def native_cases(records):
    cases = []
    for index, record in enumerate(records):
        question = record['question']
        validate_question(question)
        checks = []
        for field_index, field in enumerate(question[':question/answer-fields']):
            key = answer_id(field[':answer-field/correct'])
            choices = field[':answer-field/choices']
            selected = next(answer for answer in choices if str(answer[':answer/id']) == key)
            kind = enum(field[':answer-field/type'])
            if kind in (':answer-field.type/radio', ':answer-field.type/select', ':answer-field.type/checkbox'):
                for answer in choices:
                    checks.append({'field_index': field_index, 'submitted_answer_id': str(answer[':answer/id']),
                                   'expected': 'accepted' if str(answer[':answer/id']) == key else 'rejected',
                                   'purpose': 'actual selected answer control'})
            else:
                checks.append({'field_index': field_index, 'submitted': selected[':answer/value'],
                               'expected': 'accepted', 'purpose': 'actual canonical response'})
                # Contextual negatives/equivalents belong to the reviewed hook.
                # Neither numeric offsets nor text suffixes are universally
                # wrong under tolerance, fragment, or solution-family grading.
        cases.append({'label': 'publication-survivor-' + str(index), 'record': record, 'checks': checks})
    return cases


def _run_checker(root, manifest, contract, records, inventory, directory, python):
    """Relocation check: no workspace/repository path or environment is supplied.

    This is dependency isolation, not a security sandbox against hostile code.
    Installed declared Python dependencies remain available.
    """
    script = declared_file(root, manifest, contract.get('script'))
    args, files = contract.get('args', []), contract.get('files', [])
    if (script.suffix != '.py' or not isinstance(args, list) or not isinstance(files, list)
            or any(not isinstance(arg, str) or '\0' in arg or
                   Path(arg.split('=', 1)[-1]).is_absolute() or '..' in Path(arg.split('=', 1)[-1]).parts for arg in args)):
        raise ValueError('Refill check needs a Python script, package-relative arguments and declared files')
    for name in files:
        declared_file(root, manifest, name)
    before = package_digest(root, manifest['entrypoint'], manifest['files'], dependencies=manifest.get('dependencies'))
    with tempfile.TemporaryDirectory(prefix='course-academy-refill-', dir='/tmp') as temporary:
        temporary = Path(temporary)
        package, io = temporary / 'package', temporary / 'io'
        package.mkdir(); io.mkdir(); (temporary / 'home').mkdir(); (temporary / 'tmp').mkdir()
        for name in manifest['files']:
            destination = package / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(declared_file(root, manifest, name), destination)
        for name, value in (('records.json', records), ('inventory.json', inventory)):
            _write(io / name, value)
        # -I excludes ambient PYTHONPATH/user-site/cwd. Only the copied package
        # is deliberately restored for declared sibling imports.
        bootstrap = ('import runpy,sys; from pathlib import Path; '
                     'p=Path(sys.argv[1]); sys.path.insert(0,str(p.parent)); '
                     'sys.argv=sys.argv[1:]; runpy.run_path(str(p),run_name="__main__")')
        environment = {'PATH': os.defpath, 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
                       'HOME': str(temporary / 'home'), 'TMPDIR': str(temporary / 'tmp')}
        # Keep a virtualenv executable's symlink path: resolving it to the base
        # interpreter would discard the already-checked package dependencies.
        completed = subprocess.run([str(Path(python).absolute()), '-I', '-B', '-c', bootstrap,
            str(package / contract['script']), *args, '--records', str(io / 'records.json'),
            '--inventory', str(io / 'inventory.json'), '--output', str(io / 'report.json')],
            cwd=package, env=environment, capture_output=True, text=True, timeout=180)
        (directory / 'package-check.stderr').write_text(completed.stderr)
        if completed.returncode:
            raise ValueError('Package refill regression failed in declared-file isolation: ' + completed.stderr[-2000:])
        if before != package_digest(package, manifest['entrypoint'], manifest['files'], dependencies=manifest.get('dependencies')):
            raise ValueError('Refill validation modified its declared package')
        report = _read(io / 'report.json')
    _write(directory / 'package-check.json', report)
    return report


def validate_survivors(records, inventory_snapshot, directory, *, root, manifest,
                       band, python, repo_root, environment, expected_plan=None):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    before = package_digest(root, manifest['entrypoint'], manifest['files'], dependencies=manifest.get('dependencies'))
    from scripts.generator_refill_plan import load_refill_plan, validate_check_results
    plan, plan_binding = load_refill_plan(root, manifest, expected=expected_plan)
    catalog = check_catalog_membership(root, manifest, band, records)
    fingerprints = sorted(content_fingerprint(row['question']) for row in records)
    inventory = sorted(inventory_snapshot['fingerprints'])
    eligible = {}
    for question in inventory_snapshot.get('questions', []):
        if question.get(':question/retired'):
            continue
        try:
            normalized = normalized_question(question)
            for field in normalized[':question/answer-fields']:
                field[':answer-field/correct'] = [':answer/id', field[':answer-field/correct']]
            validate_question(normalized)
            eligible[content_fingerprint(normalized)] = {'question': normalized}
        except (KeyError, ValueError, TypeError):
            continue
    exhausted = catalog is not None and set(catalog['fingerprints']) <= set(eligible)
    result = {'format': 'course-academy-refill-validation-v1', 'checked_fingerprints': fingerprints,
              'records': len(records), 'finite_catalog': catalog, 'exhausted': exhausted,
              'refill_plan': plan_binding, 'legacy_fallback': plan is None,
              'inventory_sha256': hashlib.sha256(json.dumps(inventory).encode()).hexdigest()}
    if not records and not exhausted:
        result['status'] = 'no-new-records'
        result['reason'] = ('catalog_contains_retired_or_unusable_inventory' if catalog is not None
                            and set(catalog['fingerprints']) <= set(inventory) else 'sample_does_not_prove_exhaustion')
        _write(directory / 'result.json', result)
        return result
    # A zero-new-record finite outcome is justified only after checking the
    # existing nonretired catalog through the current native grader as well.
    grading_records = records if records else [eligible[fingerprint] for fingerprint in catalog['fingerprints']]
    records_path, inventory_path = directory / 'records.json', directory / 'inventory.json'
    _write(records_path, records)
    usable_inventory = {'fingerprints': inventory, 'usable_fingerprints': sorted(eligible),
                        'questions': [eligible[fingerprint]['question'] for fingerprint in sorted(eligible)]}
    usable_inventory['questions_sha256'] = hashlib.sha256(json.dumps(
        usable_inventory['questions'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    _write(inventory_path, usable_inventory)
    cases = native_cases(grading_records)
    result['limitations'] = [
        {'fingerprint': content_fingerprint(record['question']), 'field_index': index,
         'scope': 'Canonical acceptance only; contextual negatives and equivalents require reviewed package checks.'}
        for record in grading_records for index, field in enumerate(record['question'][':question/answer-fields'])
        if enum(field[':answer-field/type']) in (':answer-field.type/blank', ':answer-field.type/free')]
    descriptor_name = 'refill-validation.json'
    if descriptor_name in manifest['files']:
        contract = _read(declared_file(root, manifest, descriptor_name))
        if contract.get('format') != 'course-academy-refill-check-v1':
            raise ValueError('Invalid refill-validation.json format')
        report_path = directory / 'package-check.json'
        report_path.unlink(missing_ok=True)
        checked_records = records if records else grading_records
        checked_fingerprints = sorted(content_fingerprint(row['question']) for row in checked_records)
        report = _run_checker(root, manifest, contract, checked_records, usable_inventory, directory, python)
        covered = report.get('checked_fingerprints', []) if isinstance(report, dict) else None
        if (not isinstance(report, dict) or report.get('status') != 'passed' or not checked_fingerprints
                or not isinstance(covered, list) or any(not isinstance(value, str) for value in covered)
                or sorted(covered) != checked_fingerprints):
            raise ValueError('Package refill check must pass and cover every actual surviving question')
        validate_check_results(report, plan_binding, checked_fingerprints)
        # Optional extra wrong/equivalent forms must run through the native
        # grader against our actual record, not a checker-supplied replacement.
        by_fingerprint = {content_fingerprint(case['record']['question']): case for case in cases}
        extra_cases = report.get('native_checks', [])
        if not isinstance(extra_cases, list):
            raise ValueError('Refill native_checks must be a list')
        for extra in extra_cases:
            if not isinstance(extra, dict):
                raise ValueError('Refill native check must identify a surviving record')
            target = by_fingerprint.get(extra.get('fingerprint'))
            if target is None or not isinstance(extra.get('checks'), list):
                raise ValueError('Refill native checks reference an unserved record')
            for check in extra['checks']:
                if not isinstance(check, dict):
                    raise ValueError('Refill native check must be an object')
                fields = target['record']['question'][':question/answer-fields']
                index = check.get('field_index')
                if (type(index) is not int or not 0 <= index < len(fields)
                        or check.get('expected') not in ('accepted', 'rejected')
                        or not isinstance(check.get('purpose'), str) or not check['purpose'].strip()
                        or (('submitted' in check) == ('submitted_answer_id' in check))):
                    raise ValueError('Refill native check has invalid field, expected result or submission')
                submitted = check.get('submitted', check.get('submitted_answer_id'))
                if not isinstance(submitted, str) or not submitted.strip():
                    raise ValueError('Refill native checks require a nonempty learner response')
                if 'submitted_answer_id' in check and submitted not in {
                        str(answer[':answer/id']) for answer in fields[index][':answer-field/choices']}:
                    raise ValueError('Refill native check selects an unauthored answer')
            target['checks'].extend(extra['checks'])
        result['package_check'] = str(report_path)
        result['package_check_scope'] = 'survivors' if records else 'existing_catalog'
    inputs, native = directory / 'native-input.json', directory / 'native-report.json'
    _write(inputs, cases)
    completed = subprocess.run([str(Path(repo_root) / 'generate/runs/current/check-engine'), str(inputs), str(native)],
        cwd=repo_root, env=environment, capture_output=True, text=True, timeout=180)
    (directory / 'native.stderr').write_text(completed.stderr)
    if completed.returncode:
        raise ValueError('Native refill grading failed: ' + completed.stderr[-2000:])
    from scripts.generator_evidence import validate_tool_report
    report = validate_tool_report(native, directory, engine_sha256=hashlib.sha256(
        (Path(repo_root) / 'generate/runs/current/check-engine').read_bytes()).hexdigest())
    if (not report or report.get('passed') is not True
            or report.get('input_sha256') != hashlib.sha256(inputs.read_bytes()).hexdigest()):
        raise ValueError('Native refill grading evidence is missing, failed or bound to different inputs')
    if before != package_digest(root, manifest['entrypoint'], manifest['files'], dependencies=manifest.get('dependencies')):
        raise ValueError('Refill validation modified the approved package')
    result.update(status='finite-limit' if exhausted and not records else 'passed', native_report=str(native),
                  scope='No distinct catalog question remains to publish; this does not claim learner availability.')
    _write(directory / 'result.json', result)
    return result
