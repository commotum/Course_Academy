import json,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
IDS=[17592186048127,17592186048187,17592186048391,17592186048449,17592186048489,17592186048569,17592186048630,17592186048697,17592186048707,17592186048754,17592186048774,17592186048777,17592186048813,17592186048870,17592186049007,17592186049044,17592186049053,17592186049091,17592186049131,17592186049146,17592186049187,17592186049209,17592186049380,17592186049396,17592186049406,17592186049423,17592186049438,17592186049456,17592186049481,17592186049486,17592186049533,17592186049543,17592186049774,17592186049854,17592186050101,17592186050150,17592186050271,17592186050321,17592186050451,17592186050608,17592186050905,17592186050929,17592186050995,17592186051084]
assert len(set(IDS))==44;db=connection();basis=db.basis();(H/'basis.json').write_text(json.dumps({'basis_t':basis})+'\n')
topics=[r[0]for r in db.query('[:find (pull ?t [:db/id :topic/id :topic/title :topic/math-academy-id]) :in $ [?t ...] :where [?t :topic/title _]]',[IDS],H,'topics',basis)];assert len(topics)==len(IDS)
links=db.query('[:find ?t ?kp ?q :in $ [?t ...] :where [?t :topic/knowledge-points ?kp] (or [?kp :knowledge-point/questions ?q] [?kp :knowledge-point/canonical-example ?q])]',[IDS],H,'question-links',basis)
records=[{'entity':t[':db/id'],'title':t[':topic/title'],'ma_id':t.get(':topic/math-academy-id'),'questions':len({q for tid,k,q in links if tid==t[':db/id']}),'kp_ids':sorted({k for tid,k,q in links if tid==t[':db/id']})}for t in topics]
inv={'basis_t':basis,'topics':records,'links':links};(H/'topic-ids.json').write_text(json.dumps(IDS,indent=2)+'\n');(H/'inventory.json').write_text(json.dumps(inv,indent=2,default=str)+'\n');groups=[[]for _ in range(3)];weights=[0]*3
for rec in sorted(records,key=lambda x:x['questions'],reverse=True):i=weights.index(min(weights));groups[i].append(rec['entity']);weights[i]+=rec['questions']
for i,group in enumerate(groups,1):(H/f'group-{i}.json').write_text(json.dumps({'topics':group,'basis_t':basis,'questions':weights[i-1]},indent=2)+'\n')
print('Basis',basis,'topics',len(records),'unique question/examples',len({q for t,k,q in links}),'group counts',weights)
for r in records:print(r['entity'],r['ma_id'],r['questions'],r['title'])
