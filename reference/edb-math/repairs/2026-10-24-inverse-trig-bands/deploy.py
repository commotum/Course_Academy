"""Publish four immutable successors and fresh banks with exact recoverable requests."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

import sympy

H = Path(__file__).resolve().parent;ROOT = H.parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from scripts.generator_publish import Publisher, GeneratorCommitter, StaleBasis, SourceChanged, digest, dumps, loads, kw, file_lock, normalized_question, jsonable
from scripts.generator_packages import publish_package, build_manifest, manifest_digest, materialize_package, verify_package
from capture.scripts.storage import atomic_json

KPS = (17592186064218,17592186064219,17592186064250,17592186064220)


def read(path):return json.loads((H/path).read_text())


def reviewed(kp):
    review = read('generator-verification.json');assert review['passed'] and review['new_questions'] == 102
    grader = read('grader-verification.json');assert grader['documented_unresolved_checks'] == 0
    assert read('grader-build.json')['input_sha256'] == hashlib.sha256((H/'grader-input.json').read_bytes()).hexdigest()
    assert read('render/rendering.json')['passed']
    assert read('render/input.json') == read('render-input.json')
    assert read('render-inspection.json')['passed']
    package = H/'packages'/str(kp)
    dependencies = {'python':platform.python_version(),'packages':{'sympy':sympy.__version__}}
    manifest = build_manifest(package,'generator.py',['generator.py','inverse_trig.py','evidence.json'],dependencies=dependencies)
    assert manifest_digest(manifest) == review['approved_package_hashes'][str(kp)]
    records = [r for r in read('candidate-pool.json') if r['knowledge_point']['db_id'] == kp]
    assert len(records) == (30 if kp == 17592186064220 else 24)
    return package,manifest,records


def prepare(publisher,kp,directory):
    package,manifest,records = reviewed(kp)
    published = publish_package(package,'generator.py',manifest['files'],publisher.config.math_root,
        dependencies=manifest['dependencies'],expected_digest=manifest_digest(manifest))
    runtime = H/'deployed-runtime'/published.digest
    if runtime.exists():verify_package(runtime,published.digest);entry = runtime/'generator.py'
    else:entry = materialize_package(published.reference,publisher.config.math_root,runtime)
    replay = subprocess.run([sys.executable,'-B',str(entry),'--difficulty','all','--count','10' if kp == 17592186064220 else '8',
        '--seed','864218','--format','json'],capture_output=True,text=True,check=True,timeout=180)
    reproduced = json.loads(replay.stdout)
    assert len(reproduced) == len(records)
    # Delivery deliberately rekeys field-owned identities; semantic content and
    # instance metadata must reproduce exactly after package relocation.
    for a,b in zip(reproduced,records):
        assert normalized_question(a['question'],identity=False) == normalized_question(b['question'],identity=False)
        assert a['generation'] == b['generation']
    atomic_json(directory/'package-verification.json',{'reference':published.reference,'digest':published.digest,
        'relocated_records_identical':len(records),'manifest':manifest})
    source = read(Path('source')/f'{kp}.json')
    expected = source['registered_generator']
    prepared = publisher.prepare(kp,records,published.reference,published.digest,directory,
        source_snapshot=source,assets_directory=package,
        expected_registered_generator=expected[':question-generator/script'] if expected else None)
    before = loads(prepared['before_edn'])
    assert jsonable(before.get(':knowledge-point/question-generator')) == expected, 'Concurrent generator replacement requires review'
    assert prepared['new_questions'] == len(records) and prepared['duplicates'] == 0
    # At capture all 75 existing practice questions were imported. Still compute
    # the retirement set from the guarded live value, never mistake imports for
    # generations. A newly arrived unimported item requires provenance review.
    old_generated = [q for q in before[':knowledge-point/questions'] if not q.get(':question/math-academy-id')]
    captured = read(Path('source')/str(kp)/'inventory.json')
    known = {q[':db/id'] for q in captured['questions'] if not q.get(':question/math-academy-id')}
    if {q[':db/id'] for q in old_generated} != known: raise SourceChanged('Unreviewed generated questions arrived during repair')
    batch = loads(prepared['batch_edn']);retired = []
    for q in old_generated:
        if q.get(':question/retired') is True:continue
        eid = q[':db/id'];old = q.get(':question/retired')
        batch['forms'].append([kw('db/cas'),eid,kw('question/retired'),old,True])
        batch['assertions'].append([eid,kw('question/retired'),True])
        if old is False:batch['retractions'].append([eid,kw('question/retired'),False])
        retired.append(eid)
    prepared['batch_edn'] = dumps(batch);prepared['retired_question_ids'] = retired
    atomic_json(directory/'preparation.json',prepared)
    committer = GeneratorCommitter(publisher.config,publisher.client,directory)
    snapshot = loads(prepared['snapshot_edn']);committer.preview(batch,snapshot)
    request = committer.save_request(batch,snapshot,digest(prepared))
    return prepared,committer,request


def apply(publisher,kp,directory,prepared,committer,request):
    assert request['content_sha256'] == digest(prepared)
    receipt = committer.submit(request);proof = committer.verify_receipt(request,receipt)
    after = publisher.read_kp(kp,directory/'after',receipt[':edb/db-after-t'])
    before = loads(prepared['before_edn']);old = {str(q[':question/id']):q for q in before[':knowledge-point/questions']}
    current = {str(q[':question/id']):q for q in after[':knowledge-point/questions']}
    assert len(current) == len(old)+prepared['new_questions']
    for identity,q in old.items():
        expected = dict(q)
        if q[':db/id'] in prepared['retired_question_ids']:expected[kw('question/retired')] = True
        assert current[identity] == expected, ('Existing question or answer changed',identity)
    new = []
    for record in prepared['records']:
        q = current[record['question'][':question/id']]
        assert normalized_question(q) == normalized_question(record['question'])
        assert not q.get(':question/math-academy-id') and not q.get(':question/retired')
        new.append({'entity':q[':db/id'],'uuid':str(q[':question/id']),'band':record['question'][':question/difficulty'],
                    'template':record['generation']['template']})
    exclude = {':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude} == {k:v for k,v in after.items() if k not in exclude}
    assert after[':knowledge-point/question-generator'][':question-generator/script'] == prepared['generator_path']
    assert str(after[':knowledge-point/question-generator'][':question-generator/id']) == prepared['generator_id']
    # Update legacy entrypoints only after their live pointers have moved to the
    # reviewed immutable successors. Keep old scripts in originals/ for audit.
    package = H/'packages'/str(kp);local = ROOT/'generate/scratch'/str(kp)
    shutil.copy2(package/'evidence.json',local/'band-evidence.json')
    shutil.copy2(package/'generator.py',ROOT/'generate/scratch'/f'{kp}.py')
    result = {'passed':True,'committed':True,'kp':kp,'basis_before':receipt[':edb/db-before-t'],'basis_after':receipt[':edb/db-after-t'],
              'new_questions':new,'new_counts':dict(Counter(q['band'] for q in new)),
              'retired_old_generated_questions':prepared['retired_question_ids'],
              'imported_questions_preserved':sum(bool(q.get(':question/math-academy-id')) for q in old.values()),
              'canonical_preserved':True,'existing_question_and_answer_content_preserved':True,
              'generator_reference':prepared['generator_path'],'request_key':request['request_key'],**proof}
    atomic_json(directory/'verification.json',result)
    committer.retire(request,'verified',result)
    print(json.dumps({k:v for k,v in result.items() if k != 'new_questions'}),flush=True)
    return result


def main():
    publisher = Publisher.from_environment(source=':agent/codex');results = []
    for kp in KPS:
        directory = H/'publication'/str(kp);directory.mkdir(parents=True,exist_ok=True)
        lock = ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'
        with file_lock(lock),file_lock(Path(publisher.config.request_directory)/'api.lock'):
            committer = GeneratorCommitter(publisher.config,publisher.client,directory);pending = committer.pending()
            if pending:
                results.append(apply(publisher,kp,directory,json.loads((directory/'preparation.json').read_text()),committer,pending));continue
            if (directory/'verification.json').exists():
                result = json.loads((directory/'verification.json').read_text());assert result['passed'];results.append(result);continue
            for _ in range(3):
                request = None
                try:
                    prepared,committer,request = prepare(publisher,kp,directory)
                    results.append(apply(publisher,kp,directory,prepared,committer,request));break
                except StaleBasis:
                    if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed stale basis; prepare afresh'})
            else:raise RuntimeError('Repeated concurrent writes; retained repair evidence')
    atomic_json(H/'completion.json',{'passed':True,'committed':True,'new_questions':sum(len(r['new_questions']) for r in results),
        'imported_questions_preserved':sum(r['imported_questions_preserved'] for r in results),
        'old_generated_questions_retired':sum(len(r['retired_old_generated_questions']) for r in results),'knowledge_points':results})


if __name__ == '__main__':main()
