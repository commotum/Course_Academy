"""Read-only final inventory/key/identity check at one fresh database basis."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
D=H/'final-check';D.mkdir(exist_ok=True);db=connection();t=db.basis();inventory=json.loads((H/'inventory.json').read_text());qs={}
for group,file in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]:
 for q in json.loads((H/group/file).read_text())['questions']:qs[q[':db/id']]=q
assert len(qs)==2306
fields={f[':db/id']:f for q in qs.values()for f in q.get(':question/answer-fields',[])};correct={f:obj[':answer-field/correct'][':db/id']for f,obj in fields.items()if ':answer-field/correct'in obj}
for name in ['flagged','group-1','group-2','group-3','group-3/checkbox-repair']:
 assert json.loads((H/name/'verification.json').read_text())['committed']
 for p in json.loads((H/name/'approved-proposals.json').read_text()):
  if p['attribute']=='answer-field/correct':correct[p['entity']]=p['after']
links=db.query((H/'question-links-query.edn').read_text(),[[x['entity']for x in inventory['topics']]],D,'pool',t);original=set(map(tuple,inventory['links']));assert original.issubset(set(map(tuple,links)))
expected_qfields={(q[':db/id'],f[':db/id'])for q in qs.values()for f in q.get(':question/answer-fields',[])};expected_qfields.remove((17592186106313,17592186104026))
actual_qfields=db.query('[:find ?q ?f :in $ [?q ...] :where [?q :question/answer-fields ?f]]',[sorted(qs)],D,'question-fields',t);assert set(map(tuple,actual_qfields))==expected_qfields
actual_correct=dict(db.query('[:find ?f ?a :in $ [?f ...] :where [?f :answer-field/correct ?a]]',[sorted(fields)],D,'correct-links',t));assert actual_correct==correct
expected_banks={(f,a[':db/id'])for f,obj in fields.items()for a in obj.get(':answer-field/choices',[])};actual_banks=db.query('[:find ?f ?a :in $ [?f ...] :where [?f :answer-field/choices ?a]]',[sorted(fields)],D,'choice-memberships',t);assert set(map(tuple,actual_banks))==expected_banks
qids=dict(db.query('[:find ?q ?id :in $ [?q ...] :where [?q :question/id ?id]]',[sorted(qs)],D,'question-ids',t));assert {q:str(v)for q,v in qids.items()}=={q:str(obj[':question/id'])for q,obj in qs.items()}
fids=dict(db.query('[:find ?f ?id :in $ [?f ...] :where [?f :answer-field/id ?id]]',[sorted(fields)],D,'field-ids',t));assert {f:str(v)for f,v in fids.items()}=={f:str(obj[':answer-field/id'])for f,obj in fields.items()}
answers={a[':db/id']:a for f in fields.values()for a in f.get(':answer-field/choices',[])};aids=dict(db.query('[:find ?a ?id :in $ [?a ...] :where [?a :answer/id ?id]]',[sorted(answers)],D,'answer-ids',t));assert {a:str(v)for a,v in aids.items()}=={a:str(obj[':answer/id'])for a,obj in answers.items()}
active={f for q,f in expected_qfields};missing=sorted(active-set(correct));assert missing==[17592186123602],missing
report={'passed':True,'basis_t':t,'topics':38,'question_example_records':len(qs),'original_question_pool_links_preserved':True,'additional_pool_links_since_snapshot':len(set(map(tuple,links))-original),'active_answer_fields':len(active),'retained_answer_field_entities':len(fields),'retained_answer_entities':len(answers),'question_field_and_answer_UUIDs_unchanged':True,'all_answer_banks_and_existing_correct_links_preserved':True,'only_expected_duplicate_membership_detached':True,'remaining_unkeyed_fields':missing,'remaining_unresolved_question':17592186125167,'remaining_unresolved_source':'q-47586'}
(H/'final-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
