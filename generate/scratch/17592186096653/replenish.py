"""Additive ratio-vector inventory, guarded by the application lock and basis."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import math
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
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
from capture.scripts.database.edn import dumps, loads, kw
from capture.scripts.storage import atomic_json, atomic_text
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database, QUESTION_PULL

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

v = module('ratio_validation', HERE / 'validate.py')
g = v.g
finder = module('ratio_inventory_reader', ROOT / 'generate/scripts/find_candidates.py')
KP = g.KP_ID
TOPIC = 17592186048780
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '6ce6a7be69dc97f4040fed5499a50a80fcb0788fc58d24dec23ed0eaf6df9e77'
OUT = ROOT / 'reference/edb-math/imports/generated' / str(KP)
CFG = Config()
CLIENT = EDBClient(CFG, threading.Event())
DB = Database(SimpleNamespace(edb_bin=str(CFG.edb_bin), database='math', endpoint=CFG.endpoint))
LEVELS = ('easy', 'moderate', 'hard')
QUERY = '[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example ' + QUESTION_PULL + '} {[:knowledge-point/questions :limit nil] ' + QUESTION_PULL + '}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
USAGE = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path, binary):
    req = dict(database='math', learner=LEARNER, topics=[TOPIC], activity_type='lesson')
    r = subprocess.run([str(binary)], input=json.dumps(req), env=DB.env, text=True,
                       capture_output=True, check=True, timeout=60)
    x = json.loads(r.stdout)
    assert x['cursor']['lineage'] == LINEAGE
    atomic_json(path, x)
    return next(k for t in x['topics'] for k in t['knowledge_points'] if k['db/id'] == KP), x['basis']

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

def fingerprint(q):
    try:
        p = g.parameters_for(q)
    except ValueError:
        # The canonical example states its ratio without AX:XB notation.
        m = re.search(r'in the ratio \$(\d+):(\d+)', q[':question/problem'])
        if not m: raise
        p = dict(r=int(m[1]), s=int(m[2]))
    return g.digest([str(g.sp.Rational(p['s'], p['r']+p['s'])), str(g.sp.Rational(p['r'], p['r']+p['s']))])

def validate_existing(q):
    p = g.parameters_for(q)
    t = g.sp.Rational(p['r'], p['r']+p['s']); a = 1-t
    fields = sorted(q[':question/answer-fields'], key=lambda f:f[':answer-field/key'])
    assert q.get(':question/worked-solution') and fields
    if fields[0][':answer-field/type'][':db/ident'] == ':answer-field.type/radio':
        assert len(fields) == 1
        f = fields[0]; bank = f[':answer-field/choices']
        values = [v.rhs(x[':answer/value'], p) for x in bank]
        assert len(values) == len(set(values)) == 5
        expected = a*v.U+t*v.V
        assert sum(x == expected for x in values) == 1
        assert v.rhs(f[':answer-field/correct'][':answer/value'],p) == expected
        assert f[':answer-field/correct'][':answer/id'] in {x[':answer/id'] for x in bank}
    else:
        assert len(fields) == 2
        for f, expected in zip(fields, [a,t]):
            assert f[':answer-field/type'][':db/ident'] == ':answer-field.type/blank'
            assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
            assert v.parse(f[':answer-field/correct'][':answer/value']) == expected
            assert f[':answer-field/correct'][':answer/id'] in {x[':answer/id'] for x in f[':answer-field/choices']}

def counts(path, kp, basis):
    unavailable = {r[0] for r in DB.query(USAGE, [KP,LEARNER], path, 'unavailable', basis)}
    unavailable.update(r[0] for r in DB.query(USAGE, [KP,LEARNER], path, 'historically-unavailable', basis, history=True))
    tasks = {level:set() for level in LEVELS}; excluded = []
    for q in kp[':knowledge-point/questions']:
        level = str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        try:
            assert q[':db/id'] not in unavailable, 'Shown or reserved, including history'
            assert not q.get(':knowledge-point/_canonical-example'), 'Canonical example'
            assert level in LEVELS, 'Unrated'
            validate_existing(q)
            tasks[level].add(fingerprint(q))
        except (AssertionError, KeyError, ValueError, TypeError) as error:
            excluded.append(dict(question=str(q[':question/id']), source=q.get(':question/math-academy-id'), reason=str(error) or 'Invalid mathematical answer/field'))
    result = dict(basis=basis, distinct_available={k:len(x) for k,x in tasks.items()}, fingerprints={k:sorted(x) for k,x in tasks.items()}, excluded=excluded)
    atomic_json(path/'available-counts.json', result)
    return result

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
    attrs = dict(DB.attributes(path, report[':edb/db-before-t']))
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected contributor/retraction'
        name = str(attrs[a])
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    b = report[':edb/db-after-t']
    check_report(report, path/'receipt-check', intent['source_eid'])
    before = loads((path/'before.edn').read_text()); after = read_kp(path/'readback', b)
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in after[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items()), 'Original question/answer history changed'
    assert {k:x for k,x in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k:x for k,x in after.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old)+len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
        validate_existing(q)
        assets = rec['generation']['published_assets']
        for asset in assets:
            assert sha(CFG.math_root / asset['path']) == asset['sha256']
    assert not transaction([], after, intent['generator_id'])
    count = counts(path/'readback', after, b)
    result = dict(passed=True, basis_before=intent['basis'], basis_after=b, new_questions=len(records), unchanged_source_questions=len(old), canonical_unchanged=True, learner_history_unchanged=True, only_scoped_additions=True, repeat_preparation_content_changes=0, available_counts_after=count, generator_registration_verified=True)
    atomic_json(path/'verification.json', result)
    return result

def finish(path, gid, verified, binary):
    native, basis = inventory(path/'inventory-after.json', binary)
    count = verified['available_counts_after']['distinct_available']
    preparation = json.loads((path/'preparation.json').read_text())
    remaining = {level:max(0,5-count[level]) for level in LEVELS}
    result = dict(outcome='finite-limit' if any(remaining.values()) else 'generated', knowledgePoint=KP, topic=TOPIC, generator_path=SCRIPT, generator_id=gid, verified_commit_basis=verified['basis_after'], lineage=LINEAGE, source=SOURCE, new_questions=verified['new_questions'], new_questions_by_level=preparation['new_by_level'], available_by_level=count, native_available_by_level=native['inventory']['available'], inventory_recheck_basis=basis, supported_levels=list(LEVELS), unsupported_levels=[], unsupported_levels_filled=False, remaining_supported_shortages=remaining, capability_exceptions=[], finite_limits=json.loads((HERE/'capabilities.json').read_text())['finite_limits'], evidence=[str(p.relative_to(ROOT)) for p in path.iterdir() if p.is_file()]+[str((HERE/n).relative_to(ROOT)) for n in ('validation.json','classification.md','template-extraction.md','plot-extraction.md','capabilities.json','current-engine-build.json')], note='Source ratios, common scaling, seed, labels and choice order cannot create new mathematical tasks. Source content is preserved; incomplete source records are excluded from validated inventory. Authored easy/hard workload constraints retain the internal-section method.')
    atomic_json(path/'outcome.json', result)
    atomic_json(JOB.with_suffix('.result'), result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level')}), flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['status'] == 'passed'
    binary = finder.build(ROOT.parent/'EDB')
    preview = preview_executable(CFG, threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        status = CLIENT.status(); assert status['lineage'] == LINEAGE
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists(): continue
            intent = json.loads((path/'commit-intent.json').read_text())
            assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE
            assert intent['transaction_sha256'] == sha(path/'transaction.edn')
            assert intent['exact_edn'] == (path/'transaction.edn').read_text()
            if not (path/'commit.edn').exists():
                assert CLIENT.status()['basis'] == intent['basis'], 'Basis advanced; return to preparation before submission'
            report = DB._commit(intent,path/'transaction.edn',path)
            finish(path,intent['generator_id'],verify(path,intent,report),binary)
            return
        native, b = inventory(OUT/'inventory-current.json',binary)
        assert CLIENT.status()['basis'] == b
        path = OUT/('basis-'+str(b)); path.mkdir(exist_ok=True)
        kp = read_kp(path,b); assert str(kp[':knowledge-point/id']) == g.KP_UUID
        atomic_text(path/'before.edn',dumps(kp)+'\n')
        current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for mid,q in g.QS.items():
            new = current[mid]
            for k in (':question/problem',':question/worked-solution'):
                assert new.get(k) == q.get(k), 'Source changed; reclassify '+mid
            assert [[a[':answer/value'] for a in f[':answer-field/choices']] for f in new[':question/answer-fields']] == [[a[':answer/value'] for a in f[':answer-field/choices']] for f in q[':question/answer-fields']]
        count = counts(path,kp,b)
        needed = {level:max(0,5-count['distinct_available'][level]) for level in LEVELS}
        used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        original_used = set(used)
        gen = kp.get(':knowledge-point/question-generator')
        regs = DB.query('[:find ?g ?id :in $ ?script :where [?g :question-generator/script ?script] [?g :question-generator/id ?id]]',[SCRIPT],path,'generator-identity',b)
        assert len(regs)<=1
        gid = str(gen[':question-generator/id']) if gen else str(regs[0][1]) if regs else g.uid('question-generator')
        records=[]; added={level:0 for level in LEVELS}
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=instances.get('instances',[])
        for rec in instances:
            v.inspect(rec); assert rec['generation']['raw_wrong_blank_key'] is False
            level=rec['question'][':question/difficulty'].split('/')[-1]
            assert level in LEVELS
            fp=fingerprint(rec['question'])
            if fp not in used and added[level]<needed[level]:
                records.append(rec);used.add(fp);added[level]+=1
        atomic_json(path/'supplied-status.json',dict(exists=supplied_path.exists(),validated=len(instances)))
        # Bounded exhaustive domain in seed-selected order, with coprime tasks.
        import random
        for level in LEVELS:
            bound={'easy':4,'moderate':12,'hard':20}[level]
            pairs=[(r,s) for r in range(1,bound+1) for s in range(1,bound+1) if math.gcd(r,s)==1 and (level!='hard' or min(r,s)>=5 and r+s>=19)]
            random.Random(int(JOB.name[:8],16)).shuffle(pairs)
            for r,s in pairs:
                if added[level]>=needed[level]:break
                fp=g.digest([str(g.sp.Rational(s,r+s)),str(g.sp.Rational(r,r+s))])
                if fp in used:continue
                kind='coefficients' if added[level]%2==0 or r==s else 'radio'
                rec=g.generate(level,int(JOB.name[:8],16)+added[level],kind,parameters=dict(A='A',B='B',X='T',u='a',v='b',r=r,s=s))
                v.inspect(rec);assert fingerprint(rec['question'])==fp
                records.append(rec);used.add(fp);added[level]+=1
        assert len({fingerprint(r['question']) for r in records}) == len(records)
        images=ImageLibrary(CFG.math_root,path)
        for rec in records:
            plot=Path(rec['generation']['plot']);data=plot.read_bytes();relative=images.store(data,str(plot))
            assert sha(CFG.math_root/relative)==hashlib.sha256(data).hexdigest()
            rec['generation']['published_assets']=[dict(path=relative,sha256=hashlib.sha256(data).hexdigest())]
            rec['question'][':question/problem']=rec['question'][':question/problem'].replace(str(plot),relative)
        atomic_json(path/'generated.json',records)
        for kind in ('question','answer-field','answer'):
            items=[x for rec in records for x in ([rec['question']] if kind=='question' else rec['question'][':question/answer-fields'] if kind=='answer-field' else [a for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]
            ids=[uuid.UUID(x[':'+kind+'/id']) for x in items]; assert len(ids)==len(set(ids))
            assert not DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]',[ids],path,'identity-'+kind,b)
        engine=[v.native(rec,'commit:'+str(i)) for i,rec in enumerate(records)]
        atomic_json(path/'native-input.json',engine)
        subprocess.run([str(HERE/'check-current-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        atomic_json(path/'preparation.json',dict(basis=b,lineage=LINEAGE,source=SOURCE,generator_id=gid,generator_path=SCRIPT,generator_sha256=sha(HERE.with_suffix('.py')),new_by_level=added,needed_by_level=needed,available_counts=count,native_inventory=native['inventory'],finite_remaining={level:max(0,needed[level]-added[level]) for level in LEVELS},existing_tasks=len(original_used),distinct_new_tasks=len(records),dependency_versions={'sympy':g.sp.__version__,'python':sys.version},assets=images.saved))
        forms=transaction(records,kp,gid)
        assert forms, 'No fresh changes; verify existing registered inventory instead'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=60)
        atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b)
        assert len(source)==1
        check_report(pr,path/'preview-check',source[0][0])
        assert CLIENT.status()==dict(database='math',lineage=LINEAGE,basis=b)
        intent=dict(database='math',endpoint=CFG.endpoint,lineage=LINEAGE,source=SOURCE,source_eid=source[0][0],basis=b,expected_basis=b,request_key='ratio-vector-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),transaction_sha256=sha(txpath),sha256=sha(txpath),exact_edn=tx,generator_id=gid,generator_path=SCRIPT,question_uuids=[r['question'][':question/id'] for r in records],lock=str(ROOT/'.local/learning/requests/math/api.lock'))
        atomic_json(path/'commit-intent.json',intent)
        if '--prepare-only' in sys.argv:
            print('Prepared',len(records),'questions at basis',b,'with native preview; commit pending.')
            return
        report=DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report),binary)

if __name__=='__main__':main()
