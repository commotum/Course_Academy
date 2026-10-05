#!/usr/bin/env python3
"""Prepare the saved history batch without contacting MA or writing to EDB.

Keep the original reconstruction and answer evidence immutable. Missing source
options are never invented: straightforward missing-option questions become
entered-answer questions; bounded categorical responses use explicitly local
choices. Image answers and ambiguous responses go to a separate review queue.
"""
import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reference/mathacademy/history-question-import-2026-10-04'
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from core import build_transaction, validate_question
from edn import dumps, loads

# Decompositions of saved conclusions; field labels specify response order.
COMPONENTS = {
    'q-28183': [('negative-imaginary', r'-1-7\text{i}'), ('positive-imaginary', r'-1+7\text{i}')],
    'q-28178': [('negative-imaginary', r'3-2\text{i}'), ('positive-imaginary', r'3+2\text{i}')],
    'q-66787': [('negative-imaginary', r'-3-2\text{i}'), ('positive-imaginary', r'-3+2\text{i}')],
    'q-66775': [('negative-imaginary', r'2-\sqrt{2}\text{i}'), ('positive-imaginary', r'2+\sqrt{2}\text{i}')],
    'q-48907': [('initial-position-m', '1'), ('initial-velocity-m-per-s', '2/e')],
    'q-48705': [('initial-position-m', '1/e^2'), ('initial-velocity-m-per-s', '3/e^2')],
    'q-73243': [('time-s', '2'), ('velocity-m-per-s', '-1/e^2')],
    'q-49233': [('f-of-x', r'\cos^2 x'), ('b', '0')],
    'q-73178': [('f-of-x', r'\sec^2 x'), ('b', r'\pi/4')],
    'q-16149': [('x-range', r'[-\frac14,\infty)'), ('y-range', r'[-2,\infty)')],
    'q-36695': [('left-limit', '1'), ('right-limit', '1')],
    'q-104282': [('x', '2')], 'q-48219': [('x', '1')], 'q-104247': [('x', '3')],
    'q-3043': [('a', '8')], 'q-88472': [('product-of-solutions', r'-\frac34')],
    'q-27119': [('fixed-cost-dollars', '20'), ('hourly-cost-dollars', '5')],
    'q-121583': [('opposite', '1'), ('adjacent', '2'), ('hypotenuse', r'\sqrt5')],
}
ROOTS = {
    'q-178255': ['-5', '1', '5'], 'q-39790': [r'-\frac32', '1'],
    'q-4698': [r'-\frac12', '0'], 'q-114339': ['-3', r'\frac34', '3'],
    'q-114105': ['0', r'\frac43', '2'], 'q-71778': ['0', '2', '5'],
    'q-3984': ['-2', '0', '9'], 'q-13468': ['0', '1', '7'],
    'q-114111': [r'-\frac12', '0', r'\frac52'],
    'q-71782': [r'-\frac13', '0', r'\frac72'], 'q-39802': ['-7', '1'],
    'q-24395': ['2', '3'], 'q-39832': ['-4', '5'], 'q-39833': ['2', '6'],
    'q-70913': ['-2', '5'], 'q-131072': [r'-\frac23', '2'], 'q-19154': ['-4', '4'],
    'q-118955': ['-6', '6'], 'q-156159': [r'-\sqrt2', r'\sqrt2'],
    'q-114145': [r'-\sqrt2', r'\sqrt2', '3'], 'q-14077': ['-7', r'-\sqrt3', r'\sqrt3'],
    'q-14108': [r'-\sqrt{\frac37}', r'\frac12', r'\sqrt{\frac37}'],
    'q-114210': ['-5', '-3', '5'], 'q-114205': [r'-\frac72', r'-\frac13', r'\frac13'],
    'q-14102': [r'-\sqrt{\frac12}', r'\sqrt{\frac12}', r'\frac43'],
    'q-10318': ['-60', '60'], 'q-13454': [r'-2-\sqrt6', r'-2+\sqrt6'],
}


