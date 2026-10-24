"""Publish verified immutable successors and retire demonstrated descendants."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

H=Path(__file__).resolve().parent;ROOT=H.parents[3];MATH=Path('/media/jake/SSD/EDB/math')
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.edn import dumps,loads,kw
from scripts.generator_packages import publish_package,verify_package
from migrate_learner_history import connection


def save(name,value):(H/name).write_text(json.dumps(value,default=str,indent=2)+'\n')


def packages():
    plan=json.loads((H/'installation-plan.json').read_text());result=[]
    validated={r['kp']:r for r in json.loads((H/'runtime-validation.json').read_text())}
    for row in plan:
        assert any(r['returncode']==0 for r in validated[row['kp']]['results']),row['kp']
        assert hashlib.sha256(Path(row['entrypoint']).read_bytes()).hexdigest()==row['new_sha256']
        if not row['packaged']:continue
        oldref=row['registration'][':question-generator/script'];oldroot=MATH/Path(*Path(oldref).parts[:3])
        verify_package(oldroot,Path(oldref).parts[2])
        manifest=row['manifest']
        package=publish_package(H/'packages'/str(row['kp']),manifest['entrypoint'],manifest['files'],MATH,
            dependencies=manifest['dependencies'],expected_digest=row['digest'])
        result.append({'kp':row['kp'],'old_generator':row['registration'][':db/id'],
            'old_reference':oldref,'reference':package.reference,'digest':package.digest,
            'generator_id':str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:source-eligibility:'+str(row['kp'])+':'+package.digest))})
    save('published-packages.json',result);print('Published',len(result),'immutable successors; originals verified unchanged')


def prepare():
    assert not (H/'commit-intent.json').exists(),'Recover the exact retained intent first'
    db=connection();basis=db.basis()
    plan=json.loads((H/'installation-plan.json').read_text());pkgs=json.loads((H/'published-packages.json').read_text())
    rows=db.query('[:find (pull ?kp [:db/id {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/question-generator _]]',
        [[r['kp'] for r in plan]],H,'registrations-before',basis)
    actual={r[0][':db/id']:json.loads(json.dumps(r[0][':knowledge-point/question-generator'],default=str)) for r in rows}
    assert actual=={r['kp']:r['registration'] for r in plan},'Registration changed; reconcile current package before preparing'
    candidates=[r for r in json.loads((H/'question-dispositions.json').read_text()) if r['decision']=='retire-generated-descendant']
    rows=db.query('[:find (pull ?q [:db/id :question/id :question/math-academy-id :question/retired {:knowledge-point/_canonical-example [:db/id]} {:knowledge-point/_questions [:db/id]} {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',
        [[r[':db/id'] for r in candidates]],H,'retirements-before',basis)
    before={r[0][':db/id']:r[0] for r in rows};retired=[];forms=[]
    for row in candidates:
        q=before[row[':db/id']]
        assert str(q[':question/id'])==row[':question/id'] and not q.get(':question/math-academy-id')
        assert not q.get(':knowledge-point/_canonical-example'),'Canonical needs separate repair'
        if q.get(':question/retired') is True:continue
        retired.append(q)
        forms.append([kw('db/cas'),q[':db/id'],kw('question/retired'),q.get(':question/retired'),True])
    for row in pkgs:
        temp='source-eligible-'+str(row['kp'])
        forms.extend([{kw('db/id'):temp,kw('question-generator/id'):uuid.UUID(row['generator_id']),kw('question-generator/script'):row['reference']},
            [kw('db/cas'),row['kp'],kw('knowledge-point/question-generator'),row['old_generator'],temp]])
    affected_kps={k[':db/id'] for q in retired for k in q[':knowledge-point/_questions']}|{r['kp'] for r in pkgs}
    forms.extend([kw('db/ensure'),kp,kw('knowledge-point/validate')] for kp in sorted(affected_kps))
    payload=dumps(forms);(H/'transaction.edn').write_text(payload)
    save('preparation.json',{'basis':basis,'source':':agent/codex','retirements':retired,'packages':pkgs,
        'sha256':hashlib.sha256(payload.encode()).hexdigest(),'forms':len(forms),
        'authorization':'User: yeah, make the required fixes everywhere'})
    db.query('[:find ?ident ?e :where [?e :db/ident ?ident]]',[],H,'transaction-attributes',basis)
    print('Prepared',len(retired),'retirements and',len(pkgs),'registrations at T'+str(basis))


def check(report):
    prep=json.loads((H/'preparation.json').read_text());attrs=dict(loads((H/'transaction-attributes.edn').read_text()))
    expected=Counter()
    for row in prep['retirements']:
        if row.get(':question/retired') is not None:expected[(row[':db/id'],attrs[':question/retired'],str(row[':question/retired']),False)]+=1
        expected[(row[':db/id'],attrs[':question/retired'],'True',True)]+=1
    for row in prep['packages']:
        eid=report[':edb/tempids']['source-eligible-'+str(row['kp'])]
        expected[(eid,attrs[':question-generator/id'],row['generator_id'],True)]+=1
        expected[(eid,attrs[':question-generator/script'],row['reference'],True)]+=1
        expected[(row['kp'],attrs[':knowledge-point/question-generator'],str(row['old_generator']),False)]+=1
        expected[(row['kp'],attrs[':knowledge-point/question-generator'],str(eid),True)]+=1
    data=report[':edb/tx-data'];actual=Counter((d[0],d[1],str(d[2]),d[-1]) for d in data if d[1]!=attrs[':db/txInstant'])
    assert actual==expected,(actual-expected,expected-actual)
    assert all(d[-2]==attrs[':agent/codex'] for d in data)
    return prep


def preview():
    db=connection();native=preview_executable(SimpleNamespace(math_root=MATH,repo_root=ROOT,preview_bin=None),threading.Event())
    p=subprocess.run([str(native),'with','--database','math','--source',':agent/codex','--file',str(H/'transaction.edn')],env=db.env,check=True,capture_output=True,text=True,timeout=180)
    (H/'preview.edn').write_text(p.stdout);report=loads(p.stdout);prep=check(report)
    assert report[':edb/committed'] is False
    save('preview-verification.json',{'sha256':prep['sha256'],'basis':report[':edb/db-before-t'],'exact_datoms_verified':True,'native_validation_passed':True})
    print('Native preview passed; exact retirement/registration datoms verified')


def apply():
    db=connection();prep=json.loads((H/'preparation.json').read_text());v=json.loads((H/'preview-verification.json').read_text())
    assert v['exact_datoms_verified'] and v['sha256']==prep['sha256']==hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest()
    intent={'database':'math','source':':agent/codex','endpoint':'/tmp/edb-math/writer.sock',
        'sha256':prep['sha256'],'request_key':'repair-multistep-generators-2026-10-23-'+prep['sha256'][:24]}
    if (H/'commit-intent.json').exists():assert json.loads((H/'commit-intent.json').read_text())==intent
    else:save('commit-intent.json',intent)
    report=None
    if (H/'receipt.edn').exists():
        try:report=loads((H/'receipt.edn').read_text())
        except ValueError:pass
    if not report or report.get(':edb/committed') is not True:
        command=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',str(H/'transaction.edn'),
                 '--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000']
        with (H/'receipt.edn').open('w') as out,(H/'submission.stderr').open('w') as err:
            subprocess.run(command,env=db.env,stdout=out,stderr=err,timeout=160,check=True)
        report=loads((H/'receipt.edn').read_text())
    assert report[':edb/committed'] is True;check(report);basis=report[':edb/db-after-t']
    ids=[q[':db/id'] for q in prep['retirements']]
    rows=db.query('[:find (pull ?q [:db/id :question/id :question/retired {:knowledge-point/_questions [:db/id]} {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/retired true]]',
        [ids],H,'retirements-after',basis)
    assert len(rows)==len(ids)
    for [q] in rows:
        old=next(r for r in prep['retirements'] if r[':db/id']==q[':db/id'])
        for attr in [':question/id',':knowledge-point/_questions',':task-item/_content']:
            assert json.loads(json.dumps(q.get(attr),default=str))==old.get(attr),(q[':db/id'],attr)
    rows=db.query('[:find (pull ?kp [:db/id {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/question-generator _]]',
        [[r['kp'] for r in prep['packages']]],H,'registrations-after',basis)
    for [kp] in rows:
        pkg=next(r for r in prep['packages'] if r['kp']==kp[':db/id']);reg=kp[':knowledge-point/question-generator']
        assert str(reg[':question-generator/id'])==pkg['generator_id'] and reg[':question-generator/script']==pkg['reference']
        verify_package(MATH/Path(*Path(pkg['reference']).parts[:3]),pkg['digest'])
        verify_package(MATH/Path(*Path(pkg['old_reference']).parts[:3]),Path(pkg['old_reference']).parts[2])
    save('verification.json',{'committed':True,'basis':basis,'retired_questions':ids,'successor_packages':len(prep['packages']),
        'legacy_generators_repaired':46,'exact_datoms_verified':True,'question_ownership_and_saved_tasks_preserved':True,
        'original_packages_preserved':True,'request_key':intent['request_key']})
    print('Committed and verified T'+str(basis),len(ids),'retirements;',len(prep['packages']),'immutable successors')


if __name__=='__main__':
    {'packages':packages,'prepare':prepare,'preview':preview,'apply':apply}[sys.argv[1]]()
