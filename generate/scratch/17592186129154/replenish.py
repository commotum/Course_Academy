"""Scoped replenishment; api.lock covers basis recheck, submission and readback."""
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

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(ROOT/'scripts/question_capture'))
import validate_current as v
import commit_helpers as h
from database import Database
from edn import dumps, loads
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment

g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = v.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'3bf66f06d91abae2e3361f167059cc742ccb42b8d4b2e6c48947680f53b82b0b'
OUT = HERE/'reference/replenishment'
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),
                             database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'
h.DB, h.KP, h.SCRIPT = DB, KP, SCRIPT

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    result = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint],
                            input='{"action":"inventory"}', env=database_environment('math'),
                            capture_output=True, text=True, check=True, timeout=90)
    wrapper = json.loads(result.stdout)
    assert wrapper['ok'] and wrapper['data']['lineage'] == LINEAGE
    save(path, wrapper['data'])
    return wrapper['data']

def read_kp(path, basis):
    return DB.query((HERE/'source-query.edn').read_text(), [[KP]], path, 'kp', basis)[0][0]

def plain(value):
    return json.loads(json.dumps(value, default=str))

def known_records():
    records = {}
    for path in OUT.glob('basis-*/generated.json'):
        for rec in json.loads(path.read_text()):
            records[rec['question'][':question/id']] = rec
    return records

def counts(kp, path, basis):
    unavailable = {row[0] for row in DB.query((HERE/'unavailable-query.edn').read_text(),
                                           [LEARNER, KP], path, 'unavailable', basis)}
    sources = {q[':db/id']:q for q in v.SOURCE['record'][':knowledge-point/questions']}
    generated = known_records()
    used = set()
    stock = {level:set() for level in g.SUPPORTED_LEVELS}
    excluded = []
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in sources:
            assert plain(q) == sources[q[':db/id']], 'Current source evidence changed; reclassify'
            name = q[':question/math-academy-id']
            t = g.RECIPES[name]
            p = {k:t[k] for k in ('roots', 'multiplicities', 'coefficient')}
            fp = g.mathematical_fingerprint(p, g.claims_for(t, p))
        else:
            rec = generated[str(q[':question/id'])]
            assert v.normalize(q) == v.ordered(rec['question'])
            v.check(rec)
            fp = rec['generation']['mathematical_fingerprint']
        used.add(fp)
        if ':question/difficulty' not in q:
            excluded.append({'source_id':q[':db/id'], 'reason':'unrated; preserved unchanged'})
            continue
        level = str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        if q[':db/id'] not in unavailable:
            stock[level].add(fp)
    assert plain(kp[':knowledge-point/canonical-example']) == v.SOURCE['record'][':knowledge-point/canonical-example']
    # Canonical categories and claims independently read from its retained graph.
    used.add(g.mathematical_fingerprint({'roots':[-3,-1,2], 'multiplicities':[1,2,1], 'coefficient':'1/6'},
                                      [['even',1], ['simple_pair',0,2], ['limit',-1,-1]]))
    result = {'basis':basis, 'distinct_available':{k:len(x) for k,x in stock.items()},
              'missing':{k:max(0,5-len(x)) for k,x in stock.items()},
              'excluded':excluded, 'unavailable_ids':sorted(unavailable),
              'supported_levels':list(g.SUPPORTED_LEVELS), 'validated_source_questions':len(sources),
              'authored_hard_level':True, 'source_and_canonical_facts_unchanged':True}
    save(path/'validated-inventory.json', result)
    return result, used

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    h.check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    for key in before:
        if key not in (':knowledge-point/questions', ':knowledge-point/question-generator'):
            assert kp[key] == before[key]
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert v.normalize(q) == v.ordered(rec['question'])
        v.check(rec)
        assert sha(Path('/media/jake/SSD/EDB/math')/rec['generation']['plot']) == rec['generation']['asset_sha256']
    assert not h.transaction([], kp, intent['generator_id'])
    stock, used = counts(kp, path/'post-inventory', report[':edb/db-after-t'])
    assert all(rec['generation']['mathematical_fingerprint'] in used for rec in records)
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'],
              'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty'].endswith('/'+level)
              for r in records) for level in g.SUPPORTED_LEVELS}, 'unchanged_existing_questions':len(old),
              'unchanged_canonical_example':True, 'learner_history_unchanged':True,
              'only_additive_scoped_content_datoms':True, 'generator_registration_verified':True,
              'repeat_preparation_content_changes':0, 'inventory':stock}
    save(path/'verification.json', result)
    return result

def finish(path, gid, verified):
    inv = inventory(path/'inventory-after.json')
    shortages = {k:n for k,n in verified['inventory']['missing'].items() if n}
    result = {'outcome':'finite-limit' if shortages else 'generated', 'knowledgePoint':KP,
              'generator_path':SCRIPT, 'generator_id':gid, 'lineage':LINEAGE,
              'verified_commit_basis':verified['basis_after'], 'new_questions':verified['new_questions'],
              'generated_by_level':verified['by_level'], 'supported_levels':list(g.SUPPORTED_LEVELS),
              'unsupported_levels':[], 'supported_inventory':verified['inventory']['distinct_available'],
              'remaining_supported_shortages':shortages, 'unsupported_levels_filled':False,
              'difficulty_evidence':'Easy/Moderate source labels; explicit authored four-root Hard family',
              'finite_variant_limits':{k:x['meaningful_tasks'] for k,x in json.loads((HERE/'finite-domains.json').read_text()).items()},
              'capability_exceptions':json.loads((path/'preparation.json').read_text())['capability_exceptions'],
              'inventory_recheck_basis':inv['basis'], 'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
              'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json', path/'preparation.json',
                path/'commit-intent.json', path/'commit.edn', path/'preview.edn', path/'inventory-after.json',
                path/'post-inventory/validated-inventory.json', HERE/'current-validation.json',
                HERE/'current-classification.md', HERE/'current-template-extraction.md', HERE/'plot-extraction.md')]}
    save(path/'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','supported_inventory','remaining_jobs')}))

