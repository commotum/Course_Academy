"""Remove a demonstrated one-application bypass from repeated-angle practice."""
import hashlib, json, platform, subprocess, sys
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[3]; sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher, GeneratorCommitter, StaleBasis, digest, loads, dumps, kw, file_lock, normalized_question, prepare_records, inventory_fingerprints, content_fingerprint
from scripts.generator_packages import publish_package, build_manifest, manifest_digest, verify_package
from capture.scripts.storage import atomic_json
from review_pool import numeric, solution_scope
KP=17592186059672
D=H/'repeated-angle-refinement'
F=ROOT/'generate/repairs/2026-11-04-four-trig-lessons/sine-double'/str(KP)
RETIRE={17592186749269,17592186749243,17592186749226,17592186749214}

def review(p):
    D.mkdir(exist_ok=True); proof=json.loads((H/'verification.json').read_text()); old=next(k for k in proof['kps'] if k['kp']==KP)
    manifest=json.loads((F/'runtime-manifest.json').read_text()); files=manifest['runtime_files']
    hashes={n:hashlib.sha256((F/n).read_bytes()).hexdigest() for n in files}
    before=p.read_kp(KP,D/'capture',p.client.status()['basis'])
    samples=[]; evidence=[]
    for band,count in [('easy',4),('moderate',10),('hard',10)]:
        raw=json.loads(subprocess.run([sys.executable,str(F/'generator.py'),'--difficulty',band,'--count',str(count),'--seed','20261106','--format','json'],check=True,capture_output=True,text=True).stdout)
        rows,_=prepare_records(raw,KP,before[':knowledge-point/id'],set(),Path('/tmp'),D)
        for i,r in enumerate(rows):
            key=numeric.audit(r['question'],f'{band}/{i}',str(KP)); sol=solution_scope['check'](r['question'],f'{band}/{i}',str(KP))
            assert key['status']=='match' and not key['choice_ambiguities'],key
            assert not sol.get('suspected_bad_equalities') and not sol.get('unparsed_equalities'),sol
            evidence.append({'key':key,'solution':sol})
        samples+=rows
    # c4/end30 already exists as imported moderate practice. Do not copy it
    # merely to inflate easy stock; preserve the two valid c8 cases already live.
    easy=next(r for r in samples if str(r['question'][':question/difficulty']).endswith('/easy') and r['generation']['parameters']['end_degrees']=='45' and r['generation']['parameters']['coefficient']=='4')
    fingerprints=inventory_fingerprints(before[':knowledge-point/questions'])
    hard=next(r for r in samples if str(r['question'][':question/difficulty']).endswith('/hard') and
              content_fingerprint(r['question']) not in fingerprints)
    assert hashes=={n:hashlib.sha256((F/n).read_bytes()).hexdigest() for n in files}
    dependencies={'python':platform.python_version(),'packages':{'sympy':'1.14.0'}}
    m=build_manifest(F,'generator.py',files,dependencies=dependencies)
    package=publish_package(F,'generator.py',files,p.config.math_root,dependencies=dependencies,expected_digest=manifest_digest(m)); verify_package(package.directory,package.digest)
    atomic_json(D/'review.json',{'passed':True,'runtime_sha256':hashes,'records':samples,'selected':[easy,hard],'checks':evidence,
        'source_clone_excluded':'coefficient4/end30 is imported moderate17592186060239','easy_mathematical_capacity':4,'easy_fresh_pool':3})
    from generate.pipeline import render_preview as renderer
    renderer.render([easy,hard],D/'desktop',[])
    original_script=renderer.BROWSER_SCRIPT
    try:
        renderer.BROWSER_SCRIPT=original_script.replace('width:1280,height:1000','width:390,height:844')
        renderer.render([easy,hard],D/'phone',[])
    finally:renderer.BROWSER_SCRIPT=original_script
    return old,package,[easy,hard]

def main():
    p=Publisher.from_environment(source=':agent/codex'); old,package,records=review(p)
    lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
        work=D/'publication'; c=GeneratorCommitter(p.config,p.client,work)
        if (D/'verification.json').exists(): return
        for attempt in range(5):
            request=c.pending()
            try:
                if request: prepared=json.loads((work/'preparation.json').read_text())
                else:
                    prepared=p.prepare(KP,records,package.reference,package.digest,work,
                        source_snapshot=json.loads((H/'source'/str(KP)/'source.json').read_text()),assets_directory=D,expected_registered_generator=old['generator'])
                    assert prepared['new_questions']==2 and prepared['duplicates']==0
                    before=loads(prepared['before_edn']); batch=loads(prepared['batch_edn'])
                    for q in before[':knowledge-point/questions']:
                        if q[':db/id'] not in RETIRE: continue
                        assert not q.get(':question/math-academy-id') and not q.get(':question/retired')
                        batch['forms'].append([kw('db/cas'),q[':db/id'],kw('question/retired'),q.get(':question/retired'),True])
                        batch['assertions'].append([q[':db/id'],kw('question/retired'),True])
                    prepared['batch_edn']=dumps(batch);atomic_json(work/'preparation.json',prepared)
                    c.preview(batch,loads(prepared['snapshot_edn']));request=c.save_request(batch,loads(prepared['snapshot_edn']),digest(prepared))
                receipt=c.submit(request); verification=c.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t']
                after=p.read_kp(KP,D/'after',basis);before=loads(prepared['before_edn']);now={q[':db/id']:q for q in after[':knowledge-point/questions']}
                for q in before[':knowledge-point/questions']:
                    expected=dict(q)
                    if q[':db/id'] in RETIRE:expected[kw('question/retired')]=True
                    assert now[q[':db/id']]==expected,q[':db/id']
                assert after[':knowledge-point/question-generator'][':question-generator/script']==package.reference
                assert len(now)==len(before[':knowledge-point/questions'])+2
                excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
                assert {k:v for k,v in before.items() if k not in excluded}=={k:v for k,v in after.items() if k not in excluded}
                added=[]
                for r in prepared['records']:
                    q=next(q for q in now.values() if str(q[':question/id'])==r['question'][':question/id'])
                    assert normalized_question(q)==normalized_question(r['question'])
                    added.append({'entity':q[':db/id'],'id':str(q[':question/id']),'level':str(q[':question/difficulty'][':db/ident']).split('/')[-1]})
                result={'passed':True,'generator':package.reference,'package_sha256':package.digest,'basis':basis,'retired':sorted(RETIRE),'new_questions':added,**verification}
                atomic_json(D/'verification.json',result);c.retire(request,'verified',result)
                proof=json.loads((H/'verification.json').read_text());atomic_json(H/'verification-initial.json',proof)
                if (H/'completion.json').exists():atomic_json(H/'completion-initial.json',json.loads((H/'completion.json').read_text()))
                current=next(k for k in proof['kps'] if k['kp']==KP)
                current.update(generator=package.reference,package_sha256=package.digest,basis_after=basis,
                    retired=sorted(set(current['retired'])|RETIRE),
                    new_questions=[q for q in current['new_questions'] if q['entity'] not in RETIRE]+added,
                    purpose_refinement=str((D/'verification.json').relative_to(ROOT)))
                proof.update(retired=sum(len(k['retired']) for k in proof['kps']),new=sum(len(k['new_questions']) for k in proof['kps']))
                atomic_json(H/'verification.json',proof);print(json.dumps(result),flush=True);break
            except StaleBasis:
                if request:c.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; refresh state'})
        else:raise RuntimeError('Repeated basis races')

if __name__=='__main__':main()
