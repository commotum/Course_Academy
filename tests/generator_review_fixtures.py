"""Structured boundary fixtures; these are not pedagogical certification."""
import json
import hashlib
from pathlib import Path
from scripts.generator_evidence import ROOT, TOOL_SOURCES, batch_sha256, record_sha256, sha256_file


def write_tool_evidence(directory, records, prefix="", engine_sha256=None):
    """Explicitly synthetic tool-bound fixtures, never pedagogical certification."""
    directory = Path(directory)
    identities = [record_sha256(row) for row in records]
    implementation = {name: sha256_file(ROOT / name) for name in TOOL_SOURCES.values()}
    input_name = prefix + "input.json"
    (directory / input_name).write_text(json.dumps(records))
    input_hash = sha256_file(directory / input_name)
    accepted_name = prefix + "accepted.json"
    (directory / accepted_name).write_text(json.dumps(records))
    captured = {}
    for name in ("source", "inventory"):
        file = prefix + name + ".json"
        (directory / file).write_text(json.dumps({"fixture": True}))
        captured[name] = {"file": file, "sha256": sha256_file(directory / file)}
    delivery = {"format": "course-academy-delivery-v1", "passed": True, "input_file": input_name,
                "input_sha256": input_hash, "record_sha256": identities, "checked_record_sha256": identities,
                "batch_sha256": batch_sha256(records), "accepted_file": accepted_name,
                "accepted_sha256": sha256_file(directory / accepted_name), "accepted_record_sha256": identities,
                "input_count": len(records), "accepted_count": len(records), "captured_inputs": captured,
                "implementation_sha256": implementation}
    checks = [{"submitted": "4", "expected": "accepted", "purpose": "Boundary fixture only"}]
    grader_input = [{"record": row, "checks": checks} for row in records]
    grader_name = prefix + "grading-input.json"
    (directory / grader_name).write_text(json.dumps(grader_input))
    grading = {"format": "course-academy-native-grading-v1", "passed": True, "input_file": grader_name,
               "input_sha256": sha256_file(directory / grader_name), "record_sha256": identities,
               "checked_record_sha256": identities, "implementation_sha256": implementation,
               "engine_sha256": engine_sha256 or "e" * 64, "accepted_checks": len(records), "rejected_checks": 0,
               "documented_unresolved_checks": 0, "records": [{"record_sha256": identity,
               "checks": [{"field_index": 0, "submitted_input": "4", "outcome": "accepted"}]} for identity in identities]}
    screenshot = prefix + "fixture.png"
    (directory / screenshot).write_bytes(b"synthetic screenshot boundary fixture")
    rendering = {"format": "course-academy-rendering-v1", "passed": True, "input_file": input_name,
                 "input_sha256": input_hash, "record_sha256": identities, "checked_record_sha256": identities,
                 "selection": {"input_count": len(records), "selected_indices": list(range(len(records))), "omitted_indices": []},
                 "runtime": {"browser_sha256": "b" * 64, "node_sha256": "c" * 64},
                 "implementation_sha256": implementation, "cases": [{"record_sha256": identity, "passed": True,
                 "state": state, "viewport": {"width": 1280, "height": 1000}, "screenshot": screenshot}
                 for identity in identities for state in ('active', 'completed')]}
    paths = {}
    for kind, report in (("grading", grading), ("rendering", rendering), ("delivery", delivery)):
        name = prefix + kind + ".json"
        (directory / name).write_text(json.dumps(report))
        paths[kind] = name
    return paths


def write_band_evidence(directory, binding=None, records_by_band=None):
    """Write explicit three-band boundary evidence for structured test agents."""
    directory = Path(directory)
    records_by_band = records_by_band or {band: [{"fixture": True, "band": band}] for band in ("easy", "moderate", "hard")}
    if binding is None:
        binding = {'verification_batches': {band: {
            'batch_hash': batch_sha256(records_by_band[band])}
            for band in ('easy', 'moderate', 'hard')}}
    (directory / 'final-binding.json').write_text(json.dumps(binding))
    result = {}
    for band in ('easy', 'moderate', 'hard'):
        name = f'{band}-verification.json'
        row = {'fixture': True, 'band': band,
               'batch_sha256': binding['verification_batches'][band]['batch_hash']}
        (directory / name).write_text(json.dumps(row))
        tools = write_tool_evidence(directory, records_by_band[band], band + '-', binding.get('grader_sha256'))
        result[band] = {'status': 'passed', 'batch_sha256': row['batch_sha256'],
                        'evidence_paths': [name, *tools.values()], 'details': 'Structured boundary fixture, not pedagogical certification.'}
    return result


def write_decision_evidence(directory):
    directory = Path(directory)
    name = 'pedagogical-variation.json'
    tools = write_tool_evidence(directory, [{'fixture': True, 'sample': 'decision'}])
    samples = ['decision-samples.json']
    (directory / samples[0]).write_text(json.dumps({'fixture': True, 'inputs': [2, 3], 'answers': [4, 9]}))
    report = {
        'learner_operation': 'Square the presented positive integer.',
        'fixed_features': [{'feature': 'One squaring operation', 'justification': 'The source teaches squaring, not selecting operators.'}],
        'answer_roles': [{'role': 'Presented operand', 'eligible_variation': 'Positive integers', 'observed': '2 and 3 require 4 and 9.'}],
        'coverage': [{'case': 'Operand-dependent result', 'sample_refs': samples, 'result': 'Both operands exercised.'}],
        'counterfactuals': [
            {'kind': 'relevant', 'change': 'Change operand 2 to 3.', 'expected': 'Answer and explanation change from 4 to 9.', 'observed': 'Answer, solution and grading follow the operand.', 'status': 'passed', 'justification': 'Operand determines the square.', 'sample_refs': samples},
            {'kind': 'irrelevant', 'change': 'Rename the surrounding context.', 'expected': 'Answer remains the square.', 'observed': 'Answer, solution and grading remain equivalent.', 'status': 'passed', 'justification': 'Context name is not an operand.', 'sample_refs': samples},
        ],
        'shortcut_probes': [{'cue': 'First number in prompt', 'subgroup': 'Single squaring template', 'scope': 'within_template', 'strategy': 'Copy operand without squaring.', 'correct': 0, 'total': 2, 'baseline': 0.5, 'disposition': 'not_predictive', 'conclusion': 'Copying the operand fails both controlled inputs.', 'sample_refs': samples}],
        'delivery': {'stages_examined': ['rejection', 'deduplication', 'difficulty', 'inventory selection'], 'sample_refs': [tools['delivery']], 'result': 'Fixture keeps both distinct inputs in the requested band.'},
        'limitations': ['Boundary fixture only; not a real independent review.'],
    }
    (directory / name).write_text(json.dumps(report))
    (directory / 'solution-paths.json').write_text(json.dumps({'cases': [{
        'template': 'square', 'field_key': 'answer', 'final_expression': '9',
        'keyed_answer': '9', 'domain': 'Positive integers', 'conversions': [],
        'sample_refs': samples, 'status': 'passed',
        'conclusion': 'The worked multiplication ends at the keyed integer.'}]}))
    return name
