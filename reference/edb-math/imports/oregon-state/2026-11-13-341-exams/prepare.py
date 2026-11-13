import collections,hashlib,json,re,sys,uuid
from pathlib import Path
from datetime import datetime,timezone
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,COURSES,PROBLEM,QUIZ,NAV_SECTION,UniqueKeyLoader
from import_school_assignments import Import,DEFAULT_LEARNER,tidy
from migrate_learner_history import connection,kw,Keyword
from sync_f26_assignments import edn
import yaml
V=R.parent/'study/vault';H=R/'reference/edb-math/imports/oregon-state/2026-11-13-341-exams'
def save(n,v):(H/n).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
def normalize(v):
 if isinstance(v,Keyword):return {'$keyword':str(v).lstrip(':')}
 if isinstance(v,uuid.UUID):return {'$uuid':str(v)}
 if isinstance(v,dict):return v[':db/id']if ':db/id'in v else{str(k).lstrip(':'):normalize(x)for k,x in v.items()}
 if isinstance(v,list):return[normalize(x)for x in v]
 return v
class ExamBuilder(Builder):
 def render_text(self,value,path,location):
  value=re.sub(r'^Source capture:.*$','Source capture: original Canvas questions, responses, and scores archived with this import.',value,flags=re.M)
  return super().render_text(value,path,location)
 def canonical_question(self,source,key,q,path,context=''):
  if all(f['type']=='radio' for f in q['fields']):
   fs=[];fa=[]
   for f in q['fields']:
    options={}
    for c in f['choices']:
     options[c['id']]=self.entity(source,key+'/'+f['key']+'/option-'+c['id'],'answer',answer__type=':answer.type/'+c['type'],answer__value=c['value'] if c['type']=='math' else self.render_text(c['value'],path,q['id']+'/'+c['id']),answer__feedback=self.render_text(c['feedback'],path,q['id']+'/'+c['id']+'/feedback'))
    fid=self.entity(source,key+'/'+f['key'],'answer-field',answer_field__key=f['key'],answer_field__type=':answer-field.type/radio',answer_field__choices=list(options.values()),answer_field__correct=options[f['correct']]);fs.append(fid);fa.append({'key':f['key'],'type':'radio','field_id':fid,'options':options,'correct_answer_id':options[f['correct']]})
   uid=self.entity(source,key,'question',question__problem=self.render_text(tidy(context+'\n\n'+q['content']),path,q['id']),question__answer_fields=fs,question__worked_solution=self.render_text(q['feedback'],path,q['id']+'/feedback'))
   return uid,{'question_id':uid,'quiz_id':q['id'],'fields':fa}
  fs=[];fa=[]
  for f in q['fields']:
   assert set(f)=={'key','type','correct'}and f['type']in['blank','free'];c=f['correct'];assert c['type']in['math','text']
   aid=self.entity(source,key+'/'+f['key']+'/canonical','answer',answer__type=':answer.type/'+c['type'],answer__value=c['value']if c['type']=='math'else self.render_text(c['value'],path,q['id']+'/canonical'))
   fid=self.entity(source,key+'/'+f['key'],'answer-field',answer_field__key=f['key'],answer_field__type=':answer-field.type/'+f['type'],answer_field__choices=[aid],answer_field__correct=aid)
   fs.append(fid);fa.append({'key':f['key'],'type':f['type'],'field_id':fid,'correct_answer_id':aid})
  uid=self.entity(source,key,'question',question__problem=self.render_text(tidy(context+'\n\n'+q['content']),path,q['id']),question__answer_fields=fs,question__worked_solution=self.render_text(q['feedback'],path,q['id']+'/feedback'))
  return uid,{'question_id':uid,'quiz_id':q['id'],'fields':fa}
 def exam(self,n):
  relative=f'F26/341/{"10-16-26"if n==1 else"10-30-26"}_E-{n}.md';path=V/relative;raw=path.read_text();data=json.loads((V/f'F26/source/341/E-{n}/canvas-submission.json').read_text());source=f'F26/341/E-{n}';marks=list(PROBLEM.finditer(raw));assert len(marks)==len(data['questions'])
  contents=[self.entity(source,'instructions','tutorial',tutorial__title='Original exam and submission information',tutorial__content=self.render_text(tidy(NAV_SECTION.sub('',raw[:marks[0].start()])),path,'instructions'))];problems=[]
  for j,m in enumerate(marks):
   num=j+1;body=raw[m.end():marks[j+1].start()if j+1<len(marks)else len(raw)];blocks=list(QUIZ.finditer(body));assert len(blocks)==1;match=blocks[0];q=yaml.load(match[1],Loader=UniqueKeyLoader);assert q['id']==f'q-{num}'
   context=tidy(body[:match.start()]);qid,qa=self.question(source,f'problem-{num}/question',q,path,context);maps=self.topic_links(body,path);direct=sorted({x['topic_id']for x in maps['direct']});support=sorted({x['topic_id']for x in maps['supporting']});topics=sorted(set(direct+support));qa['topics']=maps
   pid=self.entity(source,f'problem-{num}','assigned-problem',assigned_problem__content=qid,assigned_problem__topic_coverage=[{'$ref':[':topic/math-academy-id',t]}for t in topics]);contents.append(pid);problems.append({'number':num,'content_id':qid,'assigned_problem_id':pid,'topics':topics,'direct':direct,'supporting':support,'quizzes':[qa]})
  steps=self.sequence(source,['instructions/step']+[f'problem-{i}/step'for i in range(1,len(problems)+1)],contents)
  due=datetime.fromisoformat(data['due_local']).astimezone(timezone.utc).isoformat().replace('+00:00','Z');activity=self.entity(source,'activity','activity',activity__title=data['title'],activity__type=':activity.type/assignment',activity__steps=steps,activity__first_step=steps[0],activity__course={'$ref':[':course/id',{'$uuid':COURSES['341']}]},activity__due={'$inst':due})
  # The existing assignment reader derives occurrence IDs from task UUID and leaf step UUID.
  task_uuid=str(uuid.uuid5(uuid.NAMESPACE_URL,f'canvas/2064363/{data["canvas_assignment"]}/6660414/attempt/1'));records={e[':db/id']:e for e in self.entities};items=[];responses=[];ended=datetime.fromisoformat(data['submitted_local']).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
  for p,step,qsrc in zip(problems,steps[1:],data['questions']):
   q=records[p['content_id']];submitted=[];fs=[records[f]for f in q[':question/answer-fields']]
   if qsrc['kind']=='radio':
    field=fs[0];mapping=p['quizzes'][0]['fields'][0]['options'];submitted=[mapping[str(qsrc['submitted'])]]
   else:
    values=[qsrc['submitted']]if qsrc['kind']=='free'else qsrc['submitted']
    for field,value in zip(fs,values):
     canonical=records[field[':answer-field/correct']]
     if canonical[':answer/value']==value:aid=canonical[':db/id']
     else:
      aid=self.entity(source,f'historical/response-{p["number"]}/{field[":answer-field/key"]}','answer',answer__type=canonical[':answer/type'],answer__value=value);field[':answer-field/choices'].append(aid)
     submitted.append(aid)
   digest=bytearray(hashlib.sha256(json.dumps(['assignment-occurrence-v1',task_uuid,step],separators=(',',':'),ensure_ascii=True).encode()).digest()[:16]);digest[6]=(digest[6]&15)|128;digest[8]=(digest[8]&63)|128;uid=str(uuid.UUID(bytes=bytes(digest)))
   state='completed'if qsrc['kind']=='free'else('correct'if qsrc['awarded']==qsrc['points']else'incorrect');row={':db/id':uid,':task-item/id':{'$uuid':uid},':task-item/content':p['content_id'],':task-item/status':':task-item.status/'+state,':task-item/responses':submitted,':task-item/working-ended-at':{'$inst':ended},':db/ensure':':task-item/validate'};self.entities.append(row);items.append(uid);responses.append({'number':p['number'],'item_uuid':uid,'question_uuid':p['content_id'],'step_uuid':step,'response_answer_ids':submitted,'status':state,'awarded':qsrc['awarded'],'points':qsrc['points']})
  for a,b in zip(items,items[1:]):next(e for e in self.entities if e[':db/id']==a)[':task-item/next']=b
  self.entities.append({':db/id':task_uuid,':learner-task/id':{'$uuid':task_uuid},':learner-task/activity':activity,':learner-task/status':':learner-task.status/completed',':learner-task/items':items,':learner-task/finished-at':{'$inst':ended},':db/ensure':':learner-task/validate'})
  self.audit['activities'].append({'source':relative,'identity_source':source,'title':data['title'],'activity_id':activity,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'due':due,'due_convention':'Verified Canvas date at 23:59 PDT.','problems':problems,'task_uuid':task_uuid,'submitted_at':ended,'timestamp_precision':'minute','historical_responses':responses,'canvas_score':data['score'],'canvas_points_possible':data['points_possible']})
  return activity

