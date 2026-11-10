"""Capture and prepare an atomic dropdown-classification to checkbox migration."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
import time
import uuid

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from migrate_learner_history import connection, dumps, kw
from question_capture.core import stable_id

db = connection()
basis = db.basis()
def save(name, value):
    (H / (name + '.json')).write_text(json.dumps(value, default=str, indent=2) + '\n')
def query(text, inputs, name):
    start=time.monotonic()
    result = db.query(text, inputs, H, name, basis)
    save(name, result)
    print(name,round(time.monotonic()-start,2),flush=True)
    return result

assert not (H / 'commit-intent.json').exists(), 'Reconcile existing request before preparing again.'
save('basis', dict(basis=basis))
(H / 'database-status.txt').write_text(db.command('status'))
topic = query((H / 'topic-before-query.edn').read_text(), [17592186050677], 'topic-before')[0][0]
questions = {}
for kp in topic[':topic/knowledge-points']:
    for q in kp.get(':knowledge-point/questions', []) + [kp[':knowledge-point/canonical-example']]:
        questions[q[':db/id']] = q
save('questions-before', list(questions.values()))
targets = [q for q in questions.values() if any(
    a.get(':answer/value') in ('homogeneous', 'inhomogeneous')
    for f in q.get(':question/answer-fields', []) for a in f.get(':answer-field/choices', []))]
targets.sort(key=lambda q:q[':db/id'])
assert len(targets) == 8 and {17592186397107,17592186311909} <= {q[':db/id'] for q in targets}
save('targets-before', targets)
qids = [q[':db/id'] for q in targets]
items = [r[0] for r in query('[:find (pull ?i [*]) :in $ [?q ...] :where [?i :task-item/content ?q]]', [qids], 'presentations-before')]
oldfields = [f[':db/id'] for q in targets for f in q[':question/answer-fields']]
oldanswers = [a[':db/id'] for q in targets for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
uses = query('[:find ?i ?a :in $ [?a ...] :where [?i :task-item/responses ?a]]', [oldanswers], 'response-uses-before')
assert {r[0] for r in uses} <= {i[':db/id'] for i in items}, 'Response use outside scope'
links = query('[:find (pull ?f [:db/id {[:question/_answer-fields :limit nil] [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]', [oldfields], 'field-uses-before')
def many(value):
    return [value] if isinstance(value,dict) else value
assert {q[':db/id'] for r in links for q in many(r[0].get(':question/_answer-fields',[]))} <= set(qids), 'Shared field outside scope'
query('[:find (pull ?f [*]) :in $ [?f ...] :where [?f :answer-field/id _]]', [oldfields], 'old-fields-before')
query('[:find (pull ?a [*]) :in $ [?a ...] :where [?a :answer/id _]]', [oldanswers], 'old-answers-before')
query('[:find (pull ?q [:db/id {[:knowledge-point/_questions :limit nil] [:db/id]} {[:knowledge-point/_canonical-example :limit nil] [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]', [qids], 'memberships-before')
source = query('[:find ?e :in $ ?ident :where [?e :db/ident ?ident]]', [kw('agent/codex')], 'contributor')
assert len(source) == 1

# Independent review: forcing term after moving all y-independent terms right.
forcing = {
 'q-337919':['0','2','2x'], 'q-337990':['0','exp(x)','-x'],
 'q-337996':['7','0','-x^3'], 'q-338006':['0','4x','0'],
 'q-338023':['ln(x)','0','exp(x)'], 'q-338087':['0','0','-9'],
 'q-338004':['0','x','-4x'], 'q-338082':['x','0','-5x'],
}
forms, plan, proposed, answer_map = [], [], [], {}
new_field_ids, new_answer_ids = [], []
prompt = 'Select all homogeneous second-order linear differential equations.\n\nSelect all that apply. If none apply, leave all boxes unchecked.'
for q in targets:
    qid, ma = q[':db/id'], q[':question/math-academy-id']
    matched = list(re.finditer(r'The equation \$(.*?)\$ is \{\{(field-[123])\}\}', q[':question/problem'], re.S))
    assert len(matched) == 3
    bykey = {f[':answer-field/key']:f for f in q[':question/answer-fields']}
    assert set(bykey) == {'field-1','field-2','field-3'}
    new, objects, mappings, fields = copy.deepcopy(q), [], [], []
    for index, match in enumerate(matched):
        label = match[2]
        assert label == 'field-' + str(index+1)
        old = bykey[label]
        assert old[':answer-field/type'][':db/ident'] == ':answer-field.type/select'
        equation = re.sub(r'^\\,\s*', '', match[1]).strip()
        content = '$' + equation + '$'
        truth = forcing[ma][index] == '0'
        assert (old[':answer-field/correct'][':answer/value'] == 'homogeneous') == truth
        assert {a[':answer/value'] for a in old[':answer-field/choices']} == {'homogeneous','inhomogeneous'}
        token = ma + '/homogeneous-checkbox-v1/' + label
        fid, tempid = stable_id('field',token), ma+'-'+label
        bank = []
        for value in ('false','true'):
            aid, atemp = stable_id('answer',token+'/'+value), tempid+'-'+value
            new_answer_ids.append(aid)
            forms.append({kw('db/id'):atemp,kw('answer/id'):aid,kw('answer/type'):kw('answer.type/text'),kw('answer/value'):value})
            bank.append({':answer/id':str(aid),':answer/type':{':db/ident':':answer.type/text'},':answer/value':value,':db/id':atemp})
            forms.append([kw('db/ensure'),atemp,kw('answer/validate')])
        correct = tempid+'-'+str(truth).lower()
        forms.append({kw('db/id'):tempid,kw('answer-field/id'):fid,kw('answer-field/key'):content,
          kw('answer-field/type'):kw('answer-field.type/checkbox'),kw('answer-field/choices'):[a[':db/id'] for a in bank],kw('answer-field/correct'):correct})
        forms += [[kw('db/ensure'),tempid,kw('answer-field/validate')],
          [kw('db/retract'),qid,kw('question/answer-fields'),old[':db/id']],
          [kw('db/add'),qid,kw('question/answer-fields'),tempid]]
        new_field_ids.append(fid)
        fields.append({':answer-field/id':str(fid),':answer-field/key':content,':answer-field/type':{':db/ident':':answer-field.type/checkbox'},
          ':answer-field/choices':bank,':answer-field/correct':next(a for a in bank if a[':db/id']==correct),':db/id':tempid})
        objects.append(dict(source_label=label,field_id=str(fid),content=content,source_fragment=match[0]))
        for a in old[':answer-field/choices']:
            boolean = str(a[':answer/value']=='homogeneous').lower()
            mapping=dict(old_field=old[':db/id'],old_answer=a[':db/id'],old_value=a[':answer/value'],
              new_field_uuid=str(fid),new_answer_uuid=str(stable_id('answer',token+'/'+boolean)),new_tempid=tempid+'-'+boolean,
              selected=boolean=='true',source_label=label)
            answer_map[a[':db/id']] = mapping
            mappings.append(mapping)
    forms += [[kw('db/cas'),qid,kw('question/problem'),q[':question/problem'],prompt],[kw('db/ensure'),qid,kw('question/validate')]]
    new[':question/problem'], new[':question/answer-fields'] = prompt, fields
    proposed.append(dict(question=new,objects=objects))
    tuples = []
    for values in itertools.product(('homogeneous','inhomogeneous'), repeat=3):
        oldids = [next(a[':db/id'] for a in bykey['field-'+str(i+1)][':answer-field/choices'] if a[':answer/value']==v) for i,v in enumerate(values)]
        tuples.append(dict(old_answers=oldids,new_answers=[answer_map[a]['new_answer_uuid'] for a in oldids],
          selected=[i+1 for i,v in enumerate(values) if v=='homogeneous'],correct=all((v=='homogeneous')==(forcing[ma][i]=='0') for i,v in enumerate(values))))
    plan.append(dict(entity=qid,ma_id=ma,forcing=forcing[ma],correct_selected=[i+1 for i,f in enumerate(forcing[ma]) if f=='0'],objects=objects,choice_mapping=mappings,tuple_mapping=tuples))

response_migrations=[]
for item in items:
    responses = [r[':db/id'] for r in item.get(':task-item/responses',[])]
    assert all(a in answer_map for a in responses)
    for a in responses:
        forms += [[kw('db/retract'),item[':db/id'],kw('task-item/responses'),a],
          [kw('db/add'),item[':db/id'],kw('task-item/responses'),answer_map[a]['new_tempid']]]
    if responses:
        forms.append([kw('db/ensure'),item[':db/id'],kw('task-item/validate')])
        response_migrations.append(dict(item=item[':db/id'],before=responses,after=[answer_map[a]['new_answer_uuid'] for a in responses]))
for attribute, values in [('answer-field/id',new_field_ids),('answer/id',new_answer_ids)]:
    assert not query('[:find ?e ?v :in $ [?v ...] :where [?e :'+attribute+' ?v]]', [values], 'new-'+attribute.split('/')[0]+'-identity-check')
save('plan',dict(basis=basis,source=':agent/codex',source_entity=source[0][0],topic=topic[':db/id'],questions=plan,response_migrations=response_migrations))
save('proposed-presentation',dict(cases=proposed))
(H/'transaction.edn').write_text(dumps(forms)+'\n')
pattern='[* {:question/difficulty [:db/id :db/ident]} {[:knowledge-point/_questions :limit nil] [:db/id]} {[:knowledge-point/_canonical-example :limit nil] [:db/id]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'
(H/'question-pattern.edn').write_text(pattern)
(H/'question-ids.edn').write_text(dumps(qids))
(H/'old-field-ids.edn').write_text(dumps(oldfields))
(H/'old-answer-ids.edn').write_text(dumps(oldanswers))
(H/'item-ids.edn').write_text(dumps([i[':db/id'] for i in items]))
(H/'all-pattern.edn').write_text('[*]')
print(json.dumps(dict(basis=basis,questions=len(plan),fields=len(new_field_ids),answers=len(new_answer_ids),saved_attempts=len(response_migrations),forms=len(forms))))
