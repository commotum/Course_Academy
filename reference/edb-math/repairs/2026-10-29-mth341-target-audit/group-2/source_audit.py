import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer,reconstruct
S=json.loads((H/'current.json').read_text());targets={q[':question/math-academy-id']:q for q in S['questions']};tutorials={str(c[':tutorial/math-academy-id']):c for c in S['contents']if ':tutorial/content'in c};sources=collections.defaultdict(list)
def add(mid,attr,node,path):
 if node is not None:sources[mid,attr].append({'path':str(path),'html':str(node)})
for t in S['topics']:
 ma=t['ma_id'];p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(ma)/'Source'/f'{ma}.html';data=json.loads(p.with_suffix('.json').read_text());s=BeautifulSoup(p.read_text(),'html.parser')
 for item in data['lesson']['items']:
  node=s.find(id=item['dom_id'])
  if node is None:continue
  if item.get('step_type')=='tutorial'and str(item.get('content_id'))in tutorials:add('tutorial:'+str(item['content_id']),'tutorial/content',node,p)
  mid='e-'+str(item['content_id'])if item.get('step_type')=='example'else'q-'+str(item['question_id'])if item.get('question_id')else None
  if mid not in targets:continue
  add(mid,'question/problem',node.select_one('.exampleQuestion,.questionText,.questionWidget-text'),p);add(mid,'question/worked-solution',node.select_one('.exampleSolution,.exampleExplanation,.questionExplanation,.questionWidget-explanation'),p)
for line in(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)|example-(\d+)',p.name)
 if not m:continue
 mid=m[1]or'e-'+m[2]
 if mid not in targets or not p.exists():continue
 try:d=json.loads(p.read_text())
 except Exception:continue
 html=d.get('html')or d.get('raw_html')
 if not html:continue
 s=BeautifulSoup(html,'html.parser');add(mid,'question/problem',s.select_one('.exampleQuestion,.questionText,.questionWidget-text'),p);add(mid,'question/worked-solution',s.select_one('.exampleSolution,.exampleExplanation,.questionExplanation,.questionWidget-explanation'),p)
(H/'source-inventory.json').write_text(json.dumps([{'identity':mid,'attribute':a,**r}for(mid,a),ss in sources.items()for r in ss],indent=2)+'\n')
print('Sources',len(sources),'identities',len(set(mid for mid,a in sources)),'missing',[(q[':db/id'],mid)for mid,q in targets.items()if not sources[mid,'question/problem']])