def main():
    validation = json.loads((HERE/'current-validation.json').read_text())
    assert validation['passed']
    assert all(sha(ROOT/p) == digest for p,digest in validation['hashes'].items())
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),
                                  repo_root=ROOT, preview_bin=None), threading.Event())
    lock_path = ROOT/'.local/learning/requests/math/api.lock'
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE
                assert intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['transaction_sha256'] == sha(path/'transaction.edn')
                report = DB._commit(intent, path/'transaction.edn', path)
                finish(path, intent['generator_id'], verify(path, intent, report))
                return
        inv = inventory(OUT/'inventory-under-lock.json')
        b = inv['basis']
        assert DB.basis() == b
        path = OUT/('basis-'+str(b))
        path.mkdir(parents=True, exist_ok=True)
        kp = read_kp(path, b)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        stock, used = counts(kp, path/'count-before', b)
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(source) == 1
        registered = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',
                              [uuid.UUID(gid)], path, 'generator-identity', b)
        assert not registered or registered[0][0][':question-generator/script'] == SCRIPT
        supplied_file = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_file.read_text()) if supplied_file.exists() else {}
        instances = supplied.get('instances', [])
        if isinstance(instances, dict): instances = [instances]
        selected = {level:0 for level in g.SUPPORTED_LEVELS}
        records = []
        for rec in instances:
            v.check(rec)
            level = rec['question'][':question/difficulty'].split('/')[-1]
            fp = rec['generation']['mathematical_fingerprint']
            if fp not in used and selected[level] < stock['missing'][level]:
                records.append(copy.deepcopy(rec)); used.add(fp); selected[level] += 1
        exceptions = []
        for level in g.SUPPORTED_LEVELS:
            for seed in range(500):
                if selected[level] >= stock['missing'][level]: break
                rec = g.generate(level, seed=int(JOB.name[:8],16)+seed)
                v.check(rec)
                fp = rec['generation']['mathematical_fingerprint']
                if fp in used: continue
                records.append(rec); used.add(fp); selected[level] += 1
            if selected[level] < stock['missing'][level]:
                exceptions.append({'level':level, 'shortage':stock['missing'][level]-selected[level],
                                   'filled':False, 'reason':'Bounded 500-seed distinct-task search exhausted'})
        identities = [uuid.UUID(r['question'][':question/id']) for r in records]
        if identities:
            assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',
                                [identities], path, 'generated-identities', b)
        library = ImageLibrary(Path('/media/jake/SSD/EDB/math'))
        assets = []
        for rec in records:
            asset = Path(rec['generation']['plot'])
            relative = library.put_bytes(asset.read_bytes(), content_type='image/png')
            rec['question'][':question/problem'] = rec['question'][':question/problem'].replace(str(asset), relative)
            rec['generation'].update(plot_original=str(asset), plot=relative, asset_sha256=sha(asset))
            assert (Path('/media/jake/SSD/EDB/math')/relative).read_bytes() == asset.read_bytes()
            assets.append({'local':str(asset), 'stored':relative, 'sha256':sha(asset)})
            v.check(rec)
        save(path/'generated.json', records)
        save(path/'native-input.json', [v.native(r['question'][':question/id'], r) for r in records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(path/'native-input.json'),
                        str(path/'native-report.json')], check=True)
        save(path/'preparation.json', {'basis':b, 'lineage':LINEAGE, 'source':SOURCE,
              'generator_id':gid, 'missing':stock['missing'], 'selected':selected,
              'capability_exceptions':exceptions, 'asset_hashes':assets,
              'supplied_instances_validated':len(instances), 'supplied_file_exists':supplied_file.exists(),
              'current_validation_sha256':sha(HERE/'current-validation.json'),
              'generator_sha256':sha(HERE.with_suffix('.py')), 'dependency_versions':{
              'python':sys.version, 'sympy':g.sp.__version__, 'matplotlib':g.matplotlib.__version__}})
        forms = h.transaction(records, kp, gid)
        assert forms, 'No changes; reuse existing verified receipt'
        txpath = path/'transaction.edn'
        tx = dumps(forms)+'\n'
        with txpath.open('w') as stream:
            stream.write(tx); stream.flush(); os.fsync(stream.fileno())
        preview_result = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath),
                                        '--source', SOURCE], env=DB.env, capture_output=True, text=True,
                                        check=True, timeout=90)
        (path/'preview.edn').write_text(preview_result.stdout)
        pr = loads(preview_result.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == b
        h.check_report(pr, path/'preview-check', source[0][0])
        assert DB.basis() == b
        intent = {'database':'math', 'endpoint':DB.args.endpoint, 'lineage':LINEAGE,
                  'source':SOURCE, 'source_eid':source[0][0], 'basis':b, 'expected_basis':b,
                  'request_key':'polynomial-statements-'+str(KP)+'-'+str(b)+'-'+sha(txpath),
                  'transaction_sha256':sha(txpath), 'sha256':sha(txpath), 'exact_edn':tx,
                  'generator_id':gid, 'generator_path':SCRIPT, 'generator_sha256':sha(HERE.with_suffix('.py')),
                  'question_uuids':[r['question'][':question/id'] for r in records], 'lock':str(lock_path)}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        finish(path, gid, verify(path, intent, report))

if __name__ == '__main__':
    main()
