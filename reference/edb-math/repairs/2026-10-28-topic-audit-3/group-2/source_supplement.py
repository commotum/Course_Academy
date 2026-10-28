import copy,json,re,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent
P=json.loads((H/'source-supplement-proposals.json').read_text());Q=json.loads((H/'proposed-questions.json').read_text());A=json.loads((H/'proposed-activities.json').read_text());nodes={}
def index(value):
 if isinstance(value,dict):
  if ':db/id'in value:nodes.setdefault(value[':db/id'],[]).append(value)
  for v in value.values():index(v)
 elif isinstance(value,list):
  for v in value:index(v)
index(Q);index(A)
# The39 overlapping source-format candidates are weaker presentations of fields
# already repaired in freeze1. Apply any truly additional exact math-span changes
# inside delimiters, never as unrestricted character replacements.
import sys
sys.path.insert(0,str(H.parents[4]/'scripts'));from question_capture.math_format import MATH,validate_math_structure
for p in json.loads((H/'source-supplement-overlaps.json').read_text()):
 before=nodes[p['entity']][0].get(':'+p['attribute']);after=before
 for e in p['evidence']:
  old,new=e.get('before_math'),e.get('after_math')
  if old is None or new is None:continue
  def repl(m):
   edge=2 if m[0].startswith('$$')else 1
   return m[0][:edge]+new+m[0][-edge:]if m[0][edge:-edge].strip()==old.strip()else m[0]
  after=MATH.sub(repl,after)
 if after!=before:P.append({**p,'before':before,'after':after,'reason':'Additional retained hashed-history source notation after frozen main repair'})
render=[]
for p in P:
 for n in nodes[p['entity']]:assert n.get(':'+p['attribute'])==p['before'];n[':'+p['attribute']]=p['after']
 validate_math_structure(p['after']);render.append({'entity':p['entity'],'attribute':p['attribute'],'value':p['after'],'bare_math':p['attribute']=='answer/value'})
(H/'source-supplement-proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'source-supplement-render-input.json').write_text(json.dumps(render,indent=2)+'\n');(H/'supplement-proposed-questions.json').write_text(json.dumps(Q,indent=2)+'\n');print('supplement',len(P))
# Actual native checks only for questions whose prospective entities changed.
ids={p['entity']for p in P};changed=[]
for q in Q:
 if q[':db/id']in ids or any(f[':db/id']in ids or any(a[':db/id']in ids for a in f.get(':answer-field/choices',[]))for f in q.get(':question/answer-fields',[])):changed.append(q)
grade={x['label']:x for x in json.loads((H/'prospective-grading-input.json').read_text())};checks=[]
for q in changed:
 if str(q[':db/id'])not in grade:continue
 item=copy.deepcopy(grade[str(q[':db/id'])]);payload=copy.deepcopy(q)
 for f in payload.get(':question/answer-fields',[]):
  f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f.get(':answer-field/choices',[]):a[':answer/type']=a[':answer/type'][':db/ident']
 item['record']['question']=payload;checks.append(item)
(H/'source-supplement-grading-input.json').write_text(json.dumps(checks,indent=2)+'\n');subprocess.run([str(H.parent/'check-engine'),str(H/'source-supplement-grading-input.json'),str(H/'source-supplement-grading.json')],check=True)
