"""Exhaustive read-only live grading before/after the conversion."""
import concurrent.futures
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
    q=next(q for q in questions if q[':db/id']==p['entity'])
    fs=q[':question/answer-fields']
    for t in p['tuple_mapping']:
        if phase=='before':
            responses=[dict(fieldId=f[':db/id'],choiceId=next(a[':db/id'] for a in f[':answer-field/choices'] if a[':db/id'] in t['old_answers'])) for f in fs]
        else:
            responses=[dict(fieldId=f[':db/id'],choiceId=next(a[':db/id'] for a in f[':answer-field/choices'] if a[':answer/id'] in t['new_answers'])) for f in fs]
        cases.append(dict(question=q[':db/id'],selected=t['selected'],responses=responses,expected='correct' if t['correct'] else 'incorrect'))

def grade(c):
    req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(dict(topicId=17592186050677,questionId=c['question'],responses=c['responses'])).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=90) as r:
        result=json.load(r)
    return dict(c,actual=result.get('status'),basis=result.get('basis'),preview=result.get('preview'),passed=result.get('status')==c['expected'])

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    checks=list(pool.map(grade,cases))
(H/('api-'+phase+'.json')).write_text(json.dumps(dict(phase=phase,database_writes=0,passed=all(c['passed'] for c in checks),checks=checks),indent=2)+'\n')
assert all(c['passed'] and c['preview'] for c in checks),[c for c in checks if not c['passed']]
print(f'{phase}: all {len(checks)} subsets passed live native grading with no learner writes.')
