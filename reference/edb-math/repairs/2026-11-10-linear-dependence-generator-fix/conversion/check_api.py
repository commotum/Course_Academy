"""Read-only native grading of original radio choices and converted subsets."""
import concurrent.futures
import itertools
import json
from pathlib import Path
import sys
import urllib.request

H=Path(__file__).resolve().parent
phase=sys.argv[1]
plan=json.loads((H/'plan.json').read_text())
questions=json.loads((H/('targets-before.json' if phase=='before' else 'questions-committed.json')).read_text())
cases=[]
for p in plan['questions']:
    q=next(q for q in questions if q[':db/id']==p['entity']);fs=q[':question/answer-fields']
    if phase=='before':
        for m in p['choice_mapping']:
            cases.append(dict(question=q[':db/id'],selected=m['selected'],responses=[dict(fieldId=fs[0][':db/id'],choiceId=m['old_answer'])],expected='correct' if m['correct'] else 'incorrect'))
    else:
        object_by_uuid={o['field_id']:o for o in p['objects']}
        for bits in itertools.product((False,True),repeat=len(fs)):
            selected=[object_by_uuid[f[':answer-field/id']]['source_label'] for f,b in zip(fs,bits) if b]
            responses=[dict(fieldId=f[':db/id'],choiceId=next(a[':db/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(b).lower())) for f,b in zip(fs,bits)]
            cases.append(dict(question=q[':db/id'],selected=selected,responses=responses,expected='correct' if set(selected)==set(p['correct']) else 'incorrect'))

def grade(c):
    req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(dict(topicId=17592186050426,questionId=c['question'],responses=c['responses'])).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=90) as r:result=json.load(r)
    return dict(c,actual=result.get('status'),basis=result.get('basis'),preview=result.get('preview'),passed=result.get('status')==c['expected'])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:checks=list(pool.map(grade,cases))
(H/('api-'+phase+'.json')).write_text(json.dumps(dict(phase=phase,database_writes=0,passed=all(c['passed'] for c in checks),checks=checks),indent=2)+'\n')
assert all(c['passed'] and c['preview'] for c in checks),[c for c in checks if not c['passed']]
print(f'{phase}: all {len(checks)} live native grading checks passed without learner writes.')
