"""Freeze manual source-backed reviews without database access or capture edits.

Run only after both assignment-N-review.json files have been written. All
coverage and source checks finish before any output is written.
"""
import copy
import hashlib
import json
from pathlib import Path

from bs4 import BeautifulSoup
from decisions import HELD, REVIEW


ROOT = Path(__file__).resolve().parent
DIRECT = ROOT.parent / '2026-10-10-held-direct'
ORIGINAL = ROOT.parent / '2026-10-10-held-next'
CATEGORY = 'math_candidate_literal_present_but_not_bound_to_answer'
EXPECTED_TOTAL = 230
REVIEW_KEYS = {
    'ready', 'choice_index', 'answer', 'binding', 'source_quote',
    'source_location', 'disagreements',
}
KNOWN_DISAGREEMENTS = [
    {
        'question': 'q-123292',
        'issue': 'The initial component integration line uses sin t, whereas '
                 'the original prompt and subsequent integration use cos(t+1).',
        'resolution': 'Preserve the source verbatim; the subsequent full '
                      'antiderivative explicitly binds the original option '
                      'with sin(t+1) and the vector integration constant.',
        'material_answer_conflict': False,
    },
    {
        'question': 'q-116755',
        'issue': 'The final source prose calls dV/dt = 8 cubic meters per hour '
                 'the water-level rate.',
        'resolution': 'Preserve the source verbatim; the volume derivative '
                      'calculation and cubic-meter-per-hour units explicitly '
                      'bind the requested volume rate.',
        'material_answer_conflict': False,
    },
]


def read(path):
    return json.loads(Path(path).read_text())


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def value(choice):
    return {key: choice[key] for key in ('type', 'value')}


def require(condition, message):
    # These integrity checks must also run when Python is invoked with -O.
    if not condition:
        raise ValueError(message)


def source_snapshot(mid, row, raw):
    """Recheck one original occurrence against the current saved capture."""
    path = Path(row['directory'])
    hashes = {str(p): sha(p) for p in (path / 'state.json', path / 'content.json')}
    state = read(path / 'state.json')
    rec = state['questions'][mid]
    before = rec['before']
    occurrences = [o for o in raw[mid]['occurrences'] if o['directory'] == str(path)]
    require(len(occurrences) == 1, f'{mid}: occurrence is not unique')
    occurrence = occurrences[0]
    stage = occurrence['source_solution_stage']
    require(stage in rec, f'{mid}: saved solution stage is absent from state.json')
    solution = rec[stage]['worked_solution']
    problem = before.get('source_problem') or before['problem']
    require(solution == row['worked_solution'] == occurrence['worked_solution'],
            f'{mid}: saved source solution changed')
    require(problem == row['source_problem'] == occurrence['source_problem'],
            f'{mid}: saved source problem changed')
    location = {'file': str(path / 'state.json'),
                'json_pointer': f'/questions/{mid}/{stage}/worked_solution'}
    require(row['source_solution_location'] == location['json_pointer'],
            f'{mid}: analysis solution stage differs from the occurrence')
    require(len(before['fields']) == len(occurrence['before_fields']) == 1,
            f'{mid}: expected one original radio field')
    field = before['fields'][0]
    original = occurrence['before_fields'][0]
    require(field['key'] == original['key'] and field['type'] == original['type'] == 'radio',
            f'{mid}: original field identity changed')
    require(len(field['choices']) == len(original['choices']),
            f'{mid}: original choice count changed')
    for current, old in zip(field['choices'], original['choices']):
        # Older recovery input omits HTML; compare every property it retains.
        require(all(current.get(k) == v for k, v in old.items()),
                f'{mid}: original choice or its DOM identity changed')
    require([value(c) for c in field['choices']] ==
            [value(c) for c in row['original_choices']],
            f'{mid}: analysis original choice order changed')
    choices = [value(c) for c in field['choices']]
    require(len(choices) >= 2 and all(c['value'].strip(' $\t\r\n') for c in choices),
            f'{mid}: incomplete original choices')
    soup = BeautifulSoup(before['html'], 'html.parser')
    nodes = soup.select('.questionWidget-choiceText, .choiceText')
    require(len(nodes) == len(choices), f'{mid}: original DOM choice layout differs')
    for current in field['choices']:
        require(soup.find(id=current['dom_id']) is not None,
                f'{mid}: original choice DOM ID is absent')
    return path, occurrence, before, field, solution, location, hashes


def checked_location(mid, supplied, expected):
    if isinstance(supplied, str):
        require(supplied == expected['json_pointer'], f'{mid}: wrong solution pointer')
    else:
        require(isinstance(supplied, dict) and supplied == expected,
                f'{mid}: wrong saved solution location')
    return copy.deepcopy(expected)


def add_disagreements(mid, entries, result):
    require(isinstance(entries, list), f'{mid}: disagreements must be a list')
    for entry in entries:
        if isinstance(entry, str):
            require(bool(entry.strip()), f'{mid}: empty disagreement')
            item = {'question': mid, 'issue': entry}
        else:
            require(isinstance(entry, dict) and bool(entry.get('issue')),
                    f'{mid}: malformed disagreement')
            require(entry.get('question', mid) == mid,
                    f'{mid}: disagreement names another question')
            item = dict(entry, question=mid)
        result.append(item)


