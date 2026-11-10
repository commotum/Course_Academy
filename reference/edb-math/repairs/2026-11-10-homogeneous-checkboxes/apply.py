"""Submit the checked exact guarded request, retaining its durable receipt."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,loads

db=connection()
def read(name): return json.loads((H/(name+'.json')).read_text())
for name in ['speculative-verification','player-verification','api-before']:
    assert read(name)['passed'],name
assert not (H/'commit-intent.json').exists(),'Reconcile existing exact request first.'
validated=read('proposed-presentation')
if db.basis()!=read('plan')['basis']:
    archived=H/'preparations'/str(read('plan')['basis'])
    archived.mkdir(parents=True,exist_ok=True)
    for f in H.iterdir():
        if f.is_file() and f.suffix in ('.json','.edn','.txt','.stderr','.stdout'):
            shutil.copy2(f,archived/f.name)
    if (H/'preview').exists():shutil.copytree(H/'preview',archived/'preview',dirs_exist_ok=True)
    subprocess.run([sys.executable,str(H/'prepare.py')],check=True)
    assert read('proposed-presentation')==validated,'Question contents changed since the rendering/grading review.'
    subprocess.run([sys.executable,str(ROOT/'skills/radio2checkbox/scripts/lint_presentation.py'),str(H/'proposed-presentation.json'),'--output',str(H/'proposed-presentation-lint.json')],check=True)
    args=['/tmp/homogeneous-checkbox-native-preview','math',str(read('plan')['basis']),str(H/'preview'),':agent/codex',str(H/'transaction.edn')]
    for pattern,ids in [('question-pattern','question-ids'),('all-pattern','old-field-ids'),('all-pattern','old-answer-ids'),('all-pattern','item-ids')]:
        args+=['--pull',str(H/(pattern+'.edn')),str(H/(ids+'.edn'))]
    result=subprocess.run(args,env=db.env,capture_output=True,text=True)
    (H/'preview.stdout').write_text(result.stdout);(H/'preview.stderr').write_text(result.stderr)
    if result.returncode:
        print(result.stdout,result.stderr);raise SystemExit(result.returncode)
    subprocess.run([sys.executable,str(H/'check.py')],check=True)

plan=read('plan')
digest=hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest()
key='homogeneous-checkboxes-'+str(plan['basis'])+'-'+digest[:24]
intent=dict(database='math',source=plan['source'],source_entity=plan['source_entity'],basis=plan['basis'],
 endpoint='/tmp/edb-math/writer.sock',request_key=key,file=str(H/'transaction.edn'),sha256=digest,
 authorization='User requested both named questions and all similar questions in this lesson be converted to checkboxes.')
(H/'commit-intent.json').write_text(json.dumps(intent,indent=2)+'\n')
command=[db.args.edb_bin,'transact','--database','math','--file',intent['file'],'--request-key',key,
 '--source',plan['source'],'--endpoint',intent['endpoint'],'--basis',str(plan['basis'])]
result=subprocess.run(command,env=db.env,capture_output=True,text=True,timeout=210)
(H/'submit.stderr').write_text(result.stderr)
(H/('receipt.edn' if result.returncode==0 else 'submit-rejection-or-unknown.stdout')).write_text(result.stdout)
if result.returncode:
    print(result.stderr);raise SystemExit(result.returncode)
receipt=loads(result.stdout)
assert receipt[':edb/db-before-t']==plan['basis']
print(json.dumps(dict(committed=True,basis_before=plan['basis'],basis_after=receipt[':edb/db-after-t'],request_key=key,datoms=len(receipt[':edb/tx-data']))))
