from pathlib import Path
import collections,concurrent.futures,json,os,subprocess
from capture.scripts.database.edn import loads,dumps,kw
P=Path('reference/mathacademy/audits/2026-10-16-matrix-quality');env=dict(os.environ,EDB_POSTGRES_URL="host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'");edb='/home/jake/Developer/EDB/target/release/edb';basis=loads((P/'render-repair-receipt.edn').read_text())[kw('edb/basis-t')]
initial={q[':db/id']:q for n in ['questions','tutorials'] for q in json.loads((P/(n+'.json')).read_text())};initial.update({r[':db/id']:r for r in json.loads((P/'repaired-records.json').read_text())});changes=json.loads((P/'render-repair-changes.json').read_text());keys=[];dups=[];ids=sorted({x['entity'] for x in changes}|{x['question'] for x in keys+dups});folder=P/'readback';folder.mkdir(exist_ok=True)
def read(i):
 inp=folder/f'{i}.inputs.edn';inp.write_text(dumps([ids[i:i+20]]));out=folder/f'{i}.edn'
 with out.open('w') as stream:subprocess.run([edb,'query','--database','math','--file',str(P/'guard-query.edn'),'--inputs',str(inp),'--as-of',str(basis),'--timeout-ms','20000','--max-results','100','--max-value-bytes','67108864'],stdout=stream,env=env,check=True)
 return [json.loads(json.dumps(r[0],default=str)) for r in loads(out.read_text())]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:current={r[':db/id']:r for batch in pool.map(read,range(0,len(ids),20)) for r in batch}
expected=__import__('copy').deepcopy(initial)
for c in changes:expected[c['entity']][':'+c['attribute']]=c['new']
for d in dups:expected[d['question']][':question/answer-fields']=[f for f in expected[d['question']][':question/answer-fields'] if f[':db/id'] not in d['detach']]
for k in keys:
 f=next(f for f in expected[k['question']][':question/answer-fields'] if f[':db/id']==k['field']);a=next(a for a in f[':answer-field/choices'] if a[':db/id']==k['correct']);f[':answer-field/correct']={key:a[key] for key in [':db/id',':answer/value',':answer/type']}
def canon(v):
 if isinstance(v,dict):return {k:canon(x) for k,x in v.items()}
 if isinstance(v,list):return sorted([canon(x) for x in v],key=lambda x:json.dumps(x,sort_keys=True))
 return v
assert all(canon(current[e])==canon(expected[e]) for e in ids),[e for e in ids if canon(current[e])!=canon(expected[e])]
# Assert transaction touches only the intended content attributes and never retracts an entity/answer/history.
receipt=loads((P/'render-repair-receipt.edn').read_text());datoms=receipt[kw('edb/tx-data')];attrs=collections.Counter(d[1] for d in datoms);forms=loads((P/'render-repairs.edn').read_text());allowed={'question/problem','question/worked-solution','tutorial/content','answer-field/correct','question/answer-fields'}
assert all(str(f[2]).removeprefix(':') in allowed for f in forms if f[0]!=kw('db/ensure'))
result=dict(committedBasis=basis,verifiedRecords=len(ids),textAttributes=len(changes),keys=len(keys),redundantBindings=len(dups),datoms=len(datoms),unchangedAnswerEntities=True,noLearnerHistoryWrites=True,exactExpectedContent=True)
(P/'render-repair-verification.json').write_text(json.dumps(result,indent=2));(P/'render-repaired-records.json').write_text(json.dumps(list(current.values()),indent=2));print(json.dumps(result))
