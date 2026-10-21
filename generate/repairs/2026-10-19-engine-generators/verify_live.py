"""Verify four scoped registrations and read-only grading after publication."""
from pathlib import Path
import json
import sys
import urllib.request
import uuid

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher
from capture.scripts.database.client import QUESTION_PULL

TOPICS={17592186096617:17592186048813,17592186096618:17592186048813,
        17592186092261:17592186050271,17592186096842:17592186051084}


def preview(body):
    request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',
        data=json.dumps(body).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'})
    return json.load(urllib.request.urlopen(request,timeout=45))


def main():
    publisher=Publisher.from_environment();client=publisher.client
    states={kp:json.loads((HERE/str(kp)/'job.json').read_text()) for kp in TOPICS}
    assert all(s['stage']=='verified' and s.get('approval_recorded') for s in states.values())
    identity=client.status();directory=HERE/'final-live';directory.mkdir(exist_ok=True)
    rows=client.query('[:find (pull ?kp [:db/id :knowledge-point/title {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',
        [list(TOPICS)],directory,'registrations',identity['basis'])
    registered={kp[':db/id']:kp for [kp] in rows}
    for kp,state in states.items():
        assert registered[kp][':knowledge-point/question-generator'][':question-generator/script']==state['registration']
    sample_ids={}
    for kp in TOPICS:
        prep=json.loads((HERE/str(kp)/'publication/preparation.json').read_text())
        sample_ids[kp]=prep['records'][0]['question'][':question/id']
    rows=client.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?id ...] :where [?q :question/id ?id]]',
        [[uuid.UUID(str(qid)) for qid in sample_ids.values()]],directory,'published-questions',identity['basis'])
    questions={str(q[':question/id']):q for [q] in rows}
    results=[]
    for kp,topic in TOPICS.items():
        q=questions[str(sample_ids[kp])];field,=q[':question/answer-fields'];correct=field[':answer-field/correct']
        kind=field[':answer-field/type'][':db/ident']
        if kind==':answer-field.type/blank':
            responses=[({'fieldId':field[':db/id'],'value':correct[':answer/value']},'correct'),
                       ({'fieldId':field[':db/id'],'value':'('+correct[':answer/value']+')*2/2'},'correct'),
                       ({'fieldId':field[':db/id'],'value':'0'},'incorrect')]
        else:
            wrong=next(a for a in field[':answer-field/choices'] if a[':db/id']!=correct[':db/id'])
            responses=[({'fieldId':field[':db/id'],'choiceId':correct[':db/id']},'correct'),
                       ({'fieldId':field[':db/id'],'choiceId':wrong[':db/id']},'incorrect')]
        checks=[]
        for response,expected in responses:
            result=preview({'topicId':topic,'questionId':q[':db/id'],'responses':[response]})
            assert result['status']==expected
            checks.append({'expected':expected,'actual':result['status'],'basis':result['basis']})
        availability=json.load(urllib.request.urlopen(f'http://127.0.0.1:8765/api/topic-study-availability?topicId={topic}',timeout=45))
        assert availability['available']
        results.append({'topic':topic,'kp':kp,'registration':states[kp]['registration'],
                        'publication_basis':states[kp]['publication']['basis_after'],
                        'sample_question':q[':db/id'],'live_grading':checks,'availability':availability})
    disabled='COURSE_ACADEMY_DISABLE_GENERATION=1' in (ROOT/'.local/ui.env').read_text().splitlines()
    assert disabled
    source_regressions=[]
    source_checks=[
        (17592186096617,'q-310188',r'3^x*ln(9)*sin(x)/2'),
        (17592186096618,'q-320815',r'4^x/(2x*ln(2))'),
        (17592186092261,'q-312462',r'3x^2*ln(25)/2'),
        (17592186096842,'q-342764',r'-5/(2sqrt((5x+1)^3))'),
    ]
    for kp,ma,equivalent in source_checks:
        source=json.loads((HERE/str(kp)/'source/source.json').read_text())
        question=next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']==ma)
        field,=question[':question/answer-fields']
        checks=[]
        for value,expected in [(equivalent,'correct'),('0','incorrect')]:
            result=preview({'topicId':TOPICS[kp],'questionId':question[':db/id'],
                'responses':[{'fieldId':field[':db/id'],'value':value}]})
            assert result['status']==expected,(ma,value,result)
            checks.append({'submitted':value,'expected':expected,'actual':result['status'],'basis':result['basis']})
        source_regressions.append({'kp':kp,'ma_id':ma,'question':question[':db/id'],'checks':checks})
    result={'verified':True,'identity':identity,'generator_publications':results,
            'live_source_regressions':source_regressions,
            'automatic_generation_disabled':disabled,'learner_attempts_created_by_verification':0}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
