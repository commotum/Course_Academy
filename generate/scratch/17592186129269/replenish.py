"""KP-scoped additive inventory repair using the configured application writer."""
import copy, fcntl, hashlib, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import integration as i
import validate as v

HERE=i.HERE; ROOT=i.ROOT; DB=i.DB; KP=v.g.KP_ID; g=v.g
LEVELS=('easy','moderate','hard'); SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
OUT=HERE/'reference/replenishment'
JOB=ROOT/'.local/learning/inventory/math'/i.LEARNER/'7f47e6c56bd56667c4a6adcf0cd5e0c8fbfd65e80c734bd93f1abc23d22ee797'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
EXCLUDED={'q-39300':'Incorrect component function labels in worked solution',
          'q-161807':'Incorrect cofactor minor in worked solution',
          'q-161808':'Historical distractors have poles inside the stated domain'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x): i.save(p,x)
def normalized(q):
    q=copy.deepcopy(q)
    for k in (':question/id',): q[k]=str(q[k])
    if isinstance(q[':question/difficulty'],dict): q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    for f in q[':question/answer-fields']:
        f.pop(':db/id',None);f[':answer-field/id']=str(f[':answer-field/id'])
        if isinstance(f[':answer-field/type'],dict): f[':answer-field/type']=str(f[':answer-field/type'][':db/ident'])
        c=f[':answer-field/correct']
        f[':answer-field/correct']=[':answer/id',str(c[':answer/id'])] if isinstance(c,dict) else c
        for a in f[':answer-field/choices']:
            a.pop(':db/id',None);a[':answer/id']=str(a[':answer/id'])
            if isinstance(a[':answer/type'],dict):a[':answer/type']=str(a[':answer/type'][':db/ident'])
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    return {k:q[k] for k in (':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields')}

def comparable(q):
    q=normalized(q)
    for key in (':question/problem',':question/worked-solution'):q[key]=g.math_format.normalize_prose(q[key])
    return q

def fingerprint(q):
    # Ignore UUIDs, seeds, bank order, difficulty labels and prose changes.
    F=v.prompt_components({'question':q})
    return hashlib.sha256(json.dumps([g.sp.srepr(e) for e in F]).encode()).hexdigest()

def native(r,label):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned radio option'} for a in f[':answer-field/choices']]}

