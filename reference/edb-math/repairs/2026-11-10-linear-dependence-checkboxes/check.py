"""Check actual speculative/readback records, history mappings and native grading."""
import copy
import json
from pathlib import Path
import subprocess
import sys

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import loads

def save(name,value):
    (H/(name+'.json')).write_text(json.dumps(value,default=str,indent=2)+'\n')
def load(name):
    return json.loads((H/(name+'.json')).read_text())
def pull(name):
    return json.loads(json.dumps(loads((H/'preview'/(name+'.edn')).read_text()),default=str))

if __name__=='__main__':
    plan=load('plan')
    questions=[r[1] for r in pull('final-pull1')]
    before={q[':db/id']:q for q in load('targets-before')}
    proposed={c['question'][':db/id']:c for c in load('proposed-presentation')['cases']}
    cases=[]
    records=[]
    for q in questions:
        qid=q[':db/id']; expected=proposed[qid]['question']
        assert q[':question/problem']==expected[':question/problem']
        assert q[':question/worked-solution']==expected[':question/worked-solution']
        for attr in [':question/id',':question/math-academy-id',':question/difficulty']:
            if attr==':question/difficulty':
                assert q[attr][':db/id']==before[qid][attr][':db/id']
            else:
                assert q.get(attr)==before[qid].get(attr),(qid,attr)
        byuuid={f[':answer-field/id']:f for f in q[':question/answer-fields']}
        assert set(byuuid)=={f[':answer-field/id'] for f in expected[':question/answer-fields']}
        enginefields=[];checks=[]
        p=next(p for p in plan['questions'] if p['entity']==qid)
        for i,ef in enumerate(expected[':question/answer-fields']):
            f=byuuid[ef[':answer-field/id']]
            assert f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
            assert f[':answer-field/key']==ef[':answer-field/key']
            assert len(f[':answer-field/choices'])==2
            assert {(a[':answer/id'],a[':answer/value']) for a in f[':answer-field/choices']}=={(a[':answer/id'],a[':answer/value']) for a in ef[':answer-field/choices']}
            assert f[':answer-field/correct'][':answer/id']==ef[':answer-field/correct'][':answer/id']
            assert all(a[':answer/type'][':db/ident']==':answer.type/text' for a in f[':answer-field/choices'])
            enginefields.append({':answer-field/id':f[':answer-field/id'],':answer-field/key':f[':answer-field/key'],
                ':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':[
                    {':answer/id':a[':answer/id'],':answer/type':':answer.type/text',':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],
                ':answer-field/correct':[':answer/id',f[':answer-field/correct'][':answer/id']]})
            for a in f[':answer-field/choices']:
                checks.append(dict(field_index=i,submitted_answer_id=a[':answer/id'],
                  expected='accepted' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else 'rejected',purpose='actual speculative owned Boolean bank'))
        records.append(dict(label=p['ma_id'] or p['question_uuid'],record=dict(question={':question/problem':q[':question/problem'],':question/answer-fields':enginefields},
             knowledge_point=dict(title='Identifying true statements about linear dependence'),generation=dict(template='authored-checkbox-v1')),
             checks=checks,mapped_responses=[dict(old_answer=t['old_answer'],answer_ids=t['new_answers'],expected=t['correct']) for t in p['choice_mapping']]))
        cases.append(dict(question=q,objects=proposed[qid]['objects']))
    save('speculative-questions',questions)
    save('speculative-presentation',dict(cases=cases))
    subprocess.run([sys.executable,str(ROOT/'skills/radio2checkbox/scripts/lint_presentation.py'),str(H/'speculative-presentation.json'),'--output',str(H/'speculative-presentation-lint.json')],check=True)
    for label,n in [('old-fields',2),('old-answers',3)]:
        actual={r[0]:r[1] for r in pull('final-pull'+str(n))}
        original={r[0][':db/id']:r[0] for r in load(label+'-before')}
        assert actual==original,label
    items={r[0]:r[1] for r in pull('final-pull4')}
    amap={a[':answer/id']:a[':db/id'] for q in questions for f in q[':question/answer-fields'] for a in f[':answer-field/choices']}
    for oldrow in load('presentations-before'):
        old=oldrow[0];after=copy.deepcopy(items[old[':db/id']]); observed=after.pop(':task-item/responses',[])
        unchanged=copy.deepcopy(old);unchanged.pop(':task-item/responses',None)
        assert after==unchanged,'Saved status/timing or other item state changed'
        m=next(m for m in plan['response_migrations'] if m['item']==old[':db/id'])
        assert {a[':db/id'] for a in observed}=={amap[a] for a in m['after']}
    report=loads((H/'preview/stage1-preview.edn').read_text())
    assert report[':edb/db-before-t']==plan['basis']
    assert all(d[4]==plan['source_entity'] for d in report[':edb/tx-data'])
    attributes=dict(loads((H/'attribute-idents.edn').read_text()))
    allowed={':db/txInstant',':question/problem',':question/worked-solution',':question/answer-fields',':task-item/responses',
      ':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value'}
    assert {str(attributes[d[1]]) for d in report[':edb/tx-data']}<=allowed
    save('engine-input',records)
    subprocess.run(['/tmp/linear-dependence-checkbox-grade',str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
    save('speculative-verification',dict(passed=True,questions=len(questions),owned_fields=3*len(questions),owned_answers=6*len(questions),
      saved_attempts=len(items),all_original_radio_choices_preserved=True,old_fields_and_answers_unchanged=True,
      solution_math_difficulty_membership_and_item_state_preserved=True,all_datom_sources=plan['source'],basis=plan['basis']))
    print('Speculative identities, presentation, mappings, provenance and native grading passed.')
