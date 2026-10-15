"""Scoped additive linear-exponent inventory, exact requests and receipt readback."""
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database, StaleBasis
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning

KP, TOPIC = 17592186092260, 17592186050271
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'7116e35d995b3ef231e17799abde785497cb1c5d9a57b10b93b24b08a9d86f6a'
OUT = HERE/'reference/replenishment'
LOCK = ROOT/'.local/learning/requests/math/api.lock'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV.copy()
LEVELS = ('easy', 'moderate', 'hard')
QUERY = (OUT/'source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Load only independent displayed-string validators; preserve source replay artifacts.
assert json.loads((HERE/'validation.json').read_text())['status'] == 'passed'
helpers = {'__file__':str(HERE/'validate.py'), '__name__':'linear_readback'}
exec(compile((HERE/'validate.py').read_text().split("\nsource=json.load")[0], str(HERE/'validate.py'), 'exec'), helpers)
v = SimpleNamespace(**helpers)
g = v.g

USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/unlocked]
       [?status :db/ident :learner-task.status/started]
       [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id'}
    if isinstance(value, (tuple,list)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x,sort_keys=True))
    return str(value) if isinstance(value,uuid.UUID) else value

def normalized(q):
    q = json.loads(json.dumps(q, default=str))
    result = {k:q[k] for k in (':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty')}
    if isinstance(result[':question/difficulty'],dict):
        result[':question/difficulty'] = result[':question/difficulty'][':db/ident']
    fields = []
    for f in q[':question/answer-fields']:
        kind = f[':answer-field/type']
        correct = f[':answer-field/correct']
        fields.append({':answer-field/id':f[':answer-field/id'], ':answer-field/key':f[':answer-field/key'],
            ':answer-field/type':kind[':db/ident'] if isinstance(kind,dict) else kind,
            ':answer-field/correct':[':answer/id',correct[':answer/id']] if isinstance(correct,dict) else correct,
            ':answer-field/choices':sorted([{':answer/id':a[':answer/id'], ':answer/value':a[':answer/value'],
                ':answer/type':a[':answer/type'][':db/ident'] if isinstance(a[':answer/type'],dict) else a[':answer/type']}
                for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    result[':question/answer-fields'] = sorted(fields,key=lambda f:f[':answer-field/key'])
    return result

def record(q):
    template = q.get(':question/math-academy-id')
    if template is None:
        for saved in OUT.glob('basis-*/generated.json'):
            for rec in json.loads(saved.read_text()):
                if rec['question'][':question/id'] == str(q[':question/id']):
                    result = copy.deepcopy(rec);result['question'] = normalized(q);return result
    assert template in g.LEVEL, 'Unknown source family requires classification'
    return {'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE}, 'question':normalized(q), 'generation':{'template':template}}

def printed_math(q):
    import re
    ms = re.findall(r'\$(.*?)\$',q[':question/problem'],re.S)
    definition = next(z for z in ms if 'f(x)=' in z.replace(' ','') or z.startswith('y='))
    f = v.parse(definition.split('=',1)[1].strip().rstrip('.,'))
    z = next((v.parse(m.split('=',1)[1].rstrip('.')) for m in ms if m.startswith('x=')),None)
    kind = 'tangent' if 'equation of the tangent' in q[':question/problem'] else 'slope' if 'slope' in q[':question/problem'] else 'derivative'
    return f,z,kind

def fingerprint(q):
    f,z,kind = printed_math(q)
    # Derivative-only tasks ignore additive constants and presentation/bank aliases.
    semantic = [kind,sp.srepr(sp.expand(sp.diff(f,v.x)))] if kind == 'derivative' else [kind,sp.srepr(sp.expand(f)),sp.srepr(z)]
    return hashlib.sha256(g.stable(semantic).encode()).hexdigest()

def validate_record(rec):
    q = rec['question']
    assert q.get(':question/answer-fields') and q.get(':question/worked-solution')
    assert len({f[':answer-field/key'] for f in q[':question/answer-fields']}) == len(q[':question/answer-fields'])
    for f in q[':question/answer-fields']:
        assert f.get(':answer-field/correct') and any(a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices'])
    v.formatting(q)
    check = copy.deepcopy(rec)
    for f in check['question'][':question/answer-fields']:
        if f[':answer-field/type'].endswith('/blank'):
            correct = next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert all(v.equal(v.parse(a[':answer/value']),v.parse(correct[':answer/value'])) for a in f[':answer-field/choices']), 'Non-equivalent blank-bank alias'
            # Current capture may retain several equivalent canonical fragments.
            # Collapse only the validation copy; grading uses the complete record.
            f[':answer-field/choices'] = [correct]
    v.actual_math(check)

def engine_checks(rec):
    tests=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        correct=f[':answer-field/correct'][1]
        if f[':answer-field/type'].endswith('/radio'):
            tests.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete owned choice ID'} for a in f[':answer-field/choices'])
        else:
            answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
            tests.extend([{'field_index':i,'submitted':answer,'expected':'accepted','purpose':'canonical fragment'},
                {'field_index':i,'submitted':'2('+answer+')/2','expected':'accepted','purpose':'equivalent fragment'},
                {'field_index':i,'submitted':'('+answer+')+1','expected':'rejected','purpose':'incorrect fragment'}])
    return tests

def read_kp(path,basis):
    return DB.query(QUERY,[[KP]],path,'kp',basis)[0][0]

def inventory(binary,path):
    r = subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint], input='{"action":"inventory"}',
        env=ENV,capture_output=True,text=True,check=True,timeout=55)
    reply = json.loads(r.stdout)
    assert reply['ok'] and reply['data']['lineage'] == LINEAGE
    save(path,reply['data'])
    return reply['data']

def available_counts(kp,basis,path):
    unavailable = {r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    pools = {l:[] for l in LEVELS}
    excluded,checked = [],[]
    for q in kp[':knowledge-point/questions']:
        level = q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
        reason = None
        if q[':db/id'] in unavailable:reason = 'Presented or reserved, including retained history'
        elif level not in LEVELS:reason = 'Unrated; excluded from inventory'
        else:
            try:
                rec = record(q)
                assert len({f[':answer-field/key'] for f in rec['question'][':question/answer-fields']}) == len(rec['question'][':question/answer-fields'])
                validate_record(rec)
            except (KeyError,ValueError,AssertionError,TypeError) as error:
                reason = 'Incomplete field or failed independent printed mathematical readback: '+type(error).__name__+' '+str(error)
        if reason:excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
        else:
            pools[level].append(q)
            checked.append({'label':str(q[':question/id']),'record':rec,'checks':engine_checks(rec)})
    save(path/'available-native-input.json',checked)
    native(path/'available-native-input.json',path/'available-native-report.json')
    result = {'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),
        'rated_gradable_unseen_unreserved':len(qs),'question_ids':[str(q[':question/id']) for q in qs]} for l,qs in pools.items()},
        'excluded':excluded,'unavailable_including_history':sorted(unavailable),
        'counting':'Independent printed function, answer bank and solution readback plus current native grading; mathematical task fingerprints ignore seed/identity/notation/choice order. Canonical example never included.'}
    save(path/'available-counts.json',result)
    return result

def native(input_path,output_path):
    subprocess.run([str(OUT/'check-engine'),str(input_path),str(output_path)],check=True,timeout=55)
    report = json.loads(output_path.read_text())
    assert report['documented_unresolved_checks'] == 0
    return report

def transaction(records,kp,gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_datoms(report,path,source):
    attrs = {e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')} | {':answer-field/'+s for s in ('id','key','type','choices','correct')} | {':answer/'+s for s in ('id','type','value')} | {':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name != ':db/txInstant':assert e in new and name in allowed

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    kp = read_kp(path/'readback',report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e]) == canonical(q) for e,q in old.items())
    omit = {':knowledge-point/questions',':knowledge-point/question-generator'}
    assert canonical({k:x for k,x in before.items() if k not in omit}) == canonical({k:x for k,x in kp.items() if k not in omit})
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old)+len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    used = {fingerprint(q) for q in old.values()}
    for rec in records:
        validate_record(rec)
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalized(q) == normalized(rec['question'])
        fp = fingerprint(q)
        assert fp not in used
        used.add(fp)
    assert not transaction([],kp,intent['generator_id'])
    counts = available_counts(kp,report[':edb/db-after-t'],path/'readback')
    result = {'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],
        'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},
        'available_counts_after':counts,'unchanged_source_questions':len(old),'unchanged_canonical_example':True,
        'source_attribution':SOURCE,'only_additive_requested_kp_content_datoms':True,'learner_history_unchanged':True,
        'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result)
    return result

def finish(binary,path,gid,verified):
    inv = inventory(binary,path/'inventory-after.json')
    levels = verified['available_counts_after']['levels']
    remaining = {l:max(0,5-levels[l]['distinct_available_tasks']) for l in LEVELS}
    result = {'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':TOPIC,
        'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],
        'preparation_basis':verified['basis_before'],'new_questions':verified['new_questions'],'new_by_level':verified.get('new_by_level',{}),
        'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,
        'difficulty_evidence':{'easy':'Observed linear-exponent chain products, including signed scales and translation',
            'moderate':'Observed sum-rule, log-point slope and reciprocal-point tangent templates',
            'hard':'Validated authored shifted and vertically translated tangent calculation; nonunit a,c, nonzero b,d, point (1-b)/a'},
        'available_by_level':{l:levels[l]['distinct_available_tasks'] for l in LEVELS},'shortage_remaining':remaining,
        'capability_exceptions':[],'source_questions_and_learner_history_preserved':True,
        'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint'] == KP],
        'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',
            path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'generated.json',path/'native-report.json',
            path/'inventory-after.json',path/'readback/available-counts.json',HERE/'classification.md',HERE/'classification-current.md',HERE/'template-extraction.md',
            HERE/'validation.json',HERE/'generator-freeze.json',OUT/'current-native-build.json') if p.exists()]}
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_remaining')},indent=2),flush=True)

