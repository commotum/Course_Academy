#!/usr/bin/env python3
"""Fit all retained quiz bases to assigned E/M/H counts; no learner times.

Run with /home/jake/Developer/MA/.venv/bin/python (NumPy dependency).
No holdout. No database writes. No learned coefficients are applied to engine.
"""
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BANDS = ('E', 'M', 'H')
LABELS = {'easy': 'E', 'moderate': 'M', 'hard': 'H', 'E': 'E', 'M': 'M', 'H': 'H'}


def main():
    rows = []

    def add(task_id, base, origin, questions, source):
        counts = Counter(LABELS[q['difficulty']] for q in questions)
        rows.append({'task_id': str(task_id), 'base_xp': int(base), 'origin': origin,
                     'band_counts': dict(counts), 'question_count': len(questions),
                     'source': str(source.relative_to(ROOT))})

    historical_path = ROOT / 'reference/mathacademy/progress-history-2026-10-04/observations.json'
    history = json.loads(historical_path.read_text())
    for task in history['tasks']:
        if task['activity-type'] == 'Assessment':
            add(task['task-id'], task['base_xp'], 'learner', task['questions'], historical_path)

    for path in sorted((ROOT / 'reference/mathacademy/question-capture').glob('*/state.json')):
        state = json.loads(path.read_text())
        if state.get('task_type') != 'assessment' or not state.get('activity_complete'):
            continue
        text = state.get('completion', '')
        match = (re.search(r"(?:of|all of) the task's (\d+) XP", text)
                 or re.search(r'-?\d+/(\d+) XP', text))
        assert match, path
        metadata_path = path.parent / 'activity-metadata.json'
        metadata = json.loads(metadata_path.read_text())
        assert len(metadata) == int(state['assessment_details']['Questions'])
        add(path.parent.name, match[1], 'automated', metadata, metadata_path)

    pilot = ROOT / 'reference/mathacademy/assessment-13930620'
    completion = re.sub('<[^>]*>', ' ', (pilot / 'completion.html').read_text())
    base_match = re.search(r"task's\s+(\d+)\s+XP", completion)
    assert base_match
    pilot_metadata = pilot / 'activity-questions.json'
    add('13930620', base_match[1], 'automated-pilot',
        json.loads(pilot_metadata.read_text()), pilot_metadata)

    assert len({r['task_id'] for r in rows}) == len(rows)
    x = np.array([[r['band_counts'].get(b, 0) for b in BANDS] for r in rows], float)
    y = np.array([r['base_xp'] * 60 for r in rows], float)
    assert np.linalg.matrix_rank(x) == 3

    def metrics(seconds):
        predicted = x @ np.asarray(seconds)
        difference = predicted - y
        rounded_xp = np.floor(predicted / 60 + .5)
        xp_error = rounded_xp - y / 60
        return {'band_seconds': dict(zip(BANDS, map(float, seconds))),
                'mean_absolute_minutes': float(np.mean(abs(difference)) / 60),
                'maximum_absolute_minutes': float(np.max(abs(difference)) / 60),
                'rounded_xp_mae': float(np.mean(abs(xp_error))),
                'rounded_xp_maximum_error': float(np.max(abs(xp_error))),
                'rounded_xp_exact': int(np.sum(xp_error == 0)),
                'sum_squared_seconds_error': float(difference @ difference)}

    fitted = np.linalg.lstsq(x, y, rcond=None)[0]
    assert np.all(fitted > 0) and fitted[0] <= fitted[1] <= fitted[2]
    count = x.sum(axis=1)
    flat = float((count @ y) / (count @ count))
    best = None
    # Exhaustive five-second grid, enforcing Easy <= Moderate <= Hard.
    # For the integer-XP approximation: smallest rounded MAE, most exact bases,
    # smallest unrounded MAE, then squared seconds error.
    for easy in range(30, 181, 5):
        candidates = np.array([(easy, moderate, hard)
                               for moderate in range(easy, 241, 5)
                               for hard in range(moderate, 301, 5)])
        predicted = x @ candidates.T
        error = predicted - y[:, None]
        rounded_error = np.floor(predicted / 60 + .5) - y[:, None] / 60
        rounded_mae = np.mean(abs(rounded_error), axis=0)
        exact = np.sum(rounded_error == 0, axis=0)
        raw_mae = np.mean(abs(error), axis=0) / 60
        squared = np.sum(error ** 2, axis=0)
        index = np.lexsort((squared, raw_mae, -exact, rounded_mae))[0]
        score = (float(rounded_mae[index]), -int(exact[index]),
                 float(raw_mae[index]), float(squared[index]))
        if best is None or score < best[0]:
            best = (score, candidates[index].tolist())

    candidates = {'least_squares': metrics(fitted),
                  'equal_band_baseline': metrics([flat] * 3),
                  'simple_1_2_3_minutes': metrics([60, 120, 180]),
                  'best_monotone_five_second_grid': metrics(best[1])}
    for row, counts in zip(rows, x):
        row['predictions'] = {name: {'seconds': float(counts @ np.array(list(model['band_seconds'].values()))),
                                    'rounded_xp': int(np.floor(counts @ np.array(list(model['band_seconds'].values())) / 60 + .5))}
                              for name, model in candidates.items()}
    results = {'method': 'Fit all observed quiz bases to complete assigned question-band counts. No holdout.',
               'target': 'base XP * 60 seconds; excludes earned XP and learner/automator durations',
               'limitations': ['Quiz base/time allowance is a proxy for expected work, not measured per-question expectation.',
                               'Difficulty is relative to content; a global band cannot account for every topic.',
                               'The expired zero-answer quiz is included using its full assigned question set.'],
               'quiz_count': len(rows), 'question_count': int(x.sum()),
               'origins': dict(Counter(r['origin'] for r in rows)),
               'band_counts': dict(zip(BANDS, map(int, x.sum(axis=0)))),
               'total_base_minutes': int(y.sum() / 60), 'candidates': candidates, 'quizzes': rows}
    (HERE / 'quiz-question-time-fit.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({k: v for k, v in results.items() if k != 'quizzes'}, indent=2))


if __name__ == '__main__':
    main()
