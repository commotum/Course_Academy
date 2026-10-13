"""Read active attribution before comparing authored captures with repaired content."""
from pathlib import Path
import threading
from scripts.config import Config
from scripts.database.client import EDBClient, QUESTION_PULL
from scripts.storage import atomic_json

root=Path(__file__).resolve().parent/'active-correction-sources'
client=EDBClient(Config(),threading.Event())
identity=client.status();basis=identity['basis']
rows=client.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?id ...] :where [?q :question/math-academy-id ?id]]',
                 [['q-79044','q-5538']],root,'questions',basis)
findings=[]
for row in rows:
 q=row[0];ids={q[':db/id']}
 for field in q.get(':question/answer-fields',[]):
  ids.add(field[':db/id'])
  ids.update(a[':db/id'] for a in field.get(':answer-field/choices',[]))
  if field.get(':answer-field/correct'):ids.add(field[':answer-field/correct'][':db/id'])
 facts=client.query('''[:find ?e ?attr ?v ?source :in $ [?e ...]
 :where [?e ?a ?v _ ?s] [?a :db/ident ?attr] [?s :db/ident ?source]]''',
 [sorted(ids)],root,q[':question/math-academy-id']+'-facts',basis)
 authored={'question/problem','question/worked-solution','question/answer-fields',
           'answer-field/key','answer-field/type','answer-field/choices','answer-field/correct','answer/type','answer/value'}
 selected=[fact for fact in facts if str(fact[1]).lstrip(':') in authored]
 sources=sorted({str(fact[3]) for fact in selected})
 findings.append({'id':q[':question/math-academy-id'],'sources':sources,
   'protected_agent_sources':sorted(s for s in sources if s.startswith(':agent/')),
   'facts':[{'entity':f[0],'attribute':str(f[1]),'value':str(f[2]),'source':str(f[3])} for f in selected]})
atomic_json(root/'verification.json',{'identity':identity,'questions':findings})
print({'basis':basis,'questions':[{k:v for k,v in f.items() if k!='facts'} for f in findings]})