class ReviewNeeded(ValueError):
    pass


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def split_top(value, separator):
    """Split outside braces and LaTeX environments (including matrix rows)."""
    result, start, depth, environments, i = [], 0, 0, [], 0
    while i < len(value):
        match = re.match(r'\\(begin|end)\{([^}]+)\}', value[i:])
        if match:
            direction, name = match.groups()
            if direction == 'begin':
                environments.append(name)
            elif not environments or environments.pop() != name:
                raise ReviewNeeded('Unbalanced LaTeX environment')
            i += len(match[0])
            continue
        if value.startswith(separator, i) and depth == 0 and not environments:
            result.append(value[start:i])
            i += len(separator)
            start = i
            continue
        if value[i] == '\\':
            i += 2
            continue
        if value[i] == '{':
            depth += 1
        elif value[i] == '}':
            depth -= 1
            if depth < 0:
                raise ReviewNeeded('Unbalanced LaTeX braces')
        i += 1
    if depth or environments:
        raise ReviewNeeded('Unbalanced LaTeX braces or environment')
    result.append(value[start:])
    return result


def clean_math(value):
    """Select the terminal expression, without splitting inside a matrix."""
    value = value.strip().strip('$').strip()
    outer = re.fullmatch(r'\\begin\{aligned\}([\s\S]*)\\end\{aligned\}', value)
    if outer:
        value = outer[1]
    rows = [x.strip() for x in split_top(value, r'\\') if x.strip().strip('&')]
    value = rows[-1].strip().rstrip('&').strip()
    if value.startswith('&'):
        value = value[1:].strip()
    if value.startswith('='):
        value = value[1:].strip()
    equations = split_top(value, '=')
    if len(equations) > 2:
        value = equations[-1].strip()
    value = value.rstrip('&').strip()
    # Sentence punctuation follows a final formula; preserve decimal literals.
    if value.endswith('.') and not re.fullmatch(r'[+-]?\d+\.', value):
        value = value[:-1].rstrip()
    split_top(value, '\x00')
    if not value or any(x in value for x in [r'\cancel', r'\begin{aligned}', '$']):
        raise ReviewNeeded('Answer still contains working or malformed math')
    if len(value) > 512:
        raise ReviewNeeded('Unusually long answer needs interpretation')
    return value


def field(key, kind, value, interaction='blank', choices=None, evidence=None):
    return {'key': key, 'type': interaction,
            'choices': choices or [{'type': kind, 'value': value}],
            'correct_value': value, 'evidence': evidence}


def categorical(question, answer):
    """Local choices, never represented as original MA options."""
    value = answer['value'].strip().rstrip('.')
    if re.fullmatch(r'Quadrant (?:I|II|III|IV)', value):
        options = ['Quadrant I', 'Quadrant II', 'Quadrant III', 'Quadrant IV']
    elif value in ('Odd', 'Even', 'Neither'):
        options = ['Even', 'Odd', 'Neither']
    elif value in ('Yes', 'No'):
        options = ['Yes', 'No']
    elif value == 'Exponential':
        options = ['Linear', 'Quadratic', 'Cubic', 'Exponential', 'Logarithmic']
    elif value == 'Right cylinder':
        options = ['Right cylinder', 'Oblique cylinder', 'Cone', 'Sphere', 'Pyramid', 'Prism']
    elif value in ('Converges', 'Diverges') and (value == 'Diverges' or not re.search(
            r'if it converges.*(?:sum|limit)', question['problem'], re.I | re.S)):
        options = ['Converges', 'Diverges']
    elif re.fullmatch(r'(?:I|II|III)(?:,? (?:and )?(?:II|III))*(?: only)?', value) or value in (
            'All the statements are true', 'None of those listed'):
        # Statement subsets require explicit, complete labels in the prompt.
        labels = re.findall(r'(?m)^(I|II|III|IV|V|VI)\.', question['problem'])
        if labels not in (['I', 'II', 'III'], ['I', 'II', 'III', 'IV']):
            return None
        options = ['I only', 'II only', 'III only', 'I and II only',
                   'I and III only', 'II and III only', 'I, II, and III',
                   'None of those listed']
        if len(labels) == 4:
            options = [', '.join(x for i, x in enumerate(labels) if mask & (1 << i))
                       for mask in range(1, 16)] + ['None of those listed']
        if value == 'All the statements are true':
            value = 'I, II, and III' if len(labels) == 3 else ', '.join(labels)
        if value not in options:
            return None
    else:
        return None
    return field('selection', 'text', value, 'radio',
                 [{'type': 'text', 'value': x} for x in options],
                 'Locally authored options; correct response from saved worked solution')


