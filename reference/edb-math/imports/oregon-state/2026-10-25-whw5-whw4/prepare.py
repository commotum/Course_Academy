"""Add exactly two reviewed assignments with native blank/free fields and targets."""
import collections,hashlib,json,re,sys,uuid
from datetime import datetime,date,time,timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import yaml
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,QUIZ,NAV_LINE,NAV_SECTION,UniqueKeyLoader,COURSES
from import_school_assignments import Import,PROBLEM,tidy,DEFAULT_LEARNER
from sync_f26_assignments import edn
from migrate_learner_history import connection,kw,Keyword
V=R.parent/'study/vault';SOURCES=[('F26/255/10-29-26_WHW-5.md',5,34),('F26/341/10-28-26_WHW-4.md',13,15)]
def save(name,v):(H/name).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
def normalize(v):
 if isinstance(v,Keyword):return {'$keyword':str(v).lstrip(':')}
 if isinstance(v,uuid.UUID):return {'$uuid':str(v)}
 if isinstance(v,dict):return v[':db/id']if ':db/id'in v else {str(k).lstrip(':'):normalize(x)for k,x in v.items()}
 if isinstance(v,list):return [normalize(x)for x in v]
 return v
class AssignmentBuilder(Builder):
 def native_question(self,source,key,q,path,context=''):
  assert set(q)<={'id','content','fields','feedback','shuffle','gated'};prompt=self.render_text(q['content'],path,q['id']);assert len(q['fields'])==1;f=q['fields'][0];assert set(f)=={'key','type','correct'};kind=f['type'];assert kind in ['blank','free'];a=f['correct'];assert set(a)=={'type','value'}and a['type']in ['text','math'];answer=self.entity(source,key+'/'+f['key']+'/canonical','answer',answer__type=':answer.type/'+a['type'],answer__value=self.render_text(a['value'],path,q['id']+'/canonical'));fid=self.entity(source,key+'/'+f['key'],'answer-field',answer_field__key=f['key'],answer_field__type=':answer-field.type/'+kind,answer_field__choices=[answer],answer_field__correct=answer)
  if '{{'+f['key']+'}}'not in prompt:
   assert kind=='free' 
  attrs={'question__problem':tidy(context+'\n\n'+prompt),'question__answer_fields':[fid]}
  if q.get('feedback'):attrs['question__worked_solution']=self.render_text(q['feedback'],path,q['id']+'/feedback')
  uid=self.entity(source,key,'question',**attrs);return uid,{'quiz_id':q['id'],'question_id':uid,'source_field_type':kind,'answer_type':a['type'],'field_id':fid,'answer_id':answer}
 def assignment(self,relative,problem_count,quiz_count):
  path=self.vault/relative;raw=path.read_text();course=path.parent.name;code=path.stem.split('_',1)[1];seed=f'F26/{course}/{code}';prefix=f'mth{course}-{code.lower().replace("-","")}-';markers=list(PROBLEM.finditer(raw));assert [int(m[1])for m in markers]==list(range(1,problem_count+1));assert len(list(QUIZ.finditer(raw)))==quiz_count
  intro=self.render_text(tidy(NAV_SECTION.sub('',raw[:markers[0].start()])),path,'instructions');contents=[self.entity(seed,'instructions','tutorial',tutorial__title='Assignment information',tutorial__content=intro)];problems=[];seen=set()
  for i,m in enumerate(markers):
   n=m[1];body=raw[m.end():markers[i+1].start()if i+1<len(markers)else len(raw)];blocks=list(QUIZ.finditer(body));assert blocks;context=self.render_text(tidy(body[:blocks[0].start()]),path,f'problem-{n}/context');questions=[];qa=[];direct=set();support=set();parts=[]
   for j,block in enumerate(blocks):
    q=yaml.load(block[1],Loader=UniqueKeyLoader);assert q['id']not in seen;seen.add(q['id']);label=re.fullmatch(re.escape(prefix+n)+r'([a-z]*)',q['id']);assert label,(relative,q['id']);part=label[1];assert part or len(blocks)==1;parts.append(part);key=f'problem-{n}/part-{part}'if part else f'problem-{n}/question';uid,audit=self.native_question(seed,key,q,path,context if len(blocks)==1 else'');questions.append(uid)
    tail=body[block.end():blocks[j+1].start()if j+1<len(blocks)else len(body)];assert not tidy(NAV_LINE.sub('',tail)),(relative,q['id'],'Unowned trailing material');maps=self.topic_links(tail,path);direct.update(x['topic_id']for x in maps['direct']);support.update(x['topic_id']for x in maps['supporting']);audit['mapping_evidence']=maps;audit['source_study_links']=[x[0]for x in NAV_LINE.finditer(tail)];qa.append(audit)
   if len(questions)>1:
    inner=self.sequence(seed,[f'problem-{n}/part-{p}/step'for p in parts],questions);attrs={'multistep__steps':inner,'multistep__first_step':inner[0]}
    if context:attrs['multistep__context']=context
    content=self.entity(seed,f'problem-{n}/multistep','multistep',**attrs)
   else:content=questions[0]
   topics=sorted(direct|support);assigned=self.entity(seed,f'problem-{n}','assigned-problem',assigned_problem__content=content,assigned_problem__topic_coverage=[{'$ref':[':topic/math-academy-id',t]}for t in topics]);contents.append(assigned);problems.append({'number':int(n),'assigned_problem_id':assigned,'content_id':content,'direct':sorted(direct),'supporting':sorted(support),'topics':topics,'quizzes':qa})
  summary={}
  for title in ['Topics','Prerequisites']:
   section=re.search(r'^## '+title+r'\s*\n(.*?)(?=^## |\Z)',raw,re.M|re.S);summary[title]=self.topic_links('**'+title+':** '+(section[1].replace('\n',' ')if section else''),path)
  steps=self.sequence(seed,['instructions/step']+[f'problem-{n}/step'for n in range(1,problem_count+1)],contents);day=date.fromisoformat(re.search(r'^Due:\s*(\d{4}-\d{2}-\d{2})\s*$',raw,re.M)[1]);assert re.search(r'^Due time: 11:59 p\.m\. PDT$',raw,re.M);due=datetime.combine(day,time(23,59),ZoneInfo('America/Los_Angeles')).astimezone(timezone.utc).isoformat().replace('+00:00','Z');uid=self.entity(seed,'activity','activity',activity__title=f'MTH {course} — {code}',activity__type=':activity.type/assignment',activity__steps=steps,activity__first_step=steps[0],activity__course={'$ref':[':course/id',{'$uuid':COURSES[course]}]},activity__due={'$inst':due});self.audit['activities'].append({'source':relative,'identity_source':seed,'title':f'MTH {course} — {code}','activity_id':uid,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'due':due,'problems':problems,'summary_links':summary,'quiz_count':quiz_count});return uid

