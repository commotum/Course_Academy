"""Replace unused stock and repair reported feedback without changing responses."""
import json,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,normalized_question
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,verify_package
from capture.scripts.storage import atomic_json
KP=17592186166788

def prepare(p,package):
    capture=json.loads((H/'capture.json').read_text());work=H/'publication'
    prepared=p.prepare(KP,json.loads((H/'candidate-pool.json').read_text()),package.reference,package.digest,work,
        source_snapshot=json.loads((H/'source/source.json').read_text()),assets_directory=H,
        expected_registered_generator=capture['registered_generator'])
    assert prepared['new_questions']==15 and prepared['duplicates']==0
    before=loads(prepared['before_edn']);batch=loads(prepared['batch_edn'])
    active=[q for q in before[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
    usage=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',
        [[q[':db/id'] for q in active]],work,'usage',prepared['basis'])
    used={r[0][':db/id'] for r in usage if r[0].get(':task-item/_content')};retired=[]
    for q in active:
        if q[':db/id'] in used:continue
        eid=q[':db/id'];old=q.get(':question/retired');retired.append(eid)
        batch['forms'].append([kw('db/cas'),eid,kw('question/retired'),old,True])
        batch['assertions'].append([eid,kw('question/retired'),True])
        if old is False:batch['retractions'].append([eid,kw('question/retired'),False])
    proposals=json.loads((H/'reported-question-repairs.json').read_text())
    for proposal in proposals:
        target=next(q for q in before[':knowledge-point/questions'] if q[':db/id']==proposal['entity'])
        assert target[':'+proposal['attribute']]==proposal['before']
        batch['forms'].append([kw('db/cas'),proposal['entity'],kw(proposal['attribute']),proposal['before'],proposal['after']])
        batch['assertions'].append([proposal['entity'],kw(proposal['attribute']),proposal['after']])
        batch['retractions'].append([proposal['entity'],kw(proposal['attribute']),proposal['before']])
    batch['forms'].append([kw('db/ensure'),proposals[0]['entity'],kw('question/validate')])
    prepared.update(batch_edn=dumps(batch),retired_questions=sorted(retired),used_questions_preserved=sorted(used),reported_question_repairs=proposals)
    atomic_json(work/'preparation.json',prepared);c=GeneratorCommitter(p.config,p.client,work)
    c.preview(batch,loads(prepared['snapshot_edn']));request=c.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared))
    return prepared,c,request

def apply(p,prepared,c,request):
    assert request['content_sha256']==digest(prepared)
    receipt=c.submit(request);proof=c.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t']
    after=p.read_kp(KP,H/'publication/after',basis);before=loads(prepared['before_edn'])
    now={str(q[':question/id']):q for q in after[':knowledge-point/questions']};proposals=prepared['reported_question_repairs']
    assert len(now)==len(before[':knowledge-point/questions'])+15
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in prepared['retired_questions']:expected[kw('question/retired')]=True
        for proposal in proposals:
            if q[':db/id']==proposal['entity']:expected[kw(proposal['attribute'])]=proposal['after']
        assert now[str(q[':question/id'])]==expected
    new=[]
    for r in prepared['records']:
        q=now[r['question'][':question/id']]
        assert normalized_question(q)==normalized_question(r['question'])
        new.append({'entity':q[':db/id'],'level':str(q[':question/difficulty'][':db/ident']).split('/')[-1]})
    excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in excluded}=={k:v for k,v in after.items() if k not in excluded}
    assert after[':knowledge-point/question-generator'][':question-generator/script']==prepared['generator_path']
    result={'passed':True,'committed':True,'kp':KP,'basis_before':request['basis'],'basis_after':basis,
        'generator':prepared['generator_path'],'unused_retired':prepared['retired_questions'],
        'used_preserved':prepared['used_questions_preserved'],'equivalent_prompt_and_solution_repaired':proposals[0]['entity'],
        'new_questions':new,'all_existing_question_field_answer_identities_keys_and_saved_responses_preserved':True,
        'imports_canonical_and_observed_levels_preserved':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);c.retire(request,'verified',result);print(json.dumps(result),flush=True)

def install():
    capture=json.loads((H/'capture.json').read_text());result=json.loads((H/'verification.json').read_text())
    local=ROOT/'generate/scratch'/str(KP);local.mkdir(exist_ok=True)
    for name in capture['files']:
        out=local/name
        if out.exists():out.chmod(out.stat().st_mode|0o200)
        shutil.copy2(H/'package'/name,out);out.chmod(out.stat().st_mode|0o200)
    (ROOT/f'generate/scratch/{KP}.py').write_text('import runpy,sys\nfrom pathlib import Path\nLOCAL=Path(__file__).with_suffix("")\nsys.path.insert(0,str(LOCAL))\nif __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")\n')
    (local/'README.md').write_text('# Identifying equilibrium solutions\n\nVersion 2.0.0 preserves source families and uses one unexpanded residual throughout each solution. Easy uses small unshifted expressions; moderate adds an actual rearrangement or one small translation; hard tests original-domain membership and equilibrium with a valid nonroot, using four candidates. No imported moderate/hard anchors are available.\n\nRegistered package: `'+result['generator']+'`. Evidence: `reference/edb-math/repairs/2026-11-02-equilibrium-generator/`.\n')

def main():
    assert json.loads((H/'repair-verification.json').read_text())['passed']
    for mode in ('desktop','phone','phone-active'):
        assert json.loads((H/mode/'rendering.json').read_text())['passed']
        assert json.loads((H/mode/'geometry.json').read_text())['passed']
    p=Publisher.from_environment(source=':agent/codex');work=H/'publication'
    lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
        c=GeneratorCommitter(p.config,p.client,work);request=c.pending()
        if request:apply(p,json.loads((work/'preparation.json').read_text()),c,request)
        elif not (H/'verification.json').exists():
            capture=json.loads((H/'capture.json').read_text());manifest=build_manifest(H/'package','generator.py',capture['files'],dependencies=capture['dependencies'])
            package=publish_package(H/'package','generator.py',capture['files'],p.config.math_root,dependencies=capture['dependencies'],expected_digest=manifest_digest(manifest))
            verify_package(package.directory,package.digest)
            for _ in range(5):
                request=None
                try:
                    prepared,c,request=prepare(p,package);apply(p,prepared,c,request);break
                except StaleBasis:
                    if request:c.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; refresh basis and usage'})
            else:raise RuntimeError('Repeated basis races; publication incomplete')
        install()

if __name__=='__main__':main()