def check(r):
    assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
    v.check(r)
    m=r['generation']; twin=g.generate(r['question'][':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['profile'])
    # Explicit parameters skip sampler RNG draws, which may reorder choices.
    # Compare complete field-owned content and metadata independent of order.
    assert normalized(r['question'])==normalized(twin['question']) and m==twin['generation'], 'Instance differs from deterministic generator replay'
    return fingerprint(r['question'])

def source_validation():
    accepted=[]; excluded=[]; inputs=[]
    for key,q in g.Q.items():
        t=key.replace('q-','source_');level=g.LEVELS[t]
        r=g.generate(level,template=t,parameters={'u':1,'v':1,'w':1},profile='observed')
        assert normalized(q)==normalized(r['question']) or all(normalized(q)[k]==normalized(r['question'])[k] for k in (':question/problem',':question/worked-solution',':question/difficulty'))
        # Full source-bank fidelity and correct designation are frozen separately.
        f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
        assert f[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
        v.check(r)
        r['question']=normalized(q);inputs.append(native(r,key))
        entry={'source':key,'id':q[':db/id'],'difficulty':level,'mathematical_fingerprint':fingerprint(q)}
        if key in EXCLUDED:excluded.append({**entry,'reason':EXCLUDED[key],'preserved_unchanged':True})
        else:accepted.append(entry)
    save(OUT/'source-native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(OUT/'source-native-input.json'),str(OUT/'source-native-report.json')],check=True)
    report={'basis':g.SOURCE['basis'],'accepted':accepted,'excluded':excluded,'passed':True}
    save(OUT/'source-inventory-validation.json',report)
    return report

def source_unchanged(kp):
    current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    for q in g.Q.values():
        assert q[':db/id'] in current and comparable(q)==comparable(current[q[':db/id']]),'Source changed: reclassification required'
    assert str(kp[':knowledge-point/id'])==g.KP_UUID
    old=g.RAW[':knowledge-point/canonical-example'];now=kp[':knowledge-point/canonical-example']
    assert str(old[':question/id'])==str(now[':question/id'])
    for key in (':question/problem',':question/worked-solution'):
        assert g.math_format.normalize_prose(old[key])==g.math_format.normalize_prose(now[key])

def validated_counts(kp,native_counts):
    valid={q['id'] for q in json.loads((OUT/'source-inventory-validation.json').read_text())['accepted']}
    packages=[]
    for p in OUT.glob('basis-*/generated.json'): packages.extend(json.loads(p.read_text()))
    byid={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    for eid,q in byid.items():
        if eid not in valid:
            for r in packages:
                if str(q[':question/id'])==r['question'][':question/id'] and normalized(q)==normalized(r['question']):check(r);valid.add(eid);break
    available=set(native_counts['available_questions']) & valid
    return {level:len({fingerprint(byid[e]) for e in available if str(byid[e][':question/difficulty'][':db/ident'])==':question.difficulty/'+level}) for level in LEVELS}

def transaction(records,kp,gid):
    k=i.kw; forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({k('db/id'):a[':answer/id'],k('answer/id'):uuid.UUID(a[':answer/id']),k('answer/type'):k(a[':answer/type']),k('answer/value'):a[':answer/value'],k('db/ensure'):k('answer/validate')})
            forms.append({k('db/id'):f[':answer-field/id'],k('answer-field/id'):uuid.UUID(f[':answer-field/id']),k('answer-field/key'):f[':answer-field/key'],k('answer-field/type'):k(f[':answer-field/type']),k('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],k('answer-field/correct'):f[':answer-field/correct'][1],k('db/ensure'):k('answer-field/validate')})
        forms.append({k('db/id'):q[':question/id'],k('question/id'):uuid.UUID(q[':question/id']),k('question/problem'):q[':question/problem'],k('question/worked-solution'):q[':question/worked-solution'],k('question/difficulty'):k(q[':question/difficulty']),k('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],k('db/ensure'):k('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:
        forms += [{k('db/id'):'generator',k('question-generator/id'):uuid.UUID(gid),k('question-generator/script'):SCRIPT},[k('db/add'),KP,k('knowledge-point/question-generator'),'generator']]
    if records:forms.append({k('db/id'):KP,k('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([k('db/ensure'),KP,k('knowledge-point/validate')])
    return forms

def check_datoms(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,val,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected retraction or contributor'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    kp=i.read_kp(path/'readback',report[':edb/db-after-t']);before=i.loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalized(q)==normalized(r['question']);check(r)
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,intent,verified,binary):
    inv,native_counts=i.inventory(binary,path/'inventory-after.json');kp=i.read_kp(path/'inventory-readback',inv['basis']);available=validated_counts(kp,native_counts)
    shortage={l:max(0,5-available[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'topic':17592186049530,'database':'math','lineage':i.LINEAGE,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_registered':True,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_questions_by_level':verified.get('by_level',{}),'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':available,'native_available_by_level':native_counts['available_by_level'],'remaining_supported_shortages':shortage,'inventory_recheck_basis':inv['basis'],'source_questions_and_learner_history_preserved':True,'source_quality_exclusions':EXCLUDED,'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'inventory-after-counts.json',OUT/'source-inventory-validation.json',OUT/'source-native-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'review.md',HERE/'native-build.json',HERE/'capabilities.json')]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','remaining_supported_shortages')}),flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
    for name,digest in validation['frozen'].items():assert sha(HERE.parent/name)==digest,name
    source_validation()
    binary=i.build_learning(ROOT.parent/'EDB')
    preview=i.preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==i.LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent,verified,binary);return
        inv,native_counts=i.inventory(binary,OUT/'inventory-before.json');b=inv['basis'];path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        for name in ('inventory-before.json','inventory-before-counts.json'):(path/name).write_bytes((OUT/name).read_bytes())
        kp=i.read_kp(path,b);source_unchanged(kp);(path/'before.edn').write_text(i.dumps(kp)+'\n')
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        byscript=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b);assert len(byscript)<=1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(byscript[0][0][':question-generator/id']) if byscript else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not collision or len(collision)==1 and collision[0][0][':question-generator/script']==SCRIPT
        available=validated_counts(kp,native_counts);needed={l:max(0,5-available[l]) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};selected={l:0 for l in LEVELS};records=[]
        def select(r):
            fp=check(r);level=r['question'][':question/difficulty'].split('/')[-1]
            if selected[level]>=needed[level] or fp in used:return False
            records.append(copy.deepcopy(r));selected[level]+=1;used.add(fp);return True
        supplied=JOB.with_suffix('.generated');data=json.loads(supplied.read_text()) if supplied.exists() else {};instances=data.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        supplied_report=[{'question_id':r['question'][':question/id'],'validated':True,'selected':select(r)} for r in instances]
        for level in LEVELS:
            for seed in range(1930,2930):
                if selected[level]>=needed[level]:break
                select(g.generate(level,seed))
        save(path/'supplied-validation.json',{'exists':supplied.exists(),'instances':supplied_report,'generatorError':data.get('generatorError')})
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        clashes=DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'question-identities',b) if ids else [];assert not clashes
        save(path/'generated.json',records);save(path/'native-input.json',[native(r,r['question'][':question/id']) for r in records])
        subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':i.LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'generator_id':gid,'generator_path':SCRIPT,'available_by_level':available,'native_available_by_level':native_counts['available_by_level'],'needed_by_level':needed,'selected_by_level':selected,'unfilled_by_level':{l:needed[l]-selected[l] for l in LEVELS},'asset_hashes':[],'source_evidence_unchanged':True,'validation_sha256':sha(HERE/'validation.json'),'distinctness':'Exact displayed inverse maps differ; no identity, seed, difficulty label or option-order novelty','lock':str(LOCK)})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True};save(path/'verification.json',verified);finish(path,{'generator_id':gid},verified,binary);return
        txpath=path/'transaction.edn';tx=i.dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        response=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(response.stdout);report=i.loads(response.stdout);assert report[':edb/committed'] is False and report[':edb/db-before-t']==b
        check_datoms(report,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':i.LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'inverse-jacobian-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,intent,verified,binary)

if __name__=='__main__':main()
