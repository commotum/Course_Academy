"""Expand the official MiniExam 3 coverage upstream through saved learner targets."""
import collections,hashlib,json,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads,dumps,Tagged
from import_school_assignments import DEFAULT_LEARNER
LEARNER=DEFAULT_LEARNER
GUIDE=17592186761967
SOURCE=':course-academy.source/editor'
TITLE='MTH 341 — MiniExam 3 Preparation'
SEED='course-academy/341/mini-exam-3-preparation/from/67a9d64d-9f6b-5276-b3ba-06d503c39c11'
PATTERN='''[:db/id :activity/id :activity/title :activity/due :activity/course :activity/first-step
 {[:activity/steps :limit nil] [:db/id :step/next {:step/content [:db/id :assigned-problem/id :tutorial/content
 {[:assigned-problem/topic-coverage :limit nil] [:db/id :topic/id :topic/title :topic/math-academy-id]}]}]}]'''
def save(n,v):(H/n).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
def identity(key):return uuid.uuid5(uuid.NAMESPACE_URL,SEED+'/'+key)
def source_inputs(db,basis,prefix):
 guide=db.query('[:find (pull ?a '+PATTERN+') :in $ ?a :where [?a :activity/id _]]',[GUIDE],H,prefix+'guide',basis)[0][0]
 learner=db.query('[:find (pull ?l [:db/id {[:learner/targets :limit nil] [:db/id]} {[:learner/assignments :limit nil] [:db/id]}]) :in $ ?id :where [?l :learner/id ?id]]',[LEARNER],H,prefix+'learner',basis)[0][0]
 edges=db.query('[:find ?a ?b :where [?a :topic/next ?b]]',[],H,prefix+'edges',basis)
 nodes=db.query('[:find ?e ?id ?title :where [?e :topic/id ?id] [?e :topic/title ?title]]',[],H,prefix+'nodes',basis)
 return guide,learner,edges,nodes
