import importlib.util,collections,hashlib,json,re,sys,uuid
from datetime import datetime,time,timezone
from pathlib import Path
from zoneinfo import ZoneInfo
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,COURSES
from import_school_assignments import Import,DEFAULT_LEARNER
from migrate_learner_history import connection,kw,Keyword
from sync_f26_assignments import edn
prior=R/'reference/edb-math/imports/oregon-state/2026-10-25-whw5-whw4/prepare.py'
spec=importlib.util.spec_from_file_location('prior_import',prior);prior_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior_module)
V=R.parent/'study/vault';H=R/'reference/edb-math/imports/oregon-state/2026-10-26-255-r5'
H.mkdir(parents=True,exist_ok=True)
def save(name,v):(H/name).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
class NativeBuilder(Builder):
 canonical_question=prior_module.AssignmentBuilder.native_question
 def assignment(self,relative):
  uid=super().assignment(relative)
  activity=next(r for r in self.entities if r[':db/id']==uid)
  due=datetime(2026,10,29,23,59,tzinfo=ZoneInfo('America/Los_Angeles')).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
  activity[':activity/due']={'$inst':due}
  audit=self.audit['activities'][-1];audit['due']=due;audit['due_convention']='Explicit 23:59 PDT deadline, converted without adding seconds.'
  return uid

def main():
 assert not(H/'commit-intent.json').exists(),'A durable intent exists; reconcile it before preparing another.'
 b=NativeBuilder(V);activities=[b.assignment('F26/255/10-29-26_R-5.md')];b.validate()
 assert len([r for r in b.entities if ':question/id' in r])==15
 assert collections.Counter(r[':answer-field/type']for r in b.entities if ':answer-field/id'in r)=={':answer-field.type/free':8,':answer-field.type/blank':7}
 save('entities.json',b.entities)
 targets={t for a in b.audit['activities']for p in a['problems']for t in p['topics']}
 # Include top summary links even when a future source adds a noninteractive study item.
 path=V/'F26/255/10-29-26_R-5.md';raw=path.read_text()
 for title in ['Topics','Prerequisites']:
  sec=re.search(r'^## '+title+r'\s*\n(.*?)(?=^## |\Z)',raw,re.M|re.S)
  mapping=b.topic_links('**'+title+':** '+sec[1].replace('\n',' '),path)
  targets.update(x['topic_id']for kind in ['direct','supporting']for x in mapping[kind])
 db=connection();basis=db.basis();identities=[]
 for row in b.entities:
  attr=next(k for k in row if k.endswith('/id')and k!=':db/id');identities.append([kw(attr),uuid.UUID(row[attr]['$uuid'])])
 present=db.query('[:find ?a ?v ?e :in $ [[?a ?v]] :where [?e ?a ?v]]',[identities],H,'identities-before',basis)
 assert not present,'Assignment content already exists; preserve identities and reconcile.'
 enums=['activity.type/assignment','answer.type/text','answer.type/math','answer-field.type/free','answer-field.type/blank','course-academy.source/editor']
 external=[[kw('topic/math-academy-id'),t]for t in sorted(targets)]+[[kw('course/id'),uuid.UUID(COURSES['255'])]]+[[kw('db/ident'),kw(e)]for e in enums]
 ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[external],H,'external-before',basis)
 assert len(ext)==len(external),(len(ext),len(external))
 learner=db.query('[:find (pull ?l [:db/id :learner/id [:learner/assignments :limit nil] [:learner/targets :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis)
 # Use default explicit pattern if this installed Pull parser lacks selector-map syntax.
 assert len(learner)==1
 learner=learner[0][0]
 snapshot={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):prior_module.normalize(v)for k,v in r.items()}for r in [x[2]for x in ext]+[learner]}}
 save('snapshot.json',snapshot);model=Import(V,{});model.entities=b.entities
 forms=model.transaction(snapshot,DEFAULT_LEARNER,activities)
 topicrows={r[':topic/math-academy-id']:r for a,v,r in ext if ':topic/math-academy-id'in r}
 oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])};added={f[3]for f in forms if isinstance(f,list)and f[2]==':learner/targets'}
 for n in sorted(targets):
  eid=topicrows[n][':db/id']
  if eid not in oldtargets|added:forms.append([':db/add',learner[':db/id'],':learner/targets',eid]);added.add(eid)
 payload='[\n'+'\n '.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload)
 describe=lambda ns:[{'entity':topicrows[n][':db/id'],'math_academy_id':n,'title':topicrows[n][':topic/title']}for n in sorted(ns)]
 audit={'database':'math','basis_t':basis,'source':':course-academy.source/editor','activities':b.audit['activities'],'activity_ids':activities,'learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'all_requested_targets':describe(targets),'added_targets':[x for x in describe(targets)if x['entity']in added],'assets':list(b.assets.values()),'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in b.entities)),'field_types':dict(collections.Counter(r[':answer-field/type']for r in b.entities if ':answer-field/id'in r)),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'forms':len(forms),'target_policy':'Add all verified explicit coverage and prerequisite topics; preserve prior assignments, targets and history.'}
 save('source-audit.json',audit)
 print(json.dumps({'basis_t':basis,'counts':audit['counts'],'field_types':audit['field_types'],'unique_requested_targets':len(targets),'new_targets':len(added),'already_targets':len(targets)-len(added),'sha256':audit['sha256']},indent=2))
if __name__=='__main__':main()
