"""Resolve requested topics and audit completion evidence at one EDB basis."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
ids=json.loads((H/'requested-topic-ids.json').read_text());prior={};audits=[]
for name,report in [('2026-10-27-linear-algebra-audit','README.md'),('2026-10-27-topic-audit-2','REPORT.md'),('2026-10-28-topic-audit-3','REPORT.md')]:
 d=H.parent/name;v=json.loads((d/'final-verification.json').read_text());assert v['passed'];inv=json.loads((d/'inventory.json').read_text());audits.append({'directory':str(d),'report':report,'basis_t':v['basis_t']})
 for t in inv['topics']:prior.setdefault(t['entity'],[]).append({'directory':str(d),'report':report,'verified_basis_t':v['basis_t'],'original_question_count':t['questions']})
last=H.parent/'2026-10-29-q17592186604616';v=json.loads((last/'full-review/live-verification.json').read_text());assert v['passed']
for e in[17592186050463,17592186049548,17592186049043,17592186050092]:prior.setdefault(e,[]).append({'directory':str(last),'report':'REPORT.md','verified_basis_t':v['basis_t']})
db=connection();basis=db.basis();pattern='[:db/id :topic/id :topic/title :topic/math-academy-id {:topic/knowledge-points [:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/questions [:db/id]} {:knowledge-point/canonical-example [:db/id]} {:knowledge-point/question-generator [*]}]}]'
topics=[r[0]for r in db.query('[:find (pull ?t '+pattern+') :in $ [?t ...] :where [?t :topic/id _]]',[ids],H,'current-topics',basis)];assert{t[':db/id']for t in topics}==set(ids)
links=[[t[':db/id'],k[':db/id'],q[':db/id']]for t in topics for k in t[':topic/knowledge-points']for a in[':knowledge-point/questions',':knowledge-point/canonical-example']for q in(k.get(a,[])if isinstance(k.get(a,[]),list)else[k[a]])]
qids=sorted({q for t,k,q in links});unkeyed=db.query('[:find ?q ?f :in $ [?q ...] :where [?q :question/answer-fields ?f] [(missing? $ ?f :answer-field/correct)]]',[qids],H,'missing-correct-links',basis);missing_solutions=db.query('[:find ?q :in $ [?q ...] :where [?q :question/id _] [(missing? $ ?q :question/worked-solution)]]',[qids],H,'missing-solutions',basis);badqs={q for q,f in unkeyed}|{r[0]for r in missing_solutions};reopen={t for t,k,q in links if q in badqs};decisions=[]
for t in topics:
 eid=t[':db/id'];history=prior.get(eid,[]);reasons=[]
 if not history:reasons.append('No completed full-topic audit in prior scope manifests')
 if eid in reopen:reasons.append('Current missing solution or unkeyed field requires renewed review despite prior audit')
 decisions.append({'topic':eid,'title':t[':topic/title'],'source_topic':t[':topic/math-academy-id'],'questions':sum(1 for x in links if x[0]==eid),'action':'audit'if reasons else'skip-completed','reasons':reasons,'prior_completed_audits':history})
record={'basis_t':basis,'requested_topics':ids,'topics':topics,'links':links,'decisions':decisions,'current_unkeyed_fields':unkeyed,'current_missing_solutions':missing_solutions};(H/'inventory.json').write_text(json.dumps(record,default=str,indent=2)+'\n');print('Basis',basis,'requested',len(topics),'audit',sum(d['action']=='audit'for d in decisions),'skip',sum(d['action']=='skip-completed'for d in decisions));print('Current incomplete',unkeyed,missing_solutions)
for d in sorted(decisions,key=lambda d:d['topic']):print(d['action'],d['topic'],d['source_topic'],d['questions'],d['title'])
