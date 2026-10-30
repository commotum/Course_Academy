"""Publish the generator and presentation-only repairs in one guarded request."""
import json,os,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,jsonable
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,verify_package
from capture.scripts.storage import atomic_json
from build import patch_question,verify
KP=17592186115226

def prepare(p):
    assert json.loads((H/'generator-verification.json').read_text())['passed']
    assert json.loads((H/'render/rendering.json').read_text())['passed']
    capture=json.loads((H/'capture.json').read_text());files=[*capture['files'],'matrix_product_prompt_policy.py']
    manifest=build_manifest(H/'package','generator.py',files,dependencies=capture['dependencies'])
    package=publish_package(H/'package','generator.py',files,p.config.math_root,dependencies=capture['dependencies'],expected_digest=manifest_digest(manifest))
    verify_package(package.directory,package.digest)
    for level in ('easy','moderate','hard'):
        result=subprocess.run([sys.executable,str(package.directory/'generator.py'),'--difficulty',level,'--count','5','--seed','20261029'],check=True,capture_output=True,text=True,timeout=30,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        for r in json.loads(result.stdout):verify(r['question'])
    work=H/'publication'
    prepared=p.prepare(KP,[],package.reference,package.digest,work,assets_directory=H/'package',expected_registered_generator=capture['registered_generator'])
    before=loads(prepared['before_edn']);batch=loads(prepared['batch_edn'])
    saved={x['entity']:x for x in json.loads((H/'repairs.json').read_text())}
    affected={q[':db/id'] for q in before[':knowledge-point/questions'] if '\\ast' in q.get(':question/problem','')}
    assert affected==set(saved),('Affected inventory changed',affected)
    patches=[]
    for q in before[':knowledge-point/questions']:
        if q[':db/id'] not in affected:continue
        assert q[':question/problem']==saved[q[':db/id']]['before']
        updated=patch_question(jsonable(q));verify(updated);value=updated[':question/problem'];assert value==saved[q[':db/id']]['after']
        batch['forms'].append([kw('db/cas'),q[':db/id'],kw('question/problem'),q[':question/problem'],value])
        batch['assertions'].append([q[':db/id'],kw('question/problem'),value]);batch['retractions'].append([q[':db/id'],kw('question/problem'),q[':question/problem']])
        patches.append({'entity':q[':db/id'],'before':q[':question/problem'],'after':value})
    prepared.update(batch_edn=dumps(batch),prompt_repairs=patches)
    atomic_json(work/'preparation.json',prepared)
    committer=GeneratorCommitter(p.config,p.client,work);committer.preview(batch,loads(prepared['snapshot_edn']))
    request=committer.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared))
    return prepared,committer,request

def apply(p,prepared,committer,request):
    assert request['content_sha256']==digest(prepared)
    receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t']
    after=p.read_kp(KP,H/'publication/after',basis);before=loads(prepared['before_edn']);patches={x['entity']:x['after'] for x in prepared['prompt_repairs']}
    now={q[':db/id']:q for q in after[':knowledge-point/questions']}
    assert len(now)==len(before[':knowledge-point/questions'])
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in patches:expected[kw('question/problem')]=patches[q[':db/id']];verify(jsonable(now[q[':db/id']]))
        assert now[q[':db/id']]==expected,('Unexpected question/field/answer change',q[':db/id'])
    excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in excluded}=={k:v for k,v in after.items() if k not in excluded}
    assert after[':knowledge-point/question-generator'][':question-generator/script']==prepared['generator_path']
    assert not any('\\ast' in q.get(':question/problem','') for q in now.values())
    result={'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':basis,'generator':prepared['generator_path'],'questions_repaired':sorted(patches),'question_field_answer_ids_and_saved_responses_preserved':True,'imports_and_canonical_preserved':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);committer.retire(request,'verified',result);print(json.dumps(result,indent=2))

def install():
    result=json.loads((H/'verification.json').read_text());local=ROOT/'generate/scratch'/str(KP);local.mkdir(exist_ok=True)
    capture=json.loads((H/'capture.json').read_text())
    for name in [*capture['files'],'matrix_product_prompt_policy.py']:
        out=local/name
        if out.exists():out.chmod(out.stat().st_mode|0o200)
        shutil.copy2(H/'package'/name,out);out.chmod(out.stat().st_mode|0o200)
    (local/'README.md').write_text('# Distributive matrix products\n\nVersion 3 supplies actual matrix entries outside the requested cells, matching imported partial answer matrices. Numbers, targets, difficulty profiles and worked calculations are unchanged.\n\nLive reference: `'+result['generator']+'`.\nRepair: `reference/edb-math/repairs/2026-10-29-matrix-supplied-entries/`.\n')
    (ROOT/f'generate/scratch/{KP}.py').write_text('import runpy,sys\nfrom pathlib import Path\nLOCAL=Path(__file__).with_suffix("")\nsys.path.insert(0,str(LOCAL))\nif __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")\n')

def main():
    p=Publisher.from_environment(source=':agent/codex');work=H/'publication'
    lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
        committer=GeneratorCommitter(p.config,p.client,work);request=committer.pending()
        if request:apply(p,json.loads((work/'preparation.json').read_text()),committer,request)
        elif not (H/'verification.json').exists():
            for _ in range(3):
                request=None
                try:
                    prepared,committer,request=prepare(p);apply(p,prepared,committer,request);break
                except StaleBasis:
                    if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; prepare at a fresh basis'})
            else:raise RuntimeError('Repeated basis races; repair is not committed')
        install()

if __name__=='__main__':main()
