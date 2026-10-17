"""Read-only topic audit pinned to the basis recorded by seed discovery."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps

HERE = Path(__file__).resolve().parent
QUESTION = '''[* {:question/difficulty [:db/id :db/ident]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''
ITEM = '''[* {:task-item/status [:db/id :db/ident]}
 {[:task-item/responses :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {[:learner-task/_items :limit nil] [:db/id :learner-task/status]}]'''


def main():
    assert not (HERE / 'snapshot.json').exists(), 'Preserve the captured audit'
    identity = json.loads((HERE / 'capture-identity.json').read_text())
    basis = identity['basis']
    client = Publisher.from_environment().client
    assert client.status()['lineage'] == identity['lineage']

    def read(name, query, inputs):
        return client.query(query, inputs, HERE / 'evidence', name, basis)

    topics = [17592186049723]
    with ThreadPoolExecutor(max_workers=2) as executor:
        scope_future = executor.submit(read, 'scope', '''[:find (pull ?topic [*
          {[:topic/knowledge-points :limit nil] [*
          {[:knowledge-point/questions :limit nil] [:db/id]}
          {:knowledge-point/canonical-example [:db/id]}
          {:knowledge-point/question-generator [*]}]}])
          :in $ [?topic ...] :where [?topic :topic/id _]]''', [topics])
        activities_future = executor.submit(read, 'activities', '''[:find (pull ?activity [*
          {:activity/type [:db/id :db/ident]}
          {[:activity/steps :limit nil] [* {:step/content [*]}]}])
          :in $ [?topic ...] :where [?activity :activity/scope ?topic]]''', [topics])
        scope, activities = scope_future.result(), activities_future.result()
    ids = {q[':db/id'] for [topic] in scope for kp in topic.get(':topic/knowledge-points', [])
           for q in kp.get(':knowledge-point/questions', []) +
           ([kp[':knowledge-point/canonical-example']] if kp.get(':knowledge-point/canonical-example') else [])}
    # Include questions directly embedded in any topic-scoped activity.
    def question_ids(value):
        if isinstance(value, dict):
            if ':question/id' in value:
                ids.add(value[':db/id'])
            for child in value.values():
                question_ids(child)
        elif isinstance(value, list):
            for child in value:
                question_ids(child)
    question_ids(activities)
    ids = sorted(ids)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            'questions': executor.submit(read, 'questions', '[:find (pull ?q ' + QUESTION + ') :in $ [?q ...] :where [?q :question/id _]]', [ids]),
            'items': executor.submit(read, 'items', '[:find ?q (pull ?item ' + ITEM + ') :in $ [?q ...] :where [?item :task-item/content ?q]]', [ids]),
            'question_sources': executor.submit(read, 'question-sources', '[:find ?q ?tx (pull ?source [:db/id :db/ident]) :in $ [?q ...] :where [?q :question/id _ ?tx ?source]]', [ids]),
        }
        results = {name: future.result() for name, future in futures.items()}
    assert len(results['questions']) == len(ids)
    snapshot = {**identity, 'requested_entity': 17592186124704,
                'seed': json.loads((HERE / 'seed.json').read_text()),
                'scope': scope, 'activities': activities, **results}
    (HERE / 'snapshot.edn').write_text(dumps(snapshot) + '\n')
    (HERE / 'snapshot.json').write_text(json.dumps(snapshot, indent=2, default=str) + '\n')
    print(json.dumps({'basis': basis, 'topics': topics, 'questions': len(ids),
                      'activities': len(activities), 'learner_items': len(results['items']),
                      'kps': [{k: kp[k] for k in (':db/id', ':knowledge-point/title', ':knowledge-point/question-generator') if k in kp}
                              for [topic] in scope for kp in topic[':topic/knowledge-points']]}, indent=2, default=str))


if __name__ == '__main__':
    main()
