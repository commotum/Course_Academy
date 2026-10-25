import hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
p=H/'transaction.edn';r=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(p)],env=connection().env,check=True,text=True,capture_output=True);(H/'preview.log').write_text(r.stdout);(H/'native-preview-verification.json').write_text(json.dumps({'passed':True,'committed':False,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'basis_t':int((H/'preview-basis.txt').read_text()),'native_predicates':True,'output':r.stdout},indent=2)+'\n');print(r.stdout)
