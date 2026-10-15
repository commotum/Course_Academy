#!/usr/bin/env python3
"""Zero-matrix recognition, steps 3–7 draft. No registration/database operations.

All levels use explicit numerical matrices and the same entrywise recognition
method. Moderate/hard are authored uncalibrated placements, not recovered levels.
Templates store only extracted masks/prose, not completed answer payloads.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import random
import re
import uuid
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import matrix_tex, normalize_prose, checked_math_content

HERE = Path(__file__).with_suffix('')
KP_ID = 17592186087695
KP_UUID = 'ddb59990-7419-585f-aa1b-901d59c8cfc1'
TITLE = 'Identifying a Zero Matrix'
VERSION = '2.0.0-draft'
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
TEMPLATES = json.loads((HERE / 'templates.json').read_text())
DEFAULT_TEMPLATES = tuple(k for k in TEMPLATES if k != 'canonical')
ENTRY_VALUES = ('0', '1', '0.1', '3', '10')


def arrays(text):
    """Read the actual displayed named arrays, not generation metadata."""
    out = {}
    for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}', text):
        out[m[1]] = [[v.strip() for v in row.strip().split('&')] for row in m[2].split('\\\\')]
    if len(out) != 3:
        raise ValueError('Three complete distinct named matrices required')
    return out


def fingerprint_text(text):
    # Labels, matrix order and the sizes of NONZERO entries are incidental to
    # recognizing zero matrices. Shape/support remain the substantive task.
    objects = []
    for rows in arrays(text).values():
        objects.append([len(rows), len(rows[0]), [[int(Fraction(v) != 0) for v in row] for row in rows]])
    return hashlib.sha256(json.dumps(sorted(objects), separators=(',', ':')).encode()).hexdigest()


def uid(scope, value):
    return str(uuid.uuid5(uuid.UUID(scope), value))


def sample_parameters(t, rng):
    for _ in range(2000):
        p = {'labels': rng.sample(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 3), 'matrices': [], 'witnesses': []}
        for count in t['nonzero_counts']:
            r, c = rng.randint(1, 4), rng.randint(1, 6)
            if r*c < count:
                break
            rows = [['0'] * c for _ in range(r)]
            cells = rng.sample(range(r*c), count)
            for cell in cells:
                rows[cell // c][cell % c] = rng.choice(ENTRY_VALUES[1:])
            p['matrices'].append(rows)
            p['witnesses'].append([cells[0] // c + 1, cells[0] % c + 1] if cells else None)
        if len(p['matrices']) == 3 and sum(len(z)*len(z[0]) for z in p['matrices']) <= 46:
            return p
    raise ValueError('No complete eligible instance')


def validate_parameters(p, t):
    if not isinstance(p, dict) or set(p) != {'labels', 'matrices', 'witnesses'}:
        raise ValueError('Parameters require exactly labels, matrices, witnesses')
    labels, matrices, witnesses = p['labels'], p['matrices'], p['witnesses']
    if len(labels) != 3 or len(set(labels)) != 3 or any(not isinstance(x, str) or not re.fullmatch('[A-Z]', x) for x in labels):
        raise ValueError('Three distinct uppercase labels required')
    if len(matrices) != 3 or len(witnesses) != 3:
        raise ValueError('Three matrix/witness slots required')
    for i, rows in enumerate(matrices):
        if not rows or not 1 <= len(rows) <= 4 or not 1 <= len(rows[0]) <= 6 or any(len(z) != len(rows[0]) for z in rows):
            raise ValueError('Matrix outside 1–4 by 1–6 rectangular domain')
        if any(not isinstance(v, str) or v not in ENTRY_VALUES for row in rows for v in row):
            raise ValueError('Entry outside explicit observed number-form domain')
        nz = [(r+1, c+1) for r, row in enumerate(rows) for c, v in enumerate(row) if Fraction(v) != 0]
        if len(nz) != t['nonzero_counts'][i]:
            raise ValueError('Source-shaped zero/nonzero role and count must be retained')
        w = witnesses[i]
        if nz and (not isinstance(w, list) or len(w) != 2 or any(type(x) is not int for x in w) or tuple(w) not in nz):
            raise ValueError('Witness must identify an actually nonzero cell')
        if not nz and w is not None:
            raise ValueError('Zero matrices have no nonzero witness')
    if sum(len(z)*len(z[0]) for z in matrices) > 46:
        raise ValueError('Observed recognition workload ceiling is 46 entries')


def conclusion(labels, zero):
    names = ['$'+x+'$' for x, z in zip(labels, zero) if z]
    if len(names) == 3:
        return 'Therefore, '+names[0]+', '+names[1]+', and '+names[2]+' are zero matrices.'
    if len(names) == 2:
        return 'Therefore, only '+' and '.join(names)+' are zero matrices.'
    return 'Therefore, only '+names[0]+' is a zero matrix.'


def build(level, seed, template, parameters, profile, field_type):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unknown difficulty')
    if type(seed) is not int:
        raise ValueError('Seed must be an integer')
    rng = random.Random(seed)
    if template is None:
        choices = [k for k in DEFAULT_TEMPLATES if field_type is None or TEMPLATES[k]['field_type'] == field_type]
        if not choices:
            raise ValueError('Unsupported answer field type')
        template = rng.choice(choices)
    if template not in TEMPLATES:
        raise ValueError('Unknown template')
    t = TEMPLATES[template]
    if profile not in (None, template, 'observed'):
        raise ValueError('Unknown complete bank profile')
    if field_type is not None and field_type != t['field_type']:
        raise ValueError('Field type does not match selected source family')
    p = sample_parameters(t, rng) if parameters is None else json.loads(json.dumps(parameters))
    validate_parameters(p, t)
    labels, matrices, ws = p['labels'], p['matrices'], p['witnesses']
    zero = [all(Fraction(v) == 0 for row in rows for v in row) for rows in matrices]
    if t['layout'] == 'legacy':
        problem = 'Which of the following are zero matrices?\n$'+', '.join(n+' = '+matrix_tex(rows) for n, rows in zip(labels, matrices))+'$'
    else:
        problem = 'Which of the following are zero matrices?\n\n$$\n'+r',\,'.join(n+'='+matrix_tex(rows) for n, rows in zip(labels, matrices))+'\n$$\n\nSelect all that apply.'
    bullets = []
    for i, name in enumerate(labels):
        sentence = t['bullet_templates'][i].replace('{LABEL}', name)
        if ws[i]:
            row, col = ws[i]
            sentence = sentence.replace('{lower}', name.lower()).replace('{row}', str(row)).replace('{col}', str(col)).replace('{value}', matrices[i][row-1][col-1])
        bullets.append(sentence)
    worked = '\n\n'.join(bullets)+'\n\n'+conclusion(labels, zero)
    problem, worked = normalize_prose(problem), normalize_prose(worked)
    banks = []
    if t['field_type'] == 'checkbox':
        for name, z in zip(labels, zero):
            banks.append((name, ['false', 'true'], str(z).lower()))
    else:
        values = []
        for mask in t['subset_masks']:
            names = ['$'+labels[i]+'$' for i in mask]
            if len(names) == 3:
                text = names[0]+', '+names[1]+', and '+names[2]
            else:
                text = ' and '.join(names)+' only'
            values.append(normalize_prose(text))
        target = [i for i, z in enumerate(zero) if z]
        if t['subset_masks'].count(target) != 1:
            raise ValueError('Complete bank must contain exactly one correct subset')
        banks.append(('selection', values, values[t['subset_masks'].index(target)]))
    identity_banks = sorted((key, t['field_type'], sorted(values), correct) for key, values, correct in banks)
    qid = uid(KP_UUID, json.dumps([VERSION, level, problem, worked, identity_banks], sort_keys=True))
    fields = []
    for key, values, correct in banks:
        fid = uid(qid, 'field:'+key)
        answers = [{':answer/id': uid(fid, v), ':answer/type': ':answer.type/text', ':answer/value': v} for v in values]
        correct_id = uid(fid, correct)
        rng.shuffle(answers)
        fields.append({':answer-field/id': fid, ':answer-field/key': key, ':answer-field/type': ':answer-field.type/'+t['field_type'], ':answer-field/choices': answers, ':answer-field/correct': [':answer/id', correct_id]})
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE}, 'question': {':question/id': qid, ':question/problem': problem, ':question/worked-solution': worked, ':question/difficulty': ':question.difficulty/'+level, ':question/answer-fields': fields}, 'generation': {'version': VERSION, 'template': template, 'bank_profile': template, 'seed': seed, 'parameters': p, 'parameter_fingerprint': fingerprint_text(problem), 'source_basis': 2275, 'source_lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1', 'difficulty_status': 'source-observed easy or authored unrated placement' if level == 'easy' else 'same-method authored/uncalibrated', 'python_version': sys.version.split()[0], 'plots': 'none'}}


@checked_math_content
def generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None):
    return build(level, seed, template, parameters, profile, field_type)


def generate_easy(seed=0, **kwargs):
    return generate('easy', seed=seed, **kwargs)


def generate_moderate(seed=0, **kwargs):
    return generate('moderate', seed=seed, **kwargs)


def generate_hard(seed=0, **kwargs):
    return generate('hard', seed=seed, **kwargs)


def batch(level, count, seed=0, template=None, profile=None):
    if type(count) is not int or not 1 <= count <= 1000:
        raise ValueError('Count must be 1–1000 per level')
    levels = SUPPORTED_LEVELS if level == 'all' else (level,)
    if any(z not in SUPPORTED_LEVELS for z in levels):
        raise ValueError('Unknown difficulty')
    source = json.loads((HERE/'source.json').read_text())['record']
    used = {fingerprint_text(q[':question/problem']) for q in source[':knowledge-point/questions']}
    canonical = json.loads((HERE/'canonical.json').read_text())['restored_parameters']
    canonical_prompt = ','.join(n+'='+matrix_tex(rows) for n,rows in zip(canonical['labels'], canonical['matrices']))
    used.add(fingerprint_text(canonical_prompt))
    records = []
    for difficulty in levels:
        count_here = 0
        for n in range(20000):
            r = generate(difficulty, seed+n, template=template, profile=profile)
            fp = r['generation']['parameter_fingerprint']
            if fp in used:
                continue
            records.append(r); used.add(fp); count_here += 1
            if count_here == count:
                break
        else:
            raise ValueError('Insufficient distinct mathematical tasks')
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=(*SUPPORTED_LEVELS, 'all'), default='easy')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('markdown', 'json'), default='json')
    parser.add_argument('--template')
    parser.add_argument('--profile')
    a = parser.parse_args()
    records = batch(a.difficulty, a.count, a.seed, a.template, a.profile)
    print(json.dumps(records, indent=2) if a.format == 'json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
