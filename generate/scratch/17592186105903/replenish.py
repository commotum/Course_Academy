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
from serve_graph_explorer import database_environment, build_learning
import ast, math, re, shutil
from decimal import Decimal, ROUND_HALF_UP
import sympy as sp
spec = importlib.util.spec_from_file_location('triangle', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
g.SUPPORTED_LEVELS = ('easy','moderate','hard')
g.GENERATOR_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:question-generator:'+g.KP_UUID))
# Reuse the validated independent displayed-mathematics checks without running
# the validator's top-level batch generation or changing its evidence files.
module = ast.parse((HERE/'validate.py').read_text())
check_node = next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='display_check')
def checked(label, condition):
    assert condition, label
check_namespace = dict(g=g, checked=checked, sp=sp, re=re, math=math,
    Decimal=Decimal, ROUND_HALF_UP=ROUND_HALF_UP, Path=Path, hashlib=hashlib)
exec(compile(ast.Module(body=[check_node],type_ignores=[]),str(HERE/'validate.py'),'exec'),check_namespace)
ASSET_ROOT = Path('/media/jake/SSD/EDB/math')

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        return [dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==correct else 'rejected',purpose='Field-owned choice') for a in f[':answer-field/choices']]
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
    return [dict(submitted=value,expected='accepted',purpose='Canonical rounded numeric fragment'),dict(submitted=str(sp.Rational(value)+1),expected='rejected',purpose='Incorrect area')]

KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '1e5f4e058f179e6c2e5f966b50cf9307494316312c98cd35f398246a2f06ef7e'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent/'EDB')
(HERE/'reference/learning-binary.txt').write_text(str(NATIVE))
QUERY = (HERE / 'reference/initial/source-query.edn').read_text()

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
    if ':question/requires-calculator' in q:result[':question/requires-calculator']=q[':question/requires-calculator']
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
    assert rec['knowledge_point']['db_id']==KP
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    r=copy.deepcopy(rec)
    r['question'][':question/problem']=re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![]('+str(ASSET_ROOT/m[1])+')',r['question'][':question/problem'])
    check_namespace['display_check'](r)
    assert fingerprint(rec['question']) == rec['generation']['math_fingerprint']

def source_record(q):
    sid=q.get(':question/math-academy-id')
    if sid not in g.ANCHORS:raise ValueError('Unknown existing question requires classification')
    rec=g.generate('easy',template=g.SOURCE_TEMPLATE[sid],profile='raw_'+sid,parameters=g.ANCHORS[sid])
    if ':question/requires-calculator' in q:rec['question'][':question/requires-calculator']=q[':question/requires-calculator']
    return rec

def solution_check(q):
    if q.get(':question/math-academy-id'):
        sid=q[':question/math-academy-id']
        if sid in ('q-18021','q-279752'):raise ValueError('Known precision/prose source errors retained')
        rec=source_record(q)
        f=q[':question/answer-fields'][0]
        actual=f[':answer-field/correct'][':answer/value']
        expected=g.rounded(g.area(g.ANCHORS[sid]),g.TEMPLATES[g.SOURCE_TEMPLATE[sid]]['digits'])
        assert actual==expected
    else:
        matches=[r for path in OUT.glob('basis-*/generated.json') for r in json.loads(path.read_text()) if r['question'][':question/id']==str(q[':question/id'])]
        assert matches,'Unrecognized generated question'
        rec=matches[-1];assert normalize(q)==ordered(rec['question']);validate_instance(rec)

USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def available_counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    # Retained historical presentations and reservations stay excluded as well.
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    available={level:[] for level in g.SUPPORTED_LEVELS}
    excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'):reason='Canonical example'
        elif level not in available:reason='Unrated or unsupported difficulty'
        elif not q.get(':question/worked-solution') or not q.get(':question/answer-fields'):reason='Incomplete solution or fields'
        else:
            try:solution_check(q)
            except (AssertionError,ValueError,KeyError,TypeError) as error:reason='Mathematical/gradation validation exclusion: '+str(error)
        if reason:excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
        else:available[level].append(q)
    counts={'basis':basis,'levels':{level:{'rated_gradable_unseen_unreserved':len(rows),
        'distinct_available_tasks':len({fingerprint(q) for q in rows}),
        'available_question_ids':[str(q[':question/id']) for q in rows],
        'available_task_fingerprints':sorted({fingerprint(q) for q in rows})} for level,rows in available.items()},
        'excluded_shown_or_reserved':sorted(unavailable),'excluded_questions':excluded}
    gradable=[{'label':str(q[':question/id']),'record':{'question':normalize(q)},'checks':checks({'question':normalize(q)})} for rows in available.values() for q in rows]
    save(path/'inventory-grade-input.json',gradable)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'inventory-grade-input.json'),str(path/'inventory-grade-report.json')],check=True)
    assert json.loads((path/'inventory-grade-report.json').read_text())['documented_unresolved_checks']==0
    save(path/'available-counts.json',counts)
    return counts

def fingerprint(q):
    sid=q.get(':question/math-academy-id')
    if sid in g.ANCHORS:
        return g.digest({**g.canonical(g.ANCHORS[sid]),'digits':g.TEMPLATES[g.SOURCE_TEMPLATE[sid]]['digits']})
    # Asset bytes identify parameters; all fresh rasters have a retained sidecar.
    asset=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
    png=Path(asset) if Path(asset).is_absolute() else ASSET_ROOT/asset
    sha256=sha(png)
    for sidecar in (HERE/'plots').glob('*.json'):
        data=json.loads(sidecar.read_text())
        if data['png_sha256']==sha256:
            value=next(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])
            return g.digest({**g.canonical(data['parameters']),'digits':len(value.split('.')[1])})
    raise ValueError('Unrecognized existing diagram: '+asset)

