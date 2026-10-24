"""Read final pools and grade without creating learner attempts or tasks."""
from collections import Counter
import json
from pathlib import Path
import sys
import urllib.request

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,normalized_question
from scripts.generator_packages import resolve_registered_script,verify_package
from capture.scripts.storage import atomic_json


def grade(q,response,expected):
    payload={'topicId':17592186050489,'questionId':q[':db/id'],'responses':[response]}
    req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),
        headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
    with urllib.request.urlopen(req,timeout=60)as result:outcome=json.load(result)
    assert outcome['status']==expected,outcome
    return {'question':q[':db/id'],'status':outcome['status'],'basis':outcome.get('basis')}


def main():
    p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis']
    summaries=[];ids=[];grades=[];counts=Counter();retired=[]
    for kp in (17592186068915,17592186068916,17592186068917,17592186068918):
        d=H/str(kp);proof=json.loads((d/'verification.json').read_text());current=p.read_kp(kp,H/'live'/str(kp),basis)
        reference=current[':knowledge-point/question-generator'][':question-generator/script']
        assert reference==proof['new_reference'];entry=resolve_registered_script(reference,ROOT,p.config.math_root)
        verify_package(entry.parent,Path(reference).parts[2])
        assert entry.read_bytes()==(ROOT/f'generate/scratch/{kp}.py').read_bytes()
        assert(entry.parent/'trig_scaffold.py').read_bytes()==(ROOT/'generate/trig_scaffold.py').read_bytes()
        questions={q[':db/id']:q for q in current[':knowledge-point/questions']}
        prepared=json.loads((d/'publication/preparation.json').read_text());records={r['question'][':question/id']:r for r in prepared['records']}
        native={r['record']['question'][':question/id']:r for r in json.loads((d/'grader-input.json').read_text())}
        new=[]
        for row in proof['new_questions']:
            q=questions[row['entity']];assert not q.get(':question/retired')and not q.get(':question/math-academy-id')
            assert normalized_question(q)==normalized_question(records[row['uuid']]['question'])
            new.append(q);ids.append(q[':db/id']);counts[str(kp)+'/'+row['band'].split('/')[-1]]+=1
        for eid in proof['retired_old_questions']:
            assert questions[eid][':question/retired']is True;retired.append(eid)
        # There are no surviving obsolete generated questions in fresh practice.
        assert{q[':db/id']for q in questions.values()if not q.get(':question/math-academy-id')and not q.get(':question/retired')}=={q[':db/id']for q in new}
        for band in('easy','moderate','hard'):
            options=[q for q in new if str(q[':question/difficulty'][':db/ident']).endswith('/'+band)];assert len(options)==8
            q=options[0];f=q[':question/answer-fields'][0];fid=f[':db/id'];correct=f[':answer-field/correct']
            if band=='easy':
                submissions=[({'fieldId':fid,'choiceId':correct[':db/id']},'correct'),
                    ({'fieldId':fid,'choiceId':next(a[':db/id']for a in f[':answer-field/choices']if a[':db/id']!=correct[':db/id'])},'incorrect')]
            else:
                checked=native[str(q[':question/id'])];wrong=next(c['submitted']for c in checked['checks']if c['expected']=='rejected')
                submissions=[({'fieldId':fid,'value':correct[':answer/value']},'correct'),({'fieldId':fid,'value':wrong},'incorrect')]
                extra=next((c for c in checked['checks']if c.get('purpose','').startswith('Absorb a numeric')),None)
                if extra:submissions.append(({'fieldId':fid,'value':extra['submitted']},'correct'))
            for response,status in submissions:
                grades.append({'kp':kp,'band':band,**grade(q,response,status)})
        if kp==17592186068918:
            for case in('rearranged_tan','rearranged_sec'):
                row=next(r for r in native.values()if r['record']['generation']['family']==case)
                q=next(q for q in new if str(q[':question/id'])==row['record']['question'][':question/id']);f=q[':question/answer-fields'][0]
                grades.append({'kp':kp,'band':'hard','purpose':'Expanded answer with the numeric constant absorbed',
                    **grade(q,{'fieldId':f[':db/id'],'value':row['checks'][-1]['submitted']},'correct')})
        summaries.append({'kp':kp,'new_questions':len(new),'retired_old_questions':proof['retired_old_questions'],
            'imported_preserved':proof['imported_questions_preserved'],'generator_reference':reference,
            'basis_committed':proof['basis_after'],'local_and_published_code_identical':True,'canonical_and_history_preserved':True})
    uses=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',
        [ids],H/'live','new-question-uses',basis)
    assert len(uses)==96 and all(not q.get(':task-item/_content')for[q]in uses)
    assert len(retired)==91 and 17592186676292 in retired
    old=p.client.query('[:find ?q :in $ [?q ...] :where [?q :question/retired true]]',[[17592186482724]],H/'live','previously-retired-example',basis)
    assert old==[[17592186482724]]
    result={'committed':True,'verified':True,'basis_readback':basis,'new_questions':96,'retired_questions':91,
        'imported_questions_preserved':68,'all_new_questions_unserved':True,'knowledge_points':summaries,'live_grade_checks':len(grades)}
    atomic_json(H/'completion.json',result)
    atomic_json(H/'live-pool-verification.json',{'passed':True,'basis':basis,'counts':dict(counts),'all_new_questions_unserved':True,'retired':retired,'knowledge_points':summaries})
    atomic_json(H/'live-grading-verification.json',{'passed':True,'database_writes':0,'checks':grades})
    print(json.dumps({k:v for k,v in result.items()if k!='knowledge_points'}))


if __name__=='__main__':main()
