"""Register the reviewed package, retire unused old stock, and refill atomically."""
import json,os,platform,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock,normalized_question,jsonable
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,materialize_package,verify_package
from capture.scripts.storage import atomic_json
KP=17592186105906

def prepare(p):
    assert json.loads((H/'generator-verification.json').read_text())['passed']
    assert json.loads((H/'grader-verification.json').read_text())['documented_unresolved_checks']==0
    assert json.loads((H/'render/rendering.json').read_text())['passed']
    captured=json.loads((H/'capture.json').read_text());work=H/'publication'
    files=[*captured['files'],'triangle_complement_contract.py']
    dependencies={'python':platform.python_version(),'packages':{'matplotlib':'3.11.2'}}
    manifest=build_manifest(H/'package','generator.py',files,dependencies=dependencies)
    package=publish_package(H/'package','generator.py',files,p.config.math_root,dependencies=dependencies,expected_digest=manifest_digest(manifest))
    runtime=work/'runtime'/package.digest
    entry=runtime/'generator.py' if runtime.exists() else materialize_package(package.reference,p.config.math_root,runtime)
    verify_package(runtime,package.digest)
    records=json.loads((H/'candidate-pool.json').read_text());reproduced=[]
    for i,level in enumerate(('easy','moderate','hard')):
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(H/'relocated-assets')}
        out=subprocess.run([sys.executable,str(entry),'--difficulty',level,'--count','5','--seed',str(20261027+137*i)],check=True,capture_output=True,text=True,timeout=90,env=env)
        reproduced+=json.loads(out.stdout)
    assert reproduced==records
    prepared=p.prepare(KP,records,package.reference,package.digest,work,source_snapshot=json.loads((H/'fresh-source/source.json').read_text()),assets_directory=H/'assets',expected_registered_generator=captured['registered_generator'])
    assert prepared['new_questions']==15 and prepared['duplicates']==0
    before=loads(prepared['before_edn']);old=json.loads((H/'before.json').read_text())
    active=[q for q in before[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
    assert {q[':db/id'] for q in active}=={q[':db/id'] for q in old[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')}
    ids=[q[':db/id'] for q in active]
    usage=p.client.query('[:find ?q ?item :in $ [?q ...] :where [?q :question/answer-fields ?f] [?f :answer-field/choices ?a] [?item :task-item/responses ?a]]',[ids],work,'response-usage',prepared['basis'])
    rows=p.client.query('[:find (pull ?q [:db/id :question/retired {:task-item/_content [:db/id]} {:knowledge-point/_canonical-example [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[ids],work,'old-stock-usage',prepared['basis'])
    used={q for q,item in usage}|{q[':db/id'] for [q] in rows if q.get(':task-item/_content')}
    retire=[q for [q] in rows if q[':db/id'] not in used and not q.get(':knowledge-point/_canonical-example')]
    batch=loads(prepared['batch_edn'])
    for q in retire:
        old_value=q.get(':question/retired');batch['forms'].append([kw('db/cas'),q[':db/id'],kw('question/retired'),old_value,True]);batch['assertions'].append([q[':db/id'],kw('question/retired'),True])
        if old_value is False:batch['retractions'].append([q[':db/id'],kw('question/retired'),False])
    prepared.update(batch_edn=dumps(batch),retirements=jsonable(retire),preserved_used=sorted(used),package_manifest=manifest)
    atomic_json(work/'preparation.json',prepared)
    committer=GeneratorCommitter(p.config,p.client,work);committer.preview(batch,loads(prepared['snapshot_edn']))
    request=committer.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared))
    return prepared,committer,request

def apply(p,prepared,committer,request):
    assert request['content_sha256']==digest(prepared)
    receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t']
    after=p.read_kp(KP,H/'publication/after',basis);before=loads(prepared['before_edn']);retired={q[':db/id'] for q in prepared['retirements']}
    now={str(q[':question/id']):q for q in after[':knowledge-point/questions']}
    assert len(now)==len(before[':knowledge-point/questions'])+15
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in retired:expected[kw('question/retired')]=True
        assert now[str(q[':question/id'])]==expected,('Changed existing content',q[':db/id'])
    final=[]
    for record in prepared['records']:
        q=now[record['question'][':question/id']]
        assert normalized_question(q)==normalized_question(record['question']) and not q.get(':question/retired')
        final.append({'entity':q[':db/id'],'uuid':str(q[':question/id']),'band':record['question'][':question/difficulty']})
    exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in after.items() if k not in exclude}
    assert after[':knowledge-point/question-generator'][':question-generator/script']==prepared['generator_path']
    active={q[':db/id'] for q in now.values() if not q.get(':question/math-academy-id') and not q.get(':question/retired')}
    assert active=={r['entity'] for r in final}|set(prepared['preserved_used'])
    result={'passed':True,'committed':True,'basis_after':basis,'new_reference':prepared['generator_path'],'new_questions':final,'retired_questions':sorted(retired),'preserved_used_questions':prepared['preserved_used'],'imported_questions_preserved':sum(bool(q.get(':question/math-academy-id')) for q in before[':knowledge-point/questions']),'canonical_preserved':True,'existing_questions_fields_answers_unchanged':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);committer.retire(request,'verified',result)
    print('Committed at',basis,':',len(retired),'unused questions retired;',len(final),'new questions;',len(prepared['preserved_used']),'used records preserved',flush=True)

def install(p):
    result=json.loads((H/'verification.json').read_text());runtime=H/'publication/runtime'/Path(result['new_reference']).parts[2]
    local=ROOT/f'generate/scratch/{KP}';local.mkdir(exist_ok=True)
    for name in json.loads((runtime/'generator-package.json').read_text())['files']:
        out=local/name
        if out.exists():out.chmod(out.stat().st_mode|0o200)
        shutil.copy2(runtime/name,out);out.chmod(out.stat().st_mode|0o200)
    (ROOT/f'generate/scratch/{KP}.py').write_text('import runpy,sys\nfrom pathlib import Path\nLOCAL=Path(__file__).with_suffix("")\nsys.path.insert(0,str(LOCAL))\nif __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")\n')
    (local/'README.md').write_text('# Triangle area from a quadrilateral area\n\nVersion 3.0.0 preserves the sine-area calculation and area subtraction in all bands. Easy uses small convenient whole numbers; moderate uses odd whole-number sides; hard uses one simple decimal side. Calculator use and final-only rounding are shared. These are authored numerical bands: the 12 imported practice records supply 11 hard labels and one unclassified record, with no easy/moderate anchors.\n\nRepair, publication and verification: `reference/edb-math/repairs/2026-10-27-triangle-area-progression/`. Earlier reports describe superseded generators.\n')
    atomic_json(local/'capabilities.json',{'knowledge_point':KP,'version':'3.0.0','supported_levels':{level:{'origin':'authored numerical progression','method':method,'target':5} for level,method in [('easy','small integer half-product, sine area, subtraction'),('moderate','half-integer half-product, sine area, subtraction'),('hard','quarter-valued half-product from one decimal side, sine area, subtraction')]},'source_evidence':{'imported_practice':12,'hard':11,'unclassified':1,'canonical':1},'limitations':['Difficulty differences are deliberately modest and have not been empirically calibrated.','The incomplete unclassified imported question is unchanged.'],'contract':'triangle-complement-full-calculation-v1'})

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
            else:raise RuntimeError('Publication raced repeatedly; saved evidence retained')
        install(p)

if __name__=='__main__':main()