def derived_fields(question, answer):
    mid = question['math_academy_id']
    if mid == 'q-77896':
        return [field('degree', 'text', 'Quartic', 'select', [{'type':'text', 'value':x}
                       for x in ['Linear', 'Quadratic', 'Cubic', 'Quartic', 'Quintic']]),
                field('terms', 'text', 'Binomial', 'select', [{'type':'text', 'value':x}
                       for x in ['Monomial', 'Binomial', 'Trinomial', 'Four or more terms']])], 'local-category-choices'
    complements = {
        'q-11670': ('The patient is not a smoker', 'The patient is a smoker', '0.6'),
        'q-119653': ('Mary does not wear an orange shirt', 'Mary wears an orange shirt', r'\frac34'),
        'q-119652': ('The participant has brown hair', 'The participant has black hair', r'\frac23'),
    }
    if mid in complements:
        correct, alternative, probability = complements[mid]
        return [field('complement-event', 'text', correct, 'select',
                      [{'type':'text', 'value':x} for x in [correct, alternative]], evidence=answer['evidence']),
                field('complement-probability', 'math', probability, evidence=answer['evidence'])], 'reviewed-components'
    if mid == 'q-138998':
        return [field('L', 'math', '1', evidence=answer['evidence']),
                field('root-test-conclusion', 'text', 'Inconclusive', 'select',
                      [{'type':'text', 'value':x} for x in ['Converges', 'Diverges', 'Inconclusive']],
                      evidence=answer['evidence'])], 'reviewed-components'
    if mid == 'q-99965':
        return [field('right-limit-at-0', 'text', 'Does not exist', evidence=answer['evidence']),
                field('right-limit-at-1', 'math', '1', evidence=answer['evidence'])], 'reviewed-components'
    if mid in COMPONENTS:
        return [field(k, 'math', v, evidence='Explicit decomposition of saved conclusion: ' + answer['value'])
                for k, v in COMPONENTS[mid]], 'reviewed-components'
    if mid in ROOTS:
        return [field(f'root-{i + 1}', 'math', v,
                      evidence='Saved roots, ordered from least to greatest: ' + answer['value'])
                for i, v in enumerate(ROOTS[mid])], 'ordered-real-roots'
    if answer['type'] == 'image':
        raise ReviewNeeded('image-answer')
    if answer['type'] == 'math':
        value = clean_math(answer['value'])
        # Matrices are an explicit ordered collection of component responses.
        matrix = re.fullmatch(r'\\begin\{bmatrix\}([\s\S]*)\\end\{bmatrix\}', value)
        if matrix:
            rows = [split_top(row, '&') for row in split_top(matrix[1], r'\\')]
            if len({len(row) for row in rows}) != 1 or len(rows) > 4 or len(rows[0]) > 4:
                raise ReviewNeeded('Unusual matrix shape')
            return [field(f'r{i + 1}c{j + 1}', 'math', clean_math(cell),
                          evidence=answer.get('evidence'))
                    for i, row in enumerate(rows) for j, cell in enumerate(row)], 'matrix-components'
        pure_imaginary = re.fullmatch(r'\\pm\s*(.+\\text\{i\})', value)
        if pure_imaginary:
            return [field('negative-imaginary', 'math', '-' + pure_imaginary[1], evidence=answer['evidence']),
                    field('positive-imaginary', 'math', pure_imaginary[1], evidence=answer['evidence'])], 'reviewed-components'
        if re.search(r'\\begin\{|\\pm|\\mp', value):
            raise ReviewNeeded('Set-valued or structured answer needs response design')
        # Coordinate pairs have an explicit positional meaning.
        pair = re.fullmatch(r'\(([^()]+)\)', value)
        if pair:
            components = split_top(pair[1], ',')
            if 2 <= len(components) <= 3:
                return [field(f'coordinate-{i + 1}', 'math', clean_math(x),
                              evidence=answer.get('evidence'))
                        for i, x in enumerate(components)], 'coordinate-components'
        assignment = re.fullmatch(r'([A-Za-z])\s*=\s*(.+)', value)
        if assignment:
            return [field(assignment[1], 'math', assignment[2], evidence=answer.get('evidence'))], 'equation-component'
        return [field('answer', 'math', value, evidence=answer.get('evidence'))], 'entered-math'
    choice = categorical(question, answer)
    if choice:
        origin = 'local-category-choices' if mid in ('q-10764', 'q-107246') else 'local-exhaustive-choices'
        return [choice], origin
    value = answer['value'].strip().rstrip('.')
    # Separate distinct named scalar outputs; repeated variables are root sets,
    # whose ordering is not implied by the source and therefore need review.
    named = re.fullmatch(r'\$([^$]+)\$\s*(?:,|and|;)\s*\$([^$]+)\$', value)
    if named:
        parts = [re.fullmatch(r'([A-Za-z])\s*=\s*(.+)', x) for x in named.groups()]
        if all(parts) and parts[0][1] != parts[1][1]:
            return [field(x[1], 'math', clean_math(x[2]), evidence=answer.get('evidence'))
                    for x in parts], 'named-components'
    # These concise terms are reasonable literal responses, with a visible
    # format instruction. Narrative interpretations and incomplete multipart
    # conclusions are deferred rather than graded by exact prose matching.
    literals = {'Undefined', 'No maximum value', 'No minimum value',
                'No roots have the requested multiplicity', 'No real solutions',
                'No real roots', 'No horizontal asymptotes', 'No vertical asymptotes',
                'All real numbers', 'Exponential', 'Right cylinder', 'Quartic binomial',
                'Dollars per point', 'Visitors per hour'}
    if value in literals:
        return [field('answer', 'text', value, evidence=answer.get('evidence'))], 'entered-text'
    raise ReviewNeeded('Narrative, unordered multi-answer, or conditional response needs interpretation')


