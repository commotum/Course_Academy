import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
I=json.loads((H.parent/'inventory.json').read_text()); G=json.loads((H.parent/'group-2.json').read_text());topics=[t for t in I['topics']if t['entity']in G['topics']];db=connection();Q=[];K=[];A=[]
for t in topics:
 e=t['entity'];qids=sorted({q for te,k,q in I['links']if te==e})
 qs=db.query('[:find (pull ?q [* {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]) :in $ [?q ...] :where [?q :question/id ?id]]',[qids],H,f'questions-{t["ma_id"]}',9047);Q.extend([r[0]for r in qs]);assert len(qs)==len(qids)
 ks=db.query('[:find (pull ?kp [* {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id ?id]]',[t['kp_ids']],H,f'kps-{t["ma_id"]}',9047);K.extend(r[0]for r in ks)
 links=db.query('[:find ?a ?s ?c :in $ ?t :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson] [?a :activity/steps ?s] [?s :step/content ?c]]',[e],H,f'activity-links-{t["ma_id"]}',9047)
 cs=sorted({c for a,s,c in links});contents=db.query('[:find (pull ?c [:db/id :tutorial/id :tutorial/math-academy-id :tutorial/title :tutorial/content :knowledge-point/id :knowledge-point/title]) :in $ [?c ...] :where [?c ?a ?v]]',[cs],H,f'contents-{t["ma_id"]}',9047)
 A.append({'topic':e,'links':links,'contents':[r[0]for r in contents]});print(t['ma_id'],len(qs),len(contents),flush=True)
(H/'current.json').write_text(json.dumps({'basis':9047,'topics':topics,'questions':Q,'kps':K,'activities':A},indent=2,default=str)+'\n')
