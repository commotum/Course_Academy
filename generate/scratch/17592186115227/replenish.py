"""Locked additive replenish, exact-request recovery and exact-basis verification."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from integration import DB,LINEAGE,LEARNER,read_kp,inventory,build_learning,preview_executable,save,dumps,loads,kw
import validate as v
g=v.g;KP=g.KP_ID;SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'7f1b963f4add4fb0996d096a8de069a349a3492a2c8f3821aed28a4953f3dbb0'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
LOCK=ROOT/'.local/learning/requests/math/api.lock'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k:v for k,v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        assert g.fingerprint(q) == rec['generation']['mathematical_fingerprint']
        for ref in __import__('re').findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']+'\n'+q[':question/worked-solution']):
            assert ref.startswith('images/') and (Path('/media/jake/SSD/EDB/math')/ref).is_file()
        v.check(rec)
    for asset in json.loads((path/'preparation.json').read_text())['asset_hashes']:
        assert sha(Path('/media/jake/SSD/EDB/math')/asset['database_path'])==asset['sha256']
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in g.LEVELS}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'assets_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result


def counts(kp,native):
    validated={r['id'] for r in json.loads((HERE/'source-inventory-validation.json').read_text())['accepted']}
    available=set(native['available_questions']);byid={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    packages=[]
    for file in OUT.glob('basis-*/generated.json'):packages.extend(json.loads(file.read_text()))
    for eid,q in byid.items():
        if eid not in validated:
            for rec in packages:
                if str(q[':question/id'])==rec['question'][':question/id'] and normalize(q)==ordered(rec['question']):
                    v.check(rec);validated.add(eid);break
    return {level:len({g.fingerprint(byid[eid]) for eid in available&validated if str(byid[eid][':question/difficulty'][':db/ident'])==':question.difficulty/'+level}) for level in g.LEVELS}

def finish(path,intent,verified,binary):
    inv,native=inventory(binary,path/'inventory-after.json')
    kp=read_kp(path/'inventory-readback',inv['basis']);available=counts(kp,native)
    shortage={level:max(0,5-available[level]) for level in g.LEVELS}
    result={'outcome':'generated' if not any(shortage.values()) else 'finite-limit','knowledgePoint':KP,'topic':17592186050122,'database':'math','lineage':LINEAGE,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_registered':True,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_questions_by_level':verified.get('by_level',{}),'supported_levels':list(g.LEVELS),'unsupported_levels':['hard'],'unsupported_levels_filled':False,'unsupported_shortages':{'hard':5},'remaining_supported_shortages':shortage,'available_by_level':available,'native_available_by_level':native['available_by_level'],'inventory_recheck_basis':inv['basis'],'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'source_questions_and_learner_history_preserved':True,'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'inventory-after-counts.json',HERE/'source.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'source-components.json',HERE/'source-replay.json',HERE/'slot-coverage.json',HERE/'boundaries.json',HERE/'native-report.json',HERE/'source-inventory-validation.json',HERE/'source-native-report.json',HERE/'validation.json',HERE/'review.md',HERE/'capabilities.json',HERE/'native-build.json')]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','remaining_supported_shortages','unsupported_shortages')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
    for p,digest in validation['hashes'].items():assert sha(ROOT/p)==digest,p
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['endpoint']==DB.args.endpoint and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent,verified,binary);return
        inv,native=inventory(binary,OUT/'inventory-before.json');b=inv['basis']
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        for name in ('inventory-before.json','inventory-before-counts.json'):(path/name).write_bytes((OUT/name).read_bytes())
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        frozen=loads((HERE/'source.edn').read_text());old={q[':db/id']:q for q in frozen[':knowledge-point/questions']};current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(current.get(e)==q for e,q in old.items()),'Source evidence changed; reclassify'
        assert frozen[':knowledge-point/canonical-example']==kp[':knowledge-point/canonical-example']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        byscript=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b);assert len(byscript)<=1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(byscript[0][0][':question-generator/id']) if byscript else g.GENERATOR_UUID
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not collision or len(collision)==1 and collision[0][0][':question-generator/script']==SCRIPT
        available=counts(kp,native);needed={level:max(0,5-available[level]) for level in g.LEVELS}
        used={g.fingerprint(q) for q in kp[':knowledge-point/questions']}
        outputs={json.dumps(v.printed(q[':question/worked-solution'])[-1]) for q in kp[':knowledge-point/questions'] if q.get(':question/worked-solution')}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:v.check(r)
        records=[];selected={level:0 for level in g.LEVELS};supplied_report=[]
        def select(rec):
            R=v.check(rec);level=rec['question'][':question/difficulty'].split('/')[-1];fp=g.fingerprint(rec['question']);out=json.dumps(R)
            if selected[level]>=needed[level] or fp in used or out in outputs:return False
            records.append(copy.deepcopy(rec));selected[level]+=1;used.add(fp);outputs.add(out);return True
        for rec in instances:supplied_report.append({'question_id':rec['question'][':question/id'],'validated':True,'selected':select(rec)})
        for level in g.LEVELS:
            for seed in range(1930,2930):
                if selected[level]>=needed[level]:break
                select(g.generate(level,seed))
            assert selected[level]==needed[level],'Bounded sampling failed; document shortage before any commit'
        save(path/'supplied-validation.json',{'exists':supplied_path.exists(),'instances':supplied_report,'generatorError':supplied.get('generatorError')})
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        clashes=DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'question-identities',b) if ids else [];assert not clashes
        save(path/'generated.json',records);save(path/'native-input.json',[v.native(r['question'][':question/id'],r) for r in records])
        subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'generator_id':gid,'generator_path':SCRIPT,'available_by_level':available,'native_available_by_level':native['available_by_level'],'missing_by_level':needed,'selected_by_level':selected,'new_questions':len(records),'asset_hashes':[],'source_evidence_unchanged':True,'hard_unsupported_unfilled':5,'validation_sha256':sha(HERE/'validation.json'),'distinctness':'Different exact input matrices and final results; no seed/identity/option-order novelty','lock':str(LOCK)})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True}
            save(path/'verification.json',verified);finish(path,{'generator_id':gid},verified,binary);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as out:out.write(tx);out.flush();os.fsync(out.fileno())
        response=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(response.stdout);pr=loads(response.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'matrix-associative-17592186115227-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,intent,verified,binary)
if __name__=='__main__':main()
