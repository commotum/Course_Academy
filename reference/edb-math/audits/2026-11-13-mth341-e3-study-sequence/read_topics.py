"""Cache read-only app topic lessons/practice; safe for parallel branch auditors."""
import argparse,collections,fcntl,json,sys
from pathlib import Path
from urllib.request import urlopen
OUT=Path(__file__).resolve().parent

def fetch(topic):
 graph=json.loads((OUT/'graph-api.json').read_text());node=next(n for n in graph['nodes']if n['id']==topic)
 directory=OUT/'topics'/str(topic);directory.mkdir(parents=True,exist_ok=True)
 with (directory/'capture.lock').open('a')as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for name,url in [('lesson','/api/topic?topic='+node['uuid']),('practice','/api/preview?topicId='+str(topic))]:
   path=directory/(name+'.json')
   if not path.exists():
    with urlopen('http://127.0.0.1:8765'+url,timeout=60)as r:data=json.load(r)
    temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2));temporary.replace(path)
  lesson=json.loads((directory/'lesson.json').read_text());practice=json.loads((directory/'practice.json').read_text())
  lines=['# '+str(topic)+' '+node['name'],f'Lesson API basis {lesson.get("basis")}; practice API basis {practice.get("basis")}; graph/progress basis {graph["basis"]}.','## Lesson content']
  for s in lesson.get('sections',[]):
   lines.extend([f'### {s.get("kind")} {s.get("contentId")} — {s.get("title")}',s.get('markdown',''),s.get('workedSolution','')])
  grouped=collections.defaultdict(list)
  for s in practice.get('steps',[]):
   if s['kind']=='question':grouped[s.get('title','')].append(s)
  lines.append('## Representative practice (first three per skill; full bank in practice.json)')
  for title,questions in grouped.items():
   lines.append('### '+title+f' ({len(questions)} captured questions)')
   for s in questions[:3]:
    lines.extend([f'Question {s["contentId"]} — {s.get("difficulty")}',s['markdown'],'Solution: '+s.get('solution','')])
    for f in s.get('fields',[]):
     if f.get('correctAnswer'):lines.append('Answer '+f['key']+': '+str(f['correctAnswer'].get('value')))
  (directory/'readable.md').write_text('\n\n'.join(lines)+'\n')
 return {'id':topic,'title':node['name'],'lesson_basis':lesson.get('basis'),'practice_basis':practice.get('basis'),'path':str(directory/'readable.md'),'sections':len(lesson.get('sections',[])),'questions':sum(map(len,grouped.values()))}
if __name__=='__main__':
 for topic in map(int,sys.argv[1:]):print(json.dumps(fetch(topic)),flush=True)
