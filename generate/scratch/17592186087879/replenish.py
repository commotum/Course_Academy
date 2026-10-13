"""Scoped additive ODE inventory replenishment with saved basis-guarded requests."""
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
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('ode_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
c = g
s = g.sp
KP = g.KP
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'b5ddfdc824fdb876f747bc122e58f210d97978bfd8afe06d8e724aba23804cfd'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True,exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-0ee7e7bd24d378f7'
DISCOVERY = ROOT/'.local/generate/find-candidates-b13a7928a9573a2f'
LEVELS = ('easy','moderate','hard')
FAMILIES = {l:[t for t,(level,_) in g.AUTH.items() if level==l] for l in LEVELS}
Q = '''[* {:question/difficulty [:db/id :db/ident]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'''
QUERY = '[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data'])
    return x['data']

def counts(path):
    request={'database':'math','learner':LEARNER,'topics':[17592186048569],'activity_type':'lesson','after_basis':None,'lineage':None,'at':None}
    r = subprocess.run([str(DISCOVERY)],input=json.dumps(request),env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout)
    assert x['cursor']['lineage']==LINEAGE
    save(path,x)
    pools=[kp for t in x['topics'] for kp in t['knowledge_points'] if kp['db/id']==KP]
    assert len(pools)==1
    return x['basis'],pools[0]['inventory']['available']

def read_kp(path,basis):
    return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def validated_counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    known={}
    for p in OUT.glob('basis-*/generated.json'):
        for rec in json.loads(p.read_text()):known[rec['question'][':question/id']]=rec
    rows={l:[] for l in LEVELS};excluded=[];fixtures=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if q[':db/id'] in unavailable:
            excluded.append({'id':str(q[':question/id']),'reason':'shown or reserved'});continue
        if sid in ('q-334916','q-335811','q-335812','q-335830'):
            excluded.append({'id':str(q[':question/id']),'source_id':sid,'reason':'incomplete fields, duplicate correct solutions, or redundant IF bank'});continue
        if sid in g.OBS:
            level,_,p,_,_=g.OBS[sid]
            rec=g.generate(level,template=sid,parameters=p,profile='observed')
            v.check_record(rec)
            assert str(q[':question/difficulty'][':db/ident'])==rec['question'][':question/difficulty']
            # Source-bank replay and source evidence were checked against this basis.
            rec['question']=normalize(q)
        elif str(q[':question/id']) in known:
            rec=known[str(q[':question/id'])];check(rec)
            assert normalize(q)==ordered(rec['question'])
        else:
            excluded.append({'id':str(q[':question/id']),'reason':'unrecognized validation provenance'});continue
        level=rec['question'][':question/difficulty'].split('/')[-1]
        rows[level].append((fingerprint(q),str(q[':question/id'])))
        fixtures.append(native(rec))
    save(path/'available-native-input.json',fixtures)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True,stdout=subprocess.DEVNULL)
    grade=json.loads((path/'available-native-report.json').read_text())
    assert grade['documented_unresolved_checks']==0
    result={l:len({fp for fp,_ in qs}) for l,qs in rows.items()}
    save(path/'validated-available-counts.json',{'basis':basis,'available_by_level':result,'question_ids':{l:[qid for _,qid in qs] for l,qs in rows.items()},'excluded':excluded,'canonical_excluded':True,'native_grading':{k:v for k,v in grade.items() if k!='records'}})
    return result

def source_projection(actual,expected):
    if isinstance(expected,dict):
        assert all(k in actual for k in expected)
        return {k:source_projection(actual[k],val) for k,val in expected.items()}
    if isinstance(expected,list):
        assert len(actual)==len(expected)
        if expected and isinstance(expected[0],dict):
            key=next(k for k in (':db/id',':answer/id',':answer-field/id',':question/id') if k in expected[0])
            actual=sorted(actual,key=lambda a:str(a[key]));expected=sorted(expected,key=lambda a:str(a[key]))
        return [source_projection(a,e) for a,e in zip(actual,expected)]
    return str(actual) if isinstance(expected,str) else actual

