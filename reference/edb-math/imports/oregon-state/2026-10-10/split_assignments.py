#!/usr/bin/env python3
"""Prepare auditable F26 source-transcription and authored-study layers; no DB I/O."""
from pathlib import Path
import ast
import collections
import copy
import hashlib
import json
import re
from urllib.parse import unquote

ROOT = Path('/home/jake/Developer/Course_Academy/.local/edb')
OUT = Path('/tmp/osu-preparation')
S1 = Path('/home/jake/.codex/sessions/2026/10/01/rollout-2026-10-01T17-59-57-01a0fa20-034f-7671-a28b-702142706776.jsonl')
S2 = Path('/home/jake/.codex/sessions/2026/10/06/rollout-2026-10-06T07-25-53-01a1119b-4fd2-7bc3-9627-c5f32d0dcea5.jsonl')

def read(p):
    return json.loads(p.read_text())

def write(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def session_evidence(path, requested):
    context, context_line = {}, None
    evidence, commands = [], {}
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        row = json.loads(line)
        payload = row.get('payload', {})
        if row['type'] == 'turn_context':
            context, context_line = payload, line_number
        if line_number not in requested:
            continue
        assert payload.get('type') in ('function_call', 'custom_tool_call')
        raw = payload.get('arguments', payload.get('input', ''))
        match = re.search(r'cmd:("(?:[^"\\]|\\.)*")', raw)
        command = json.loads(match[1])
        commands[line_number] = command
        evidence.append({
            'session_path': str(path), 'session_id': re.search(r'([0-9a-f]{8}-[0-9a-f-]{27,})$', path.stem)[1],
            'call_line': line_number, 'turn_context_line': context_line,
            'timestamp': row['timestamp'], 'model': context.get('model'),
            'reasoning_effort': context.get('effort'),
            'tool': payload['name'], 'purpose': requested[line_number],
            'command_sha256': hashlib.sha256(command.encode()).hexdigest(),
        })
    assert len(evidence) == len(requested)
    return evidence, commands

evidence1, commands1 = session_evidence(S1, {
    302: 'Author MTH 255 OHW-1, OHW-2, OHW-3 local quiz answers and feedback in /tmp/achieve-import/build.py.',
    393: 'Author MTH 255 WHW-1 local quiz answers and feedback in /tmp/mth255-whw1/build.py.',
    973: 'Author MTH 341 WHW-1 local quiz answers, feedback, and reference graphs in /tmp/author_mth341_whw1.py.',
    1619: 'Add MTH 255 OHW-1 Math Academy study links.',
    1871: 'Author MTH 255 R-1 and MTH 256 R-1, OHW-1, WHW-1 local answers and feedback in /tmp/f26-quality/author.py.',
    1929: 'Author or refine Math Academy mappings for the first nine assignments in /tmp/f26-quality/match.py.',
    1975: 'Correct authored MTH 255 OHW-3 Q8 key and option-specific feedback.',
    1988: 'Generate authored MTH 255 WHW-1 and MTH 256 WHW-1 reference graphs in /tmp/f26-quality/plots.py.',
    2015: 'Adjust authored graph labels and regenerate reference graphs.',
})
evidence2, commands2 = session_evidence(S2, {
    73: 'Write common importer helpers and author MTH 255 R-2 local answers, feedback and mappings in /tmp/ingest255/r2.py.',
    132: 'Author MTH 255 WHW-2 local answers, feedback and mappings in /tmp/ingest255/whw2.py; generate authored radial and tangential reference graphics.',
    293: 'Author MTH 255 OHW-4 local answers, feedback and mappings in /tmp/ingest255/ohw4.py.',
    348: 'Author MTH 255 OHW-5 local answers, feedback and mappings in /tmp/ingest255/ohw5.py.',
    402: 'Author MTH 255 OHW-6 local answers, feedback and mappings in /tmp/ingest255/ohw6.py.',
    437: 'Author MTH 255 OHW-7 local answers, feedback and mappings in /tmp/ingest255/ohw7.py.',
    498: 'Author MTH 255 OHW-8 local answers, feedback and mappings in /tmp/ingest255/ohw8.py.',
    564: 'Author MTH 255 OHW-9 local answers, feedback and mappings in /tmp/ingest255/ohw9.py.',
    648: 'Author MTH 255 OHW-10 local answers, feedback and mappings in /tmp/ingest255/ohw10.py.',
    697: 'Author MTH 255 OHW-11 local answers, feedback and mappings in /tmp/ingest255/ohw11.py.',
})
assert all(e['model'] == 'gpt-6-astra' and e['reasoning_effort'] == 'high' for e in evidence1+evidence2)

refresh = read(ROOT/'f26-refresh/refresh-audit.json')['source_audit']
remaining = read(ROOT/'f26-remaining-2026-10-07/audit.json')
activities = refresh['activities'] + remaining['activities']
entities = read(ROOT/'f26-refresh/entities.json') + read(ROOT/'f26-remaining-2026-10-07/entities.json')
full = {e[':db/id']: e for e in entities}
assert len(full) == len(entities) == 1289
due = read(ROOT/'f26-due-correction-2026-10-07/commit-intent.json')['changes']
for change in due:
    activity = full[change['activity_id']]
    activity[':activity/due'] = {'$inst': change['instant']}
    intro = full[full[activity[':activity/first-step']][':step/content']]
    assert 'Due: unknown' in intro[':tutorial/content']
    intro[':tutorial/content'] = intro[':tutorial/content'].replace('Due: unknown', 'Due: '+change['date'])

# The author script explicitly appends these response labels after the original
# source prompt. Parse only literal dictionaries; never execute saved tool code.
author_script = commands1[1871].split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
author_dicts = {}
for node in ast.parse(author_script).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('R255','R256','O256','W256'):
        author_dicts[node.targets[0].id] = ast.literal_eval(node.value)
dict_for_source = {
    'F26/255/09-29-26_R-1.md': 'R255',
    'F26/256/09-29-26_R-1.md': 'R256',
    'F26/256/10-02-26_OHW-1.md': 'O256',
    'F26/256/10-02-26_WHW-1.md': 'W256',
}
qmeta = {q['question_id']: {'source': a['source'], 'quiz': q, 'activity_id': a['activity_id'], 'problem': p['number']}
         for a in activities for p in a['problems'] for q in p['quizzes']}

original, additions, transforms = [], [], []
for entity in entities:
    uid = entity[':db/id']
    if ':answer/id' in entity or ':answer-field/id' in entity:
        additions.append(copy.deepcopy(entity))
        continue
    base = copy.deepcopy(entity)
    patch = {k: copy.deepcopy(v) for k,v in entity.items() if k == ':db/id' or k.endswith('/id') or k == ':db/ensure'}
    if ':question/id' in entity:
        patch[':question/worked-solution'] = base.pop(':question/worked-solution')
        fields = base.pop(':question/answer-fields', [])
        if fields:
            patch[':question/answer-fields'] = fields
        prompt = entity[':question/problem']
        actions = []
        qm = qmeta[uid]
        if qm['source'] in dict_for_source:
            answer, feedback, free = author_dicts[dict_for_source[qm['source']]][qm['quiz']['quiz_id'].removeprefix('q-')]
            if not free:
                answer = answer.replace('\\n', '\n')
                i = iter(range(1, 100))
                suffix = re.sub(r'==(.+?)==', lambda _: '{{field-'+str(next(i))+'}}', answer, flags=re.S)
                assert prompt.endswith(suffix), (uid, suffix, prompt)
                prompt = prompt[:-len(suffix)].rstrip()
                actions.append({'kind': 'remove_verified_authored_response_label', 'removed': suffix})
        # Keep source tasks and neutral response blanks; remove no mathematical
        # premise, choice, or shared context. No correct answers enter this layer.
        if '{{' in prompt:
            prompt = re.sub(r'\{\{[^}]+\}\}', '____', prompt)
            actions.append({'kind': 'render_unfilled_response_slots'})
        for field_id in fields:
            field = full[field_id]
            if field[':answer-field/type'] == ':answer-field.type/blank':
                continue
            choices = []
            for index, choice_id in enumerate(field[':answer-field/choices'], 1):
                choice = full[choice_id]
                value = choice[':answer/value']
                if choice[':answer/type'] == ':answer.type/image':
                    value = f'![Choice {index}]({value})'
                elif choice[':answer/type'] == ':answer.type/math':
                    value = '$'+value+'$'
                choices.append(f'{index}. {value}')
            prompt += '\n\n'+'\n\n'.join(choices)
            actions.append({'kind': 'render_source_choices_without_answer_key', 'field_id': field_id,
                            'choice_ids': field[':answer-field/choices']})
        if prompt != entity[':question/problem']:
            base[':question/problem'] = prompt
            patch[':question/problem'] = entity[':question/problem']
            transforms.append({'question_id': uid, 'source': qm['source'], 'quiz_id': qm['quiz']['quiz_id'], 'actions': actions})
    elif ':assigned-problem/id' in entity and ':assigned-problem/topic-coverage' in base:
        patch[':assigned-problem/topic-coverage'] = base.pop(':assigned-problem/topic-coverage')
    elif ':tutorial/id' in entity:
        content = base[':tutorial/content']
        cleaned = re.sub(r'(?:\n\n)?Study answers[^\n]*', '', content).strip()
        if cleaned != content:
            base[':tutorial/content'] = cleaned
            patch[':tutorial/content'] = content
    original.append(base)
    if set(patch)-{':db/id', ':db/ensure'}-{k for k in patch if k.endswith('/id')}:
        additions.append(patch)

merged = {e[':db/id']: copy.deepcopy(e) for e in original}
for row in additions:
    merged.setdefault(row[':db/id'], {}).update(row)
assert merged == full, 'Two-layer merge must exactly restore the saved graph plus due corrections.'
assert all(not any(k in e for k in (':question/worked-solution', ':question/answer-fields', ':answer-field/correct', ':assigned-problem/topic-coverage')) for e in original)
assert not any(':answer/id' in e or ':answer-field/id' in e for e in original)
assert not any('{{' in e.get(':question/problem','') for e in original)
assert len({e[':db/id'] for e in original}) == len(original)
assert len({e[':db/id'] for e in additions}) == len(additions)

assets = refresh['assets'] + remaining['assets']
for asset in assets:
    assert Path(asset['path']).is_file() and sha(Path(asset['path'])) == asset['sha256']

def counts(rows):
    return dict(collections.Counter(next(k[1:-3] for k in e if k.endswith('/id') and k != ':db/id') for e in rows))

author_rows = []
for a in activities:
    source = a['source']
    if a in refresh['activities']:
        session = str(S1)
        if source in dict_for_source: lines = [1871]
        elif '/341/' in source: lines = [973]
        elif source.endswith('_WHW-1.md'): lines = [393]
        else: lines = [302]
        lines += [1619 if source.endswith('/10-01-26_OHW-1.md') else 1929]
    else:
        session = str(S2)
        suffix = Path(source).stem.split('_',1)[1]
        lines = [{'OHW-4':293,'OHW-5':348,'OHW-6':402,'OHW-7':437,'OHW-8':498,'OHW-9':564,'OHW-10':648,'OHW-11':697,'R-2':73,'WHW-2':132}[suffix]]
    author_rows.append({'activity_id': a['activity_id'], 'source': source, 'model':'gpt-6-astra', 'reasoning_effort':'high',
                        'session_path':session, 'authoring_call_lines':lines,
                        'question_ids':[q['question_id'] for p in a['problems'] for q in p['quizzes']],
                        'assigned_problem_ids':[p['assigned_problem_id'] for p in a['problems']]})

write('assignments-original.json', original)
write('assignments-additions.json', additions)
write('assignments-merged-reference.json', entities)
write('assignment-layer-audit.json', {
    'original_counts': counts(original), 'addition_counts': counts(additions), 'merged_counts': counts(entities),
    'original_maps':len(original),'addition_maps':len(additions),'merged_entities':len(entities),
    'activities': [{k:v for k,v in a.items() if k != 'problems'} | {'assigned_problems':len(a['problems']), 'questions':sum(len(p['quizzes']) for p in a['problems'])} for a in activities],
    'due_corrections':due,'transforms':transforms,'assets':assets,
    'verified': {'merge_equals_saved_graph_plus_due_corrections':True,'all_assets_match_saved_sha256':True,
                 'original_has_no_answer_key_or_solution_or_coverage':True,'source_questions_preserve_stable_ids':True},
    'limitations':[
        'Original layer is the saved local transcription of source assignment tasks, not an assertion of verbatim source wording. Introductory instructions are locally condensed source instructions.',
        'Unfilled response slots and ordered choice lists are display-only adaptations. The later layer restores the old interactive response markup.',
        'All original assignment URLs and PDF references are retained. Publisher choice content is retained without marking correct choices.',
        'Actual PDF/publisher authorship differs from OSU course assignment provenance; OSU attribution must not imply OSU authored Macmillan or Lyryx material.',
        'No runtime grading promise is made. Old free responses are reference-only; the old grading limitations remain in the original audit files.',
        'Current vault files were not regenerated: nine first-batch notes were later converted to another quiz field representation, which changes 186 field/answer identities.',
    ]})
write('author-evidence.json', {
    'author': {'model':'gpt-6-astra','reasoning_effort':'high','role':'Author of local answers, solutions, feedback, Math Academy mappings, and reference graphics'},
    'method':'Read saved Codex tool-call records that wrote authoring scripts; associate each exact writing call with its preceding turn_context model and effort. Do not execute historical commands.',
    'writing_calls':evidence1+evidence2,'assignments':author_rows,
    'distinction':'gpt-6.1-sol imported the remaining content into the old EDB on Oct 7; that import does not establish original study-content authorship.',
    'git_evidence':'All 19 current assignment Markdown files are untracked in the study repository. Existing JP git authorship does not identify the author of these additions.',
    'publisher_manifest_paths':[str(Path('/home/jake/Developer/study/vault/F26/source/255')/f'OHW-{n}'/'source-manifest.json') for n in (1,2,3)],
    'publisher_manifest_answer_provenance':'Answers and feedback independently derived for local practice; no answers entered or submitted in Achieve.',
    'known_authored_solution_images':[a for a in assets if any(a['path'] in unquote(e.get(':question/worked-solution','')) for e in entities)],
    'due_correction_evidence':{
        'session_path':'/home/jake/.codex/sessions/2026/10/07/rollout-2026-10-07T00-28-43-01a11543-bdd9-74f0-bff1-b1a7657539ef.jsonl',
        'line':239,'role':'user','text':'255 WHW 2 is due 10/08 and 255 R2 was due 10/6',
        'interpretation':'User-confirmed due dates; the PDFs themselves do not state these deadlines.'},
    'unresolved':[],
})
print(json.dumps({'original':len(original),'additions':len(additions),'full':len(entities),'author':'gpt-6-astra high','transforms':len(transforms)},indent=2))
