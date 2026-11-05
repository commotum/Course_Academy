"""Bounded checks of actual publication survivors; no database operations.

An optional package checker adds reviewed semantic regressions. The native
fallback checks the actual response controls, not generator-declared metadata.
Finite exhaustion requires an enforced, package-bound complete catalog.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import re

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
    path = (Path(root) / name).resolve()
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
                prompt = question[':question/problem'].lower()
                value = selected[':answer/value']
                # Do not invent a universal wrong expression: +C, external
                # squaring and response fragments can change equivalence.
                if (enum(selected[':answer/type']) == ':answer.type/math'
                        and re.fullmatch(r'[+-]?\d+(?:\.\d+)?', value)
                        and not any(marker in prompt for marker in ('arbitrary', '+c', '+ c', 'integrat', 'family'))):
                    wrong = '1' if float(value) == 0 else '0'
                    checks.append({'field_index': field_index, 'submitted': wrong,
                                   'expected': 'rejected', 'purpose': 'distinct simple numeric response'})
                elif enum(selected[':answer/type']) == ':answer.type/text':
                    checks.append({'field_index': field_index, 'submitted': value + ' __incorrect__',
                                   'expected': 'rejected', 'purpose': 'distinct text response'})
        cases.append({'label': 'publication-survivor-' + str(index), 'record': record, 'checks': checks})
    return cases


def validate_survivors(records, inventory_snapshot, directory, *, root, manifest,
                       band, python, repo_root, environment):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    before = package_digest(root, manifest['entrypoint'], manifest['files'], dependencies=manifest.get('dependencies'))
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
    _write(inventory_path, {'fingerprints': inventory})
    cases = native_cases(grading_records)
    descriptor_name = 'refill-validation.json'
    if records and descriptor_name in manifest['files']:
        contract = _read(declared_file(root, manifest, descriptor_name))
        if contract.get('format') != 'course-academy-refill-check-v1':
            raise ValueError('Invalid refill-validation.json format')
        script = declared_file(root, manifest, contract.get('script'))
        args = contract.get('args', [])
        files = contract.get('files', [])
        if (script.suffix != '.py' or not isinstance(args, list)
                or any(not isinstance(arg, str) or '\0' in arg for arg in args)
                or not isinstance(files, list)):
            raise ValueError('Refill check needs a Python script, string arguments and declared files')
        for name in files:
            declared_file(root, manifest, name)
        report_path = directory / 'package-check.json'
        report_path.unlink(missing_ok=True)
        completed = subprocess.run([python, '-E', '-s', '-B', str(script), *args,
            '--records', str(records_path), '--inventory', str(inventory_path), '--output', str(report_path)],
            cwd=root, env=environment, capture_output=True, text=True, timeout=180)
        (directory / 'package-check.stderr').write_text(completed.stderr)
        if completed.returncode:
            raise ValueError('Package refill regression failed: ' + completed.stderr[-2000:])
        report = _read(report_path)
        if (report.get('status') != 'passed' or not fingerprints
                or sorted(report.get('checked_fingerprints', [])) != fingerprints):
            raise ValueError('Package refill check must pass and cover every actual surviving question')
        # Optional extra wrong/equivalent forms must run through the native
        # grader against our actual record, not a checker-supplied replacement.
        by_fingerprint = {content_fingerprint(case['record']['question']): case for case in cases}
        for extra in report.get('native_checks', []):
            target = by_fingerprint.get(extra.get('fingerprint'))
            if target is None or not isinstance(extra.get('checks'), list):
                raise ValueError('Refill native checks reference an unserved record')
            for check in extra['checks']:
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
