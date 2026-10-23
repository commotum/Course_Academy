"""Strict finite-pool regression. Run with repo Python; defaults to delivered batch.
The current batch must fail: its repeated q-73544 coefficient family fixes rank 4.
Pass an alternative complete-record JSON array as argv[1] to test a replacement.
"""
import sys,json,re
from pathlib import Path
from fractions import Fraction
root=Path(__file__).resolve().parent
input_path=Path(sys.argv[1]) if len(sys.argv)>1 else root/'delivery-batch/accepted.json'
records=json.loads(input_path.read_text())
selected=[];rows=[]
for r in records:
    q=r['question']
    # Recognize the visible coefficient pattern, not hidden template metadata.
    if not ('2x-4y &=' in q[':question/problem'] and '4x-7y &=' in q[':question/problem']):continue
    selected.append(r);f=q[':question/answer-fields'][0];aa=f[':answer-field/choices'];ys=[]
    for a in aa:
        body=re.search(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}',a[':answer/value'],re.S)[1]
        ys.append(Fraction(body.split(r'\\')[1].split('&')[2].strip()))
    target=sorted(ys)[-2];picked=[a[':answer/id'] for a,y in zip(aa,ys) if y==target]
    rows.append({'question_id':q[':question/id'],'generation':r['generation'],'sorted_bottom_right':list(map(str,sorted(ys))),'chosen_answer_ids':picked,'correct_answer_id':f[':answer-field/correct'][1],'strategy_correct':picked==[f[':answer-field/correct'][1]]})
result={'input':str(input_path),'cue':'Visible coefficient family 2x-4y, 4x-7y','strategy':'Choose unique second-largest bottom-right matrix entry','correct':sum(x['strategy_correct'] for x in rows),'total':len(rows),'random_choice_baseline':0.2,'cases':rows,'failure_scope':'Current delivered finite batch; not universal sampler failure'}
(root/'batch-shortcut-records.json').write_text(json.dumps(selected,indent=2))
(root/'batch-shortcut-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
assert not (len(rows)>1 and all(x['strategy_correct'] for x in rows)), 'Delivered repeated coefficient family is perfectly answered by second-largest-entry cue'
