"""Preview, verify, and submit one guarded, authorized checkbox migration."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from prepare import HERE, DB, SOURCE, m, prepare
from scripts.database.edn import loads

def save(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')

def by_id(rows):return {q[':db/id']:q for q in rows}

receipt_path=HERE/'receipt.edn'
intent_path=HERE/'commit-intent.json'
if not intent_path.exists():
    prepare()
    plan=json.loads((HERE/'plan.json').read_text())
    result=subprocess.run([str(HERE/'native/preview'),str(HERE),SOURCE,str(plan['basis'])],
                          env=DB.environment,capture_output=True,text=True,timeout=150)
    (HERE/'preview.stderr').write_text(result.stderr)
    result.check_returncode()
    (HERE/'preview.edn').write_text(result.stdout)
    report=m.loads(result.stdout)
    m.verify_preview(report)
    before=by_id(loads((HERE/'preview-questions-before.edn').read_text()))
    after=by_id(loads((HERE/'preview-questions-after.edn').read_text()))
    snapshot=loads((HERE/'snapshot.edn').read_text())
    audited={q[':db/id']:q for [q] in snapshot['questions']}
    for q in plan['questions']:
        eid=q['id'];assert before[eid]==audited[eid]
        assert after[eid][':question/problem']==q['problem_after']
        omit=lambda d:{k:v for k,v in d.items() if k not in (':question/problem',':question/answer-fields')}
        assert omit(before[eid])==omit(after[eid])
        assert {f[':answer-field/key'] for f in after[eid][':question/answer-fields']}==set(q['labels'])
    for group in ('retained','items'):
        assert loads((HERE/f'preview-{group}-before.edn').read_text())==loads((HERE/f'preview-{group}-after.edn').read_text())
    subprocess.run([sys.executable,str(HERE/'native/check_native.py')],check=True,env=DB.environment)
    save('preview-preservation.json',{'passed':True,'questions':2,'retained_original_entities':12,
         'task_items_unchanged':1,'solutions_difficulties_memberships_unchanged':True})
    if '--preview-only' in sys.argv:
        print('Preview and native grading passed; no write requested by this invocation.')
        sys.exit(0)
    intent=json.loads((HERE/'prepared-request.json').read_text())
    intent.update(state='ready_for_submission',lineage=snapshot['lineage'])
    save('commit-intent.json',intent)
else:
    intent=json.loads(intent_path.read_text())

transaction=Path(intent['transaction_file'])
assert hashlib.sha256(transaction.read_bytes()).hexdigest()==intent['sha256']
if not receipt_path.exists():
    # Retain this exact request on transport failure; a retry must reuse it.
    output=DB.command('transact','--source',intent['source'],'--file',transaction,
        '--basis',intent['basis'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],
        '--timeout-ms','120000',timeout=150)
    receipt_path.write_text(output)
committed=m.loads(receipt_path.read_text())
assert committed[':edb/committed'] is True
m.verify_preview(committed,committed=True)
basis=committed[':edb/basis-t']
preview=m.loads((HERE/'preview.edn').read_text())
remap={eid:committed[':edb/tempids'][temp] for temp,eid in preview[':edb/tempids'].items()}
def durable(x):
    if isinstance(x,int):return remap.get(x,x)
    if isinstance(x,list):return [durable(v) for v in x]
    if isinstance(x,dict):return {k:durable(v) for k,v in x.items()}
    return x
for group,pattern,ids in loads((HERE/'native-pulls.edn').read_text()):
    rows=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',
                   [ids],HERE/'committed','read-'+group,basis)
    expected=durable(loads((HERE/f'preview-{group}-after.edn').read_text()))
    assert by_id([r[0] for r in rows])==by_id(expected),group
    if group in ('retained','items'):
        historical=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',
                     [ids],HERE/'committed','history-'+group,intent['basis'])
        assert by_id([r[0] for r in historical])==by_id([r[0] for r in rows])
plan=json.loads((HERE/'plan.json').read_text())
report={'committed':True,'basis_before':intent['basis'],'basis_after':basis,'lineage':intent['lineage'],
        'source':intent['source'],'request_key':intent['request_key'],'transaction_sha256':intent['sha256'],
        'converted_ids':[q['id'] for q in plan['questions']],'counts':plan['counts'],
        'exact_committed_readback':True,'native_grading_passed':True,
        'original_fields_answers_retained_unchanged':True,'saved_task_state_preserved':True,
        'solutions_difficulty_memberships_preserved':True,'historical_readback_matches':True}
save('verification.json',report)
save('status.json',{**report,'stage':'committed_verified','committed_ids':report['converted_ids'],'unsubmitted_ids':[]})
print(json.dumps(report))
