#!/usr/bin/env python3
"""Extract historical question evidence and question-time/base-XP summaries.

Run with /home/jake/Developer/MA/.venv/bin/python (BeautifulSoup dependency).
Original browser captures and progress.csv are read-only inputs. Lesson times
exclude instructional reading; displayed elapsed times may include pauses.
"""
import csv
import hashlib
import json
import re
import statistics
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROGRESS = ROOT / "reference/progress.csv"
LESSONS = Path("/home/jake/Developer/MA/DATA/Lessons")


def title_key(text):
    text = re.sub(r"^KP\s+\d+\.\s*", "", text or "")
    # The archived topic 281 uses "Leibnitz"; the history uses "Leibniz".
    return " ".join(unicodedata.normalize("NFKC", text).casefold().replace('leibnitz', 'leibniz').split())


def main():
    rows = list(csv.DictReader(PROGRESS.open()))
    assert len({r['task-id'] for r in rows}) == len(rows)
    lessons = {}
    examples = {}
    extra_examples = {}
    for path in HERE.glob('canonical-example-*.json'):
        extra = json.loads(path.read_text())
        extra_examples[extra['topic_id'] + ':' + extra['historical_example_id']] = extra
    tasks = []
    counts = Counter()
    for row in rows:
        path = HERE / (row['task-id'] + '.json')
        if not path.exists():
            counts['missing_tasks'] += 1
            continue
        captured = json.loads(path.read_text())
        if captured['status'] != 'captured':
            counts['failed_tasks'] += 1
            continue
        assert captured['task_id'] == row['task-id']
        assert captured['source_url'] == row['url']
        soup = BeautifulSoup(captured['raw_html'], 'html.parser')
        nodes_by_id = {node['id']: node for node in soup.find_all(id=True)}
        task = {**row, 'source_file': str(path.relative_to(ROOT)),
                'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'captured_at': captured['captured_at'], 'questions': []}
        for original in captured['questions']:
            q = {k: v for k, v in original.items() if k != 'raw_html'}
            match = re.fullmatch(r'Elapsed:\s*(\d+):(\d\d)', q['displayed_elapsed'])
            assert match and int(match[2]) < 60, (path, q['id'])
            q['elapsed_seconds'] = int(match[1]) * 60 + int(match[2])
            node = nodes_by_id.get(q['id'])
            assert node is not None, (path, q['id'])
            prompt = node.select_one('.questionText')
            solution = nodes_by_id.get(q['id'].replace('question-', 'questionExplanation-'))
            q['problem_html'] = str(prompt) if prompt else None
            q['worked_solution_html'] = str(solution) if solution else None
            counts['questions'] += 1
            counts['with_problem'] += bool(prompt and prompt.get_text(strip=True))
            counts['with_worked_solution'] += bool(solution and solution.get_text(strip=True))
            counts['with_difficulty'] += q['difficulty'] in ('E', 'M', 'H')
            counts['with_outcome'] += q['result'] in ('Correct', 'Incorrect')
            q['asset_urls'] = sorted({urljoin(row['url'], image['src'])
                                      for parent in (prompt, solution) if parent
                                      for image in parent.find_all('img', src=True)})
            href = re.fullmatch(r'/topics/(\d+)#(\d+)', q['kp_href'] or '')
            topic_id = href[1] if href else row['topic-id']
            example_id = href[2] if href else None
            q['topic_id'] = topic_id or None
            if topic_id:
                if topic_id not in lessons:
                    source = LESSONS / topic_id / 'Source' / (topic_id + '.json')
                    lessons[topic_id] = json.loads(source.read_text()) if source.exists() else None
                lesson = lessons[topic_id]
                candidates = [item for item in lesson['lesson']['items']
                              if item.get('item_type') == 'step' and item.get('step_type') == 'example'
                              and (item['content_id'] == example_id if example_id else
                                   title_key(item['title']) == title_key(q['kp_title']))] if lesson else []
                if len(candidates) == 1:
                    example = candidates[0]
                    key = topic_id + ':' + example['content_id']
                    q['canonical_example_key'] = key
                    examples[key] = {'topic_id': topic_id, 'example_id': example['content_id'],
                                     'step_id': example['step_id'], 'title': example['title'],
                                     'source_file': str(LESSONS / topic_id / 'Source' / (topic_id + '.json')),
                                     'provenance': 'Existing captured reference lesson; not newly observed historical instruction.',
                                     'sections': example['sections']}
                    counts['with_canonical_example_match'] += 1
                else:
                    extra_key = topic_id + ':' + example_id if example_id else None
                    if extra_key in extra_examples:
                        q['canonical_example_key'] = extra_key
                        examples[extra_key] = extra_examples[extra_key]
                        counts['with_canonical_example_match'] += 1
                    else:
                        q['canonical_example_match_status'] = 'ambiguous' if candidates else 'not_found'
            task['questions'].append(q)
        task['question_count'] = len(task['questions'])
        task['question_elapsed_seconds'] = sum(q['elapsed_seconds'] for q in task['questions'])
        task['base_xp'] = int(row['xp-possible']) if row['xp-possible'] else None
        task['question_time_base_ratio'] = (task['question_elapsed_seconds'] / (60 * task['base_xp'])
                                           if task['base_xp'] else None)
        tasks.append(task)
        counts['captured_tasks'] += 1

    def summarize(group):
        eligible = [t for t in group if t['base_xp'] is not None and t['base_xp'] > 0]
        seconds = sum(t['question_elapsed_seconds'] for t in eligible)
        base = sum(t['base_xp'] for t in eligible)
        ratios = [t['question_time_base_ratio'] for t in eligible]
        return {'activities': len(eligible), 'questions': sum(t['question_count'] for t in eligible),
                'base_minutes': base, 'question_minutes': seconds / 60,
                'total_time_ratio': seconds / (base * 60) if base else None,
                'mean_activity_ratio': statistics.mean(ratios) if ratios else None,
                'median_activity_ratio': statistics.median(ratios) if ratios else None}

    by_type = defaultdict(list)
    for task in tasks:
        by_type[task['activity-type']].append(task)
    summary = {'source': str(PROGRESS.relative_to(ROOT)),
               'source_sha256': hashlib.sha256(PROGRESS.read_bytes()).hexdigest(),
               'requested_activities': len(rows), 'coverage': dict(counts),
               'interpretation': 'Question-time/base-XP ratio, assuming 1 base XP = 1 minute. '
                                 'Lesson tutorial/example reading is excluded. Displayed times may include pauses. '
                                 'No durations inferred from gaps between completions. Diagnostics without base XP excluded from ratios.',
               'overall': summarize(tasks),
               'reviews_and_assessments': summarize(by_type['Review'] + by_type['Assessment']),
               'by_type': {kind: summarize(group) for kind, group in by_type.items()}}
    (HERE / 'observations.json').write_text(json.dumps({'summary': summary, 'tasks': tasks,
                                                      'canonical_examples': examples}, indent=2) + '\n')
    (HERE / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
