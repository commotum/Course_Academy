"""Validate the application preview for a combined activity/content repair."""
from pathlib import Path
import hashlib,json,sys,copy
HERE=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve()
before=json.loads((out/'api-preview-before.json').read_text())
after=json.loads((out/'api-preview-after.json').read_text())
scenarios=json.loads((out/'api-preview-resume-continue.json').read_text())
assert len(before['tasks'])==len(after['tasks'])==len(scenarios['scenarios'])==1
b=before['tasks'][0];a=after['tasks'][0];task=17592186413350;bad=17592186576280
assert b['task']==a['task']==task
assert [i['item'] for i in b['chain']]==[17592186576278,17592186576279,bad]
assert [i['item'] for i in a['chain']]==[17592186576278,17592186576279]
for old,new in zip(b['chain'],a['chain']):
 old=copy.deepcopy(old)
 if old['record'].get('task-item/next')==bad:old['record'].pop('task-item/next')
 assert old==new,'Retained tutorial/example content or state changed'
record=copy.deepcopy(b['record'])
record['learner-task/items']=[i for i in record['learner-task/items'] if i!=bad]
record['learner-task/elapsed-seconds']=sum(i['record']['task-item/elapsed-seconds'] for i in a['chain'])
assert record==a['record'],'Task attributes other than planned elapsed/membership changed'
assert a['taskJson']['ok'] and a['position']['ok'] and a['practiceState']['ok']
scenario=scenarios['scenarios'][0]
assert scenario['preview']['ok'],scenario
value=scenario['preview']['value']
assert value['nextQuestion']!=17592186487475
assert value['nextQuestionIsMultistep'] is False
assert value['nextQuestionWasPreviouslyUnavailable'] is False
result={'passed':True,'committed':False,'speculative':True,'basis_before':before['basis'],'transaction_sha256':hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest(),'task':task,'bad_item_detached':bad,'retained_items_unchanged':2,'retained_content_and_responses_unchanged':True,'resume_continue_passed':True,'fresh_next_question':value['nextQuestion'],'paused_task_preserved':True}
(out/'application-preview.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
