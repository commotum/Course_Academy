"""Preview and commit an exact reviewed CAS batch, retaining its request identity."""
import collections,hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads

def save(p,v):p.write_text(json.dumps(v,default=str,indent=2)+'\n')
def main(folder):
 fields=json.loads((folder/'fields.json').read_text());payload=folder/'transaction.edn';sha=hashlib.sha256(payload.read_bytes()).hexdigest();render=json.loads((folder/'render-verification.json').read_text());assert render['passed']and render['fields']==len(fields);assert [(r['entity'],r['attribute'],r['before_sha256'],r['after_sha256'])for r in render['checks']]==[(r['entity'],r['attribute'],r['before_sha256'],r['after_sha256'])for r in fields]
 forms=loads(payload.read_text());cas=[f for f in forms if str(f[0])==':db/cas'];assert len(cas)==len(fields);assert all(f[1:]==[r['entity'],kw(r['attribute']),r['before'],r['after']]for f,r in zip(cas,fields));db=connection();intent_path=folder/'commit-intent.json'
 if not intent_path.exists():
  subprocess.run([str(R/'.local/edb/percent-escaping/preview'),str(payload),str(folder/'fields.json'),str(folder/'native-preview.json')],env=db.env,check=True,capture_output=True,text=True)
  intent={'database':'math','source':':agent/codex','sha256':sha,'request_key':'mixed-title-repair-2026-10-26-'+folder.name+'-'+sha[:24],'file':str(payload.resolve()),'endpoint':'/tmp/edb-math/writer.sock'};save(intent_path,intent)
 else:intent=json.loads(intent_path.read_text());assert intent['sha256']==sha
 receipt=folder/'receipt.edn';r=None
 if receipt.exists():
  try:r=loads(receipt.read_text())
  except (IndexError,ValueError):pass
 if not isinstance(r,dict)or r.get(':edb/committed')is not True:
  cmd=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000']
  with receipt.open('w')as out,(folder/'submit.stderr').open('w')as err:subprocess.run(cmd,env=db.env,stdout=out,stderr=err,check=True,timeout=160)
  r=loads(receipt.read_text())
 assert r[':edb/committed']is True;basis=r[':edb/db-after-t'];values=db.query('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]',[[[f['entity'],kw(f['attribute'])]for f in fields]],folder,'after',basis);assert {(e,str(a).lstrip(':')):v for e,a,v in values}=={(f['entity'],f['attribute']):f['after']for f in fields}
 attrs=db.query('[:find ?a ?id :in $ [?id ...] :where [?a :db/ident ?id]]',[[kw(f['attribute'])for f in fields]+[kw('db/txInstant')]],folder,'attribute-ids',basis);attr={str(k).lstrip(':'):e for e,k in attrs};data=r[':edb/tx-data'];assert len(data)==len(fields)*2+1 and all(d[4]==17592186576411 for d in data);expected=collections.Counter((f['entity'],attr[f['attribute']],f[side],added)for f in fields for side,added in [('before',False),('after',True)]);actual=collections.Counter((d[0],d[1],d[2],d[5])for d in data if d[1]!=attr['db/txInstant']);assert actual==expected
 result={'committed':True,'basis_t':basis,'fields':len(fields),'sha256':sha,'request_key':intent['request_key'],'exact_readback_verified':True,'only_reviewed_content_changed':True,'learner_history_preserved':True};save(folder/'verification.json',result);print(json.dumps(result))
if __name__=='__main__':main(Path(sys.argv[1]))
