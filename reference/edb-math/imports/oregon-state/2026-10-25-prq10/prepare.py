"""Prepare this assignment only, using existing canonical quiz/assignment builders."""
import collections,hashlib,json,re,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,QUIZ,NAV_LINE,NAV_SECTION,UniqueKeyLoader,COURSES
from import_school_assignments import Import,PROBLEM,tidy,DEFAULT_LEARNER
from sync_f26_assignments import edn
from migrate_learner_history import connection,kw,Keyword
import yaml
V=R.parent/'study/vault';REL='F26/341/10-27-26_PRQ-10.md';SEED='F26/341/PRQ-10'
def save(name,v):(H/name).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
def normalize(v):
 if isinstance(v,Keyword):return {'$keyword':str(v).lstrip(':')}
 if isinstance(v,uuid.UUID):return {'$uuid':str(v)}
 if isinstance(v,dict):return v[':db/id'] if ':db/id'in v else {str(k).lstrip(':'):normalize(x)for k,x in v.items()}
 if isinstance(v,list):return [normalize(x)for x in v]
 return v
def main():
 assert not(H/'commit-intent.json').exists(),'Do not regenerate a pending intent'
 path=V/REL;raw=path.read_text();builder=Builder(V);markers=list(PROBLEM.finditer(raw));assert [m[1]for m in markers]==list('123456')
 intro=builder.render_text(tidy(NAV_SECTION.sub('',raw[:markers[0].start()])),path,'instructions');contents=[builder.entity(SEED,'instructions','tutorial',tutorial__title='Assignment information',tutorial__content=intro)];problems=[]
 for i,m in enumerate(markers):
  number=m[1];body=raw[m.end():markers[i+1].start()if i+1<len(markers)else len(raw)];blocks=list(QUIZ.finditer(body));assert len(blocks)==1;block=blocks[0];quiz=yaml.load(block[1],Loader=UniqueKeyLoader);assert quiz['id']=='canvas-'+str(59459018+int(number));assert quiz['fields'][0]['type']=='radio'
  context=builder.render_text(tidy(body[:block.start()]),path,'problem-'+number+'/context');qid,qa=builder.question(SEED,'problem-'+number+'/question',quiz,path,context);tail=body[block.end():];mapping_tail=tail.split('**Closing reading reminder**',1)[0];maps=builder.topic_links(mapping_tail,path);topics=sorted({x['topic_id']for group in ['direct','supporting']for x in maps[group]});extra=tidy(NAV_LINE.sub('',tail))
  if number=='6':assert extra.startswith('**Closing reading reminder**');reminder=builder.render_text(extra,path,'closing-reminder')
  else:assert not extra
  ap=builder.entity(SEED,'problem-'+number,'assigned-problem',assigned_problem__content=qid,assigned_problem__topic_coverage=[{'$ref':[':topic/math-academy-id',t]}for t in topics]);contents.append(ap);problems.append({'number':int(number),'question_id':qid,'assigned_problem_id':ap,'quizzes':[qa],'direct':sorted({x['topic_id']for x in maps['direct']}),'supporting':sorted({x['topic_id']for x in maps['supporting']}),'topics':topics,'mapping_evidence':maps,'coverage':'Component coverage only; source explicitly does not claim whole-task equivalence.'})
 contents.append(builder.entity(SEED,'closing-reminder','tutorial',tutorial__title='Closing reading reminder',tutorial__content=reminder));keys=['instructions/step']+[f'problem-{n}/step'for n in range(1,7)]+['closing-reminder/step'];steps=builder.sequence(SEED,keys,contents)
 assert 'Due: 2026-10-27'in raw and 'Due time: 11:59 p.m. PDT'in raw
 activity=builder.entity(SEED,'activity','activity',activity__title='MTH 341 — PRQ-10',activity__type=':activity.type/assignment',activity__steps=steps,activity__first_step=steps[0],activity__due={'$inst':'2026-10-28T06:59:00Z'},activity__course={'$ref':[':course/id',{'$uuid':COURSES['341']}]});builder.validate();save('entities.json',builder.entities)
 db=connection();basis=db.basis();requests=[]
 for row in builder.entities:
  attr=next(k for k in row if k.endswith('/id')and k!=':db/id');requests.append([kw(attr),uuid.UUID(row[attr]['$uuid'])])
 present=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[requests],H,'identities-before',basis);assert not present,'Assignment identities already exist; review instead of overwriting'
 targets=sorted({t for p in problems for t in p['topics']});external=[[kw('topic/math-academy-id'),t]for t in targets]+[[kw('course/id'),uuid.UUID(COURSES['341'])],[kw('db/ident'),kw('activity.type/assignment')],[kw('db/ident'),kw('answer.type/text')],[kw('db/ident'),kw('answer-field.type/radio')],[kw('db/ident'),kw('course-academy.source/editor')]]
 ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[external],H,'external-before',basis);assert len(ext)==len(external)
 learner=db.query('[:find (pull ?l [:db/id :learner/id :learner/assignments :learner/targets]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis)[0][0]
 records=[row for a,v,row in ext]+[learner];snapshot={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):normalize(v)for k,v in r.items()}for r in records}}
 save('snapshot.json',snapshot);model=Import(V,{});model.entities=builder.entities;forms=model.transaction(snapshot,DEFAULT_LEARNER,[activity]);payload='[\n'+'\n '.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload)
 topicrows={r[':topic/math-academy-id']:r for a,v,r in ext if ':topic/math-academy-id'in r};oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])};describe=lambda ns:[{'entity':topicrows[n][':db/id'],'math_academy_id':n,'title':topicrows[n][':topic/title']}for n in ns]
 requested=describe(targets);added=[x for x in requested if x['entity']not in oldtargets];audit={'database':'math','basis_t':basis,'learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'activities':[{'source':REL,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'title':'MTH 341 — PRQ-10','activity_id':activity,'due':'2026-10-28T06:59:00Z','problems':problems}],'activity_ids':[activity],'source':':course-academy.source/editor','all_requested_targets':requested,'added_targets':added,'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'direct_topics':describe(sorted({t for p in problems for t in p['direct']})),'explicit_prerequisites':describe(sorted({t for p in problems for t in p['supporting']})),'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in builder.entities)),'forms':len(forms),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'vault_unchanged':True,'reading_reminder_is_noninteractive':True}
 save('source-audit.json',audit);print(json.dumps({k:audit[k]for k in ['basis_t','counts','added_targets','direct_topics','explicit_prerequisites','sha256']},indent=2))
if __name__=='__main__':main()