class Assets:
    def __init__(self, output, saved):
        self.output, self.saved, self.copied = output, saved, {}
        (output / 'assets').mkdir(exist_ok=True)

    def resolve(self, reference):
        if reference.startswith('data:'):
            raise ReviewNeeded('Embedded image needs review')
        source = Path(self.saved.get(reference, reference))
        if not source.is_file():
            raise ReviewNeeded('Unavailable image asset: ' + reference)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        name = digest + source.suffix.lower()
        target = self.output / 'assets' / name
        if not target.exists():
            shutil.copy2(source, target)
        result = str(target.resolve())
        self.copied[reference] = {'path': result, 'sha256': digest}
        return result

    def text(self, value):
        return re.sub(r'(!\[[^\]]*\]\()([^\n)]+)(\))',
                      lambda m: m[1] + self.resolve(m[2]) + m[3], value)


def adjust_prompt(problem):
    # Saved history omits MC options. Explicitly adapt references to absent
    # options when constructing a blank, while retaining the source verbatim.
    replacements = [
        (r'Which of the following is equivalent to', 'Give an expression equivalent to'),
        (r'Which of the following is the', 'What is the'),
        (r'Which of the following', 'What'),
    ]
    for pattern, replacement in replacements:
        problem = re.sub(pattern, replacement, problem, flags=re.I)
    return problem


