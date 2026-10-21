import json,subprocess,threading,hashlib,sys
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient,QUESTION_PULL
from capture.scripts.database.edn import dumps,loads,kw
from scripts.generator_packages import materialize_package
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];DB=EDBClient(Config(),threading.Event());KP=17592186184153
QUESTION='''[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]'''
ITEM='[* {:task-item/status [:db/id :db/ident]} {:task-item/content [:db/id]} {[:task-item/responses :limit nil] [*]}]'
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def native(directory,basis,groups):
 directory.mkdir(parents=True,exist_ok=True);(directory/'native-pulls.edn').write_text(dumps(groups)+'\n');p=subprocess.run([str(ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'),str(directory),str(basis)],env=DB.environment,capture_output=True,text=True,timeout=180);(directory/'stderr').write_text(p.stderr);p.check_returncode();return {n:loads((directory/(n+'.edn')).read_text())for n,_,_ in groups}
if __name__=='__main__':
 identity=DB.status();save('identity.json',identity);pattern='[* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION+'} {[:knowledge-point/questions :limit nil] '+QUESTION+'}]';kp=DB.query('[:find (pull ?kp '+pattern+') :in $ ?kp :where [?kp :knowledge-point/id _]]',[KP],HERE/'evidence','kp',identity['basis'])[0][0];save('kp.json',kp);qids=[q[':db/id']for q in kp[':knowledge-point/questions']];items=DB.query('[:find ?q (pull ?i '+ITEM+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[qids],HERE/'evidence','items',identity['basis']);save('items.json',items)
 if not(HERE/'original').exists():materialize_package(kp[':knowledge-point/question-generator'][':question-generator/script'],Path(DB.config.math_root),HERE/'original')
 print(json.dumps({'identity':identity,'generator':kp[':knowledge-point/question-generator'],'pool_size':len(qids),'items':items},indent=2,default=str))
 for q in kp[':knowledge-point/questions']:print(json.dumps({'id':q[':db/id'],'ma':q.get(':question/math-academy-id'),'problem':q[':question/problem'],'solution':q.get(':question/worked-solution'),'correct':[f.get(':answer-field/correct',{}).get(':answer/value')for f in q.get(':question/answer-fields',[])]},ensure_ascii=False))
