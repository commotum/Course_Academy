import sys,json
from pathlib import Path
sys.path.insert(0,'scripts')
from migrate_learner_history import connection
out=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/foundations'); db=connection(); basis=db.basis()
q=Path('reference/edb-math/audits/2026-11-08-topic-17592186048459/topic-before-query.edn').read_text(); lq=Path('reference/edb-math/audits/2026-11-08-topic-17592186048459/lessons-before-query.edn').read_text()
summary=[]
for eid in [17592186048535,17592186048202,17592186050537,17592186050677,17592186050426,17592186048257]:
 d=out/str(eid);d.mkdir(exist_ok=True)
 t=db.query(q,[eid],d,'topic-before',basis)[0][0];ls=db.query(lq,[eid],d,'lessons-before',basis)
 (d/'topic-before.json').write_text(json.dumps(t,indent=2,default=str));(d/'lessons-before.json').write_text(json.dumps(ls,indent=2,default=str))
 qs={x[':db/id']:x for kp in t[':topic/knowledge-points'] for x in kp.get(':knowledge-point/questions',[])+([kp[':knowledge-point/canonical-example']]if kp.get(':knowledge-point/canonical-example')else[])}
 (d/'questions-before.json').write_text(json.dumps(list(qs.values()),indent=2,default=str))
 summary.append({'entity':eid,'title':t[':topic/title'],'mid':t[':topic/math-academy-id'],'kps':len(t[':topic/knowledge-points']),'questions':len(qs),'steps':sum(len(a[0].get(':activity/steps',[]))for a in ls),'missing_solution':[x[':db/id']for x in qs.values()if not x.get(':question/worked-solution')],'missing_key':[x[':db/id']for x in qs.values()if any(not f.get(':answer-field/correct')for f in x.get(':question/answer-fields',[])if f[':answer-field/type'][':db/ident']!=':answer-field.type/free')]})
(out/'basis.json').write_text(json.dumps({'basis':basis}));(out/'summary-before.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
