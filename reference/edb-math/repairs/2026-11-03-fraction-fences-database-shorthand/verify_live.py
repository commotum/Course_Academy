"""Compare real grading before/after without creating learner attempts."""
import json,sys,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable,QUESTION_PULL

def grade_signature(check):
    result=check['result']
    return {'question':check['question'],'variant':check['variant'],'status':result.get('status'),'fields':sorted((f['id'],f.get('grade')) for f in result.get('fields',[])),'http_status':result.get('http_status')}

def main():
    before='--before' in sys.argv;p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];sample=json.loads((H/'live-samples.json').read_text());old={r[0][':db/id']:r[0] for r in sample['questions']};topics=dict(sample['topics']);proposals=json.loads((H/'proposals.json').read_text());planned={(r['entity'],':'+r['attribute']):r['after'] for r in proposals}
    current=old if before else {r[0][':db/id']:jsonable(r[0]) for r in p.client.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[sorted(old)],H/'live','questions-after',basis)}
    checks=[];skipped=[]
    for eid,q in sorted(current.items()):
        if eid not in topics:skipped.append({'question':eid,'reason':'No topic owner'});continue
        fields=q.get(':question/answer-fields',[])
        if not fields or any(not f.get(':answer-field/correct') for f in fields):skipped.append({'question':eid,'reason':'Incomplete imported key'});continue
        if not before:
            for key in (':question/problem',':question/worked-solution'):
                if key in old[eid]:assert q.get(key)==planned.get((eid,key),old[eid][key])
            oldfields={f[':db/id']:f for f in old[eid][':question/answer-fields']}
            for f in fields:
                original=oldfields[f[':db/id']];assert f[':answer-field/correct'][':db/id']==original[':answer-field/correct'][':db/id']
                answers={a[':db/id']:a for a in f[':answer-field/choices']}
                for a in original[':answer-field/choices']:assert answers[a[':db/id']][':answer/value']==planned.get((a[':db/id'],':answer/value'),a[':answer/value'])
        correct=[]
        for f in fields:
            kind=f[':answer-field/type'][':db/ident'];a=f[':answer-field/correct'];row={'fieldId':f[':db/id']}
            if kind in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox'):row['choiceId']=a[':db/id']
            else:row['value']=a[':answer/value']
            correct.append(row)
        variants=[(correct,'key')]
        for i,f in enumerate(fields):
            if f[':answer-field/type'][':db/ident'] not in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox'):continue
            for a in f[':answer-field/choices']:
                if a[':db/id']==f[':answer-field/correct'][':db/id']:continue
                wrong=[dict(r) for r in correct];wrong[i]['choiceId']=a[':db/id'];variants.append((wrong,'alternative-'+str(f[':db/id'])+'-'+str(a[':db/id'])))
        for responses,label in variants:
            payload={'topicId':topics[eid],'questionId':eid,'responses':responses};req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
            try:
                with urllib.request.urlopen(req,timeout=45) as response:result=json.load(response)
            except urllib.error.HTTPError as error:result={'http_status':error.code,'body':error.read().decode()}
            checks.append({'question':eid,'variant':label,'result':result})
    if not before:
        previous=json.loads((H/'live-before.json').read_text())
        expected=[grade_signature(c) for c in previous['checks']];actual=[grade_signature(c) for c in checks]
        assert expected==actual,[(b,a) for b,a in zip(expected,actual) if b!=a]
    result={'passed':True,'basis':basis,'checks':checks,'live_grading_checks':len(checks),'questions_checked':len({r['question'] for r in checks}),'partial_imports_preserved':skipped,'database_writes':0,'grading_unchanged':not before}
    (H/('live-before.json' if before else 'live-verification.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))

if __name__=='__main__':main()
