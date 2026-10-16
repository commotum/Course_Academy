"""Capture one ordered lesson snapshot and prepare canonical, CAS-guarded repairs."""
import hashlib,json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads,dumps,kw
from math_format import normalize_tex,normalize_prose,validate_tex,validate_prose,FORMAT_VERSION
BIN='/home/jake/Developer/EDB/target/release/edb'
ENV={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
def cli(*args):return subprocess.check_output([BIN,*args],env=ENV,text=True,timeout=120)
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
fields={};inventory=[];counts=[]
def walk(x,topic):
    if isinstance(x,list):
        for v in x:walk(v,topic)
    if not isinstance(x,dict):return
    eid=x.get(':db/id')
    for attr in [':tutorial/content',':question/problem',':question/worked-solution',':answer/value',':answer/feedback',':multistep/context']:
        if eid and isinstance(x.get(attr),str):
            kind='math' if attr==':answer/value' and x.get(':answer/type',{}).get(':db/ident')==':answer.type/math' else 'prose'
            key=eid,attr
            if key not in fields:fields[key]={'entity':eid,'attribute':attr,'before':x[attr],'kind':kind,'topics':[]}
            assert fields[key]['before']==x[attr]
            if topic not in fields[key]['topics']:fields[key]['topics'].append(topic)
    for v in x.values():walk(v,topic)
for eid in json.loads((HERE/'requested-order.json').read_text()):
    topic=loads((HERE/f'{eid}.edn').read_text());walk(topic,eid)
    kps=[{'id':k[':db/id'],'title':k.get(':knowledge-point/title'),'generator':k.get(':knowledge-point/question-generator')} for k in topic.get(':topic/knowledge-points',[])]
    inventory.append({'id':eid,'title':topic[':topic/title'],'kps':kps})
    counts.append({'id':eid,'title':topic[':topic/title'],'fields':sum(eid in f['topics'] for f in fields.values())})
changes=[];issues=[]
for f in fields.values():
    norm=normalize_tex if f['kind']=='math' else normalize_prose
    validate=validate_tex if f['kind']=='math' else validate_prose
    try:
        f['after']=validate(norm(f['before']));assert norm(f['after'])==f['after'],'Not idempotent'
        if f['before']!=f['after']:changes.append(f)
    except Exception as e:issues.append({'entity':f['entity'],'attribute':f['attribute'],'error':str(e)})
save('fields.json',list(fields.values()));save('inventory.json',inventory);save('lesson-counts.json',counts)
save('normalization-changes.json',changes);save('normalization-issues.json',issues)
scripts=sorted({str(p.relative_to(ROOT)) for t in inventory for k in t['kps'] for p in (ROOT/'generate/scratch').glob(str(k['id'])+'*.py')})
save('generator-scripts.json',scripts)
assert not issues,issues
(HERE/'all-expected.edn').write_text(dumps([[f['entity'],kw(f['attribute']),f['after']] for f in fields.values()]))
if '--prepare' in sys.argv:
    assert not (HERE/'commit-intent.json').exists(),'Never replace a retained request'
    forms=[[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']] for f in changes]
    transaction=HERE/'transaction.edn';transaction.write_text(dumps(forms));digest=hashlib.sha256(transaction.read_bytes()).hexdigest()
    (HERE/'expected.edn').write_text(dumps([[f[1],f[2],f[4]] for f in forms]))
    (HERE/'read-query.edn').write_text('[:find ?entity ?attr ?value :in $ [[?entity ?attr]] :where [?entity ?attr ?value]]')
    (HERE/'read-inputs.edn').write_text(dumps([[[f[1],f[2]] for f in forms]]))
    save('commit-intent.json',{'database':'math','source':':application/ca-engine','endpoint':'/tmp/edb-math/writer.sock','file':str(transaction),'sha256':digest,'request_key':'linear-algebra-tex-v1-'+digest,'fields':len(forms),'entities':len({f[1] for f in forms})})
print(json.dumps({'fields':len(fields),'changes':len(changes),'scripts':scripts,'issues':issues}))
