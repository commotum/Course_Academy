"""Scoped normal cleanup. Durable CAS, immutable prior state, exact recovery."""
import argparse,copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,GeneratorCommitter,StaleBasis,jsonable,digest,dumps,loads,kw,file_lock
from capture.scripts.storage import atomic_json as save
KPS=[17592186092240,17592186092384,17592186092385]
RETIRE={17592186092240:[17592186234077],17592186092384:[17592186092723,17592186092725,17592186234307],17592186092385:[17592186092507,17592186092510,17592186233120,17592186240795,17592186240796,17592186493316,17592186578858,17592186710717,17592186233928,17592186234308]}
FIX=17592186317210
read=lambda p:json.loads(Path(p).read_text())
p=Publisher.from_environment(source=':agent/codex')
LOCK=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
def prepare(kp):
 status=p.client.status();basis=status['basis'];D=H/'cleanup-publication'/str(kp)/str(basis);D.mkdir(parents=True,exist_ok=True)
 before=p.read_kp(kp,D/'before',basis);after=copy.deepcopy(before);forms=[];assertions=[];retractions=[]
 for q in after[':knowledge-point/questions']:
  eid=q[':db/id']
  if eid in RETIRE[kp]:
   old=q.get(':question/retired');assert old is not True,'Already retired without saved outcome: reconcile'
   forms.append([kw('db/cas'),eid,kw('question/retired'),old,True]);assertions.append([eid,kw('question/retired'),True]);q[':question/retired']=True
   if old is not None:retractions.append([eid,kw('question/retired'),old])
  if eid==FIX:
   old=q[':question/worked-solution'];needle=r'm={f}^{′}\left(\frac{1}{4}\right)=\frac{1}{2\sqrt{{x}^{3}}}='
   replacement=r'm={f}^{′}\left(\frac{1}{4}\right)='
   assert old.count(needle)==1,'Unexpected solution: review before changing'
   new=old.replace(needle,replacement);forms.append([kw('db/cas'),eid,kw('question/worked-solution'),old,new]);assertions.append([eid,kw('question/worked-solution'),new]);retractions.append([eid,kw('question/worked-solution'),old]);q[':question/worked-solution']=new
 attrs=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],D,'attributes',basis)
 idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],D,'idents',basis)
 items=p.client.query('[:find (pull ?i [*]) :in $ [?q ...] :where [?i :task-item/content ?q]]',[[q[':db/id'] for q in before[':knowledge-point/questions']]],D,'task-items-before',basis)
 batch=dict(source=':agent/codex',forms=forms,assertions=assertions,retractions=retractions);snapshot=dict(basis=basis,lineage=status['lineage'],attributes=attrs,idents=idents)
 c=GeneratorCommitter(p.config,p.client,D);preview=c.preview(batch,snapshot)
 save(D/'before.json',jsonable(before));save(D/'expected.json',jsonable(after));save(D/'items-before.json',jsonable(items));(D/'batch.edn').write_text(dumps(batch));(D/'snapshot.edn').write_text(dumps(snapshot));save(D/'plan.json',dict(kp=kp,basis=basis,retired_ids=RETIRE[kp],solution_repair=FIX if kp==17592186092384 else None,batch_digest=digest(batch),preview_datoms=len(preview[':edb/tx-data'])));return D

def apply(kp):
 pending=[f.parent for f in (H/'cleanup-publication'/str(kp)).glob('*/request.json')];assert len(pending)<=1
 for attempt in range(5):
  if pending:D=pending.pop();c=GeneratorCommitter(p.config,p.client,D);request=c.pending()
  elif (H/'cleanup-results'/f'{kp}.json').exists():return read(H/'cleanup-results'/f'{kp}.json')
  else:
   D=prepare(kp);c=GeneratorCommitter(p.config,p.client,D);request=c.save_request(loads((D/'batch.edn').read_text()),loads((D/'snapshot.edn').read_text()),read(D/'plan.json')['batch_digest'])
  try:
   with file_lock(Path(p.config.request_directory)/'api.lock'):
    receipt=c.submit(request);proof=c.verify_receipt(request,receipt)
  except StaleBasis:c.retire(request,'rejected_stale_basis',dict(reason='Confirmed basis rejection'));continue
  after=receipt[':edb/db-after-t'];actual=jsonable(p.read_kp(kp,D/'readback',after));assert actual==read(D/'expected.json'),'Exact scoped readback mismatch'
  assert jsonable(p.read_kp(kp,D/'history',request['basis']))==read(D/'before.json'),'Historical snapshot changed'
  ids=[q[':db/id'] for q in actual[':knowledge-point/questions']];items=p.client.query('[:find (pull ?i [*]) :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids],D,'items-readback',after);assert jsonable(items)==read(D/'items-before.json')
  result=dict(passed=True,kp=kp,basis_before=request['basis'],basis_after=after,retired_ids=RETIRE[kp],solution_repair=FIX if kp==17592186092384 else None,exact_siblings_verified=True,historical_snapshot_preserved=True,learner_task_items_unchanged=True,request_key=request['request_key'],**proof)
  save(H/'cleanup-results'/f'{kp}.json',result);c.retire(request,'verified',result);return result
 raise RuntimeError('Repeated basis races')

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--apply',action='store_true');args=a.parse_args()
 for kp in KPS:
  with file_lock(LOCK/f'kp-{kp}.lock'):
   result=apply(kp) if args.apply else dict(directory=str(prepare(kp)));print(json.dumps(result),flush=True)