def main():
 assert not(H/'commit-intent.json').exists(),'Recover existing durable intent.'
 db=connection();basis=db.basis();guide,learner,edges,rows=source_inputs(db,basis,'before-')
 assert str(guide[':activity/id'])=='67a9d64d-9f6b-5276-b3ba-06d503c39c11'
 steps={s[':db/id']:s for s in guide[':activity/steps']};cursor=guide[':activity/first-step'][':db/id'];problems=[];seen=set()
 while cursor:
  assert cursor not in seen;seen.add(cursor);step=steps[cursor];c=step[':step/content']
  if ':assigned-problem/id'in c:problems.append(c)
  cursor=step.get(':step/next',{}).get(':db/id')
 assert len(seen)==len(steps)and len(problems)==4
 root_problems=collections.defaultdict(set)
 for i,p in enumerate(problems,1):
  for t in p.get(':assigned-problem/topic-coverage',[]):root_problems[t[':db/id']].add(i)
 roots=set(root_problems);targets={t[':db/id']for t in learner[':learner/targets']}
 incoming=collections.defaultdict(set);outgoing=collections.defaultdict(set)
 for a,b in edges:incoming[b].add(a);outgoing[a].add(b)
 # Traverse through every prerequisite, including non-target bridge topics.
 reach=collections.defaultdict(set)
 for root in roots:
  todo=[root];visited={root}
  while todo:
   n=todo.pop();reach[n].add(root)
   for p in incoming[n]:
    if p not in visited:visited.add(p);todo.append(p)
 ancestry=set(reach);selected=ancestry&targets
 nodes={e:{'id':e,'uuid':str(i),'title':t}for e,i,t in rows}
 allnodes=set(nodes)|set(incoming)|set(outgoing)
 assert selected<=nodes.keys(),'A selected target lacks a title or identity'
 degree={e:len(incoming[e])for e in allnodes};layer={e:0 for e in allnodes};todo=[e for e in allnodes if not degree[e]]
 for e in todo:
  for n in outgoing[e]:
   layer[n]=max(layer[n],layer[e]+1);degree[n]-=1
   if degree[n]==0:todo.append(n)
 assert len(todo)==len(allnodes),'Prerequisite graph contains a cycle'
 ordered=sorted(selected,key=lambda e:(layer[e],nodes[e]['title'],e));assert roots<=selected,'Source coverage includes non-target topics; review selection before writing.'
 assert all(layer[a]<layer[b]for a,b in edges)
 entities=[]
 def entity(key,kind,attrs):
  uid=str(identity(key));row={kw('db/id'):uid,kw(kind+'/id'):identity(key),kw('db/ensure'):kw(kind+'/validate')};row.update({kw(k):v for k,v in attrs.items()});entities.append(row);return uid
 due=guide.get(':activity/due');assert due
 intro=(f'**{TITLE}**\n\nSource: [{guide[":activity/title"]}](http://127.0.0.1:8765/assignments?assignment={guide[":activity/id"]}).\n\n'
  'Due: November 13, 2026, at 11:59 p.m. Pacific, inherited from the official guide.\n\n'
  f'The official guide supplies {len(roots)} starting coverage topics across its four items, including the coursework review reminder. '
  'Trace all prerequisite paths upstream from that coverage, then retain the topics that are in your saved targets. '
  f'This gives **{len(ordered)} targets**: **{len(roots)} guide coverage topics** and **{len(selected-roots)} additional upstream targets**.\n\n'
  'The list includes targets already studied and orders everything by global prerequisite layer, using the same ordering as the earlier Quiz 3 preparation assignment. '
  'Each item links to its topic and identifies its connection to the guide. Use this to place the exam material within your broader study goals and work through shared prerequisites efficiently.')
 contents=[entity('instructions','tutorial',{'tutorial/title':'Official guide and upstream target scope','tutorial/content':intro})]
 topics=[]
 for e in ordered:
  n=nodes[e];source_items=sorted({p for root in reach[e]for p in root_problems[root]});direct=sorted(root_problems.get(e,[]))
  relation=('Guide coverage: item'+('s 'if len(direct)>1 else' ')+', '.join(map(str,direct))+'.')if direct else('Upstream of coverage on guide item'+('s 'if len(source_items)>1 else' ')+', '.join(map(str,source_items))+'.')
  prompt=f'Study or review **{n["title"]}**.\n\nGlobal layer: **L{layer[e]+1:02d}**.\n\n{relation}\n\n[Open topic](http://127.0.0.1:8765/topic?topic={n["uuid"]})'
  q=entity(f'topic/{e}/prompt','question',{'question/problem':prompt})
  contents.append(entity(f'topic/{e}/assigned','assigned-problem',{'assigned-problem/content':q,'assigned-problem/topic-coverage':[e]}))
  topics.append({**n,'layer':layer[e]+1,'guide_coverage':bool(direct),'direct_guide_items':direct,'upstream_guide_items':source_items})
 keys=['instructions/step']+[f'topic/{e}/step'for e in ordered];sids=[str(identity(k))for k in keys]
 for i,(key,content)in enumerate(zip(keys,contents)):
  attrs={'step/content':content}
  if i+1<len(sids):attrs['step/next']=sids[i+1]
  entity(key,'step',attrs)
 activity=entity('activity','activity',{'activity/title':TITLE,'activity/type':kw('activity.type/assignment'),'activity/course':guide[':activity/course'][':db/id'],'activity/due':Tagged('inst',due),'activity/steps':sids,'activity/first-step':sids[0]})
 identities=[[k,v]for e in entities for k,v in e.items()if str(k).endswith('/id')and str(k)!=':db/id']
 existing=db.query('[:find ?e :in $ [[?a ?id]] :where [?e ?a ?id]]',[identities],H,'identities-before',basis);assert not existing,'An expansion already exists; reconcile instead of duplicating.'
 similar=db.query('[:find ?e :in $ ?title :where [?e :activity/title ?title]]',[TITLE],H,'title-before',basis);assert not similar
 source=db.query('[:find ?e :in $ ?ident :where [?e :db/ident ?ident]]',[kw(SOURCE)],H,'source-before',basis);assert len(source)==1
 forms=entities+[[kw('db/add'),learner[':db/id'],kw('learner/assignments'),activity]]
 payload=dumps(forms)+'\n';(H/'transaction.edn').write_text(payload);(H/'entities.edn').write_text(dumps(entities)+'\n')
 audit={'basis':basis,'source':SOURCE,'source_entity':source[0][0],'guide_entity':GUIDE,'guide_uuid':str(guide[':activity/id']),'activity_uuid':activity,'title':TITLE,'course_entity':guide[':activity/course'][':db/id'],'learner_entity':learner[':db/id'],'due':due,'due_local':'2026-11-13T23:59:00-08:00','root_topic_ids':sorted(roots),'source_problem_ids':[p[':db/id']for p in problems],'all_ancestor_topic_ids':sorted(ancestry),'topic_ids':ordered,'topics':topics,'topic_count':len(ordered),'root_count':len(roots),'upstream_target_count':len(selected-roots),'old_target_ids':sorted(targets),'old_assignment_ids':sorted(t[':db/id']for t in learner[':learner/assignments']),'new_entities':len(entities),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'fieldless_study_items':True}
 save('audit.json',audit)
 save('render-input.json',[{'entity':e[':db/id'],'attribute':a,'value':e[a]}for e in entities for a in [':tutorial/content',':question/problem']if a in e])
 print(json.dumps({k:audit[k]for k in ['basis','root_count','upstream_target_count','topic_count','activity_uuid','new_entities','due_local']},indent=2))
if __name__=='__main__':main()
