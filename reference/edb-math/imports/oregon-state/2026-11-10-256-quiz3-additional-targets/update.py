"""Add the three user-requested study topics to the existing Quiz 3 assignment."""
import collections
import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from migrate_learner_history import connection, dumps, kw, loads

ACTIVITY = 17592186755207
SOURCE = ':course-academy.source/editor'
TITLES = ['Reduction of Order', 'General Solutions of First-Order Linear ODEs',
          'General Solutions of Linear ODEs']
PATTERN = '''[:db/id :activity/id :activity/title :activity/due :activity/course
 :activity/type :activity/first-step
 {[:activity/steps :limit nil] [:db/id :step/id :step/next
  {:step/content [:db/id :tutorial/id :tutorial/title :tutorial/content
   :assigned-problem/id
   {:assigned-problem/topic-coverage [:db/id :topic/id :topic/title]}
   {:assigned-problem/content [:db/id :question/id :question/problem]}]}]}]'''


def save(name, value):
    (HERE / name).write_text(json.dumps(value, default=str, indent=2) + '\n')


def ordered(activity):
    steps = {s[':db/id']: s for s in activity[':activity/steps']}
    cursor = activity[':activity/first-step'][':db/id']
    result = []
    while cursor is not None:
        assert cursor not in {s[':db/id'] for s in result}, 'Cycle in assignment'
        step = steps[cursor]
        result.append(step)
        cursor = step.get(':step/next', {}).get(':db/id')
    assert len(result) == len(steps), 'Unreachable assignment steps'
    return result


def read_activity(db, name, basis):
    rows = db.query('[:find (pull ?a ' + PATTERN + ') :in $ ?a :where [?a :activity/id _]]',
                    [ACTIVITY], HERE, name, basis)
    assert len(rows) == 1
    return rows[0][0]


