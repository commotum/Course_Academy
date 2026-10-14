"""Scoped additive inventory commits through the existing EDB integration."""
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
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/question_capture')]
from database import Database, StaleBasis
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment

spec = importlib.util.spec_from_file_location('derivative_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '8b9467499a91aae97f20ee77fadedaf5db08ea8b091b709fc7551820c5f6a552'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = Path((HERE / 'reference/initial/native-path.txt').read_text())
QUERY = (HERE / 'source-query.edn').read_text()
LOCK = ROOT / '.local/learning/requests/math/api.lock'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(value):
    if isinstance(value, dict):
        return {str(k): canonical(x) for k, x in sorted(value.items())}
    if isinstance(value, list):
        return sorted([canonical(x) for x in value], key=lambda x: json.dumps(x, sort_keys=True))
    return str(value) if isinstance(value, uuid.UUID) else value

def fingerprint(q):
    prompt = q[':question/problem']
    if 'spherical balloon' in prompt:
        return g.digest({'output':'volume','input':'radius','shape':'sphere','fixed':None})
    _, _, out, inp = v.read_displayed_roles({'question':q})
    if prompt.startswith('Consider a regular '):
        shape = re.search(r'Consider a regular (\w+)',prompt)[1]
    else:
        shapes = ('parallelogram','rectangle','triangle','cylinder','ellipse','sphere','circle','square','cube','cone')
        shape = next(s for s in shapes if re.search(r'\b'+s+r'\b', prompt))
    fixed = None
    if 'fixed' in prompt:
        if shape == 'ellipse': fixed = 'minor axis' if inp == 'major axis' else 'major axis'
        elif shape in ('rectangle','triangle','parallelogram'): fixed = 'height' if inp == 'base' else 'base'
        elif shape in ('cylinder','cone'): fixed = 'height' if inp == 'radius' else 'radius'
    return g.digest({'output':out,'input':inp,'shape':shape,'fixed':fixed})

def inventory(path):
    request = {'action': 'inventory'}
    response = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input=json.dumps(request), env=ENV, capture_output=True, text=True, check=True, timeout=55)
    result = json.loads(response.stdout)
    assert result['ok'], result
    inv = result['data']
    assert inv['lineage'] == LINEAGE
    save(path, inv)
    return inv

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

