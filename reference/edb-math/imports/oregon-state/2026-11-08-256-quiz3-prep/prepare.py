"""Prepare the user-requested Quiz 3 study assignment from existing target paths."""
import collections,hashlib,json,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads,dumps,Tagged
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
ANNOUNCEMENT="""Hi All,

I posted Written Homework 4 and WebWork 4. Problems 1 and 2 of Written Homework 4 and 1-9 of the WebWork 4 relate to material that will be assessed on Quiz 3 which has been pushed back to week 7.

Best,

Pat"""
def save(name,v):(H/name).write_text(json.dumps(v,default=str,indent=2)+'\n')
def identity(key):return uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/256/quiz3-preparation/2026-11-10/'+key)
def main():
 assert not (H/'commit-intent.json').exists(),'An intent already exists; recover it without regenerating.'
 db=connection();basis=db.basis()
 s=json.load(open('/tmp/exam-target-graph-current.json'));assert basis==s['basis']
 edges=db.query('[:find ?a ?b :where [?a :topic/next ?b]]',[],H,'edges-before',basis)
 assert {tuple(e) for e in edges}=={(e['source'],e['target']) for e in s['links']}
 learner=db.query('[:find (pull ?l [:db/id {[:learner/targets :limit nil] [:db/id]} {[:learner/assignments :limit nil] [:db/id]}]) :in $ ?id :where [?l :learner/id ?id]]',[LEARNER],H,'learner-before',basis)[0][0]
 targets={t[':db/id'] for t in learner[':learner/targets']};assert targets==set(s['learner']['targets'])
 course=db.query('[:find ?c :in $ ?code :where [?c :course/code ?code]]',['MTH 256'],H,'course-before',basis);assert len(course)==1;course=course[0][0]
 source=db.query('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]',[kw('course-academy.source/editor')],H,'source-before',basis);assert len(source)==1
 roots=set();source_problems=[]
 for name,limit in [('whw',2),('ohw',9)]:
  a=json.load(open('/tmp/exam-256-'+name+'4-fresh.json'))['assignment']
  ps=[st['content'] for st in a['steps'] if st['content'].get('kind')=='assigned-problem'][:limit]
  source_problems.extend(p['entityId'] for p in ps)
 coverage=db.query('[:find ?p ?t :in $ [?p ...] :where [?p :assigned-problem/topic-coverage ?t]]',[source_problems],H,'exam-coverage-before',basis)
 roots={t for _,t in coverage};assert len(roots)==15
 incoming=collections.defaultdict(set);outgoing=collections.defaultdict(set)
 for a,b in edges:incoming[b].add(a);outgoing[a].add(b)
 ancestry=set(roots);pending=list(roots)
 while pending:
  for p in incoming[pending.pop()]:
   if p not in ancestry:ancestry.add(p);pending.append(p)
 selected=ancestry&targets;assert len(selected)==105
 nodes={n['id']:n for n in s['nodes']};degree={i:len(incoming[i]) for i in nodes};layer={i:0 for i in nodes};todo=[i for i in nodes if degree[i]==0]
 for i in todo:
  for n in outgoing[i]:
   layer[n]=max(layer[n],layer[i]+1);degree[n]-=1
   if not degree[n]:todo.append(n)
 assert len(todo)==len(nodes)
 ordered=sorted(selected,key=lambda i:(layer[i],nodes[i]['name'],i))
 entities=[]
 def entity(key,kind,attrs):
  temp=str(identity(key));record={kw('db/id'):temp,kw(kind+'/id'):identity(key),kw('db/ensure'):kw(kind+'/validate')};record.update({kw(k):v for k,v in attrs.items()});entities.append(record);return temp
 intro='**MTH 256 — Quiz 3 Preparation**\n\nDue: Tuesday, November 10, 2026, at 11:59:59 p.m. America/Los_Angeles (PST).\n\nProfessor Pat’s announcement:\n\n'+'\n'.join('> '+line if line else '>' for line in ANNOUNCEMENT.splitlines())+'\n\nStudy scope: the 15 topics mapped to Written Homework 4 problems 1–2 and WebWork 4 problems 1–9, plus all their prerequisite ancestors that are in your saved targets. All 105 topics are included in global layer order, including topics already studied. Each item links to its topic for study or review.'
 contents=[entity('announcement','tutorial',{'tutorial/title':'Pat’s announcement and study scope','tutorial/content':intro})]
 for i in ordered:
  n=nodes[i]
  question=entity(f'topic/{i}/prompt','question',{'question/problem':f"Study or review **{n['name']}**.\n\nGlobal layer: **L{layer[i]+1:02d}**.\n\n[Open topic](/topic?topic={n['uuid']})"})
  contents.append(entity(f'topic/{i}/assigned','assigned-problem',{'assigned-problem/content':question,'assigned-problem/topic-coverage':[i]}))
 stepkeys=['announcement/step']+[f'topic/{i}/step' for i in ordered];steps=[str(identity(k)) for k in stepkeys]
 for j,(key,content) in enumerate(zip(stepkeys,contents)):
  attrs={'step/content':content}
  if j+1<len(steps):attrs['step/next']=steps[j+1]
  assert entity(key,'step',attrs)==steps[j]
 activity=entity('activity','activity',{'activity/title':'MTH 256 — Quiz 3 Preparation','activity/type':kw('activity.type/assignment'),'activity/course':course,'activity/due':Tagged('inst','2026-11-11T07:59:59.000Z'),'activity/steps':steps,'activity/first-step':steps[0]})
 existing=db.query('[:find ?e :in $ ?id :where [?e :activity/id ?id]]',[identity('activity')],H,'identity-before',basis);assert not existing
 forms=entities+[[kw('db/add'),learner[':db/id'],kw('learner/assignments'),activity]]
 text=dumps(forms)+'\n';(H/'transaction.edn').write_text(text)
 assert len(entities)==318
 audit={'basis':basis,'source':':course-academy.source/editor','announcement':ANNOUNCEMENT,'activity_uuid':activity,'course_entity':course,'learner_entity':learner[':db/id'],'due':'2026-11-11T07:59:59.000Z','due_local':'2026-11-10T23:59:59-08:00','topic_count':len(ordered),'root_topic_ids':sorted(roots),'source_problem_ids':source_problems,'topic_ids':ordered,'topics':[{'id':i,'uuid':nodes[i]['uuid'],'title':nodes[i]['name'],'layer':layer[i]+1} for i in ordered],'old_target_ids':sorted(targets),'old_assignment_ids':sorted(t[':db/id'] for t in learner[':learner/assignments']),'new_entities':len(entities),'sha256':hashlib.sha256(text.encode()).hexdigest(),'fieldless_study_items':True}
 save('audit.json',audit);print(json.dumps({k:audit[k] for k in ('basis','activity_uuid','due_local','topic_count','new_entities','sha256')},indent=2))
if __name__=='__main__':main()
