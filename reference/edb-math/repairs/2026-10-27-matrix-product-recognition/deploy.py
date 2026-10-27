"""Publish the prompt-only repair and preserve existing attempt content."""
import json,os,platform,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,normalized_question,jsonable
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,materialize_package,verify_package
from capture.scripts.storage import atomic_json
KP=17592186059747

def prepare(p):
    assert json.loads((H/'generator-verification.json').read_text())['passed']
    assert json.loads((H/'grader-verification.json').read_text())['documented_unresolved_checks']==0
    assert json.loads((H/'render/rendering.json').read_text())['passed']
    capture=json.loads((H/'capture.json').read_text());work=H/'publication'
    files=[*capture['files'],'matrix_product_prompt_policy.py'];deps={'python':platform.python_version(),'packages':{}}
    manifest=build_manifest(H/'package','generator.py',files,dependencies=deps)
    package=publish_package(H/'package','generator.py',files,p.config.math_root,dependencies=deps,expected_digest=manifest_digest(manifest))
    runtime=work/'runtime'/package.digest
    entry=runtime/'generator.py' if runtime.exists() else materialize_package(package.reference,p.config.math_root,runtime)
    verify_package(runtime,package.digest)
    spec=__import__('importlib.util',fromlist=['spec_from_file_location']);sys.path.insert(0,str(H/'package'))
    module=spec.module_from_spec(s:=spec.spec_from_file_location('matrix_local',H/'package/generator.py'));s.loader.exec_module(module)
    for level in ('easy','moderate','hard'):
        out=subprocess.run([sys.executable,str(entry),'--difficulty',level,'--count','10','--seed','20261027'],check=True,capture_output=True,text=True,timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        assert json.loads(out.stdout)==module.generate(level,10,20261027)
    records=json.loads((H/'candidate-pool.json').read_text())
    prepared=p.prepare(KP,records,package.reference,package.digest,work,source_snapshot=json.loads((H/'fresh-source/source.json').read_text()),assets_directory=H/'package',expected_registered_generator=capture['registered_generator'])
    assert prepared['new_questions']==5 and prepared['duplicates']==0
    before=loads(prepared['before_edn']);retire_ids={r['old'] for r in json.loads((H/'replacement-inputs.json').read_text())}
    active_hinted={q[':db/id'] for q in before[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired') and 'Use a row' in q[':question/problem']}
    assert active_hinted==retire_ids
    batch=loads(prepared['batch_edn'])
    for q in before[':knowledge-point/questions']:
        if q[':db/id'] not in retire_ids:continue
        assert not q.get(':question/math-academy-id')
        old=q.get(':question/retired');batch['forms'].append([kw('db/cas'),q[':db/id'],kw('question/retired'),old,True]);batch['assertions'].append([q[':db/id'],kw('question/retired'),True])
        if old is False:batch['retractions'].append([q[':db/id'],kw('question/retired'),False])
    prepared.update(batch_edn=dumps(batch),retired_questions=sorted(retire_ids))
    atomic_json(work/'preparation.json',prepared);committer=GeneratorCommitter(p.config,p.client,work)
    committer.preview(batch,loads(prepared['snapshot_edn']));request=committer.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared))
    return prepared,committer,request

def apply(p,prepared,committer,request):
    assert request['content_sha256']==digest(prepared)
    receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t']
    after=p.read_kp(KP,H/'publication/after',basis);before=loads(prepared['before_edn']);now={str(q[':question/id']):q for q in after[':knowledge-point/questions']}
    assert len(now)==len(before[':knowledge-point/questions'])+5
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in prepared['retired_questions']:expected[kw('question/retired')]=True
        assert now[str(q[':question/id'])]==expected,('Existing question content changed',q[':db/id'])
    new=[]
    for record in prepared['records']:
        q=now[record['question'][':question/id']];assert normalized_question(q)==normalized_question(record['question']) and not q.get(':question/retired')
        new.append({'entity':q[':db/id'],'uuid':str(q[':question/id'])})
    assert not any('Use a row' in q[':question/problem'] for q in now.values() if not q.get(':question/math-academy-id') and not q.get(':question/retired'))
    exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in after.items() if k not in exclude}
    assert after[':knowledge-point/question-generator'][':question-generator/script']==prepared['generator_path']
    result={'passed':True,'committed':True,'basis_after':basis,'new_reference':prepared['generator_path'],'new_questions':new,'retired_questions':prepared['retired_questions'],'imported_questions_preserved':sum(bool(q.get(':question/math-academy-id')) for q in before[':knowledge-point/questions']),'canonical_preserved':True,'existing_question_field_answer_content_preserved':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);committer.retire(request,'verified',result)
    print('Committed at',basis,': five hinted questions retired, five replacements published',flush=True)

def install():
    result=json.loads((H/'verification.json').read_text());runtime=H/'publication/runtime'/Path(result['new_reference']).parts[2];local=ROOT/f'generate/scratch/{KP}';local.mkdir(exist_ok=True)
    for name in json.loads((runtime/'generator-package.json').read_text())['files']:
        out=local/name
        if out.exists():out.chmod(out.stat().st_mode|0o200)
        shutil.copy2(runtime/name,out);out.chmod(out.stat().st_mode|0o200)
    (ROOT/f'generate/scratch/{KP}.py').write_text('import runpy,sys\nfrom pathlib import Path\nLOCAL=Path(__file__).with_suffix("")\nsys.path.insert(0,str(LOCAL))\nif __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")\n')
    (local/'README.md').write_text('# Multiplying 3×3 square matrices\n\nVersion 1.1.0 retains partial answer matrices, target positions, numerical ranges and existing difficulty definitions. Ordinary prompts contain no row/column process reminder or expanded entry calculation. All calculations remain in the worked solution.\n\nRepair and evidence: `reference/edb-math/repairs/2026-10-27-matrix-product-recognition/`.\n')

def main():
    p=Publisher.from_environment(source=':agent/codex');work=H/'publication'
    lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
        committer=GeneratorCommitter(p.config,p.client,work);request=committer.pending()
        if request:apply(p,json.loads((work/'preparation.json').read_text()),committer,request)
        elif not (H/'verification.json').exists():
            for attempt in range(3):
                request=None
                try:
                    prepared,committer,request=prepare(p);apply(p,prepared,committer,request);break
                except StaleBasis:
                    if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed writer rejection; prepare afresh'})
            else:raise RuntimeError('Publication raced repeatedly; original evidence retained')
        install()

if __name__=='__main__':main()
