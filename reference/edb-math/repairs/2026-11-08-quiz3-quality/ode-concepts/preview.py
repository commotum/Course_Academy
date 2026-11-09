import sys,json,subprocess
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');H=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection
b=ROOT/'.local/edb/capture-runtime/native-preview-74dc6726c42c0594c98069f66077a9078a8cf13732f8beabc35fba79f9795d81'
r=subprocess.run([str(b),'with','--database','math','--file',str(H/'transaction.edn'),'--source',':course-academy.source/editor'],env=connection().env,capture_output=True,text=True)
(H/'preview.edn').write_text(r.stdout);(H/'preview.stderr').write_text(r.stderr);print(r.returncode,r.stdout[:1200],r.stderr[:3000]);sys.exit(r.returncode)
