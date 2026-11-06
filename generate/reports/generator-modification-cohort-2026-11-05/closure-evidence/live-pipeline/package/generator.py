"""Independent 2×2 entry reading. No database, service or filesystem writes."""
import argparse
import json
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, matrix_operands, matrix_tex, normalize_prose

BANDS = {'easy': (1, 9), 'moderate': (10, 99), 'hard': (100, 999)}
NAMESPACE = uuid.UUID('b29dafc4-3fef-4dcf-8c37-cff5a59f1d18')


def values(band):
    low, high = BANDS[band]
    return list(range(-high, -low + 1)) + [0] + list(range(low, high + 1))


def capacity(band):
    return 4 * len(values(band)) ** 4


@checked_math_content
def generate(matrix, row, column, difficulty='easy'):
    if difficulty not in BANDS or type(row) is not int or type(column) is not int or row not in (0, 1) or column not in (0, 1):
        raise ValueError('Invalid difficulty or position')
    if len(matrix) != 2 or any(len(r) != 2 or any(type(v) is not int for v in r) for r in matrix):
        raise ValueError('Expected a two-by-two integer matrix')
    # Preserve source parentheses while using shared canonical matrix construction.
    tex = matrix_tex(matrix).replace('bmatrix', 'pmatrix')
    problem = normalize_prose('For the matrix\n\n' + matrix_operands(['A=' + tex])
                              + f'\n\nfind $a_{{{row+1}{column+1}}}$.\n\n{{{{answer}}}}')
    result = matrix[row][column]
    conclusion = f'a_{{{row+1}{column+1}}}={result}'
    solution = normalize_prose(f'The first index is {row+1}, so use row {row+1}. '
                              f'The second index is {column+1}, so use column {column+1} of that row. ${conclusion}$.')
    identity = json.dumps([problem, solution, difficulty], separators=(',', ':'))
    qid = uuid.uuid5(NAMESPACE, identity)
    field = str(uuid.uuid5(qid, 'field:answer'))
    answer = str(uuid.uuid5(uuid.UUID(field), 'answer:' + str(result)))
    return {'knowledge_point_id': 900001,
            'question': {':question/id': str(qid), ':question/problem': problem,
                         ':question/worked-solution': solution,
                         ':question/difficulty': ':question.difficulty/' + difficulty,
                         ':question/answer-fields': [{':answer-field/id': field, ':answer-field/key': 'answer',
                           ':answer-field/type': ':answer-field.type/blank', ':answer-field/correct': [':answer/id', answer],
                           ':answer-field/choices': [{':answer/id': answer, ':answer/type': ':answer.type/math', ':answer/value': str(result)}]}]},
            'generation': {'version': 1, 'template': 'single-entry',
                           'parameters': {'matrix': matrix, 'row': row, 'column': column},
                           'domain': '2x2 integer matrix; one-based displayed indices',
                           'source_refs': ['source.md: Lesson', 'fixture-q11', 'fixture-q12', 'fixture-q21', 'fixture-q22'],
                           'difficulty_status': 'authored ranges; moderate/hard uncalibrated'}}


def sample(band, count, seed):
    if type(count) is not int or not 0 <= count <= capacity(band):
        raise ValueError(f'count must be between 0 and {capacity(band)}')
    rng = random.Random(seed)
    bank = values(band)
    records = []
    # Sample distinct complete learner-visible instances, no rejection or bank guards.
    # Position is an independent radix digit, never derived from entry signs/ranks.
    for code in rng.sample(range(capacity(band)), count):
        position, code = code % 4, code // 4
        entries = []
        for _ in range(4):
            code, digit = divmod(code, len(bank))
            entries.append(bank[digit])
        record = generate([entries[:2], entries[2:]], position // 2, position % 2, band)
        record['generation']['seed'] = seed
        records.append(record)
    return records


def replay(source_id):
    cases = json.loads(Path(__file__).with_name('source-cases.json').read_text())
    selected = cases if source_id == 'all' else [c for c in cases if c['id'] == source_id]
    if not selected:
        raise ValueError('Unknown source case')
    records = []
    for case in selected:
        record = generate(**case['parameters'])
        record['generation']['replay_source'] = case['id']
        records.append(record)
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=list(BANDS), default='easy')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay', help='Source ID or all; retains original easy labels')
    args = parser.parse_args()
    try:
        output = replay(args.replay) if args.replay else sample(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(output, ensure_ascii=False, indent=2))