def prepare():
    assert not (HERE / 'intent.json').exists(), 'Recover existing intent instead'
    db = connection()
    basis = db.basis()
    activity = read_activity(db, 'assignment-before', basis)
    steps = ordered(activity)
    topics = db.query('''[:find ?title (pull ?t [:db/id :topic/id :topic/title])
      :in $ [?title ...] :where [?t :topic/title ?title]]''', [TITLES], HERE,
      'additional-topics', basis)
    assert len(topics) == len(TITLES)
    bytitle = {title: topic for title, topic in topics}
    assert set(bytitle) == set(TITLES)
    edges = db.query('[:find ?a ?b :where [?a :topic/next ?b]]', [], HERE, 'edges', basis)
    incoming, outgoing = collections.defaultdict(set), collections.defaultdict(set)
    for a, b in edges:
        incoming[b].add(a)
        outgoing[a].add(b)
    nodes = set(incoming) | set(outgoing)
    degree = {n: len(incoming[n]) for n in nodes}
    layers = {n: 0 for n in nodes}
    todo = [n for n in nodes if degree[n] == 0]
    for n in todo:
        for nxt in outgoing[n]:
            layers[nxt] = max(layers[nxt], layers[n] + 1)
            degree[nxt] -= 1
            if degree[nxt] == 0:
                todo.append(nxt)
    assert len(todo) == len(nodes), 'Topic graph has a cycle'
    oldtopicsteps = {}
    topicrecords = {}
    for step in steps[1:]:
        coverage = step[':step/content'][':assigned-problem/topic-coverage']
        assert len(coverage) == 1
        topic = coverage[0]
        eid = topic[':db/id']
        assert eid not in oldtopicsteps
        oldtopicsteps[eid] = step[':db/id']
        topicrecords[eid] = topic
    assert len(oldtopicsteps) == 105
    for topic in bytitle.values():
        assert topic[':db/id'] not in oldtopicsteps, 'Requested topic already present'
        topicrecords[topic[':db/id']] = topic
    key = lambda eid: (layers.get(eid, 0), topicrecords[eid][':topic/title'], eid)
    original = [s[':step/content'][':assigned-problem/topic-coverage'][0][':db/id']
                for s in steps[1:]]
    assert original == sorted(original, key=key), 'Existing ordering needs separate review'
    combined = sorted(topicrecords, key=key)
    forms = []
    newsteps = {}

    def identity(eid, kind):
        return uuid.uuid5(uuid.NAMESPACE_URL,
            f'course-academy/256/quiz3-preparation/2026-11-10/topic/{eid}/{kind}')

    for title in TITLES:
        topic = bytitle[title]
        eid = topic[':db/id']
        qid, pid, sid = (identity(eid, kind) for kind in ('prompt', 'assigned', 'step'))
        newsteps[eid] = str(sid)
        prompt = (f'Study or review **{title}**.\n\nGlobal layer: **L{layers.get(eid, 0)+1:02d}**.'
                  f'\n\n[Open topic](/topic?topic={topic[":topic/id"]})')
        forms.extend([
            {kw('db/id'): str(qid), kw('question/id'): qid,
             kw('question/problem'): prompt, kw('db/ensure'): kw('question/validate')},
            {kw('db/id'): str(pid), kw('assigned-problem/id'): pid,
             kw('assigned-problem/content'): str(qid),
             kw('assigned-problem/topic-coverage'): [eid],
             kw('db/ensure'): kw('assigned-problem/validate')},
            {kw('db/id'): str(sid), kw('step/id'): sid,
             kw('step/content'): str(pid), kw('db/ensure'): kw('step/validate')},
        ])
    stepids = {**oldtopicsteps, **newsteps}
    route = [steps[0][':db/id']] + [stepids[eid] for eid in combined]
    existing = {s[':db/id']: s for s in steps}
    for index, sid in enumerate(route):
        nxt = route[index+1] if index+1 < len(route) else None
        if sid in existing:
            old = existing[sid].get(':step/next', {}).get(':db/id')
            if old != nxt:
                forms.append([kw('db/cas'), sid, kw('step/next'), old, nxt])
        elif nxt is not None:
            next(f for f in forms if isinstance(f, dict) and f.get(':db/id') == sid)[kw('step/next')] = nxt
    forms.append({kw('db/id'): ACTIVITY, kw('activity/steps'): list(newsteps.values()),
                  kw('db/ensure'): kw('activity/validate')})
    intro = steps[0][':step/content']
    oldtext = intro[':tutorial/content']
    assert 'All 105 topics are included in global layer order' in oldtext
    newtext = oldtext.replace('All 105 topics are included in global layer order',
        'The study scope also includes Reduction of Order, General Solutions of First-Order '
        'Linear ODEs, and General Solutions of Linear ODEs. All 108 topics are included in global layer order')
    forms.append([kw('db/cas'), intro[':db/id'], kw('tutorial/content'), oldtext, newtext])
    payload = dumps(forms) + '\n'
    (HERE / 'transaction.edn').write_text(payload)
    digest = hashlib.sha256(payload.encode()).hexdigest()
    audit = {'basis': basis, 'activity': ACTIVITY, 'source': SOURCE, 'sha256': digest,
             'old_topic_ids': original, 'new_topic_ids': combined,
             'additional_topics': [{'entity': t[':db/id'], 'title': title,
                                   'layer': layers.get(t[':db/id'], 0)+1}
                                  for title, t in bytitle.items()],
             'original_steps': [s[':db/id'] for s in steps],
             'new_steps': newsteps, 'intro_entity': intro[':db/id'], 'intro_text': newtext}
    save('audit.json', audit)
    print(json.dumps({k: audit[k] for k in ('basis', 'additional_topics', 'sha256')}, indent=2))


def preview():
    db = connection()
    audit = json.loads((HERE / 'audit.json').read_text())
    result = db.command('with', '--source', SOURCE, '--file', HERE / 'transaction.edn')
    (HERE / 'preview.edn').write_text(result)
    report = loads(result)
    assert report[':edb/committed'] is False
    assert report[':edb/db-before-t'] == audit['basis'], 'Refresh before committing changed database'
    print(json.dumps({'preview_passed': True, 'basis': audit['basis'],
                      'datoms': len(report[':edb/tx-data'])}))


