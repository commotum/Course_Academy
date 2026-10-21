"""Compare choice grading before/after; report preexisting unkeyed fields honestly."""
import copy, json, subprocess
from snapshot import *
GRADER=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/check-checkbox-engine'
FIELD='[* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]'
def capture():
    snapshot=Path((HERE/'snapshot-directory.txt').read_text().strip());identity=json.loads((snapshot/'identity.json').read_text())
    answers=json.loads((snapshot/'answer-ownership/answers.json').read_text());ids=set()
    for a in answers:
        fields=a.get(':answer-field/_choices',[])
        if isinstance(fields,dict):fields=[fields]
        ids.update(f[':db/id'] for f in fields)
    out=snapshot/'fields';out.mkdir(exist_ok=True);(out/'native-pulls.edn').write_text(dumps([['fields',FIELD,sorted(ids)]])+'\n')
    db=Publisher.from_environment(source=SOURCE).client
    run=subprocess.run([str(READ),str(out),str(identity['basis'])],env=db.environment,capture_output=True,text=True,timeout=180)
    (out/'read.stderr').write_text(run.stderr);run.check_returncode();save(out/'fields.json',loads((out/'fields.edn').read_text()));print(run.stdout)
def check():
    data=json.loads((HERE/'integrated-changes.json').read_text());snapshot=Path(data['snapshot']);fields=json.loads((snapshot/'fields/fields.json').read_text())
    changes={c['entity']:c for c in data['changes'] if c['attribute']==':answer/value'}
    tests=[];unkeyed=[];checked=[];duplicates=[]
    for f in fields:
        ids={a[':db/id'] for a in f.get(':answer-field/choices',[])}
        if not ids.intersection(changes):continue
        before=copy.deepcopy(f);after=copy.deepcopy(f)
        for a in after[':answer-field/choices']:
            if a[':db/id'] in changes:
                c=changes[a[':db/id']];assert a[':answer/value']==c['before'];a[':answer/value']=c['after']
        def duplicate_pairs(field):
            bank=field[':answer-field/choices'];return {(a[':db/id'],b[':db/id']) for i,a in enumerate(bank) for b in bank[i+1:] if a[':answer/type']==b[':answer/type'] and a[':answer/value']==b[':answer/value']}
        new_duplicates=duplicate_pairs(after)-duplicate_pairs(before)
        if new_duplicates:duplicates.append({'field':f[':db/id'],'pairs':list(new_duplicates)})
        if not f.get(':answer-field/correct'):
            unkeyed.append(f[':db/id']);continue
        checked.append(f[':db/id'])
        for stage,field in [('before',before),('after',after)]:
            correct=str(field[':answer-field/correct'][':answer/id'])
            qfield={':answer-field/id':str(field[':answer-field/id']),':answer-field/key':field[':answer-field/key'],':answer-field/type':field[':answer-field/type'][':db/ident'],
                ':answer-field/correct':[':answer/id',correct],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in field[':answer-field/choices']]}
            checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Preserved choice identity and canonical membership'} for a in qfield[':answer-field/choices']]
            tests.append({'label':f"{f[':db/id']}-{stage}",'record':{'question':{':question/problem':'Choose the answer.',':question/answer-fields':[qfield]},'knowledge_point':{'title':'Original import restoration'},'generation':{'template':'original-source-bulk'}},'checks':checks,'mapped_responses':[]})
    out=HERE/'grading';out.mkdir(exist_ok=True);save(out/'input.json',tests)
    assert not duplicates,('Restoration creates indistinguishable choice values',duplicates)
    if tests:subprocess.run([str(GRADER),str(out/'input.json'),str(out/'native-report.json')],check=True)
    result={'passed':True,'input_sha256':hashlib.sha256((HERE/'integrated-changes.json').read_bytes()).hexdigest(),'keyed_fields_graded_before_and_after':checked,
        'preexisting_unkeyed_fields_preserved':unkeyed,'new_duplicate_choice_pairs':duplicates,'keyed_field_count':len(checked),'preexisting_unkeyed_field_count':len(unkeyed)}
    save(out/'verification.json',result);print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},indent=2))
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('action',choices=['capture','check']);args=p.parse_args();globals()[args.action]()
