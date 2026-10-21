"""Read the current repair dependencies at one database basis."""
import json,threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];AUDIT=ROOT/'reference/mathacademy/audits/2026-10-18-equation-chain-import'
DB=EDBClient(Config(),threading.Event())
QUESTION='''[:db/id :question/id :question/math-academy-id :question/problem :question/worked-solution {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]'''
TUTORIAL='[*]'
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def run():
 assert not (HERE/'identity.json').exists(),'Keep the original preparation snapshot'
 identity=DB.status();save('identity.json',identity);basis=identity['basis'];findings=json.loads((AUDIT/'findings.json').read_text());qids=sorted({f['entity'] for f in findings if f['attribute'].startswith(':question/')});tids=sorted({f['entity'] for f in findings if f['attribute']==':tutorial/content'});groups=[]
 for name,ids,attr,pattern in [('questions',qids,'question/id',QUESTION),('tutorials',tids,'tutorial/id',TUTORIAL)]:
  for start in range(0,len(ids),100):groups.append((name,start,ids[start:start+100],attr,pattern))
 def read(group):
  name,start,ids,attr,pattern=group
  rows=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e :'+attr+' _]]',[ids],HERE/'evidence',name+'-'+str(start),basis)
  return name,rows
 result={'questions':[],'tutorials':[]}
 with ThreadPoolExecutor(max_workers=3) as pool:
  for name,rows in pool.map(read,groups):result[name].extend(rows)
 for name,rows in result.items():save(name+'.json',rows)
 current={e[':db/id']:e for group in result.values() for [e] in group};changed=[]
 for f in findings:
  value=current.get(f['entity'],{}).get(f['attribute'])
  if value!=f['value']:changed.append({'entity':f['entity'],'attribute':f['attribute'],'audited':f['value'],'current':value})
 save('changed-since-audit.json',changed)
 schema=DB.query('[:find ?e ?i :where [?e :db/ident ?i]]',[],HERE/'evidence','idents',basis);save('idents.json',schema)
 print(json.dumps({'identity':identity,'questions':len(result['questions']),'tutorials':len(result['tutorials']),'changed_fields':len(changed)}))
if __name__=='__main__':run()
