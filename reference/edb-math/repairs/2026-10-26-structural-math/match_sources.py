"""Identity-bound structural matches with equivalent derivative spellings."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';OLD=R/'reference/edb-math/repairs/2026-10-24-mathml-tables';sys.path[:0]=[str(R/'scripts'),str(OLD)]
from source_tables import LegacyRenderer
def slim_dom(markup):
 return re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:'<svg>'+''.join(re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I))+'</svg>',markup,flags=re.I)
from layout import grid_key,expected_layout
meta=json.loads((W/'metadata.json').read_text());parents=json.loads((W/'parents.json').read_text());candidates=json.loads((H/'table-candidates.json').read_text())
def identities(e,attr):
 m=meta.get(str(e),{})
 if attr=='tutorial/content':return ['tutorial:'+str(m.get('tutorial/math-academy-id'))]
 if attr=='answer/value':return list({meta.get(str(q),{}).get('question/math-academy-id')for f,a in parents.get(str(e),[])if a=='answer-field/choices'for q,a in parents.get(str(f),[])if a=='question/answer-fields'})
 return [m.get('question/math-academy-id')]
wanted={(i,c['a'])for c in candidates+json.loads((H/'malformed-structure.json').read_text()) for i in identities(c['e'],c['a'])if i}
field_sources=[]
def normcell(s):
 # Matching only: retain current bytes when a repair is compiled.
 s=s.replace('′',"'").replace(r'\prime',"'").replace('\u2061','').replace('\u2062','').replace('−','-')
 return s
def key(rows):return grid_key([[normcell(c)for c in row]for row in rows])
sources=[]
for name in ['archived-tables.json','capture-tables.json','choice-tables.json','new-capture-tables.json']:
 for s in json.loads((OLD/name).read_text()):
  if(s['identity'],s['attribute'])in wanted:sources.append(s)
counts=collections.Counter()
for p in sorted(Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*.json')):
 counts['archive_metadata_files_examined']+=1
 if not p.with_suffix('.html').exists():continue
 d=json.loads(p.read_text());use=[]
 for i in d.get('lesson',{}).get('items',[]):
  if i.get('item_type')=='step':identity='tutorial:'+str(i['content_id'])if i.get('step_type')=='tutorial'else'e-'+str(i['content_id'])
  elif i.get('question_id'):identity='q-'+str(i['question_id'])
  else:continue
  if any(x==identity for x,a in wanted):use.append((i,identity))
 if not use:continue
 raw=p.with_suffix('.html').read_text();counts['source_html_files_read']+=1
 if '<mtable'not in raw:continue
 soup=BeautifulSoup(slim_dom(raw),'html.parser')
 for i,identity in use:
  root=soup.find(id=i.get('dom_id'))
  if root is None:continue
  if identity.startswith('tutorial:'):parts=[('tutorial/content',root)]
  else:parts=[(a,n)for a,cs in [('question/problem',['exampleQuestion','questionWidget-text','questionText']),('question/worked-solution',['exampleExplanation','questionExplanation','questionWidget-explanation'])]for cls in cs for n in root.find_all(class_=cls)]
  for a,part in parts:
   if(identity,a)not in wanted:continue
   field_sources.append({'identity':identity,'attribute':a,'path':str(p.with_suffix('.html')),'html':str(part)})
   for t in part.find_all('mtable'):
    r=LegacyRenderer(None);rows=[[r.m(td)for td in tr.find_all('mtd',recursive=False)]for tr in t.find_all(['mtr','mlabeledtr'],recursive=False)]
    sources.append({'identity':identity,'attribute':a,'path':str(p.with_suffix('.html')),'source_attributes':dict(t.attrs),'rows':rows,'source_mathml':str(t),'errors':r.errors,'topic':d['topic_id'],'dom_id':i.get('dom_id'),'source_parent':str(t.parent)[:15000]})
# Older question captures retain exact practice question DOM, including unruled tables.
def captured(html,identity,path):
 if not isinstance(html,str)or '<'not in html:return
 soup=BeautifulSoup(slim_dom(html),'html.parser')
 for a,classes in [('question/problem',['exampleQuestion','questionWidget-text','questionText']),('question/worked-solution',['exampleExplanation','questionExplanation','questionWidget-explanation'])]:
  if(identity,a)not in wanted:continue
  seen=set()
  for cls in classes:
   for part in soup.find_all(class_=cls):
    if id(part)in seen:continue
    seen.add(id(part));field_sources.append({'identity':identity,'attribute':a,'path':str(path),'html':str(part)})
    for t in part.find_all('mtable'):
     r=LegacyRenderer(None);rows=[[r.m(td)for td in tr.find_all('mtd',recursive=False)]for tr in t.find_all(['mtr','mlabeledtr'],recursive=False)]
     sources.append({'identity':identity,'attribute':a,'path':str(path),'source_attributes':dict(t.attrs),'rows':rows,'source_mathml':str(t),'errors':r.errors,'source_parent':str(t.parent)[:15000]})
paths=json.loads((H/'additional-source-paths.json').read_text());states=set()
for filename,identity in paths:
 p=Path(filename);p=p if p.is_absolute()else R/p
 if not p.exists():continue
 data=json.loads(p.read_text());captured(data.get('html')or data.get('raw_html'),identity,p);counts['capture_files_read']+=1
 state=p.parent/'state.json'
 if state.exists()and state not in states:
  states.add(state);d=json.loads(state.read_text());counts['capture_state_files_read']+=1
  for identity,q in d.get('questions',{}).items():
   if not isinstance(q,dict)or not any(i==identity for i,a in wanted):continue
   for k in ['before','history','after']:
    if isinstance(q.get(k),dict):captured(q[k].get('html')or q[k].get('raw_html'),identity,state)
(W/'source-fields.json').write_text(json.dumps(field_sources))
index=collections.defaultdict(list)
for s in sources:index[s['identity'],s['attribute'],key(s['rows'])].append(s)
matched=[];unmatched=[];ambiguous=[]
for c in candidates:
 found=[s for identity in identities(c['e'],c['a'])for s in index.get((identity,c['a'],key(c['rows'])),[])]
 # Only source layout, not spelling or color, controls a structural repair.
 layouts=collections.defaultdict(list)
 for s in found:
  a=s['source_attributes'];layout=tuple((k,str(a.get(k,'')))for k in ['columnalign','columnlines','rowlines','frame','columnspacing','rowspacing']);layouts[layout].append(s)
 if len(layouts)==1:matched.append({**c,'source':found[0],'source_options':len(found)})
 elif found:ambiguous.append({**c,'sources':found})
 else:unmatched.append({**c,'identities':identities(c['e'],c['a'])})
for name,rows in [('source-matches',matched),('source-unmatched',unmatched),('source-ambiguous',ambiguous)]: (H/(name+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
(W/'sources.json').write_text(json.dumps(sources));report={**counts,'candidate_occurrences':len(candidates),'retained_or_archive_source_tables':len(sources),'identity_and_grid_matched_occurrences':len(matched),'unmatched_occurrences':len(unmatched),'ambiguous_occurrences':len(ambiguous)};(H/'source-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
