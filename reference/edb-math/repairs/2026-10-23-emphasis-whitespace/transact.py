"""Preview and commit the exact user-authorized content-only EDB CAS repair."""
import collections,hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,dumps,loads,kw
ALLOWED={'tutorial/content','question/problem','question/worked-solution'}
def save(n,v):(H/n).write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(db,basis,name):
 rows=db.query('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]',[[[f['entity'],kw(f['attribute'])] for f in F]],H,name,basis)
 return {(e,str(a)[1:]):v for e,a,v in rows}
def check(report,committed):
 assert report[':edb/committed'] is committed
 ds=report[':edb/tx-data'];ids={f['entity'] for f in F}
 wanted=collections.Counter([(f['entity'],f['before'],False) for f in F]+[(f['entity'],f['after'],True) for f in F])
 assert collections.Counter((d[0],d[2],d[-1]) for d in ds if d[0] in ids)==wanted
 assert len(ds)==2*len(F)+1 and all(d[-2]==17592186576411 for d in ds)
def main():
 global F
 F=json.loads((H/'fields.json').read_text());assert all(f['attribute'] in ALLOWED for f in F)
 forms=[[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']] for f in F]
 if sys.argv[1:]==['--prepare']:
  (H/'transaction.edn').write_text(dumps(forms)+'\n');save('preparation.json',{'database':'math','basis_t':6225,'fields':len(F),'entities':len({f['entity'] for f in F}),'emphasis_spans':sum(len(f['edits']) for f in F),'attributes':dict(collections.Counter(f['attribute'] for f in F)),'transaction_sha256':sha(H/'transaction.edn'),'source':':agent/codex'});print('Prepared',len(forms),'CAS forms.');return
 assert sys.argv[1:] in (['--preview'],['--apply-user-authorized'])
 assert loads((H/'transaction.edn').read_text())==forms
 digest=sha(H/'transaction.edn');render=json.loads((H/'render-verification.json').read_text());assert render['passed'] and render['fields']==len(F)
 rendered={(r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']) for r in json.loads((H/'render-checks.json').read_text())}
 assert rendered=={(f['entity'],f['attribute'],f['before_sha256'],f['after_sha256']) for f in F}
 db=connection()
 if sys.argv[1:]==['--preview']:
  basis=db.basis();assert read(db,basis,'preflight')=={(f['entity'],f['attribute']):f['before'] for f in F}
  text=db.command('with','--source',':agent/codex','--file',H/'transaction.edn');(H/'preview.edn').write_text(text);report=loads(text);check(report,False)
  save('preview-verification.json',{'sha256':digest,'basis_t':basis,'committed':False,'fields':len(F),'exact_content_only_diff_verified':True});print('Preview passed: exactly',len(F),'content replacements.');return
 preview=json.loads((H/'preview-verification.json').read_text());assert preview['sha256']==digest and preview['exact_content_only_diff_verified']
 intent={'database':'math','source':':agent/codex','endpoint':'/tmp/edb-math/writer.sock','file':str(H/'transaction.edn'),'sha256':digest,'request_key':'repair-emphasis-whitespace-2026-10-23-'+digest[:24]}
 if (H/'commit-intent.json').exists():assert json.loads((H/'commit-intent.json').read_text())==intent
 else:save('commit-intent.json',intent)
 receipt=None
 if (H/'receipt.edn').exists():
  try:receipt=loads((H/'receipt.edn').read_text())
  except (ValueError,IndexError):pass
 if not isinstance(receipt,dict) or receipt.get(':edb/committed') is not True:
  command=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000']
  with (H/'receipt.edn').open('w') as out,(H/'submit.stderr').open('w') as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,timeout=160,check=True)
  receipt=loads((H/'receipt.edn').read_text())
 check(receipt,True);basis=receipt[':edb/db-after-t'];assert read(db,basis,'after')=={(f['entity'],f['attribute']):f['after'] for f in F}
 report={'database':'math','committed':True,'basis_t':basis,'fields':len(F),'entities':len({f['entity'] for f in F}),'emphasis_spans':sum(len(f['edits']) for f in F),'request_key':intent['request_key'],'sha256':digest,'exact_content_only_diff_verified':True,'exact_readback_verified':True,'math_answer_values_entity_ids_links_and_learner_history_preserved':True};save('verification.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
