"""Add only distinct validated vector-field tasks; retain guarded requests/receipts."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('vector_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'question-generator'))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'00e6089982c3551c3c5885a5b43ed4cdd0e108bde50747d37fad406c29ab9531'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env = database_environment('math')
NATIVE = ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'
QUERY = (HERE/'reference/source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=DB.env, capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def canonical(x):
    if isinstance(x, dict):
        return {str(k):canonical(z) for k,z in x.items() if '/_' not in str(k) and not (k == ':db/id' and ':db/ident' in x)}
    if isinstance(x, (list, tuple)):
        return sorted((canonical(z) for z in x), key=lambda z:json.dumps(z, sort_keys=True))
    if isinstance(x, uuid.UUID):
        return str(x)
    if isinstance(x, str):
        return str(x)
    return x

def normalize(q):
    out = {k:str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    level = q[':question/difficulty']
    out[':question/difficulty'] = str(level[':db/ident']) if isinstance(level, dict) else level
    out[':question/answer-fields'] = []
    for f in q[':question/answer-fields']:
        kind = f[':answer-field/type']
        correct = f[':answer-field/correct']
        out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(kind[':db/ident']) if isinstance(kind,dict) else kind, ':answer-field/correct':[':answer/id',str(correct[':answer/id'])] if isinstance(correct,dict) else correct, ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']) if isinstance(a[':answer/type'],dict) else a[':answer/type'], ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return out

def task_fingerprint(rec):
    m = rec['generation']
    p = m['parameters']
    # Mathematical field and unordered rational tails; profiles/order/UUIDs do not count.
    return g.digest({'field':[g.s.srepr(z) for z in g.field_components(m['template'],p)], 'points':sorted([[str(g.rat(z)) for z in row] for row in p['points']]), 'grid':1 if m['level']=='easy' else str(g.s.Rational(1,2 if m['level']=='moderate' else 4))})

def localize(rec, path):
    v.verify(rec)
    library = ImageLibrary(Path(DB.env['EDB_MATH_ROOT']), path)
    q = copy.deepcopy(rec['question'])
    mapping = {}
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']:
            original = a[':answer/value']
            relative = library.resolve(original)
            mapping[original] = relative
            a[':answer/value'] = relative
            assert sha(Path(DB.env['EDB_MATH_ROOT'])/relative) == sha(Path(original))
    for key in (':question/problem', ':question/worked-solution'):
        for original,relative in mapping.items():
            q[key] = q[key].replace(original, relative)
    return {'question':q, 'generation':rec['generation'], 'knowledge_point':rec['knowledge_point'], 'raw_record':rec, 'asset_map':library.saved}

def check_localized(rec):
    v.verify(rec['raw_record'])
    expected = copy.deepcopy(rec['raw_record']['question'])
    for original,asset in rec['asset_map'].items():
        target = Path(DB.env['EDB_MATH_ROOT'])/asset['path']
        assert target.exists() and sha(target) == asset['sha256'] == sha(Path(original))
        for f in expected[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                if a[':answer/value'] == original:
                    a[':answer/value'] = asset['path']
        for key in (':question/problem', ':question/worked-solution'):
            expected[key] = expected[key].replace(original, asset['path'])
    assert normalize(expected) == normalize(rec['question'])

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def saved_records():
    return [r for path in sorted(OUT.glob('basis-*/generated.json')) for r in json.loads(path.read_text())]

def source_record(sid):
    return g.generate('easy', 71, g.OBSERVED[sid][0], parameters=g.source_parameters(sid), profile='observed_'+sid)

def counts(kp, path, basis):
    unavailable = {r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    # Retained presentations cannot become fresh by removal from current tasks.
    historical = DB.query('[:find ?q :in $ [?q ...] :where [_ :task-item/content ?q ?tx ?source true]]', [[q[':db/id'] for q in kp[':knowledge-point/questions']]], path, 'historical-presentations', basis, history=True)
    unavailable.update(r[0] for r in historical)
    known = {r['question'][':question/id']:r for r in saved_records()}
    rows = {l:{} for l in LEVELS}
    used = set()
    excluded = []
    for q in kp[':knowledge-point/questions']:
        sid = q.get(':question/math-academy-id')
        if sid in g.OBSERVED:
            raw = source_record(sid)
            fp = task_fingerprint(raw)
            used.add(fp)
            # Source errors are evidence only, never silently repaired in place.
            if ':question/difficulty' not in q or ':question/worked-solution' not in q or len(q[':question/answer-fields']) != 1 or ':answer-field/correct' not in q[':question/answer-fields'][0]:
                excluded.append({'id':str(q[':question/id']),'reason':'unrated, missing solution/key, or duplicate response fields'})
                continue
            v.verify(raw)
            sf = q[':question/answer-fields'][0]
            correct_path = str(Path(DB.env['EDB_MATH_ROOT'])/sf[':answer-field/correct'][':answer/value'])
            rf = raw['question'][':question/answer-fields'][0]
            assert correct_path == next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id'] == rf[':answer-field/correct'][1])
            candidate = {'question':normalize(q)}
        elif str(q[':question/id']) in known:
            rec = known[str(q[':question/id'])]
            check_localized(rec)
            assert normalize(q) == normalize(rec['question'])
            fp = task_fingerprint(rec)
            used.add(fp)
            candidate = rec
        else:
            raise AssertionError('Unrecognized content requires classification before replenishment')
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):
            continue
        level = q[':question/difficulty'][':db/ident'].split('/')[-1]
        rows[level][fp] = candidate
    # Canonical task is assessed at its three explicitly supplied points.
    canonical_question = kp[':knowledge-point/canonical-example']
    prompt = canonical_question[':question/problem']
    field_tex = re.search(r'\$F\(x,y\)=(.*?)\$',prompt)
    if field_tex:
        field = v.parse(field_tex[1])
        points = re.findall(r'F\(([^)]*)\)\s*&\s*=',canonical_question.get(':question/worked-solution',''))
        if len(points)==3:
            fs = [g.s.expand(field).coeff(v.I),g.s.expand(field).coeff(v.J)]
            used.add(g.digest({'field':[g.s.srepr(z.xreplace({v.X:g.X,v.Y:g.Y})) for z in fs], 'points':sorted([[str(v.parse(z)) for z in p.split(',')] for p in points]), 'grid':1}))
    cases = []
    for level in LEVELS:
        for fp,rec in rows[level].items():
            cases.append(v.engine_case(rec,level+'/'+fp))
    save(path/'inventory-native-input.json',cases)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'inventory-native-input.json'),str(path/'inventory-native-report.json')],check=True)
    native = json.loads((path/'inventory-native-report.json').read_text())
    assert native['accepted_checks'] == len(cases) and native['rejected_checks'] == 4*len(cases)
    result = {'basis':basis, 'levels':{l:{'distinct_available_tasks':len(rows[l]), 'available_question_ids':[r['question'][':question/id'] for r in rows[l].values()]} for l in LEVELS}, 'excluded_shown_or_reserved':sorted(unavailable), 'excluded_incomplete_sources':excluded, 'mathematical_deduplication':True}
    save(path/'available-counts.json',result)
    return result,used

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
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    attrs = {e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution/retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis = report[':edb/db-after-t']
    kp = read_kp(path/'readback',basis)
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:z for k,z in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')} == {k:z for k,z in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old)+len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q) == normalize(rec['question'])
        check_localized(rec)
    assert not transaction([],kp,intent['generator_id'])
    c,_ = counts(kp,path/'readback',basis)
    result = {'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result)
    return result

def finish(path,gid,verified,inv):
    prep = json.loads((path/'preparation.json').read_text())
    after = verified['available_counts_after']
    remaining = {l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result = {'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'validation-receipt.json',HERE/'capabilities.json') if p.exists()]}
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
    validation = json.loads((HERE/'validation.json').read_text())
    receipt = json.loads((HERE/'validation-receipt.json').read_text())
    assert validation['status'] == 'pass' and receipt['generator_sha256'] == sha(HERE.with_suffix('.py')) and receipt['validator_sha256'] == sha(HERE/'validate.py') and receipt['validation_sha256'] == sha(HERE/'validation.json')
    preview = preview_executable(SimpleNamespace(math_root=Path(DB.env['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE and intent['transaction_sha256'] == sha(path/'transaction.edn') and intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report = DB._commit(intent,path/'transaction.edn',path)
                verified = verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        basis = inv['basis']
        assert DB.basis() == basis
        path = OUT/('basis-'+str(basis))
        path.mkdir(exist_ok=True)
        kp = read_kp(path,basis)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured = g.SOURCE['record']
        current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:
            assert canonical(current[q[':question/math-academy-id']]) == canonical(q), 'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example']) == canonical(captured[':knowledge-point/canonical-example'])
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        registered = DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'registered-generator',basis)
        if registered:
            assert len(registered)==1
            gid = str(registered[0][0][':question-generator/id'])
        orphan = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not orphan or orphan[0][0][':question-generator/script'] == SCRIPT
        c,used = counts(kp,path,basis)
        needed = {l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        added = {l:0 for l in LEVELS}
        records = []
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances',[])
        assert isinstance(instances,list)
        for rec in instances:
            v.verify(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        # Bounded search exercises actual changed fields/coordinates, not choice shuffles.
        candidates = instances+[r['record'] for r in json.loads((HERE/'review.json').read_text()) if 'authored-default' in r['label']]
        for level in LEVELS:
            for seed in range(1000,1100):
                if added[level] == needed[level]:
                    break
                rec = next((r for r in candidates if r['generation']['level'] == level and task_fingerprint(r) not in used),None)
                if rec is not None:
                    candidates.remove(rec)
                else:
                    rec = g.generate(level,seed)
                fp = task_fingerprint(rec)
                if fp in used:
                    continue
                v.verify(rec)
                records.append(localize(rec,path))
                used.add(fp)
                added[level] += 1
        ids = [uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id']]+[f[':answer-field/id'] for f in rec['question'][':question/answer-fields']]+[a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        existing = DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing, 'Existing identities require reconciliation'
        save(path/'generated.json',records)
        native = [v.engine_case(r,r['question'][':question/id']) for r in records]
        save(path/'native-input.json',native)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        report = json.loads((path/'native-report.json').read_text())
        assert report['accepted_checks'] == len(records) and report['rejected_checks'] == 4*len(records)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':[asset for r in records for asset in r['asset_map'].values()],'source_evidence_unchanged':True,'source_basis':g.SOURCE['basis']})
        forms = transaction(records,kp,gid)
        if not forms:
            verified = {'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c}
            save(path/'verification.json',verified)
            finish(path,gid,verified,inv)
            return
        txpath = path/'transaction.edn'
        tx = dumps(forms)+'\n'
        with txpath.open('w') as f:
            f.write(tx)
            f.flush()
            os.fsync(f.fileno())
        r = subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr = loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == basis
        check_report(pr,path/'preview-check',source[0][0])
        assert DB.basis() == basis
        intent = {'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'vector-field-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report = DB._commit(intent,txpath,path)
        verified = verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__ == '__main__':
    main()
