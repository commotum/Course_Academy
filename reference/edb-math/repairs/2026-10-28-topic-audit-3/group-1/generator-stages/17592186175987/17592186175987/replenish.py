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
from capture.scripts.database.images import ImageLibrary
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.gen
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '05abd65b4c7133224bf41048615b599b3f28940705e335ca521df2bade862074'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-ef48cfde3a25d91e'
QUERY = (HERE / 'reference/source-query.edn').read_text()
LEVELS = ('easy', 'moderate', 'hard')

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and '/_' not in str(k)}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value, uuid.UUID):return str(value)
    return value

def fingerprint(q):
    """Read the mathematical task; exclude seed, bank, identity and asset paths."""
    rec={'question':q,'generation':{'template':'source'}}
    sid=q.get(':question/math-academy-id')
    if sid=='e-9076':
        P,Q=2*g.Y+g.sp.log(g.sp.sqrt(g.X+5)),g.sp.exp(g.Y/3)+3*g.X
        a,b,radius=g.sp.pi/2,2*g.sp.pi,3
    elif '{{field-1}}' in q[':question/problem']:
        supplied=re.search(r'\{∬\}_\{D\}(.*?)\\,\\text\{d\}A',q[':question/problem'],re.S)[1]
        curl=v.expr(supplied)
        f={f[':answer-field/key']:f for f in q[':question/answer-fields']}
        def correct(field):
            target=field[':answer-field/correct'][1]
            return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==target)
        return g.digest(['convert_supplied_curl',str(g.sp.expand(curl)),str(g.sp.pi/2),str(v.expr(correct(f['field-2']))),str(v.expr(correct(f['field-3'])))])
    else:
        P,Q=v.prompt_field(rec)
        f=q[':question/answer-fields'][0];target=f[':answer-field/correct'][1]
        answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==target)
        _,a,b,radius=v.integral_parts(answer)
    return g.digest(['provided_partials' if 'The cross partials are' in q[':question/problem'] else 'derive_polar_setup',str(g.sp.expand(P)),str(g.sp.expand(Q)),str(a),str(b),str(radius)])

def validate_instance(rec):
    assert rec['knowledge_point']['db_id']==KP
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    assert rec['generation']['version']==g.VERSION
    v.check_normal(rec)
    gm=rec['generation']
    replay=g.generate(rec['question'][':question/difficulty'].split('/')[-1],gm['seed'],gm['template'],parameters=gm['parameters'],profile=gm['profile'])
    assert replay['question'][':question/id']==rec['question'][':question/id']
    assert fingerprint(replay['question'])==fingerprint(rec['question'])

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    bad={d['source_id'] for d in json.loads((HERE/'validation.json').read_text())['source_defects']}
    known={r['question'][':question/id']:r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text())}
    levels={l:[] for l in LEVELS};excluded=[];checks=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id');reason=None
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if q[':db/id'] in unavailable:reason='shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'):reason='canonical example'
        elif level not in LEVELS:reason='unrated or unsupported'
        elif sid in bad:reason='documented source mathematical, bank or context defect'
        elif sid:
            template=next(t for t,z in g.SPECS.items() if z[0]==sid)
            z=g.SPECS[template]
            rec=g.generate('moderate',template=template,parameters={'scale':1,'radius':z[3]},profile='observed')
            rec['question']=normalize(q);v.check_normal(rec)
            checks.append(v.engine_item(rec,sid));levels[level].append(q)
        elif str(q[':question/id']) in known:
            rec=known[str(q[':question/id'])];assert normalize(q)==ordered(rec['question']);validate_instance(rec)
            checks.append(v.engine_item(rec,str(q[':question/id'])));levels[level].append(q)
        else:reason='unrecognized generated question requires validation'
        if reason:excluded.append({'db_id':q[':db/id'],'source_id':sid,'reason':reason})
    if checks:
        save(path/'available-native-input.json',checks)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True,stdout=subprocess.DEVNULL)
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(normalize(q)) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for l,qs in levels.items()},'excluded_questions':excluded,'excluded_shown_or_reserved':sorted(unavailable)}
    save(path/'available-counts.json',result);return result

