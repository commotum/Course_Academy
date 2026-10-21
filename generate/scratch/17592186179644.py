#!/usr/bin/env python3
"""Bounded, source-backed flux-diagram catalog; never pads exhausted inventory.

The diagrams have no numerical scales or supplied field equations. This version
reuses the ten verified situations and their existing identities. It does not
claim new mathematical questions from resizing, seed changes or claim shuffles.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186179644
HOME = Path(__file__).with_suffix('')
SOURCE = json.loads((HOME / 'source.json').read_text())
SPECS = json.loads((HOME / 'specs.json').read_text())
KP_UUID = SOURCE['record'][':knowledge-point/id']
TITLE = SOURCE['record'][':knowledge-point/title']
VERSION = 'flux-sign-finite-1'
GENERATOR_ID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SUPPORTED_LEVELS = ('easy', 'moderate')
QUESTIONS = {q[':question/math-academy-id']: q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES = {t: q[':question/difficulty'][':db/ident'].split('/')[-1] for t, q in QUESTIONS.items()}


def fingerprint(template):
    """Assessed diagram relationship and unordered, path-specific claim set.

    Ignore traversal orientation, profile name, identities, seed and statement
    order. Distinguish radial/saddle/tangent fields and circle/ellipse geometry.
    """
    z = SPECS[template]
    data = {'diagram_relation': z['relation'], 'shape': z['shape'],
            'claims': sorted((c['path'], c['sign']) for c in z['claims'])}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def normalize(q):
    out = {k: str(q[k]) if k == ':question/id' else q[k]
           for k in (':question/id', ':question/problem', ':question/worked-solution')}
    out[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    out[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        out[':question/answer-fields'].append({
            ':answer-field/id': str(f[':answer-field/id']),
            ':answer-field/key': f[':answer-field/key'],
            ':answer-field/type': str(f[':answer-field/type'][':db/ident']),
            ':answer-field/correct': [':answer/id', str(f[':answer-field/correct'][':answer/id'])],
            ':answer-field/choices': sorted([
                {':answer/id': str(a[':answer/id']), ':answer/type': str(a[':answer/type'][':db/ident']),
                 ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']],
                key=lambda a: a[':answer/value'])})
    return out


def generate(level, seed=0, template=None, parameters=None, profile=None, field_type=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty; hard has no validated source workload. See capabilities.json.')
    if parameters not in (None, {}):
        raise ValueError('Finite source catalog has no numerical or geometric parameter slots.')
    if profile not in (None, 'three-checkbox-true-false'):
        raise ValueError('Only the complete observed checkbox bank profile is supported.')
    if field_type not in (None, 'checkbox', ':answer-field.type/checkbox'):
        raise ValueError('Three checkbox fields are required.')
    eligible = sorted(t for t, l in TEMPLATES.items() if l == level)
    template = template or random.Random(seed).choice(eligible)
    if template not in eligible:
        raise ValueError('Template does not belong to the requested difficulty.')
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
            'question': copy.deepcopy(normalize(QUESTIONS[template])),
            'generation': {'version': VERSION, 'template': template, 'seed': seed, 'parameters': {},
                           'bank_profile': 'three-checkbox-true-false',
                           'mathematical_fingerprint': fingerprint(template),
                           'source': {k: SOURCE[k] for k in ('database', 'basis', 'lineage')},
                           'source_question_id': QUESTIONS[template][':db/id'],
                           'existing_identity_reused': True, 'eligible_for_learning': True,
                           'evidence_only': False, 'novel_variant': False,
                           'dependencies': {'sympy': sp.__version__}}}


def generate_easy(seed=0, **kwargs):
    return generate('easy', seed=seed, **kwargs)


def generate_moderate(seed=0, **kwargs):
    return generate('moderate', seed=seed, **kwargs)


def batch(level, count, seed=0):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty; see capabilities.json.')
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ValueError('Count must be a nonnegative integer.')
    order = sorted(t for t, l in TEMPLATES.items() if l == level)
    random.Random(seed).shuffle(order)
    seen, out = set(), []
    for t in order:
        fp = fingerprint(t)
        if fp in seen:
            continue
        seen.add(fp)
        if len(out) < count:
            out.append(generate(level, seed, t))
    return out


def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\nWorked solution\n\n' + q[':question/worked-solution']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty', choices=['easy', 'moderate', 'hard', 'all'], default='all')
    ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--template')
    ap.add_argument('--format', choices=['json', 'markdown'], default='json')
    args = ap.parse_args()
    if args.template:
        level = TEMPLATES.get(args.template) if args.difficulty == 'all' else args.difficulty
        records = [generate(level, args.seed, args.template)]
    else:
        levels = SUPPORTED_LEVELS if args.difficulty == 'all' else (args.difficulty,)
        records = [r for level in levels for r in batch(level, args.count, args.seed)]
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))



# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate', 'generate_easy', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
