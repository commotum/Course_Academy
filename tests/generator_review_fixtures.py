"""Structured boundary fixtures; these are not pedagogical certification."""
import json
from pathlib import Path


def write_decision_evidence(directory):
    directory = Path(directory)
    name = 'pedagogical-variation.json'
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
        'delivery': {'stages_examined': ['rejection', 'deduplication', 'difficulty', 'inventory selection'], 'sample_refs': samples, 'result': 'Fixture keeps both distinct inputs in the requested band.'},
        'limitations': ['Boundary fixture only; not a real independent review.'],
    }
    (directory / name).write_text(json.dumps(report))
    (directory / 'solution-paths.json').write_text(json.dumps({'cases': [{
        'template': 'square', 'field_key': 'answer', 'final_expression': '9',
        'keyed_answer': '9', 'domain': 'Positive integers', 'conversions': [],
        'sample_refs': samples, 'status': 'passed',
        'conclusion': 'The worked multiplication ends at the keyed integer.'}]}))
    return name
