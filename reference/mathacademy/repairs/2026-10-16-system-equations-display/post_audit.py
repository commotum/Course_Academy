"""Recheck current target-topic membership and both text fields at committed basis."""
import json,re,sys
from concurrent.futures import ThreadPoolExecutor
from read import HERE,ROOT,DB
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import MATH,legacy_system_rows
v=json.loads((HERE/'verification.json').read_text());basis=v['basis_after']
prior=json.loads((ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display/wide-mth341/fields.json').read_text())
tids=sorted({f['topic'] for f in prior})
pattern='''[:db/id :topic/title {[:topic/knowledge-points :limit nil]
 [:db/id {[:knowledge-point/questions :limit nil] [:db/id :question/problem :question/worked-solution]}
 {:knowledge-point/canonical-example [:db/id :question/problem :question/worked-solution]}]}]'''
def query(ids):return DB.query('[:find (pull ?topic '+pattern+') :in $ [?topic ...] :where [?topic :topic/id _]]',[ids],HERE/'post-audit','topics-'+str(ids[0]),basis)
with ThreadPoolExecutor(max_workers=3) as pool:topics=[row[0] for group in pool.map(query,[tids[i:i+7] for i in range(0,len(tids),7)]) for row in group]
fields=[];questions=set();kps=set();issues=[]
for topic in topics:
 for kp in topic[':topic/knowledge-points']:
  kps.add(kp[':db/id'])
  for q in kp.get(':knowledge-point/questions',[])+([kp[':knowledge-point/canonical-example']] if ':knowledge-point/canonical-example' in kp else []):
   questions.add(q[':db/id'])
   for a in (':question/problem',':question/worked-solution'):
    if a not in q:continue
    f={'entity':q[':db/id'],'attribute':a,'topic':topic[':db/id'],'value':q[a]};fields.append(f)
    for m in MATH.finditer(q[a]):
     raw=m[0];n=2 if raw.startswith(('$$',r'\[',r'\(')) else 1;tex=raw[n:-n]
     if legacy_system_rows(tex) or re.search(r'\\mid\s*\\mid\s*\\cdot',tex):issues.append(f|{'tex':tex})
(HERE/'post-audit/fields.json').write_text(json.dumps(fields,indent=2)+'\n')
summary={'passed':not issues,'basis':basis,'topics':len(topics),'kps':len(kps),'questions':len(questions),'fields':len(fields),'remaining_flat_systems_or_duplicate_operation_bars':len(issues),'issues':issues}
(HERE/'post-audit/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary));assert not issues
