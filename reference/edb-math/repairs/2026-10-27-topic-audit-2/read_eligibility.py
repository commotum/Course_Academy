"""Read source eligibility with forward pulls; inverse joins exceed query timeout."""
import json,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
qmap={}
for g,f in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]:
 for q in json.loads((H/g/f).read_text())['questions']:qmap[q[':db/id']]=q
db=connection()
try:
 mids=[r[0]for r in db.query('[:find ?m :where [?m :multistep/id _]]',[],H,'multistep-ids',9122)]
 print('Parents',len(mids),flush=True);parents=[]
 for i in range(0,len(mids),15):parents +=[r[0]for r in db.query('[:find (pull ?m [:db/id :multistep/id :multistep/context {:multistep/steps [:db/id :step/content]}]) :in $ [?m ...] :where [?m :multistep/id _]]',[mids[i:i+15]],H,'parent-forward-'+str(i),9122)]
 assigned=db.query('[:find ?p ?c :where [?p :assigned-problem/content ?c]]',[],H,'assigned-forward-all',9122)
except Exception as e:
 print(getattr(e,'stderr',str(e)),flush=True);raise
children=collections.defaultdict(list)
for p,c in assigned:children[p].append(c)
contained=collections.defaultdict(set);direct=[]
for parent in parents:
 for s in parent.get(':multistep/steps',[]):
  if ':step/content'not in s:continue
  c=s[':step/content'][':db/id'];direct.append([parent[':db/id'],s[':db/id'],c]);pending=[c];seen=set()
  while pending:
   value=pending.pop()
   if value in seen:continue
   seen.add(value);contained[value].add(parent[':db/id']);pending.extend(children[value])
out=[]
for q,obj in qmap.items():
 if obj.get(':question/retired')or q in contained:out.append({k:v for k,v in obj.items()if k in [':db/id',':question/id',':question/math-academy-id',':question/retired']}|{'multistep_parents':sorted(contained.get(q,[])),'reasons':(['retired']if obj.get(':question/retired')else[])+(['structurally-contained']if q in contained else[])})
(H/'source-eligibility.json').write_text(json.dumps({'basis_t':9122,'scope_question_records':3012,'excluded_questions':out,'direct_edges':direct,'assigned_edges':assigned},indent=2,default=str)+'\n');(H/'multistep-parent-records.json').write_text(json.dumps(parents,indent=2,default=str)+'\n');print('Excluded',len(out),flush=True)
