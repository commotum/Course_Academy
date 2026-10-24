"""Assemble exact problem CAS and versioned package registration forms."""
import hashlib,json,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import dumps,loads,kw

def main():
 fields=json.loads((HERE/'fields.json').read_text());package=json.loads((HERE/'package-publication.json').read_text());reg=package['registration'];forms=loads((HERE/'questions-transaction.edn').read_text())
 forms += [{kw('db/id'):'generator-successor',kw('question-generator/id'):uuid.UUID(package['new_generator_id']),kw('question-generator/script'):package['new_reference']},[kw('db/cas'),reg['kp'],kw('knowledge-point/question-generator'),reg['generator'],'generator-successor']]
 payload=dumps(forms)+'\n';(HERE/'transaction.edn').write_text(payload)
 manifest={'database':'math','source':':agent/codex','preparation_basis':6099,'questions':len(fields),'radio':sum(f['type']=='radio' for f in fields),'free':sum(f['type']=='free' for f in fields),'new_generator_id':package['new_generator_id'],'knowledge_point':reg['kp'],'old_generator':reg['generator'],'new_script':package['new_reference'],'sha256':hashlib.sha256(payload.encode()).hexdigest(),'forms':len(forms),'authorization':"Prepare the transaction to make that repair to all affected questions and when it's ready go ahead and push it to the database. In addition, you'll need to fix all generators that have this flaw. Don't wait for me."}
 (HERE/'preparation.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
