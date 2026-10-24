"""Install the validated successor and withdraw the identity-only descendant."""
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
from capture.scripts.database.edn import dumps,loads,kw
from capture.scripts.database.preview import preview_executable
from scripts.generator_packages import build_manifest,manifest_digest,publish_package,verify_package,materialize_package
from migrate_learner_history import connection

def save(name,value):(H/name).write_text(json.dumps(value,default=str,indent=2)+'\n')

def prepare():
    assert not (H/'intent.json').exists(),'Recover retained intent first'
    check=json.loads((H/'generator-verification.json').read_text());assert check['withdrawals']==[17592186576201]
    assert json.loads((H/'grader-verification.json').read_text())['accepted_checks']==24
    old=json.loads((H/'original-package-manifest.json').read_text())
    manifest=build_manifest(H/'package',old['entrypoint'],old['files'],dependencies=old['dependencies']);digest=manifest_digest(manifest)
    pkg=publish_package(H/'package',manifest['entrypoint'],manifest['files'],MATH,dependencies=manifest['dependencies'],expected_digest=digest)
    dest=H/'published-runtime'
    if not dest.exists():entry=materialize_package(pkg.reference,MATH,dest)
    else:verify_package(dest,digest);entry=dest/manifest['entrypoint']
    p=subprocess.run([sys.executable,str(entry),'--difficulty','easy','--count','25','--seed','271828','--format','json'],check=True,capture_output=True,text=True)
    rows=json.loads(p.stdout);assert len(rows)==25 and all(r['generation']['region']!='equal' for r in rows)
    original=json.loads((H/'kp-before.json').read_text())['kp'];reg=original[':knowledge-point/question-generator']
    db=connection();basis=db.basis()
    query='[:find (pull ?kp [:db/id {:knowledge-point/question-generator [*]}]) (pull ?q [:db/id :question/id :question/retired {:task-item/_content [:db/id]}]) :in $ ?kp ?q :where [?kp :knowledge-point/questions ?q]]'
    rows=db.query(query,[17592186054745,17592186576201],H,'preparation-before',basis);assert len(rows)==1
    kp,q=rows[0];assert json.loads(json.dumps(kp[':knowledge-point/question-generator'],default=str))==reg
    assert str(q[':question/id'])=='f5daa79d-c02f-5774-b003-6dd284769848' and not q.get(':question/retired')
    gid=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:calculator-change-base:'+digest))
    forms=[{kw('db/id'):'calculator-successor',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):pkg.reference},
           [kw('db/cas'),17592186054745,kw('knowledge-point/question-generator'),reg[':db/id'],'calculator-successor'],
           [kw('db/cas'),17592186576201,kw('question/retired'),q.get(':question/retired'),True],
           [kw('db/ensure'),17592186054745,kw('knowledge-point/validate')]]
    payload=dumps(forms);(H/'transaction.edn').write_text(payload)
    save('preparation.json',{'basis':basis,'before':q,'old_generator':reg,'new_generator_id':gid,'reference':pkg.reference,
        'digest':digest,'sha256':hashlib.sha256(payload.encode()).hexdigest(),'published_package_records_checked':25})
    db.query('[:find ?i ?e :where [?e :db/ident ?i]]',[],H,'attributes',basis)
    native=preview_executable(SimpleNamespace(math_root=MATH,repo_root=ROOT,preview_bin=None),threading.Event())
    p=subprocess.run([str(native),'with','--database','math','--source',':agent/codex','--file',str(H/'transaction.edn')],check=True,env=db.env,capture_output=True,text=True,timeout=180)
    (H/'preview.edn').write_text(p.stdout);report=loads(p.stdout);validate(report)
    assert report[':edb/committed'] is False
    save('preview-verification.json',{'exact_datoms_verified':True,'native_validation_passed':True,'sha256':hashlib.sha256(payload.encode()).hexdigest()})
    print('Successor published, relocated and checked; guarded native preview passed')

def validate(report):
    p=json.loads((H/'preparation.json').read_text());attrs=dict(loads((H/'attributes.edn').read_text()));new=report[':edb/tempids']['calculator-successor']
    expected=Counter([(17592186576201,attrs[':question/retired'],'True',True),
        (17592186054745,attrs[':knowledge-point/question-generator'],str(p['old_generator'][':db/id']),False),
        (17592186054745,attrs[':knowledge-point/question-generator'],str(new),True),
        (new,attrs[':question-generator/id'],p['new_generator_id'],True),
        (new,attrs[':question-generator/script'],p['reference'],True)])
    data=report[':edb/tx-data'];actual=Counter((d[0],d[1],str(d[2]),d[-1]) for d in data if d[1]!=attrs[':db/txInstant'])
    assert actual==expected,(actual-expected,expected-actual)
    assert all(d[-2]==attrs[':agent/codex'] for d in data)

def apply():
    p=json.loads((H/'preparation.json').read_text());preview=json.loads((H/'preview-verification.json').read_text())
    assert preview['exact_datoms_verified'] and preview['sha256']==p['sha256']==hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest()
    intent={'request_key':'repair-logarithm-degenerate-2026-10-24-'+p['sha256'][:24],'sha256':p['sha256'],'source':':agent/codex'}
    if (H/'intent.json').exists():assert json.loads((H/'intent.json').read_text())==intent
    else:save('intent.json',intent)
    db=connection();receipt=None
    if (H/'receipt.edn').exists():
        try:receipt=loads((H/'receipt.edn').read_text())
        except ValueError:pass
    if not receipt or receipt.get(':edb/committed') is not True:
        command=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',str(H/'transaction.edn'),
                 '--endpoint','/tmp/edb-math/writer.sock','--request-key',intent['request_key'],'--timeout-ms','120000']
        with (H/'receipt.edn').open('w') as out,(H/'submit.stderr').open('w') as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,check=True,timeout=160)
        receipt=loads((H/'receipt.edn').read_text())
    assert receipt[':edb/committed'] is True;validate(receipt);basis=receipt[':edb/db-after-t']
    query='[:find (pull ?kp [:db/id {:knowledge-point/question-generator [*]}]) (pull ?q [:db/id :question/id :question/retired {:task-item/_content [:db/id]}]) :in $ ?kp ?q :where [?kp :knowledge-point/questions ?q]]'
    rows=db.query(query,[17592186054745,17592186576201],H,'after',basis);kp,q=rows[0]
    assert q[':question/retired'] is True and str(q[':question/id'])==p['before'][':question/id']
    assert q.get(':task-item/_content')==p['before'].get(':task-item/_content')
    assert kp[':knowledge-point/question-generator'][':question-generator/script']==p['reference']
    verify_package(MATH/Path(*Path(p['reference']).parts[:3]),p['digest'])
    old=p['old_generator'][':question-generator/script'];verify_package(MATH/Path(*Path(old).parts[:3]),Path(old).parts[2])
    save('verification.json',{'committed':True,'basis':basis,'retired_question':17592186576201,'new_reference':p['reference'],
        'exact_datoms_verified':True,'saved_attempt_references_preserved':True,'original_package_preserved':True})
    print('Committed and verified T'+str(basis))

if __name__=='__main__':{'prepare':prepare,'apply':apply}[sys.argv[1]]()
