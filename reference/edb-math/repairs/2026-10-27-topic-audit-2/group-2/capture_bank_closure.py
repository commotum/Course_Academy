import json,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[4]/'scripts'));from migrate_learner_history import connection
out=H/'bank-closure';out.mkdir(exist_ok=True);db=connection();basis=9169;ids=[17592186147726,17592186217793]
qs=db.query('[:find (pull ?q [* {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]) :in $ [?q ...] :where [?q :question/id _]]',[ids],out,'questions',basis)
parents=db.query('[:find ?q ?parent ?step :in $ [?q ...] :where [?step :step/content ?q] [?parent :multistep/steps ?step]]',[ids],out,'multistep-parents',basis)
assigned=db.query('[:find ?q ?parent :in $ [?q ...] :where [?parent :assigned-problem/content ?q]]',[ids],out,'assigned-parents',basis)
context=[x for x in json.loads((H/'completion-context.json').read_text())if x['q'][':db/id']in ids];(out/'context.json').write_text(json.dumps(context,indent=2)+'\n');sources=[]
for mid,qid in[(2522,'106074'),(6353,'337099')]:
 path=Path('/home/jake/Developer/MA/DATA/Lessons')/str(mid)/'Source'/f'{mid}.html';soup=BeautifulSoup(path.read_text(),'html.parser');node=soup.find(id='question-'+qid)
 if node is None:
  candidates=soup.find_all(id=True);node=next((n for n in candidates if n.get('id')in['questionWidget-'+qid,'question-'+qid]),None)
 if node is None:
  root=soup.find(id='selectList-'+qid+'-0')
  if root:node=root.find_parent(class_='questionWidget')or root.find_parent(class_='questionContainer')or root.parent
 if node is None:
  # The retained scalar index preserves its complete captured questionText frame.
  record=next(s for s in json.loads((H/'sources.json').read_text())if s['identity']=='q-'+qid and s['attribute']=='question/problem');html=record['html']
 else:html=str(node)
 (out/('source-q'+qid+'.html')).write_text(html);sources.append({'identity':'q-'+qid,'archive':str(path),'saved_frame':'source-q'+qid+'.html','frame_id':node.get('id')if node else None,'frame_classes':node.get('class')if node else None,'graphic_count':len(BeautifulSoup(html,'html.parser').find_all('img'))})
report={'basis':basis,'questions':[r[0]for r in qs],'multistep_parents':parents,'assigned_problem_parents':assigned,'sources':sources};(out/'current.json').write_text(json.dumps(report,indent=2,default=str)+'\n');print(json.dumps(report,indent=2,default=str)[:12500])
