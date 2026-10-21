"""Read current checkbox content and retained pre-migration source choices."""
import json,subprocess,threading,re
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
DB=EDBClient(Config(),threading.Event())
QUESTION='''[* {:question/difficulty [:db/id :db/ident]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]'''
ITEM='''[* {:task-item/content [:db/id]} {[:task-item/responses :limit nil] [:db/id :answer/id :answer/value]}]'''
def save(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def native(directory,basis,groups):
 directory.mkdir(parents=True,exist_ok=True);(directory/'native-pulls.edn').write_text(dumps(groups)+'\n')
 run=subprocess.run([str(ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'),str(directory),str(basis)],env=DB.environment,capture_output=True,text=True,timeout=240)
 (directory/'read.stderr').write_text(run.stderr);run.check_returncode()
 return {n:loads((directory/(n+'.edn')).read_text())for n,_,_ in groups}
def pull_many(name,ids,basis,pattern=QUESTION):
 ids=sorted(ids);groups=[(name+'-'+str(i),pattern,ids[i:i+100])for i in range(0,len(ids),100)]
 result=native(HERE/name,basis,groups);return [v for n,_,_ in groups for v in result[n]if v]
def refs(value):return [value]if isinstance(value,dict)else value
if __name__=='__main__':
 identity=DB.status();save(HERE/'identity.json',identity);basis=identity['basis']
 fields=DB.query('[:find ?f :where [?f :answer-field/type :answer-field.type/checkbox]]',[],HERE/'queries','checkbox-fields',basis)
 data=pull_many('field-census',[f for f, in fields],basis,'[:db/id {[:question/_answer-fields :limit nil] [:db/id]}]')
 ids={q[':db/id']for f in data for q in refs(f.get(':question/_answer-fields',[]))}
 current=pull_many('current',ids,basis);save(HERE/'current.json',current)
 imported=[q[':db/id']for q in current if q.get(':question/math-academy-id')]
 originals=pull_many('originals',imported,1100);save(HERE/'originals.json',originals)
 print(json.dumps({'basis':basis,'checkbox_questions':len(current),'imported':len(imported),'originals':len(originals)}),flush=True)
 candidates=[]
 for q in originals:
  none=[(f,a)for f in q.get(':question/answer-fields',[])if f.get(':answer-field/type',{}).get(':db/ident')==':answer-field.type/radio'for a in f.get(':answer-field/choices',[])if re.fullmatch(r'(?i)\W*none(?: of (?:the )?(?:above|these)(?: statements)?)?\W*',a.get(':answer/value',''))]
  if none:candidates.append({'id':q[':db/id'],'source_basis':1100,'ma_id':q.get(':question/math-academy-id'),'none_choices':[{'field':f[':db/id'],'answer':a[':db/id'],'value':a[':answer/value'],'source_correct':f.get(':answer-field/correct',{}).get(':db/id')==a[':db/id']}for f,a in none]})
 save(HERE/'original-none-candidates.json',candidates)
 print(json.dumps({'source_none_questions':len(candidates),'none_correct':sum(any(c['source_correct']for c in q['none_choices'])for q in candidates)}),flush=True)
