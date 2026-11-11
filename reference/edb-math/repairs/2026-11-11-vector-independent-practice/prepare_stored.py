"""Prepare a two-field CAS repair and native preview; no live commit."""
import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_publish import Publisher,jsonable
from capture.scripts.database.edn import dumps,loads,kw

def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(jsonable(v),indent=2)+'\n')
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];out=H/'stored/preparations'/str(basis);out.mkdir(parents=True,exist_ok=True)
current=jsonable(p.read_kp(17592186235285,out,basis));baseline=json.loads((H/'capture/kp.json').read_text());before=json.loads((H/'stored/before.json').read_text());proposed=json.loads((H/'stored/proposed.json').read_text())
assert current[':knowledge-point/questions']==baseline[':knowledge-point/questions'],'Pool changed; refresh sibling audit before preparing'
assert current[':knowledge-point/question-generator']==baseline[':knowledge-point/question-generator'],'Generator registration changed since review'
assert next(q for q in current[':knowledge-point/questions'] if q[':db/id']==before[':db/id'])==before
forms=[]
for attribute in ['question/problem','question/worked-solution']:
 forms.append([kw('db/cas'),before[':db/id'],kw(attribute),before[':'+attribute],proposed[':'+attribute]])
forms.append([kw('db/ensure'),before[':db/id'],kw('question/validate')])
# The durable apply also guards the captured basis and holds the worker KP lock.
oldgen=current[':knowledge-point/question-generator'][':db/id']
(out/'transaction.edn').write_text(dumps(forms)+'\n')
report=p.client.command('with','--file',out/'transaction.edn','--source',':agent/codex')
(out/'preview.edn').write_text(report);preview=loads(report)
assert preview[':edb/db-before-t']==basis,'Preview moved; prepare at a fresh basis'
attrs=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],out,'attribute-idents',basis);names=dict(attrs)
allowed={(before[':db/id'],kw('question/problem')),(before[':db/id'],kw('question/worked-solution'))}
for entity,attr,value,tx,source,added in preview[':edb/tx-data']:
 assert names[attr]==kw('db/txInstant') or (entity,names[attr]) in allowed,(entity,names[attr])
save(out/'preparation.json',dict(status,basis=basis,source=':agent/codex',pool_count=len(current[':knowledge-point/questions']),forms=len(forms),changed_question=before[':db/id'],old_generator=oldgen,preview_passed=True,database_writes=0))
save(H/'stored/preview-latest.json',dict(directory=str(out),basis=basis,passed=True,database_writes=0))
print(json.dumps(dict(basis=basis,preview_passed=True,forms=len(forms),directory=str(out))))