def fingerprint(q):
    """Printed normalized ODE plus initial point/value; no banks, IDs or seeds."""
    q=copy.deepcopy(q)
    prompt=q[':question/problem']
    prompt=re.sub(r'\\dfrac\s*\{\s*\\textrm\{d\}y\s*\}\s*\{\s*\\textrm\{d\}x\s*\}',r'\\frac{dy}{dx}',prompt)
    prompt=prompt.replace(r'\qquad',r'\quad')
    q[':question/problem']=prompt
    P,Q,t,h=v.displayed_problem({'question':q})
    return hashlib.sha256(json.dumps([s.srepr(s.simplify(z)) for z in (P,Q,t,h)]).encode()).hexdigest()

def check(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.SOURCE['record'][':knowledge-point/id']
    meta=rec['generation'];assert meta['profile']=='authored' and not meta['source_ambiguous_bank']
    level=rec['question'][':question/difficulty'].split('/')[-1]
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
    assert ordered(replay['question'])==ordered(rec['question'])
    assert meta['mathematical_fingerprint']==replay['generation']['mathematical_fingerprint']
    v.check_record(rec)
    return True

def native(rec):
    return {'label':rec['question'][':question/id'],'record':rec,'checks':v.native_checks(rec)}

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
        assert str(gen[':question-generator/id']) == gid
        if gen.get(':question-generator/script') != SCRIPT:
            forms.append([kw('db/add'),gen[':db/id'],kw('question-generator/script'),SCRIPT])
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
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:val for k,val in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:val for k,val in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question'])
        assert fingerprint(q)==rec['generation']['inventory_fingerprint']
        check(rec)
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result)
    return result

