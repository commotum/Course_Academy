"""Trace actual imported tutorial/example values through retained EDB history."""
import json,threading
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
 db=EDBClient(Config(),threading.Event());ids=[17592186065338,17592186065339,17592186063922,17592186063924]
 rows=[]
 for attr in ('tutorial/content','question/worked-solution'):
  text='[:find ?e ?value ?tx ?source ?added :in $ [?e ...] :where [?e :'+attr+' ?value ?tx ?source ?added]]'
  q=HERE/('evidence/history-'+attr.replace('/','-')+'-query.edn');a=HERE/('evidence/history-'+attr.replace('/','-')+'-inputs.edn');q.write_text(text);a.write_text(dumps([ids]))
  result=db.command('query','--file',q,'--inputs',a,'--history','--as-of',json.loads((HERE/'identity.json').read_text())['basis'],'--max-value-bytes','67108864');q.with_name(q.name.replace('-query.edn','.edn')).write_text(result)
  rows.extend([e,attr,value,tx,source,added] for e,value,tx,source,added in loads(result))
 idents={eid:str(i) for eid,i in loads((HERE/'evidence/idents.edn').read_text())};out=[]
 for e,attr,val,tx,source,added in sorted(rows,key=lambda r:(r[0],r[3],r[5])):
  item={'entity':e,'attribute':str(attr),'value':val,'tx':tx,'source':idents.get(source,source),'added':added};out.append(item)
  print(e,tx,item['source'],added,repr(val[:190]))
 (HERE/'history.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
