"""Recover verification of the committed batch; never submits a transaction."""
import collections,concurrent.futures,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
fields=json.loads((H/'fields.json').read_text());receipt=loads((H/'receipt.edn').read_text());assert receipt[':edb/committed']is True;basis=receipt[':edb/db-after-t'];db=connection()
def read(offset):
 rows=db.query('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]',[[[f['entity'],kw(f['attribute'])]for f in fields[offset:offset+100]]],H,'after-'+str(offset),basis)
 return {(e,str(a).lstrip(':')):v for e,a,v in rows}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 actual={k:v for rows in pool.map(read,range(0,len(fields),100))for k,v in rows.items()}
assert actual=={(f['entity'],f['attribute']):f['after']for f in fields};names=sorted({f['attribute']for f in fields}|{'db/txInstant'});attrs=db.query('[:find ?a ?id :in $ [?id ...] :where [?a :db/ident ?id]]',[[kw(a)for a in names]],H,'attribute-ids',basis);attrs={str(a).lstrip(':'):e for e,a in attrs};data=receipt[':edb/tx-data'];assert len(data)==len(fields)*2+1 and all(d[4]==17592186576411 for d in data)
expected=collections.Counter((f['entity'],attrs[f['attribute']],f[side],added)for f in fields for side,added in [('before',False),('after',True)]);actual=collections.Counter((d[0],d[1],d[2],d[5])for d in data if d[1]!=attrs['db/txInstant']);assert actual==expected
intent=json.loads((H/'commit-intent.json').read_text());assert intent['sha256']==hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest();result={'committed':True,'basis_t':basis,'fields':len(fields),'datoms':len(data),'sha256':intent['sha256'],'request_key':intent['request_key'],'exact_readback_verified':True,'only_reviewed_content_changed':True,'learner_history_preserved':True,'readback_batch_size':100};(H/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
