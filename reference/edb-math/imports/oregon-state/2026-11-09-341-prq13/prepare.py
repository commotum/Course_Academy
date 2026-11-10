import collections,hashlib,json,re,sys,uuid,importlib.util
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,QUIZ,NAV_LINE,NAV_SECTION,UniqueKeyLoader,COURSES
from import_school_assignments import Import,PROBLEM,tidy,DEFAULT_LEARNER
from sync_f26_assignments import edn
from migrate_learner_history import connection,kw,Keyword
import yaml
V=R.parent/'study/vault';H=R/'reference/edb-math/imports/oregon-state/2026-11-09-341-prq13';REL='F26/341/11-10-26_PRQ-13.md';SEED='F26/341/PRQ-13'
def save(n,v):(H/n).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
def normalize(v):
 if isinstance(v,Keyword):return {'$keyword':str(v).lstrip(':')}
 if isinstance(v,uuid.UUID):return {'$uuid':str(v)}
 if isinstance(v,dict):return v[':db/id'] if ':db/id'in v else {str(k).lstrip(':'):normalize(x)for k,x in v.items()}
 if isinstance(v,list):return [normalize(x)for x in v]
 return v
def main():
 H.mkdir(parents=True,exist_ok=True);assert not(H/'commit-intent.json').exists()
 path=V/REL;raw=path.read_text();b=Builder(V);markers=list(PROBLEM.finditer(raw));assert [m[1]for m in markers]==list('123')
 intro=b.render_text(tidy(NAV_SECTION.sub('',raw[:markers[0].start()])),path,'instructions');contents=[b.entity(SEED,'instructions','tutorial',tutorial__title='Assignment information',tutorial__content=intro)];problems=[];targets=set();items=[]
 for i,m in enumerate(markers):
  number=m[1];body=raw[m.end():markers[i+1].start()if i+1<len(markers)else len(raw)];blocks=list(QUIZ.finditer(body));maps=b.topic_links(body,path);direct={x['topic_id']for x in maps['direct']};support={x['topic_id']for x in maps['supporting']};topics=sorted(direct|support);targets.update(topics)
  assert len(blocks)==1;block=blocks[0];q=yaml.load(block[1],Loader=UniqueKeyLoader);assert q['id']=='canvas-'+str(59459050+int(number))
  context=b.render_text(tidy(body[:block.start()]),path,'problem-'+number+'/context');qid,qa=b.question(SEED,'problem-'+number+'/question',q,path,context)
  assert not tidy(NAV_LINE.sub('',body[block.end():]))
  assigned=b.entity(SEED,'problem-'+number,'assigned-problem',assigned_problem__content=qid,assigned_problem__topic_coverage=[{'$ref':[':topic/math-academy-id',t]}for t in topics]);contents.append(assigned)
  qa['topics']=maps;problems.append({'number':int(number),'assigned_problem_id':assigned,'content_id':qid,'quizzes':[qa],'direct':sorted(direct),'supporting':sorted(support),'topics':topics});items.append({'number':int(number),'source_id':59459050+int(number),'kind':'assigned-problem','topics':topics,'content_id':assigned})
 for title in ['Topics','Prerequisites']:
  sec=re.search(r'^## '+title+r'\s*\n(.*?)(?=^## |\Z)',raw,re.M|re.S);maps=b.topic_links('**'+title+':** '+sec[1].replace('\n',' '),path);targets.update(x['topic_id']for group in ['direct','supporting']for x in maps[group])
 assert targets=={862,1195,1198,1375,1964}
 steps=b.sequence(SEED,['instructions/step','problem-1/step','problem-2/step','problem-3/step'],contents)
 activity=b.entity(SEED,'activity','activity',activity__title='MTH 341 — PRQ-13',activity__type=':activity.type/assignment',activity__steps=steps,activity__first_step=steps[0],activity__due={'$inst':'2026-11-11T07:59:00Z'},activity__course={'$ref':[':course/id',{'$uuid':COURSES['341']}]})
 b.validate();save('entities.json',b.entities)
 db=connection();basis=db.basis();requests=[]
 for row in b.entities:
  a=next(k for k in row if k.endswith('/id')and k!=':db/id');requests.append([kw(a),uuid.UUID(row[a]['$uuid'])])
 present=db.query('[:find ?a ?v ?e :in $ [[?a ?v]] :where [?e ?a ?v]]',[requests],H,'identities-before',basis);assert not present,'Existing identities require reconciliation.'
 # Also reject a pre-existing assignment with the same source quiz, under another code.
 duplicate=db.query('[:find ?e :in $ ?learner ?fragment :where [?l :learner/id ?learner] [?l :learner/assignments ?a] [?a :activity/steps ?s] [?s :step/content ?e] [?e :tutorial/content ?v] [(includes? ?v ?fragment)]]',[DEFAULT_LEARNER,'quizzes/3193301'],H,'source-identity-before',basis);assert not duplicate
 external=[[kw('topic/math-academy-id'),t]for t in sorted(targets)]+[[kw('course/id'),uuid.UUID(COURSES['341'])]]+[[kw('db/ident'),kw(x)]for x in ['activity.type/assignment','answer.type/text','answer.type/math','answer-field.type/free','answer-field.type/radio','course-academy.source/editor']]
 ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[external],H,'external-before',basis);assert len(ext)==len(external)
 learner=db.query('[:find (pull ?l [:db/id :learner/id [:learner/assignments :limit nil] [:learner/targets :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis)[0][0]
 snapshot={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):normalize(v)for k,v in r.items()}for r in [x[2]for x in ext]+[learner]}};save('snapshot.json',snapshot);model=Import(V,{});model.entities=b.entities;forms=model.transaction(snapshot,DEFAULT_LEARNER,[activity])
 topicrows={r[':topic/math-academy-id']:r for a,v,r in ext if ':topic/math-academy-id'in r};oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])};added={f[3]for f in forms if isinstance(f,list)and f[2]==':learner/targets'}
 for t in sorted(targets):
  e=topicrows[t][':db/id']
  if e not in oldtargets|added:forms.append([':db/add',learner[':db/id'],':learner/targets',e]);added.add(e)
 payload='[\n'+'\n '.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload)
 describe=lambda ns:[{'entity':topicrows[n][':db/id'],'math_academy_id':n,'title':topicrows[n][':topic/title']}for n in sorted(ns)]
 audit={'database':'math','basis_t':basis,'source':':course-academy.source/editor','learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'activities':[{'source':REL,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'title':'MTH 341 — PRQ-13','activity_id':activity,'due':'2026-11-11T07:59:00Z','problems':problems,'source_items':items}],'activity_ids':[activity],'all_requested_targets':describe(targets),'added_targets':[x for x in describe(targets)if x['entity']in added],'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in b.entities)),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'source_choice_order_preserved':True,'source_wording_issue':"Question 3's equation is called Characteristic Polynomial in its supplied choices; feedback states the precise distinction."}
 save('source-audit.json',audit);print(json.dumps({'basis':basis,'counts':audit['counts'],'topics':len(targets),'new_targets':len(added),'activity_id':activity,'sha256':audit['sha256']},indent=2))
if __name__=='__main__':main()
