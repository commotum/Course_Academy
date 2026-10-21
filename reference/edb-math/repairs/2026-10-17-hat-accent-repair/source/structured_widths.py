import sys
sys.dont_write_bytecode=True
import json,collections,importlib.util
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path('/home/jake/Developer/Course_Academy');P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('hat_history_width',ROOT/'scripts/import_historical_question_content.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
metadata={x[':db/id']:x for x in json.loads((P.parent/'evidence/metadata.json').read_text())}
archive=json.loads((P/'archive-index.json').read_text());inventory=json.loads((P.parent/'structured-base-inventory.json').read_text());seed=json.loads((P/'seed-source-proofs.json').read_text())
def identity(obj):
 if isinstance(obj,dict):
  if ':question/math-academy-id'in obj:return obj[':question/math-academy-id']
  if ':tutorial/math-academy-id'in obj:return 'tutorial-'+str(obj[':tutorial/math-academy-id'])
  for v in obj.values():
   found=identity(v)
   if found:return found
 elif isinstance(obj,list):
  for v in obj:
   found=identity(v)
   if found:return found
 return None
bybase=collections.defaultdict(list);byid=collections.defaultdict(list)
for sid,entries in archive.items():
 for e in entries:
  n=BeautifulSoup(e['mathml'],'html.parser').mover;cs=n.find_all(recursive=False);base=m.Renderer(None).m(cs[0]);item={'command':e['command'],'base':base,'source_identity':sid,'sourcepath':e['file'],'source_sha256':e['file_sha256'],'selector':e['selector'],'mathml':e['mathml'],'operator_attrs':e['operator_attrs']}
  bybase[base].append(item);byid[sid].append(item)
for s in seed:
 for e in s['source_hats']:
  n=BeautifulSoup(e['mathml'],'html.parser').mover;cs=n.find_all(recursive=False);base=m.Renderer(None).m(cs[0]);item={'command':'hat'if e['operator_attrs'].get('stretchy')=='false'else'widehat','base':base,'source_identity':s['source_identity'],'sourcepath':s['source_file'],'source_sha256':s['source_sha256'],'selector':s['selector'],'mathml':e['mathml'],'operator_attrs':e['operator_attrs']}
  bybase[base].append(item);byid[s['source_identity']].append(item)
result={};uncovered=[]
for base,entry in inventory.items():
 source=bybase[base];options={x['command']for x in source}
 if len(options)==1:result[base]={'command':next(iter(options)),'match_policy':'Exact base across archived and seed-source corpus has one width; source scope retained.','source_occurrences':len(source),'evidence':list({(x['sourcepath'],x['selector'],x['mathml']):json.dumps(x)for x in source}.values())}
 else:
  for entity,attr in entry['fields']:
   sid=identity(metadata[entity]);source=[x for x in byid[sid]if x['base']==base];options={x['command']for x in source}
   if len(options)==1:result[str(entity)+'|'+str(attr)+'|'+base]={'command':next(iter(options)),'match_policy':'Exact base and owning source identity','source_occurrences':len(source),'evidence':source}
   else:uncovered.append({'entity':entity,'attribute_id':attr,'source_identity':sid,'base':base,'width_options':list(options)})
for v in result.values():v['evidence']=[json.loads(x)if isinstance(x,str)else x for x in v['evidence']]
(P/'structured-widths.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(P/'structured-widths-uncovered.json').write_text(json.dumps(uncovered,ensure_ascii=False,indent=2)+'\n')
print('keys',len(result),'uncoveredfields',len(uncovered));print(json.dumps(uncovered,indent=2))
