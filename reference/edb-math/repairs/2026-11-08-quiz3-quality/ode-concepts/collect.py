import json,hashlib,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path('/home/jake/Developer/Course_Academy');HERE=Path(__file__).resolve().parent
occ=json.loads((ROOT/'reference/edb-math/imports/math-academy/newer-captures/source-occurrences.json').read_text())['records'];legacy=json.loads((ROOT/'reference/mathacademy/kp-difficulty-analysis-2026-10-12/capture-occurrences.json').read_text())
for out in sorted(HERE.glob('175*')):
 topic=json.loads((out/'topic.json').read_text());mid=topic[':topic/math-academy-id'];qs=json.loads((out/'questions.json').read_text());ids={q[':question/math-academy-id'] for q in qs}
 rec=[r for r in occ if r.get('topic_id')==mid or r.get('math_academy_id') in ids];dirs={Path(r['source_directory']) for r in rec};dirs.update((ROOT/r['source_file']).parent for r in legacy if r.get('question')in ids)
 source=Path(f'/home/jake/Developer/MA/DATA/Lessons/{mid}/Source/{mid}.html');soup=BeautifulSoup(source.read_text(),'html.parser')
 manifest=[]
 def desc(path,html,role):return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'html':html,'role':role}
 lessons=json.loads((out/'lessons.json').read_text());steps={s[':step/content'][':db/id']:s[':step/math-academy-id'] for a in lessons for s in a[0][':activity/steps']}
 for kp in topic[':topic/knowledge-points']:
  ce=kp[':knowledge-point/canonical-example'][':db/id'];
  for q in [kp[':knowledge-point/canonical-example']]+kp.get(':knowledge-point/questions',[]):
   qmid=q[':question/math-academy-id'];n=qmid.split('-')[-1];row={'entity':q[':db/id'],'mid':qmid,'prompt_sources':[],'solution_sources':[]}
   node=soup.select_one(('#step-'+str(steps[kp[':db/id']]))if qmid.startswith('e-')else('#question-'+n))
   if node:
    row['prompt_sources'].append(desc(source,str(node),'original lesson snapshot'))
    if qmid.startswith('e-'):row['solution_sources'].append(desc(source,str(node),'original lesson snapshot'))
   for d in sorted(dirs):
    pp=[d/(qmid+'-before.json')];sp=[d/('history-'+qmid+'.json')]
    if qmid.startswith('e-'):pp=[d/('example-'+n+'.json')];sp=pp
    if (d/'observations').exists():pp+=list((d/'observations').glob('history-'+qmid+'-*.json'));sp+=list((d/'observations').glob('history-solution-'+qmid+'-*.json'))
    for role,paths in [('prompt_sources',pp),('solution_sources',sp)]:
     for p in paths:
      if p.is_file():
       c=json.loads(p.read_text());html=c.get('html','')
       if html:row[role].append(desc(p,html,'saved original DOM'))
   manifest.append(row)
 (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2));(out/'source-records.json').write_text(json.dumps(rec,indent=2));
 (out/'source-summary.json').write_text(json.dumps({'topic':mid,'original':str(source),'questions':len(manifest),'missing_prompt':[r['mid']for r in manifest if not r['prompt_sources']],'missing_solution':[r['mid']for r in manifest if not r['solution_sources']]},indent=2))
 print(out.name,mid,'orig prompts',sum(bool(r['prompt_sources'])for r in manifest),'solutions',sum(bool(r['solution_sources'])for r in manifest),flush=True)