def add_locations(question, origin):
    fields = question['answer_fields']
    found = re.findall(r'\{\{([^{}]+)\}\}', question['problem'])
    if set(found) - {f['key'] for f in fields}:
        raise ReviewNeeded('Source has unmatched response locations')
    if found:
        if set(found) != {f['key'] for f in fields}:
            raise ReviewNeeded('Source omits some response locations')
        return
    if len(fields) == 1 and fields[0]['type'] == 'radio':
        return
    if origin != 'saved-fields':
        question['problem'] = adjust_prompt(question['problem'])
    labels = []
    for f in fields:
        key = f['key']
        if origin == 'matrix-components':
            match = re.fullmatch(r'r(\d)c(\d)', key)
            label = f'Row {match[1]}, column {match[2]}'
        elif origin == 'coordinate-components':
            label = 'Coordinate ' + key.split('-')[-1]
        elif origin in ('named-components', 'reviewed-components'):
            label = ('$' + key + '$') if len(key) == 1 else key.replace('-', ' ').capitalize()
        elif origin == 'equation-component':
            label = '$' + key + ' =$'
        elif origin == 'ordered-real-roots':
            label = 'Value ' + key.split('-')[-1] + ' (least to greatest)'
        else:
            label = 'Answer' if len(fields) == 1 else key
        labels.append(f'{label}: {{{{{key}}}}}')
    question['problem'] += '\n\n' + '\n\n'.join(labels)
    if question['math_academy_id'] == 'q-99965':
        question['problem'] += '\n\nIf a requested limit does not exist, enter "Does not exist".'
    if origin == 'entered-text':
        value = fields[0]['correct_value']
        if value == 'Undefined':
            question['problem'] += '\n\nIf the value is undefined, enter "Undefined".'
        elif value == 'All real numbers':
            question['problem'] += '\n\nUse an interval in words, such as "All real numbers".'
        elif value in ('No maximum value', 'No minimum value', 'No real solutions', 'No real roots',
                       'No horizontal asymptotes', 'No vertical asymptotes',
                       'No roots have the requested multiplicity'):
            question['problem'] += '\n\nIf none exist, enter a phrase such as \"' + value + '\".'
        elif value in ('Dollars per point', 'Visitors per hour'):
            question['problem'] += '\n\nWrite the units in the form \"[output units] per [input unit]\".'
        else:
            raise ReviewNeeded('Categorical response needs authored alternatives')


def validate_ready(question):
    validate_question(question)
    fields = question['answer_fields']
    locations = re.findall(r'\{\{([^{}]+)\}\}', question['problem'])
    if fields[0]['type'] != 'radio' or len(fields) > 1:
        if Counter(locations) != Counter(f['key'] for f in fields):
            raise ReviewNeeded('Response locations do not match fields exactly once')
    for f in fields:
        if not f['correct_value'].strip():
            raise ReviewNeeded('Empty canonical answer')
        if f['type'] != 'blank' and len(f['choices']) < 2:
            raise ReviewNeeded('Choice interaction has fewer than two options')
        for choice in f['choices']:
            if choice['type'] == 'image':
                raise ReviewNeeded('image-answer')
            if choice['type'] == 'math':
                split_top(choice['value'], '\x00')


def draft_transaction(questions):
    transaction = []
    groups = defaultdict(list)
    for q in questions:
        groups[q['topic_id']].append(q)
    for tid, group in sorted(groups.items()):
        points = {q['knowledge_point_id']: q['knowledge_point'] for q in group}
        topic = {':topic/math-academy-id': tid, ':topic/knowledge-points': [
            {':knowledge-point/id': uuid.UUID(k), ':knowledge-point/title': v} for k, v in points.items()]}
        changes, _ = build_transaction({'topic_id': tid, 'questions': group}, topic, {})
        transaction.extend(changes)
    text = dumps(transaction) + '\n'
    assert loads(text) == transaction
    return transaction, text


