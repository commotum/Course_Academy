import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('index=collections.defaultdict(list)')[0],str(p),'exec'),ns)
D=json.loads((H/'current.json').read_text());targets={q[':question/math-academy-id']:q for q in D['questions']if ':question/math-academy-id'in q};tu={str(c[':tutorial/math-academy-id']):c for c in D['contents']if ':tutorial/content'in c};sources=json.loads((H/'sources.json').read_text())if(H/'sources.json').exists()else[];seen={(s['identity'],s['attribute'],s['html'])for s in sources};prior=bool(sources)
def add(ident,attr,part,path):
 if part is None:return
 html=str(part);key=(ident,attr,html)
 if key in seen:return
 seen.add(key);fs=ns['formulas'](html);sources.append({'identity':ident,'attribute':attr,'path':str(path),'formulas':fs,'html':html})
for t in ([]if prior else D['topics']):
 p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(t['ma_id'])/'Source'/f"{t['ma_id']}.html"
 if not p.exists():continue
 s=BeautifulSoup(p.read_text(),'html.parser');m=json.loads(p.with_suffix('.json').read_text())
 for i in m['lesson']['items']:
  node=s.find(id=i['dom_id'])
  if node is None:continue
  if i.get('step_type')=='tutorial'and str(i.get('content_id'))in tu:add('tutorial:'+str(i['content_id']),'tutorial/content',node,p)
  ident=('e-'+str(i['content_id']))if i.get('step_type')=='example'else'q-'+str(i['question_id'])if i.get('question_id')else None
  if ident not in targets:continue
  add(ident,'question/problem',node.find(class_='exampleQuestion')if ident.startswith('e-')else node.find(class_='questionText')or node.find(class_='questionWidget-text'),p)
  add(ident,'question/worked-solution',node.find(class_='exampleSolution')or node.find(class_='questionExplanation')or node.find(class_='questionWidget-explanation'),p)
for line in((H/'source-paths-added.txt')if prior else(H/'source-paths-fresh.txt')).read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)|(?:example|e)-(\d+)',p.name)
 if not m:continue
 ident=m[1]or'e-'+m[2]
 if ident not in targets:continue
 p=p if p.is_absolute()else R/p
 if not p.exists():continue
 try:d=json.loads(p.read_text())
 except Exception:continue
 html=d.get('html')or d.get('raw_html')
 if not html:continue
 s=BeautifulSoup(html,'html.parser')
 observed={('q-'+m[1]) for n in s.select('[id]') if (m:=re.fullmatch(r'question-(\d+)',n.get('id','')))}
 if observed and ident not in observed:continue
 add(ident,'question/problem',s.find(class_='exampleQuestion')if ident.startswith('e-')else s.find(class_='questionWidget-text')or s.find(class_='questionText'),p)
 add(ident,'question/worked-solution',s.find(class_='exampleSolution')or s.find(class_='questionExplanation')or s.find(class_='questionWidget-explanation'),p)
(H/'sources.json').write_text(json.dumps(sources,indent=2)+'\n');print('source records',len(sources),'identities',len(set(s['identity']for s in sources)),'tutorials',len(tu),'source question identities',len(targets));print('source formula errors',[(s['identity'],s['attribute'],f)for s in sources for f in s['formulas']if not isinstance(f,str)])
