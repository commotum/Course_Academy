#!/usr/bin/env python3
"""Prepare the five October 12 assignments. No durable database writes.

Reuse canonical conversion and deterministic identities, but retain the newly
supported free fields and resolve verified file links into the study repository.
The source, authored study content, and learner enrollment are separate requests.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
import threading
import uuid
from urllib.parse import unquote, urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from f26_assignment_content import Builder
from import_school_assignments import VAULT, DEFAULT_LEARNER
from question_markers import repair_problem
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import kw, Keyword, Tagged, dumps
from scripts.database.images import ImageLibrary

FILES = [
    'F26/255/10-15-26_R-3.md', 'F26/255/10-15-26_WHW-3.md',
    'F26/256/10-14-26_R-3.md', 'F26/256/10-16-26_WHW-2.md',
    'F26/341/10-14-26_WHW-2.md',
]

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

class CurrentBuilder(Builder):
    def local_link(self, target, source):
        parsed = urlsplit(target)
        if parsed.scheme == 'file':
            path = Path(unquote(parsed.path)).resolve()
            if parsed.netloc or not path.is_relative_to(VAULT.parent / 'MA') or not path.is_file() or path.suffix != '.md':
                raise ValueError(f'Unverified study lesson link: {target}')
            return path, parsed
        return super().local_link(target, source)

    def canonical_question(self, source, key, quiz, path, context=''):
        # Use the existing canonical answer conversion. Free references have
        # the same owned bank shape, but never assert correctness at runtime.
        converted = copy.deepcopy(quiz)
        free = {f['key'] for f in converted['fields'] if f['type'] == 'free'}
        for field in converted['fields']:
            if field['key'] in free:
                field['type'] = 'blank'
        uid, audit = super().canonical_question(source, key, converted, path, context)
        for field in audit['fields']:
            if field['key'] in free:
                field['type'] = 'free'
                row = next(r for r in self.entities if r[':db/id'] == field['field_id'])
                row[':answer-field/type'] = ':answer-field.type/free'
        question = next(r for r in self.entities if r[':db/id'] == uid)
        answer_fields = [r for r in self.entities if r[':db/id'] in question[':question/answer-fields']]
        question[':question/problem'] = repair_problem(question[':question/problem'], answer_fields)
        return uid, audit

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    b = CurrentBuilder(VAULT)
    activities = [b.assignment(f) for f in FILES]
    b.validate()
    full = copy.deepcopy(b.entities)
    ids = {r[':db/id']: next((k, v) for k, v in r.items() if k.endswith('/id') and k != ':db/id') for r in full}
    config = Config()
    c = EDBClient(config, threading.Event())
    dbdir = OUT / 'db'
    dbdir.mkdir(parents=True, exist_ok=True)
    identity = c.status()
    basis = identity['basis']
    save('db/identity.json', identity)

    def query(name, text, args):
        return c.query(text, args, dbdir, name, basis)

    attrs = query('attributes', '''[:find ?a ?ident ?typ ?card :where
      [?a :db/ident ?ident] [?a :db/valueType ?t] [?t :db/ident ?typ]
      [?a :db/cardinality ?c] [?c :db/ident ?card]]''', [])
    schema = {str(name): (eid, str(typ), str(card)) for eid, name, typ, card in attrs}
    references = {v for r in full for k, v in r.items() if isinstance(v, str) and v.startswith(':')}
    references |= {':org/Oregon-State', ':agent/gpt-6.1-sol-high', ':person/jake'}
    enums = query('idents', '[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]', [[kw(x) for x in sorted(references)]])
    found = {str(name) for _, name in enums}
    assert references <= found, references - found
    pairs = [[kw(a), uuid.UUID(v['$uuid'])] for a, v in ids.values()]
    existing = query('candidate-identities', '''[:find ?e ?attr ?id :in $ [[?attr ?id]] :where [?e ?attr ?id]]''', [pairs])
    assert not existing, 'Selected content already exists; reconcile explicitly instead of replacing it.'
    topic_ids = sorted({t for a in b.audit['activities'] for p in a['problems'] for t in p['topics']})
    topics = query('topics', '[:find ?e ?mid ?id :in $ [?mid ...] :where [?e :topic/math-academy-id ?mid] [?e :topic/id ?id]]', [topic_ids])
    assert {mid for _, mid, _ in topics} == set(topic_ids), 'Unresolved coverage topics'
    courses = sorted({r[':activity/course']['$ref'][1]['$uuid'] for r in full if ':activity/course' in r})
    course_rows = query('courses', '[:find ?e ?id :in $ [?id ...] :where [?e :course/id ?id]]', [[uuid.UUID(x) for x in courses]])
    assert {str(uid) for _, uid in course_rows} == set(courses)
    learners = query('learner', '''[:find (pull ?l [:db/id :learner/id
      {[:learner/assignments :limit nil] [:db/id]}
      {[:learner/targets :limit nil] [:db/id]}])
      :in $ ?id :where [?l :learner/id ?id]]''', [DEFAULT_LEARNER])
    assert len(learners) == 1
    learner = learners[0][0]
    assigned = {v[':db/id'] for v in learner.get(':learner/assignments', [])}
    targets = {v[':db/id'] for v in learner.get(':learner/targets', [])}

    # Original images and authored diagrams are staged by hash, never installed
    # into the live image library by this preparation command.
    images = ImageLibrary(OUT / 'assets', OUT)
    def localize(value):
        def replace(m):
            path = Path(parse_qs(urlsplit(m[0]).query)['path'][0])
            relative = images.store(path.read_bytes(), str(path))
            return relative
        return images.text(re.sub(r'/api/asset\?path=[^\s)"<>]+', replace, value))
    def convert(value, attr=''):
        if isinstance(value, dict):
            if '$uuid' in value: return uuid.UUID(value['$uuid'])
            if '$inst' in value: return Tagged('inst', value['$inst'])
            if '$ref' in value: return [kw(value['$ref'][0]), convert(value['$ref'][1], value['$ref'][0])]
            return {kw(k): convert(v, k) for k, v in value.items()}
        if isinstance(value, list): return [convert(v, attr) for v in value]
        if isinstance(value, str):
            if attr == ':db/ensure' or schema.get(attr, ('', '', ''))[1] in (':db.type/ref', ':db.type/keyword'):
                return kw(value) if value.startswith(':') else value
            if schema.get(attr, ('', '', ''))[1] == ':db.type/string': return localize(value)
        return value

    original, authored, transformations = [], [], []
    for r in full:
        uid = r[':db/id']
        if ':answer/id' in r or ':answer-field/id' in r:
            authored.append(r)
            continue
        base = copy.deepcopy(r)
        patch = {':db/id': {'$ref': list(ids[uid])}, ':db/ensure': r[':db/ensure']}
        for attr in (':question/worked-solution', ':question/answer-fields', ':assigned-problem/topic-coverage'):
            if attr in base: patch[attr] = base.pop(attr)
        if ':question/problem' in base:
            before = base[':question/problem']
            after = re.sub(r'\n\nWritten response: \{\{[^}]+\}\}\s*$', '', before)
            after = re.sub(r'\{\{[^}]+\}\}', '____', after)
            if after != before:
                base[':question/problem'] = after
                patch[':question/problem'] = before
                transformations.append({'id': uid, 'change': 'Move response editors to agent layer; source layer contains unfilled prompts.'})
        if ':tutorial/content' in base:
            before = base[':tutorial/content']
            header = before.split('\n\n## Instructions', 1)[0]
            kept = [line for line in header.splitlines() if line.startswith(('**MTH', 'Due:', 'Due time:', 'Source:', 'Textbook:'))]
            base[':tutorial/content'] = '\n\n'.join(kept)
            if base[':tutorial/content'] != before: patch[':tutorial/content'] = before
        original.append(base)
        if set(patch) - {':db/id', ':db/ensure'}: authored.append(patch)

    # Later-stage refs use installed unique identities, never preview tempids.
    original_ids = {r[':db/id'] for r in original}
    def refs(value):
        if isinstance(value, dict):
            if any(k.startswith('$') for k in value): return value
            return {k: refs(v) for k, v in value.items()}
        if isinstance(value, list): return [refs(v) for v in value]
        if isinstance(value, str) and value in original_ids:
            return {'$ref': list(ids[value])}
        return value
    authored = [refs(r) for r in authored]
    learner_forms = [[kw('db/add'), [kw('learner/id'), DEFAULT_LEARNER], kw('learner/assignments'),
                      [kw('activity/id'), uuid.UUID(ids[a][1]['$uuid'])]] for a in activities]
    added_topics = [(eid, mid, uid) for eid, mid, uid in topics if eid not in targets]
    learner_forms += [[kw('db/add'), [kw('learner/id'), DEFAULT_LEARNER], kw('learner/targets'),
                       [kw('topic/id'), uid]] for _, _, uid in added_topics]
    transactions = []
    for name, source, forms in [('1-assigned-material.edn', ':org/Oregon-State', original),
                                ('2-authored-study-content.edn', ':agent/gpt-6.1-sol-high', authored),
                                ('3-learner-links.edn', ':person/jake', learner_forms)]:
        text = dumps(convert(forms)) + '\n'
        (OUT / name).write_text(text)
        transactions.append({'file': name, 'source': source, 'forms': len(forms),
                             'sha256': hashlib.sha256(text.encode()).hexdigest(),
                             'request_key': 'f26-oct12-' + str(uuid.uuid4())})
    # Fixed output projections query only the prepared entities at db-after.
    (OUT / 'pull-pattern.edn').write_text('[:db/id *]\n')
    (OUT / 'pull-identities.edn').write_text(dumps([[kw(a), uuid.UUID(v['$uuid'])] for a, v in ids.values()]) + '\n')
    b.audit.update({'assets': list(b.assets.values()), 'basis': basis,
                    'selected_sources': FILES, 'added_target_math_academy_ids': [mid for _, mid, _ in added_topics],
                    'response_fields': 'Free fields collect written responses without automatic correctness or mastery evidence.',
                    'image_map': images.saved, 'source_transformations': transformations})
    save('audit.json', b.audit)
    save('entities.json', full)
    save('prepared-manifest.json', {'database': identity['database'], 'lineage': identity['lineage'],
        'basis_read': basis, 'committed': False, 'transactions': transactions,
        'learner_id': DEFAULT_LEARNER, 'existing_assignments': len(assigned),
        'new_assignments': len(activities), 'new_targets': len(added_topics),
        'counts': {kind: sum(':' + kind + '/id' in r for r in full) for kind in
                   ['activity', 'assigned-problem', 'question', 'multistep', 'step', 'tutorial', 'answer-field', 'answer']},
        'sources': 'OSU is the assigning institution. Author references and explanations use the verified writing-session model. Publisher/PDF links remain in content.',
        'policy': 'Add definitions, assignments and their verified coverage targets. Preserve existing assignments, targets, learner history, progress, and engine configuration.'})
    print(json.dumps(json.loads((OUT / 'prepared-manifest.json').read_text()), indent=2))

if __name__ == '__main__': main()
