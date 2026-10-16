"""Read-only current state, ownership, usage and provenance for the 18 flags."""
import json,os,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];OLD=H.parent/'2026-10-14-study-backlog';sys.path.insert(0,str(R/'scripts/question_capture'))
from edn import loads,dumps
B='/home/jake/Developer/EDB/target/release/edb';E={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
def cli(*args):return subprocess.check_output([B,*args],env=E,text=True,timeout=150)
def save(name,x):(H/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def query(name,text,args,history=False):
 q=H/(name+'-query.edn');q.write_text(text);i=H/(name+'-inputs.edn');i.write_text(dumps(args))
 out=cli('query','--database','math','--as-of',str(basis),'--file',str(q),'--inputs',str(i),*(['--history'] if history else []),'--max-value-bytes','1073741824');(H/(name+'.edn')).write_text(out);return loads(out)
assert not (H/'snapshot.json').exists(),'Keep the original read snapshot'
basis=int(re.search(r'basis_t=(\d+)',cli('status','--database','math'))[1]);ids=sorted({x['question'] for x in json.loads((OLD/'content-quality-findings.json').read_text())})
save('snapshot.json',{'basis':basis,'database':'math','questions':ids,'purpose':'Investigation only; no answer/field repair authorized'})
pattern=H/'question-pull.edn';pattern.write_text('[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]} {:knowledge-point/_questions [:db/id :knowledge-point/id :knowledge-point/title {:topic/_knowledge-points [:db/id :topic/title]}]}]')
records=[]
for eid in ids:
 out=cli('pull','--database','math','--as-of',str(basis),'--file',str(pattern),'--entity',str(eid));(H/f'{eid}.edn').write_text(out);records.append(loads(out))
save('questions.json',records)
question_fields=query('field-history','[:find ?question ?field ?tx ?source ?added :in $ [?question ...] :where [?question :question/answer-fields ?field ?tx ?source ?added]]',[ids],True)
fields=sorted({r[1] for r in question_fields})
correct=query('correct-history','[:find ?field ?answer ?tx ?source ?added :in $ [?field ...] :where [?field :answer-field/correct ?answer ?tx ?source ?added]]',[fields],True)
worked=query('solution-history','[:find ?question ?solution ?tx ?source ?added :in $ [?question ...] :where [?question :question/worked-solution ?solution ?tx ?source ?added]]',[ids],True)
usage=query('presentations','[:find ?question ?item :in $ [?question ...] :where [?item :task-item/content ?question]]',[ids])
answers=sorted({a[':db/id'] for q in records for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])})
responses=query('responses','[:find ?answer ?item :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',[answers])
# Question difficulty / source intake history is small; no assumptions about why unrated.
difficulty=query('difficulty-history','[:find ?question ?rating ?tx ?source ?added :in $ [?question ...] :where [?question :question/difficulty ?rating ?tx ?source ?added]]',[ids],True)
refs=sorted({r[2] for rs in [question_fields,correct,worked,difficulty] for r in rs}|{r[3] for rs in [question_fields,correct,worked,difficulty] for r in rs})
(H/'any-pull.edn').write_text('[*]');ref_records={}
for eid in refs:
 out=cli('pull','--database','math','--as-of',str(basis),'--file',str(H/'any-pull.edn'),'--entity',str(eid));(H/f'provenance-{eid}.edn').write_text(out);ref_records[str(eid)]=loads(out)
save('provenance.json',ref_records)
if usage:
 (H/'item-pull.edn').write_text('[* {:task-item/status [:db/ident]} {:learner-task/_items [:db/id :learner-task/status {:learner/_activity [:db/id :learner/name]}]}]')
 for eid in sorted({r[1] for r in usage}):
  (H/f'item-{eid}.edn').write_text(cli('pull','--database','math','--as-of',str(basis),'--file',str(H/'item-pull.edn'),'--entity',str(eid)))
print(json.dumps({'basis':basis,'questions':len(records),'field_history_events':len(question_fields),'correct_events':len(correct),'worked_solution_events':len(worked),'presentations':len(usage),'submitted_responses':len(responses),'provenance_entities':len(refs)}))