def apply():
    db = connection()
    audit = json.loads((HERE / 'audit.json').read_text())
    digest = hashlib.sha256((HERE / 'transaction.edn').read_bytes()).hexdigest()
    assert digest == audit['sha256']
    preview = loads((HERE / 'preview.edn').read_text())
    assert preview[':edb/committed'] is False and preview[':edb/db-before-t'] == audit['basis']
    intentpath = HERE / 'intent.json'
    if intentpath.exists():
        intent = json.loads(intentpath.read_text())
        assert intent['sha256'] == digest
    else:
        intent = {'database': 'math', 'source': SOURCE, 'basis': audit['basis'],
                  'endpoint': '/tmp/edb-math/writer.sock', 'sha256': digest,
                  'file': str(HERE / 'transaction.edn'),
                  'request_key': 'mth256-quiz3-add-topics-' + digest[:24] + '-b' + str(audit['basis'])}
        save('intent.json', intent)
    receipt = None
    if (HERE / 'receipt.edn').exists():
        try:
            receipt = loads((HERE / 'receipt.edn').read_text())
        except (ValueError, IndexError):
            pass
    if not isinstance(receipt, dict) or receipt.get(':edb/committed') is not True:
        command = [db.args.edb_bin, 'transact', '--database', intent['database'],
                   '--source', intent['source'], '--file', intent['file'],
                   '--endpoint', intent['endpoint'], '--request-key', intent['request_key'],
                   '--basis', str(intent['basis']), '--timeout-ms', '120000']
        with (HERE / 'receipt.edn').open('w') as out, (HERE / 'submit.stderr').open('w') as err:
            subprocess.run(command, env=db.env, stdout=out, stderr=err, timeout=160, check=True)
        receipt = loads((HERE / 'receipt.edn').read_text())
    assert receipt[':edb/committed'] is True
    basis = receipt[':edb/db-after-t']
    activity = read_activity(db, 'assignment-after', basis)
    before = loads((HERE / 'assignment-before.edn').read_text())[0][0]
    for attribute in (':activity/id', ':activity/title', ':activity/due', ':activity/course',
                      ':activity/type', ':activity/first-step'):
        assert activity[attribute] == before[attribute]
    steps = ordered(activity)
    covered = [s[':step/content'][':assigned-problem/topic-coverage'][0][':db/id']
               for s in steps[1:]]
    assert covered == audit['new_topic_ids'] and len(covered) == len(set(covered)) == 108
    assert [s[':db/id'] for s in steps if s[':db/id'] in audit['original_steps']] == audit['original_steps']
    assert steps[0][':step/content'][':tutorial/content'] == audit['intro_text']
    assert all(s[':step/content'][':assigned-problem/content'][':question/problem']
               for s in steps[1:])
    beforesteps = {s[':db/id']: s for s in ordered(before)[1:]}
    for step in steps[1:]:
        if step[':db/id'] in beforesteps:
            assert step[':step/content'] == beforesteps[step[':db/id']][':step/content']
    attrs = {r[0]: r[1] for r in db.query('[:find ?a ?ident :where [?a :db/ident ?ident]]',
                                       [], HERE, 'attributes-after', basis)}
    newids = set(receipt[':edb/tempids'].values())
    txids = {d[3] for d in receipt[':edb/tx-data']}
    allowed = {(ACTIVITY, ':activity/steps'), (audit['intro_entity'], ':tutorial/content')}
    allowed.update((sid, ':step/next') for sid in audit['original_steps'])
    for datom in receipt[':edb/tx-data']:
        if datom[0] not in newids | txids:
            assert (datom[0], attrs[datom[1]]) in allowed, datom
    verification = {'committed': True, 'basis': basis, 'activity': ACTIVITY,
                    'topics': len(covered), 'ordered_steps': len(steps),
                    'added_topics': TITLES, 'original_content_and_order_preserved': True,
                    'only_assignment_content_changed': True, 'request_key': intent['request_key']}
    save('verification.json', verification)
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    {'prepare': prepare, 'preview': preview, 'apply': apply}[sys.argv[1]]()
