#!/usr/bin/env python3
"""Package saved graph reconstruction evidence; never write to the database."""
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
IMPORT = ROOT / 'reference/mathacademy/history-question-import-2026-10-04'
OUT = ROOT / 'reference/mathacademy/graph-reconstruction-packages-2026-10-04'
ARCHIVE = Path('/home/jake/Developer/MA/DATA/Lessons')


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, default=str) + '\n')


class Assets:
    def __init__(self, package, topic_id, saved):
        self.package, self.topic_id, self.saved = package, topic_id, saved
        self.copied, self.unavailable = {}, set()

    def resolve(self, reference):
        if reference.startswith('image_assets/') and (self.package / reference).is_file():
            return reference
        if reference in self.copied:
            return self.copied[reference]['path']
        if reference.startswith('data:'):
            return reference
        url = urljoin('https://mathacademy.com', reference)
        source = Path(self.saved.get(url, reference))
        if not source.is_file():
            name = Path(urlparse(reference).path).name
            candidates = [ARCHIVE / str(self.topic_id) / 'Source/Images' / name,
                          ARCHIVE / str(self.topic_id) / 'Source/Images' / (name + '.png')]
            source = next((p for p in candidates if p.is_file()), source)
        if not source.is_file():
            self.unavailable.add(reference)
            return reference
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        name = re.sub(r'[^\w.-]', '-', source.stem) + '-' + digest[:10] + source.suffix
        target = self.package / 'image_assets' / name
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(source, target)
        self.copied[reference] = {'path': target.relative_to(self.package).as_posix(),
                                  'sha256': digest, 'original_reference': reference}
        return self.copied[reference]['path']

    def text(self, value):
        value = re.sub(r'(!\[[^\]]*\]\()([^\n)]+)(\))',
                       lambda m: m[1] + self.resolve(m[2]) + m[3], value)
        return re.sub(r'(\bsrc=["\'])([^"\']+)(["\'])',
                      lambda m: m[1] + self.resolve(m[2]) + m[3], value)

    def tree(self, value):
        if isinstance(value, list):
            return [self.tree(x) for x in value]
        if isinstance(value, dict):
            result = {k: self.tree(v) for k, v in value.items()}
            if result.get('type') == 'image' and isinstance(result.get('value'), str):
                result['value'] = self.resolve(value['value'])
            if isinstance(value.get('correct_value'), str) and any(
                    c.get('type') == 'image' and c.get('value') == value['correct_value']
                    for c in value.get('choices', [])):
                result['correct_value'] = self.resolve(value['correct_value'])
            if value.get(':answer/type', {}).get(':db/ident') == ':answer.type/image':
                result[':answer/value'] = self.resolve(value[':answer/value'])
            return result
        return self.text(value) if isinstance(value, str) else value


def db_record(q, kp_id, title):
    fields = []
    for f in q.get(':question/answer-fields', []):
        fields.append({'key': f[':answer-field/key'],
                       'type': f[':answer-field/type'][':db/ident'].split('/')[-1],
                       'choices': [{'type': a[':answer/type'][':db/ident'].split('/')[-1],
                                    'value': a[':answer/value']} for a in f.get(':answer-field/choices', [])],
                       'correct_value': f.get(':answer-field/correct', {}).get(':answer/value')})
    return {'math_academy_id': q[':question/math-academy-id'], 'knowledge_point_id': kp_id,
            'knowledge_point': title, 'problem': q.get(':question/problem', ''),
            'worked_solution': q.get(':question/worked-solution', ''),
            'difficulty': q.get(':question/difficulty', {}).get(':db/ident', '').split('/')[-1],
            'answer_fields': fields, 'source_kind': 'existing database content'}


def question_md(q, missing=False):
    mid = q['math_academy_id']
    lines = ['## ' + mid + (' — missing answer graph' if missing else ''), '',
             'Source: ' + q.get('source_kind', q.get('provenance', {}).get('source_kind', 'saved history')), '',
             'Difficulty: ' + (q.get('difficulty') or 'not recorded'), '',
             '### Problem', '', q['problem'], '', '### Worked solution', '', q['worked_solution'], '']
    for f in q.get('answer_fields', []):
        lines.extend(['### Answer field `' + f['key'] + '` (' + f['type'] + ')', ''])
        for i, c in enumerate(f.get('choices', []), 1):
            answer = '![](' + c['value'] + ')' if c['type'] == 'image' else '$' + c['value'] + '$' if c['type'] == 'math' else c['value']
            lines.extend([str(i) + '. ' + answer + (' **[stored correct answer]**' if c['value'] == f.get('correct_value') else ''), ''])
        if not f.get('correct_value'):
            lines.extend(['Correct answer key is absent in this saved record.', ''])
    return '\n'.join(lines)


