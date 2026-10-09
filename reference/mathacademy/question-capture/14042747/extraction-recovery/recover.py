import copy,hashlib,json,random,shutil,sys,time
from pathlib import Path
sys.path.insert(0,str(Path('/home/jake/Developer/Course_Academy/scripts/question_capture')))
from capture import arguments,locked
from browser import CaptureBrowser,EXTRACT,repair_math_editor_document
from core import Pacer,atomic_json
from database import Database
from retry_policy import completion_outcome,update_policy
from playwright.sync_api import sync_playwright
D=Path(__file__).resolve().parent.parent;A=D/'extraction-recovery';pkg=Path('/home/jake/Developer/Course_Academy/scripts/question_capture')
normal=json.loads((A/'normal-worker-before.json').read_text());args=arguments(normal['command'][3:])
args.no_import_repair=True;args.no_capture_repair=True
with locked(args.state_dir):
    state=json.loads((D/'state.json').read_text());original=copy.deepcopy(state)
    originals=A/'original';originals.mkdir(exist_ok=True)
    paths=[D/'state.json']+[D/(mid+suffix) for mid in state['questions'] for suffix in ('-before.json','-after.json')]
    manifest=[]
    for source in paths:
        target=originals/source.name
        if target.exists():assert target.read_bytes()==source.read_bytes()
        else:shutil.copy2(source,target)
        manifest.append({'source':str(source),'archive':str(target),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    atomic_json(A/'original-bindings.json',manifest)
    with sync_playwright() as p:
        context=p.chromium.launch_persistent_context(str(args.profile),headless=True,slow_mo=args.ui_delay_ms)
        try:
            context.route('https://mathacademy.com/**',repair_math_editor_document)
            page=context.pages[0] if context.pages else context.new_page()
            reader=CaptureBrowser(page,args,Pacer(args,random.Random()),None)
            reader.database=Database(args)
            reader.navigate(state['activity_url'],force=True)
            (A/'server-before.html').write_text(page.content());page.screenshot(path=str(A/'server-before.png'))
            task=page.locator('#task-14042747.taskCompleted')
            assert task.count()==1 and task.locator('.pointsLost').count()==1
            row=task.inner_text();row_html=task.inner_html();assert '-2' in row and '4 XP' in row
            topic=reader.database.topic(state['topic_id'],D/'selection')
            preflight=A/'history-preflight';preflight.mkdir(exist_ok=True)
            preflight_state=copy.deepcopy(state)
            reader.history(preflight_state,preflight,topic)
            grades={mid:r['history']['worked_solution'] for mid,r in preflight_state['questions'].items()}
            assert set(grades)==set(state['questions'])
            original_terminal=D/'diagnostics/1791457125356707055/page.html'
            terminal_page=context.new_page();terminal_page.route('**/*',lambda r:r.abort())
            terminal_page.set_content(original_terminal.read_text())
            terminal=terminal_page.locator('#finalScreen').inner_text();terminal_page.close()
            assert completion_outcome(terminal,'review')=='failed'
            atomic_json(A/'server-before.json',{'url':page.url,'completed_task_text':row,
                'completed_task_html':row_html,
                'archived_terminal':terminal,'archived_terminal_path':str(original_terminal),
                'archived_terminal_sha256':hashlib.sha256(original_terminal.read_bytes()).hexdigest(),
                'history_grades':{mid:preflight_state['questions'][mid]['actual_result'] for mid in grades}})
            # Re-extract only study content from hash-bound authentic source DOM.
            extraction=context.new_page();extraction.route('**/*',lambda route:route.abort())
            regenerated={}
            for mid,record in state['questions'].items():
                before=json.loads((originals/(mid+'-before.json')).read_text());after=json.loads((originals/(mid+'-after.json')).read_text())
                extraction.set_content(before['html']);b=extraction.locator('#'+before['dom_id']).evaluate(EXTRACT)
                extraction.set_content(after['html']);a=extraction.locator('#'+after['dom_id']).evaluate(EXTRACT)
                assert not b['errors'] and not a['errors']
                assert a['result']==record['actual_result']
                old=copy.deepcopy(record['content']);record['content']['problem']=b['problem'];record['content']['worked_solution']=a['worked_solution']
                assert len(b['fields'])==len(record['content']['answer_fields'])
                for incoming,field,verified in zip(b['fields'],record['content']['answer_fields'],record.get('verification',record['decision'])['answers']):
                    assert incoming['key']==field['key']==verified['key']
                    assert incoming['type']=='radio'
                    correct=[c for c in incoming['choices'] if c['option']==verified['correct_option']]
                    assert len(correct)==1
                    field['choices']=[{k:c[k] for k in ('type','value')} for c in incoming['choices']]
                    field['correct_value']=correct[0]['value']
                regenerated[mid]={'original_content':old,'regenerated_content':copy.deepcopy(record['content']), 'before_extraction':b,'after_extraction':a}
            extraction.close();atomic_json(A/'regenerated-study-content.json',regenerated)
            atomic_json(D/'state.json',state)
            topic=reader.database.topic(state['topic_id'],D/'selection')
            state.update(completion=terminal,activity_complete=True,review_complete=True,activity_outcome='failed',earned_xp=-2)
            state['terminal_recovery']={'evidence':str(A/'server-before.json'),'method':'archived_terminal_attested_by_completed_server_row_and_exact_history_grades'}
            atomic_json(D/'state.json',state)
            reader.knowledge_snapshot(state,D,'review-completed',recovered=True)
            assert state['activity_outcome']=='failed' and state['earned_xp']==-2
            update_policy(args.state_dir,completed_state=state)
            content=reader.history(state,D,topic)
            assert all(state['questions'][mid]['actual_result']==original['questions'][mid]['actual_result'] and state['questions'][mid]['decision']==original['questions'][mid]['decision'] for mid in state['questions'])
            atomic_json(A/'recovery-result.json',{'task_id':state['task_id'],'activity_outcome':state['activity_outcome'],'earned_xp':state['earned_xp'],'question_count':len(content['questions']),'history_complete':state['history_complete'],'pattern':state['review_sequence'],'completed_at':time.time()})
            print('Confirmed failed terminal, snapshot and 4-question history captured without answers')
        finally:context.close()
