"""Apply one freshly captured, previewed, basis-guarded lesson migration."""
from contextlib import ExitStack
from pathlib import Path
import copy,json,shutil,sys,subprocess
from migration import H,ROOT,Publisher,MigrationCommitter,prepare,loads,dumps,kw,atomic_json,atomic_text,digest,jsonable,StaleBasis,Q_PATTERN,RETAIN
from verify import verify,question_content
from scripts.generator_publish import file_lock

def readback(p,prepared,receipt,d):
 basis=receipt[':edb/db-after-t'];rows=[]
 for start in range(0,len(prepared['all_question_ids']),20):rows+=p.client.query('[:find (pull ?q '+Q_PATTERN+') :in $ [?q ...] :where [?q :question/id _]]',[prepared['all_question_ids'][start:start+20]],d,f'after-{start}',basis)
 atomic_text(d/'committed-questions.edn',dumps([q for [q] in rows]))
 ret=p.client.query('[:find (pull ?e '+RETAIN+') :in $ [?e ...] :where (or-join [?e] [?e :answer-field/id _] [?e :answer/id _])]',[prepared['retained_ids']],d,'retained-after',basis);atomic_text(d/'committed-retained.edn',dumps([q for [q] in ret]))
 result=verify(d,d/'committed-questions.edn',d/'committed-retained.edn',d/'receipt.edn',stage='committed')
 ids=[r['question'] for r in prepared['plans']];historical=p.client.query('[:find (pull ?q '+Q_PATTERN+') :in $ [?q ...] :where [?q :question/id _]]',[ids],d,'historical-before',prepared['basis']);old={q[':db/id']:q for q in loads(prepared['before_edn'])}
 assert all(jsonable(q)==jsonable(old[q[':db/id']]) for [q] in historical)
 result.update(committed=True,basis_before=prepared['basis'],basis_after=basis,historical_read_verified=True)
 atomic_json(H/'verification.json',result);return result

def run():
 engine=json.loads((H/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0 and engine['whole_question_canonical_accepted']==10
 for folder in ('render','render-narrow'):assert json.loads((H/folder/'rendering.json').read_text())['passed']
 review=json.loads((H/'review/preparation.json').read_text());assert json.loads((H/'review/speculative-verification.json').read_text())['passed']
 signature=digest([question_content(c['question']) for c in review['proposed']])
 p=Publisher.from_environment(source=':agent/codex');p.config.preview_bin=Path(json.loads((H/'native-build.json').read_text())['preview_executable']);d=H/'publication'
 with ExitStack() as stack:
  stack.enter_context(file_lock(Path(p.config.request_directory)/'api.lock'))
  for kp in (17592186064162,17592186064273):stack.enter_context(file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'))
  committer=MigrationCommitter(p.config,p.client,d);pending=committer.pending()
  if pending:
   prepared=json.loads((d/'preparation.json').read_text());request=pending
  elif (H/'verification.json').exists():print('Already committed and verified; no new request');return
  else:
   for attempt in range(4):
    request=None
    try:
     prepared=prepare(p,d);assert digest([question_content(c['question']) for c in prepared['proposed']])==signature,'Reviewed content changed; re-review required'
     report=committer.preview(loads(prepared['batch_edn']),loads(prepared['snapshot_edn']))
     verify(d,d/'preview-questions.edn',d/'preview-retained.edn',d/'preview.edn',stage='speculative')
     request=committer.save_request(loads(prepared['batch_edn']),loads(prepared['snapshot_edn']),digest(prepared));receipt=committer.submit(request);break
    except StaleBasis:
     if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; refresh uncommitted work'})
     archive=H/'superseded'/f'basis-{prepared["basis"]}-attempt-{attempt}'
     if d.exists():shutil.copytree(d,archive)
   else:raise RuntimeError('Repeated confirmed basis changes; no uncertain request rebuilt')
  if pending:receipt=committer.submit(request)
  atomic_json(H/'commit-receipt.json',{'committed':True,'basis_before':receipt[':edb/db-before-t'],'basis_after':receipt[':edb/db-after-t'],'request_key':request['request_key'],'source':':agent/codex','transaction_sha256':request['transaction_sha256']})
  committer.verify_receipt(request,receipt);result=readback(p,prepared,receipt,d);committer.retire(request,'verified',result)
  ledger=json.loads((H/'case-ledger.json').read_text())
  for row in ledger:
   if row['decision'] in ('convert','remove_redundant_none'):row.update(commit_status='committed',commit_basis=result['basis_after'],request_key=request['request_key'])
   else:row['commit_status']='retained_unchanged'
  atomic_json(H/'case-ledger.json',ledger);atomic_json(H/'status.json',{'state':'committed_verified','topic':17592186048123,'questions_audited':29,'kps':2,'converted_question_ids':[r['question_eid'] for r in ledger if r['decision']=='convert'],'none_cleanup_ids':[r['question_eid'] for r in ledger if r['decision']=='remove_redundant_none'],'retained_radio_ids':[r['question_eid'] for r in ledger if r['decision']=='retain_radio'],'basis_before':result['basis_before'],'basis_after':result['basis_after'],'pending_request':None,'source':':agent/codex','generator_follow_up':'Neither KP has a registered generator. Refresh future source snapshots from the converted database.'})
  print(json.dumps(result))

if __name__=='__main__':run()
