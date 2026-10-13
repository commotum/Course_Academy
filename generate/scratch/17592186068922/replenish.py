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
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'f7022189a6afff9689566b66632a86cd77f65e4765c3dcfb33dc0c247b09e718'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY = (HERE / 'source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

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

def fingerprint(q):
    return v.fingerprint(q)

USAGE_QUERY="""[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""
def available_counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    pools={level:[] for level in ('easy','moderate')};excluded=[]
    original={q[':db/id']:q for q in loads((HERE/'source.edn').read_text())[0][0][':knowledge-point/questions'] if q.get(':question/math-academy-id') in g.DATA}
    # Sources were replayed/graded completely; only unchanged evidence counts.
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if q[':db/id'] in unavailable:reason='Shown or reserved, including retained history'
        elif level not in pools:reason='Unrated or unsupported band'
        elif q[':db/id']==kp.get(':knowledge-point/canonical-example',{}).get(':db/id'):reason='Canonical example'
        elif q[':db/id'] in original and q==original[q[':db/id']]:reason=None
        else:
            reason='Unvalidated, incomplete or excluded source'
            # Validated stable generated identities can count on repeat runs.
            if ':question/math-academy-id' not in q:
                for t,params in g.candidates(level):
                    rec=g.generate(level,basis,t,params)
                    if rec['question'][':question/id']==str(q[':question/id']):
                        assert normalize(q)==ordered(rec['question']);v.check(rec);reason=None;break
        if reason:excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
        else:pools[level].append(q)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in rows}),'available_question_ids':[str(q[':question/id']) for q in rows]} for level,rows in pools.items()},'excluded':excluded}
    save(path/'available-counts.json',result);return result

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
        v.check(rec)
    assert not transaction([], kp, intent['generator_id'])
    counts=available_counts(path/'verified-inventory',kp,report[':edb/db-after-t'])
    remaining=json.loads((path/'finite-remaining.json').read_text())
    assert all(counts['levels'][level]['distinct_available_tasks']>=5 or remaining[level]>0 for level in ('easy','moderate'))
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in ('easy','moderate')}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0,'verified_distinct_available_counts':counts['levels']}
    save(path/'verification.json', result)
    return result

def finish(path,gid,verified,inv):
    caps=json.loads((HERE/'capabilities.json').read_text())
    remaining=json.loads((path/'finite-remaining.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'] if not verified.get('no_changes') else None,'verification_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':caps['supported_levels'],'unsupported_levels':['hard'],'capability_exceptions':caps['exceptions'],'excluded_source_questions':caps['excluded_source_questions'],'unsupported_levels_filled':False,'unfilled_hard_reserve':5,'remaining_supported_shortages':remaining,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'generator_registered':True,'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'inventory-after.json',path/'preparation.json',path/'available-counts.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'native-grading.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'review.json',HERE/'capabilities.json') if p.exists()],'note':'Validated easy/moderate bounded generator registered. Supported shortages filled only where independently verified; hard remains unsupported and unfilled. All source questions and learner history preserved.'}
    if (path/'commit-intent.json').exists():result['evidence'] += [str((path/name).relative_to(ROOT)) for name in ('commit-intent.json','transaction.edn','commit.edn','preview.edn')]
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','remaining_jobs','remaining_supported_shortages')}),flush=True)

def main():
    validation = json.loads((HERE/'validation.json').read_text())
    assert validation['passed']
    assert all(sha(ROOT/p)==digest for p,digest in validation['hashes'].items())
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE and intent['transaction_sha256'] == sha(path/'transaction.edn')
                assert intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report = DB._commit(intent, path/'transaction.edn', path)
                verified = verify(path, intent, report)
                finish(path, intent['generator_id'], verified, inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        b = inv['basis']
        assert DB.basis() == b
        path = OUT / ('basis-'+str(b))
        path.mkdir(exist_ok=True)
        kp = read_kp(path, b)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        evidence=loads((HERE/'source.edn').read_text())[0][0]
        expected={q[':db/id']:q for q in evidence[':knowledge-point/questions']}
        current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(current[e]==q for e,q in expected.items()), 'Source evidence changed; reclassify'
        assert kp[':knowledge-point/canonical-example']==evidence[':knowledge-point/canonical-example']
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        jobs = {j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint'] == KP}
        counts=available_counts(path,kp,b)
        needed={level:max(jobs.get(level,{}).get('missing',0),5-counts['levels'][level]['distinct_available_tasks'],0) for level in ('easy','moderate')}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        if kp.get(':knowledge-point/canonical-example'):used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[]
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        selected={level:0 for level in needed}
        for rec in instances:
            v.check(rec)
            level=rec['question'][':question/difficulty'].split('/')[-1]
            assert level in needed and rec['knowledge_point']['db_id']==KP
            fp=fingerprint(rec['question']);assert fp==rec['generation']['mathematical_fingerprint']
            if selected[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);selected[level]+=1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        local=json.loads((HERE/'previews.json').read_text())
        # Reuse the validated finite generator when preview tasks were already
        # consumed. Mathematical fingerprints, rather than seeds, select stock.
        seen_local={fingerprint(rec['question']) for rec in local}
        for level in needed:
            for template,parameters in g.candidates(level):
                rec=g.generate(level,b,template,parameters)
                fp=fingerprint(rec['question'])
                if fp not in seen_local:
                    local.append(rec);seen_local.add(fp)
        for rec in local:
            level=rec['question'][':question/difficulty'].split('/')[-1]
            fp=fingerprint(rec['question'])
            if selected[level]<needed[level] and fp not in used:
                v.check(rec)
                records.append(copy.deepcopy(rec));used.add(fp);selected[level]+=1
        remaining={level:max(0,needed[level]-selected[level]) for level in needed}
        save(path/'finite-remaining.json',remaining)
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        collisions=DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',b) if ids else []
        assert not collisions,'Generated identity already exists outside this KP; reconcile before commit'
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or (len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        for attr,values in [('answer-field/id',[f[':answer-field/id'] for rec in records for f in rec['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for rec in records for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            rows=DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in values]],path/'identity-check',attr.replace('/','-'),b) if values else []
            assert not rows,'Generated field/answer identity collision'
        assets=[]  # All templates have plot rating none.
        save(path/'local-preview.json',local);save(path/'generated.json',records)
        save(path/'native-input.json',[v.native(rec['question'][':question/id'],rec) for rec in instances+records])
        subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'local_previews':len(local),'new_questions':len(records),'source_evidence_unchanged':True,'asset_hashes':assets,'inventory_count_evidence':{level:jobs.get(level,{'missing':0}) for level in needed},'available_counts':counts,'finite_remaining':remaining,'distinctness':'Reduced actual printed rational integrand; algebraic form, seed, UUID, profile and bank order excluded'})
        forms = transaction(records, kp, gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'generator_registration_verified':True}
            save(path/'verification.json',verified)
            finish(path,gid,verified,inv)
            return
        txpath = path/'transaction.edn'
        tx = dumps(forms)+'\n'
        with txpath.open('w') as f:
            f.write(tx)
            f.flush()
            os.fsync(f.fileno())
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr = loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == b
        check_report(pr, path/'preview-check', source[0][0])
        assert DB.basis() == b
        intent = {'database':'math', 'endpoint':DB.args.endpoint, 'lineage':LINEAGE, 'source':SOURCE, 'source_eid':source[0][0], 'basis':b, 'expected_basis':b, 'request_key':'partial-fractions-replenish-17592186068922-'+str(b)+'-'+sha(txpath), 'transaction_sha256':sha(txpath), 'sha256':sha(txpath), 'exact_edn':tx, 'generator_id':gid, 'generator_path':SCRIPT, 'generator_sha256':sha(HERE.with_suffix('.py')), 'question_uuids':[rec['question'][':question/id'] for rec in records], 'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified, inventory(path/'inventory-after.json'))

if __name__ == '__main__':
    main()
