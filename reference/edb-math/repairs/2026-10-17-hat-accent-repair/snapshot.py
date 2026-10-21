"""Pinned full records, answer ownership, and source/lesson metadata; read only."""
import concurrent.futures, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher, jsonable
from capture.scripts.database.edn import loads, dumps
from capture.scripts.database.client import QUESTION_PULL
HERE = Path(__file__).resolve().parent
E = HERE / 'evidence'
status = json.loads((E / 'status.json').read_text())
basis = status['basis']
client = Publisher.from_environment(source=':agent/codex').client
candidates = json.loads((HERE / 'candidates.json').read_text())
answers = sorted({v['entity'] for v in candidates if v['attribute_id'] in [1080,1081]})
questions = {v['entity'] for v in candidates if v['attribute_id'] in [1071,1074]}
tutorials = sorted({v['entity'] for v in candidates if v['attribute_id'] == 1064})
ANSWER_PULL = '''[* {:answer/type [:db/id :db/ident]}
 {:answer-field/_choices [* {:answer-field/type [:db/id :db/ident]} {:question/_answer-fields [:db/id]}]}
 {:answer-field/_correct [:db/id {:question/_answer-fields [:db/id]}]}
 {:task-item/_responses [*]}]'''
def query_pull(name, pattern, ids):
    if not ids: return []
    rows = client.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]', [ids], E/'snapshots', name, basis)
    return [v for [v] in rows]
ans = query_pull('answers', ANSWER_PULL, answers)
def many(value):
    return [value] if isinstance(value, dict) else value
for answer in ans:
    for rel in [':answer-field/_choices', ':answer-field/_correct']:
        for field in many(answer.get(rel, [])):
            questions.update(q[':db/id'] for q in many(field.get(':question/_answer-fields', [])))
questions = sorted(questions)
def run(args):
    name, pattern, ids = args
    rows = query_pull(name, pattern, ids)
    print(name, len(rows), flush=True)
    return name, rows
groups = [('questions-'+str(i), QUESTION_PULL, questions[i:i+250]) for i in range(0,len(questions),250)]
groups += [('tutorials', '[*]', tutorials), ('source', '[*]', [17592186576411])]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = dict(pool.map(run, groups))
q = sorted([v for n, vs in results.items() if n.startswith('questions-') for v in vs], key=lambda v:v[':db/id'])
assert len(q) == len(questions)
for name, values in [('questions', q), ('tutorials', results['tutorials']), ('answers', ans), ('source', results['source'])]:
    (E/(name+'.edn')).write_text(dumps(values)+'\n')
    (E/(name+'.json')).write_text(json.dumps(jsonable(values),ensure_ascii=False,indent=2)+'\n')
assert results['source'][0][':db/ident'] == ':agent/codex'
client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], E, 'attributes', basis)
native = [['questions', QUESTION_PULL, questions], ['tutorials', '[*]', tutorials], ['answers', ANSWER_PULL, answers]]
(HERE/'native-pulls.edn').write_text(dumps(native)+'\n')
TP='[:db/id :topic/math-academy-id :topic/title]'
KP='[:db/id :knowledge-point/title {:topic/_knowledge-points '+TP+'}]'
ACT='[:db/id :activity/title :activity/type {:activity/scope '+TP+'}]'
STEP='[:db/id {:activity/_steps '+ACT+'}]'
Q='[:db/id :question/id :question/math-academy-id {:knowledge-point/_questions '+KP+'} {:knowledge-point/_canonical-example '+KP+'} {:step/_content '+STEP+'}]'
F='[:db/id :answer-field/type {:question/_answer-fields '+Q+'}]'
P='[:db/id :question/id :question/math-academy-id :tutorial/id :tutorial/math-academy-id :tutorial/title :answer/id {:knowledge-point/_questions '+KP+'} {:knowledge-point/_canonical-example '+KP+'} {:step/_content '+STEP+'} {:answer-field/_choices '+F+'} {:answer-field/_correct '+F+'}]'
allids = sorted({v['entity'] for v in candidates} | set(questions))
meta = []
for i in range(0,len(allids),250):
    meta += query_pull('metadata-'+str(i), P, allids[i:i+250])
(E/'metadata.json').write_text(json.dumps(jsonable(meta),ensure_ascii=False,indent=2)+'\n')
print('Snapshot complete',len(q),'questions',len(tutorials),'tutorials',len(ans),'answers at',basis,flush=True)