def runtime_check(output):
    """Use the actual native grader, without constructing learner evidence."""
    subprocess.run(['cargo', 'build', '--release', '--lib', '--offline'], cwd=ROOT,
                   check=True, capture_output=True)
    deps = ROOT / 'target/release/deps'
    binary = ROOT / '.local/edb/validate-historical-question-readiness'
    binary.parent.mkdir(parents=True, exist_ok=True)
    command = ['rustc', '--edition=2024', '-O', str(ROOT / 'scripts/validate_historical_question_readiness.rs')]
    for name in ['course_academy_engine', 'serde_json']:
        library = max(deps.glob(f'lib{name}-*.rlib'), key=lambda p: p.stat().st_mtime_ns)
        command += ['--extern', f'{name}={library}']
    command += ['-L', f'dependency={deps}', '-o', str(binary)]
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
    subprocess.run([str(binary), str(output / 'questions.json'), str(output / 'runtime-readiness.json')],
                   check=True, capture_output=True)
    report = json.loads((output / 'runtime-readiness.json').read_text())
    assert all(q['reason'] in (None, 'this blank needs a symbolic grader before it can be served')
               for q in report['questions']), 'Unexpected native grader failure'
    report['grader_source_sha256'] = hashlib.sha256((ROOT / 'engine/rust/learning.rs').read_bytes()).hexdigest()
    save(output / 'runtime-readiness.json', report)
    return report