def package():
    export = json.loads((OUT / 'database-export.json').read_text())
    prepared = json.loads((IMPORT / 'prepared.json').read_text())['questions']
    saved = json.loads((IMPORT / 'asset-map.json').read_text())['assets']
    history = json.loads((ROOT / 'reference/mathacademy/progress-history-2026-10-04/observations.json').read_text())
    capture_files = sorted((ROOT / 'reference/mathacademy/question-capture').glob('*/content.json'))
    captures = [(file, json.loads(file.read_text())) for file in capture_files]
    report = []
    for group in export['knowledge_points']:
        tid, kp_id, title = group['topic_id'], group['knowledge_point_id'], group['title']
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        folder = OUT / (str(tid) + '-' + slug)
        folder.mkdir(parents=True, exist_ok=True)
        assets = Assets(folder, tid, saved)
        # The entire source lesson supplies tutorial context, neighboring worked examples, and all original images.
        shutil.copytree(ARCHIVE / str(tid) / 'Source', folder / 'original_lesson', dirs_exist_ok=True)
        schema = folder / 'content_schema'; schema.mkdir(exist_ok=True)
        for name in ['4-question.edn', '5-answer-field.edn', '6-answer.edn']:
            shutil.copy2(ROOT / 'schema/content' / name, schema / name)
        database = assets.tree(group)
        dump(folder / 'database_content.json', database)
        dbq = [assets.tree(db_record(q, kp_id, title)) for q in group['database_questions'].values()]
        observed = [assets.tree(q) for q in prepared if q['knowledge_point_id'] == kp_id]
        raw_questions, observations = [], []
        raw_cache = {}
        for task in history['tasks']:
            for q in task['questions']:
                mid = q['id'].replace('question-', 'q-')
                if mid not in {o['math_academy_id'] for o in observed} and mid not in group['database_questions']:
                    continue
                observations.append({'task_id': task['task-id'], 'activity_type': task['activity-type'],
                                     'history_url': task['url'], 'completed_at': task['completed-at'],
                                     'question': q})
                source = ROOT / task['source_file']
                if source not in raw_cache:
                    raw_cache[source] = {x['id']: x for x in json.loads(source.read_text())['questions']}
                raw = raw_cache[source][q['id']]
                raw_questions.append({'task_id': task['task-id'], **raw})
        dump(folder / 'historical_questions.json', assets.tree(observed))
        dump(folder / 'historical_observations.json', assets.tree(observations))
        dump(folder / 'historical_raw_questions.json', raw_questions)
        # Raw HTML is evidence only; its studentAnswer elements are never treated as answer keys.
        for item in raw_questions:
            path = folder / 'raw_html'; path.mkdir(exist_ok=True)
            html = assets.text(item.get('raw_html', '')).replace('src="image_assets/', 'src="../image_assets/')
            (path / (str(item['task_id']) + '-' + item['id'] + '.html')).write_text(html)
        automated = []
        for file, content in captures:
            matching = [q for q in content.get('questions', []) + content.get('canonical_examples', [])
                        if str(q.get('knowledge_point_id')) == kp_id]
            if matching:
                automated.append({'source_file': str(file.relative_to(ROOT)), 'questions': assets.tree(matching)})
        dump(folder / 'automated_captures.json', automated)
        md = ['# ' + title, '', 'Topic ID: ' + str(tid), '', 'Knowledge-point UUID: `' + kp_id + '`', '',
              'Questions needing reconstruction: ' + ', '.join('`' + i + '`' for i in group['missing']), '',
              '## Existing database examples and questions', '']
        md.extend(question_md(q) for q in sorted(dbq, key=lambda q: q['math_academy_id']))
        md.extend(['## Additional captured historical questions', ''])
        md.extend(question_md(q, q['math_academy_id'] in group['missing']) for q in observed)
        (folder / 'QUESTIONS.md').write_text('\n'.join(md) + '\n')
        missing_text = '\n\n'.join(question_md(q, True) for q in observed if q['math_academy_id'] in group['missing'])
        (folder / 'MISSING_GRAPHS.md').write_text('# Questions needing reconstructed answer graphs\n\n' + missing_text + '\n')
        prompt = f'''Use this ZIP to reconstruct missing graph answer-choice groups for the knowledge point "{title}" (topic {tid}).

Start with MISSING_GRAPHS.md and QUESTIONS.md. Reconstruct these question IDs: {', '.join(group['missing'])}.

Use the saved mathematical problem and worked solution to determine the correct graph. Inspect the canonical example and existing questions, their stored choices, original_lesson/{tid}.pdf, original_lesson/{tid}.json, and image_assets/ for Math Academy's graph conventions. The full lesson is background context; focus on this particular knowledge point. historical_raw_questions.json and raw_html/ contain the original evidence. Ignore studentAnswer and studentAnswerHeader when determining correctness: those contain the learner's submitted answer and can be wrong. A stored database correct answer is explicitly labeled in QUESTIONS.md.

The original choices are missing for the requested IDs. Do not claim to have recovered the exact original distractors. Author a new group of 5 mathematically plausible choices, exactly one correct, matching the response task and the source drawing style. If the evidence cannot determine the original target image, explain the limitation and create an equivalent question with clearly documented prompt changes. In particular, a question asking only for a graph continuous at a given x does not determine a unique original graph; create a valid new choice group satisfying that criterion. Do not invent source facts.

Use Python and Matplotlib to generate the actual diagrams. Preserve equal units where geometrically appropriate, axis arrows/labels, origin, ticks, open/closed endpoints, asymptotes, breaks, periodic boundaries, and transformation coordinates. Keep comparable scales and styling across each group so visual formatting does not reveal the correct choice. Derive distractors from specific likely mathematical mistakes and explain why each is wrong. Verify the equation, domain, roots, vertex, intercepts, orientation, and endpoint inclusion as applicable. For source image coordinates, distinguish observed values from estimates and state uncertainty.

Return a ZIP containing:
- generate_choices.py, with dependencies and a single command that regenerates all output;
- one PNG and one SVG per choice, named <question-id>-choice-1 through -choice-5;
- one labeled choice-group contact sheet per question for review;
- answer_choices.json with records shaped as below;
- reconstruction_notes.md giving derivation, source references, distractor mistakes, and any uncertainty or changed prompt.

JSON contract (paths relative to the returned ZIP):
{{"questions":[{{"math_academy_id":"q-...","problem":"original or explicitly revised prompt","answer_fields":[{{"key":"selection","type":"radio","choices":[{{"type":"image","value":"images/q-...-choice-1.png"}}],"correct_value":"images/q-...-choice-1.png"}}],"reconstructed":true}}]}}
Include all five choices in each choices array. correct_value must exactly equal one of its choice image paths. Do not transact into any database. Provide the artifacts themselves, not just proposed code.
'''
        (folder / 'PROMPT_FOR_CHATGPT_PRO.md').write_text(prompt)
        readme = f'''# Graph reconstruction package

Knowledge point: **{title}**\n\nTopic: {tid}\n\nMissing answer graphs: {', '.join(group['missing'])}

Upload this ZIP to ChatGPT Pro and use PROMPT_FOR_CHATGPT_PRO.md. MISSING_GRAPHS.md gives the work list; QUESTIONS.md presents our existing content and stored answer keys. image_assets/ contains portable copies referenced in the Markdown and normalized JSON. original_lesson/ contains the complete archived source lesson (PDF, HTML, JSON, sections, images), including neighboring skills for context.

The database content was exported read-only at basis {export['basis']}. No learner progress, attempts, or XP were transacted. Historical outcomes and submitted answers remain in the raw source evidence, but are not answer-key authority. The packages distinguish existing database content, historical captures, and reconstructed answers. No reconstructed graphs have been supplied yet.

Original archived HTML may retain external scripts or original image paths; use its accompanying PDF, JSON, or Images/ directory. Normalized question Markdown uses local portable images. assets.json records every copied reference, and manifest.json records SHA-256 checksums for every package file. Unavailable images are listed in assets.json; no missing image has been replaced with guessed content.
'''
        (folder / 'README.md').write_text(readme)
        dump(folder / 'assets.json', {'copied': list(assets.copied.values()), 'unavailable_references': sorted(assets.unavailable)})
        manifest = {'knowledge_point_id': kp_id, 'topic_id': tid, 'title': title, 'missing_graph_questions': group['missing'],
                    'database_basis': export['basis'], 'database_question_count': len(dbq),
                    'historical_question_count': len(observed), 'automated_capture_count': len(automated),
                    'copied_reference_count': len(assets.copied), 'files': []}
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path.name != 'manifest.json':
                manifest['files'].append({'path': path.relative_to(folder).as_posix(), 'bytes': path.stat().st_size,
                                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        dump(folder / 'manifest.json', manifest)
        target = OUT / (folder.name + '.zip')
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
            for path in sorted(folder.rglob('*')):
                if path.is_file(): z.write(path, folder.name + '/' + path.relative_to(folder).as_posix())
        with zipfile.ZipFile(target) as z:
            assert z.testzip() is None
            assert len(z.namelist()) == len(manifest['files']) + 1
        report.append({k: v for k, v in manifest.items() if k != 'files'} | {'zip': str(target), 'zip_bytes': target.stat().st_size,
                        'zip_sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'verified': True})
        print(target.name, len(manifest['files']) + 1, 'files', target.stat().st_size, 'bytes', flush=True)
    dump(OUT / 'package-report.json', report)


if __name__ == '__main__':
    package()
