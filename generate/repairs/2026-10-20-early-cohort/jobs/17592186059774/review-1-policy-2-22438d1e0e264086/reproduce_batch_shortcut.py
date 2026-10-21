"""Minimal finite-pool failure: run with job Python from evidence_root."""
from independent import *

records=json.load(open(ROOT/'batch-shortcut-records.json'))
raw={r['generation']['seed']:r for r in json.load(open(ROOT/'runner-batch.json'))}
results=[]
for record in records:
    generation=record['generation']
    replay=g.generate(seed=generation['seed'],parameters=generation['parameters'])
    assert replay['question']==raw[generation['seed']]['question']
    assert replay['question'][':question/problem']==record['question'][':question/problem']
    assert replay['question'][':question/worked-solution']==record['question'][':question/worked-solution']
    assert [a[':answer/value'] for a in replay['question'][':question/answer-fields'][0][':answer-field/choices']]==[a[':answer/value'] for a in record['question'][':question/answer-fields'][0][':answer-field/choices']]
    choices=record['question'][':question/answer-fields'][0][':answer-field/choices']
    # Cue uses only bank expression shape, with no prompt matrix or target.
    candidates=[]
    for i,choice in enumerate(choices):
        operation=op(choice[':answer/value'])
        if operation[0]=='linear' and sum(c!=0 for c in operation[2])==2:
            candidates.append(i)
    assert len(candidates)==1
    expected=analyze(record)['position']
    assert candidates[0]==expected
    results.append({'raw_id':replay['question'][':question/id'],'delivered_id':record['question'][':question/id'],'seed':generation['seed'],
                    'predicted_choice':choices[candidates[0]][':answer/value'],
                    'correct':True,'parameters':generation['parameters']})
assert len(results)==2
save('minimal-batch-failure.json',{'command':'PYTHONDONTWRITEBYTECODE=1 '+sys.executable+' reproduce_batch_shortcut.py',
 'defect':'The sole distinct-row addition answers every q-72858 member of the exact delivered pool without using matrix data.',
 'cases':results,'native_grader_evidence':'grader-input.json and grader-results.json contain all five responses for these exact questions.',
 'control':'17/34 successes in fresh restored-profile controls; this is a batch-selection defect.'})
print(json.dumps({'matrix_free_strategy_successes':len(results),'attempts':len(records),'scope':'exact delivered q-72858 subpool'}))
