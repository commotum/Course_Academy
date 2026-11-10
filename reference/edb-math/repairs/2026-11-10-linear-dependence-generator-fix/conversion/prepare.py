"""Prepare independently reviewed statement-subset questions as checkboxes."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

H=Path(__file__).resolve().parent
ROOT=H.parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,dumps,kw
from question_capture.core import stable_id

db=connection();basis=db.basis()
def save(name,value):(H/(name+'.json')).write_text(json.dumps(value,default=str,indent=2)+'\n')
def query(text,inputs,name):
    r=db.query(text,inputs,H,name,basis);save(name,r);return r
def many(v):return [v] if isinstance(v,dict) else v
assert not (H/'commit-intent.json').exists(),'Reconcile existing exact request first.'
save('basis',dict(basis=basis));(H/'database-status.txt').write_text(db.command('status'))
topicrows=query((H/'topic-before-query.edn').read_text(),[17592186050426],'topic-before')
topic=topicrows[0][0]
questions={};memberships={}
for kp in topic[':topic/knowledge-points']:
    for q in kp.get(':knowledge-point/questions',[])+([kp[':knowledge-point/canonical-example']] if kp.get(':knowledge-point/canonical-example') else []):
        questions[q[':db/id']]=q;memberships.setdefault(q[':db/id'],[]).append(kp[':db/id'])
save('questions-before',list(questions.values()))
all_resolved=json.loads((H/'resolutions.json').read_text())
resolved=[r for r in all_resolved if r['decision']=='convert']
ids=[r['entity'] for r in resolved]
targets=[questions[i] for i in ids]
save('targets-before',targets)
assert 17592186707100 in ids
for q in questions.values():
    if any(f[':answer-field/type'][':db/ident']==':answer-field.type/radio' for f in q.get(':question/answer-fields',[])) and re.search(r'(?m)^I\. ',q[':question/problem']):
        assert q[':db/id'] in {r['entity'] for r in all_resolved},'New candidate requires independent mathematical review.'
source=query('[:find ?e :in $ ?ident :where [?e :db/ident ?ident]]',[kw('agent/codex')],'contributor')
assert len(source)==1
query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],'attribute-idents')
query('[:find (pull ?q [:db/id {[:knowledge-point/_questions :limit nil] [:db/id]} {[:knowledge-point/_canonical-example :limit nil] [:db/id]} {[:task-item/_content :limit nil] [*]}]) :in $ [?q ...] :where [?q :question/id _]]',[ids],'incoming-before')
incoming=json.loads((H/'incoming-before.json').read_text())
items={i[':db/id']:i for row in incoming for i in many(row[0].get(':task-item/_content',[]))}
save('presentations-before',[[i] for i in items.values()])
oldfields=[f[':db/id'] for q in targets for f in q[':question/answer-fields']]
oldanswers=[a[':db/id'] for q in targets for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
fieldrows=query('[:find (pull ?e [* {[:question/_answer-fields :limit nil] [:db/id]}]) :in $ [?e ...] :where [?e :answer-field/id _]]',[oldfields],'old-fields-with-uses')
assert {q[':db/id'] for row in fieldrows for q in many(row[0].get(':question/_answer-fields',[]))}<=set(ids)
answerrows=query('[:find (pull ?e [* {[:task-item/_responses :limit nil] [:db/id]}]) :in $ [?e ...] :where [?e :answer/id _]]',[oldanswers],'old-answers-with-uses')
assert {i[':db/id'] for row in answerrows for i in many(row[0].get(':task-item/_responses',[]))}<=set(items),'Response outside scoped questions'
for label,rows,reverse in [('old-fields',fieldrows,':question/_answer-fields'),('old-answers',answerrows,':task-item/_responses')]:
    clean=copy.deepcopy(rows)
    for row in clean:row[0].pop(reverse,None)
    save(label+'-before',clean)

forms=[];cases=[];plans=[];newfields=[];newanswers=[];response_map={}
for q in targets:
    resolution=next(r for r in resolved if r['entity']==q[':db/id'])
    matches=list(re.finditer(r'(?m)^(I|II|III)\.\s+(.*?)(?=\n\n(?:II|III)\. |\n\nChoose the correct combination\.|\Z)',q[':question/problem'],re.S))
    assert [(m[1],m[2].strip()) for m in matches]==[(o['label'],o['content']) for o in resolution['objects']],'Source statements changed since independent review'
    assert len(q[':question/answer-fields'])==1
    oldfield=q[':question/answer-fields'][0]
    assert oldfield[':answer-field/type'][':db/ident']==':answer-field.type/radio'
    assert oldfield[':answer-field/correct'][':answer/value']==resolution['source_key']
    assert oldfield[':answer-field/correct'][':db/id'] in {a[':db/id'] for a in oldfield[':answer-field/choices']}
    labelcontent={o['label']:o['content'] for o in resolution['objects']}
    oldsolution=q[':question/worked-solution']
    def replace_refs(m):
        labels=re.findall(r'\b(?:III|II|I)\b',m[1])
        text=('the statement ' if len(labels)==1 else 'the statements ')+ ' and '.join('“'+labelcontent[l]+'”' for l in labels)
        return text[0].upper()+text[1:] if m[0][0].isupper() else text
    solution=re.sub(r'\b[Ss]tatements?\s+((?:III|II|I)(?:\s*(?:,|and)\s*(?:III|II|I))*)',replace_refs,oldsolution)
    solution=re.sub(r'\b(III|II|I) is\b',lambda m:'The statement “'+labelcontent[m[1]]+'” is',solution)
    solution=re.sub(r'(?m)^Therefore, the correct answer is .*$', 'Select exactly the statements shown to be true above.',solution)
    solution=re.sub(r'\s*Choose [“"][^”"]+[”"]\.?','',solution)
    assert not re.search(r'\b(?:Statement|statement)\s+(?:III|II|I)\b|[“"](?:III|II|I)(?: only| and)',solution)
    problem=q[':question/problem'][:matches[0].start()].rstrip()+'\n\nSelect all that apply. If none apply, leave all boxes unchecked.'
    keytoken=q.get(':question/math-academy-id') or str(q[':question/id'])
    fields=[];objects=[];mapping=[]
    for obj in resolution['objects']:
        label=obj['label'];token=keytoken+'/authored-checkbox-v1/'+label;tempid=str(q[':db/id'])+'-'+label
        fid=stable_id('field',token);newfields.append(fid);bank=[]
        for boolean in ('false','true'):
            aid=stable_id('answer',token+'/'+boolean);newanswers.append(aid);atemp=tempid+'-'+boolean
            forms.append({kw('db/id'):atemp,kw('answer/id'):aid,kw('answer/type'):kw('answer.type/text'),kw('answer/value'):boolean})
            forms.append([kw('db/ensure'),atemp,kw('answer/validate')])
            bank.append({':db/id':atemp,':answer/id':str(aid),':answer/type':{':db/ident':':answer.type/text'},':answer/value':boolean})
        correct=tempid+'-'+str(obj['truth']).lower()
        forms.append({kw('db/id'):tempid,kw('answer-field/id'):fid,kw('answer-field/key'):obj['content'],kw('answer-field/type'):kw('answer-field.type/checkbox'),kw('answer-field/choices'):[a[':db/id'] for a in bank],kw('answer-field/correct'):correct})
        forms += [[kw('db/ensure'),tempid,kw('answer-field/validate')],[kw('db/add'),q[':db/id'],kw('question/answer-fields'),tempid]]
        fields.append({':db/id':tempid,':answer-field/id':str(fid),':answer-field/key':obj['content'],':answer-field/type':{':db/ident':':answer-field.type/checkbox'},':answer-field/choices':bank,':answer-field/correct':next(a for a in bank if a[':db/id']==correct)})
        objects.append(dict(source_label=label,field_id=str(fid),content=obj['content'],source_fragment=obj['source_fragment']))
    for a in oldfield[':answer-field/choices']:
        value=a[':answer/value'];selected=[] if value.lower().startswith('none') else re.findall(r'\b(?:III|II|I)\b',value)
        assert selected or value.lower().startswith('none'),value
        assert len(selected)==len(set(selected)) and set(selected)<=set(labelcontent)
        newids=[str(stable_id('answer',keytoken+'/authored-checkbox-v1/'+o['label']+'/'+str(o['label'] in selected).lower())) for o in resolution['objects']]
        tempids=[str(q[':db/id'])+'-'+o['label']+'-'+str(o['label'] in selected).lower() for o in resolution['objects']]
        mapping.append(dict(old_answer=a[':db/id'],old_value=value,selected=selected,new_answers=newids,new_tempids=tempids,correct=a[':db/id']==oldfield[':answer-field/correct'][':db/id']))
        assert (set(selected)==set(resolution['correct']))==(a[':db/id']==oldfield[':answer-field/correct'][':db/id'])
        response_map[a[':db/id']]=mapping[-1]
    forms += [[kw('db/retract'),q[':db/id'],kw('question/answer-fields'),oldfield[':db/id']],
      [kw('db/cas'),q[':db/id'],kw('question/problem'),q[':question/problem'],problem],
      [kw('db/cas'),q[':db/id'],kw('question/worked-solution'),oldsolution,solution],[kw('db/ensure'),q[':db/id'],kw('question/validate')]]
    proposed=copy.deepcopy(q);proposed[':question/problem']=problem;proposed[':question/worked-solution']=solution;proposed[':question/answer-fields']=fields
    cases.append(dict(question=proposed,objects=objects))
    plans.append(dict(entity=q[':db/id'],ma_id=q.get(':question/math-academy-id'),question_uuid=str(q[':question/id']),kp_ids=memberships[q[':db/id']],objects=objects,correct=resolution['correct'],choice_mapping=mapping,proof=resolution))

response_migrations=[]
for item in items.values():
    old=[a[':db/id'] for a in item.get(':task-item/responses',[])]
    assert len(old)<=1,'Multiple selected old radio answers require investigation'
    for answer in old:
        assert answer in response_map
        mapping=response_map[answer]
        forms.append([kw('db/retract'),item[':db/id'],kw('task-item/responses'),answer])
        for aid in mapping['new_tempids']:forms.append([kw('db/add'),item[':db/id'],kw('task-item/responses'),aid])
        forms.append([kw('db/ensure'),item[':db/id'],kw('task-item/validate')])
        response_migrations.append(dict(item=item[':db/id'],before=old,after=mapping['new_answers'],selected=mapping['selected']))
for attr,values in [('answer-field/id',newfields),('answer/id',newanswers)]:
    assert not query('[:find ?e ?v :in $ [?v ...] :where [?e :'+attr+' ?v]]',[values],'new-'+attr.split('/')[0]+'-identity-check')
save('plan',dict(basis=basis,source=':agent/codex',source_entity=source[0][0],topic=17592186050426,questions=plans,response_migrations=response_migrations))
save('proposed-presentation',dict(cases=cases));(H/'transaction.edn').write_text(dumps(forms)+'\n')
pattern='[* {:question/difficulty [:db/id :db/ident]} {[:knowledge-point/_questions :limit nil] [:db/id]} {[:knowledge-point/_canonical-example :limit nil] [:db/id]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'
(H/'question-pattern.edn').write_text(pattern)
for name,value in [('question-ids',ids),('old-field-ids',oldfields),('old-answer-ids',oldanswers),('item-ids',list(items))]:
    (H/(name+'.edn')).write_text(dumps(value))
(H/'all-pattern.edn').write_text('[*]')
print(json.dumps(dict(basis=basis,questions=len(plans),fields=len(newfields),answers=len(newanswers),saved_attempts=len(response_migrations),presentations=len(items),forms=len(forms))))