def finish(path,gid,verified,inv,available):
    prep=json.loads((path/'preparation.json').read_text())
    shortage={l:max(0,5-available[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'observed_levels':['moderate','hard'],'authored_levels':['easy'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':available,'shortage_by_level':shortage,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':prep['capability_exceptions'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'discovery-after.json',path/'generated.json',HERE/'freeze.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md')],'note':'Validated integrating-factor IVP generator reused with current source replay. Easy authored; moderate/hard anchored to observed demands. Incomplete and ambiguous/redundant source banks remain untouched and excluded from validated inventory. Source questions, canonical example and learner history preserved.'}
    save(path/'outcome.json',result)
    save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)

def assert_current_sources(kp,path,basis):
    current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert set(current)==set(g.QUESTIONS)
    details=[]
    for sid,original in g.QUESTIONS.items():
        q=current[sid]
        assert source_projection(q,original)==original,sid+' source evidence changed'
        level,_,parameters,_,_=g.OBS[sid]
        rec=g.generate(level,template=sid,parameters=parameters,profile='observed')
        v.check_record(rec,rec['generation']['source_ambiguous_bank'])
        n=0
        for rawfield in q[':question/answer-fields']:
            f=next(f for f in rec['question'][':question/answer-fields'] if f[':answer-field/key']==rawfield[':answer-field/key'])
            originals=[v.parse(a[':answer/value']) for a in rawfield[':answer-field/choices']]
            remaining=[v.parse(a[':answer/value']) for a in f[':answer-field/choices']]
            for value in originals:
                match=next(i for i,z in enumerate(remaining) if v.equal(value,z));remaining.pop(match);n+=1
            assert not remaining
            if ':answer-field/correct' in rawfield:
                correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
                assert v.equal(v.parse(rawfield[':answer-field/correct'][':answer/value']),v.parse(correct[':answer/value']))
        details.append({'source_id':sid,'complete_banks_replayed':2,'choices_matched':n,'source_evidence_unchanged':True,'evidence_only':rec['generation']['source_ambiguous_bank'] or sid=='q-334916'})
    assert source_projection(kp[':knowledge-point/canonical-example'],g.CURRENT['record'][':knowledge-point/canonical-example'])==g.CURRENT['record'][':knowledge-point/canonical-example']
    save(path/'current-source-validation.json',{'passed':True,'basis':basis,'historical_basis':1356,'current_source_basis':g.CURRENT['basis'],'source_questions':len(current),'complete_banks':2*len(details),'values_matched':sum(x['choices_matched'] for x in details),'details':details})

def main():
    frozen=json.loads((HERE/'freeze.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in frozen['files'].items()),'Frozen generator changed'
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='passed_with_documented_source_anomalies' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    assert validation['source_fidelity']['complete_banks']==2*len(g.OBS)==18
    assert validation['native_grading']['documented_unresolved_checks']==0
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        # Reconcile exact durable requests before calculating new intent.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report)
                inv=inventory(path/'inventory-after.json');b,_=counts(path/'discovery-after.json');assert inv['basis']==b
                available=validated_counts(read_kp(path/'available-readback',b),path/'available-readback',b)
                finish(path,intent['generator_id'],verified,inv,available)
                return
        inv=inventory(OUT/'inventory-before.json')
        b,scheduler_available=counts(OUT/'discovery-before.json')
        assert DB.basis()==inv['basis']==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.SOURCE['record'][':knowledge-point/id']
        assert_current_sources(kp,path,b)
        available=validated_counts(kp,path,b)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b)
        assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.SOURCE['record'][':knowledge-point/id']),'question-generator'))
        if gen:assert gen.get(':question-generator/script',SCRIPT)==SCRIPT
        needed={l:max(0,5-available[l]) for l in LEVELS}
        selected={l:0 for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];local=[];attempts={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        def select(rec):
            check(rec)
            level=rec['question'][':question/difficulty'].split('/')[-1]
            fp=fingerprint(rec['question'])
            if selected[level]<needed[level] and fp not in used:
                rec=copy.deepcopy(rec);rec['generation']['inventory_fingerprint']=fp
                records.append(rec);used.add(fp);selected[level]+=1
        for rec in instances:select(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        # Bound search explicitly. Failed searches retain the shortage, not aliases.
        for level in LEVELS:
            for i in range(1000):
                if selected[level]>=needed[level] and len([r for r in local if r['question'][':question/difficulty'].endswith('/'+level)])>=2:break
                template=FAMILIES[level][i%len(FAMILIES[level])]
                rec=c.generate(level,seed=int(JOB.name[:8],16)+i,template=template)
                attempts[level]+=1
                if len([r for r in local if r['question'][':question/difficulty'].endswith('/'+level)])<2:
                    check(rec);local.append(rec)
                select(rec)
        exceptions=[]
        for level in LEVELS:
            if selected[level]<needed[level]:exceptions.append({'level':level,'missing':needed[level]-selected[level],'attempt_limit':1000,'evidence':'Bounded deterministic sampler exhausted without enough distinct validated tasks. No finite total is inferred.'})
        for attribute,ids in (('question/id',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[ids],path,attribute.replace('/','-')+'-collisions',b),'Generated identity exists; reconcile'
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or (len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        save(path/'generated.json',records);save(path/'local-preview.json',local)
        (path/'review.md').write_text('# Replenishment question review\n\n'+'\n\n---\n\n'.join(c.markdown(r) for r in records)+'\n')
        save(path/'native-input.json',[native(rec) for rec in local+instances+records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        report=json.loads((path/'native-report.json').read_text())
        assert report['documented_unresolved_checks']==0
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_by_level':available,'missing_by_level':needed,'selected_by_level':selected,'sampling_attempts':attempts,'capability_exceptions':exceptions,'local_previews':len(local),'new_questions':len(records),'source_evidence_unchanged':True,'assets':[],'difficulty_evidence':'Easy unit-coefficient IVPs authored; moderate/hard anchored to labeled source templates and canonical cubic example; bounded scope documented in classification.md','distinctness':'Normalized ODE P,Q and initial t,h read from actual printed prompts. Banks, seeds, IDs and choice order excluded. Current practice and canonical tasks excluded.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'by_level':{l:0 for l in LEVELS}}
            save(path/'verification.json',{'passed':True,'no_change':True,**verified})
            finish(path,gid,verified,inv,available)
            return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:
            stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0])
        # Recheck current counts while still serialized, before saving/submitting.
        b2,scheduler2=counts(path/'discovery-precommit.json')
        assert b2==b and scheduler2==scheduler_available and DB.basis()==b
        assert validated_counts(read_kp(path/'precommit',b),path/'precommit',b)==available
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'ode-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        verified=verify(path,intent,report)
        inv=inventory(path/'inventory-after.json');after,_=counts(path/'discovery-after.json')
        available=validated_counts(read_kp(path/'available-readback',after),path/'available-readback',after)
        assert after==inv['basis']==verified['basis_after']
        finish(path,gid,verified,inv,available)

if __name__=='__main__':main()
