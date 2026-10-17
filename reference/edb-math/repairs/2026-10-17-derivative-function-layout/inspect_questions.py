"""Read-only fixed-basis investigation of four derivative questions."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps, loads

HERE = Path(__file__).resolve().parent
IDS = [17592186514433, 17592186235429, 17592186096417, 17592186514464]
KP_PULL = '[* {[:topic/_knowledge-points :limit nil] [:db/id :topic/title :topic/math-academy-id]} {:knowledge-point/question-generator [*]} {[:knowledge-point/questions :limit nil] [:db/id :question/math-academy-id]} {:knowledge-point/canonical-example [:db/id :question/math-academy-id]}]'
QUESTION_PULL = '[* {:question/difficulty [:db/id :db/ident]} {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/title]} {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/title]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]} {[:assigned-problem/_content :limit nil] [* {[:step/_content :limit nil] [:db/id :step/id]}]} {[:step/_content :limit nil] [:db/id :step/id {[:activity/_steps :limit nil] [:db/id :activity/id :activity/title]}]}]'

def main():
    db = Publisher.from_environment(source=':agent/gpt-6.1-sol-high').client
    identity = db.status(); basis = identity['basis']
    directory = HERE / f'capture-{basis}'; directory.mkdir(exist_ok=True)
    def read(name, query, inputs): return db.query(query, inputs, directory, name, basis)
    questions = read('questions', '[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?q ...] :where [?q :question/id _]]', [IDS])
    kids = sorted({kp[':db/id'] for [q] in questions for key in (':knowledge-point/_questions', ':knowledge-point/_canonical-example') for kp in q.get(key, [])})
    queries = {
        'scope': ('[:find (pull ?kp ' + KP_PULL + ') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]', [kids]),
        'current-provenance': ('[:find ?q ?attr ?value ?tx (pull ?source [*]) :in $ [?q ...] [?attr ...] :where [?q ?attr ?value ?tx ?source]]', [IDS, [':question/id', ':question/math-academy-id', ':question/problem']]),
    }
    # Literal attribute keywords are encoded separately from strings below.
    from capture.scripts.database.edn import kw
    queries['current-provenance'][1][1] = list(map(kw, queries['current-provenance'][1][1]))
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {name: pool.submit(read, name, *args) for name, args in queries.items()}
        data = {name: f.result() for name, f in futures.items()}
    snapshot = {**identity, 'questions': questions, **data}
    (directory / 'snapshot.edn').write_text(dumps(snapshot) + '\n')
    (HERE / 'capture-directory.txt').write_text(str(directory.relative_to(ROOT)) + '\n')
    (directory / 'snapshot.json').write_text(json.dumps(snapshot, indent=2, default=str) + '\n')
    for [q] in questions:
        print(json.dumps(q, indent=2, default=str))
    print(json.dumps({'basis': basis, 'knowledge_points': data['scope'], 'capture_directory': str(directory)}, indent=2, default=str))

if __name__ == '__main__': main()
