"""Register/replenish only this KP, using the application lock and EDB boundary."""
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture'), str(ROOT/'generate/scripts')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning

spec = importlib.util.spec_from_file_location('slope_perpendicular_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP, TOPIC = g.KP_ID, 17592186048357
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'8689d79c7dd73df5dd557d4fc411c85c0d2192cbf75f1397b70a0a85247bebb6'
OUT = HERE/'reference/replenishment'
LEVELS = ('easy', 'moderate', 'hard')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY = (HERE/'source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

def normalized(q):
    q = json.loads(json.dumps(q, default=str))
    q = {k:q[k] for k in (':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields')}
    if isinstance(q[':question/difficulty'], dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
    fields=[]
    for f in q[':question/answer-fields']:
        kind=f[':answer-field/type']
        correct=f[':answer-field/correct']
        fields.append({':answer-field/id':f[':answer-field/id'], ':answer-field/key':f[':answer-field/key'], ':answer-field/type':kind[':db/ident'] if isinstance(kind,dict) else kind,
            ':answer-field/correct':[':answer/id',correct[':answer/id']] if isinstance(correct,dict) else correct,
            ':answer-field/choices':sorted([{':answer/id':a[':answer/id'], ':answer/value':a[':answer/value'], ':answer/type':a[':answer/type'][':db/ident'] if isinstance(a[':answer/type'],dict) else a[':answer/type']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    q[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key'])
    return q

def transaction(records, kp, gid):
    forms=[]
    for rec in records:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_datoms(report, path, source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')} | {':answer-field/'+s for s in ('id','key','type','choices','correct')} | {':answer/'+s for s in ('id','type','value')} | {':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added, 'Unexpected source or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed

def verify(path, intent, report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:x for k,x in before.items() if k not in omit}=={k:x for k,x in kp.items() if k not in omit}
    records=json.loads((path/'generated.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        v.check_record(rec)
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalized(q)==normalized(rec['question'])
    assert not transaction([],kp,intent['generator_id'])
    verification={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',verification)
    return verification


UNAVAILABLE_QUERY = '''[:find ?q
 :in $ ?learner ?kp
 :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
   (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
   (and [?l :learner/activity ?t] [?t :learner-task/activity ?a]
     (or [?t :learner-task/status :learner-task.status/started]
         [?t :learner-task/status :learner-task.status/paused])
     (or [?a :activity/type :activity.type/lesson]
         [?a :activity/type :activity.type/review]
         [?a :activity/type :activity.type/assessment])
     [?a :activity/steps ?st] [?st :step/content ?q]))]'''

def fingerprint(q):
    import re
    shown=re.findall(r'\$([^$]+)\$',q[':question/problem'])
    assert shown
    target=v.equation(shown[0].rstrip('?'))
    assert v.sp.degree(target,v.X)==1
    return g.digest({'target_slope':str(target.coeff(v.X))})

def inventory(binary,path):
    response=subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
    result=json.loads(response.stdout)
    assert result['ok'] and result['data']['lineage']==LINEAGE
    save(path,result['data'])
    return result['data']

def native(records,path):
    inputs=[]
    for rec in records:
        f=rec['question'][':question/answer-fields'][0]
        inputs.append({'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned choice through current learner grader'} for a in f[':answer-field/choices']]})
    save(path/'native-input.json',inputs)
    subprocess.run([str(HERE/'reference/validation/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text())
    assert report['documented_unresolved_checks']==0

def existing_math(q):
    import re
    target=v.equation(re.findall(r'\$([^$]+)\$',q[':question/problem'])[0].rstrip('?'))
    m=target.coeff(v.X)
    assert v.sp.degree(target,v.X)==1 and m!=0
    f,=q[':question/answer-fields']; assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    assert len(f[':answer-field/choices'])==5
    values=[v.equation(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(map(str,values)))==5
    assert all(v.sp.degree(p,v.X)<=1 for p in values),'Nonlinear distractors outside line-only scope'
    correct=[a for a,p in zip(f[':answer-field/choices'],values) if v.sp.degree(p,v.X)==1 and m*p.coeff(v.X)==-1]
    assert len(correct)==1 and correct[0][':answer/id']==f[':answer-field/correct'][1]
    sol=q[':question/worked-solution'];assert sol
    given=re.search(r'The line \$([^$]+)\$ is in slope-intercept form, and its slope is \$([^$]+)\$',sol)
    chosen=re.search(r'Looking at the answer choices, the line \$([^$]+)\$ has a slope of \$([^$]+)\$',sol)
    product=re.search(r'\$\$\n([^$]+)\n\$\$',sol)
    assert given and chosen and product
    assert v.equation(given[1])==target and v.expr(given[2])==m
    assert v.equation(chosen[1])==v.equation(correct[0][':answer/value']) and v.expr(chosen[2])==-1/m
    lhs,rhs=product[1].split('=');assert v.expr(lhs)==v.expr(rhs)==-1
    return m

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(UNAVAILABLE_QUERY,[LEARNER,KP],path,'unavailable',basis)}
    used={fingerprint(q) for q in kp[':knowledge-point/questions']}
    used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    available={l:set() for l in LEVELS};excluded=[];records=[];valid=[]
    for q in kp[':knowledge-point/questions']:
        level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
        if level not in LEVELS or not q.get(':question/worked-solution') or any(not f.get(':answer-field/correct') for f in q[':question/answer-fields']):
            excluded.append({'id':q[':db/id'],'reason':'Unrated or incomplete source preserved unchanged'})
            continue
        rec={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':normalized(q),'generation':{'parameter_fingerprint':fingerprint(q),'template':'current-source-validation'}}
        try:existing_math(rec['question'])
        except AssertionError as error:
            if q.get(':question/math-academy-id')!='q-72524':raise
            excluded.append({'id':q[':db/id'],'reason':str(error),'source_anomaly':'Two raw quadratic distractors; no repair to source'})
            continue
        records.append(rec);valid.append(q[':db/id'])
        if q[':db/id'] not in unavailable:available[level].add(fingerprint(q))
    native(records,path)
    result={'basis':basis,'distinct_available':{l:len(available[l]) for l in LEVELS},'missing':{l:max(0,5-len(available[l])) for l in LEVELS},'validated_practice_ids':valid,'excluded_sources':excluded,'unavailable_ids':sorted(unavailable),'fingerprint':'Reduced target slope; exclude incomplete, unrated, malformed, shown or reserved questions'}
    save(path/'validated-inventory.json',result)
    return result,used

def finish(path,gid,verified,binary):
    inv=inventory(binary,path/'inventory-after.json')
    kp=read_kp(path/'post-inventory',inv['basis'])
    stock,_=counts(kp,path/'post-inventory',inv['basis'])
    caps=json.loads((HERE/'capabilities.json').read_text())
    result={'outcome':'finite-limit' if any(stock['missing'].values()) else 'generated','knowledgePoint':KP,'topic':TOPIC,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':verified['by_level'],'supported_levels':list(LEVELS),'hard_origin':'Authored allocation supported by canonical rational slope; no observed hard source labels','unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':stock['distinct_available'],'remaining_supported_shortages':stock['missing'],'capability_exceptions':caps['exceptions'],'finite_limits':caps['finite_limits'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'generated.json',path/'supplied-status.json',path/'native-report.json',path/'inventory-after.json',path/'post-inventory/validated-inventory.json',HERE/'validation.json',HERE/'capabilities.json',HERE/'freeze.json',HERE/'review.md')],'note':'Only distinct reduced target slopes admitted. Source questions, canonical example and learner history preserved. Unrated incomplete sources and malformed moderate source remain excluded from validated inventory.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_by_level','available_by_level','remaining_supported_shortages','remaining_jobs')},indent=2),flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert freeze['supported_levels']==list(LEVELS)
    assert all(sha(ROOT/p)==digest for p,digest in freeze['files'].items()),'Frozen validation inputs changed'
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
            assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path)
            finish(path,intent['generator_id'],verify(path,intent,report),binary)
            return
        inv=inventory(binary,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        current=json.loads(json.dumps(kp,default=str))
        source=json.loads((HERE/'source.json').read_text())['record']
        existing={q[':db/id']:q for q in current[':knowledge-point/questions']}
        assert all(existing[q[':db/id']]==q for q in source[':knowledge-point/questions']), 'Source changed; reclassify'
        assert current[':knowledge-point/canonical-example']==source[':knowledge-point/canonical-example']
        stock,used=counts(kp,path/'inventory-validation',b)
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        gen=kp.get(':knowledge-point/question-generator')
        registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b);assert len(registered)<=1
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not collision or collision[0][0][':question-generator/script']==SCRIPT
        needed=stock['missing'];records=[];checked=[];selected={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        supplied_status=[]
        def consider(rec):
            assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
            level=rec['question'][':question/difficulty'].split('/')[-1];assert level in LEVELS
            v.check_record(rec)
            r=rec['generation'];replay=g.generate(level,r['seed'],r['template'],parameters=r['parameters'],profile=r['bank_profile'])
            assert normalized(replay['question'])==normalized(rec['question'])
            checked.append(rec);fp=fingerprint(rec['question'])
            if selected[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);selected[level]+=1
        for rec in instances:
            consider(rec);supplied_status.append({'question':rec['question'][':question/id'],'status':'validated'})
        previews=[g.generate(l,2188) for l in LEVELS]
        for rec in previews:consider(rec)
        # Execute the full finite slope domain if seeded previews leave shortages.
        domains={'easy':[v.sp.Integer(s*n) for s in (-1,1) for n in range(2,13)],'moderate':[v.sp.Rational(s,n) for s in (-1,1) for n in range(2,13)],'hard':sorted(set(v.sp.Rational(s*n,d) for s in (-1,1) for n in range(2,10) for d in range(2,10) if __import__('math').gcd(n,d)==1))}
        for level,slopes in domains.items():
            for slope in slopes:
                if selected[level]>=needed[level]:break
                consider(g.generate(level,2188,parameters={'m':str(slope),'b':2,'intercepts':[-4,-2,1,3,5]}))
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances':supplied_status,'generator_error':supplied.get('generatorError')})
        save(path/'generated.json',records);save(path/'validated-previews.json',previews)
        (path/'validated-previews.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in previews)+'\n')
        (path/'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        native(checked,path)
        identities=[uuid.UUID(r['question'][':question/id']) for r in records]
        if identities:assert not DB.query('[:find ?q :in $ [?id ...] :where [?q :question/id ?id]]',[identities],path,'generated-identities',b)
        save(path/'preparation.json',{'basis':b,'original_job_basis':2188,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'available_by_level_before':stock['distinct_available'],'missing_by_level':needed,'selected_by_level':selected,'unproduced_by_level':{l:needed[l]-selected[l] for l in LEVELS},'assets':[],'supplied_generated_exists':supplied_path.exists(),'source_evidence_unchanged':True,'generator_executed_for_supported_template_validation':True,'new_questions_only_for_current_supported_shortage':True,'distinctness':'Reduced target slope; exclude every existing source and canonical task; no seed/identity/order/intercept-only questions'})
        forms=transaction(records,kp,gid)
        assert forms,'Already registered: recover prior commit evidence'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_datoms(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'slope-perpendicular-register-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report),binary)

if __name__=='__main__':main()
