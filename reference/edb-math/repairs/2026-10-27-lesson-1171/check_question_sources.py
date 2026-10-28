import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('index=collections.defaultdict(list)')[0],str(p),'exec'),ns);D=json.loads((H/'proposed.json').read_text());targets={q[':question/math-academy-id']:q for q in D['questions']if':question/math-academy-id'in q};sources=collections.defaultdict(list)
raw=Path('/home/jake/Developer/MA/DATA/Lessons/1171/Source/1171.html');soup=BeautifulSoup(raw.read_text(),'html.parser');meta=json.loads(raw.with_suffix('.json').read_text())
for item in meta['lesson']['items']:
 ident=('e-'+str(item['content_id']))if item.get('step_type')=='example'else'q-'+str(item['question_id'])if item.get('question_id')else None
 if ident not in targets:continue
 node=soup.find(id=item['dom_id']);part=node.find(class_='exampleQuestion')if ident.startswith('e-')else node.find(class_='questionText')or node.find(class_='questionWidget-text')
 if part:sources[ident].append((str(raw),str(part)))
paths=[]
for line in(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)\.json$|example-(\d+)\.json$',p.name)
 if m and(m[1]or m[2]or'e-'+m[3])in targets:paths.append((m[1]or m[2]or'e-'+m[3],p if p.is_absolute()else R/p))
for ident,p in paths:
 if not p.exists():continue
 data=json.loads(p.read_text());html=data.get('html')or data.get('raw_html')
 if not html:continue
 root=BeautifulSoup(html,'html.parser');part=root.find(class_='exampleQuestion')if ident.startswith('e-')else root.find(class_='questionWidget-text')or root.find(class_='questionText')
 if part:sources[ident].append((str(p),str(part)))
# Compare complete given matrices, excluding editable HTML tables and option banks.
sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,environment,cells
canon=lambda c:re.sub(r'\s+|[{}]','',re.sub(r'\\color\{[A-Za-z]+\}','',c)).replace('⁡','').replace(r'\operatornameln',r'\ln').replace(r'\times',r'\cdot')
def matrices(text):
 out=[]
 for m in ENV.finditer(text):
  if m.groups()!=('begin','bmatrix'):continue
  span=environment(text,m.start());out.append([[canon(c)for c in row]for row in cells(text[span[0]:span[1]])])
 return out
report=[]
for ident,q in targets.items():
 want=matrices(q[':question/problem']);attempts=[]
 for path,html in sources[ident]:
  fs=ns['formulas'](html)
  if any(not isinstance(f,str)for f in fs):continue
  actual=matrices('\n'.join(fs));attempts.append({'path':path,'match':actual==want,'matrix_count':len(actual)})
 matched=next((a for a in attempts if a['match']),None);report.append({'entity':q[':db/id'],'source_identity':ident,'source_match':matched,'available_comparisons':len(attempts),'given_matrices':len(want)})
(H/'question-source-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Direct source matches',sum(bool(r['source_match'])for r in report),'of',len(report));print('No direct match',[(r['source_identity'],r['available_comparisons'])for r in report if not r['source_match']])
