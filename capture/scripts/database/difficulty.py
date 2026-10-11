"""The agreed first-two-question workload calibration, independent of grading."""
from collections import defaultdict
import math
import re

VERSION = 'lesson-content-expected-distribution-v1'
MATH = re.compile(r'\$\$(.*?)\$\$|\$([^$]*)\$', re.S)

def clean(text):
    return re.sub(r'\{\{[^}]*\}\}', '', re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text))

def math_tokens(text):
    return sum(len(re.findall(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[+*/=^_−-]', m[1] if m[1] is not None else m[2]))
               for m in MATH.finditer(clean(text)))

def prose_words(text):
    return len(re.findall(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b", MATH.sub('', clean(text))))

def calibrate(content):
    definition = content.get('lesson_definition', {})
    sample = content.get('lesson_workload_sample') or {}
    base = content.get('base_xp') or sample.get('base_xp') or content.get('xp', {}).get('base_xp') or definition.get('base_xp')
    if not definition.get('complete') or not isinstance(base, (int, float)) or base < 7 or int(base) != base:
        raise ValueError('Calibration requires a complete lesson and observed integer base XP')
    groups, seen = defaultdict(list), set()
    questions = content.get('questions', [])
    selected = sample.get('questions_by_knowledge_point')
    if selected is not None:
        by_id = {q['math_academy_id']: q for q in questions}
        if not selected or any(len(ids) != 2 or len(set(ids)) != 2 for ids in selected.values()):
            raise ValueError('Calibration sample lacks two distinct observed questions for every KP')
        ordered_ids = [mid for ids in selected.values() for mid in ids]
        if any(mid not in by_id for mid in ordered_ids):
            raise ValueError('A selected first-two question is unsupported; do not substitute a later question')
        questions = [by_id[mid] for mid in ordered_ids]
    for q in questions:
        mid, kp = q['math_academy_id'], str(q.get('knowledge_point_id') or q.get('kp_id') or '')
        if not kp:
            raise ValueError('Calibration question lacks knowledge point')
        if mid not in seen and len(groups[kp]) < 2:
            groups[kp].append(q)
        seen.add(mid)
    examples = content.get('canonical_examples', [])
    example_kps = [str(q.get('knowledge_point_id') or q.get('kp_id') or '') for q in examples]
    if not groups or any(len(v) != 2 for v in groups.values()) or set(example_kps) != set(groups) or len(set(example_kps)) != len(examples):
        raise ValueError('Calibration requires two questions and one canonical example for every KP')
    f = dict(kp_count=len(groups), solution_math_100=0., reading_100=0., question_steps=0.,
             example_steps=0., question_math_100=0., extra_fields=0., blank_kp=0.)
    for questions in groups.values():
        for q in questions:
            problem, solution, fields = q.get('problem'), q.get('worked_solution'), q.get('answer_fields', [])
            if not problem or not solution or not fields:
                raise ValueError('Incomplete sampled question content')
            f['solution_math_100'] += math_tokens(solution) / 200
            f['question_steps'] += clean(solution).count('=') / 2
            f['question_math_100'] += math_tokens(problem) / 200
            f['extra_fields'] += max(0, len(fields) - 1) / 2
            f['blank_kp'] += any(a.get('type') == 'blank' for a in fields) / 2
    for example in examples:
        if not example.get('worked_solution'):
            raise ValueError('Incomplete canonical example')
        f['reading_100'] += (prose_words(example['problem']) + prose_words(example['worked_solution'])) / 100
        f['example_steps'] += clean(example['worked_solution']).count('=')
    f['reading_100'] += sum(prose_words(t.get('content', '')) for t in content.get('tutorials', [])) / 100
    weights = {'solution_math_100': 1.2364010385163302, 'kp_count': .46544714915426905,
               'reading_100': .07513004637186382, 'question_steps': .001586056170966394,
               'example_steps': .034422123109798704, 'question_math_100': 2.7349018409710975,
               'extra_fields': .06047150091696244, 'blank_kp': .5742034148595132}
    score = sum(f[k] * v for k, v in weights.items())
    multiplier = 1. if base == 7 and max(7, math.floor(score + .5)) == 7 else base / score
    return {'formula_version': VERSION, 'distribution': [.6, .3, .1], 'features': f,
            'selected_questions': {k: [q['math_academy_id'] for q in qs] for k, qs in groups.items()},
            'base_xp': int(base), 'unscaled_score': score, 'multiplier': multiplier,
            'expected_seconds': float(base * 60), 'canonical_solution_proxy_count': 0}