def build_reviews():
    rows = read(DIRECT / 'remaining-questions.json')
    raw = read(ORIGINAL / 'recovery-input.json')
    held_ids = {q['math_academy_id'] for q in read(ROOT.parent / 'held-questions.json')['questions']}
    targets = {mid for mid, row in rows.items() if row['category'] == CATEGORY}
    require(len(targets) == EXPECTED_TOTAL, 'Expected exactly 230 current literal-category questions')
    require(len(REVIEW) == 170, 'Expected 170 existing manual binding notes')
    notes = {f'q-{n}': note for n, note in REVIEW.items()}
    explicit_held = {f'q-{n}': note for n, note in HELD.items()}
    require(not (set(notes) & set(explicit_held)), 'Manual ready and held notes overlap')
    agents = {}
    for number in (1, 2):
        assigned = read(ROOT / f'assignment-{number}.json')
        submitted = read(ROOT / f'assignment-{number}-review.json')
        require(set(assigned) == set(submitted), f'Assignment {number}: missing or extra reviews')
        require(not (set(agents) & set(submitted)), 'Assignment review IDs overlap')
        for mid, row in assigned.items():
            require(row == rows[mid], f'{mid}: assignment differs from current remaining analysis')
        agents.update(submitted)
    require(not ((set(notes) | set(explicit_held)) & set(agents)), 'Manual and assignment IDs overlap')
    covered = set(notes) | set(explicit_held) | set(agents)
    require(covered == targets and covered <= held_ids,
            'Every one of the 230 held category IDs must be reviewed or explicitly held')
    review, used, still_held = {}, {}, {}
    disagreements = copy.deepcopy(KNOWN_DISAGREEMENTS)
    all_hashes = {}
    for mid in sorted(covered):
        row = rows[mid]
        path, occurrence, before, field, solution, location, hashes = source_snapshot(mid, row, raw)
        all_hashes.update(hashes)
        if mid in explicit_held:
            require(bool(explicit_held[mid].strip()), f'{mid}: missing explicit hold reason')
            still_held[mid] = {'ready': False, 'binding': explicit_held[mid],
                               'source_quote': solution, 'source_location': location}
            continue
        if mid in notes:
            binding = notes[mid]
            require(isinstance(binding, str) and bool(binding.strip()), f'{mid}: missing manual binding')
            require(len(row['candidates']) == 1, f'{mid}: ambiguous manual-note candidate')
            answer = value(row['candidates'][0])
            indices = [i for i, c in enumerate(field['choices']) if value(c) == answer]
            require(len(indices) == 1, f'{mid}: candidate is not a unique exact original choice')
            index, quote = indices[0], solution
        else:
            decision = agents[mid]
            require(isinstance(decision, dict) and REVIEW_KEYS <= decision.keys(),
                    f'{mid}: assignment review has missing fields')
            require(type(decision['ready']) is bool, f'{mid}: ready must be Boolean')
            add_disagreements(mid, decision['disagreements'], disagreements)
            binding, quote = decision['binding'], decision['source_quote']
            require(isinstance(binding, str) and bool(binding.strip()), f'{mid}: missing prompt-role binding')
            require(isinstance(quote, str) and bool(quote.strip()) and quote in solution,
                    f'{mid}: field quote is not an exact saved solution substring')
            checked_location(mid, decision['source_location'], location)
            if not decision['ready']:
                still_held[mid] = copy.deepcopy(decision)
                continue
            require(not any(isinstance(d, dict) and d.get('material_answer_conflict')
                            for d in decision['disagreements']),
                    f'{mid}: ready review has a material answer conflict')
            answer, index = decision['answer'], decision['choice_index']
            require(isinstance(answer, dict) and set(answer) == {'type', 'value'},
                    f'{mid}: answer must contain exact type and value only')
            require(type(index) is int and 0 <= index < len(field['choices']),
                    f'{mid}: invalid original choice index')
            require(value(field['choices'][index]) == answer,
                    f'{mid}: answer differs from the original indexed choice')
            require(sum(value(c) == answer for c in field['choices']) == 1,
                    f'{mid}: answer is not a unique exact original choice')
        review[mid] = {
            'directory': str(path), 'category': CATEGORY, 'source': ':org/Math-Academy',
            'review_method': 'manual interpretation of saved MA solution and prompt role',
            'source_problem': occurrence['source_problem'], 'source_quote': solution,
            'solution_location': location, 'source_hashes': hashes,
            'before_layout_sha256': hashlib.sha256(json.dumps(
                before, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
            # Retain complete captured MathML/HTML and exact authored choice strings.
            'original_before_fields': copy.deepcopy(before['fields']),
            'fields': [{'key': field['key'], 'choice_index': index,
                        'answer': copy.deepcopy(answer), 'binding': binding,
                        'source_location': location, 'source_quote': quote,
                        'method': 'saved_worked_solution_with_manual_field_binding'}],
        }
        used[mid] = {'occurrences': [copy.deepcopy(occurrence)]}
    require(set(review) | set(still_held) == targets, 'Final review coverage differs')
    require(all(sha(p) == digest for p, digest in all_hashes.items()),
            'A saved capture changed during review freezing')
    counts = {'questions': len(review), 'radio': len(review), 'select': 0,
              'fields': sum(len(r['fields']) for r in review.values()),
              'covered_questions': len(covered), 'explicitly_held': len(still_held),
              'ready_ids': sorted(review), 'held_ids': sorted(still_held),
              'manual_binding_notes': len(notes), 'assignment_reviews': len(agents)}
    return review, used, still_held, disagreements, counts


def main():
    review, used, still_held, disagreements, counts = build_reviews()
    for name, data in (
        ('answer-review.json', review), ('recovery-input.json', used),
        ('held-review.json', still_held), ('disagreements.json', disagreements),
        ('review-counts.json', counts),
    ):
        save(ROOT / name, data)
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
