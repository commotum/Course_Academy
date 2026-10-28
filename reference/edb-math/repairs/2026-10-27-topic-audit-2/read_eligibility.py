import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,kw
qmap={}
for g,f in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]:
 for q in json.loads((H/g/f).read_text())['questions']:qmap[q[':db/id']]=q
assert len(qmap)==3012;db=connection();direct=[];assigned=[];seen=set();pending=set(qmap)
while pending:
 current=sorted(pending-seen);pending=set();seen.update(current)
 for offset in range(0,len(current),100):
  ids=current[offset:offset+100];label=str(len(seen))+'-'+str(offset)
  rows=db.query('[:find ?p ?c :in $ [?c ...] :where [?p :assigned-problem/content ?c]]',[ids],H,'assigned-bounded-'+label,9122);assigned+=rows;pending.update(p for p,c in rows if p not in seen)
  step_rows=db.query('[:find ?c ?s :in $ [?c ...] :where [?s :step/content ?c]]',[ids],H,'content-steps-'+label,9122)
  if step_rows:
   owners=db.query('[:find ?m ?s :in $ [?s ...] :where [?m :multistep/steps ?s]]',[sorted({s for c,s in step_rows})],H,'step-owners-'+label,9122)
   bystep=collections.defaultdict(list)
   for m,s in owners:bystep[s].append(m)
   direct.extend([m,s,c]for c,s in step_rows for m in bystep[s])
children=collections.defaultdict(list)
for p,c in assigned:children[p].append(c)
contained=collections.defaultdict(set)
for m,s,c in direct:
 pending=[c];seen=set()
 while pending:
  value=pending.pop()
  if value in seen:continue
  seen.add(value);contained[value].add(m);pending.extend(children[value])
out=[]
for q,obj in qmap.items():
 if obj.get(':question/retired')or q in contained:out.append({k:v for k,v in obj.items()if k in [':db/id',':question/id',':question/math-academy-id',':question/retired']}|{'multistep_parents':sorted(contained.get(q,[])),'reasons':(['retired']if obj.get(':question/retired')else[])+(['structurally-contained']if q in contained else[])})
(H/'source-eligibility.json').write_text(json.dumps({'basis_t':9122,'scope_question_records':3012,'excluded_questions':out,'direct_edges':direct,'assigned_edges':assigned},indent=2,default=str)+'\n');print('Retired or structurally multistep:',len(out),'directedges',len(direct),'assignededges',len(assigned))
