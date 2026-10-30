"""Publish the two layout repairs; leave the unaffected range KP unchanged."""
import json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,jsonable,normalized_question
from scripts.generator_packages import publish_package,build_manifest,manifest_digest
from capture.scripts.storage import atomic_json

def prepare(p,kp,h,package):
    capture=json.loads((h/'capture.json').read_text());work=h/'publication'
    prepared=p.prepare(kp,json.loads((h/'candidate-pool.json').read_text()),package.reference,package.digest,work,source_snapshot=json.loads((h/'source/source.json').read_text()),assets_directory=h,expected_registered_generator=capture['registered_generator'])
    assert prepared['new_questions']==15 and prepared['duplicates']==0
    before=loads(prepared['before_edn']);active=[q for q in before[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
    usage=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[[q[':db/id'] for q in active]],work,'usage',prepared['basis'])
    used={row[0][':db/id'] for row in usage if row[0].get(':task-item/_content')};retired=[];batch=loads(prepared['batch_edn'])
    for q in active:
        if q[':db/id'] in used:continue
        eid=q[':db/id'];old=q.get(':question/retired');retired.append(eid)
        batch['forms'].append([kw('db/cas'),eid,kw('question/retired'),old,True]);batch['assertions'].append([eid,kw('question/retired'),True])
        if old is False:batch['retractions'].append([eid,kw('question/retired'),False])
    prepared.update(batch_edn=dumps(batch),retired_questions=sorted(retired),used_questions_preserved=sorted(used))
    atomic_json(work/'preparation.json',prepared);committer=GeneratorCommitter(p.config,p.client,work)
    committer.preview(batch,loads(prepared['snapshot_edn']));request=committer.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared))
    return prepared,committer,request

def apply(p,kp,h,prepared,c,request):
    assert request['content_sha256']==digest(prepared)
    receipt=c.submit(request);proof=c.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t'];after=p.read_kp(kp,h/'publication/after',basis);before=loads(prepared['before_edn']);now={str(q[':question/id']):q for q in after[':knowledge-point/questions']}
    assert len(now)==len(before[':knowledge-point/questions'])+15
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in prepared['retired_questions']:expected[kw('question/retired')]=True
        assert now[str(q[':question/id'])]==expected
    new=[]
    for r in prepared['records']:
        q=now[r['question'][':question/id']];assert normalized_question(q)==normalized_question(r['question']);new.append({'entity':q[':db/id'],'level':str(q[':question/difficulty'][':db/ident']).split('/')[-1]})
    excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in excluded}=={k:v for k,v in after.items() if k not in excluded}
    assert after[':knowledge-point/question-generator'][':question-generator/script']==prepared['generator_path']
    result={'passed':True,'committed':True,'kp':kp,'basis_before':request['basis'],'basis_after':basis,'generator':prepared['generator_path'],'unused_retired':prepared['retired_questions'],'used_preserved':prepared['used_questions_preserved'],'new_questions':new,'imports_canonical_old_question_content_and_saved_responses_preserved':True,'request_key':request['request_key'],**proof}
    atomic_json(h/'verification.json',result);c.retire(request,'verified',result);print(json.dumps(result),flush=True)

def install(kp,h):
    local=ROOT/'generate/scratch'/str(kp);local.mkdir(exist_ok=True);capture=json.loads((h/'capture.json').read_text());result=json.loads((h/'verification.json').read_text())
    for name in capture['files']:
        out=local/name
        if out.exists():out.chmod(out.stat().st_mode|0o200)
        shutil.copy2(h/'package'/name,out);out.chmod(out.stat().st_mode|0o200)
    (ROOT/f'generate/scratch/{kp}.py').write_text('import runpy,sys\nfrom pathlib import Path\nLOCAL=Path(__file__).with_suffix("")\nsys.path.insert(0,str(LOCAL))\nif __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")\n')
    (local/'README.md').write_text('# '+capture['title']+'\n\nThe current generator has a layout-only readability repair: small table panels with repeated headings, or independently visible trigonometric coordinate formulas. Sampled mathematics, answer values and difficulty definitions are preserved.\n\nRegistered package: `'+result['generator']+'`. Evidence: `reference/edb-math/repairs/2026-10-30-parametric-other-kps/`. Older evidence files in this folder describe historical versions.\n')

def main():
    assert json.loads((H/'repair-verification.json').read_text())['passed']
    for mode in ('desktop','phone'):assert json.loads((H/f'repaired-{mode}/rendering.json').read_text())['passed']
    p=Publisher.from_environment(source=':agent/codex');results=[]
    for kp in (17592186087717,17592186087736):
        h=H/str(kp);capture=json.loads((h/'capture.json').read_text());work=h/'publication';c=GeneratorCommitter(p.config,p.client,work)
        lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'
        with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
            request=c.pending()
            if request:apply(p,kp,h,json.loads((work/'preparation.json').read_text()),c,request)
            elif not (h/'verification.json').exists():
                manifest=build_manifest(h/'package','generator.py',capture['files'],dependencies=capture['dependencies'])
                package=publish_package(h/'package','generator.py',capture['files'],p.config.math_root,dependencies=capture['dependencies'],expected_digest=manifest_digest(manifest))
                for attempt in range(5):
                    request=None
                    try:
                        prepared,c,request=prepare(p,kp,h,package);apply(p,kp,h,prepared,c,request);break
                    except StaleBasis:
                        if request:c.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; refresh basis and usage'})
                else:raise RuntimeError('Repeated basis races; publication incomplete')
            install(kp,h);results.append(json.loads((h/'verification.json').read_text()))
    atomic_json(H/'publication-verification.json',{'passed':True,'kps':results})

if __name__=='__main__':main()
