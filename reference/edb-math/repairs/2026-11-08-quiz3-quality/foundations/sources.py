import json,re,hashlib,sys
from pathlib import Path
from bs4 import BeautifulSoup
root=Path.cwd();out=root/'reference/edb-math/repairs/2026-11-08-quiz3-quality/foundations'
occ=json.loads((root/'reference/edb-math/imports/math-academy/newer-captures/source-occurrences.json').read_text())['records']
# Search filenames once, including ignored captures.
import subprocess
paths=[Path(s)for s in subprocess.check_output(['rg','--files','--hidden','--no-ignore','reference/mathacademy'],text=True).splitlines()if s.endswith(('.json','.html'))]
index={}
for path in paths:
 for ident in re.findall(r'(?:q|e)-[0-9]+',path.name):index.setdefault(ident,[]).append(path)
print('indexed',len(paths),flush=True)
for d in sorted(out.glob('175*')):
 t=json.loads((d/'topic-before.json').read_text());qs=json.loads((d/'questions-before.json').read_text()); mid=t[':topic/math-academy-id'];p=Path(f'/home/jake/Developer/MA/DATA/Lessons/{mid}/Source/{mid}.html');soup=BeautifulSoup(p.read_text(),'html.parser')
 steps={s[':step/content'][':knowledge-point/canonical-example'][':db/id']:str(s[':step/math-academy-id'])for a in json.loads((d/'lessons-before.json').read_text())for s in a[0].get(':activity/steps',[])if s.get(':step/content',{}).get(':knowledge-point/canonical-example')}
 manifest=[]
 for q in qs:
  id=q.get(':question/math-academy-id','');n=id.split('-')[-1];r={'entity':q[':db/id'],'mid':id,'prompt_sources':[],'solution_sources':[]}
  def add(role,path,html,kind):
   if html and not any(a['path']==str(path)for a in r[role]):r[role].append({'path':str(path),'html':html,'role':kind,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  node=soup.select_one('#question-'+n)if id.startswith('q-')else soup.select_one('#step-'+steps.get(q[':db/id'],'MISSING'))
  if node:
   add('prompt_sources',p,str(node),'lesson snapshot')
   if id.startswith('e-'):add('solution_sources',p,str(node),'lesson snapshot')
  matches=index.get(id,[])
  for f in matches:
   if f.suffix!='.json':continue
   try:c=json.loads(f.read_text())
   except:continue
   if not isinstance(c,dict):continue
   html=c.get('html')
   if not html:continue
   role='solution_sources'if 'solution-'in f.name or re.match('history-q-[^-]+\.json',f.name)else'prompt_sources'
   add(role,root/f,html,'saved DOM')
   if id.startswith('e-'):add('solution_sources',root/f,html,'saved DOM')
  manifest.append(r)
 (d/'source-manifest.json').write_text(json.dumps(manifest,indent=2))
 print(mid,len(qs),'prompt sources',sum(bool(r['prompt_sources'])for r in manifest),'solutions',sum(bool(r['solution_sources'])for r in manifest))
