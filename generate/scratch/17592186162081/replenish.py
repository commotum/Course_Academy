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
from image_library import ImageLibrary
import re
import sympy as sp
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '634b27497bce3bae7581fccca0afcb2cc85d9490a40bb9be476e7da08b48b624'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent/'EDB')
(HERE/'reference/learning-binary.txt').write_text(str(NATIVE))
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
    v.check(rec)
    assert not rec["generation"]["evidence_only"] and rec["generation"]["eligible_for_learning"]
    assert rec["knowledge_point"]["db_id"]==KP
    assert fingerprint(rec["question"])==rec["generation"]["mathematical_fingerprint"]

USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def scoped(kp,b,seen):
    entities={};enums={};next_enum=1
    def enum(value):
        nonlocal next_enum
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            enums[name]=next_enum;entities[str(next_enum)]={'db/ident':name};next_enum+=1
        return enums[name]
    def question(q):
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]}
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        entities[str(q[':db/id'])]=r
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id'])
            field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]}
            if ':answer-field/correct' in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            entities[str(f[':db/id'])]=field
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:question(q)
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every displayed radio option'} for a in f[':answer-field/choices']]

def known_records():
    records=[x['record'] for x in json.loads((HERE/'review.json').read_text())]
    for package in OUT.glob('basis-*/generated.json'):records.extend(json.loads(package.read_text()))
    return {r['question'][':question/id']:r for r in records if not r['generation']['evidence_only']}

def roles(t,p):
    if t=='semicircle':value=['semicircle',str(sp.Rational(p['r']))]
    else:
        a=abs(sp.Rational(p['x2'])-sp.Rational(p['x1']));b=abs(sp.Rational(p['y2'])-sp.Rational(p['y1']))
        value=['axis',str(a+b)] if not a or not b else ['diagonal',*sorted([str(a),str(b)])]
    return hashlib.sha256(g.dump(value).encode()).hexdigest()

def fingerprint(q):
    sid=q.get(':question/math-academy-id')
    if sid in g.P:
        t,p=g.P[sid];return roles(t,p)
    rec=known_records().get(str(q[':question/id']))
    if rec:return roles(rec['generation']['template'],rec['generation']['parameters'])
    # Locally generated candidates have a recipe sidecar, including exact endpoints.
    refs=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem'])
    assert refs,'Cannot establish mathematical identity without diagram'
    side=Path(refs[0]).with_suffix('.json')
    assert side.is_file(),'Unrecognized published question; reconcile saved generator evidence'
    recipe=json.loads(side.read_text())['recipe']
    p={'r':recipe['radius']} if recipe['kind']=='semicircle' else dict(zip(('x1','y1','x2','y2'),recipe['endpoints'][0]+recipe['endpoints'][1]))
    return roles(recipe['kind'],p)

