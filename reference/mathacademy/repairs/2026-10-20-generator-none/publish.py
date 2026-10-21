"""Publish immutable package revisions with exact CAS guards and receipt checks."""
import copy,sys,uuid
from read import *
from capture.scripts.database.edn import kw
from scripts.generator_packages import build_manifest,manifest_digest,publish_package,verify_package
SOURCE=':agent/codex'
IDENTS=dict(json.loads((ROOT/'reference/mathacademy/repairs/2026-10-18-equation-chains/idents.json').read_text()));NAMES={v:k for k,v in IDENTS.items()}
PATTERN='[:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/question-generator [*]}]'
SUBMIT=ROOT/'.local/fraction-fence-audit/submit-cas'
def prepare():
 assert not(HERE/'request.json').exists(),'Recover existing request before changing preparation'
 rows=json.loads((HERE/'patched.json').read_text());identity=DB.status();assert identity['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
 current=native(HERE/'preparation',identity['basis'],[('knowledge-points',PATTERN,[r['kp']for r in rows])]);byid={k[':db/id']:k for k in current['knowledge-points']};updates=[]
 for row in rows:
  assert sha(row['updated_script'])==row['updated_sha256']
  kp=byid[row['kp']];old=kp[':knowledge-point/question-generator'];assert old[':db/id']==row['entity']and old[':question-generator/script']==row['reference'],('Concurrent registration change',row['kp'])
  if row['packaged']:
   directory=Path(row['updated_script']).parent;m=row['manifest'];files=list(m['files'])
   if 'source-none-evidence.json'not in files:files.append('source-none-evidence.json')
   manifest=build_manifest(directory,m['entrypoint'],files,dependencies=m['dependencies']);digest=manifest_digest(manifest)
   updates.append({'kp':row['kp'],'old_generator':old,'directory':str(directory),'manifest':manifest,'digest':digest,'reference':f'generators/{digest[:2]}/{digest}/{manifest["entrypoint"]}','generator_uuid':str(uuid.uuid5(uuid.UUID(str(kp[':knowledge-point/id'])),'generator-package:'+digest))})
 save('publication-identity.json',identity);save('package-updates.json',updates);save('registration-before.json',current)
 print(json.dumps({'basis':identity['basis'],'immutable_package_updates':len(updates),'legacy_script_updates':len(rows)-len(updates)}))
def check_report(report,committed,updates,rows):
 assert report[':edb/committed']is committed;expected=set();guards=set()
 for row in rows:
  guards.add((row['kp'],':knowledge-point/question-generator',row['entity'],True));guards.add((row['entity'],':question-generator/script',row['reference'],True))
 for u in updates:
  new=report[':edb/tempids']['generator-'+str(u['kp'])];old=u['old_generator']
  expected.update({(new,':question-generator/id',uuid.UUID(u['generator_uuid']),True),(new,':question-generator/script',u['reference'],True),(u['kp'],':knowledge-point/question-generator',old[':db/id'],False),(u['kp'],':knowledge-point/question-generator',new,True)})
 actual=set();times=0
 for e,a,v,t,source,added in report[':edb/tx-data']:
  assert source==NAMES[SOURCE]
  if IDENTS[a]==':db/txInstant':assert added;times+=1
  else:actual.add((e,IDENTS[a],v,added))
 assert times==1 and expected<=actual and actual-expected<=guards,(actual-expected-guards,expected-actual)
def commit():
 assert json.loads((HERE/'quality-verification.json').read_text())['passed'];assert json.loads((HERE/'ui-verification.json').read_text())['passed']
 rows=json.loads((HERE/'patched.json').read_text());updates=json.loads((HERE/'package-updates.json').read_text());request_path=HERE/'request.json'
 for row in rows:assert sha(row['updated_script'])==row['updated_sha256']and row['policy_sha256']==sha(ROOT/'scripts/generator_policy.py')
 if not request_path.exists():
  assert DB.status()['lineage']==json.loads((HERE/'publication-identity.json').read_text())['lineage'];forms=[];modern={u['kp']for u in updates}
  for u in updates:
   m=u['manifest'];package=publish_package(Path(u['directory']),m['entrypoint'],list(m['files']),Path(DB.config.math_root),dependencies=m['dependencies'],expected_digest=u['digest']);assert package.reference==u['reference'];temp='generator-'+str(u['kp'])
   forms.extend([{kw('db/id'):temp,kw('question-generator/id'):uuid.UUID(u['generator_uuid']),kw('question-generator/script'):u['reference']},[kw('db/cas'),u['kp'],kw('knowledge-point/question-generator'),u['old_generator'][':db/id'],temp]])
  for row in rows:
   if row['kp']not in modern:forms.append([kw('db/cas'),row['kp'],kw('knowledge-point/question-generator'),row['entity'],row['entity']])
   forms.append([kw('db/cas'),row['entity'],kw('question-generator/script'),row['reference'],row['reference']])
  tx=HERE/'transaction.edn';tx.write_text(dumps(forms)+'\n');preview=DB.command('with','--file',tx,'--source',SOURCE);(HERE/'preview.edn').write_text(preview);check_report(loads(preview),False,updates,rows)
  save('request.json',{'database':'math','source':SOURCE,'lineage':DB.status()['lineage'],'endpoint':str(DB.config.endpoint),'transaction_file':str(tx),'sha256':sha(tx),'quality_sha256':sha(HERE/'quality-verification.json'),'updates_sha256':sha(HERE/'package-updates.json'),'request_key':'generator-visible-none-v1-'+sha(tx),'concurrency_guards':'Exact CAS for all 26 KP registrations and old generator script references'})
 request=json.loads(request_path.read_text());assert sha(request['transaction_file'])==request['sha256']and sha(HERE/'quality-verification.json')==request['quality_sha256']and sha(HERE/'package-updates.json')==request['updates_sha256'];receipt=HERE/'receipt.edn'
 if not receipt.exists():
  p=subprocess.run([str(SUBMIT),'transact','--database','math','--file',request['transaction_file'],'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--source',SOURCE,'--timeout-ms','180000'],env=DB.environment,capture_output=True,text=True,timeout=210);(HERE/'submission.stderr').write_text(p.stderr);p.check_returncode();receipt.write_text(p.stdout)
 report=loads(receipt.read_text());assert report[':edb/committed'];save('commit-confirmation.json',{'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'request_key':request['request_key'],'sha256':request['sha256']});check_report(report,True,updates,rows)
 before=native(HERE/'committed-before',report[':edb/db-before-t'],[('knowledge-points',PATTERN,[r['kp']for r in rows])]);after=native(HERE/'committed-after',report[':edb/db-after-t'],[('knowledge-points',PATTERN,[r['kp']for r in rows])]);umap={u['kp']:u for u in updates};bmap={q[':db/id']:q for q in before['knowledge-points']}
 for kp in after['knowledge-points']:
  old=bmap[kp[':db/id']];expected=copy.deepcopy(old)
  if kp[':db/id']in umap:
   u=umap[kp[':db/id']];expected[':knowledge-point/question-generator']={':db/id':report[':edb/tempids']['generator-'+str(u['kp'])],':question-generator/id':uuid.UUID(u['generator_uuid']),':question-generator/script':u['reference']};verify_package(Path(DB.config.math_root)/Path(u['reference']).parent,u['digest'])
  assert expected==kp,('Unexpected readback',kp[':db/id'])
 for row in rows:
  assert sha(row['updated_script'])==row['updated_sha256']
  if row['packaged']:assert sha(row['script'])==row['before_sha256'],'Old immutable package changed'
 save('verification.json',{'passed':True,'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'affected_generators':len(rows),'immutable_package_revisions':len(updates),'repository_script_revisions':len(rows)-len(updates),'exact_cas_guards_and_datom_scope_verified':True,'all_26_active_registrations_verified':True,'old_immutable_packages_unchanged':True,'stored_questions_and_learner_records_unchanged':True,'quality':json.loads((HERE/'quality-verification.json').read_text()),'ui':json.loads((HERE/'ui-verification.json').read_text())});print((HERE/'verification.json').read_text())
if __name__=='__main__':{'prepare':prepare,'commit':commit}[sys.argv[1]]()
