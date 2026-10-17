"""Apply the shared UI math convention after accepting original source evidence.

The capture package is itself named ``scripts`` when run from ``capture/``.
Load the repository's dependency-free formatter by path to avoid importing that
package under the wrong name. Saved request transactions never pass this layer.
"""
from functools import lru_cache
import importlib.util
from pathlib import Path

from .text import markdown


@lru_cache(maxsize=1)
def formatter():
    path = Path(__file__).resolve().parents[3] / 'scripts/question_capture/math_format.py'
    spec = importlib.util.spec_from_file_location('course_academy_capture_math_format', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def value(kind, source):
    """Canonical display spelling only; image references stay byte-for-byte."""
    if kind == 'math':
        return formatter().normalize_tex(source)
    if kind == 'text':
        return formatter().normalize_prose(source)
    return source


def prose(source):
    return formatter().validate_prose(value('text', markdown(source)))


def question(source):
    """Normalize an already verified copy without rewriting its source evidence."""
    for key in ('problem', 'worked_solution', 'local_problem'):
        if isinstance(source.get(key), str):
            source[key] = prose(source[key])
    for field in source.get('answer_fields', []):
        correct = (field['correct_type'], field['correct_value'])
        seen = {}
        for choice in field.get('choices', []):
            original = (choice['type'], choice['value'])
            choice['value'] = value(*original)
            signature = (choice['type'], choice['value'])
            if signature in seen and seen[signature] != original:
                raise ValueError('Distinct source choices collapse after math formatting')
            seen[signature] = original
            if choice['type'] == 'math':
                formatter().validate_tex(choice['value'])
            elif choice['type'] == 'text':
                formatter().validate_prose(choice['value'])
            if original == correct:
                field['correct_value'] = choice['value']
            if choice.get('feedback') is not None:
                choice['feedback'] = prose(choice['feedback'])
    return source
