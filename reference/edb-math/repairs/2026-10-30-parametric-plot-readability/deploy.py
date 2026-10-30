"""Register readable plots, retire unused old stock, append five per band."""
import json,os,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,jsonable,normalized_question,verify_assets
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,verify_package
from capture.scripts.storage import atomic_json
KP=17592186087721

def prepare(p):
    assert json.loads((H/'generator-verification.json').read_text())['passed']
    for mode in ('desktop','phone'):assert json.loads((H/f'render-{mode}/rendering.json').read_text())['passed']
    capture=json.loads((H/'capture.json').read_text());files=[*capture['files'],'parametric_plot_policy.py']
    manifest=build_manifest(H/'package','generator.py',files,dependencies=capture['dependencies'])
    package=publish_package(H/'package','generator.py',files,p.config.math_root,dependencies=capture['dependencies'],expected_digest=manifest_digest(manifest));verify_package(package.directory,package.digest)
    # Check the immutable entry point, not only the editable workspace module.
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(H/'package-cli-assets')}
    for index,level in enumerate(('easy','moderate','hard')):
        output=subprocess.run([sys.executable,str(package.directory/'generator.py'),'--difficulty',level,'--count','1','--seed',str(2026103087721+index*1009)],check=True,capture_output=True,text=True,env=env,timeout=45)
        from generate.parametric_plot_policy import validate_delivery_batch
        validate_delivery_batch(json.loads(output.stdout),KP)
    records=json.loads((H/'candidate-pool.json').read_text());work=H/'publication'
    prepared=p.prepare(KP,records,package.reference,package.digest,work,source_snapshot=json.loads((H/'source/source.json').read_text()),assets_directory=H/'assets',expected_registered_generator=capture['registered_generator'])
    assert prepared['new_questions']==15 and prepared['duplicates']==0
    before=loads(prepared['before_edn']);basis=prepared['basis'];active=[q for q in before[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
    usage=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[[q[':db/id'] for q in active]],work,'usage',basis)
    used={r[0][':db/id'] for r in usage if r[0].get(':task-item/_content')};retired=[];batch=loads(prepared['batch_edn'])
    for q in active:
        if q[':db/id'] in used:continue
        eid=q[':db/id'];old=q.get(':question/retired');retired.append(eid)
        batch['forms'].append([kw('db/cas'),eid,kw('question/retired'),old,True]);batch['assertions'].append([eid,kw('question/retired'),True])
        if old is False:batch['retractions'].append([eid,kw('question/retired'),False])
    prepared.update(batch_edn=dumps(batch),retired_questions=sorted(retired),used_questions_preserved=sorted(used),usage=jsonable(usage))
    atomic_json(work/'preparation.json',prepared);committer=GeneratorCommitter(p.config,p.client,work)
    committer.preview(batch,loads(prepared['snapshot_edn']));request=committer.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared))
    return prepared,committer,request

def apply(p,prepared,committer,request):
    assert request['content_sha256']==digest(prepared)
    receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t']
    after=p.read_kp(KP,H/'publication/after',basis);before=loads(prepared['before_edn']);now={str(q[':question/id']):q for q in after[':knowledge-point/questions']}
    assert len(now)==len(before[':knowledge-point/questions'])+15
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in prepared['retired_questions']:expected[kw('question/retired')]=True
        assert now[str(q[':question/id'])]==expected,('Unexpected old content change',q[':db/id'])
    new=[]
    for r in prepared['records']:
        q=now[r['question'][':question/id']];assert normalized_question(q)==normalized_question(r['question'])
        new.append({'entity':q[':db/id'],'uuid':str(q[':question/id']),'level':str(q[':question/difficulty'][':db/ident']).split('/')[-1]})
    excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in excluded}=={k:v for k,v in after.items() if k not in excluded}
    assert after[':knowledge-point/question-generator'][':question-generator/script']==prepared['generator_path']
    verify_assets(prepared['records'],p.config.math_root)
    result={'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':basis,'generator':prepared['generator_path'],'retired_questions':prepared['retired_questions'],'used_questions_preserved':prepared['used_questions_preserved'],'new_questions':new,'imported_preserved':16,'canonical_preserved':True,'question_field_answer_content_and_saved_responses_preserved':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);committer.retire(request,'verified',result);print(json.dumps(result,indent=2),flush=True)

def install():
    local=ROOT/'generate/scratch'/str(KP);local.mkdir(exist_ok=True);capture=json.loads((H/'capture.json').read_text());result=json.loads((H/'verification.json').read_text())
    for name in [*capture['files'],'parametric_plot_policy.py']:
        out=local/name
        if out.exists():out.chmod(out.stat().st_mode|0o200)
        shutil.copy2(H/'package'/name,out);out.chmod(out.stat().st_mode|0o200)
    (ROOT/f'generate/scratch/{KP}.py').write_text('import runpy,sys\nfrom pathlib import Path\nLOCAL=Path(__file__).with_suffix("")\nsys.path.insert(0,str(LOCAL))\nif __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")\n')
    (local/'README.md').write_text('# Parametric graph recognition\n\nProduction version parametric-graphs-3 uses readable one-unit grids, labels outside the plot, common bank-wide bounds and unmarked choices. Table-point dots appear only in the solution. Unreadable oversized banks are resampled, retaining all 16 source families.\n\nUse `COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=/tmp/parametric-plots .venv/bin/python generate/scratch/17592186087721.py --difficulty easy --count 5 --seed 42`.\n\nCurrent immutable reference: `'+result['generator']+'`. Repair and exact publication evidence: `reference/edb-math/repairs/2026-10-30-parametric-plot-readability/`. Older files in this folder retain historical investigations and are not the registered renderer.\n')

def main():
    p=Publisher.from_environment(source=':agent/codex');work=H/'publication';lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
        committer=GeneratorCommitter(p.config,p.client,work);request=committer.pending()
        if request:apply(p,json.loads((work/'preparation.json').read_text()),committer,request)
        elif not (H/'verification.json').exists():
            for attempt in range(3):
                request=None
                try:
                    prepared,committer,request=prepare(p);apply(p,prepared,committer,request);break
                except StaleBasis:
                    if request:committer.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; refresh basis and usage'})
            else:raise RuntimeError('Repeated basis races; publication not completed')
        install()

if __name__=='__main__':main()
