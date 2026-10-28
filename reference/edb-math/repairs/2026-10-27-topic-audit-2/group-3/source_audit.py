import collections,json,re,sys,difflib
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'snapshot.json').read_text());p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};code=p.read_text();exec(compile(code.split('parents=json.loads')[0],str(p),'exec'),ns);exec(compile(code[code.index('def roots('):code.index('def visible(')],str(p),'exec'),ns)
from question_capture.math_format import MATH,normalize_source_tex,normalize_tex
sources=collections.defaultdict(list);topics={t['entity']:t for t in D['topics']};allq={q[':question/math-academy-id']:q for q in D['questions']if ':question/math-academy-id'in q};srcroot=Path('/home/jake/Developer/MA/DATA/Lessons');tutorials={c[':tutorial/math-academy-id']:c for c in D['content']if ':tutorial/content'in c};tutorial_source={};rawpaths=[]
for topic in topics.values():
 raw=srcroot/str(topic['ma_id'])/'Source'/f"{topic['ma_id']}.html"
 if not raw.exists():continue
 soup=BeautifulSoup(raw.read_text(),'html.parser');meta=json.loads(raw.with_suffix('.json').read_text())
 for item in meta['lesson']['items']:
  node=soup.find(id=item['dom_id'])
  if node is None:continue
  if item.get('step_type')=='tutorial':
   mid=int(item['content_id'])
   if mid in tutorials:tutorial_source[mid]=(str(raw),str(node))
  elif item.get('step_type')=='example':
   ident='e-'+str(item['content_id'])
   if ident in allq:sources[ident].append((str(raw),str(node)))
for line in (R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)\.json$|example-(\d+)\.json$',p.name)
 if m and(m[1]or m[2]or'e-'+m[3])in allq:rawpaths.append((m[1]or m[2]or'e-'+m[3],p if p.is_absolute()else R/p))
for ident,p in rawpaths:
 if not p.exists():continue
 try:data=json.loads(p.read_text());html=data.get('html')or data.get('raw_html')
 except Exception:continue
 if html:sources[ident].append((str(p),html))
reports=[];candidates=[];direct=[];source_records=[]
def plain(v):
 return re.sub(r'\s+|[{}]','',re.sub(r'\\color\{[^{}]+\}','',normalize_source_tex(v))).replace('⁡','').replace(r'\cdot',r'\times')
def extract(v):return [m[0][2:-2]if m[0].startswith(('$$',r'\[',r'\('))else m[0][1:-1]for m in MATH.finditer(v)]
def check(e,a,before,html,path,ident):
 fs=ns['formulas'](html);old=extract(before);errors=[f for f in fs if not isinstance(f,str)]
 r={'entity':e,'attribute':a,'source_identity':ident,'path':path,'source_formulas':len(fs),'stored_formulas':len(old),'source_errors':errors,'exact_formula_sequence':not errors and list(map(plain,fs))==list(map(plain,old))};reports.append(r)
 if errors:return
 source_records.append({'entity':e,'attribute':a,'source_identity':ident,'path':path,'html':html,'formulas':fs})
 if len(fs)==len(old):
  change=[]
  for i,(x,y)in enumerate(zip(old,fs)):
   if plain(x)==plain(y)and r'\color'in y and r'\color'not in x:change.append((i,x,y))
  if change:
   after=before;ms=list(MATH.finditer(before))
   for i,x,y in reversed(change):
    m=ms[i];after=after[:m.start()]+('$$\n'+y+'\n$$'if m[0].startswith('$$')else'$'+y+'$')+after[m.end():]
   candidates.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':'Restore original source row/column highlighting.','evidence':{'path':path,'identity':ident,'formula_indices':[c[0]for c in change]},'confidence':'high'})
for mid,c in tutorials.items():
 if mid in tutorial_source:
  path,html=tutorial_source[mid];check(c[':db/id'],'tutorial/content',c[':tutorial/content'],html,path,'t-'+str(mid))
 else:reports.append({'entity':c[':db/id'],'attribute':'tutorial/content','source_identity':'t-'+str(mid),'missing_source':True})
for ident,q in allq.items():
 avail=sources[ident]
 if not avail:reports.append({'entity':q[':db/id'],'source_identity':ident,'missing_source':True});continue
 # Retain all source alternatives in manifest, compare distinct source contents once.
 hashes=set()
 for path,html in avail:
  soup=BeautifulSoup(html,'html.parser');problem=soup.find(class_='exampleQuestion')if ident.startswith('e-')else soup.find(class_='questionWidget-text')or soup.find(class_='questionText');solution=soup.find(class_='exampleExplanation')if ident.startswith('e-')else soup.find(class_='questionExplanation')or soup.find(class_='questionWidget-explanation')or soup.find(class_='workedSolution')
  for a,node in [('question/problem',problem),('question/worked-solution',solution)]:
   if node is None or ':'+a not in q:continue
   key=(a,str(node))
   if key in hashes:continue
   hashes.add(key);check(q[':db/id'],a,q[':'+a],str(node),path,ident)
(H/'source-comparisons.json').write_text(json.dumps(reports,indent=2));(H/'source-highlight-candidates.json').write_text(json.dumps(candidates,indent=2));(H/'source-records.json').write_text(json.dumps(source_records,indent=2));(H/'source-manifest.json').write_text(json.dumps({i:[x[0]for x in ss]for i,ss in sources.items()},indent=2));print('source questions',len(sources),'tutorials',len(tutorial_source),'comparisons',len(reports),'exact',sum(bool(r.get('exact_formula_sequence'))for r in reports),'candidates',len(candidates));print('missing',sum(bool(r.get('missing_source'))for r in reports))
