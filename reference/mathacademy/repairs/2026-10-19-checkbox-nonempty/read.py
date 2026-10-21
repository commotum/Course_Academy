"""Capture reported questions and the current registered generator inventory."""
import json
import threading
import subprocess
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient, QUESTION_PULL
from capture.scripts.database.edn import dumps, loads

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DB = EDBClient(Config(), threading.Event())

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')

if __name__ == '__main__':
    identity = DB.status()
    save('identity.json', identity)
    questions = []
    for eid in (17592186561248, 17592186272199):
        rows = DB.query('[:find (pull ?q ' + QUESTION_PULL + ') :in $ ?q :where [?q :question/id _]]',
                        [eid], HERE / 'evidence', 'reported-' + str(eid), identity['basis'])
        questions.append(rows[0][0])
    save('reported-questions.json', questions)
    registry = DB.query('''[:find ?kp ?g ?script :where
        [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?script]]''',
        [], HERE / 'evidence', 'registry', identity['basis'])
    save('registry.json', registry)
    fields = DB.query('''[:find ?f :where [?f :answer-field/type :answer-field.type/checkbox]]''',
                      [], HERE / 'evidence', 'checkbox-fields', identity['basis'])
    ids = sorted({row[0] for row in fields})
    directory = HERE / 'field-census'
    directory.mkdir(exist_ok=True)
    pattern = '''[:db/id :answer-field/key {:answer-field/correct [:db/id :answer/value]}
        {[:question/_answer-fields :limit nil] [:db/id]}]'''
    groups = [('fields-' + str(i), pattern, ids[i:i+500]) for i in range(0, len(ids), 500)]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    reader = ROOT / 'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'
    run = subprocess.run([str(reader), str(directory), str(identity['basis'])], env=DB.environment,
                         capture_output=True, text=True, timeout=240)
    (directory / 'read.stderr').write_text(run.stderr)
    run.check_returncode()
    fields = [field for name, _, _ in groups for field in loads((directory / (name + '.edn')).read_text())]
    save('checkbox-fields.json', fields)
    print(json.dumps({'identity': identity, 'generators': len(registry), 'checkbox_fields': len(fields)}))