def normalized(q):
    q = json.loads(json.dumps(q, default=str))
    out = {k: q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    d = q[':question/difficulty']
    out[':question/difficulty'] = d[':db/ident'] if isinstance(d, dict) else d
    fields = []
    for f in q[':question/answer-fields']:
        kind, correct = f[':answer-field/type'], f[':answer-field/correct']
        fields.append({':answer-field/id': f[':answer-field/id'], ':answer-field/key': f[':answer-field/key'], ':answer-field/type': kind[':db/ident'] if isinstance(kind, dict) else kind,
            ':answer-field/correct': [':answer/id', correct[':answer/id']] if isinstance(correct, dict) else correct,
            ':answer-field/choices': sorted([{':answer/id': a[':answer/id'], ':answer/value': a[':answer/value'], ':answer/type': a[':answer/type'][':db/ident'] if isinstance(a[':answer/type'], dict) else a[':answer/type']} for a in f[':answer-field/choices']], key=lambda a: a[':answer/value'])})
    out[':question/answer-fields'] = sorted(fields, key=lambda f: f[':answer-field/key'])
    return out

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'): a[':answer/id'], kw('answer/id'): uuid.UUID(a[':answer/id']), kw('answer/type'): kw(a[':answer/type']), kw('answer/value'): a[':answer/value'], kw('db/ensure'): kw('answer/validate')})
            forms.append({kw('db/id'): f[':answer-field/id'], kw('answer-field/id'): uuid.UUID(f[':answer-field/id']), kw('answer-field/key'): f[':answer-field/key'], kw('answer-field/type'): kw(f[':answer-field/type']), kw('answer-field/choices'): [a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'): f[':answer-field/correct'][1], kw('db/ensure'): kw('answer-field/validate')})
        forms.append({kw('db/id'): q[':question/id'], kw('question/id'): uuid.UUID(q[':question/id']), kw('question/problem'): q[':question/problem'], kw('question/worked-solution'): q[':question/worked-solution'], kw('question/difficulty'): kw(q[':question/difficulty']), kw('question/answer-fields'): [f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'): kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e: str(a) for e, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e, a, value, tx, s, added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected contributor or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'])
    kp = read_kp(path / 'readback', report[':edb/db-after-t'])
    before = loads((path / 'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e]) == canonical(q) for e, q in old.items())
    assert canonical({k: x for k, x in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}) == canonical({k: x for k, x in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')})
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path / 'generated.json').read_text())
    byid = {str(q[':question/id']): q for q in now.values()}
    assert len(now) == len(old) + len(records)
    fps = set()
    previous = {fingerprint(q) for q in before[':knowledge-point/questions']}
    previous.add(fingerprint(before[':knowledge-point/canonical-example']))
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalized(q) == normalized(rec['question'])
        fp = fingerprint(q)
        assert fp == rec['generation']['parameter_fingerprint'] and fp not in previous and fp not in fps
        fps.add(fp)
        v.inspect(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': report[':edb/db-after-t'], 'new_questions': len(records), 'by_level': {level: sum(r['question'][':question/difficulty'] == ':question.difficulty/' + level for r in records) for level in LEVELS}, 'unchanged_source_questions': len(old), 'unchanged_canonical_example': True, 'only_additive_scoped_content_datoms': True, 'learner_history_unchanged': True, 'generator_registration_verified': True, 'distinct_from_sources_and_each_other': True, 'repeat_preparation_content_changes': 0}
    save(path / 'verification.json', result)
    return result


USAGE = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def grade(records, path):
    path.mkdir(parents=True, exist_ok=True)
    save(path/'native-input.json', [v.engine_entry(r['question'][':question/id'], r) for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text())
    assert report['accepted_checks']==len(records) and report['rejected_checks']==4*len(records)
    assert report['documented_unresolved_checks']==0

def counts(kp, path, basis):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    canonical_ids={r[0] for r in DB.query('[:find ?q :in $ [?q ...] :where [_ :knowledge-point/canonical-example ?q]]',[[q[':db/id'] for q in kp[':knowledge-point/questions']]],path,'canonical-exclusions',basis)}
    available={level:set() for level in LEVELS};records=[];excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if level not in LEVELS:
            excluded.append({'id':str(q[':question/id']),'reason':'Unrated; original key and solution absent; preserved'})
            continue
        rec={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':normalized(q)}
        v.inspect(rec);records.append(rec)
        if q[':db/id'] not in shown|reserved|canonical_ids:available[level].add(fingerprint(q))
    if records:grade(records,path/'inventory-grading')
    result={'basis':basis,'distinct_available':{l:len(s) for l,s in available.items()},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'canonical_exclusions':sorted(canonical_ids),'excluded_source_questions':excluded}
    save(path/'available-counts.json',result)
    return result

def subset_equal(current, captured):
    if isinstance(captured,dict):
        return isinstance(current,dict) and all(k in current and subset_equal(current[k],x) for k,x in captured.items())
    if isinstance(captured,list):
        return len(current)==len(captured) and all(any(subset_equal(c,x) for c in current) for x in captured)
    return str(current)==str(captured)

def finish(path, gid, verified, inv):
    stock=counts(read_kp(path/'current-inventory',inv['basis']),path/'current-inventory',inv['basis'])
    remaining={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
    prep=json.loads((path/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'verified_commit_basis':verified.get('basis_after'),'lineage':LINEAGE,'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':stock['distinct_available'],'shortage_by_level':remaining,'capability_exceptions':prep['capability_exceptions'],'finite_catalog':{'easy':8,'moderate':20,'hard':8},'excluded_source_questions':stock['excluded_source_questions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'preparation.json',path/'generated.json',path/'native-report.json',path/'review.md',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json',path/'current-inventory/available-counts.json',HERE/'validation.json',HERE/'freeze.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'semantic-catalog.json',HERE/'capabilities.json'] if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_questions_by_level','available_by_level','shortage_by_level','remaining_jobs')}),flush=True)

def prepare_and_commit(preview):
    for path in sorted(OUT.glob('basis-*')):
        if (path/'commit-intent.json').exists():
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
            assert intent['generator_sha256']==sha(HERE.with_suffix('.py'))
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path)
            verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
    inv=inventory(OUT/'inventory-before.json');b=inv['basis']
    assert DB.basis()==b and LINEAGE in DB.command('status')
    path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
    kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
    original=json.loads((HERE/'source.json').read_text())['record']
    current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(subset_equal(current[q[':db/id']],q) for q in original[':knowledge-point/questions']), 'Source changed; reclassify'
    assert subset_equal(kp[':knowledge-point/canonical-example'],original[':knowledge-point/canonical-example'])
    (path/'before.edn').write_text(dumps(kp)+'\n')
    source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
    reg=kp.get(':knowledge-point/question-generator')
    existing=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b)
    assert len(existing)<=1
    idpath=HERE/'generator-id.json';saved=json.loads(idpath.read_text()) if idpath.exists() else {}
    gid=str(reg[':question-generator/id']) if reg else str(existing[0][0][':question-generator/id']) if existing else saved.get('id',str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator')))
    assert not saved or saved['id']==gid
    save(idpath,{'id':gid,'script':SCRIPT,'knowledge_point':KP})
    stock=counts(kp,path,b);needed={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
    used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    records=[];selected={l:0 for l in LEVELS}
    def consider(rec):
        v.inspect(rec);meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
        replay=g.generate(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
        assert normalized(rec['question'])==normalized(replay['question'])
        fp=fingerprint(rec['question']);assert fp==meta['parameter_fingerprint']
        if selected[level]<needed[level] and fp not in used:
            records.append(copy.deepcopy(rec));used.add(fp);selected[level]+=1
    supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
    if isinstance(instances,dict):instances=[instances]
    for rec in instances:consider(rec)
    seed=int(JOB.name[:8],16)
    for level,catalog in g.semantic_catalog().items():
        if level=="moderate":catalog=sorted(catalog,key=lambda item:item[0]!="moderate_fixed")
        # Exhaust the finite domain rather than relying on random seed counts.
        for i,(template,params) in enumerate(catalog):
            if selected[level]>=needed[level]:break
            consider(g.generate(level,seed+i,template=template,parameters=params))
    exceptions=[{'level':l,'type':'finite-semantic-domain','catalog_size':len(g.semantic_catalog()[l]),'requested':needed[l],'produced':selected[l],'shortage':needed[l]-selected[l],'filled':False,'evidence':'All catalog tasks evaluated; existing sources and canonical tasks excluded. Symbol/seed/choice order cannot create tasks.'} for l in LEVELS if selected[l]<needed[l]]
    for attr,label,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
        if ids:
            assert len(ids)==len(set(ids))
            assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+label,b),'Identity collision: reconcile before writing'
    registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
    assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
    save(path/'generated.json',records)
    if records:grade(instances+records,path)
    (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
    save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'generator_id':gid,'generator_path':SCRIPT,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_before':stock,'needed':needed,'selected':selected,'new_questions':len(records),'distinct_mathematical_tasks':len({fingerprint(r['question']) for r in records}),'capability_exceptions':exceptions,'supplied_generated_exists':supplied_path.exists(),'supplied_instances_validated':len(instances),'source_evidence_unchanged':True,'asset_hashes':[],'distinctness':'Geometric object, output, input, held dimension; excludes all current and canonical tasks; seed, bank, symbols and order ignored'})
    forms=transaction(records,kp,gid)
    if not forms:
        verified={'passed':True,'new_questions':0,'by_level':selected,'basis_after':None,'no_change_basis':b}
        save(path/'verification.json',verified);finish(path,gid,verified,inv);return
    txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
    with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
    response=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    (path/'preview.edn').write_text(response.stdout);pr=loads(response.stdout)
    assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
    check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
    if '--prepare-only' in sys.argv:
        print(json.dumps({'prepared_basis':b,'selected':selected,'review':str(path/'review.md'),'preview_validated':True}),flush=True);return
    intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'derivative-interpretation-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
    save(path/'commit-intent.json',intent)
    report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
    finish(path,gid,verified,inventory(path/'inventory-after.json'))

def main():
    assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
    for p,d in json.loads((HERE/'freeze.json').read_text())['sha256'].items():assert sha(ROOT/p)==d,'Frozen artifact changed: '+p
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    for attempt in range(3):
        try:
            with LOCK.open('a') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX);prepare_and_commit(preview)
            return
        except StaleBasis:
            if attempt==2:raise

if __name__=='__main__':main()
