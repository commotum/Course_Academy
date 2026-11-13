import collections,hashlib,json,re,sys,uuid,importlib.util
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,COURSES,PROBLEM,QUIZ,NAV_LINE,NAV_SECTION,UniqueKeyLoader
from import_school_assignments import tidy
import yaml
from import_school_assignments import Import,DEFAULT_LEARNER
from sync_f26_assignments import edn
from migrate_learner_history import connection,kw,Keyword
spec=importlib.util.spec_from_file_location('native_import',R/'reference/edb-math/imports/oregon-state/2026-11-06-six-downloads/prepare.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
V=R.parent/'study/vault';H=R/'reference/edb-math/imports/oregon-state/2026-11-13-341-sg3';REL='F26/341/Undated_SG-3.md'
def save(n,v):(H/n).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
def normalize(v):
 if isinstance(v,Keyword):return {'$keyword':str(v).lstrip(':')}
 if isinstance(v,uuid.UUID):return {'$uuid':str(v)}
 if isinstance(v,dict):return v[':db/id'] if ':db/id'in v else {str(k).lstrip(':'):normalize(x)for k,x in v.items()}
 if isinstance(v,list):return [normalize(x)for x in v]
 return v
class MixedBuilder(native.NativeBuilder):
 def render_text(self,value,source,location):
  for name,uid in [('10-28-26_WHW-4.md','d58af8ee-31ff-5364-87d1-9474dd41865f'),('11-04-26_WHW-5.md','4771eb83-434d-5edb-a38a-03676de85913')]:
   value=value.replace(']('+name+')','](http://127.0.0.1:8765/assignments?assignment='+uid+')')
  return super().render_text(value,source,location)
 def assignment(self,relative):
  path=V/relative;raw=path.read_text();seed='F26/341/SG-3';markers=list(PROBLEM.finditer(raw));assert [int(m[1]) for m in markers]==[1,2,3,4]
  intro=self.render_text(tidy(NAV_SECTION.sub('',raw[:markers[0].start()])),path,'instructions')
  contents=[self.entity(seed,'instructions','tutorial',tutorial__title='Exam information and preparation advice',tutorial__content=intro)];problems=[]
  for i,m in enumerate(markers):
   n=int(m[1]);body=raw[m.end():markers[i+1].start() if i+1<len(markers) else len(raw)];mapping=self.topic_links(body,path)
   direct=sorted({x['topic_id'] for x in mapping['direct']});support=sorted({x['topic_id'] for x in mapping['supporting']});topics=sorted(set(direct+support));blocks=list(QUIZ.finditer(body));quizzes=[]
   if n==1:
    assert not blocks
    prompt=self.render_text(tidy(NAV_LINE.sub('',body)),path,'problem-1')
    content=self.entity(seed,'problem-1/question','question',question__problem=prompt)
   else:
    assert len(blocks)==1;block=blocks[0];q=yaml.load(block[1],Loader=UniqueKeyLoader);assert q['id']==f'q-{n}'
    context=self.render_text(tidy(body[:block.start()]),path,f'problem-{n}/context')
    content,qa=self.question(seed,f'problem-{n}/question',q,path,context);qa['topics']=mapping;quizzes.append(qa)
   assigned=self.entity(seed,f'problem-{n}','assigned-problem',assigned_problem__content=content,assigned_problem__topic_coverage=[{'$ref':[':topic/math-academy-id',t]} for t in topics])
   contents.append(assigned);problems.append({'number':n,'assigned_problem_id':assigned,'content_id':content,'topics':topics,'direct':direct,'supporting':support,'mapping_evidence':mapping,'quizzes':quizzes,'kind':'fieldless-review-reminder' if n==1 else 'written-response'})
  steps=self.sequence(seed,['instructions/step']+[f'problem-{n}/step' for n in range(1,5)],contents)
  title='MTH 341 — SG-3: MiniExam 3 Review'
  uid=self.entity(seed,'activity','activity',activity__title=title,activity__type=':activity.type/assignment',activity__steps=steps,activity__first_step=steps[0],activity__course={'$ref':[':course/id',{'$uuid':COURSES['341']}]})
  self.audit['activities'].append({'source':relative,'identity_source':seed,'title':title,'activity_id':uid,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'due':None,'due_convention':'No verified deadline; no due instant stored.','problems':problems,'quiz_count':3,'fieldless_questions':1,'source_numbered_items':4})
  return uid
def main():
 H.mkdir(parents=True,exist_ok=True);assert not(H/'commit-intent.json').exists()
 path=V/REL;raw=path.read_text();b=MixedBuilder(V);activity=b.assignment(REL)
 b.validate();save('entities.json',b.entities)
 targets={t for p in b.audit['activities'][0]['problems']for t in p['topics']}
 for title in ['Topics','Prerequisites']:
  sec=re.search(r'^## '+title+r'\s*\n(.*?)(?=^## |\Z)',raw,re.M|re.S);maps=b.topic_links('**'+title+':** '+sec[1].replace('\n',' '),path);targets.update(x['topic_id']for group in ['direct','supporting']for x in maps[group])
 # Include the supplied definition and all theorem cases, even those without exercises.
 intro=raw.split('## Problem 1')[0];maps=b.topic_links(intro,path);targets.update(x['topic_id']for group in ['direct','supporting']for x in maps[group])
 db=connection();basis=db.basis();identities=[]
 for row in b.entities:
  a=next(k for k in row if k.endswith('/id')and k!=':db/id');identities.append([kw(a),uuid.UUID(row[a]['$uuid'])])
 present=db.query('[:find ?a ?v ?e :in $ [[?a ?v]] :where [?e ?a ?v]]',[identities],H,'identities-before',basis);assert not present,'Existing identities require reconciliation.'
 external=[[kw('topic/math-academy-id'),t]for t in sorted(targets)]+[[kw('course/id'),uuid.UUID(COURSES['341'])]]+[[kw('db/ident'),kw(x)]for x in ['activity.type/assignment','answer.type/text','answer.type/math','answer-field.type/free','answer-field.type/blank','course-academy.source/editor']]
 ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[external],H,'external-before',basis);assert len(ext)==len(external)
 learner=db.query('[:find (pull ?l [:db/id :learner/id [:learner/assignments :limit nil] [:learner/targets :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis)[0][0]
 snapshot={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):normalize(v)for k,v in r.items()}for r in [x[2]for x in ext]+[learner]}};save('snapshot.json',snapshot);model=Import(V,{});model.entities=b.entities;forms=model.transaction(snapshot,DEFAULT_LEARNER,[activity])
 topicrows={r[':topic/math-academy-id']:r for a,v,r in ext if ':topic/math-academy-id'in r};oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])};added={f[3]for f in forms if isinstance(f,list)and f[2]==':learner/targets'}
 for t in sorted(targets):
  e=topicrows[t][':db/id']
  if e not in oldtargets|added:forms.append([':db/add',learner[':db/id'],':learner/targets',e]);added.add(e)
 payload='[\n'+'\n '.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload)
 describe=lambda ns:[{'entity':topicrows[n][':db/id'],'math_academy_id':n,'title':topicrows[n][':topic/title']}for n in sorted(ns)]
 audit={'database':'math','basis_t':basis,'source':':course-academy.source/editor','learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'activities':b.audit['activities'],'activity_ids':[activity],'all_requested_targets':describe(targets),'added_targets':[x for x in describe(targets)if x['entity']in added],'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in b.entities)),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'assets':list(b.assets.values()),'fieldless_questions':1,'quiz_count':3,'matching_gaps':'Item 1 uses the named coursework; items 2–4 have component coverage, not a verified whole-task equivalent.'}
 save('source-audit.json',audit);print(json.dumps({'basis':basis,'counts':audit['counts'],'topics':len(targets),'new_targets':len(added),'already_targets':len(targets)-len(added),'activity_id':activity,'sha256':audit['sha256']},indent=2))
if __name__=='__main__':main()
