"""Read-only current evidence capture and scoped build of actual learner QA tools."""
import sys,json,hashlib,subprocess,importlib.util,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment,build_learning
from database import Database
from edn import dumps
from inventory_jobs import save
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
# Read only; regeneration and all durable submissions get a new locked recheck.
b=DB.basis();p=OUT/'initial';p.mkdir(exist_ok=True)
kp=DB.query((HERE/'source-query.edn').read_text(),[[17592186115241]],p,'kp',b)[0][0]
print(json.dumps({'basis':b,'title':kp[':knowledge-point/title'],'practice_questions':len(kp[':knowledge-point/questions']),'generator':kp.get(':knowledge-point/question-generator')},default=str),flush=True)
save(p/'kp.json',json.loads(json.dumps(kp,default=str)))
freeze=json.loads((HERE/'frozen-sha256.json').read_text());bad=[rel for rel,h in freeze.items() if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=h];save(p/'previous-freeze-check.json',{'passed':not bad,'changed':bad});assert not bad,bad
native=build_learning(ROOT.parent/'EDB')
deps=ROOT/'target/release/deps';libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
for source,name in [(HERE/'inspect-inventory.rs','inspect-inventory'),(ROOT/'generate/runs/current/check-engine.rs','check-engine')]:
 cmd=['rustc','--edition=2024','-O',str(source),'-L','dependency='+str(deps),'-L','dependency='+str(ROOT.parent/'EDB/target/release/deps'),'-o',str(OUT/name)]
 for n,path in libs.items():cmd+=['--extern',n+'='+str(path)]
 subprocess.run(cmd,check=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save(OUT/'native-build.json',{'learning':str(native),'libraries':{str(p):sha(p) for p in libs.values()},'executables':{str(p):sha(p) for p in (native,OUT/'inspect-inventory',OUT/'check-engine')},'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in (HERE/'inspect-inventory.rs',ROOT/'generate/runs/current/check-engine.rs')}})
subprocess.run([str(OUT/'check-engine'),str(HERE/'native-input.json'),str(p/'current-native-report.json')],check=True)
print('Current-source capture, frozen package and current learner grading verified',flush=True)
