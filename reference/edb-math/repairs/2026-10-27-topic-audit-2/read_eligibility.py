import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,kw
from scripts.generator_source_policy import exclusion_query
qmap={}
for g,f in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]:
 for q in json.loads((H/g/f).read_text())['questions']:qmap[q[':db/id']]=q
assert len(qmap)==3012;db=connection();direct=db.query('[:find ?m ?s ?c :where [?m :multistep/steps ?s] [?s :step/content ?c]]',[],H,'multistep-edges',9122);assigned=db.query('[:find ?p ?c :where [?p :assigned-problem/content ?c]]',[],H,'assigned-edges',9122)
legacy=db.query('[:find ?a :where [?a :db/ident :multistep-step/question]]',[],H,'legacy-multistep-attribute',9122)
if legacy:direct +=db.query('[:find ?m ?s ?c :where [?m :multistep/steps ?s] [?s :multistep-step/question ?c]]',[],H,'legacy-multistep-edges',9122)
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
