"""Resolve answer types/owners and retain fixed-basis question/tutorial data."""
import json,subprocess,threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DB=EDBClient(Config(),threading.Event());BASIS=json.loads((HERE/'identity.json').read_text())['basis']
READ=ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'
QUESTION='''[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]'''
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def run():
    changes=json.loads((HERE/'candidate-changes.json').read_text());answers=sorted({c['entity'] for c in changes if c['attribute'].startswith(':answer/')});types=[];owners=[]
    def read(start):
        ids=answers[start:start+100]
        types=DB.query('[:find (pull ?a [:db/id {:answer/type [:db/id :db/ident]}]) :in $ [?a ...] :where [?a :answer/id _]]',[ids],HERE/'answer-evidence','types-'+str(start),BASIS)
        owners=DB.query('[:find ?a ?q ?f :in $ [?a ...] :where (or-join [?a ?f] [?f :answer-field/choices ?a] [?f :answer-field/correct ?a]) [?q :question/answer-fields ?f]]',[ids],HERE/'answer-evidence','owners-'+str(start),BASIS)
        return types,owners
    if (HERE/'answer-types.json').exists() and (HERE/'answer-owners.json').exists():
        types=json.loads((HERE/'answer-types.json').read_text());owners=json.loads((HERE/'answer-owners.json').read_text())
    else:
        with ThreadPoolExecutor(max_workers=3) as pool:
            for ts,os in pool.map(read,range(0,len(answers),100)):types.extend(ts);owners.extend(os)
    save('answer-types.json',types);save('answer-owners.json',owners)
    qids=sorted({c['entity'] for c in changes if c['attribute'].startswith(':question/')}|{q for a,q,f in owners});tids=sorted({c['entity'] for c in changes if c['attribute']==':tutorial/content'});groups=[]
    for name,pattern,ids in [('questions',QUESTION,qids),('tutorials','[*]',tids)]:
        for start in range(0,len(ids),100):groups.append([name+'-'+str(start),pattern,ids[start:start+100]])
    (HERE/'native-pulls.edn').write_text(dumps(groups)+'\n')
    run=subprocess.run([str(READ),str(HERE),str(BASIS)],env=DB.environment,capture_output=True,text=True,timeout=240);(HERE/'native-read.stderr').write_text(run.stderr);run.check_returncode()
    for name in ('questions','tutorials'):
        entities=[e for group,_,_ in groups if group.startswith(name) for e in loads((HERE/(group+'.edn')).read_text())];save(name+'.json',entities)
    print(json.dumps({'basis':BASIS,'questions':len(qids),'tutorials':len(tids),'answer_types':len(types),'answer_owner_links':len(owners)}))
if __name__=='__main__':run()
