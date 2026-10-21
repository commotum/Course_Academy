"""Reconcile the historical audit with a fresh, read-only EDB snapshot."""
import collections, hashlib, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps, loads
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent/'2026-10-16-import-root-cause/database'
SOURCE = ':agent/gpt-6.1-sol-high'
READ = HERE/'native_read'
QUESTION = '[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]'
USES = '[:db/id {[:task-item/_content :limit nil] [* {[:task-item/responses :limit nil] [*]}]}]'
def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str)+'\n')
def main():
    rows = {}
    for queue in ('source-backed-candidates.jsonl','secondary-source-backed-candidates.jsonl'):
        for line in (AUDIT/queue).read_text().splitlines():
            row=json.loads(line);key=(row['entity'],row['attribute'])
            if key in rows: assert rows[key]['current_value']==row['current_value']
            else: rows[key]=row
    db=Publisher.from_environment(source=SOURCE).client
    identity=db.status();out=HERE/f"snapshot-{identity['basis']}";out.mkdir(exist_ok=True)
    save(out/'identity.json',identity)
    ids=sorted({e for e,a in rows})
    qids=sorted({q for r in rows.values() for q in r['context']['question_ids']})
    contentids=sorted(set(qids)|{e for e,a in rows if a==':tutorial/content'})
    groups=[['entities','[* {:answer/type [:db/id :db/ident]}]',ids],['questions',QUESTION,qids],['saved-uses',USES,contentids]]
    (out/'native-pulls.edn').write_text(dumps(groups)+'\n')
    run=subprocess.run([str(READ),str(out),str(identity['basis'])],env=db.environment,capture_output=True,text=True,timeout=240)
    (out/'read.stderr').write_text(run.stderr);run.check_returncode();print(run.stdout,flush=True)
    entities={e[':db/id']:e for e in loads((out/'entities.edn').read_text()) if e}
    reconciled=[]
    for (e,a),r in rows.items():
        current=entities.get(e,{}).get(a)
        reconciled.append({'entity':e,'attribute':a,'audit_value':r['current_value'],'current_value':current,'status':'unchanged' if current==r['current_value'] else 'absent' if current is None else 'changed-since-audit'})
    save(out/'reconciliation.json',reconciled)
    save(out/'entities.json',list(entities.values()))
    save(out/'questions.json',loads((out/'questions.edn').read_text()))
    uses=loads((out/'saved-uses.edn').read_text())
    summary={**identity,'candidate_fields':len(rows),'states':dict(collections.Counter(r['status'] for r in reconciled)),'saved_items':sum(len(e.get(':task-item/_content',[])) for e in uses),'snapshot_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.edn')}}
    save(out/'summary.json',summary);(HERE/'snapshot-directory.txt').write_text(str(out)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
