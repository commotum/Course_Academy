"""Atomically register, refresh all bands, and retire the old generated pool."""
from collections import Counter
import json
from pathlib import Path
import platform
import subprocess
import sys

import sympy

BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];H=BASE;MATH=Path('/media/jake/SSD/EDB/math')
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,normalized_question,jsonable
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,materialize_package,verify_package
from capture.scripts.storage import atomic_json

DIRECTORY=None
KP=None


def save(name,value):atomic_json(H/name,value)


def prepare(publisher):
    review=json.loads((H/'generator-verification.json').read_text())
    assert review['pool_counts']=={':question.difficulty/easy':8,':question.difficulty/moderate':8,':question.difficulty/hard':8}
    grader=json.loads((H/'grader-verification.json').read_text());assert grader['documented_unresolved_checks']==0
    assert json.loads((BASE/'render/rendering.json').read_text())['passed']
    records=json.loads((H/'candidate-pool.json').read_text())
    manifest=build_manifest(H/'package','generator.py',['generator.py','substitution_pedagogy.py','source-evidence.json','band-contract.json'],
        dependencies={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}})
    package=publish_package(H/'package',manifest['entrypoint'],manifest['files'],MATH,
        dependencies=manifest['dependencies'],expected_digest=manifest_digest(manifest))
    runtime=H/'deployed-runtime'/package.digest
    if runtime.exists():verify_package(runtime,package.digest);entry=runtime/'generator.py'
    else:entry=materialize_package(package.reference,MATH,runtime)
    reproduced=[]
    for band,count in [('easy',8),('moderate',8),('hard',8)]:
        output=subprocess.run([sys.executable,str(entry),'--difficulty',band,'--count',str(count),'--seed','20261024','--format','json'],
            check=True,capture_output=True,text=True,timeout=60)
        reproduced.extend(json.loads(output.stdout))
    assert reproduced==records,'Published relocation changed the approved records'
    save('package-verification.json',{'digest':package.digest,'reference':package.reference,'manifest':manifest,
        'relocated_records_identical':len(records)})
    source=json.loads((H/'source/source.json').read_text())
    prepared=publisher.prepare(KP,records,package.reference,package.digest,DIRECTORY,
        source_snapshot=source,assets_directory=H/'package',expected_registered_generator=(source.get('registered_generator') or {}).get(':question-generator/script'))
    assert prepared['new_questions']==24 and prepared['duplicates']==0
    before=loads(prepared['before_edn'])
    actual=(before.get(':knowledge-point/question-generator') or {}).get(':question-generator/script')
    initial=(source.get('registered_generator') or {}).get(':question-generator/script')
    assert actual==initial,'Generator registration changed since review'
    intended={r['entity'] for r in json.loads((H/'retirement-evidence.json').read_text())}
    assert {q[':db/id'] for q in before[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')}==intended,'Old pool changed; refresh retirement evidence'
    ids=[r['entity'] for r in json.loads((H/'retirement-evidence.json').read_text())]
    rows=publisher.client.query('[:find (pull ?q [:db/id :question/id :question/math-academy-id :question/retired {:task-item/_content [:db/id]} {:knowledge-point/_canonical-example [:db/id]}]) :in $ ?kp [?q ...] :where [?kp :knowledge-point/questions ?q]]',
        [KP,ids],DIRECTORY,'retirements-before',prepared['basis']) if ids else []
    assert len(rows)==len(ids)
    evidence={r['entity']:r for r in json.loads((H/'retirement-evidence.json').read_text())}
    batch=loads(prepared['batch_edn']);retired=[]
    for [question] in rows:
        assert str(question[':question/id'])==evidence[question[':db/id']]['uuid']
        assert not question.get(':question/math-academy-id') and not question.get(':knowledge-point/_canonical-example')
        if question.get(':question/retired') is True:continue
        eid=question[':db/id'];before=question.get(':question/retired')
        batch['forms'].append([kw('db/cas'),eid,kw('question/retired'),before,True])
        batch['assertions'].append([eid,kw('question/retired'),True])
        if before is False:batch['retractions'].append([eid,kw('question/retired'),False])
        retired.append(eid)
    prepared['batch_edn']=dumps(batch)
    prepared['retirements']=jsonable([r[0] for r in rows]);prepared['retirement_entities_changed']=retired
    atomic_json(DIRECTORY/'preparation.json',prepared)
    committer=GeneratorCommitter(publisher.config,publisher.client,DIRECTORY)
    snapshot=loads(prepared['snapshot_edn'])
    committer.preview(batch,snapshot)
    request=committer.save_request(batch,snapshot,digest(prepared))
    save('preview-verification.json',{'basis':prepared['basis'],'new_questions':24,'retirements':retired,
        'native_validation_passed':True,'exact_datoms_verified':True,'request_key':request['request_key']})
    return prepared,committer,request


def apply(publisher,prepared,committer,request):
    assert request['content_sha256']==digest(prepared),'Pending request must keep its exact preparation'
    receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt)
    basis=receipt[':edb/db-after-t']
    after=publisher.read_kp(KP,DIRECTORY/'after',basis);before=loads(prepared['before_edn'])
    original={str(q[':question/id']):q for q in before[':knowledge-point/questions']}
    current={str(q[':question/id']):q for q in after[':knowledge-point/questions']}
    assert len(current)==len(original)+24
    retired_ids={q[':db/id'] for q in prepared['retirements']}
    for qid,question in original.items():
        expected=dict(question)
        if expected[':db/id'] in retired_ids:expected[kw('question/retired')]=True
        assert current[qid]==expected,('Existing content changed',qid)
    new=[]
    for record in prepared['records']:
        question=current[record['question'][':question/id']]
        assert not question.get(':question/math-academy-id') and not question.get(':question/retired')
        assert normalized_question(question)==normalized_question(record['question'])
        new.append({'entity':question[':db/id'],'uuid':str(question[':question/id']),
                    'band':record['question'][':question/difficulty'],'template':record['generation']['template']})
    exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in after.items() if k not in exclude}
    reg=after[':knowledge-point/question-generator']
    assert reg[':question-generator/script']==prepared['generator_path'] and str(reg[':question-generator/id'])==prepared['generator_id']
    ids=[q[':db/id'] for q in prepared['retirements']]
    rows=publisher.client.query('[:find (pull ?q [:db/id :question/id :question/retired {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/retired true]]',
        [ids],DIRECTORY,'retirements-after',basis) if ids else []
    assert len(rows)==len(ids)
    for [question] in rows:
        old=next(q for q in prepared['retirements'] if q[':db/id']==question[':db/id'])
        assert jsonable(question.get(':task-item/_content'))==old.get(':task-item/_content')
    package=json.loads((H/'package-verification.json').read_text());verify_package(MATH/Path(*Path(prepared['generator_path']).parts[:3]),package['digest'])
    result={'committed':True,'passed':True,'basis_before':receipt[':edb/db-before-t'],'basis_after':basis,
        'new_questions':new,'fresh_generated_counts':dict(Counter(r['band'] for r in new)),
        'retired_old_questions':ids,'imported_questions_preserved':sum(':question/math-academy-id'in q for q in original.values()),
        'canonical_preserved':True,'saved_attempt_references_preserved':True,'old_question_and_answer_content_preserved':True,
        'new_reference':prepared['generator_path'],'request_key':request['request_key'],**proof}
    save('verification.json',result);atomic_json(DIRECTORY/'verification.json',result)
    committer.retire(request,'verified',result)
    print(json.dumps({k:v for k,v in result.items() if k!='new_questions'}))


def run(kp):
    global H,KP,DIRECTORY
    KP=kp;H=BASE/str(kp);DIRECTORY=H/'publication'
    publisher=Publisher.from_environment(source=':agent/codex')
    inventory_lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    # Use the same KP and API locks as the live builders/refills.
    with file_lock(inventory_lock),file_lock(Path(publisher.config.request_directory)/'api.lock'):
        committer=GeneratorCommitter(publisher.config,publisher.client,DIRECTORY)
        request=committer.pending()
        if request:
            apply(publisher,json.loads((DIRECTORY/'preparation.json').read_text()),committer,request);return
        if (H/'verification.json').exists():
            print('Already committed and verified; no new submission');return
        for attempt in range(3):
            request=None
            try:
                prepared,committer,request=prepare(publisher)
                apply(publisher,prepared,committer,request);return
            except StaleBasis:
                if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; reprepare against fresh basis'})
        raise RuntimeError('Repair repeatedly raced current database writes; retained evidence remains')


if __name__=='__main__':
    for kp in (17592186064218,17592186064219,17592186064250,17592186064220,17592186184349,17592186184350,17592186184351,17592186184352):run(kp)