def publish(rec):
    q=rec['question'];original=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1])
    digest=sha(original);relative='images/'+digest[:2]+'/'+digest+'.png';dest=ASSET_ROOT/relative
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        temp=dest.with_suffix('.tmp-'+str(uuid.uuid4()));shutil.copyfile(original,temp);os.replace(temp,dest)
    assert sha(dest)==digest
    q[':question/problem']=q[':question/problem'].replace(str(original),relative)
    return dict(original=str(original.relative_to(ROOT)),path=relative,sha256=digest,verified=True)

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
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/requires-calculator'):q[':question/requires-calculator'], kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
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
    allowed = {':question/requires-calculator', ':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
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
        assert fingerprint(q) == rec['generation']['math_fingerprint']
        validate_instance(rec)
    assert not transaction([], kp, intent['generator_id'])
    counts=available_counts(path/'readback',kp,report[':edb/db-after-t'])
    for level in g.SUPPORTED_LEVELS:
        added=sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records)
        previous=json.loads((path/'preparation.json').read_text())['available_counts']['levels'][level]['distinct_available_tasks']
        assert counts['levels'][level]['distinct_available_tasks']>=min(5,previous+added)
    result = {'available_counts_after':counts,'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path, gid, verified, inv):
    preparation=json.loads((path/'preparation.json').read_text())
    counts=verified['available_counts_after']['levels']
    remaining={level:max(0,5-counts[level]['distinct_available_tasks']) for level in g.SUPPORTED_LEVELS}
    caps={'exceptions':[]}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated',
        'knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,
        'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],
        'supported_levels':list(g.SUPPORTED_LEVELS),'capability_exceptions':caps['exceptions'],
        'available_counts_before':preparation['available_counts'],
        'available_counts_after':verified['available_counts_after'],
        'shortage_remaining':remaining,
        'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],
        'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
        'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'validation.json',HERE/'bank-mapping.json',HERE/'classification.md',HERE/'template-extraction.md') if p.exists()],
        'note':'Triangle-area variants checked against displayed mathematics, geometry, complete banks, rounding and actual learner grading. Moderate/hard are explicitly authored workload policies. Opaque historical radio profiles are evidence only. Original source questions, canonical example and learner history preserved; unrated original remains unclassified.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='passed' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application api.lock acquired; rechecking current basis and inventory',flush=True)
        # Recover exact retained requests first. Never replace unknown intent with fresh identities.
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
        source_deltas=[]
        for mid,q in expected.items():
            present=copy.deepcopy(current[mid])
            if ':question/requires-calculator' not in q and ':question/requires-calculator' in present:
                source_deltas.append({'source_id':mid,'new_metadata':{':question/requires-calculator':present.pop(':question/requires-calculator')},'mathematical_content_unchanged':True})
            assert canonical(present)==canonical(q),'Source evidence changed; reclassify '+mid
        save(path/'source-refresh.json',{'basis':b,'additive_metadata':source_deltas,'all_prompts_solutions_fields_banks_ratings_unchanged':True})
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
        jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
        needed={level:max(jobs.get(level,{}).get('missing',0),5-counts['levels'][level]['distinct_available_tasks'],0) for level in g.SUPPORTED_LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(g.digest({**g.canonical(dict(u='58',v='40',angle=31)),'digits':2}))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);assert isinstance(instances,list)
        eligible=[];rejected=[]
        for rec in instances:
            if rec['question'][':question/difficulty'].split('/')[-1] not in g.SUPPORTED_LEVELS:
                rejected.append({'question_id':rec['question'][':question/id'],'reason':'Unsupported difficulty; not counted or committed'});continue
            validate_instance(rec);eligible.append(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(eligible),'unsupported_rejected':rejected,'generator_error':supplied.get('generatorError')})
        local=[]
        seed=int(JOB.name[:8],16)
        for level in g.SUPPORTED_LEVELS:
            selected=0
            for offset in range(200):
                if selected>=needed[level]:break
                rec=g.generate(level,seed+offset)
                fp=rec['generation']['math_fingerprint']
                if fp in used:continue
                validate_instance(rec);local.append(rec);selected+=1

        records=[];added={level:0 for level in g.SUPPORTED_LEVELS}
        for rec in eligible+local:
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                validate_instance(rec);records.append(rec);used.add(fp);added[level]+=1
        assets=[publish(r) for r in records]
        for rec in records:validate_instance(rec)
        save(path/'generated.json',records)
        for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in values]],path/'identity-check',attr.replace('/','-'),b),'Existing identity; reconcile first'
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records+eligible])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'new_by_level':added,'new_questions':len(records),'source_evidence_unchanged':True,'asset_hashes':assets,'available_counts':counts,'finite_remaining':{level:max(0,needed[level]-added[level]) for level in g.SUPPORTED_LEVELS},'selection':'Rechecked native inventory, current and historical presentations/reservations, mathematical validity and normalized prompt RHS; seed and choice order excluded'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'generator_registration_verified':True,'available_counts_after':counts}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'triangle-area-inventory-17592186105903-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()
