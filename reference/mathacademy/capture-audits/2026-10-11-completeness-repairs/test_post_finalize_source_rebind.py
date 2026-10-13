import json,unittest
from copy import deepcopy
from pathlib import Path
from playwright.sync_api import sync_playwright
import run_later_repairs as driver
from scripts.database.evidence import authoritative_question
R=Path(__file__).resolve().parent
class PostFinalizeSourceKeys(unittest.TestCase):
 def test_three_actual_stale_finalized_keys_validate_after_own_source_rebind(self):
  with sync_playwright() as pw:
   browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda r:r.abort());driver.ACTIVE_PAGE=context.new_page();driver.ENABLE_LITERAL_SOURCE_REFRESH=True;driver.CURRENT_SOURCE_REPAIR=R/'literal-brace-local-tests'
   for account,task,identity in [('linear','14114807','q-172706'),('linear','14117627','q-214479'),('linear','14117627','q-214481')]:
    p=R.parents[1]/'capture'/account/task/'repairs/completeness-f31ec8f96c25ef6c';original=json.loads((p/'originals/content.json').read_text());content=json.loads((p/'content.json').read_text());old=next(q for q in original['questions'] if q['math_academy_id']==identity);new=deepcopy(next(q for q in content['questions'] if q['math_academy_id']==identity));driver.CURRENT_SOURCE_ORIGINALS={identity:old}
    # Current source quotes, including explicit own ordered-list restoration,
    # are installed before finalization. Stale historical grade stays local.
    new=driver.refresh_literal_source(old,new,driver.ACTIVE_PAGE,driver.CURRENT_SOURCE_REPAIR)
    judgment=next(j for j in reversed(content['judgments']) if j.get('question_id')==identity)
    finalized=driver.source_bound_finalize(new,[],judgment);checked=authoritative_question(finalized)
    self.assertTrue(checked['answer_fields_complete']);self.assertTrue(any(f.get('source_serializer_rebind') for f in checked['answer_fields']))
    (R/'literal-brace-local-tests'/('post-finalize-'+identity+'.json')).write_text(json.dumps(checked,indent=2)+'\n')
   browser.close()
if __name__=='__main__':unittest.main()
