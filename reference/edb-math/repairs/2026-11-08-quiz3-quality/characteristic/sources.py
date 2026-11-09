import json,sys,hashlib,re
from pathlib import Path
from bs4 import BeautifulSoup
root=Path('/home/jake/Developer/Course_Academy');base=root/'reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic'
a=json.loads((root/'reference/edb-math/imports/math-academy/newer-captures/source-occurrences.json').read_text())['records'];b=json.loads((root/'reference/mathacademy/kp-difficulty-analysis-2026-10-12/capture-occurrences.json').read_text())
files=list((root/'reference/mathacademy').rglob('*.json'))
for d in base.glob('175*'):
 qs=json.loads((d/'questions.json').read_text());t=json.loads((d/'topic.json').read_text());mid=t[':topic/math-academy-id'];mids={q[':question/math-academy-id']for q in qs};index=[r for r in a if r.get('math_academy_id')in mids];occ=[r for r in b if r.get('question')in mids]
 original=Path('/home/jake/Developer/MA/DATA/Lessons')/str(mid)/'Source'/f'{mid}.html';soup=BeautifulSoup(original.read_text(),'html.parser')
 dirs={Path(r['source_directory'])for r in index};dirs.update((root/r['source_file']).parent for r in occ);rows=[]
 for q in qs:
  qmid=q[':question/math-academy-id'];n=qmid.split('-')[-1];paths={p for p in files if re.search(re.escape(qmid)+r'(?![0-9])',p.name) or p.name==f'example-{n}.json'}
  # Source index content records preserve original structured data even where no named snapshot exists.
  sources=[{'path':str(original),'sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'kind':'original lesson HTML','node':str(soup.select_one('#question-'+n))} ]if soup.select_one('#question-'+n)else []
  for p in sorted(paths):
   try:
    cap=json.loads(p.read_text());html=cap.get('html')if isinstance(cap,dict)else None
    if html:sources.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':'saved DOM','html':html})
   except:pass
  rows.append({'eid':q[':db/id'],'mid':qmid,'sources':sources,'indexed_sources':[r for r in index if r.get('math_academy_id')==qmid],'occurrences':[r for r in occ if r.get('question')==qmid]})
 (d/'source-manifest.json').write_text(json.dumps(rows,indent=2))
 (d/'original-source.json').write_text(json.dumps({'path':str(original),'sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'tutorial_steps':[s[':step/math-academy-id']for l in json.loads((d/'lessons.json').read_text())for s in l[0][':activity/steps']]}))
 print(d.name,len(rows),sum(bool(r['sources'])for r in rows),sum(bool(r['indexed_sources'])for r in rows))
