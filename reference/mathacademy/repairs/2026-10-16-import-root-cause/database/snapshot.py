"""Read-only global content export, with reproducible queries pinned to one basis.

Run: PYTHONPATH=capture .venv/bin/python <this file>
Existing identity/evidence is resumed at its original basis, never refreshed.
No EDB mutations are used. Raw EDN and normalized JSON preserve exact strings.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import collections, hashlib, json, threading, time
from scripts.config import Config
from scripts.database.client import EDBClient, EDBCommandError
from scripts.database.edn import loads,dumps,Tagged

HERE=Path(__file__).resolve().parent
DB=EDBClient(Config(capture_only=True),threading.Event())
CONTENT=['tutorial/content','question/problem','question/worked-solution','answer/value']
METADATA=['tutorial/id','tutorial/math-academy-id','tutorial/title',
 'question/id','question/math-academy-id','answer/id','answer/type','answer-field/id','answer-field/key','answer-field/type',
 'knowledge-point/id','knowledge-point/title','topic/id','topic/math-academy-id','topic/title',
 'activity/type','activity/title','step/math-academy-id','db/ident']
RELATIONS=['topic/knowledge-points','knowledge-point/questions','knowledge-point/canonical-example',
 'question/answer-fields','answer-field/choices','answer-field/correct',
 'activity/scope','activity/steps','step/content']

def save(name,value):
 (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n')

def run():
 started=time.monotonic();HERE.mkdir(parents=True,exist_ok=True)
 identity_file=HERE/'identity.json'
 if identity_file.exists():
  identity=json.loads(identity_file.read_text());live=DB.status()
  assert identity['database']==live['database'] and identity['lineage']==live['lineage'],'Database lineage changed'
 else:
  identity=DB.status();save('identity.json',identity)
 basis=identity['basis']; evidence=HERE/'evidence'; evidence.mkdir(exist_ok=True)
 def query(name,text,args=[]):
  output=evidence/(name+'.edn')
  if output.exists():
   assert (evidence/(name+'-query.edn')).read_text()==text,'Cached query changed'
   return loads(output.read_text())
  # Global identity/relationship scans exceed the CLI's application-sized
  # default value account even when the projection contains only IDs.
  (evidence/(name+'-query.edn')).write_text(text)
  (evidence/(name+'-inputs.edn')).write_text(dumps(args))
  value=DB.command('query','--file',evidence/(name+'-query.edn'),
   '--inputs',evidence/(name+'-inputs.edn'),'--as-of',basis,
   '--max-value-bytes',268435456,'--max-join-bytes',268435456,
   '--max-results',1000000,'--timeout-ms',60000,timeout=75)
  output.write_text(value)
  return loads(value)
 def ranged(name,attr,columns):
  bounds=query(name+'-bounds','[:find (count ?e) (min ?e) (max ?e) :where [?e :'+attr+' _]]')
  count,lo,hi=bounds[0]
  lo=getattr(lo,'value',lo);hi=getattr(hi,'value',hi)
  if not count:return []
  result=[]
  for start in range(lo,hi+1,10000):
   text='[:find '+columns+' :in $ ?lo ?hi :where [?e :'+attr+' ?v] [(>= ?e ?lo)] [(< ?e ?hi)]]'
   result.extend(query(name+'-range-'+str(start),text,[Tagged('edb/ref',start),Tagged('edb/ref',start+10000)]))
  return result
 def projection(attr):
  name=attr.replace('/','--')
  if attr in CONTENT:
   try: idrows=query(name+'-ids','[:find ?e :where [?e :'+attr+' _]]')
   except EDBCommandError as error:
    if 'edn/capacity' not in (error.stderr or ''):raise
    idrows=ranged(name+'-ids',attr,'?e')
   ids=sorted(row[0] for row in idrows)
   def batch(group):
    try:
     return query(name+'-'+str(group[0])+'-'+str(group[-1]),
       '[:find ?e ?v ?tx ?s :in $ [?e ...] :where [?e :'+attr+' ?v ?tx ?s]]',[group])
    except EDBCommandError as error:
     if 'query/value-byte-limit' not in (error.stderr or '') or len(group)<2:raise
     middle=len(group)//2
     return batch(group[:middle])+batch(group[middle:])
   rows=[row for start in range(0,len(ids),500) for row in batch(ids[start:start+500])]
  else:
   query_text='[:find ?e ?v :where [?e :'+attr+' ?v]]'
   try:rows=query(name,query_text)
   except EDBCommandError as error:
    if 'edn/capacity' not in (error.stderr or ''):raise
    rows=ranged(name,attr,'?e ?v')
  save('rows/'+name+'.json',sorted(rows,key=lambda row:(row[0],str(row[1]))))
  print(json.dumps({'attribute':attr,'rows':len(rows),'basis':basis}),flush=True)
  return attr,rows
 (HERE/'rows').mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=3) as pool:
  results=dict(pool.map(projection,CONTENT+METADATA+RELATIONS))
 metadata=collections.defaultdict(dict)
 for attr in METADATA:
  for entity,value in results[attr]:metadata[entity][':'+attr]=value
 save('entities.json',dict(sorted(metadata.items())))
 save('relations.json',{':'+attr:results[attr] for attr in RELATIONS})
 facts=[]
 for attr in CONTENT:
  for entity,value,tx,source in results[attr]:
   facts.append({'entity':entity,'attribute':':'+attr,'value':value,'transaction':tx,'source':source,
                'sha256':hashlib.sha256(value.encode()).hexdigest()})
 facts.sort(key=lambda r:(r['entity'],r['attribute'],r['transaction'],r['source']))
 with (HERE/'content.jsonl').open('w') as handle:
  for row in facts:handle.write(json.dumps(row,ensure_ascii=False)+'\n')
 summary={**identity,'rows_by_attribute':{':'+attr:len(rows) for attr,rows in results.items()},
  'content_entities_by_attribute':{':'+attr:len({row[0] for row in results[attr]}) for attr in CONTENT},
  'content_facts':len(facts),'content_entities':len({f['entity'] for f in facts}),
  'content_bytes':sum(len(f['value'].encode()) for f in facts),
  'content_sha256':hashlib.sha256((HERE/'content.jsonl').read_bytes()).hexdigest(),
  'scope':'All current entities carrying the four content attributes; no course or source filter.',
  'elapsed_seconds':round(time.monotonic()-started,2),'database_mutations':0}
 save('snapshot-summary.json',summary);print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':run()