def main():
 assert not(H/'commit-intent.json').exists(),'Preserve pending import intent'
 b=AssignmentBuilder(V);activities=[b.assignment(*spec)for spec in SOURCES];b.validate();save('entities.json',b.entities);targets={t for a in b.audit['activities']for p in a['problems']for t in p['topics']};targets.update(x['topic_id']for a in b.audit['activities']for maps in a['summary_links'].values()for kind in ['direct','supporting']for x in maps[kind]);db=connection();basis=db.basis();identities=[]
 for r in b.entities:
  attr=next(k for k in r if k.endswith('/id')and k!=':db/id');identities.append([kw(attr),uuid.UUID(r[attr]['$uuid'])])
 present=db.query('[:find ?a ?v ?e :in $ [[?a ?v]] :where [?e ?a ?v]]',[identities],H,'identities-before',basis);assert not present,'A requested assignment already exists; reconcile instead of overwriting'
 enums=['activity.type/assignment','answer.type/text','answer.type/math','answer-field.type/free','answer-field.type/blank','course-academy.source/editor'];external=[[kw('topic/math-academy-id'),t]for t in sorted(targets)]+[[kw('course/id'),uuid.UUID(COURSES[c])]for c in ['255','341']]+[[kw('db/ident'),kw(e)]for e in enums];ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[external],H,'external-before',basis);assert len(ext)==len(external);learner=db.query('[:find (pull ?l [:db/id :learner/id :learner/assignments :learner/targets]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis)[0][0];snapshot={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):normalize(v)for k,v in r.items()}for r in [x[2]for x in ext]+[learner]}};save('snapshot.json',snapshot);model=Import(V,{});model.entities=b.entities;forms=model.transaction(snapshot,DEFAULT_LEARNER,activities);topicrows={r[':topic/math-academy-id']:r for a,v,r in ext if ':topic/math-academy-id'in r};oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])};added={f[3]for f in forms if isinstance(f,list)and f[2]==':learner/targets'}
 for n in sorted(targets):
  e=topicrows[n][':db/id']
  if e not in oldtargets|added:forms.append([':db/add',learner[':db/id'],':learner/targets',e]);added.add(e)
 payload='[\n'+'\n '.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload);describe=lambda ns:[{'entity':topicrows[n][':db/id'],'math_academy_id':n,'title':topicrows[n][':topic/title']}for n in sorted(ns)];audit={'database':'math','basis_t':basis,'source':':course-academy.source/editor','activities':b.audit['activities'],'activity_ids':activities,'learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'all_requested_targets':describe(targets),'added_targets':[x for x in describe(targets)if x['entity']in added],'assets':list(b.assets.values()),'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in b.entities)),'field_types':dict(collections.Counter(r[':answer-field/type']for r in b.entities if ':answer-field/id'in r)),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'forms':len(forms),'target_policy':'Union of all verified per-quiz and assignment-wide topic and prerequisite links. Explicit targets only, no transitive ancestor expansion. Existing targets and assignments preserved.'};save('source-audit.json',audit);print(json.dumps({k:audit[k]for k in ['basis_t','counts','field_types','forms','added_targets','sha256']},indent=2))
if __name__=='__main__':main()
