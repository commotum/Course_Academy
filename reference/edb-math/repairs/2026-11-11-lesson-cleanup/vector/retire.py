"""CAS-retire exactly reviewed question IDs; no entity deletion or component edits."""
import argparse,copy,json,sys
from contextlib import ExitStack
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_publish import Publisher,GeneratorCommitter,jsonable,digest
from capture.scripts.database.edn import kw,dumps
from capture.scripts.database.client import StaleBasis
from capture.scripts.storage import atomic_json,file_lock,read_json

def read(p):return json.loads(Path(p).read_text())
def save(p,v):atomic_json(Path(p),jsonable(v))
def prepare(p,out,ledger):
 status=p.client.status();basis=status['basis'];before={};forms=[];assertions=[];retractions=[]
 for kp in sorted({r['kp'] for r in ledger['questions']}):
  current=jsonable(p.read_kp(kp,out/'before'/str(kp),basis));before[str(kp)]=current
  baseline=read(H/str(kp)/'capture/kp.json');assert current==baseline,'Pool/source/registration changed: refresh evidence before retiring'
 for row in ledger['questions']:
  q=next(q for q in before[str(row['kp'])][':knowledge-point/questions'] if q[':db/id']==row['question']);old=q.get(':question/retired');assert old is not True
  forms.append([kw('db/cas'),q[':db/id'],kw('question/retired'),old,True]);assertions.append([q[':db/id'],kw('question/retired'),True])
  if old is not None:retractions.append([q[':db/id'],kw('question/retired'),old])
 attrs=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],out,'attributes',basis)
 idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],out,'idents',basis)
 snapshot=dict(basis=basis,lineage=status['lineage'],attributes=attrs,idents=idents)
 batch=dict(source=':agent/codex',forms=forms,assertions=assertions,retractions=retractions)
 prepared=dict(basis=basis,before=before,ledger_sha256=digest(ledger),batch_edn=dumps(batch),snapshot_edn=dumps(snapshot))
 save(out/'preparation.json',prepared);return prepared,batch,snapshot

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--apply',action='store_true');args=ap.parse_args();assert args.preview!=args.apply
 ledger=read(H/'retirement-ledger.json');p=Publisher.from_environment(source=':agent/codex');out=H/'retirement';out.mkdir(exist_ok=True)
 if args.apply:
  review=read(H/'review/retirement.json');assert review['verdict']=='accepted';assert review['ledger_sha256']==digest(ledger)
 with ExitStack() as locks:
  for kp in sorted({r['kp'] for r in ledger['questions']}):locks.enter_context(file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock',blocking=False))
  locks.enter_context(file_lock(H.parent/'publication.lock'))
  verified=read_json(out/'verification.json')
  if verified and verified.get('passed'):print(json.dumps(verified));return
  committer=GeneratorCommitter(p.config,p.client,out);request=committer.pending()
  if args.preview:
   assert request is None,'Recover saved pending intent before fresh planning'
   prepared,batch,snapshot=prepare(p,out,ledger);committer.preview(batch,snapshot);save(out/'preview-verification.json',dict(passed=True,basis=prepared['basis'],ledger_sha256=digest(ledger),forms=batch['forms'],script_sha256=__import__('hashlib').sha256(Path(__file__).read_bytes()).hexdigest()));print('Preview passed');return
  for attempt in range(3):
   request=committer.pending()
   if request is None:
    prepared,batch,snapshot=prepare(p,out,ledger)
    try:committer.preview(batch,snapshot)
    except StaleBasis:continue
    request=committer.save_request(batch,snapshot,digest(ledger))
   assert request['content_sha256']==digest(ledger),'Pending request differs: recover exact original intent'
   with file_lock(p.config.request_directory/'api.lock'):
    try:receipt=committer.submit(request)
    except StaleBasis:
     committer.retire(request,'rejected_stale_basis',dict(reason='Confirmed writer rejection'));continue
    evidence=committer.verify_receipt(request,receipt)
   prepared=read(out/'preparation.json');basis=receipt[':edb/db-after-t']
   for kp,old in prepared['before'].items():
    current=jsonable(p.read_kp(int(kp),out/'readback'/kp,basis));expected=copy.deepcopy(old)
    for q in expected[':knowledge-point/questions']:
     if any(q[':db/id']==r['question'] for r in ledger['questions']):q[':question/retired']=True
    assert current==expected,'Unexpected record/field/history-affecting mutation'
    historical=jsonable(p.read_kp(int(kp),out/'historical'/kp,request['basis']));assert historical==old
   result=dict(passed=True,basis_before=request['basis'],basis_after=basis,retired=[r['question'] for r in ledger['questions']],only_retired_attribute_changed=True,all_ids_components_and_pool_links_retained=True,historical_readback_verified=True,**evidence)
   save(out/'verification.json',result);committer.retire(request,'verified',result);print(json.dumps(result));return
  raise RuntimeError('Three confirmed basis conflicts; no unconfirmed new intent')
if __name__=='__main__':main()
