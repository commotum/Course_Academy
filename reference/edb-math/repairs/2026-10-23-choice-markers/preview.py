"""Preview the exact guarded repair and check all proposed content datoms."""
import collections,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'));from migrate_learner_history import connection,loads

def check(report):
 fields=json.loads((HERE/'fields.json').read_text());prep=json.loads((HERE/'preparation.json').read_text());ids={f['entity'] for f in fields};datoms=report[':edb/tx-data'];new=report[':edb/tempids']['generator-successor']
 expected=collections.Counter([(f['entity'],f['before'],False) for f in fields]+[(f['entity'],f['after'],True) for f in fields]);assert collections.Counter((d[0],d[2],d[-1]) for d in datoms if d[0] in ids)==expected
 assert collections.Counter((d[0],d[2],d[-1]) for d in datoms if d[0]==prep['knowledge_point'])==collections.Counter([(prep['knowledge_point'],prep['old_generator'],False),(prep['knowledge_point'],new,True)])
 assert {(str(d[2]),d[-1]) for d in datoms if d[0]==new}=={(prep['new_script'],True),(prep['new_generator_id'],True)}
 assert len(datoms)==2*len(fields)+5
 assert all(d[-2]==17592186576411 for d in datoms),'Unexpected source'
 return new

def main():
 prep=json.loads((HERE/'preparation.json').read_text());assert hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()==prep['sha256'];text=connection().command('with','--source',':agent/codex','--file',HERE/'transaction.edn');(HERE/'preview.edn').write_text(text);p=loads(text);assert p[':edb/committed'] is False and p[':edb/speculative'] is True;check(p)
 report={'sha256':prep['sha256'],'db_before_t':p[':edb/db-before-t'],'questions':prep['questions'],'new_generator_registration':True,'exact_content_diff_verified':True,'speculative':True,'committed':False};(HERE/'preview-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
