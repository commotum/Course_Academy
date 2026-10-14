"""Scoped additive replenishment with retained requests and exact-basis readback."""
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
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
sys.path.insert(0,str(HERE))
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '014aead0458d5a476a23e97f8e1b7ec479bd9cf4eb06cacf86616d6022e4fb97'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-ef48cfde3a25d91e'
DB.env = database_environment('math')
LEVELS = ('easy','moderate','hard')
sys.path.insert(0,str(HERE))
QUERY = (HERE / 'reference/source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

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

def validate_instance(rec):
    md=rec['generation'];level=md['difficulty']
    assert level in LEVELS and rec['question'][':question/difficulty']==':question.difficulty/'+level
    v.check(rec)
    replay=g.generate(level,md['seed'],template=md['template'],parameters=md['parameters'],profile=md['bank_profile'])
    assert ordered(rec['question'])==ordered(replay['question']) and md==replay['generation']
    assert fingerprint(rec['question'])==md['parameter_fingerprint']

def prompt_data(q):
    import re
    point=re.search(r'point \$\((-?\d+),(-?\d+)\)\$',q[':question/problem']);assert point
    coords=list(map(int,point.groups()))
    components=re.findall(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',q[':question/problem'],re.S)[-1].split(r'\\')
    assert len(components)==2
    return [v.parse(z) for z in components],coords

def fingerprint(q):
    functions,point=prompt_data(q)
    # Same mathematical operands/point/domain; independent of bank, seed or UUID.
    domain=g.domain(next((t for t in g.TEMPLATES if all(v.eq(a,b) for a,b in zip(functions,g.functions(t,g.TEMPLATES[t][2])))), 'powers'))
    canonical={'x':g.sp.srepr(functions[0]),'y':g.sp.srepr(functions[1]),'point':point,'domain':domain}
    return hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID): return str(value)
    return value

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
        assert fingerprint(q) == rec['generation']['parameter_fingerprint']
        validate_instance(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def grade(records,path):
    path.mkdir(parents=True,exist_ok=True)
    items=[]
    for r in records:
        checks=[]
        for i,f in enumerate(r['question'][':question/answer-fields']):
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independently validated owned radio selection'} for a in f[':answer-field/choices'])
        items.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
    save(path/'native-input.json',items)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    result=json.loads((path/'native-report.json').read_text());assert result['documented_unresolved_checks']==0

def validate_sources(kp,path):
    known={z['source_id']:z for z in json.loads((HERE/'source-cases.json').read_text())}
    known['q-161886']={'template':'cubic_difference','parameters':{'u0':3,'v0':1},'bank_profile':'observed_cubic_difference'}
    reports=[];usable=[]
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id')
        if mid is None:continue
        assert mid in known,'New source needs classification: '+mid
        case=known[mid];t=case['template'];p=case['parameters'];profile=case['bank_profile']
        r=g.generate('easy',parameters=p,profile=profile);v.check(r)
        assert fingerprint(q)==r['generation']['parameter_fingerprint'],'Source prompt changed: '+mid
        data=g.compute(t,p);C=data[-1];bad=[]
        for i,f in enumerate(q[':question/answer-fields']):
            values=[v.coefficient(a[':answer/value']) for a in f[':answer-field/choices']]
            expected=[v.coefficient(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            assert len(values)==len(expected)==5 and all(sum(v.eq(a,b) for b in expected)==1 for a in values)
            designated=f.get(':answer-field/correct',{}).get(':answer/id')
            correct=[a[':answer/id'] for a in f[':answer-field/choices'] if v.eq(v.coefficient(a[':answer/value']),C)]
            if designated not in correct:bad.append({'field':i,'reason':'Stale or missing correct designation; preserved'})
        # Sources with a duplicate field key are not admitted as practice.
        keys=[f.get(':answer-field/key') for f in q[':question/answer-fields']]
        if len(keys)!=len(set(keys)):bad.append({'reason':'Duplicate field key; preserved'})
        if bad:assert mid=='q-161831',bad
        else:usable.append(q)
        reports.append({'source':mid,'template':t,'fields':len(keys),'options_matched':5*len(keys),'complete_banks_matched':len(keys),'gradable_and_math_valid':not bad,'excluded':bad})
    assert len(reports)==12
    save(path/'current-source-replay.json',{'basis':kp_basis(path),'source_questions':len(reports),'complete_banks_matched':sum(r['complete_banks_matched'] for r in reports),'matched_values':sum(r['options_matched'] for r in reports),'reports':reports,'new_template':{'source':'q-161886','x':'u^3-v','y':'v-u','point':[3,1],'jacobian':'3*u^2-1','correct':'26*delta A','profile':'observed_cubic_difference','plot':'none'}})
    return usable

def kp_basis(path):
    return int(path.name.split('-')[-1]) if path.name.startswith('basis-') else None

def counts(kp,path,basis,generated):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    source_usable=validate_sources(kp,path)
    gen_byid={r['question'][':question/id']:r for r in generated}
    available={l:set() for l in LEVELS};graded=[]
    good_ids={q[':db/id'] for q in source_usable}
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id');qid=str(q[':question/id'])
        if mid and q[':db/id'] not in good_ids:continue
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        if mid:
            r={'question':normalize(q),'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'generation':{'template':mid}}
        else:
            assert qid in gen_byid,'Unrecognized generated question requires replay'
            r=gen_byid[qid];validate_instance(r);assert normalize(q)==ordered(r['question'])
        graded.append(r)
        if q[':db/id'] not in shown|reserved:available[level].add(fingerprint(q))
    grade(graded,path/'inventory-grading')
    result={'basis':basis,'distinct_available':{l:len(z) for l,z in available.items()},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'gradable_questions':len(graded),'excluded_sources':['q-161831'],'exclusion_reason':'Duplicate radio key and stale legacy designation; originals preserved'}
    save(path/'available-counts.json',result)
    return result

def finish(path,gid,verified,inv):
    records=json.loads((path/'generated.json').read_text())
    stock=counts(read_kp(path/'post-inventory',inv['basis']),path/'post-inventory',inv['basis'],records)
    shortage={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':{l:sum(r['generation']['difficulty']==l for r in records) for l in LEVELS},'supported_levels':list(LEVELS),'observed_levels':['easy'],'authored_levels':['moderate','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':stock['distinct_available'],'shortage_by_level':shortage,'capability_exceptions':[],'source_exceptions':[{'source':'q-161831','reason':'Duplicate field key/stale legacy designation; preserved and excluded'}],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'validation.json',HERE/'freeze.json',HERE/'classification-current.md',path/'preparation.json',path/'generated.json',path/'current-source-replay.json',path/'post-inventory/available-counts.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json'] if p.exists()]}
    if any(shortage.values()):result['capability_exceptions']=[{'level':l,'shortage':n,'bounded_attempts':500,'reason':'No additional distinct valid task found in bounded sampling; no claim of filled quota'} for l,n in shortage.items() if n]
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ['outcome','verified_commit_basis','new_questions','available_by_level','remaining_jobs']}),flush=True)

def main():
    freeze=json.loads((HERE/'freeze.json').read_text())
    for name,p in [('generator',HERE.with_suffix('.py')),('validator',HERE/'validate.py'),('grader',ROOT/'generate/runs/current/check-engine')]:assert freeze['hashes'][name]==sha(p),name
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        assert LINEAGE in DB.command('status')
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        stock=counts(kp,path/'current-inventory',b,[]);needed={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
        validate_sources(kp,path)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b)
        assert len(existing)<=1
        identity=HERE/'generator-identity.json'
        gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else json.loads(identity.read_text())['id'] if identity.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        if identity.exists():assert gid==json.loads(identity.read_text())['id']
        save(identity,{'id':gid,'script':SCRIPT})
        if existing and not gen:kp_for_tx=kp # Linking an existing registered identity is an upsert with identical path.
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        canonical=g.generate('moderate',parameters=g.TEMPLATES['canonical_monomial'][2]);used.add(canonical['generation']['parameter_fingerprint'])
        records=[];generated_counts={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(instances,dict):instances=[instances]
        for r in instances:validate_instance(r)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        for level in LEVELS:
            candidates=[r for r in instances if r['generation']['difficulty']==level]
            attempt=0
            while generated_counts[level]<needed[level] and attempt<500:
                r=candidates.pop(0) if candidates else g.generate(level,int(JOB.name[:8],16)+attempt)
                attempt+=1;validate_instance(r);fp=fingerprint(r['question'])
                if fp in used:continue
                records.append(r);used.add(fp);generated_counts[level]+=1
        for attribute,key,values in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[values],path,'identity-'+key,b)
        registration=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registration or registration[0][0][':question-generator/script']==SCRIPT
        save(path/'generated.json',records);grade(records,path/'generated-grading')
        (path/'review.md').write_text('\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'needed':needed,'generated_counts':generated_counts,'available_counts':stock['distinct_available'],'new_questions':len(records),'distinct_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':[],'source_questions_preserved':len(kp[':knowledge-point/questions']),'inventory_rechecked_under_lock':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'local-area-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        print(json.dumps({'phase':'submitting','basis':b,'new_by_level':generated_counts,'generator_id':gid}),flush=True)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
