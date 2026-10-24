"""Preview each exact prepared CAS payload; never writes the database."""
import collections,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'));from migrate_learner_history import connection,loads

def main():
 db=connection();batches=json.loads((HERE/'batches.json').read_text());allfields={(f['entity'],f['attribute']):f for f in json.loads((HERE/'fields.json').read_text())};reports=[]
 for b in batches:
  folder=HERE/b['name'];payload=folder/'transaction.edn';assert hashlib.sha256(payload.read_bytes()).hexdigest()==b['sha256'];stamp=folder/'preview-check.json';r=None
  if stamp.exists():
   old=json.loads(stamp.read_text())
   if old['sha256']==b['sha256']:r=old
  if r is None:
   text=db.command('with','--source',':agent/codex','--file',payload);(folder/'preview.edn').write_text(text);p=loads(text);assert p[':edb/committed'] is False and p[':edb/speculative'] is True
   fields=[allfields[tuple(k)] for k in b['field_keys']];expected=collections.Counter([(f['entity'],f['before'],False) for f in fields]+[(f['entity'],f['after'],True) for f in fields]);ids={f['entity'] for f in fields};actual=collections.Counter((d[0],d[2],d[-1]) for d in p[':edb/tx-data'] if d[0] in ids);assert actual==expected;assert len(p[':edb/tx-data'])==2*len(fields)+1
   r={'sha256':b['sha256'],'fields':len(fields),'db_before_t':p[':edb/db-before-t'],'speculative':True,'committed':False,'exact_content_diff_verified':True};stamp.write_text(json.dumps(r,indent=2)+'\n')
  reports.append({'batch':b['name'],**r});print('Previewed',b['name'],b['fields'],'fields',flush=True)
 (HERE/'preview-verification.json').write_text(json.dumps(reports,indent=2)+'\n')
if __name__=='__main__':main()
