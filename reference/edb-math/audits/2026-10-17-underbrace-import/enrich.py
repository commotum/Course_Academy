"""Join brace-affected fields to their stable identities and lesson placements."""
import concurrent.futures,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from collect import query,E,HERE,jsonable,loads
TP='[:db/id :topic/math-academy-id :topic/title]'
KP='[:db/id :knowledge-point/title {:topic/_knowledge-points '+TP+'}]'
ACT='[:db/id :activity/title :activity/type {:activity/scope '+TP+'}]'
STEP='[:db/id {:activity/_steps '+ACT+'}]'
Q='[:db/id :question/id :question/math-academy-id {:knowledge-point/_questions '+KP+'} {:knowledge-point/_canonical-example '+KP+'} {:step/_content '+STEP+'}]'
F='[:db/id :answer-field/type {:question/_answer-fields '+Q+'}]'
P='[:db/id :question/id :question/math-academy-id :tutorial/id :tutorial/math-academy-id :tutorial/title :answer/id {:knowledge-point/_questions '+KP+'} {:knowledge-point/_canonical-example '+KP+'} {:step/_content '+STEP+'} {:answer-field/_choices '+F+'} {:answer-field/_correct '+F+'}]'
if __name__=='__main__':
 rows=[]
 for p in (E/'current').glob('*.edn'):
  if p.name.endswith(('-inputs.edn','-query.edn')) or p.stem[-1:].isdigit():continue
  rows.extend(loads(p.read_text()))
 ids=sorted({r[0] for r in rows})
 def batch(i):
  name='metadata/'+str(i)
  file=(E/name).with_suffix('.edn')
  r=loads(file.read_text()) if file.exists() else query('[:find (pull ?e '+P+') :in $ [?e ...] :where [?e _ _]]',[ids[i:i+400]],name)
  print(i,len(r),flush=True);return [v for [v] in r]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:items=sum(p.map(batch,range(0,len(ids),400)),[])
 (E/'metadata.json').write_text(json.dumps(jsonable(items),ensure_ascii=False,indent=2)+'\n')
 print('entities',len(items),flush=True)
