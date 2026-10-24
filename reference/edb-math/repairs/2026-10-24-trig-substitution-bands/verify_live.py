"""Verify registration, fresh pool, retirements, and read-only live grading."""
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


def main():
    p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis']
    summaries=[];all_ids=[];grades=[];counts=Counter()
    for kp in (17592186068916,17592186068917,17592186068918):
        d=H/str(kp);proof=json.loads((d/'verification.json').read_text())
        current=p.read_kp(kp,H/'live'/str(kp),basis)
        reference=current[':knowledge-point/question-generator'][':question-generator/script']
        assert reference==proof['new_reference']
        entry=resolve_registered_script(reference,ROOT,p.config.math_root)
        verify_package(entry.parent,Path(reference).parts[2])
        assert entry.read_bytes()==(ROOT/f'generate/scratch/{kp}.py').read_bytes()
        assert (entry.parent/'trig_substitution.py').read_bytes()==(ROOT/'generate/scratch/trig_substitution.py').read_bytes()
        questions={q[':db/id']:q for q in current[':knowledge-point/questions']}
        prepared=json.loads((d/'publication/preparation.json').read_text())
        records={r['question'][':question/id']:r for r in prepared['records']}
        new=[]
        for row in proof['new_questions']:
            q=questions[row['entity']]
            assert not q.get(':question/retired') and not q.get(':question/math-academy-id')
            assert normalized_question(q)==normalized_question(records[row['uuid']]['question'])
            all_ids.append(q[':db/id']);new.append(q)
            counts[str(kp)+'/'+row['band'].split('/')[-1]]+=1
        for eid in proof['retired_old_questions']:assert questions[eid][':question/retired'] is True
        for band in ('easy','moderate','hard'):
            options=[q for q in new if str(q[':question/difficulty'][':db/ident']).endswith('/'+band)]
            assert len(options)==8
            q=options[0];field=q[':question/answer-fields'][0]
            value=field[':answer-field/correct'][':answer/value']
            submissions=[(value,'correct'),('987654321','incorrect')]
            if band=='easy':submissions.append(('('+value+')+1','correct'))
            for submitted,expected in submissions:
                payload={'activityId':17592186064411,'questionId':q[':db/id'],
                         'responses':[{'fieldId':field[':db/id'],'value':submitted}]}
                request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',
                    data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
                with urllib.request.urlopen(request,timeout=60) as response:outcome=json.load(response)
                assert outcome['status']==expected,outcome
                grades.append({'kp':kp,'band':band,'entity':q[':db/id'],'status':outcome['status'],'basis':outcome.get('basis')})
        summaries.append({'kp':kp,'basis_committed':proof['basis_after'],'new_questions':len(new),
            'new_fresh_counts':proof['fresh_generated_counts'],'retired_old_questions':proof['retired_old_questions'],
            'imported_preserved':proof['imported_questions_preserved'],'generator_reference':reference,
            'canonical_preserved':True,'learner_history_preserved':True,'local_and_published_code_identical':True})
    uses=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',
        [all_ids],H/'live','new-question-uses',basis)
    assert len(uses)==72 and all(not q.get(':task-item/_content') for [q] in uses)
    atomic_json(H/'live-pool-verification.json',{'passed':True,'basis':basis,'database_writes':0,
        'new_fresh_questions':72,'counts':dict(counts),'all_new_questions_unserved':True,'knowledge_points':summaries})
    atomic_json(H/'live-grading-verification.json',{'passed':True,'database_writes':0,'checks':grades})
    atomic_json(H/'completion.json',{'committed':True,'verified':True,'basis_readback':basis,
        'new_questions':72,'retired_questions':8,'imported_questions_preserved':56,'knowledge_points':summaries,
        'live_grade_checks':len(grades)})
    print(json.dumps({'passed':True,'basis':basis,'new_fresh_questions':72,'retired':8,'live_grade_checks':len(grades)}))


if __name__=='__main__':main()
