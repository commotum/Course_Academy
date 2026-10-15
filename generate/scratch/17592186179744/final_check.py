"""Verify final local runtime and exact registration receipt under api.lock."""
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import replenish as r

def main():
    freeze=json.loads((HERE/'reference/freeze.json').read_text())
    assert freeze['status']=='validated'
    assert all(r.sha(r.ROOT/p)==h for p,h in freeze['hashes'].items())
    path=HERE/'reference/replenishment/basis-2644'
    intent=json.loads((path/'commit-intent.json').read_text())
    receipt=r.loads((path/'commit.edn').read_text())
    assert intent['exact_edn']==(path/'transaction.edn').read_text()
    assert r.sha(path/'transaction.edn')==intent['transaction_sha256']
    assert r.sha(path/'generator-at-registration.py')==intent['generator_sha256']
    assert receipt[':edb/committed'] and receipt[':edb/db-before-t']==2644 and receipt[':edb/db-after-t']==2645
    assert intent['source']==r.SOURCE and intent['lineage']==r.LINEAGE
    with (r.ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        inv=r.inventory(HERE/'reference/inventory-final.json')
        basis=inv['basis'];assert r.DB.basis()==basis
        kp=r.read_kp(HERE/'reference/final-readback',basis)
        gen=kp[':knowledge-point/question-generator']
        assert str(gen[':question-generator/id'])==intent['generator_id']
        assert gen[':question-generator/script']==r.SCRIPT
        assert not r.transaction([],kp,intent['generator_id'])
        before={str(q[':question/id']):q for q in r.g.SOURCE['record'][':knowledge-point/questions']}
        after={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
        assert before.keys()==after.keys()
        assert all(r.canonical(q,True)==r.canonical(after[k],True) for k,q in before.items())
        assert r.canonical(kp[':knowledge-point/canonical-example'],True)==r.canonical(r.g.SOURCE['record'][':knowledge-point/canonical-example'],True)
        assert not [j for j in inv['jobs'] if j['knowledgePoint']==r.KP]
        cli=json.loads((HERE/'reference/cli-preview.json').read_text());assert len(cli)==5
        native=json.loads((HERE/'reference/cli-native-report.json').read_text())
        assert (native['accepted_checks'],native['rejected_checks'],native['documented_unresolved_checks'])==(5,20,0)
        validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
        runtime={'passed':True,'current_basis':basis,'verified_commit_basis':2645,'generator_id':intent['generator_id'],
            'generator_script':r.SCRIPT,'current_generator_version':r.g.VERSION,'current_generator_sha256':r.sha(HERE.with_suffix('.py')),
            'generator_at_registration_sha256':intent['generator_sha256'],'source_questions_unchanged':len(before),
            'registration_idempotent':True,'system_python_cli':'passed using existing repository environment',
            'cli_distinct_tasks':len({x['generation']['mathematical_task_fingerprint'] for x in cli}),
            'cli_grading':{'accepted':5,'rejected':20,'unresolved':0},'full_validation':validation['grading'],
            'registration_receipt_and_exact_request_verified':True,'durable_database_writes_in_final_check':0}
        r.save(HERE/'reference/runtime-verification.json',runtime)
        result=json.loads(r.JOB.with_suffix('.result').read_text())
        result.update({'generator_version':r.g.VERSION,'generator_sha256':runtime['current_generator_sha256'],
            'inventory_recheck_basis':basis,'runtime_verified':True,'new_questions':0,
            'evidence':result['evidence']+[str(p.relative_to(r.ROOT)) for p in (
                HERE/'reference/runtime-verification.json',HERE/'reference/cli-native-report.json',
                HERE/'reference/inventory-final.json',path/'generator-at-registration.py',path/'freeze-at-registration.json',
                path/'validation-at-registration.json',HERE/'reference/side-by-side.md')]})
        r.save(path/'outcome.json',result);r.save(r.JOB.with_suffix('.result'),result)
        print(json.dumps({'outcome':result['outcome'],'verified_commit_basis':2645,'current_basis':basis,
            'available_easy':8,'new_questions':0,'runtime_verified':True,'unsupported_shortage':result['unsupported_shortage']}))

if __name__=='__main__':main()
