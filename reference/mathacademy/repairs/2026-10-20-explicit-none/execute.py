"""Apply one verified batch at a time; refresh only confirmed stale rejections."""
import shutil
from repair import *
from capture.scripts.database.client import StaleBasis
from quality import quality

def run(number):
 base=HERE/f'batch-{number:02}';previous=None
 for attempt in range(5):
  try:
   if not(base/'request.json').exists():
    prepare(number);quality(number)
    if previous:
     old=json.loads((previous/'before.json').read_text());new=json.loads((base/'before.json').read_text())
     assert equal(old['questions'],new['questions']),'Concurrent question content changed; inspect before reusing rendered review'
     if(previous/'ui-verification.json').exists():
      save(base/'ui-verification.json',{'passed':True,'review_reused_from':str(previous/'ui-verification.json'),'captured_questions_identical':True})
   if not(base/'ui-verification.json').exists():
    p=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(HERE/'ui.py'),str(number)],env=DB.environment,capture_output=True,text=True,timeout=180);(base/'ui.stdout').write_text(p.stdout);(base/'ui.stderr').write_text(p.stderr);p.check_returncode()
   qualitydata=json.loads((base/'quality.json').read_text());assert qualitydata['passed']and qualitydata['presentation_lint_passed']and qualitydata['none_field_complete_visible_labels_verified'];assert json.loads((base/'ui-verification.json').read_text())['passed']
   commit(number);return
  except StaleBasis as error:
   assert not(base/'receipt.edn').exists(),'Reconcile existing receipt before refresh'
   request=json.loads((base/'request.json').read_text());save(base/'rejection.json',{'confirmed_not_committed':True,'code':'postgres/stale-basis','diagnostic':str(error),'request_key':request['request_key']})
   target=HERE/'rejected'/f'batch-{number:02}-basis-{request["basis"]}';target.parent.mkdir(exist_ok=True);assert not target.exists();shutil.move(str(base),str(target));previous=target
   print(json.dumps({'batch':number,'confirmed_stale_rejection':request['basis'],'refreshing_uncommitted_batch':True}),flush=True)
 raise RuntimeError('Repeated concurrent basis changes; no unknown request was rebuilt')
if __name__=='__main__':run(int(sys.argv[1]))
