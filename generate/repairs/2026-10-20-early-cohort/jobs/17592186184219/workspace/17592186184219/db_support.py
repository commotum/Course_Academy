"""Scoped representations and additive forms using the established EDB schema."""
import copy,uuid
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import kw
KP=17592186184219
SCRIPT='generate/scratch/17592186184219.py'
DB=None

def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def scoped(kp,b,seen):
    entities={};enums={};next_enum=1
    def enum(value):
        nonlocal next_enum
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            enums[name]=next_enum;entities[str(next_enum)]={'db/ident':name};next_enum+=1
        return enums[name]
    def question(q):
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]}
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        entities[str(q[':db/id'])]=r
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id'])
            field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]}
            if ':answer-field/correct' in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            entities[str(f[':db/id'])]=field
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:question(q)
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name
