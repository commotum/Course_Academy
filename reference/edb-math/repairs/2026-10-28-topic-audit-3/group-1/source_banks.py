import json,re,sys,collections,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};s=p.read_text();exec(compile(s.split('parents=json.loads')[0]+s[s.index('def roots(s):'):s.index('def visible(tex):')],str(p),'exec'),ns)
D=json.loads((H/'current.json').read_text());wanted={q.get(':question/math-academy-id')for q in D['questions']};rows=[]
# Direct original lesson banks, in their complete response frame.
for t in D['topics']:
 p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(t['ma_id'])/'Source'/f"{t['ma_id']}.html"
 if not p.exists():continue
 soup=BeautifulSoup(p.read_text(),'html.parser')
 for widget in soup.select('[id^="question-"]'):
  ident='q-'+widget.get('id','')[len('question-'):]
  if ident not in wanted:continue
  widget=soup.find(id='question-'+ident[2:])
  if widget is None:continue
  opts=widget.select('.questionWidget-choiceText')
  if opts:rows.append({'identity':ident,'path':str(p),'kind':'original-lesson','choices':[{'html':str(n),'formulas':ns['formulas'](str(n))}for n in opts]})
def read(line):
 p=Path(line);m=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)\.json$|example-(\d+)\.json$',p.name)
 if not m:return None
 ident=m[1]or m[2]or'e-'+m[3]
 if ident not in wanted:return None
 p=p if p.is_absolute()else R/p
 try:d=json.loads(p.read_text())
 except Exception:return None
 fields=[]
 for f in d.get('fields',[]):
  choices=[]
  for a in f.get('choices',[]):
   html=a.get('html','');fs=ns['formulas'](html)if html else[]
   choices.append({'html':html,'formulas':fs,'captured_value':a.get('value'),'captured_type':a.get('type'),'option':a.get('option')})
  fields.append({'key':f.get('key'),'type':f.get('type'),'choices':choices})
 return {'identity':ident,'path':str(p),'kind':'retained-capture','fields':fields}if fields else None
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for row in pool.map(read,(H/'source-paths-fresh.txt').read_text().splitlines()):
  if row:rows.append(row)
# Deduplicate equal HTML banks; retain all paths as provenance.
unique={}
for row in rows:
 bank=row.get('fields',row.get('choices'));key=(row['identity'],json.dumps(bank,sort_keys=True))
 if key in unique:unique[key]['additional_paths'].append(row['path'])
 else:row['additional_paths']=[];unique[key]=row
out=list(unique.values());(H/'source-banks.json').write_text(json.dumps(out,indent=2)+'\n');print('banks',len(out),'identities',len({r['identity']for r in out}))