def prepare(source, output):
    output.mkdir(parents=True, exist_ok=True)
    original = json.loads((source / 'prepared.json').read_text())['questions']
    answers = json.loads((source / 'derived-answers.json').read_text())
    reviewed = json.loads((source / 'answer-review.json').read_text())
    answers.update(reviewed)
    assets = Assets(output, json.loads((source / 'asset-map.json').read_text())['assets'])
    image_ids = {'q-88515', 'q-88500', 'q-88400', 'q-48086', 'q-51568',
                 'q-71805', 'q-123789', 'q-123788'}
    ready, deferred, audit = [], [], []
    for source_question in original:
        question = copy.deepcopy(source_question)
        mid = question['math_academy_id']
        try:
            if mid in image_ids:
                raise ReviewNeeded('image-reconstruction')
            answer = answers.get(mid)
            if answer and 'unresolved' in answer:
                raise ReviewNeeded('image-reconstruction: ' + answer['unresolved'])
            if answer and answer.get('type') == 'image':
                raise ReviewNeeded('image-answer')
            origin = 'saved-fields'
            fields = question.get('answer_fields', [])
            if fields and any(not f.get('correct_value') for f in fields):
                if not answer or 'fields' not in answer or len(answer['fields']) != len(fields):
                    raise ReviewNeeded('Missing or ambiguous field replacement')
                for f, replacement in zip(fields, answer['fields']):
                    if not f.get('correct_value'):
                        f['correct_value'] = replacement['value']
                        f['choices'] = [{'type': replacement['type'], 'value': replacement['value']}]
                        f['evidence'] = answer.get('evidence')
                origin = 'filled-saved-fields'
            elif not fields:
                if not answer or 'type' not in answer:
                    raise ReviewNeeded('Missing answer derivation')
                question['answer_fields'], origin = derived_fields(question, answer)
            # Captured free-response correct values are authoritative. Clean
            # terminal working only for reconstructed keys, not saved options.
            question['problem'] = assets.text(question['problem'])
            question['worked_solution'] = assets.text(question['worked_solution'])
            add_locations(question, origin)
            validate_ready(question)
            question['topic_id'] = int(question['topic_id'])
            question['preparation'] = {
                'answer_origin': origin, 'answer_evidence': answer,
                'has_explicit_answer_review': mid in reviewed,
                'source_problem': source_question['problem'],
                'difficulty_provenance': 'MA rating of the original question, before local response adaptation',
            }
            # Export a deliberately small content record. Source HTML and
            # historical timing/outcomes remain outside the import payload.
            keep = ['math_academy_id', 'topic_id', 'knowledge_point_id', 'knowledge_point',
                    'problem', 'worked_solution', 'difficulty', 'answer_fields', 'provenance',
                    'preparation', 'requires_calculator']
            ready.append({k: question[k] for k in keep if k in question})
            audit.append({'math_academy_id': mid, 'origin': origin,
                          'source_fields': source_question.get('answer_fields', []),
                          'prepared_fields': question['answer_fields'],
                          'problem_adapted': question['problem'] != source_question['problem']})
        except ReviewNeeded as error:
            deferred.append({'math_academy_id': mid, 'knowledge_point': question['knowledge_point'],
                             'reason': str(error), 'source_question': source_question,
                             'answer_evidence': answers.get(mid)})
    assert len(ready) + len(deferred) == len(original)
    assert len({q['math_academy_id'] for q in ready + deferred}) == len(original)
    # This is a content-only draft, built through the existing importer. A
    # fresh DB match and basis-guarded preview are required before transacting.
    transaction, text = draft_transaction(ready)
    (output / 'transaction-draft.edn').write_text(text)
    save(output / 'questions.json', {'questions': ready})
    runtime = runtime_check(output)
    supported_ids = {q['math_academy_id'] for q in runtime['questions'] if q['accepted_by_current_grader']}
    supported = [q for q in ready if q['math_academy_id'] in supported_ids]
    save(output / 'engine-supported-questions.json', {'questions': supported})
    _, supported_text = draft_transaction(supported)
    (output / 'transaction-engine-supported-draft.edn').write_text(supported_text)
    save(output / 'deferred.json', {'questions': deferred})
    save(output / 'answer-audit.json', audit)
    save(output / 'asset-map.json', assets.copied)
    report = {'original_count': len(original), 'prepared_count': len(ready),
              'deferred_count': len(deferred), 'database_writes': 0,
              'source_sha256': {f: hashlib.sha256((source / f).read_bytes()).hexdigest()
                                for f in ['prepared.json', 'derived-answers.json', 'answer-review.json', 'asset-map.json']},
              'answer_origins': dict(Counter(q['preparation']['answer_origin'] for q in ready)),
              'deferred_reasons': dict(Counter(q['reason'] for q in deferred)),
              'transaction_entities': len(transaction),
              'transaction_sha256': hashlib.sha256(text.encode()).hexdigest(),
              'local_asset_count': len({x['path'] for x in assets.copied.values()}),
              'current_engine_ready_count': runtime['current_engine_ready_count'],
              'needs_symbolic_grader_count': runtime['needs_symbolic_grader_count'],
              'validation': 'All prepared records passed importer validation and EDN round-trip; native preview pending',
              'runtime_note': 'Symbolic math blanks require a symbolic grader; current engine only accepts rational math blanks. No engine changes in this preparation.'}
    save(output / 'report.json', report)
    (output / 'README.md').write_text(
        '# Prepared historical questions\n\n'
        f'{len(ready)} of {len(original)} questions are prepared; {len(deferred)} are deferred. '
        'No database transaction has been committed.\n\n'
        '- `questions.json`: complete content records and answer fields.\n'
        '- `deferred.json`: excluded records, evidence, and exact reasons.\n'
        '- `answer-audit.json`: original and prepared answer fields.\n'
        '- `transaction-draft.edn`: additive content-only draft using stable importer identities.\n'
        '- `runtime-readiness.json`: exact native grader results for every prepared record.\n'
        '- `engine-supported-questions.json` and `transaction-engine-supported-draft.edn`: subset accepted by the current grader.\n'
        '- `asset-map.json` and `assets/`: local copies of referenced images, with hashes.\n'
        '- `report.json`: counts, checks, and source fingerprints.\n\n'
        'Original saved files are unchanged. Existing response fields and dropdown options are '
        'preserved. Missing-option numeric or symbolic questions are adapted to entered answers '
        'with explicit locations; their original prompts and derivations remain in preparation '
        'metadata. Quadrants, parity, yes/no, and three-statement questions use locally authored '
        'exhaustive choices, explicitly distinguished from unavailable original MA options. '
        'Regression-model, solid-name, and polynomial-classification questions use locally authored category choices. '
        'Explicit named outputs, matrix entries, coordinates, and ordered roots have separate fields. '
        'Observed difficulty remains the original MA rating, not a new rating of the adapted version.\n\n'
        'This is content preparation, not a symbolic-grading implementation. The current engine '
        'rejects symbolic math blanks at serving time. A separate runtime readiness report must '
        'identify those records before they enter a live practice pool. Native database matching '
        'and a fresh basis-guarded preview are required before any import; the draft assumes these '
        'questions remain absent and their saved KP associations remain valid.\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output', type=Path, default=SOURCE / 'import-ready')
    args = parser.parse_args()
    prepare(args.source, args.output)
