import sys
sys.dont_write_bytecode=True
import json,re,importlib.util,hashlib,collections
from pathlib import Path
from bs4 import BeautifulSoup,Tag
ROOT=Path('/home/jake/Developer/Course_Academy')
OUT=Path(__file__).resolve().parent
AUDIT=ROOT/'reference/edb-math/audits/2026-10-17-underbrace-import'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
lj=load('flat_original_json',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'))
md=load('flat_original_markdown',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py'))
PAT=re.compile(r'[_^]\(\s*[⏟⏞]')
rows=[x for x in json.loads((AUDIT/'current-affected.json').read_text()) if PAT.search(x['value'])]
links={x['source_identity']:x for x in json.loads((AUDIT/'source-census/affected-source-items.json').read_text())}
cache={};data=[]
for row in rows:
 source=links[row['source_id']];p=Path(source['file']).with_suffix('.html')
 if str(p) not in cache:cache[str(p)]=BeautifulSoup(p.read_text(),'html.parser')
 selector='#question-'+str(source['question_id']) if source['question_id'] else '#step-'+str(source['step_id'])
 step=cache[str(p)].select_one(selector);assert step
 accents=[];seen=set()
 for mo in step.select('mo'):
  if mo.text.strip() not in ('⏟','⏞'):continue
  inner=mo.parent
  assert inner.name in ['munder','mover'],str(inner)
  # Capture the full accent plus label when an outer script applies to it.
  outer=inner
  while isinstance(outer.parent,Tag) and outer.parent.name in ['mrow','mstyle'] and len(outer.parent.find_all(recursive=False))==1:outer=outer.parent
  if outer.parent.name in ['munder','mover'] and outer.parent.find_all(recursive=False)[0] is outer:outer=outer.parent
  if str(outer) in seen:continue
  seen.add(str(outer))
  raw=lj.mathml_to_text(outer);bad=md.normalize_math_tex(raw)
  accents.append({'mathml':str(outer),'raw':raw,'bad':bad,'glyph':mo.text.strip(),'math_source':str(mo.find_parent('math'))})
 data.append({'entity':row['entity'],'attribute':row['attribute'],'before':row['value'],'sourcepath':str(p),'selector':selector,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'accents':accents})
(OUT/'source-candidates.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
summary=collections.Counter();unmatched=[]
for row in data:
 s=re.sub(r'\s+','',row['before']);changed=s
 for a in sorted(row['accents'],key=lambda a:len(a['bad']),reverse=True):
  target=re.sub(r'\s+','',a['bad'])
  if target in changed:
   changed=changed.replace(target,'REPLACED');summary['matches']+=1
 if PAT.search(changed):unmatched.append({'entity':row['entity'],'attr':row['attribute'],'remaining':changed,'accents':row['accents']})
summary['rows']=len(data);summary['unmatched_rows']=len(unmatched)
(OUT/'unmatched.json').write_text(json.dumps(unmatched,ensure_ascii=False,indent=2)+'\n')
print(dict(summary))
for row in unmatched:print(row['entity'],row['attr'],[(a['bad'])for a in row['accents']])
