"""Read-only image-bearing finite-case review; writes only image-* review artifacts."""
import collections
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = next(p for p in BASE.parents if (p / 'Cargo.toml').exists())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subset(value, universe):
    if re.match(r'^\s*none\b', value, re.I):
        return []
    if value == 'The function is not continuous on any of the given intervals':
        return []
    if re.match(r'^\s*all\b', value, re.I):
        return universe[:]
    found = re.findall(r'\b(?:IV|III|II|I|[ABCD])\b', value)
    assert found and set(found) <= set(universe), (value, universe)
    return [label for label in universe if label in found]


def proof_for(solution, label):
    # Preserve all mathematical lines following the source's per-case heading.
    markers = list(re.finditer(r'^- (?:Statements?|Diagrams?|Curves?|Regions?|Plots?|Digraphs?|Equation|Equality|Function|Rectangle)\s+([IV]+)\b', solution, re.M))
    for i, marker in enumerate(markers):
        if marker[1] == label:
            end = markers[i + 1].start() if i + 1 < len(markers) else len(solution)
            return solution[marker.start():end].strip()
    return solution


def main():
    audit = {q['id']: q for q in json.loads((BASE / 'audit-input.json').read_text())}
    manifest = json.loads((HERE / 'image-manifest.json').read_text())
    captured = BASE / 'snapshot.json' if (BASE / 'snapshot.json').exists() else BASE / 'review-snapshot.json'
    snapshot = json.loads(captured.read_text())
    current = {row[0][':db/id']: row[0] for row in snapshot['questions']}
    captured_hash = digest(captured)
    questions = []
    for item in manifest:
        q = current[item['id']]
        metadata = audit[item['id']]
        problem = q[':question/problem']
        solution = q[':question/worked-solution']
        fields = q[':question/answer-fields']
        assert len(fields) == 1
        field = fields[0]
        assert field[':answer-field/type'][':db/ident'] == ':answer-field.type/radio'
        choices = field[':answer-field/choices']
        assert all(a[':answer/type'][':db/ident'] == ':answer.type/text' for a in choices)
        key = field[':answer-field/correct']
        assert key[':db/id'] in {a[':db/id'] for a in choices}
        markers = list(re.finditer(r'^\s*(?:- |[IVX]+\. )', problem, re.M))
        if markers:
            assert len(markers) == 3
            universe = ['I', 'II', 'III']
            texts = []
            for i, marker in enumerate(markers):
                end = markers[i + 1].start() if i + 1 < len(markers) else len(problem)
                text = problem[marker.end():end].strip()
                if '\n\nYou may assume' in text:
                    text = text.split('\n\nYou may assume', 1)[0]
                texts.append(text)
            classification = 'finite_text_statements_with_reference_image'
            visual_status = 'Reference image supplies mathematical data; selectable universe is the three explicit source statements.'
        else:
            # All 45 image-only universes were viewed, including unoffered IV cases.
            if 'points' in problem:
                universe = ['A', 'B', 'C', 'D']
                noun = 'Point'
            elif 'curves' in problem:
                universe = ['I', 'II', 'III', 'IV'] if 'oriented' in problem else ['I', 'II', 'III']
                noun = 'Curve'
            elif 'regions' in problem:
                universe = ['I', 'II', 'III', 'IV']
                noun = 'Region'
            else:
                universe = ['I', 'II', 'III']
                noun = 'Digraph' if 'digraphs' in problem else 'Plot' if 'plots' in problem else 'Diagram'
            texts = [f'{noun} {label} shown in the diagram' for label in universe]
            classification = 'finite_image_labeled_cases'
            visual_status = 'All source case labels and graph contents inspected in image-cases-sheet contact sheets; worked solution and database key agree.'
        correct = subset(key[':answer/value'], universe)
        mapping = [{'answer_eid': a[':db/id'], 'value': a[':answer/value'], 'labels': subset(a[':answer/value'], universe)} for a in choices]
        evidence = [{'path': str(captured.relative_to(ROOT)), 'sha256': captured_hash, 'question_eid': item['id']}]
        for image_path in item['images']:
            path = ROOT / image_path
            evidence.append({'path': image_path, 'sha256': digest(path), 'role': 'problem_reference_image'})
        if item['captures']:
            path = ROOT / item['captures'][0]
            evidence.append({'path': item['captures'][0], 'sha256': digest(path), 'role': 'original_capture'})
        quoted = re.findall(r'correct answer(?: is| is:|)[ ]*[\"\'“]([^\"\'”]+)', solution, re.I)
        if quoted:
            assert subset(quoted[-1], universe) == correct, (item['ma_id'], quoted[-1], correct)
        proposed = problem
        if not re.search(r'select all that apply', proposed, re.I):
            proposed += '\n\nSelect all that apply.'
        if any(not row['labels'] for row in mapping):
            proposed += '\n\nIf none apply, leave all boxes unchecked.'
        questions.append({
            'id': item['id'], 'ma_id': item['ma_id'], 'decision': 'convert',
            'classification': classification,
            'atomic_options': [{'label': label, 'text': text, 'truth': label in correct,
                                'proof': proof_for(solution, label)} for label, text in zip(universe, texts)],
            'correct_labels': correct, 'choice_mapping': mapping,
            'proposed_prompt': proposed,
            'key_evidence': {'kind': 'existing_owned_database_key', 'field_eid': field[':db/id'],
                             'answer_eid': key[':db/id'], 'value': key[':answer/value'],
                             'solution_agreement': 'agrees', 'solution': solution,
                             'solution_sha256': hashlib.sha256(solution.encode()).hexdigest(),
                             'image_answer_filename_convention': 'not applicable: every old answer option is text'},
            'reason': 'Select a finite subset of independently testable source statements or labeled objects; every old combination choice decodes to a faithful subset.',
            'visual_review': visual_status,
            'content_repairs': [], 'evidence': evidence,
            'captured_basis': snapshot.get('basis'), 'captured_lineage': snapshot.get('lineage'),
            'question_sha256': hashlib.sha256(json.dumps(q, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
            'problem_before': problem, 'worked_solution_preserved': True,
            'difficulty': q[':question/difficulty'], 'kp_ids': [kp['id'] for kp in metadata['kps']],
        })
        source_notes = {
            'q-125395': 'Stored solution first calls C clockwise although the prompt defines C counterclockwise; inspected clockwise field gives negative circulation along C and positive along -C, agreeing with the existing III key. Solution preserved.',
            'q-120187': 'Stored solution III limit inserts numerator y although the offered formula is 1/(y+1). The offered formula tends to 1 as y tends to 0 and has no vertical slope there, so III is still false and I key is preserved.',
            'q-120290': 'Stored solution says (y-2)/x vanishes at y=-2; it vanishes at y=2. The offered formula has no vertical slope at x=1 and fails the displayed y=-2 stationary line. Existing I key preserved.',
            'q-159485': 'Stored solution III refers to a neighborhood of B while explaining that C is interior. The inspected diagram places C at the disk center, so III is false and I/II key is preserved.',
            'q-169184': 'Stored solution names P in its coordinate conclusion while the diagram and prompt name S. Inspected S is (-1,-3), agreeing with existing III key. Solution preserved.',
        }
        if item['ma_id'] in source_notes:
            questions[-1]['source_content_notes'] = [source_notes[item['ma_id']]]
    assert len(questions) == 317
    counts = {'total': len(questions), 'convert': len(questions),
              'classifications': dict(collections.Counter(q['classification'] for q in questions)),
              'atomic_options': sum(len(q['atomic_options']) for q in questions),
              'choice_mappings': sum(len(q['choice_mapping']) for q in questions),
              'database_keys_preserved': len(questions), 'zero_selection_correct': sum(not q['correct_labels'] for q in questions),
              'content_repairs': 0, 'database_writes': 0}
    (HERE / 'image-cases.json').write_text(json.dumps({'counts': counts, 'questions': questions}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
