import json,sys
from pathlib import Path
sys.path.insert(0,'/home/jake/Developer/Course_Academy/scripts/question_capture')
from capture import arguments,locked
from database import Database
from saved_imports import eligible,complete
from core import atomic_json,journal
D=Path(__file__).resolve().parent.parent;A=D/'extraction-recovery'
args=arguments(json.loads((A/'normal-worker-before.json').read_text())['command'][3:])
args.no_import_repair=True;args.no_capture_repair=True
with locked(args.state_dir):
    state=json.loads((D/'state.json').read_text());content=json.loads((D/'content.json').read_text())
    assert eligible(D,state,content),'Recovered content not import eligible'
    assert state['activity_outcome']=='failed' and state['earned_xp']==-2 and len(content['questions'])==4
    db=Database(args)
    preview=db.import_content(content,D/'edb-import',False)
    atomic_json(A/'import-preview-result.json',preview)
    result=db.import_content(content,D/'edb-import',True)
    complete(args,D,state,result)
    journal(args.state_dir/'journal.jsonl','activity_captured',task_id=state['task_id'],topic_id=state['topic_id'],task_type='review',directory=str(D),activity_outcome='failed')
    atomic_json(A/'import-result.json',result)
    print(json.dumps(result,indent=2))
