"""Scoped additive replenishment with retained requests and exact-basis readback."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
import re
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
from image_library import ImageLibrary
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'c00af8f67e533bc294cfccb9af48e565e26dd39d54adf56d2fcf7497facd9e5f'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-64e7aa312fccadb0'
QUERY = (OUT / 'source-query.edn').read_text()

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
    md=rec['generation'];assert md['version']==g.VERSION and md['eligible_for_learning'] and not md['raw_replay']
    v.check_record(rec)
    replay=g.generate(md['level'],md['seed'],template=md['template'],profile=md['bank_profile'],parameters=md['parameters'])
    expected=copy.deepcopy(replay['question'])
    asset=rec['generation'].get('assets',[])
    for a in asset:expected[':question/problem']=expected[':question/problem'].replace(a['original_path'],a['path'])
    assert ordered(rec['question'])==ordered(expected)
    for key,value in replay['generation'].items():assert md[key]==value,key

def fingerprint(q):
    # Conservatively exclude the same ordered radii across every difficulty,
    # profile and response layout. Seed and choice order never count as novelty.
    if ':question/worked-solution' in q:
        m=re.search(r'In our case, \$a=([^$]*)\$ and \$b=([^$]*).\$',q[':question/worked-solution'])
        if m:return (str(v.coef(m[1])),str(v.coef(m[2])))
    mid=q.get(':question/math-academy-id')
    if mid in g.RECIPES:
        p=g.RECIPES[mid]['parameters'];return (str(p['a']),str(p['b']))
    raise ValueError('Unresolved existing ellipse geometry')

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
        assert fingerprint(q) == fingerprint(rec['question'])
        for asset in rec['generation']['assets']:
            assert sha(Path('/media/jake/SSD/EDB/math')/asset['path']) == asset['sha256']
        validate_instance(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def discovery(path):
    request={'database':'math','learner':LEARNER,'topics':[17592186049672],'activity_type':'lesson'}
    r=subprocess.run([str(ROOT/'.local/generate/find-candidates-356ff475fdbaa9d8')],input=json.dumps(request),env=DB.env,capture_output=True,text=True,check=True,timeout=90)
    data=json.loads(r.stdout);assert data['cursor']['lineage']==LINEAGE
    save(path,data)
    kp=next(k for t in data['topics'] for k in t['knowledge_points'] if k['db/id']==KP)
    return data,kp['inventory']['available']

def finish(path,gid,verified):
    inv=inventory(path/'inventory-after.json');disc,counts=discovery(path/'discovery-after.json')
    assert inv['basis']==disc['basis']
    shortage={level:max(0,5-counts[level]) for level in g.LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_version':g.VERSION,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'available_counts_before':json.loads((path/'preparation.json').read_text())['available_counts'],'available_counts_after':counts,'supported_levels':list(g.LEVELS),'supported_shortage_remaining':shortage,'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'bounded_capability':{'meaningful_parameter_limits':json.loads((HERE/'validation.json').read_text())['meaningful_parameter_counts'],'normal_integer_axis_bounds':[2,9],'raw_source_axis_bounds':[2,10],'hard':'Authored same-method graph reading with half-unit axes and full traversal; source has no rated hard examples. Mathematical and actual grader validation passed.','evidence_only_profile':'q-106701 opaque distractor retained for replay only','source_anomalies':'q-15803 missing rating/key/solution and q-15856 duplicate field preserved in live source records'},'evidence':[str((path/name).relative_to(ROOT)) for name in ('preparation.json','verification.json','commit-intent.json','transaction.edn','preview.edn','commit.edn','native-report.json','inventory-after.json','discovery-after.json') if (path/name).exists()]+[str((HERE/'validation.json').relative_to(ROOT)),str((HERE/'classification.md').relative_to(ROOT)),str((HERE/'capabilities.json').relative_to(ROOT))]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_counts_after','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed' and validation['source_questions']==17
    frozen=json.loads((HERE/'freeze.json').read_text());assert frozen['version']==g.VERSION
    for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'recipes.json'):
        assert sha(p)==frozen['files'][str(p.relative_to(HERE.parent))]
    assert validation['engine_sha256']==sha(ROOT/'generate/runs/current/check-engine')
    DB.env=database_environment('math')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        assert LINEAGE in DB.command('status')
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified);return
        inv=inventory(OUT/'inventory-before.json');disc,counts=discovery(OUT/'discovery-before.json');b=inv['basis'];assert disc['basis']==b==DB.basis()
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.SOURCE['record'][':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=g.SOURCE['record'];expected={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(expected)<=set(current)
        for mid,q in expected.items():assert canonical(current[mid])==canonical(q),'Source changed; reclassify '+mid
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b)
        assert len(existing)<=1
        gid=str(gen[':question-generator/id']) if gen else str(existing[0][0][':question-generator/id']) if existing else str(uuid.uuid5(g.NS,'question-generator:'+g.SOURCE['record'][':knowledge-point/id']))
        identity=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not identity or len(identity)==1 and identity[0][0][':question-generator/script']==SCRIPT
        needed={level:max(0,5-counts[level]) for level in g.LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];generated_counts={level:0 for level in g.LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        for rec in instances:validate_instance(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        for level in g.LEVELS:
            candidates=[r for r in instances if r['generation']['level']==level]
            seed=int(JOB.name[:8],16)
            for n in range(300):
                if generated_counts[level]>=needed[level]:break
                rec=candidates.pop(0) if candidates else g.generate(level,seed+n)
                validate_instance(rec);fp=fingerprint(rec['question'])
                if fp in used:continue
                used.add(fp);records.append(rec);generated_counts[level]+=1
        save(path/'raw-generated.json',records)
        save(path/'native-input.json',[v.native_record(r['question'][':question/id'],r) for r in records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        library=ImageLibrary();assets=[]
        for rec in records:
            asset=rec['generation']['plot'];original=Path(asset['prompt']);digest=sha(original);relative=library.put_file(original,expected_sha256=digest,content_type='image/png')
            assert sha(library.math_root/relative)==digest
            rec['question'][':question/problem']=rec['question'][':question/problem'].replace(str(original),relative)
            rec['generation']['assets']=[{'original_path':str(original),'path':relative,'sha256':digest}];assets.extend(rec['generation']['assets']);validate_instance(rec)
        for attribute,key,values in (('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if values:assert len(values)==len(set(values)) and not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[values],path,'identity-'+key,b)
        save(path/'generated.json',records)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'needed':needed,'generated_counts':generated_counts,'available_counts':counts,'new_questions':len(records),'source_evidence_unchanged':True,'assets':assets,'distinct_generated_radii':len({fingerprint(r['question']) for r in records}),'generator_sha256':sha(HERE.with_suffix('.py'))})
        save(HERE/'capabilities.json',{'basis':b,'supported_levels':list(g.LEVELS),'finite_variant_limit':validation['meaningful_parameter_counts'],'remaining_shortage':{level:max(0,needed[level]-generated_counts[level]) for level in g.LEVELS},'hard_level':'Authored half-unit graph reading with complete traversal, same mathematical method; no rated hard source evidence.','normal_sampling_policy':'Integer radii 2..9; captured radius10 replayed at original parameters only. Cosmetic labels and bank/field choices never create distinct tasks.','source_anomalies':'Preserved unchanged; opaque q-106701 replayed only; normal output complete and independently validated.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True};save(path/'verification.json',verified);finish(path,gid,verified);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        if '--prepare-only' in sys.argv:
            print(json.dumps({'prepared_basis':b,'new_questions':len(records),'counts':counts,'preview_passed':True}),flush=True);return
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'origin-ellipse-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified)
if __name__=='__main__':main()
