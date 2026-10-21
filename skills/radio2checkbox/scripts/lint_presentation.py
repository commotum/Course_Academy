#!/usr/bin/env python3
"""Read-only presentation checks for reviewed radio-to-checkbox objects.

CLI input: {"cases": [{"question": <full question>, "objects": [
  {"source_label": "I", "field_id": <UUID or db/id>,
   "content": "The complete selectable statement or mathematical object",
   "source_fragment": "optional exact old prompt fragment"}
]}]}. Shared-image exceptions add {"shared_image": {"image": "graphs.svg", "evidence": "path/hash",
"reason": "why this object must remain in a shared image"}} per object.

This checks presentation, not mathematical truth, grading, or transaction safety.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def canonical(text):
    text = re.sub(r'\*\*|__|\$', '', text)
    text = re.sub(r'\\(?:[,;!]|qquad\b|quad\b)', '', text)
    return re.sub(r'\s+', '', text)


def bare_label(text):
    text = re.sub(r'[*_$`{}]', '', text).strip().strip('().: ')
    return bool(re.fullmatch(r'(?:[IVXLCDM]+|[A-Z]|(?:Statement|Option|Matrix|Graph|Diagram)\s+(?:[IVXLCDM]+|[A-Z]|\d+))', text, re.I))


def matrix_bodies(text):
    return {canonical(m[1]) for m in re.finditer(
        r'\\begin\{(?:aligned|bmatrix|pmatrix|matrix|array)\}(?:\{[clr|]+\})?(.*?)'
        r'\\end\{(?:aligned|bmatrix|pmatrix|matrix|array)\}', text, re.S)}


def is_matrix_object(text):
    """Distinguish a selectable matrix from a statement about a shared matrix."""
    text = text.strip().strip('$').strip()
    text = re.sub(r'^[A-Za-z]\s*=\s*', '', text)
    return bool(re.fullmatch(
        r'\\begin\{(?:aligned|bmatrix|pmatrix|matrix|array)\}[\s\S]*'
        r'\\end\{(?:aligned|bmatrix|pmatrix|matrix|array)\}', text))


def ident(value):
    return value.get(':db/ident') if isinstance(value, dict) else str(value)


def visible_image(prompt, source):
    if not isinstance(source, str) or not source.strip():
        return False
    value = re.escape(source)
    return bool(re.search(r'!\[[^\]]*\]\(\s*<?' + value + r'>?(?:\s+["\'][^)]*["\'])?\s*\)', prompt)
                or re.search(r'<img\b[^>]*\bsrc=["\']' + value + r'["\']', prompt, re.I))


def lint_question(question, objects):
    """Return findings; `objects` is the reviewed source-to-field mapping."""
    errors = []
    qid = str(question.get(':db/id', question.get(':question/id', 'unknown')))
    def fail(code, message, field=None):
        errors.append({'question': qid, 'field': field, 'code': code, 'message': message})

    prompt = question.get(':question/problem', '')
    solution = question.get(':question/worked-solution', '')
    fields = [f for f in question.get(':question/answer-fields', [])
              if ident(f.get(':answer-field/type')) == ':answer-field.type/checkbox']
    if not fields:
        fail('no_checkbox_fields', 'Expected the proposed or repaired checkbox fields.')
        return errors
    if not isinstance(objects, list) or len(objects) != len(fields):
        fail('object_count', 'Reviewed selectable objects must cover every checkbox field exactly once.')
        return errors
    seen_fields, seen_labels = set(), set()
    for obj in objects:
        fid = str(obj.get('field_id', ''))
        matches = [f for f in fields if fid in {str(f.get(':db/id', '')), str(f.get(':answer-field/id', ''))}]
        if not fid or len(matches) != 1 or fid in seen_fields:
            fail('field_mapping', 'Each object must identify one distinct checkbox field.', fid)
            continue
        f = matches[0]
        identity = str(f.get(':answer-field/id', f.get(':db/id')))
        if identity in seen_fields:
            fail('field_mapping', 'Two objects map to the same checkbox field.', fid)
            continue
        seen_fields.add(identity)
        label = str(obj.get('source_label', '')).strip()
        if not label or label in seen_labels:
            fail('source_mapping', 'Keep a unique source label in the evidence mapping.', fid)
        seen_labels.add(label)
        content, key = obj.get('content', ''), f.get(':answer-field/key', '')
        if not isinstance(content, str) or not content.strip():
            fail('missing_object', 'Record the complete selectable object, not just its source label.', fid)
            continue
        if canonical(key) != canonical(content):
            fail('incomplete_field', 'The checkbox key must contain the complete reviewed object.', fid)
        shared = obj.get('shared_image')
        if shared is not None:
            if not (isinstance(shared, dict) and shared.get('evidence') and shared.get('reason')
                    and visible_image(prompt, shared.get('image'))):
                fail('unsupported_image_exception', 'Shared-image labels need the specified image in the prompt and recorded evidence/reason.', fid)
            else:
                continue
        if bare_label(key) or bare_label(content):
            fail('bare_label', 'Checkboxes must show the object; bare Roman, letter, or object-number references are insufficient.', fid)
        if canonical(content) and canonical(content) in canonical(prompt):
            fail('object_left_in_prompt', 'The selectable object still appears in the problem statement.', fid)
        fragment = obj.get('source_fragment', '')
        # Source fragments are exact old prompt spans. Removing math delimiters
        # and spaces here confuses a bullet "- $0$" with a term such as -0.5.
        if fragment and re.sub(r'\s+', ' ', fragment).strip() in re.sub(r'\s+', ' ', prompt):
            fail('source_left_in_prompt', 'The original selectable prompt fragment was not removed.', fid)
        if is_matrix_object(content) and matrix_bodies(content) & matrix_bodies(prompt):
            fail('matrix_left_in_prompt', 'A selectable matrix remains in the stem as well as its checkbox field.', fid)
        if label and re.search(r'(?m)^\s*(?:[-*+]\s*)?(?:\*\*)?' + re.escape(label) + r'[.)](?:\*\*)?\s+\S', prompt):
            fail('list_left_in_prompt', 'The source-labelled selectable list remains in the problem statement.', fid)
        if re.fullmatch(r'[IVXLCDM]+', label):
            reference = r'\b(?:statements?|options?)\s+(?:\*\*)?' + re.escape(label) + r'\b|["“]' + re.escape(label) + r'(?:\s+only\b|\s+and\b|,|["”])'
            if re.search(reference, solution, re.I):
                fail('removed_solution_label', 'Replace references to removed Roman choices with their actual content.', fid)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    document = json.loads(args.input.read_text())
    cases = document['cases']
    findings = [finding for case in cases for finding in lint_question(case['question'], case['objects'])]
    report = {'status': 'fail' if findings else 'pass', 'questions': len(cases), 'findings': findings}
    rendered = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end='')
    return int(bool(findings))


if __name__ == '__main__':
    raise SystemExit(main())
