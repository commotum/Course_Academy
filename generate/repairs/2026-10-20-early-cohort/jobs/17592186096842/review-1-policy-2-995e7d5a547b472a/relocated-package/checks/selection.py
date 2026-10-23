"""Read-only selection witness; no live learner state or entity IDs available."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent.parent
records=json.load(open(root/'evidence/delivery-prospective-batch/accepted.json'))
# The real selector sorts entity IDs, unavailable before publication. Use a
# disclosed fixed surrogate order; within a positive easy band its draw is uniform.
records=sorted(records,key=lambda r:r['question'][':question/id'])
counts={r['question'][':question/id']:0 for r in records}
for i in range(100):
 digest=hashlib.sha256(f'course-academy/question-selection/v1/author-check-{i}'.encode()).digest()
 uniform=(int.from_bytes(digest[8:16],'big')>>11)/2**53
 counts[records[int(uniform*len(records))]['question'][':question/id']]+=1
assert all(counts.values())
(root/'evidence/selection-results.json').write_text(json.dumps({'code':'engine/rust/question_selection.rs select(): positive difficulty weights followed by uniform SHA256 draw within band','scenario':'Five delivered batch records fresh, easy band positive, UUID surrogate ordering for unknown future entity IDs','draws':counts,'limits':['Exact future learner history, entity ordering and policy weights are unavailable.','Retired inventory radios are excluded by practice eligibility; this script does not change or query the database.','No selector bank-shape filter cures the old ladder; the repaired package itself must pass the strict spacing regression.']},indent=2))
print('Five delivered records reachable in the disclosed positive-easy scenario.')
