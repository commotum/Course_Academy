"""Read assessment evidence at one captured EDB basis. No database writes."""
from pathlib import Path
import json, os, re, subprocess, sys
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PREVIOUS = ROOT / 'reference/analysis/question-difficulty-2026-10-11'
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import dumps, loads, Tagged
env = os.environ.copy()
env['EDB_POSTGRES_URL'] = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"
env['EDB_STATEMENT_TIMEOUT_MS'] = '15000'
cli = str(ROOT / '.local/edb/capture-runtime/math-edb')
if (OUT / 'status.txt').exists():
    status = (OUT / 'status.txt').read_text()
else:
    status = subprocess.run([cli, 'status', '--database', 'math'], env=env, capture_output=True, text=True, check=True, timeout=30).stdout
    (OUT / 'status.txt').write_text(status)
basis = int(re.search(r'basis_t=(\d+)', status)[1])
lineage = re.search(r'lineage=([^ ]+)', status)[1]
rows = [json.loads(s) for s in (PREVIOUS / 'source-appearances.jsonl').read_text().splitlines()]
mids = sorted({r['question_mid'] for r in rows if r['activity_type'] == 'assessment'})
queries = {
    'assessment-questions': ('[:find (pull ?q [:db/id :question/math-academy-id {:question/difficulty [:db/ident]}]) :in $ [?mid ...] :where [?q :question/math-academy-id ?mid]]', [mids]),
    'courses': ('[:find (pull ?c [:db/id :course/math-academy-id :course/title :course/code]) :where [?c :course/id _]]', None),
    'course-units': ('[:find ?c ?u :where [?c :course/units ?u]]', None),
    'unit-modules': ('[:find ?u ?m :where [?u :unit/modules ?m]]', None),
    'module-topics': ('[:find ?m ?t :where [?m :module/topics ?t]]', None),
    'topics': ('[:find ?t ?mid ?title :where [?t :topic/math-academy-id ?mid] [?t :topic/title ?title]]', None),
    'knowledge-point-topics': ('[:find ?t ?kp :where [?t :topic/knowledge-points ?kp]]', None),
    'policy': ('[:find (pull ?p [:db/id :policy/id {:policy/question-selection-weights [:db/id {:question-weights/activity-type [:db/ident]} :question-weights/initial-easy :question-weights/initial-moderate :question-weights/initial-hard :question-weights/remedial-easy :question-weights/remedial-moderate :question-weights/remedial-hard]}]) :where [?p :policy/id _]]', None),
}
for name, (query, inputs) in queries.items():
    if (OUT / (name + '.edn')).exists(): continue
    file = OUT / (name + '-query.edn'); file.write_text(query + '\n')
    cmd = [cli, 'query', '--database', 'math', '--as-of', str(basis), '--file', str(file), '--timeout-ms', '60000', '--max-results', '100000', '--max-join-bytes', '134217728', '--max-value-bytes', '268435456']
    if inputs is not None:
        inp = OUT / (name + '-inputs.edn'); inp.write_text(dumps(inputs)); cmd += ['--inputs', str(inp)]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=90)
    if r.returncode: raise RuntimeError(name + ': ' + r.stderr)
    (OUT / (name + '.edn')).write_text(r.stdout)
    print(name, len(loads(r.stdout)), 'rows', flush=True)
# Bind the known owning KPs; searching all incoming question refs is expensive.
qids = {r[0][':db/id'] for r in loads((OUT / 'assessment-questions.edn').read_text())}
kps = sorted({kp for kp, q in loads((PREVIOUS / 'knowledge-questions.edn').read_text()) if q in qids})
query = '[:find ?kp ?q :in $ [?kp ...] :where [?kp :knowledge-point/questions ?q]]'
(OUT / 'assessment-memberships-query.edn').write_text(query + '\n')
(OUT / 'assessment-memberships-inputs.edn').write_text(dumps([[Tagged('edb/ref', kp) for kp in kps]]))
r = subprocess.run([cli, 'query', '--database', 'math', '--as-of', str(basis), '--file', str(OUT / 'assessment-memberships-query.edn'), '--inputs', str(OUT / 'assessment-memberships-inputs.edn'), '--timeout-ms', '60000', '--max-join-bytes', '134217728', '--max-value-bytes', '268435456'], env=env, capture_output=True, text=True, timeout=90)
(OUT / 'assessment-memberships-stderr.txt').write_text(r.stderr)
if r.returncode: raise RuntimeError(r.stderr)
memberships = [[kp, q] for kp, q in loads(r.stdout) if q in qids]
(OUT / 'assessment-memberships.edn').write_text(dumps(memberships) + '\n')
(OUT / 'snapshot.json').write_text(json.dumps({'database': 'math', 'basis_t': basis, 'lineage': lineage, 'source_index': str(PREVIOUS / 'source-index-metadata.json')}, indent=2) + '\n')
print('snapshot', basis, 'membership rows', len(memberships), flush=True)
