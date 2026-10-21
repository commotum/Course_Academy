"""Read the lesson's current generator registrations and full question pools."""
import json
import subprocess
import threading
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient, QUESTION_PULL
from capture.scripts.database.edn import dumps, loads
from scripts.generator_packages import materialize_package

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DB = EDBClient(Config(), threading.Event())
KPS = (17592186073776, 17592186073777, 17592186073778)
READ = ROOT / 'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'

def save(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str) + '\n')

def native_read(directory, basis, groups):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    result = subprocess.run([str(READ), str(directory), str(basis)], env=DB.environment,
                            capture_output=True, text=True, timeout=180)
    (directory / 'read.stderr').write_text(result.stderr)
    result.check_returncode()
    return {name: loads((directory / (name + '.edn')).read_text()) for name, _, _ in groups}

if __name__ == '__main__':
    identity = DB.status()
    save('identity.json', identity)
    pattern = '''[:db/id :knowledge-point/id :knowledge-point/title
        {:knowledge-point/question-generator [*]}
        {:knowledge-point/questions [:db/id :question/id]}
        {:knowledge-point/canonical-example [:db/id :question/id]}]'''
    kps = []
    for kp in KPS:
        rows = DB.query('[:find (pull ?kp ' + pattern + ') :in $ ?kp :where [?kp :knowledge-point/id _]]',
                        [kp], HERE / 'evidence', 'kp-' + str(kp), identity['basis'])
        record = rows[0][0]
        kps.append(record)
        ref = record[':knowledge-point/question-generator'][':question-generator/script']
        dest = HERE / 'original-packages' / str(kp)
        if not dest.exists():
            materialize_package(ref, Path(DB.config.math_root), dest)
    save('knowledge-points.json', kps)
    ids = sorted({q[':db/id'] for kp in kps for q in kp.get(':knowledge-point/questions', [])})
    groups = [('questions-' + str(i), QUESTION_PULL, ids[i:i+100]) for i in range(0, len(ids), 100)]
    pulled = native_read(HERE / 'question-pools', identity['basis'], groups)
    questions = [q for group in pulled.values() for q in group]
    save('questions.json', questions)
    print(json.dumps({'identity': identity, 'pool_questions': len(questions),
                      'pool_counts': {kp[':db/id']: len(kp.get(':knowledge-point/questions', [])) for kp in kps}}))
