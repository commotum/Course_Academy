import sys,json
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');H=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,kw
ids=[]
for d in H.glob('175*'):
 ids.extend(q[':db/id']for q in json.loads((d/'questions.json').read_text()))
 for aa in json.loads((d/'lessons.json').read_text()):ids.extend(s[':step/content'][':db/id']for s in aa[0][':activity/steps']if ':tutorial/content'in s[':step/content'])
b=json.loads((H/'basis.json').read_text())['basis'];db=connection();r=db.query('[:find ?e ?attr ?tx ?source :in $ [?e ...] [?attr ...] :where [?e ?attr ?value ?tx ?source]]',[ids,[kw('question/problem'),kw('question/worked-solution'),kw('tutorial/content')]],H,'content-origins',b)
txs=sorted({row[2]for row in r});sources=sorted({row[3]for row in r});metadata=db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[txs+sources],H,'origin-metadata',b)
(H/'content-origins.json').write_text(json.dumps({'basis':b,'rows':r,'transaction_and_contributor_metadata':metadata},indent=2,default=str));print('entities',len(ids),'originrows',len(r),'transactions',len(txs),'sources',len(sources))
