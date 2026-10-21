"""Capture every current checkbox question and its complete context, read only."""
import argparse,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from capture.scripts.database.edn import loads,dumps
HERE=Path(__file__).resolve().parent
E=HERE/'evidence'
E.mkdir(parents=True,exist_ok=True)
TOPIC='[:db/id :topic/id :topic/math-academy-id :topic/title]'
KP='[:db/id :knowledge-point/id :knowledge-point/title {[:topic/_knowledge-points :limit nil] '+TOPIC+'}]'
ANSWER='[* {:answer/type [:db/id :db/ident]} {[:task-item/_responses :limit nil] [:db/id :task-item/content :task-item/status :task-item/performance]}]'
FIELD='[* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] '+ANSWER+'} {:answer-field/correct '+ANSWER+'}]'
ITEM='[* {[:task-item/responses :limit nil] [* {:answer/type [:db/id :db/ident]}]}]'
STEP='[:db/id {[:activity/_steps :limit nil] [:db/id :activity/title {:activity/type [:db/id :db/ident]} {:activity/scope '+TOPIC+'}]}]'
QUESTION_PULL='[* {:question/difficulty [:db/id :db/ident]} {[:knowledge-point/_questions :limit nil] '+KP+'} {[:knowledge-point/_canonical-example :limit nil] '+KP+'} {[:question/answer-fields :limit nil] '+FIELD+'} {[:step/_content :limit nil] '+STEP+'} {[:task-item/_content :limit nil] '+ITEM+'}]'
ID_QUERY='[:find ?f :where [?f :answer-field/type :answer-field.type/checkbox]]'
def save(name,value): (HERE/name).write_text(json.dumps(jsonable(value),ensure_ascii=False,indent=2)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE);parser.add_argument('--basis',type=int);args=parser.parse_args()
    out=args.output.resolve();evidence=out/'evidence';evidence.mkdir(parents=True,exist_ok=True)
    pub=Publisher.from_environment(source=':agent/codex');client=pub.client
    if (evidence/'status.json').exists():status=json.loads((evidence/'status.json').read_text())
    else:
        status=client.status()
        if args.basis:status['basis']=args.basis
        (evidence/'status.json').write_text(json.dumps(status,indent=2)+'\n')
    if args.basis:assert status['basis']==args.basis
    basis=status['basis'];print('Audit basis',basis,flush=True)
    (evidence/'question-pull.edn').write_text(QUESTION_PULL+'\n')
    if not(evidence/'capture-complete.json').exists():
        subprocess.run([str(HERE/'native/capture'),str(evidence),str(basis)],env=client.environment,check=True)
    questions=sum([loads(p.read_text())for p in sorted(evidence.glob('capture-*.edn'),key=lambda p:int(p.stem.split('-')[-1]))],[])
    questions.sort(key=lambda q:q[':db/id']);ids=[q[':db/id']for q in questions];assert len(ids)==len(set(ids))
    for name,value in [('questions.json',questions),('question-ids.json',ids),('target.json',next(q for q in questions if q[':db/id']==17592186272202))]:
        (out/name).write_text(json.dumps(jsonable(value),ensure_ascii=False,indent=2)+'\n')
    (out/'questions.edn').write_text(dumps(questions)+'\n')
    fields=[f for q in questions for f in q.get(':question/answer-fields',[]) if f.get(':answer-field/type',{}).get(':db/ident')==':answer-field.type/checkbox']
    summary={'database':status['database'],'lineage':status['lineage'],'basis':basis,'questions':len(questions),'checkbox_fields':len(fields),'questions_with_saved_uses':sum(bool(q.get(':task-item/_content')) for q in questions),'question_pull':QUESTION_PULL,'database_writes':0}
    (out/'audit-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items()if k!='question_pull'},indent=2))
if __name__=='__main__':main()
