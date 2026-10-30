"""Cross-check complete available source prompts/tutorials and ordered numeric grids."""
import collections,copy,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;P=H.parent;R=P.parents[3];sys.path[:0]=[str(P),str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer,reconstruct
from question_capture.math_format import normalize_source_tex
from math_checks import matrices
S1=json.loads((P/'lesson.json').read_text());S2=json.loads((P/'expanded-scope/current.json').read_text());qs=json.loads((H/'proposed-questions.json').read_text());targets={q[':question/math-academy-id']:q for q in qs};sources=collections.defaultdict(list);tutorials={str(c[':tutorial/math-academy-id']):c for s in[S1,S2]for c in s['contents']if ':tutorial/content'in c};topics=[S1['topic']]+S2['topics']
def add(mid,attribute,node,path):
 if node is not None:sources[mid,attribute].append({'path':str(path),'html':str(node)})
for t in topics:
 ma=t[':topic/math-academy-id'];p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(ma)/'Source'/f'{ma}.html';data=json.loads(p.with_suffix('.json').read_text());s=BeautifulSoup(p.read_text(),'html.parser')
 for item in data['lesson']['items']:
  node=s.find(id=item['dom_id'])
  if node is None:continue
  if item.get('step_type')=='tutorial'and str(item.get('content_id'))in tutorials:add('tutorial:'+str(item['content_id']),'tutorial/content',node,p)
  mid='e-'+str(item['content_id'])if item.get('step_type')=='example'else'q-'+str(item['question_id'])if item.get('question_id')else None
  if mid not in targets:continue
  add(mid,'question/problem',node.select_one('.exampleQuestion,.questionText,.questionWidget-text'),p)
  add(mid,'question/worked-solution',node.select_one('.exampleSolution,.questionExplanation,.questionWidget-explanation'),p)
for line in(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)|example-(\d+)',p.name)
 if not m:continue
 mid=m[1]or'e-'+m[2]
 if mid not in targets or not p.exists():continue
 try:d=json.loads(p.read_text())
 except Exception:continue
 html=d.get('html')or d.get('raw_html')
 if not html:continue
 s=BeautifulSoup(html,'html.parser');add(mid,'question/problem',s.select_one('.exampleQuestion,.questionText,.questionWidget-text'),p);add(mid,'question/worked-solution',s.select_one('.exampleSolution,.questionExplanation,.questionWidget-explanation'),p)
def grids(html):
 s=BeautifulSoup(html,'html.parser')
 for control in s.select('.freeResponseTextbox,.matheditor-wrapper-answer,.selectList,.studentAnswer'):control.decompose()
 ns=s.select('.mjpage,mjx-container,math');ids={id(n)for n in ns};roots=[n for n in ns if not any(id(p)in ids for p in n.parents)];tex=[];errors=[]
 for n in roots:
  try:
   title=n.find('title')
   if title:value=reconstruct(title)
   else:
    math=n if n.name=='math'else n.find('math');assert math is not None
    r=SourceRenderer(None);value=normalize_source_tex(r.m(math));assert not r.errors,r.errors
   tex.append(value)
  except Exception as e:errors.append(str(e))
 return[tuple(tuple(str(c)for c in row)for row in m['matrix'].tolist())for t in tex for m in matrices(t)],errors
checks=[];review=[];missing=[]
for mid,q in targets.items():
 visible=q[':question/problem']+'\n'+''.join(f[':answer-field/key']for f in sorted(q.get(':question/answer-fields',[]),key=lambda f:f[':answer-field/key'])if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox');current=[tuple(tuple(str(c)for c in row)for row in m['matrix'].tolist())for m in matrices(visible)];options=sources[mid,'question/problem'];matches=[];mismatches=[]
 for src in options:
  sg,errors=grids(src['html'])
  if not errors and sg==current:matches.append(src['path'])
  else:mismatches.append({'path':src['path'],'source_grids':sg,'current_grids':current,'source_errors':errors})
 if matches:checks.append({'entity':q[':db/id'],'identity':mid,'matched_source_paths':sorted(set(matches)),'ordered_numeric_or_symbolic_matrix_grids_match':True,'matrices':len(current)})
 elif not options:missing.append({'entity':q[':db/id'],'identity':mid,'reason':'No archived prompt located'})
 else:review.append({'entity':q[':db/id'],'identity':mid,'candidates':mismatches})
for ident,c in tutorials.items():
 mid='tutorial:'+ident;options=sources[mid,'tutorial/content'];current=[tuple(tuple(str(x)for x in row)for row in m['matrix'].tolist())for m in matrices(c[':tutorial/content'])];matches=[];mismatches=[]
 for src in options:
  sg,errors=grids(src['html'])
  if sg==current and not errors:matches.append(src['path'])
  else:mismatches.append({'path':src['path'],'source_grids':sg,'current_grids':current,'source_errors':errors})
 if matches:checks.append({'entity':c[':db/id'],'identity':mid,'matched_source_paths':sorted(set(matches)),'ordered_numeric_or_symbolic_matrix_grids_match':True,'matrices':len(current)})
 elif not options:missing.append({'entity':c[':db/id'],'identity':mid,'reason':'No archived tutorial located'})
 else:review.append({'entity':c[':db/id'],'identity':mid,'candidates':mismatches})
report={'passed':not review and not missing,'checks':checks,'review':review,'missing':missing,'database_writes':0};(H/'source-grid-audit.json').write_text(json.dumps(report,indent=2)+'\n');(H/'source-inventory.json').write_text(json.dumps([{'identity':k[0],'attribute':k[1],**s}for k,ss in sources.items()for s in ss],indent=2)+'\n');print('Source matches',len(checks),'manual review',len(review),'missing',len(missing));print([(x['identity'],len(x.get('candidates',[])))for x in review]);print(missing)
