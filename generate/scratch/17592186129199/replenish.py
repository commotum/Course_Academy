"""Scoped additive inventory replenishment; retain exact requests and receipts."""
import copy
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
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database, StaleBasis
from edn import dumps, loads, kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('polar_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LINEAGE = g.SOURCE['lineage']
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'3e6791ee453a54fd1a4b995107394127793c4813a4eabc9e13ccf9ca09a4172b'
LOCK = ROOT/'.local/learning/requests/math/api.lock'
OUT = HERE/'reference/replenishment'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env.update(ENV)
QUERY = (HERE/'reference/source-query.edn').read_text()
USAGE = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical(x):
    if isinstance(x, dict):
        return {str(k): canonical(y) for k,y in x.items() if k != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(x, (list,tuple)):
        return sorted([canonical(y) for y in x], key=lambda y:json.dumps(y,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def normalized(q):
    result = {k:str(q[k]) if k == ':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in q[':question/answer-fields']:
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':[{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return ordered(result)

def inventory(binary, path):
    proc = subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55)
    x = json.loads(proc.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path,x['data'])
    return x['data']

def read_kp(path,basis):
    kp = DB.query(QUERY,[KP],path,'kp',basis)[0][0]
    assert str(kp[':knowledge-point/id']) == g.KP_UUID
    return kp

def source_check(kp,path):
    current = {q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    differences = []
    for old in g.RECORD[':knowledge-point/questions']:
        a,b = canonical(old),canonical(current[old[':question/math-academy-id']])
        if a != b:
            # The current q-83499 fixes literal set braces, already normalized
            # by the frozen source replayer. No mathematical content changed.
            assert old[':question/math-academy-id'] == 'q-83499'
            a[':question/worked-solution'] = a[':question/worked-solution'].replace('Δ={(r',r'Δ=\{(r').replace('0}.',r'0\}.')
            assert a == b, 'Source mathematics changed: reclassify'
            differences.append({'source':'q-83499','change':'Literal set braces escaped in current source; matches validated replay normalization'})
    assert canonical(g.RECORD[':knowledge-point/canonical-example']) == canonical(kp[':knowledge-point/canonical-example'])
    save(path/'source-recheck.json',{'basis':DB.basis(),'captured_source_basis':g.SOURCE['basis'],'practice_sources':9,'mathematical_changes':0,'presentation_changes':differences})

def raw_record(rec):
    rec = copy.deepcopy(rec)
    for asset in rec['generation'].get('published_assets',[]):
        for k in (':question/problem',':question/worked-solution'):
            rec['question'][k] = rec['question'][k].replace(asset['reference'],asset['local'])
    return rec

def validate(rec):
    raw = raw_record(rec)
    assert raw['knowledge_point']['db_id'] == KP and raw['knowledge_point']['id'] == g.KP_UUID
    v.check(raw)
    meta = raw['generation']
    replay = g.generate(raw['question'][':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'] if meta['bank_profile'] in g.DATA else None)
    assert ordered(replay['question']) == ordered(raw['question']), 'Deterministic replay mismatch'
    assert replay['generation']['parameter_fingerprint'] == meta['parameter_fingerprint']

def grade(records,path):
    entries=[]
    for rec in records:
        f=rec['question'][':question/answer-fields'][0]
        entries.append({'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual owned-answer radio grading'} for a in f[':answer-field/choices']]})
    save(path/'native-input.json',entries)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True)
    report=json.loads((path/'native-report.json').read_text())
    assert report['accepted_checks']==len(records) and report['rejected_checks']==4*len(records) and report['documented_unresolved_checks']==0

def stock(kp,path,basis,records=()):
    unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    unavailable.update(r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis))
    qids=[q[':db/id'] for q in kp[':knowledge-point/questions']]
    examples={r[0] for r in DB.query('[:find ?q :in $ [?q ...] :where [_ :knowledge-point/canonical-example ?q]]',[qids],path,'canonical',basis)}
    known={r['question'][':question/id']:r for r in records}
    for manifest in OUT.glob('basis-*/generated.json'):
        for rec in json.loads(manifest.read_text()):known[rec['question'][':question/id']]=rec
    cases={c['source_id']:c for c in v.CASES}
    used=set();available={l:set() for l in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id')
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if mid in cases:
            c=cases[mid];rec=g.generate(c['level'],9,c['template'],parameters=c['parameters'],profile=c['bank_profile'])
            fp=rec['generation']['parameter_fingerprint']
            if level in LEVELS:
                v.check(rec)
                f=q[':question/answer-fields'][0]
                assert f[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==rec['question'][':question/answer-fields'][0][':answer-field/correct'][1])
        else:
            rec=known[str(q[':question/id'])];assert normalized(q)==ordered(rec['question']);validate(rec)
            fp=rec['generation']['parameter_fingerprint']
        used.add(fp)
        if level not in LEVELS:excluded.append({'id':str(q[':question/id']),'source':mid,'reason':'Unrated and missing key/solution; preserved, not counted'})
        elif q[':db/id'] not in unavailable|examples:available[level].add(fp)
    result={'basis':basis,'available_by_level':{l:len(s) for l,s in available.items()},'excluded':excluded,'shown_or_reserved':sorted(unavailable),'distinctness':'Cartesian integrand, actual disk radius, sector modulo full turns; seed, IDs, profile and choice order excluded'}
    save(path/'validated-inventory.json',result)
    return result,used

def transaction(records,kp,gid):
    forms=[]
    for rec in records:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if not gen:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[rec['question'][':question/id'] for rec in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    attrs={a:str(name) for a,name in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added, 'Unexpected retraction or attribution'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalized(q)==ordered(rec['question']);validate(rec)
        for asset in rec['generation']['published_assets']:assert sha(Path(ENV['EDB_MATH_ROOT'])/asset['reference'])==asset['sha256']
    assert not transaction([],kp,intent['generator_id'])
    counts,_=stock(kp,path/'readback',report[':edb/db-after-t'],records)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'available_after':counts,'unchanged_existing_questions':len(old),'canonical_unchanged':True,'learner_history_unchanged':True,'only_additive_scoped_datoms':True,'generator_registration_verified':True,'repeat_preparation_changes':0}
    save(path/'verification.json',result)
    return result

def finish(path,intent,verified,binary):
    inv=inventory(binary,path/'inventory-after.json')
    counts=verified['available_after']['available_by_level']
    remaining={l:max(0,5-counts[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'available_by_level':counts,'shortage_remaining':remaining,'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':[],'unrated_source_preserved_and_excluded':'q-161044: missing original key/solution/difficulty','inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'preparation.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'native-report.json',path/'inventory-after.json',HERE/'validation.json',HERE/'freeze-hashes.json',HERE/'capabilities.json')]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps(result),flush=True)

def main():
    frozen=json.loads((HERE/'freeze-hashes.json').read_text())
    assert all(sha(ROOT/name)==value for name,value in frozen['files'].items())
    assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and sha(path/'transaction.edn')==intent['transaction_sha256']
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                finish(path,intent,verify(path,intent,report),binary);return
        inv=inventory(binary,OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
        print('Preparing at locked basis '+str(basis),flush=True)
        kp=read_kp(path,basis);source_check(kp,path);(path/'before.edn').write_text(dumps(kp)+'\n')
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(contributor)==1
        registrations=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'registrations',basis);assert len(registrations)<=1
        gen=kp.get(':knowledge-point/question-generator');identity=HERE/'generator-identity.json'
        gid=str(gen[':question-generator/id']) if gen else str(registrations[0][0][':question-generator/id']) if registrations else json.loads(identity.read_text())['id'] if identity.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        if identity.exists():assert json.loads(identity.read_text())['id']==gid
        save(identity,{'id':gid,'script':SCRIPT,'knowledge_point':g.KP_UUID})
        counts,used=stock(kp,path,basis)
        needed={l:max(0,5-counts['available_by_level'][l]) for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);assert isinstance(instances,list)
        records=[];checked=[];selected={l:0 for l in LEVELS}
        def consider(rec):
            validate(rec);checked.append(rec);level=rec['question'][':question/difficulty'].split('/')[-1];fp=rec['generation']['parameter_fingerprint']
            if selected[level]<needed[level] and fp not in used:
                records.append(copy.deepcopy(rec));used.add(fp);selected[level]+=1
        for rec in instances:consider(rec)
        # A bounded deterministic catalog cycles through templates and regions.
        # Only changed mathematical tasks count; bank/seed/order never do.
        for level in LEVELS:
            templates=[t for t,l in g.TEMPLATES.items() if l==level]
            for n in g.RADII:
                if selected[level]>=needed[level]:break
                for rot in range(4):
                    if selected[level]>=needed[level]:break
                    for template in templates:
                        if selected[level]>=needed[level]:break
                        if (level=='easy' or template=='xy2') and rot:continue
                        consider(g.generate(level,seed=1831,template=template,parameters={'radius_squared':n,'rotation':rot}))
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'supplied_instances_validated':len(instances),'generatorError':supplied.get('generatorError')})
        grade(checked,path)
        save(path/'raw-generated.json',records)
        library=ImageLibrary(Path(ENV['EDB_MATH_ROOT']));assets=[]
        for rec in records:
            local=rec['generation']['plot']['prompt'];ref=library.put_bytes(Path(local).read_bytes())
            asset={'local':local,'reference':ref,'sha256':sha(local)};assert sha(library.math_root/ref)==asset['sha256']
            for k in (':question/problem',':question/worked-solution'):rec['question'][k]=rec['question'][k].replace(local,ref)
            rec['generation']['published_assets']=[asset];assets.append(asset)
        save(path/'generated.json',records)
        for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in values]],path/'identities',attr.replace('/','-'),basis)
        save(HERE/'capabilities.json',{'supported_levels':list(LEVELS),'finite_distinct_tasks':{'easy':105,'moderate':735,'hard':280},'exceptions':[],'hard_evidence':'Two validated authored families combine canonical radial-root simplification with observed double-angle identities; same centered-sector setup skill. No evaluation or shifted regions.','excluded_source':'Unrated q-161044 retained and excluded; generated complete variants explicitly authored moderate.','validated_generator_sha256':sha(HERE.with_suffix('.py'))})
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'remaining_by_level':{l:needed[l]-selected[l] for l in LEVELS},'available_before':counts,'new_questions':len(records),'asset_hashes':assets,'generator_sha256':sha(HERE.with_suffix('.py')),'frozen_hashes_verified':len(frozen['files']),'supplied_instances_validated':len(instances),'native_checks':5*len(checked),'inventory_rechecked_under_lock':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':basis,'new_questions':0,'available_after':counts,'passed':True,'no_changes':True}
            save(path/'verification.json',verified);finish(path,{'generator_id':gid},verified,binary);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        proc=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(proc.stdout);pr=loads(proc.stdout)
        assert not pr[':edb/committed'] and pr[':edb/db-before-t']==basis
        check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':basis,'expected_basis':basis,'request_key':'origin-polar-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        finish(path,intent,verify(path,intent,report),binary)

if __name__=='__main__':
    main()