def prepare(binary,preview):
    # Resolve any retained exact request first, including a lost response.
    for path in sorted(OUT.glob('basis-*')):
        if not (path/'commit-intent.json').exists():continue
        intent = json.loads((path/'commit-intent.json').read_text())
        assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['source'] == SOURCE
        assert intent['endpoint'] == DB.args.endpoint and intent['transaction_sha256'] == sha(path/'transaction.edn')
        assert intent['exact_edn'] == (path/'transaction.edn').read_text() and intent['generator_sha256'] == sha(HERE.with_suffix('.py'))
        assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
        return finish(binary,path,intent['generator_id'],verify(path,intent,DB._commit(intent,path/'transaction.edn',path)))
    for rel,digest in json.loads((HERE/'generator-freeze.json').read_text())['artifacts'].items():
        assert sha(ROOT/rel) == digest, 'Validated artifact changed: '+rel
    inv = inventory(binary,OUT/'inventory-under-lock.json')
    basis = inv['basis']
    assert DB.basis() == basis
    path = OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
    kp = read_kp(path,basis)
    assert str(kp[':knowledge-point/id']) == g.KP_UUID
    (path/'before.edn').write_text(dumps(kp)+'\n')
    captured = json.loads((HERE/'source.json').read_text())['record']
    current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
    assert set(current) >= {q[':question/math-academy-id'] for q in captured[':knowledge-point/questions']}
    changes = []
    for q in captured[':knowledge-point/questions']:
        now=current[q[':question/math-academy-id']]
        # New capture repaired q-11817 and updated q-340496's equivalent answer.
        assert fingerprint(q) == fingerprint(now), 'Changed source mathematics requires reclassification'
        if canonical(now) != canonical(q):changes.append(q[':question/math-academy-id'])
    save(path/'source-refresh.json',{'basis':basis,'frozen_basis':1356,'source_questions':len(current),'changed_records':changes,'all_source_mathematical_tasks_unchanged':True,'source_edits':0})
    contributor = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis)
    assert len(contributor) == 1
    gen = kp.get(':knowledge-point/question-generator')
    registered = DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',basis)
    assert len(registered) <= 1
    identity_path = HERE/'generator-id.json'
    identity = json.loads(identity_path.read_text()) if identity_path.exists() else {}
    gid = str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else identity.get('id',str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator')))
    assert not identity or identity['id'] == gid
    identity_value = {'id':gid,'script':SCRIPT,'knowledge_point':KP}
    if identity != identity_value:save(identity_path,identity_value)
    collision = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',basis)
    assert not collision or collision[0][0][':question-generator/script'] == SCRIPT
    counts = available_counts(kp,basis,path)
    needed = {l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
    used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    records,checked = [],[]
    added = {l:0 for l in LEVELS}
    def consider(rec):
        assert rec['knowledge_point']['db_id'] == KP and rec['knowledge_point']['id'] == g.KP_UUID
        level = rec['question'][':question/difficulty'].split('/')[-1]
        assert level in LEVELS
        validate_record(rec)
        replay = g.generate(level, rec['generation']['seed'],template=rec['generation']['template'],
            parameters=rec['generation']['parameters'],profile=rec['generation']['profile'],
            field_type=rec['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1])
        assert replay == rec, 'Supplied generator output differs from deterministic replay'
        assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
        checked.append(rec)
        fp = fingerprint(rec['question'])
        if added[level] < needed[level] and fp not in used:
            records.append(rec);used.add(fp);added[level] += 1
    supplied_path = JOB.with_suffix('.generated')
    supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances = supplied.get('instances',[])
    if isinstance(instances,dict):instances = [instances]
    assert isinstance(instances,list)
    for rec in instances:consider(rec)
    templates = {l:[t for t in g.LEVEL if g.LEVEL[t]==l] for l in LEVELS}
    for level in LEVELS:
        for attempt in range(200):
            if added[level] >= needed[level]:break
            consider(g.generate(level,int(JOB.name[:8],16)+attempt,template=templates[level][attempt%len(templates[level])]))
    save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
    save(path/'generated.json',records)
    save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':engine_checks(r)} for r in checked])
    native(path/'native-input.json',path/'native-report.json')
    for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),
        ('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),
        ('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
        if values:
            assert len(set(values)) == len(values)
            assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in values]],path/'identity-check',attr.replace('/','-'),basis), 'Existing identity requires reconciliation'
    save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_version':g.VERSION,
        'needed':needed,'new_by_level':added,'available_counts':counts,'asset_hashes':[],
        'source_evidence_unchanged':True,'selection':'Independent readback and native grading; distinct mathematical functions/evaluation tasks; no seed/identity/choice-order duplicates',
        'finite_remaining':{l:needed[l]-added[l] for l in LEVELS},'original_job_request':json.loads(JOB.with_suffix('.json').read_text())['request']})
    forms = transaction(records,kp,gid)
    if not forms:
        verified = {'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'new_by_level':added,'no_changes':True,'available_counts_after':counts}
        save(path/'verification.json',verified)
        return finish(binary,path,gid,verified)
    txpath = path/'transaction.edn';tx = dumps(forms)+'\n'
    with txpath.open('w') as stream:
        stream.write(tx);stream.flush();os.fsync(stream.fileno())
    r = subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    (path/'preview.edn').write_text(r.stdout)
    report = loads(r.stdout)
    assert report[':edb/committed'] is False
    if report[':edb/db-before-t'] != basis or DB.basis() != basis:raise StaleBasis('Basis advanced during preparation')
    check_datoms(report,path/'preview-check',contributor[0][0])
    intent = {'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],
        'basis':basis,'expected_basis':basis,'request_key':'linear-exponent-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),
        'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,
        'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],
        'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
    save(path/'commit-intent.json',intent)
    report = DB._commit(intent,txpath,path)
    return finish(binary,path,gid,verify(path,intent,report))

def main():
    binary = build_learning(ROOT.parent/'EDB')
    # Recompile the fixture against the same current engine used by the app.
    native_source = OUT/'check-engine.rs'
    native_source.write_text((ROOT/'generate/runs/current/check-engine.rs').read_text())
    libs = {name:max((ROOT/'target/release/deps').glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)
        for name in ('course_academy_engine','serde_json')}
    build = {'source_sha256':sha(native_source),'libraries':{name:{'path':str(p),'sha256':sha(p)} for name,p in libs.items()}}
    subprocess.run(['rustc','--edition=2024','-O',str(native_source),*[x for name,p in libs.items() for x in ('--extern',name+'='+str(p))],
        '-L','dependency='+str(ROOT/'target/release/deps'),'-o',str(OUT/'check-engine')],check=True,timeout=55)
    save(OUT/'current-native-build.json',build)
    # Recheck every completed replay fixture with the current learner grader.
    native(HERE/'engine-input.json',OUT/'current-replay-native-report.json')
    preview = preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application api.lock acquired; rechecking inventory and basis',flush=True)
        for attempt in range(3):
            try:return prepare(binary,preview)
            except StaleBasis:
                if attempt == 2:raise
                print('Confirmed basis change; rebuilding against current inventory',flush=True)

if __name__ == '__main__':main()
