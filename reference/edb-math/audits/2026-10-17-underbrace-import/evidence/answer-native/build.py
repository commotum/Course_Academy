import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(ROOT))
from capture.scripts.config import Config
from capture.scripts.database.preview import _library
HERE=Path(__file__).resolve().parent
NAME=sys.argv[1] if len(sys.argv)>1 else 'scan'
assert NAME in ('scan','history')
lib=_library(Config())
cmd=['rustc','--edition=2024','-O',str(HERE/(NAME+'.rs')),'--extern','edb_core='+str(lib),'-L','dependency='+str(lib.parent),'-o',str(HERE/NAME)]
r=subprocess.run(cmd,capture_output=True,text=True)
(HERE/(NAME+'-build.stdout')).write_text(r.stdout);(HERE/(NAME+'-build.stderr')).write_text(r.stderr)
if r.returncode:print(r.stderr);raise SystemExit(r.returncode)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/(NAME+'-build.json')).write_text(json.dumps({'command':cmd,'database_writes':0,'input_hashes':{str(p):digest(p) for p in [lib,HERE/(NAME+'.rs')]},'binary_sha256':digest(HERE/NAME)},indent=2)+'\n')
print('built read-only '+NAME)
