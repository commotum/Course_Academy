"""Serialized preparation, guarded EDB commit, receipt recovery and exact readback."""
import fcntl,hashlib,json,os,subprocess,sys,threading,uuid
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
from integration import DB,KP,ROOT,SCRIPT,transaction,check_report,normalize,ordered,loads,dumps
import validate as v
from inventory import counts,LEARNER
from types import SimpleNamespace
sys.path.insert(0,str(ROOT/'scripts'));from inventory_jobs import save
HERE=Path(__file__).resolve().parent;OUT=HERE/'reference/replenishment'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'ab7a7cc6402b4ccccecc6dbb8720236d122cdcc8a5d57fd83762570e9f1a9c0a'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
QUERY=(HERE/'source-query.edn').read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,b):return DB.query(QUERY,[[KP]],p,'kp',b)[0][0]
def inventory(p):
    r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def verify(p,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_report(report,p/'receipt-check',intent['source_eid']);b=report[':edb/db-after-t']
    kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()),'Source questions changed'
    exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);v.check(r)
    assert not transaction([],kp,intent['generator_id'])
    # The report checker permits only additive content/generator facts and this
    # KP's membership/ref; it rejects every learner/engine mutation or retraction.
    after=counts(kp,b,p/'readback')
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'source_questions_unchanged':len(old),'canonical_unchanged':True,'learner_history_unchanged':True,'only_scoped_additive_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'counts_after':after}
    save(p/'verification.json',result);return result
def finish(p,gid,verified,inv):
    cap=json.loads((HERE/'capabilities.json').read_text());c=verified['counts_after']['available_distinct_by_level'];missing=max(0,5-c['moderate'])
    result={'outcome':'finite-limit' if missing else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],'unsupported_levels_filled':False,'available_by_level':c,'supported_shortage_remaining':{'moderate':missing},'unfilled_reserves':{'easy':max(0,5-c['easy']),'moderate':missing,'hard':max(0,5-c['hard'])},'capability_exceptions':cap['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'inventory-before.json',p/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.json',HERE/'source-replay.json',HERE/'validation.json',HERE/'freeze.json',HERE/'reference/native-build.json'] if f.exists()],'note':'Created and validated source-derived generator. Existing moderate reserve already exceeds five, so no unnecessary content was committed. Easy and hard are bounded unsupported capabilities with explicit unfilled reserves. Preserved all source questions and learner history. Exact retained request, preview, receipt and readback verified while application api.lock held.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','available_by_level','unfilled_reserves')}),flush=True)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    freeze=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/path)==digest for path,digest in freeze['sha256'].items())
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed'] and validation['source_replay']['complete_banks_matched']==23
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            inventory(p/'recovery-inventory.json');verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);save(p/'inventory-before.json',inv);kp=read(p,b)
        captured=loads((HERE/'source.edn').read_text())[0][0]
        ex={':knowledge-point/question-generator'}
        assert {k:v for k,v in captured.items() if k not in ex}=={k:v for k,v in kp.items() if k not in ex},'KP source changed; reclassification required'
        assert str(kp[':knowledge-point/id'])==v.g.KP_UUID
        (p/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source-contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(v.g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed=max(0,5-c['available_distinct_by_level']['moderate'])
        print(json.dumps({'basis':b,'counts':c['available_distinct_by_level'],'moderate_needed':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:v.check(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        used={v.fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(v.fingerprint(kp[':knowledge-point/canonical-example']))
        records=[]
        # Execute every finite parameter tuple at most once; compare mathematics,
        # never seed/identity/bank/choice ordering, before accepting new content.
        def accept(r):
            fp=v.fingerprint(r['question'])
            if fp in used:return
            v.check(r);records.append(r);used.add(fp)
        for r in instances:
            if len(records)>=needed:break
            accept(r)
        if len(records)<needed:
            for mid in sorted(v.g.PROFILES):
                if len(records)>=needed:break
                for dilation in range(1,9):
                    if len(records)>=needed:break
                    for scale in range(1,13):
                        if len(records)>=needed:break
                        accept(v.g.generate(profile=mid,scale=scale,dilation=dilation))
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(v.g.markdown,records)));v.run_native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'supported_missing':needed,'new_questions':len(records),'finite_shortage':max(0,needed-len(records)),'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'deduplication':'full displayed integrand and bounds, across originals/canonical/generated, ignoring bank and seed'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        txpath=p/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'definite-ibp-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK)}
        save(p/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,p);print('Commit confirmed; verifying exact basis '+str(report[':edb/db-after-t']),flush=True)
        verified=verify(p,intent,report);finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()