def publish(records,path):
    library=ImageLibrary(Path('/media/jake/SSD/EDB/math'),HERE)
    for rec in records:
        q=rec['question']
        for key in (':question/problem',':question/worked-solution'):
            q[key]=library.text(q[key])
        rec['generation']['assets']=[library.saved[p] for p in library.saved if library.saved[p]['path'] in q[':question/problem']+q[':question/worked-solution']]
        validate_instance(rec)
    save(path/'assets.json',library.saved)

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

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q)==ordered(rec['question'])
        validate_instance(rec)
        for a in rec['generation']['assets']:assert sha(Path('/media/jake/SSD/EDB/math')/a['path'])==a['sha256']
    assert not transaction([],kp,intent['generator_id'])
    stock=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':stock}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    remaining={l:max(0,5-verified['available_counts_after']['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified.get('basis_after'),'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'observed_levels':['moderate'],'authored_levels':['easy','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':{l:verified['available_counts_after']['levels'][l]['distinct_available_tasks'] for l in LEVELS},'shortage_by_level':remaining,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'preparation.json',path/'generated.json',path/'assets.json',path/'native-report.json',path/'preview.edn',path/'transaction.edn',path/'commit-intent.json',path/'commit.edn',path/'inventory-after.json',HERE/'validation.json',HERE/'freeze.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json') if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)

def main():
    frozen=json.loads((HERE/'freeze.json').read_text())
    assert frozen['passed'] and all(sha(ROOT/p)==h for p,h in frozen['hashes'].items())
    validation=json.loads((HERE/'validation.json').read_text());assert validation['normal_correctness']=='passed' and validation['raw_exact_prompt']==len(g.QS)
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
                assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                finish(path,intent['generator_id'],verify(path,intent,report),inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
        kp=read_kp(path,basis);(path/'before.edn').write_text(dumps(kp)+'\n')
        expected=g.SOURCE['record'];existing={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
        assert all(canonical(existing[q[':question/id']])==canonical(q) for q in expected[':knowledge-point/questions']), 'Source content changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(expected[':knowledge-point/canonical-example'])
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(contributor)==1
        gen=kp.get(':knowledge-point/question-generator')
        byscript=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',basis)
        assert len(byscript)<=1
        if gen:assert gen[':question-generator/script']==SCRIPT
        gid=str(gen[':question-generator/id']) if gen else str(byscript[0][0][':question-generator/id']) if byscript else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'course-academy-generator'))
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not collision or collision[0][0][':question-generator/script']==SCRIPT
        stock=counts(kp,path/'current-inventory',basis)
        needed={l:max(0,5-stock['levels'][l]['distinct_available_tasks']) for l in LEVELS};selected={l:0 for l in LEVELS}
        used={fingerprint(normalize(q)) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];local=[]
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        for rec in instances:
            validate_instance(rec);l=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if selected[l]<needed[l] and fp not in used:records.append(rec);used.add(fp);selected[l]+=1
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances)})
        for l in LEVELS:
            if not needed[l]:continue
            for i in range(1000):
                rec=g.generate(l,22875987+i);validate_instance(rec)
                if i<5:local.append(rec)
                fp=fingerprint(rec['question'])
                if selected[l]<needed[l] and fp not in used:records.append(rec);used.add(fp);selected[l]+=1
                if i>=4 and selected[l]==needed[l]:break
        publish(records,path)
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        collisions=DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',basis) if ids else []
        assert not collisions,'Generated UUID collision requires reconciliation'
        save(path/'generated.json',records);save(path/'local-preview.json',local)
        save(path/'native-input.json',[v.engine_item(rec,rec['question'][':question/id']) for rec in instances+local+records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,stdout=subprocess.DEVNULL)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':stock,'missing_by_level':needed,'generated_by_level':selected,'bounded_sampling_attempts_per_level':1000,'shortage_remaining':{l:needed[l]-selected[l] for l in LEVELS},'new_questions':len(records),'source_evidence_unchanged':True,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'assets':json.loads((path/'assets.json').read_text()),'distinctness':'Independent rendered field expressions, requested response role, radius and angular bounds; excludes seed, UUID, bank and choice order.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':None,'new_questions':0,'by_level':selected,'available_counts_after':stock,'passed':True}
            save(path/'verification.json',verified);finish(path,gid,verified,inventory(path/'inventory-after.json'));return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
        check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':basis,'expected_basis':basis,'request_key':'greens-polar-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report),inventory(path/'inventory-after.json'))

if __name__=='__main__':main()