def main():
 H.mkdir(parents=True,exist_ok=True);assert not(H/'commit-intent.json').exists();b=ExamBuilder(V);activities=[b.exam(n)for n in[1,2]];b.validate();save('entities.json',b.entities)
 targets={t for a in b.audit['activities']for p in a['problems']for t in p['topics']}
 for a in b.audit['activities']:
  raw=(V/a['source']).read_text()
  for k in['Topics','Prerequisites']:
   s=re.search(r'^## '+k+r'\s*\n(.*?)(?=^## )',raw,re.M|re.S);m=b.topic_links('**'+k+':** '+s[1].replace('\n',' '),V/a['source']);targets.update(t['topic_id']for group in['direct','supporting']for t in m[group])
 db=connection();basis=db.basis();ids=[[kw(k),uuid.UUID(v['$uuid'])]for r in b.entities for k,v in r.items()if k.endswith('/id')and k!=':db/id'];assert not db.query('[:find ?e :in $ [[?a ?id]] :where [?e ?a ?id]]',[ids],H,'identities-before',basis),'Existing exams require reconciliation'
 enums=['activity.type/assignment','answer.type/text','answer.type/math','answer-field.type/radio','answer-field.type/blank','answer-field.type/free','learner-task.status/completed','task-item.status/completed','task-item.status/correct','task-item.status/incorrect','course-academy.source/editor']
 extids=[[kw('topic/math-academy-id'),t]for t in sorted(targets)]+[[kw('course/id'),uuid.UUID(COURSES['341'])]]+[[kw('db/ident'),kw(x)]for x in enums]
 ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[extids],H,'external-before',basis);assert len(ext)==len(extids)
 learner=db.query('[:find (pull ?l [:db/id :learner/id [:learner/assignments :limit nil] [:learner/targets :limit nil] [:learner/activity :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis)[0][0]
 snap={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):normalize(v)for k,v in r.items()}for r in[x[2]for x in ext]+[learner]}};save('snapshot.json',snap);m=Import(V,{});m.entities=b.entities;forms=m.transaction(snap,DEFAULT_LEARNER,activities)
 for a in b.audit['activities']:forms.append([':db/add',learner[':db/id'],':learner/activity',a['task_uuid']])
 payload='[\n'+'\n'.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload)
 topicrows={r[':topic/math-academy-id']:r for _,_,r in ext if ':topic/math-academy-id'in r};oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])}
 audit={'basis_t':basis,'source':':course-academy.source/editor','learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'activities':b.audit['activities'],'activity_ids':activities,'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'old_task_eids':sorted(x[':db/id']for x in learner.get(':learner/activity',[])),'all_requested_targets':[{'entity':topicrows[t][':db/id'],'math_academy_id':t,'title':topicrows[t][':topic/title']}for t in sorted(targets)],'added_targets':[{'entity':topicrows[t][':db/id'],'math_academy_id':t,'title':topicrows[t][':topic/title']}for t in sorted(targets)if topicrows[t][':db/id']not in oldtargets],'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in b.entities)),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'historical_import':'24 actual Canvas responses; original dates have minute precision; scores preserved in source and reveal feedback. Free responses are completed without assigning correctness or mastery.'};save('source-audit.json',audit)
 save('render-input.json',[{'entity':r[':db/id'],'attribute':attr,'value':r[attr],'bare_math':attr==':answer/value'and r[':answer/type']==':answer.type/math'}for r in b.entities for attr in[':tutorial/content',':question/problem',':question/worked-solution',':answer/value',':answer/feedback']if attr in r])
 print(json.dumps({'basis':basis,'counts':audit['counts'],'targets':len(targets),'new_targets':len(audit['added_targets']),'already_targets':len(targets)-len(audit['added_targets']),'activity_ids':activities},indent=2))
if __name__=='__main__':main()
