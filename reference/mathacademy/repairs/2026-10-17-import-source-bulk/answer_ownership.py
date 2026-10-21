"""Inspect all answer owners and direct saved-response references at snapshot basis."""
from snapshot import *
def main():
    original=Path((HERE/'snapshot-directory.txt').read_text().strip())
    identity=json.loads((original/'identity.json').read_text())
    ids=[e[':db/id'] for e in json.loads((original/'entities.json').read_text()) if ':answer/value' in e]
    out=original/'answer-ownership';out.mkdir(exist_ok=True)
    pattern='[* {:answer/type [:db/id :db/ident]} {[:answer-field/_choices :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:question/_answer-fields :limit nil] [:db/id :question/id :question/math-academy-id]}]} {[:task-item/_responses :limit nil] [*]}]'
    (out/'native-pulls.edn').write_text(dumps([['answers',pattern,ids]])+'\n')
    db=Publisher.from_environment(source=SOURCE).client
    run=subprocess.run([str(READ),str(out),str(identity['basis'])],env=db.environment,capture_output=True,text=True,timeout=180)
    (out/'read.stderr').write_text(run.stderr);run.check_returncode()
    answers=loads((out/'answers.edn').read_text());save(out/'answers.json',answers)
    kinds=collections.Counter();saved=[]
    for a in answers:
        fields=a.get(':answer-field/_choices',[])
        if isinstance(fields,dict):fields=[fields]
        for f in fields:kinds[str(f[':answer-field/type'][':db/ident'])]+=1
        if a.get(':task-item/_responses'):saved.append(a[':db/id'])
    summary={'basis':identity['basis'],'answers':len(answers),'field_types':dict(kinds),'saved_response_answer_ids':saved}
    save(out/'summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
