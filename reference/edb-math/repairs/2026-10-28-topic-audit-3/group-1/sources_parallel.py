"""Bounded parallel source read including hashed observations and full ownership."""
import concurrent.futures,json,multiprocessing,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};s=p.read_text();exec(compile(s.split('parents=json.loads')[0]+s[s.index('def roots(s):'):s.index('def visible(tex):')],str(p),'exec'),ns)
D=json.loads((H/'current.json').read_text());wanted={q.get(':question/math-academy-id')for q in D['questions']};sources=json.loads((H/'sources.json').read_text());seen={(s['identity'],s['attribute'],s['html'])for s in sources}
def read(line):
 p=Path(line);m=re.search(r'(q-\d+)|(?:example|e)-(\d+)',p.name)
 if not m:return [],'no identity'
 ident=m[1]or'e-'+m[2]
 if ident not in wanted:return [],'outside scope'
 p=p if p.is_absolute()else R/p
 try:d=json.loads(p.read_text())
 except Exception as ex:return [],str(ex)
 if not isinstance(d,dict):return [],'Not a raw capture object'
 html=d.get('html')or d.get('raw_html')
 if not isinstance(html,str)or not html:return [],'No retained raw HTML'
 soup=BeautifulSoup(html,'html.parser');observed={('q-'+m[1])for n in soup.select('[id]')if(m:=re.fullmatch(r'question-(\d+)',n.get('id','')))}
 if observed and ident not in observed:return [],'Observed DOM question identity mismatch'
 out=[]
 for attr,part in [('question/problem',soup.find(class_='exampleQuestion')if ident.startswith('e-')else soup.find(class_='questionWidget-text')or soup.find(class_='questionText')),('question/worked-solution',soup.find(class_='exampleSolution')or soup.find(class_='questionExplanation')or soup.find(class_='questionWidget-explanation'))]:
  if part is None:continue
  html=str(part)
  if(ident,attr,html)in seen:continue
  fs=ns['formulas'](html);out.append({'identity':ident,'attribute':attr,'path':str(p),'formulas':fs,'html':html,'source_validation':'Retained raw capture HTML; filename identity agrees with observed source question DOM when present.'})
 return out,None
limits=[];lines=(H/'source-paths-fresh.txt').read_text().splitlines()
with concurrent.futures.ProcessPoolExecutor(max_workers=4,mp_context=multiprocessing.get_context('fork'))as pool:
 for i,(rows,error)in enumerate(pool.map(read,lines,chunksize=4)):
  for row in rows:
   key=(row['identity'],row['attribute'],row['html'])
   if key not in seen:seen.add(key);sources.append(row)
  if error:limits.append({'path':lines[i],'reason':error})
  if(i+1)%500==0:(H/'sources.json').write_text(json.dumps(sources,indent=2)+'\n');print(i+1,len(sources),flush=True)
(H/'sources.json').write_text(json.dumps(sources,indent=2)+'\n');(H/'source-path-resolution.json').write_text(json.dumps({'basis_t':9837,'paths':len(lines),'limits':limits},indent=2)+'\n');print('Final',len(sources),'identities',len({s['identity']for s in sources}),flush=True)
