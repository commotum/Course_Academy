"""Read full affected records from the saved immutable census basis."""
import concurrent.futures,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from capture.scripts.database.edn import loads,dumps
from capture.scripts.database.client import QUESTION_PULL
HERE=Path(__file__).resolve().parent;E=HERE/'evidence'
status=json.loads((E/'status.json').read_text());basis=status['basis'];client=Publisher.from_environment(source=':agent/codex').client
rows=[]
for p in E.glob('current-*.edn'):rows+=loads(p.read_text())
questions=sorted({e for e,a,v,tx,s,add in rows if a in [1071,1074]});tutorials=sorted({e for e,a,v,tx,s,add in rows if a==1064})
def run(args):
 name,pattern,ids=args
 r=client.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[ids],E/'snapshots',name,basis)
 print(name,len(r),flush=True);return name,[v for [v] in r]
groups=[('questions-'+str(i),QUESTION_PULL,questions[i:i+250]) for i in range(0,len(questions),250)]+[('tutorials','[*]',tutorials),('source','[*]',[17592186576411])]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=dict(pool.map(run,groups))
q=sorted([v for k,vs in results.items() if k.startswith('questions-') for v in vs],key=lambda v:v[':db/id']);t=results['tutorials']
assert len(q)==len(questions) and len(t)==len(tutorials)
for name,values in [('questions',q),('tutorials',t),('source',results['source'])]:
 (E/(name+'.edn')).write_text(dumps(values)+'\n');(E/(name+'.json')).write_text(json.dumps(jsonable(values),ensure_ascii=False,indent=2)+'\n')
assert results['source'][0][':db/ident']==':agent/codex'
a=client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],E,'attributes',basis)
(HERE/'native-pulls.edn').write_text(dumps([['questions',QUESTION_PULL,questions],['tutorials','[*]',tutorials]])+'\n')
print('Complete',len(q),'questions',len(t),'tutorials at',basis)
