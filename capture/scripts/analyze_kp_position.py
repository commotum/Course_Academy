"""Position comparisons with lesson matching and account-specific capture rates."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / 'reference/mathacademy/kp-difficulty-analysis-2026-10-12'
LEVELS = ('easy', 'moderate', 'hard')


def read(name):
    return json.loads((FOLDER / name).read_text())


def dump(name, value):
    (FOLDER / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def interval(values, rng):
    values = np.asarray(values)
    if not len(values):
        return None
    estimates = values[rng.integers(0, len(values), (4000, len(values)))].mean(axis=1)
    return dict(mean_percentage_points=100 * float(values.mean()),
                bootstrap_95_percent_interval=[100 * float(v) for v in np.quantile(estimates, [.025, .975])],
                topics=len(values))


def main():
    rows = read('kp-inventory.json')
    occurrences = read('capture-occurrences.json')
    # In the single duplicate canonical identity, use the larger rated pool.
    by_example = {}
    for r in sorted(rows, key=lambda r:r['rated_questions']):
        by_example[r['example_id']] = r
    lessons = defaultdict(dict)
    for r in by_example.values():
        for p in r['positions']:
            lessons[(p['topic_id'], p['task_id'])][p['position']] = r['example_id']
    latest = {}
    for (topic, task), points in lessons.items():
        if topic not in latest or int(task) > int(latest[topic][0]):
            latest[topic] = (task, points)
    rng = np.random.default_rng(20261012)
    paired = {}
    stratified = {}
    for minimum in (1, 5, 10, 15, 20):
        differences = defaultdict(list)
        presence_differences = defaultdict(list)
        for topic, (task, mapping) in latest.items():
            if len(mapping) < 2 or 1 not in mapping:
                continue
            first = by_example[mapping[1]]
            last = by_example[mapping[max(mapping)]]
            if min(first['rated_questions'], last['rated_questions']) < minimum:
                continue
            for level in LEVELS:
                differences[level].append(last['counts'][level] / last['rated_questions'] -
                                          first['counts'][level] / first['rated_questions'])
                presence_differences[level].append(float(last['counts'][level]>0)-float(first['counts'][level]>0))
        paired[str(minimum)] = dict(question_share_difference_last_minus_first={l:interval(differences[l],rng) for l in LEVELS},
                                   observed_availability_difference_last_minus_first={l:interval(presence_differences[l],rng) for l in LEVELS})
        groups = defaultdict(list)
        for r in by_example.values():
            p = r['latest_position']
            if p and r['rated_questions'] >= minimum:
                groups[(p['lesson_kps'], p['position'])].append(r)
        stratified[str(minimum)] = [dict(lesson_kps=size,position=position,kps=len(group),
            questions=sum(r['rated_questions'] for r in group),
            counts={l:sum(r['counts'][l] for r in group) for l in LEVELS},
            missing_level_counts={l:sum(r['counts'][l]==0 for r in group) for l in LEVELS},
            kp_mean_percent={l:100*sum(r['counts'][l]/r['rated_questions'] for r in group)/len(group) for l in LEVELS})
            for (size,position),group in sorted(groups.items())]
    account_cells = defaultdict(list)
    first_two = defaultdict(list)
    grouped_occurrences = defaultdict(list)
    for r in occurrences:
        kp = by_example.get(r['example_id'])
        if not kp or not kp['latest_position'] or r['level'] not in LEVELS:
            continue
        p = kp['latest_position']
        account_cells[(r['account'],r['kind'],p['position'])].append(r)
        if r['kind'] == 'lesson' and r['local_position'] is not None:
            grouped_occurrences[(r['account'],r['task_id'],r['example_id'])].append(r)
    for (account,task,example),group in grouped_occurrences.items():
        first_two[(account,group[0]['local_position'])].extend(group[:2])

    def cells(groups):
        return [dict(group=list(key), tasks=len({r['task_id'] for r in group}),
            question_occurrences=len(group), unique_questions=len({r['question'] for r in group}),
            counts=dict(Counter(r['level'] for r in group)),
            percent={l:100*sum(r['level']==l for r in group)/len(group) for l in LEVELS})
            for key,group in sorted(groups.items())]

    subsets = {}
    for minimum in (1,5,10,15,20):
        eligible = [r for r in rows if r['rated_questions']>=minimum]
        subsets[str(minimum)] = dict(kps=len(eligible),
            observed_level_sets=dict(Counter('/'.join(l for l in LEVELS if r['counts'][l]) for r in eligible)),
            missing_level_counts={l:sum(r['counts'][l]==0 for r in eligible) for l in LEVELS})
    candidates = {level:[r for r in rows if r['counts'][level]==0 and r['rated_questions']>=10]
                  for level in LEVELS}
    dump('position-comparisons.json', dict(seed=20261012, bootstrap_replicates=4000,
        paired_latest_lesson_first_last=paired, stratified_by_lesson_size_and_sample_size=stratified,
        account_and_activity_distributions=cells(account_cells),
        first_two_lesson_questions_by_account_and_position=cells(first_two),
        observed_options_by_sample_size=subsets,
        maximum_rated_questions=max(r['rated_questions'] for r in rows),
        zero_rated_questions=sum(not r['rated_questions'] for r in rows)))
    dump('missing-level-candidates.json',candidates)
    print(json.dumps(paired,indent=2))


if __name__=='__main__':
    main()
