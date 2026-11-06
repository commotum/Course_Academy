import importlib.util,collections,hashlib,json,re,sys,uuid
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,COURSES,PROBLEM,NAV_LINE,NAV_SECTION
from import_school_assignments import Import,DEFAULT_LEARNER,tidy
from migrate_learner_history import connection,kw
from sync_f26_assignments import edn
p=R/'reference/edb-math/imports/oregon-state/2026-10-25-whw5-whw4/prepare.py'
s=importlib.util.spec_from_file_location('prior_normalize',p);mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)
V=R.parent/'study/vault';H=R/'reference/edb-math/imports/oregon-state/2026-11-06-255-final-guide'
SOURCES=['F26/255/Undated_SG-2.md']
def save(name,v):(H/name).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
class FieldlessBuilder(Builder):
 def assignment(self,relative):
  path=V/relative;raw=path.read_text();seed='F26/255/SG-2';markers=list(PROBLEM.finditer(raw));assert [int(m[1])for m in markers]==list(range(1,41));assert '```' not in raw
  intro=self.render_text(tidy(NAV_SECTION.sub('',raw[:markers[0].start()])),path,'instructions')
  contents=[self.entity(seed,'instructions','tutorial',tutorial__title='Exam information and preparation advice',tutorial__content=intro)];problems=[]
  inventory=json.loads((Path('/tmp/255-final-guide-review')/'inventory.json').read_text())
  for i,m in enumerate(markers):
   n=int(m[1]);body=raw[m.end():markers[i+1].start()if i+1<len(markers)else len(raw)];mapping=self.topic_links(body,path)
   direct=sorted({x['topic_id']for x in mapping['direct']});support=sorted({x['topic_id']for x in mapping['supporting']});expected=inventory[n-1]
   assert direct==sorted(expected['direct'])and support==sorted(expected['supporting'])
   prompt=self.render_text(tidy(NAV_LINE.sub('',body)),path,f'problem-{n}')
   assert expected['objective'] in prompt,(n,'Source objective altered')
   content=self.entity(seed,f'problem-{n}/question','question',question__problem=prompt)
   assigned=self.entity(seed,f'problem-{n}','assigned-problem',assigned_problem__content=content,assigned_problem__topic_coverage=[{'$ref':[':topic/math-academy-id',t]}for t in sorted(set(direct+support))])
   contents.append(assigned);problems.append({'number':n,'assigned_problem_id':assigned,'content_id':content,'topics':sorted(set(direct+support)),'direct':direct,'supporting':support,'mapping_evidence':mapping,'quizzes':[],'kind':'fieldless-study-objective','component_only':expected['component_only'],'coverage_gap':expected.get('coverage_gap')})
  steps=self.sequence(seed,['instructions/step']+[f'problem-{n}/step'for n in range(1,41)],contents)
  uid=self.entity(seed,'activity','activity',activity__title='MTH 255 — Final Exam Study Guide',activity__type=':activity.type/assignment',activity__steps=steps,activity__first_step=steps[0],activity__course={'$ref':[':course/id',{'$uuid':COURSES['255']}]})
  self.audit['activities'].append({'source':relative,'identity_source':seed,'title':'MTH 255 — Final Exam Study Guide','activity_id':uid,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'due':None,'due_convention':'PDF states Week 11 according to the Final Exam Schedule; exact date/time unverified, so no deadline inferred.','problems':problems,'quiz_count':0,'fieldless_questions':40,'source_numbered_items':40})
  return uid

def main():
 H.mkdir(parents=True,exist_ok=True);assert not(H/'commit-intent.json').exists(),'Reconcile durable intent before preparing again.'
 b=FieldlessBuilder(V);activities=[b.assignment(s)for s in SOURCES];b.validate()
 assert len(b.entities)==123
 assert len([r for r in b.entities if ':question/id'in r])==40
 assert not any(':question/answer-fields'in r or ':question/worked-solution'in r or ':answer-field/id'in r or ':answer/id'in r for r in b.entities)
 save('entities.json',b.entities);targets={t for a in b.audit['activities']for p in a['problems']for t in p['topics']}
 for source in SOURCES:
  path=V/source;raw=path.read_text()
  for title in ['Topics','Prerequisites']:
   sec=re.search(r'^## '+title+r'\s*\n(.*?)(?=^## |\Z)',raw,re.M|re.S)
   mapping=b.topic_links('**'+title+':** '+sec[1].replace('\n',' '),path);targets.update(x['topic_id']for kind in ['direct','supporting']for x in mapping[kind])
 assert len(targets)==55
 db=connection();basis=db.basis();identities=[]
 for row in b.entities:
  attr=next(k for k in row if k.endswith('/id')and k!=':db/id');identities.append([kw(attr),uuid.UUID(row[attr]['$uuid'])])
 present=db.query('[:find ?a ?v ?e :in $ [[?a ?v]] :where [?e ?a ?v]]',[identities],H,'identities-before',basis);assert not present,'Existing requested content requires scoped reconciliation.'
 enums=['activity.type/assignment','course-academy.source/editor']
 external=[[kw('topic/math-academy-id'),t]for t in sorted(targets)]+[[kw('course/id'),uuid.UUID(COURSES['255'])]]+[[kw('db/ident'),kw(e)]for e in enums]
 ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[external],H,'external-before',basis);assert len(ext)==len(external),(len(ext),len(external))
 learner=db.query('[:find (pull ?l [:db/id :learner/id [:learner/assignments :limit nil] [:learner/targets :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis);assert len(learner)==1;learner=learner[0][0]
 snapshot={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):mod.normalize(v)for k,v in r.items()}for r in [x[2]for x in ext]+[learner]}}
 save('snapshot.json',snapshot);model=Import(V,{});model.entities=b.entities;forms=model.transaction(snapshot,DEFAULT_LEARNER,activities)
 topicrows={r[':topic/math-academy-id']:r for a,v,r in ext if ':topic/math-academy-id'in r};oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])};added={f[3]for f in forms if isinstance(f,list)and f[2]==':learner/targets'}
 for n in sorted(targets):
  eid=topicrows[n][':db/id']
  if eid not in oldtargets|added:forms.append([':db/add',learner[':db/id'],':learner/targets',eid]);added.add(eid)
 payload='[\n'+'\n '.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload)
 describe=lambda ns:[{'entity':topicrows[n][':db/id'],'math_academy_id':n,'title':topicrows[n][':topic/title']}for n in sorted(ns)]
 audit={'database':'math','basis_t':basis,'source':':course-academy.source/editor','activities':b.audit['activities'],'activity_ids':activities,'learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'all_requested_targets':describe(targets),'added_targets':[x for x in describe(targets)if x['entity']in added],'assets':list(b.assets.values()),'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in b.entities)),'field_types':{},'sha256':hashlib.sha256(payload.encode()).hexdigest(),'forms':len(forms),'target_policy':'All verified explicit coverage and prerequisites, including the 40 fieldless study objectives; no transitive prerequisite expansion.'}
 save('source-audit.json',audit);print(json.dumps({'basis_t':basis,'counts':audit['counts'],'unique_requested_targets':len(targets),'new_targets':len(added),'already_targets':len(targets)-len(added),'sha256':audit['sha256']},indent=2))
if __name__=='__main__':main()
