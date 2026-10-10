import collections
import copy
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, '/home/jake/Developer/Course_Academy/scripts/question_capture')
from core import normalize

OUT = Path('/tmp/newer-captures-prepared')
OUT.mkdir(exist_ok=True)
inventory = json.loads(Path('/tmp/newer-captures-inventory.json').read_text())
activities = sorted(inventory['activities'], key=lambda x: (x['basis'], int(x['task']), x['stream']))
records, deferred, counts, multis = [], [], collections.Counter(), []

def read(path):
    return json.loads(path.read_text()) if path.exists() else {}

def equivalent(a, b, kind):
    return a == b or normalize(a, kind) == normalize(b, kind)

for number, activity in enumerate(activities, 1):
    directory = Path(activity['path'])
    state = read(directory/'state.json')
    content = activity['content']
    metadata = read(directory/'activity-metadata.json')
    if isinstance(metadata, dict):
        metadata = metadata.get('questions', list(metadata.values()))
    metadata = {x['id'].replace('question-', 'q-'): x for x in metadata if isinstance(x, dict) and x.get('id')}
    if content.get('task_type') == 'multistep':
        multis.append({'task': activity['task'], 'source_directory': str(directory), 'source_multistep_id': content.get('multistep_id'), 'questions': content.get('question_order', []), 'shared_contexts': [{'id': c.get('id', c.get('dom_id')), 'problem': c['problem']} for c in state.get('shared_contexts', content.get('shared_contexts', []))]})
    imported_ids = activity['verification'].get('imported_question_ids')
    for q in content['questions'] + content.get('canonical_examples', []):
        mid = q['math_academy_id']
        canonical = mid.startswith('e-')
        if not canonical and imported_ids is not None and mid not in imported_ids:
            deferred.append({'question': mid, 'task': activity['task'], 'reason': 'Not listed among verified imported question IDs'})
            continue
        try:
            record = state.get('questions', {}).get(mid, {})
            if canonical:
                raw = read(directory/f'example-{mid[2:]}.json')
                before = after = raw
            else:
                before = record.get('before') or read(directory/f'{mid}-before.json')
                after = record.get('history') or read(directory/f'history-{mid}.json') or record.get('after') or read(directory/f'{mid}-after.json')
            assert before and after, 'Original before/feedback capture missing'
            assert not before.get('errors') and not after.get('errors'), 'Source extraction errors remain'
            problem = before.get('source_problem') or before.get('problem')
            solution = after.get('worked_solution')
            assert problem and solution, 'Source problem or worked solution missing'
            # The multistep runner composes prior answers into source_problem;
            # its local_problem is the original question on the MA page.
            if content.get('task_type') == 'multistep':
                problem = q.get('local_problem') or before.get('local_problem') or before['problem']
            assert not any(s in problem + solution for s in ['[Missing image:', '[MATH:', '[IMG:']), 'Unresolved source markup'
            normalized_fields = {f['key']: f for f in q.get('answer_fields', [])}
            fields = []
            for raw in before.get('fields', []):
                key, kind = raw['key'], raw['type']
                f = {'key': key, 'type': kind, 'choices': [], 'key_evidence': None}
                if kind in ('radio', 'select'):
                    f['choices'] = [{k: c[k] for k in ['type', 'value']} for c in raw.get('choices', [])]
                    assert f['choices'], 'Captured choice widget has no choices'
                    f['choices_complete'] = raw.get('choices_complete') is True or (kind == 'radio' and len(re.findall(r'class="[^"\n]*\b(?:questionWidget-choiceText|choiceText)\b', before.get('html', ''))) == len(f['choices']))
                direct = raw.get('source_correct')
                if isinstance(direct, dict) and direct.get('type') and direct.get('value') is not None:
                    f['correct'] = {k: direct[k] for k in ['type', 'value']}
                    f['key_evidence'] = 'ma_explicit_answer'
                elif not canonical and (record.get('actual_result') or record.get('after', {}).get('result')) == 'Correct' and raw.get('submitted_value') is not None:
                    submitted = raw['submitted_value']
                    if kind in ('radio', 'select'):
                        candidates = [c for c in f['choices'] if equivalent(submitted, c['value'], c['type'])]
                        if candidates:
                            f['correct'] = copy.deepcopy(candidates[0])
                            f['key_evidence'] = 'ma_successful_grade'
                    else:
                        # A successful MA grade attests this exact submitted
                        # string; its mathematical validity is not inferred.
                        known = normalized_fields.get(key, {}).get('choices', [])
                        representation = next((c['type'] for c in known if equivalent(submitted, c['value'], c['type'])), 'math' if raw.get('tag') == 'mathquill' else 'text')
                        f['correct'] = {'type': representation, 'value': submitted}
                        f['key_evidence'] = 'ma_successful_grade'
                if 'correct' in f:
                    correct = f['correct']
                    if kind == 'blank':
                        f['choices'] = [copy.deepcopy(correct)]
                    elif not any(c == correct for c in f['choices']):
                        # An explicit answer can expose an omitted source
                        # answer; it is not an invented distractor.
                        f['choices'].append(copy.deepcopy(correct))
                    counts['source_keys'] += 1
                else:
                    counts['keys_left_unknown'] += 1
                fields.append(f)
            topic = q.get('topic_id') or content.get('topic_id')
            assert topic is not None, 'Source topic not identified'
            anchor = q.get('knowledge_point_source_id')
            href = q.get('provenance', {}).get('kp_href')
            if anchor is None and href and '#' in href:
                anchor = href.rsplit('#', 1)[1]
            if canonical:
                anchor = int(mid[2:])
            if anchor is None:
                same = [e['math_academy_id'][2:] for e in content.get('canonical_examples', []) if e.get('knowledge_point_id') == q.get('knowledge_point_id')]
                if len(set(same)) == 1:
                    anchor = same[0]
            rating = metadata.get(mid, {}).get('difficulty')
            difficulty = {'E':'easy', 'M':'moderate', 'H':'hard'}.get(rating)
            if not difficulty and not canonical and q.get('difficulty') in ['easy', 'moderate', 'hard']:
                # Frozen verification covers the observed source rating. Keep
                # the historical observation, never estimate a new rating.
                difficulty = q['difficulty']
            result = {'math_academy_id': mid, 'topic_id': int(topic), 'source_example_id': str(anchor) if anchor is not None else None, 'knowledge_point': q.get('knowledge_point'), 'legacy_kp_uuid': q.get('knowledge_point_id'), 'problem': problem, 'worked_solution': solution, 'answer_fields': fields, 'difficulty': difficulty, 'requires_calculator': bool(before.get('calculator_instructions')) or None, 'task': activity['task'], 'stream': activity['stream'], 'basis': activity['basis'], 'source_directory': str(directory), 'canonical': canonical, 'multistep': content.get('task_type') == 'multistep', 'source_files': [str(directory/'state.json'), str(directory/'content.json'), str(directory/'edb-import/verification.json')], 'excluded_correct_origins': [f.get('correct_origin') for f in q.get('answer_fields', []) if f.get('correct_origin') in ('model_interpretation', 'reviewed_ma_solution', 'ma_revealed_solution')]}
            records.append(result)
            counts['canonical_occurrences' if canonical else 'practice_occurrences'] += 1
        except (AssertionError, KeyError, TypeError, ValueError) as error:
            deferred.append({'question': mid, 'task': activity['task'], 'stream': activity['stream'], 'reason': str(error), 'source_directory': str(directory)})
    if number % 200 == 0:
        print(f'Read {number}/{len(activities)} captures; {len(records)} source records; {len(deferred)} deferred.', flush=True)

(OUT/'source-occurrences.json').write_text(json.dumps({'records':records},ensure_ascii=False)+'\n')
(OUT/'source-extraction-deferred.json').write_text(json.dumps(deferred,indent=2)+'\n')
(OUT/'multisteps.json').write_text(json.dumps(multis,ensure_ascii=False)+'\n')
print(json.dumps({'activities':len(activities),'records':len(records),'deferred':len(deferred),'counts':counts,'deferred_reasons':collections.Counter(x['reason'] for x in deferred)},indent=2),flush=True)
