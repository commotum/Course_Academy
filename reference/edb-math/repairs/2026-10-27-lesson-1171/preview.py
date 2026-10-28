import json,subprocess,sys,threading
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R));sys.path.insert(0,str(R/'scripts'))
from capture.scripts.config import Config
from capture.scripts.database.preview import preview_executable
from migrate_learner_history import connection,loads
binary=preview_executable(Config(),threading.Event());db=connection();p=subprocess.run([str(binary),'with','--database','math','--file',str(H/'transaction.edn'),'--source',':agent/codex'],env=db.env,capture_output=True,text=True);(H/'preview.edn').write_text(p.stdout);(H/'preview.stderr').write_text(p.stderr);p.check_returncode();r=loads(p.stdout);assert r.get(':edb/speculative')is True;print('Native speculative transaction passed, including question, answer-field and answer validation.')