def available_counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    save(path/'scoped-snapshot.json',scoped(kp,basis,unavailable))
    subprocess.run([str(ROOT/'generate/scratch/17592186110758/check-pool'),str(path/'scoped-snapshot.json'),str(path/'native-pool.json')],check=True,timeout=55,capture_output=True)
    pool=json.loads((path/'native-pool.json').read_text())['available_ids_by_level']
    admitted={e for band in pool.values() for e in band}
    available={level:[] for level in g.SUPPORTED_LEVELS};excluded=[];native=[]
    known=known_records()
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'):reason='Canonical example'
        elif level not in available:reason='Unrated or unsupported difficulty'
        elif q[':db/id'] not in admitted:reason='Excluded by actual learner inventory pool'
        elif not q.get(':question/worked-solution'):reason='Missing worked solution'
        elif q.get(':question/math-academy-id') in g.P:
            sid=q[':question/math-academy-id'];t,p=g.P[sid]
            rec=g.generate('easy',template=t,parameters=p,profile='original:'+sid)
            v.check(rec)
            # Exact source contents are compared against the captured evidence before counting.
        else:
            rec=known.get(str(q[':question/id']))
            if not rec or normalize(q)!=ordered(rec['question']):reason='Missing or mismatched validated generated record'
            else:v.check(rec)
        if reason:excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
        else:
            available[level].append(q)
            norm={'question':normalize(q)};native.append({'label':str(q[':question/id']),'record':norm,'checks':checks(norm)})
    subprocess_input=path/'inventory-grade-input.json';save(subprocess_input,native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(subprocess_input),str(path/'inventory-grade-report.json')],check=True,capture_output=True)
    grade=json.loads((path/'inventory-grade-report.json').read_text());assert grade['documented_unresolved_checks']==0
    counts={'basis':basis,'levels':{level:{'rated_gradable_unseen_unreserved':len(rows),'distinct_available_tasks':len({fingerprint(q) for q in rows}),'available_question_ids':[str(q[':question/id']) for q in rows]} for level,rows in available.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_questions':excluded}
    save(path/'available-counts.json',counts);return counts

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
        assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
        validate_instance(rec)
    for asset in json.loads((path/'preparation.json').read_text())['asset_hashes']:
        assert sha(Path('/media/jake/SSD/EDB/math')/asset['database_path'])==asset['sha256']
    assert not transaction([], kp, intent['generator_id'])
    counts=available_counts(path/'readback',kp,report[':edb/db-after-t'])
    for level in g.SUPPORTED_LEVELS:
        added=sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records)
        previous=json.loads((path/'preparation.json').read_text())['available_counts']['levels'][level]['distinct_available_tasks']
        assert counts['levels'][level]['distinct_available_tasks']>=min(5,previous+added)
    result = {'available_counts_after':counts,'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path,gid,verified,inv):
    preparation=json.loads((path/'preparation.json').read_text())
    counts=verified['available_counts_after']['levels']
    remaining={level:max(0,5-counts[level]['distinct_available_tasks']) for level in g.SUPPORTED_LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated',
        'knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,
        'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],
        'supported_levels':list(g.SUPPORTED_LEVELS),'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],
        'available_counts_before':preparation['available_counts'],'available_counts_after':verified['available_counts_after'],
        'shortage_remaining':remaining,'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],
        'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
        'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'validation.json',HERE/'source-bank-fidelity.json',HERE/'independent-review.json',HERE/'capabilities.json') if p.exists()],
        'note':'Integer easy and explicitly authored rational-coordinate moderate/hard bands retain the same length/Pythagorean stages. Original incomplete q-122567 is excluded and preserved; raw source bank masks are evidence only. Normal geometric banks are a labeled extension. Unrated source may retain an unclassified scheduler job.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['passed'] and validation['script_sha256']==sha(HERE.with_suffix('.py'))
    review=json.loads((HERE/'independent-review.json').read_text())
    assert review['approved'] and review['generator_sha256']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application api.lock acquired; rechecking current basis and inventory',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'source.json').read_text())['record']
        expected={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(expected)<=set(current)
        for mid,q in expected.items():assert canonical(current[mid])==canonical(q),'Source evidence changed; reclassify '+mid
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        byscript=DB.query('[:find (pull ?e [:db/id :question-generator/id :question-generator/script]) :in $ ?script :where [?e :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b)
        byid=DB.query('[:find (pull ?e [:db/id :question-generator/id :question-generator/script]) :in $ ?id :where [?e :question-generator/id ?id]]',[uuid.UUID(g.GENERATOR_UUID)],path,'generator-by-id',b)
        assert len(byscript)<=1 and len(byid)<=1
        if gen:gid=str(gen[':question-generator/id']);assert gen[':question-generator/script']==SCRIPT
        elif byscript:gid=str(byscript[0][0][':question-generator/id'])
        else:gid=g.GENERATOR_UUID
        if byid:assert byid[0][0].get(':question-generator/script',SCRIPT)==SCRIPT
        counts=available_counts(path,kp,b)
        needed={level:max(0,5-counts['levels'][level]['distinct_available_tasks']) for level in g.SUPPORTED_LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(roles('semicircle',{'r':4})) # Canonical is never fresh practice.
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        records=[];added={level:0 for level in g.SUPPORTED_LEVELS};rejected=[]
        for rec in instances:
            level=rec['question'][':question/difficulty'].split('/')[-1]
            if level not in needed or rec['generation'].get('evidence_only'):
                rejected.append({'question_id':rec['question'][':question/id'],'reason':'Unsupported or evidence-only instance; not counted or committed'});continue
            validate_instance(rec);fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);added[level]+=1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_checked':len(instances),'rejected':rejected,'generator_error':supplied.get('generatorError')})
        seed=int(JOB.name[:8],16)
        for level in g.SUPPORTED_LEVELS:
            for i in range(1500):
                if added[level]>=needed[level]:break
                rec=g.generate(level,seed+i);fp=fingerprint(rec['question'])
                if fp in used:continue
                validate_instance(rec);records.append(rec);used.add(fp);added[level]+=1
        # Save local representations before rewriting assets so mathematical validation
        # and independent visual review remain reproducible at the same parameters.
        save(path/'local-generated.json',records)
        assets=[];library=ImageLibrary(Path('/media/jake/SSD/EDB/math'))
        for rec in records:
            refs=set(re.findall(r'!\[.*?\]\((.*?)\)',rec['question'][':question/problem']+'\n'+rec['question'][':question/worked-solution']))
            for ref in refs:
                local=Path(ref) if Path(ref).is_absolute() else library.math_root/ref
                digest=sha(local);relative=library.put_file(local,expected_sha256=digest)
                assert sha(library.math_root/relative)==digest
                for key in (':question/problem',':question/worked-solution'):rec['question'][key]=rec['question'][key].replace(ref,relative)
                assets.append({'local_path':str(local),'database_path':relative,'sha256':digest})
        save(path/'generated.json',records)
        for rec in records:validate_instance(rec)
        for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in values]],path/'identity-check',attr.replace('/','-'),b),'Existing identity; reconcile first'
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        grade=json.loads((path/'native-report.json').read_text());assert grade['documented_unresolved_checks']==0
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'new_by_level':added,'new_questions':len(records),'available_counts':counts,'finite_remaining':{level:max(0,needed[level]-added[level]) for level in needed},'source_evidence_unchanged':True,'asset_hashes':assets,'distinctness':'Radius, axis length, or unordered exact Pythagorean legs; collapse translations, reversal, helper layout, bank/profile aliases, seed and choice order'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'generator_registration_verified':True,'available_counts_after':counts}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        if '--prepare-only' in sys.argv:
            print(json.dumps({'prepared_basis':b,'new_by_level':added,'path':str(path)}),flush=True);return
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'unity-inventory-17592186162081-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()
