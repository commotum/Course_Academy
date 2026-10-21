"""Read-only verification of urgent publication and live learner grading."""
import json
from pathlib import Path
import sys
import urllib.request
import urllib.error
import uuid

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher, QUESTION_PULL

TOPIC=17592186050321
KPS=[17592186184153,17592186184154,17592186184155]


def preview(question,field,value,expected,choice=False):
    response={'fieldId':field[':db/id'],'choiceId' if choice else 'value':value}
    request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',
        data=json.dumps({'topicId':TOPIC,'questionId':question[':db/id'],'responses':[response]}).encode(),
        headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'})
    try:
        with urllib.request.urlopen(request,timeout=45) as stream:result=json.load(stream)
    except urllib.error.HTTPError as error:
        raise AssertionError((question[':db/id'],value,error.code,error.read().decode())) from error
    assert result['status']==expected,(question[':db/id'],value,result)
    return {'expected':expected,'actual':result['status'],'basis':result['basis']}


def main():
    publisher=Publisher.from_environment();client=publisher.client
    identity=client.status();directory=HERE/'final-live';directory.mkdir(exist_ok=True)
    states={kp:json.loads((HERE/'jobs'/str(kp)/'job.json').read_text()) for kp in KPS}
    assert all(s['stage']=='verified' and s.get('approval_recorded') and s['publication']['passed'] for s in states.values())
    rows=client.query('[:find (pull ?kp [:db/id {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',
        [KPS],directory,'registrations',identity['basis'])
    registrations={q[':db/id']:q[':knowledge-point/question-generator'][':question-generator/script'] for [q] in rows}
    for kp in KPS:assert registrations[kp]==states[kp]['registration']
    ids=[]
    for kp in KPS:
        preparation=json.loads((HERE/'jobs'/str(kp)/'publication/preparation.json').read_text())
        ids.extend(uuid.UUID(r['question'][':question/id']) for r in preparation['records'])
    rows=client.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?id ...] :where [?q :question/id ?id]]',
        [ids],directory,'published-questions',identity['basis'])
    assert len(rows)==15
    checks=[]
    for [question] in rows:
        field,=question[':question/answer-fields'];correct=field[':answer-field/correct']
        if field[':answer-field/type'][':db/ident']==':answer-field.type/blank':
            checks.append(preview(question,field,correct[':answer/value'],'correct'))
            checks.append(preview(question,field,'0','incorrect'))
            if 'antiderivative' in question[':question/problem'].lower() and '+\\,C' in question[':question/problem']:
                checks.append(preview(question,field,'('+correct[':answer/value']+')+1','correct'))
        else:
            wrong=next(a for a in field[':answer-field/choices'] if a[':db/id']!=correct[':db/id'])
            checks.append(preview(question,field,correct[':db/id'],'correct',True))
            checks.append(preview(question,field,wrong[':db/id'],'incorrect',True))
    with urllib.request.urlopen(f'http://127.0.0.1:8765/api/topic-study-availability?topicId={TOPIC}',timeout=45) as stream:
        availability=json.load(stream)
    assert availability['available']
    result={'passed':True,'read_only':True,'identity':identity,'topic':TOPIC,'availability':availability,
        'registered_generators':registrations,'published_questions':len(rows),'live_grading_checks':checks,
        'general_creation_disabled':'COURSE_ACADEMY_DISABLE_GENERATION=1' in (ROOT/'.local/ui.env').read_text().splitlines()}
    (HERE/'completion-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'generators':3,'published_questions':15,'live_grading_checks':len(checks),'study_available':True,'basis':availability['basis']}))


if __name__=='__main__':main()
