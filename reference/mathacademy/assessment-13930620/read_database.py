"""Read existing questions and resolve exact topic-scoped KP identities; never transact."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[2] / 'scripts/question_capture'))
from edn import dumps, loads

env = os.environ.copy()
env.setdefault('EDB_POSTGRES_URL', 'host=/home/jake/Developer/Course_Academy/.local/edb/run dbname=course_academy user=edb_peer sslmode=disable')
binary = '/home/jake/Developer/EDB/target/release/edb'
out = ROOT / 'database'
out.mkdir(exist_ok=True)


def command(cmd, *args):
    return subprocess.run([binary, cmd, '--database', 'course-academy-v2', *map(str, args)],
                          env=env, check=True, capture_output=True, text=True, timeout=90).stdout


status = command('status')
(out / 'status.txt').write_text(status)
basis = int(re.search(r'\bbasis_t=(\d+)', status)[1])


def query(name, source, inputs):
    qfile, ifile = out / (name + '-query.edn'), out / (name + '-inputs.edn')
    qfile.write_text(source)
    ifile.write_text(dumps(inputs))
    raw = command('query', '--file', qfile, '--inputs', ifile, '--as-of', basis)
    (out / (name + '.edn')).write_text(raw)
    return loads(raw)


content = json.loads((ROOT / 'content.json').read_text())
topics = query('topics', '''[:find (pull ?t [:topic/math-academy-id :topic/title
 {:topic/knowledge-points [:knowledge-point/id :knowledge-point/title]}])
 :in $ [?mid ...] :where [?t :topic/math-academy-id ?mid]]''',
               [sorted({q['topic_id'] for q in content['questions']})])
existing = query('questions', '''[:find (pull ?q [* {:question/difficulty [:db/ident]}
 {:knowledge-point/_questions [:knowledge-point/id :knowledge-point/title]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}])
 :in $ [?mid ...] :where [?q :question/math-academy-id ?mid]]''',
                 [[q['math_academy_id'] for q in content['questions']]])
topic_map = {row[0][':topic/math-academy-id']: row[0] for row in topics}
question_map = {row[0][':question/math-academy-id']: row[0] for row in existing}
for q in content['questions']:
    candidates = [kp for kp in topic_map[q['topic_id']][':topic/knowledge-points']
                  if kp[':knowledge-point/title'] == q['knowledge_point']]
    assert len(candidates) == 1, q['math_academy_id']
    q['knowledge_point_id'] = str(candidates[0][':knowledge-point/id'])
    q['database_match_at_capture'] = q['math_academy_id'] in question_map
content['database_read_basis'] = basis
(ROOT / 'content.json').write_text(json.dumps(content, indent=2) + '\n')
report = {'basis': basis, 'existing_ids': sorted(question_map),
          'new_ids': sorted(q['math_academy_id'] for q in content['questions'] if not q['database_match_at_capture']),
          'resolved_kps': 8, 'database_committed': False}
(out / 'matching.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
