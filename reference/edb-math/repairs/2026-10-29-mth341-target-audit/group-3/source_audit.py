import json,re,sys,collections
from pathlib import Path
from bs4 import BeautifulSoup,Tag
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer,reconstruct
from question_capture.math_format import normalize_source_tex
S=json.loads((H/'current.json').read_text());qs={q.get(':question/math-academy-id','generated:'+str(q[':db/id'])):q for q in S['questions']};src=collections.defaultdict(list)
def add(mid,node,path):
 if mid not in qs or node is None:return
 parts={}
 for attr,sel in [('question/problem','.exampleQuestion,.questionText,.questionWidget-text'),('question/worked-solution','.exampleSolution,.exampleExplanation,.questionExplanation,.questionWidget-explanation')]:
  n=node.select_one(sel)
  if n is None:continue
  roots=n.select('.mjpage,mjx-container,math');ids={id(x)for x in roots};roots=[x for x in roots if not any(id(a)in ids for a in x.parents)];tex=[];err=[]
  for x in roots:
   if x.find_parent(class_='selectList') or x.find_parent(class_='freeResponseTextbox'):continue
   try:
    title=x.find('title')
    if title:v=reconstruct(title)
    else:
     math=x if x.name=='math'else x.find('math');assert math is not None
     rd=SourceRenderer(None);v=normalize_source_tex(rd.m(math));assert not rd.errors,rd.errors
    tex.append(v)
   except Exception as e:err.append(str(e))
  parts[attr]={'html':str(n),'text':n.get_text(' ',strip=True),'formulas':tex,'errors':err,'images':[x.get('src')for x in n.select('img')],'styles':[(x.name,x.get('mathcolor'),x.get('mathvariant'))for x in n.select('[mathcolor],[mathvariant]')]}
 src[mid].append({'path':str(path),'parts':parts})
for t in S['topics']:
 ma=t['ma_id'];p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(ma)/'Source'/f'{ma}.html';soup=BeautifulSoup(p.read_text(),'html.parser');d=json.loads(p.with_suffix('.json').read_text())
 for item in d['lesson']['items']:
  mid='e-'+str(item['content_id'])if item.get('step_type')=='example'else'q-'+str(item['question_id'])if item.get('question_id')else None
  if mid:add(mid,soup.find(id=item['dom_id']),p)
paths=(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines()
for path in paths:
 p=Path(path);m=re.search(r'(q-\d+)|example-(\d+)',p.name)
 if not m:continue
 mid=m[1]or'e-'+m[2]
 if mid not in qs or not p.exists():continue
 try:d=json.loads(p.read_text())
 except Exception:continue
 html=d.get('html')or d.get('raw_html')
 if html:add(mid,BeautifulSoup(html,'html.parser'),p)
(H/'source-inventory.json').write_text(json.dumps(src,indent=2)+'\n')
report=[{'entity':q[':db/id'],'identity':mid,'source_paths':sorted({v['path']for v in src[mid]}),'sources':len(src[mid]),'prompt_formulas':len(src[mid][0]['parts'].get('question/problem',{}).get('formulas',[]))if src[mid]else 0}for mid,q in qs.items()]
(H/'source-coverage.json').write_text(json.dumps(report,indent=2)+'\n');print('Sources',sum(bool(x['sources'])for x in report),'/',len(qs),'captures',sum(x['sources']for x in report));print('Missing',[x['identity']for x in report if not x['sources']])
for q in S['questions']:
 if not q.get(':question/worked-solution'):
  print('MISSING',q[':db/id'],q.get(':question/math-academy-id','generated:'+str(q[':db/id'])),len(src[q.get(':question/math-academy-id','generated:'+str(q[':db/id']))]))
