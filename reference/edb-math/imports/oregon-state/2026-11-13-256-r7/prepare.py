import collections,hashlib,json,re,sys,uuid,importlib.util
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from f26_assignment_content import Builder,COURSES
from import_school_assignments import Import,DEFAULT_LEARNER
from sync_f26_assignments import edn
from migrate_learner_history import connection,kw,Keyword
spec=importlib.util.spec_from_file_location('native_import',R/'reference/edb-math/imports/oregon-state/2026-11-06-six-downloads/prepare.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
V=R.parent/'study/vault';H=R/'reference/edb-math/imports/oregon-state/2026-11-13-256-r7';REL='F26/256/Undated_R-7.md'
def save(n,v):(H/n).write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n')
def normalize(v):
 if isinstance(v,Keyword):return {'$keyword':str(v).lstrip(':')}
 if isinstance(v,uuid.UUID):return {'$uuid':str(v)}
 if isinstance(v,dict):return v[':db/id'] if ':db/id'in v else {str(k).lstrip(':'):normalize(x)for k,x in v.items()}
 if isinstance(v,list):return [normalize(x)for x in v]
 return v
def main():
 H.mkdir(parents=True,exist_ok=True);assert not(H/'commit-intent.json').exists()
 path=V/REL;raw=path.read_text();b=native.NativeBuilder(V);activity=Builder.assignment(b,REL)
 assert len(b.audit['activities'])==1 and len(b.audit['activities'][0]['problems'])==10
 b.audit['activities'][0]['due_convention']='Unknown: no deadline in the source; no due instant stored.'
 b.audit['activities'][0]['title']='MTH 256 — R-7: Quiz 3 Review'
 next(r for r in b.entities if ':activity/id'in r)[':activity/title']='MTH 256 — R-7: Quiz 3 Review'
 b.validate();save('entities.json',b.entities)
 targets={t for p in b.audit['activities'][0]['problems']for t in p['topics']}
 for title in ['Topics','Prerequisites']:
  sec=re.search(r'^## '+title+r'\s*\n(.*?)(?=^## |\Z)',raw,re.M|re.S);maps=b.topic_links('**'+title+':** '+sec[1].replace('\n',' '),path);targets.update(x['topic_id']for group in ['direct','supporting']for x in maps[group])
 # Include the supplied definition and all theorem cases, even those without exercises.
 intro=raw.split('## Problem 1')[0];maps=b.topic_links(intro,path);targets.update(x['topic_id']for group in ['direct','supporting']for x in maps[group])
 assert targets=={35,375,394,422,614,879,880,1007,1109,1181,1425,2528,2544,2545,2547}
 db=connection();basis=db.basis();identities=[]
 for row in b.entities:
  a=next(k for k in row if k.endswith('/id')and k!=':db/id');identities.append([kw(a),uuid.UUID(row[a]['$uuid'])])
 present=db.query('[:find ?a ?v ?e :in $ [[?a ?v]] :where [?e ?a ?v]]',[identities],H,'identities-before',basis);assert not present,'Existing identities require reconciliation.'
 external=[[kw('topic/math-academy-id'),t]for t in sorted(targets)]+[[kw('course/id'),uuid.UUID(COURSES['256'])]]+[[kw('db/ident'),kw(x)]for x in ['activity.type/assignment','answer.type/text','answer.type/math','answer-field.type/free','answer-field.type/blank','course-academy.source/editor']]
 ext=db.query('[:find ?a ?v (pull ?e [*]) :in $ [[?a ?v]] :where [?e ?a ?v]]',[external],H,'external-before',basis);assert len(ext)==len(external)
 learner=db.query('[:find (pull ?l [:db/id :learner/id [:learner/assignments :limit nil] [:learner/targets :limit nil]]) :in $ ?id :where [?l :learner/id ?id]]',[DEFAULT_LEARNER],H,'learner-before',basis)[0][0]
 snapshot={'basis_t':basis,'entities':{str(r[':db/id']):{str(k).lstrip(':'):normalize(v)for k,v in r.items()}for r in [x[2]for x in ext]+[learner]}};save('snapshot.json',snapshot);model=Import(V,{});model.entities=b.entities;forms=model.transaction(snapshot,DEFAULT_LEARNER,[activity])
 topicrows={r[':topic/math-academy-id']:r for a,v,r in ext if ':topic/math-academy-id'in r};oldtargets={x[':db/id']for x in learner.get(':learner/targets',[])};added={f[3]for f in forms if isinstance(f,list)and f[2]==':learner/targets'}
 for t in sorted(targets):
  e=topicrows[t][':db/id']
  if e not in oldtargets|added:forms.append([':db/add',learner[':db/id'],':learner/targets',e]);added.add(e)
 payload='[\n'+'\n '.join(edn(f)for f in forms)+'\n]\n';(H/'transaction.edn').write_text(payload)
 describe=lambda ns:[{'entity':topicrows[n][':db/id'],'math_academy_id':n,'title':topicrows[n][':topic/title']}for n in sorted(ns)]
 audit={'database':'math','basis_t':basis,'source':':course-academy.source/editor','learner_uuid':DEFAULT_LEARNER,'learner_entity':learner[':db/id'],'activities':b.audit['activities'],'activity_ids':[activity],'all_requested_targets':describe(targets),'added_targets':[x for x in describe(targets)if x['entity']in added],'old_assignment_eids':sorted(x[':db/id']for x in learner.get(':learner/assignments',[])),'old_target_eids':sorted(oldtargets),'counts':dict(collections.Counter(next(k[1:-3]for k in r if k.endswith('/id')and k!=':db/id')for r in b.entities)),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'source_conflicts':['Problem 1 is false for both printed equations; intended correction unconfirmed.','Problem 10: missing leading x^2 in first equation and incorrect claimed roots; study answer solves final displayed ODE.'],'assets':list(b.assets.values()),'noninteractive_coverage':{'Wronskian':[2547],'Theorem 5.2.1':[614,879,880],'Theorem 7.4.3':[2528,2544,2545]}}
 save('source-audit.json',audit);print(json.dumps({'basis':basis,'counts':audit['counts'],'topics':len(targets),'new_targets':len(added),'already_targets':len(targets)-len(added),'activity_id':activity,'sha256':audit['sha256']},indent=2))
if __name__=='__main__':main()
