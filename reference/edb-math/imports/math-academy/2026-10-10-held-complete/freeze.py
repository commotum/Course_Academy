"""Freeze complete subagent reviews against fresh original captures. No DB calls."""
import collections
import copy
import hashlib
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / '2026-10-10-held-literal'
ORIGINAL = ROOT.parent / '2026-10-10-held-next'
WORKERS = ('prose', 'compound', 'math')
HOLD_REASONS = {'math_academy_wrong_key', 'no_correct_option',
                'multiple_correct_options', 'contradictory_source',
                'missing_authoritative_evidence', 'irrecoverable_capture'}


def read(path):
    return json.loads(Path(path).read_text())


def save(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def answer(choice):
    return {k: choice[k] for k in ('type', 'value')}


def pointer(obj, path):
    assert path.startswith('/')
    for part in path[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def roman_layout(problem, html):
    widget = BeautifulSoup(html, 'html.parser').select_one('.questionWidget-text')
    lists = widget.select('ol.questionStatements') if widget else []
    if not lists:
        return None
    assert len(lists) == 1 and len(lists[0].find_all('li', recursive=False)) == 3
    lines = problem.splitlines()
    indices = [i for i, line in enumerate(lines) if line.startswith('- ')]
    assert len(indices) == 3
    for i, label in zip(indices, ('I. ', 'II. ', 'III. ')):
        lines[i] = label + lines[i][2:]
    return '\n'.join(lines)


def main():
    starting = read(ROOT / 'starting-state.json')
    index = ROOT.parent / 'held-questions.json'
    assert sha(index) == starting['held_index_sha256']
    held = {q['math_academy_id'] for q in read(index)['questions']}
    rows = read(PREVIOUS / 'remaining-questions.json')
    raw = read(ORIGINAL / 'recovery-input.json')
    assert held == set(rows) and len(held) == starting['held'] == 839
    final, events, worker_of = {}, [], {}
    supplemental = read(ROOT / 'supplemental-revision-reasons.json')
    for worker in WORKERS:
        assigned = read(ROOT / worker / 'assignment.json')
        submitted = {}
        for line in (ROOT / worker / 'reviews.jsonl').read_text().splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            mid = record['id']
            assert mid in assigned, (worker, mid, 'unassigned')
            if mid in submitted:
                assert record.get('revision_reason') or supplemental.get(worker + '/' + mid), (mid, 'unexplained revision')
            submitted[mid] = record
            events.append(dict(record, reviewer=worker))
        assert set(submitted) == set(assigned), (worker, 'incomplete coverage', sorted(set(assigned)-set(submitted)))
        assert not set(final) & set(submitted)
        final.update(submitted)
        worker_of.update({mid: worker for mid in submitted})
    assert set(final) == held

    cache, reviewed, used, holds, discrepancies, hashes = {}, {}, {}, {}, [], {}
    situations = collections.defaultdict(list)
    restored_count = 0
    for mid, decision in sorted(final.items()):
        assert type(decision['ready']) is bool
        for kind in decision['situation_types']:
            assert isinstance(kind, str) and kind.strip()
            situations[kind].append(mid)
        for issue in decision.get('disagreements', []):
            discrepancies.append({'question': mid, 'reviewer': worker_of[mid],
                                  **({'issue': issue} if isinstance(issue, str) else issue)})
        path = Path(decision['directory'])
        occurrences = [o for o in raw[mid]['occurrences'] if o['directory'] == str(path)]
        assert len(occurrences) == 1, (mid, 'ambiguous occurrence')
        o = occurrences[0]
        if str(path) not in cache:
            cache[str(path)] = read(path / 'state.json')
        state = cache[str(path)]
        rec = state['questions'][mid]
        before = rec['before']
        stage = o['source_solution_stage']
        solution = rec[stage]['worked_solution']
        problem = before.get('source_problem') or before['problem']
        assert solution == o['worked_solution'] and problem == o['source_problem'], mid
        assert [(f['key'], f['type'], [answer(c) for c in f['choices']]) for f in before['fields']] == [(f['key'], f['type'], [answer(c) for c in f['choices']]) for f in o['before_fields']], mid
        local_hashes = {str(p): sha(p) for p in (path / 'state.json', path / 'content.json')}
        for p, h in local_hashes.items():
            assert p not in hashes or hashes[p] == h, (mid, 'capture changed')
            hashes[p] = h
        location = {'file': str(path / 'state.json'),
                    'json_pointer': f'/questions/{mid}/{stage}/worked_solution'}
        if not decision['ready']:
            assert decision['hold_reason'] in HOLD_REASONS and decision.get('explanation'), mid
            holds[mid] = dict(decision, source_hashes=local_hashes,
                              source_problem=problem, source_quote=solution,
                              solution_location=location, reviewer=worker_of[mid],
                              original_before_fields=copy.deepcopy(before['fields']),
                              before_layout_sha256=hashlib.sha256(json.dumps(before, sort_keys=True, ensure_ascii=False).encode()).hexdigest())
            continue
        assert len(decision['fields']) == len(before['fields']), (mid, 'incomplete fields')
        assert len({f['key'] for f in decision['fields']}) == len(decision['fields'])
        bykey = {f['key']: f for f in decision['fields']}
        audit_fields = []
        soup = BeautifulSoup(before['html'], 'html.parser')
        for field in before['fields']:
            f = copy.deepcopy(bykey[field['key']])
            ix = f['choice_index']
            assert type(ix) is int and 0 <= ix < len(field['choices'])
            assert f['answer'] == answer(field['choices'][ix]), (mid, 'choice changed')
            assert sum(answer(c) == f['answer'] for c in field['choices']) == 1, (mid, 'duplicate chosen choice')
            assert f['binding'].strip() and f['source_quote'].strip()
            loc = f['source_location']
            assert Path(loc['file']) == path / 'state.json', (mid, 'different capture')
            cited = pointer(state, loc['json_pointer'])
            if loc['json_pointer'].endswith('/worked_solution'):
                assert loc['json_pointer'] in {f'/questions/{mid}/after/worked_solution', f'/questions/{mid}/history/worked_solution'}
                assert cited == solution and f['source_quote'] in cited, (mid, 'quote/location mismatch')
                observed_stage = rec[loc['json_pointer'].split('/')[3]]
                observed_problem = observed_stage.get('source_problem') or observed_stage.get('problem')
                if observed_problem:
                    assert observed_problem == problem, (mid, 'different observed prompt')
                if observed_stage.get('fields'):
                    assert [(g['key'], g['type'], [answer(c) for c in g['choices']]) for g in observed_stage['fields']] == [(g['key'], g['type'], [answer(c) for c in g['choices']]) for g in before['fields']], (mid, 'different observed field version')
            else:
                assert loc['json_pointer'].endswith('/source_correct')
                assert cited == f['answer'], (mid, 'grade answer mismatch')
                prefix = loc['json_pointer'].rsplit('/', 1)[0]
                observed = pointer(state, prefix)
                assert observed['key'] == field['key'] and observed['dom_id'] == field['dom_id']
                assert [answer(c) for c in observed['choices']] == [answer(c) for c in field['choices']]
                f['source_quote'] = json.dumps({'key': field['key'], 'dom_id': field['dom_id'], 'source_correct': cited}, ensure_ascii=False)
                f['method'] = 'fresh_captured_source_correct'
            if field['type'] == 'radio':
                assert len(soup.select('.questionWidget-choiceText, .choiceText')) == len(field['choices'])
            else:
                node = soup.find(id=field['dom_id'])
                assert node is not None and len(node.select('.selectListOption')) == len(field['choices'])
                assert problem.count('{{' + field['key'] + '}}') == 1
            audit_fields.append(f)
        audit = {'directory': str(path), 'category': rows[mid]['category'],
                 'source': ':org/Math-Academy', 'reviewer': worker_of[mid],
                 'review_method': 'Full source, prompt role, original options, and substantive-content review by GPT-6.1-sol/high',
                 'source_problem': problem, 'source_quote': solution,
                 'solution_location': location, 'source_hashes': local_hashes,
                 'before_layout_sha256': hashlib.sha256(json.dumps(before, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                 'original_before_fields': copy.deepcopy(before['fields']),
                 'fields': audit_fields, 'situation_types': decision['situation_types']}
        restored = roman_layout(problem, before['html'])
        if restored:
            if decision.get('restored_problem'):
                assert decision['restored_problem'] == restored, (mid, 'Roman statement restoration mismatch')
            assert any(re.search(r'\b(?:I|II|III)\b', c['value']) for field in before['fields'] for c in field['choices'])
            audit['restored_problem'] = restored
            audit['restoration_type'] = 'roman_statement_labels'
            audit['layout_note'] = 'Restore original I/II/III ordered statement labels, preserving all statement text and order from the captured questionStatements list.'
            restored_count += 1
            situations['roman_labels_restored_from_html'].append(mid)
        elif decision.get('restored_problem'):
            audit['restored_problem'] = decision['restored_problem']
            audit['layout_note'] = decision['layout_note']
            audit['restoration_type'] = 'select_field_layout' if rows[mid]['category'] == 'select_field_binding' else 'phantom_mathml_blank'
            if rows[mid]['category'] == 'select_field_binding':
                audit['layout_recovery'] = {'method': 'captured_HTML_field_geometry', 'note': decision['layout_note']}
        reviewed[mid] = audit
        used[mid] = {'occurrences': [copy.deepcopy(o)]}
    assert set(reviewed) | set(holds) == held and not set(reviewed) & set(holds)
    assert all(sha(p) == h for p, h in hashes.items())
    counts = {'covered': len(final), 'ready_questions': len(reviewed),
              'ready_fields': sum(len(r['fields']) for r in reviewed.values()),
              'held_questions': len(holds), 'hold_reasons': dict(collections.Counter(h['hold_reason'] for h in holds.values())),
              'restored_roman_statement_questions': restored_count,
              'review_events': len(events), 'workers': {w: sum(x == w for x in worker_of.values()) for w in WORKERS}}
    for name, obj in [('answer-review.json', reviewed), ('recovery-input.json', used),
                      ('held-review.json', holds), ('disagreements.json', discrepancies),
                      ('final-decisions.json', final), ('review-counts.json', counts),
                      ('source-hashes.json', hashes), ('situation-summary.json',
                       {kind: {'count': len(set(ids)), 'question_ids': sorted(set(ids))} for kind, ids in sorted(situations.items())})]:
        save(ROOT / name, obj)
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    main()
