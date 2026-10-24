"""Commit the exact user-authorized repair, retain request identity, verify db-after."""
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'));from migrate_learner_history import connection,kw,loads
from preview import check

def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def receipt():
 try:r=loads((HERE/'receipt.edn').read_text())
 except (FileNotFoundError,ValueError,IndexError):return None
 return r if isinstance(r,dict) and r.get(':edb/committed') is True else None

def main():
 assert sys.argv[1:]==['--apply-user-authorized']
 prep=json.loads((HERE/'preparation.json').read_text());preview=json.loads((HERE/'preview-verification.json').read_text());render=json.loads((HERE/'render-verification.json').read_text());generators=json.loads((HERE/'generator-verification.json').read_text());assert not render['failed_questions'] and not render['page_errors'];assert generators['only_expected_presentation_changes'];assert preview['exact_content_diff_verified'] and preview['sha256']==prep['sha256'];assert hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()==prep['sha256']
 # Refuse untested source drift, even though those files are not DB attributes.
 changes={c['path']:c for c in json.loads((HERE/'source-changes.json').read_text())}
 for r in generators['results']:
  c=changes[r['reference']];p=ROOT/c['source']/Path(c['path']).name if c['kind']=='package-successor' else ROOT/c['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['tested_source_sha256']
 fields=json.loads((HERE/'fields.json').read_text());db=connection();intent={'database':'math','source':':agent/codex','endpoint':'/tmp/edb-math/writer.sock','file':str(HERE/'transaction.edn'),'sha256':prep['sha256'],'request_key':'repair-choice-markers-2026-10-23-'+prep['sha256'][:24]}
 if (HERE/'commit-intent.json').exists():assert json.loads((HERE/'commit-intent.json').read_text())==intent
 else:save('commit-intent.json',intent)
 r=receipt()
 if not r:
  save('submission-started.json',{'intent':intent,'at':datetime.now(timezone.utc).isoformat(),'authorization':prep['authorization']})
  command=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000']
  for attempt in range(2):
   if (HERE/'receipt.edn').exists():(HERE/'receipt.edn').replace(HERE/f'receipt-before-retry-{attempt}.edn')
   try:
    with (HERE/'receipt.edn').open('w') as out,(HERE/f'submit-{attempt}.stderr').open('w') as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,timeout=160)
   except subprocess.TimeoutExpired:pass
   r=receipt()
   if r:break
   errors=(HERE/f'submit-{attempt}.stderr').read_text()
   if any(v in errors for v in ('cas-failed','request-key-conflict','type-mismatch','transaction/rejected')):raise RuntimeError(errors)
  assert r,'Unconfirmed outcome; reconcile the original request key and payload before any new write'
 new=check(r);basis=r[':edb/db-after-t']
 text=db.command('query','--as-of',basis,'--file',HERE/'read-query.edn','--inputs',HERE/'read-inputs.edn');(HERE/'after.edn').write_text(text);assert dict(loads(text))=={f['entity']:f['after'] for f in fields}
 q='[:find (pull ?kp [:db/id {:knowledge-point/question-generator [*]}]) (pull ?old [*]) :in $ ?kp ?old :where [?kp :knowledge-point/question-generator _] [?old :question-generator/id _]]'
 regs=db.query(q,[prep['knowledge_point'],prep['old_generator']],HERE,'registration-after',basis);assert len(regs)==1;current=regs[0][0][':knowledge-point/question-generator'];assert current[':db/id']==new and str(current[':question-generator/id'])==prep['new_generator_id'] and current[':question-generator/script']==prep['new_script'];assert regs[0][1][':db/id']==prep['old_generator']
 report={'database':'math','basis_t':basis,'committed':True,'questions_repaired':len(fields),'radio_questions':prep['radio'],'free_response_questions':prep['free'],'new_generator_entity':new,'new_generator_registration_verified':True,'previous_generator_retained':True,'exact_problem_readback_verified':True,'only_question_problems_new_generator_registration_and_transaction_metadata_changed':True,'source':intent['source'],'request_key':intent['request_key'],'sha256':prep['sha256']};save('verification.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
