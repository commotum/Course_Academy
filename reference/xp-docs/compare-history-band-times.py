#!/usr/bin/env python3
"""Compare 60/120/180 seconds with every historical base XP; no refitting.

Use /home/jake/Developer/MA/.venv/bin/python (BeautifulSoup dependency).
No database writes, live navigation, learner-duration fitting, or held-out set.
"""
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HISTORY = ROOT / 'reference/mathacademy/progress-history-2026-10-04/observations.json'
LESSONS = Path('/home/jake/Developer/MA/DATA/Lessons')
SECONDS = {'E': 60, 'M': 120, 'H': 180}
READING_COEFFICIENT = 0.07513004637186382
EXAMPLE_COEFFICIENT = 0.034422123109798704


def prose_words(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.select('.math, mjx-container, math, svg, script, style'):
        tag.decompose()
    return len(re.findall(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b", soup.get_text(' ', strip=True)))


def main():
    history = json.loads(HISTORY.read_text())
    lesson_cache = {}

    def instruction(topic_id):
        if topic_id not in lesson_cache:
            path = LESSONS / topic_id / 'Source' / (topic_id + '.json')
            assert path.exists(), path
            lesson = json.loads(path.read_text())
            tutorial_words = example_words = example_equals = kp_count = 0
            for item in lesson['lesson']['items']:
                if item.get('item_type') != 'step':
                    continue
                if item['step_type'] == 'tutorial':
                    tutorial_words += sum(prose_words(section['normalized_html']) for section in item['sections'])
                elif item['step_type'] == 'example':
                    kp_count += 1
                    for section in item['sections']:
                        if section['section_type'] in ('example_question', 'example_explanation'):
                            example_words += prose_words(section['normalized_html'])
                        if section['section_type'] == 'example_explanation':
                            example_equals += section['readable_text'].count('=')
            minutes = READING_COEFFICIENT * (tutorial_words + example_words) / 100 + EXAMPLE_COEFFICIENT * example_equals
            lesson_cache[topic_id] = {'source': str(path), 'tutorial_prose_words': tutorial_words,
                                     'example_prose_words': example_words, 'example_equals': example_equals,
                                     'authored_kps': kp_count, 'instruction_proxy_minutes': minutes}
        return lesson_cache[topic_id]

    rows, excluded = [], []
    for task in history['tasks']:
        if task['base_xp'] is None:
            excluded.append({'task_id': task['task-id'], 'type': task['activity-type'], 'reason': 'no base XP'})
            continue
        counts = Counter(q['difficulty'] for q in task['questions'])
        minutes = sum(counts[band] * seconds for band, seconds in SECONDS.items()) / 60
        row = {'task_id': task['task-id'], 'title': task['topic-name'], 'type': task['activity-type'],
               'base_xp': task['base_xp'], 'band_counts': dict(counts), 'question_count': len(task['questions']),
               'correct_count': sum(q['result'] == 'Correct' for q in task['questions']),
               'question_only_minutes': minutes, 'question_only_xp': int(minutes),
               'with_instruction_minutes': minutes, 'with_instruction_xp': int(minutes)}
        if row['type'] == 'Lesson':
            row['instruction'] = instruction(task['topic-id'])
            row['with_instruction_minutes'] += row['instruction']['instruction_proxy_minutes']
            row['with_instruction_xp'] = math.floor(row['with_instruction_minutes'] + .5)
        rows.append(row)

    def metrics(group, field):
        predicted = [row[field] for row in group]
        actual = [row['base_xp'] for row in group]
        errors = [p - a for p, a in zip(predicted, actual)]
        n = len(group)
        return {'activities': n, 'actual_total_xp': sum(actual), 'estimated_total_xp': sum(predicted),
                'net_error_xp': sum(errors), 'net_error_percent': 100 * sum(errors) / sum(actual),
                'mean_bias_xp': sum(errors) / n, 'mean_absolute_error_xp': sum(map(abs, errors)) / n,
                'maximum_absolute_error_xp': max(map(abs, errors)),
                'largest_underestimate_xp': min(errors), 'largest_overestimate_xp': max(errors),
                'overestimated': sum(e > 0 for e in errors), 'underestimated': sum(e < 0 for e in errors),
                'exact': sum(e == 0 for e in errors),
                'within_1_xp': sum(abs(e) <= 1 for e in errors), 'within_2_xp': sum(abs(e) <= 2 for e in errors),
                'within_3_xp': sum(abs(e) <= 3 for e in errors)}

    groups = defaultdict(list)
    for row in rows:
        groups[row['type']].append(row)
    results = {'source': str(HISTORY.relative_to(ROOT)), 'method': 'Compare all historical activities; no refitting or holdout.',
               'question_seconds': SECONDS, 'formula': 'question-only XP = E + 2*M + 3*H',
               'instruction_proxy': {'formula_minutes': '0.07513004637186382 * prose_words / 100 + 0.034422123109798704 * example_equals',
                                     'scope': 'Complete authored lesson tutorials/examples from the captured reference archive.',
                                     'qualification': 'Fitted instructional contribution, not observed reading duration. No seven-XP floor is added in this comparison.'},
               'excluded': excluded,
               'question_only': {'overall': metrics(rows, 'question_only_xp'),
                                 'by_type': {kind: metrics(group, 'question_only_xp') for kind, group in groups.items()}},
               'with_instruction': {'overall': metrics(rows, 'with_instruction_xp'),
                                    'by_type': {kind: metrics(group, 'with_instruction_xp') for kind, group in groups.items()}},
               'lesson_outcome_subgroups': {}, 'activities': rows}
    for name, predicate in [('all_correct', lambda r: r['correct_count'] == r['question_count']),
                            ('some_incorrect', lambda r: r['correct_count'] < r['question_count'])]:
        group = [r for r in groups['Lesson'] if predicate(r)]
        results['lesson_outcome_subgroups'][name] = metrics(group, 'question_only_xp')
    results['worst_question_only'] = sorted(rows, key=lambda r: abs(r['question_only_xp'] - r['base_xp']), reverse=True)[:10]
    (HERE / 'history-band-time-comparison.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({k: v for k, v in results.items() if k not in ('activities', 'worst_question_only')}, indent=2))


if __name__ == '__main__':
    main()
