"""Publish a new immutable package, preview guarded content edits, retain receipt."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
MATH = Path('/media/jake/SSD/EDB/math')
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
from scripts.generator_packages import build_manifest, manifest_digest, publish_package, verify_package
sys.path.insert(0, str(ROOT/'scripts'))
from migrate_learner_history import connection, dumps, loads, kw
sys.path.insert(0, str(ROOT/'generate/scratch/17592186064281'))
from db_support import PATTERN


def save(name, value):
    (H/name).write_text(json.dumps(value,indent=2)+'\n')


def publish():
    original=json.loads((H/'product-log-original-manifest.json').read_text())
    manifest=build_manifest(H/'product-log-package',original['entrypoint'],original['files'],dependencies=original['dependencies'])
    assert all(manifest['files'][f]==original['files'][f] for f in original['files'] if f!='generator.py')
    assert json.loads((H/'grading-report.json').read_text())['documented_unresolved_checks']==0
    assert json.loads((H/'fresh-product-grading-report.json').read_text())['documented_unresolved_checks']==0
    assert json.loads((H/'render/rendering.json').read_text())['passed']
    digest=manifest_digest(manifest)
    package=publish_package(H/'product-log-package',original['entrypoint'],original['files'],MATH,
                            dependencies=original['dependencies'],expected_digest=digest)
    verify_package(package.directory)
    save('package-publication.json',{'reference':package.reference,'digest':digest,
        'generator_id':str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+digest)),
        'manifest':manifest,'original_package_preserved':True})
    print(package.reference)


def check(report,changes,package):
    attrs=dict(loads((H/'attributes.edn').read_text()))
    expected=Counter((r['entity'],attrs[kw(r['attribute'])],value,added) for r in changes
                     for value,added in [(r['before'],False),(r['after'],True)])
    before=json.loads((H/'before.json').read_text())['records']
    kp=next(r for r in before if r[':db/id']==17592186096618)
    new=report[':edb/tempids']['generator-successor']
    expected.update([(kp[':db/id'],attrs[kw('knowledge-point/question-generator')],kp[':knowledge-point/question-generator'][':db/id'],False),
                     (kp[':db/id'],attrs[kw('knowledge-point/question-generator')],new,True),
                     (new,attrs[kw('question-generator/id')],uuid.UUID(package['generator_id']),True),
                     (new,attrs[kw('question-generator/script')],package['reference'],True)])
    observed=Counter((d[0],d[1],d[2],d[-1]) for d in report[':edb/tx-data'] if d[1]!=attrs[kw('db/txInstant')])
    assert observed==expected
    assert all(d[-2]==attrs[kw('agent/codex')] for d in report[':edb/tx-data'])
    return new


def prepare():
    assert not (H/'commit-intent.json').exists(),'Recover the retained request first'
    db=connection();basis=db.basis();changes=json.loads((H/'changes.json').read_text());package=json.loads((H/'package-publication.json').read_text())
    attributes=['db/txInstant','agent/codex','answer/value','question/problem','question/worked-solution',
                'knowledge-point/question-generator','question-generator/id','question-generator/script']
    db.query('[:find ?i ?e :in $ [?i ...] :where [?e :db/ident ?i]]',[[kw(a) for a in attributes]],H,'attributes',basis)
    forms=[]
    for r in changes:
        forms.append([kw('db/cas'),r['entity'],kw(r['attribute']),r['before'],r['after']])
        if r['attribute']=='answer/value':forms.append([kw('db/ensure'),r['entity'],kw('answer/validate')])
    questions=sorted({r['question'] for r in changes})
    for q in questions:forms.append([kw('db/ensure'),q,kw('question/validate')])
    kp=next(r for r in json.loads((H/'before.json').read_text())['records'] if r[':db/id']==17592186096618)
    forms.extend([{kw('db/id'):'generator-successor',kw('question-generator/id'):uuid.UUID(package['generator_id']),
                   kw('question-generator/script'):package['reference']},
                  [kw('db/cas'),kp[':db/id'],kw('knowledge-point/question-generator'),kp[':knowledge-point/question-generator'][':db/id'],'generator-successor']])
    (H/'transaction.edn').write_text(dumps(forms))
    native=preview_executable(SimpleNamespace(math_root=MATH,repo_root=ROOT,preview_bin=None),threading.Event())
    result=subprocess.run([str(native),'with','--database','math','--source',':agent/codex','--file',str(H/'transaction.edn')],env=db.env,check=True,capture_output=True,text=True)
    (H/'preview.edn').write_text(result.stdout);report=loads(result.stdout)
    assert report[':edb/committed'] is False
    check(report,changes,package)
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/f'generate/scratch/{k}.py' for k in (17592186124470,17592186198361,17592186129268)]}
    save('preparation.json',{'basis':report[':edb/db-before-t'],'questions':questions,'changes':len(changes),
         'source_hashes':source_hashes,'transaction_sha256':hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest(),
         'exact_preview_verified':True})
    print('Preview verified:',len(questions),'questions;',len(changes),'content values; new package registration')


def apply():
    db=connection();prep=json.loads((H/'preparation.json').read_text());package=json.loads((H/'package-publication.json').read_text());changes=json.loads((H/'changes.json').read_text())
    for path,digest in prep['source_hashes'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
    assert hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest()==prep['transaction_sha256']
    verify_package(MATH/Path(package['reference']).parent)
    intent={'database':'math','source':':agent/codex','endpoint':'/tmp/edb-math/writer.sock','file':str(H/'transaction.edn'),
            'sha256':prep['transaction_sha256'],'request_key':'repair-solution-paths-2026-10-23-'+prep['transaction_sha256'][:24]}
    if (H/'commit-intent.json').exists():assert json.loads((H/'commit-intent.json').read_text())==intent
    else:save('commit-intent.json',intent)
    if (H/'receipt.edn').exists():report=loads((H/'receipt.edn').read_text())
    else:
        result=db.command('transact','--source',intent['source'],'--endpoint',intent['endpoint'],'--file',intent['file'],'--request-key',intent['request_key'])
        (H/'receipt.edn').write_text(result);report=loads(result)
    assert report[':edb/committed'] is True
    new=check(report,changes,package);basis=report[':edb/db-after-t']
    rows=db.query('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]',
                  [[[r['entity'],kw(r['attribute'])] for r in changes]],H,'values-after',basis)
    assert {(r[0],str(r[1])):r[2] for r in rows}=={(r['entity'],':'+r['attribute']):r['after'] for r in changes}
    before=loads((H/'before.edn').read_text());inequality=loads((H/'inequality-before.edn').read_text())
    expected={q[':db/id']:q for row in before+inequality for q in row[0][':knowledge-point/questions'] if q[':db/id'] in prep['questions']}
    for q in expected.values():
        for r in changes:
            if r['entity']==q[':db/id']:q[kw(r['attribute'])]=r['after']
        for field in q[':question/answer-fields']:
            for answer in field[':answer-field/choices']+[field.get(':answer-field/correct',{})]:
                for r in changes:
                    if answer.get(':db/id')==r['entity']:answer[kw(r['attribute'])]=r['after']
    from db_support import QUESTION
    after=db.query('[:find (pull ?q '+QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',[prep['questions']],H,'questions-after',basis)
    assert {row[0][':db/id']:row[0] for row in after}==expected
    reg=db.query('[:find ?g ?script :in $ ?kp :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?script]]',[17592186096618],H,'registration-after',basis)
    assert reg==[[new,package['reference']]]
    save('verification.json',{'committed':True,'basis_t':basis,'questions':prep['questions'],'question_count':len(prep['questions']),
         'content_values':len(changes),'exact_datoms_and_readback_verified':True,'owned_question_trees_verified':True,
         'identities_keys_and_learner_state_preserved':True,'new_generator':new,'new_script':package['reference']})
    print((H/'verification.json').read_text())


if __name__=='__main__':
    {'publish':publish,'prepare':prepare,'apply':apply}[sys.argv[1]]()
