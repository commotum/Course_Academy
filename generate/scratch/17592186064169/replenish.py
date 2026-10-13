"""Additive inventory repair for reciprocal antiderivatives using existing EDB transport."""
import ast, copy, fcntl, hashlib, importlib.util, json, os, random, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
# Load only the validator's imports and definitions; its exhaustive runner is
# executed separately and freezes the evidence before this worker begins.
v = SimpleNamespace()
v.__dict__['__file__'] = str(HERE/'validate.py')
source = (HERE/'validate.py').read_text()
exec(compile(source.split('\nsource=json.loads',1)[0], str(HERE/'validate.py'), 'exec'), v.__dict__)
g = v.g
KP = g.KP_ID
LEVELS = ('easy','moderate','hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.PROVENANCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
GENERATOR_ID = g.ident('question-generator')
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'11ab16eef991b4dcc96dda3397da92bfa7eab2aeb327270625111860a9a2deef'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True,exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT'],postgres_url=ENV['EDB_POSTGRES_URL']))
NATIVE = build_learning(ROOT.parent/'EDB')
QUERY = (OUT/'kp-query.edn').read_text()


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

def canonical(value):
    if isinstance(value, dict):
        if ':db/ident' in value and set(value) <= {':db/id', ':db/ident'}:
            return str(value[':db/ident'])
        return {str(k):canonical(x) for k,x in value.items()
                if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    return str(value) if isinstance(value,uuid.UUID) else value

def fingerprint(q):
    if q.get(':question/math-academy-id') == 'e-368':
        captured=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/canonical-example']
        assert q[':question/problem'] == captured[':question/problem']
        return '-3'  # The captured canonical integrand is exactly 1/x^3.
    f=v.printed_integrand(q[':question/problem'])
    n=f.as_powers_dict().get(v.X)
    assert n is not None and v.sp.simplify(f-v.X**n)==0
    return str(n)

def validate_instance(rec):
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    v.verify(rec)
    m=rec['generation']
    expected=g.generate(m['level'],m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
    assert ordered(rec['question']) == ordered(expected['question']), 'Generated identity/content drift'
    assert m['mathematical_fingerprint'] == expected['generation']['mathematical_fingerprint']

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def available_counts(path,kp,basis,known):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    accepted={level:[] for level in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable: reason='Shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'): reason='Canonical example'
        elif level not in accepted: reason='Unrated or unsupported difficulty'
        elif not q.get(':question/worked-solution') or not q.get(':question/answer-fields'): reason='Missing worked solution or fields'
        elif not all(f.get(':answer-field/correct') for f in q[':question/answer-fields']): reason='Missing correct designation'
        else:
            rec=known.get(str(q[':question/id']))
            if rec is None or normalize(q)!=ordered(rec['question']):
                reason='No validated generated content match'
        if reason: excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
        else: accepted[level].append(q)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in rows}),
             'question_ids':[str(q[':question/id']) for q in rows]} for level,rows in accepted.items()},
             'excluded_questions':excluded,'shown_or_reserved':sorted(unavailable)}
    save(path/'available-counts.json',result)
    return result

def verify(path,intent,report,known):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b)
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')} == {k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question'])
        assert fingerprint(q)==fingerprint(rec['question'])
        validate_instance(rec)
    assert not transaction([],kp,intent['generator_id'])
    counts=available_counts(path/'readback',kp,b,known)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),
            'by_level':{level:sum(r['generation']['level']==level for r in records) for level in LEVELS},
            'unchanged_source_questions':len(old),'unchanged_canonical_example':True,
            'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,
            'generator_registration_verified':True,'repeat_preparation_content_changes':0,
            'available_counts_after':counts}
    save(path/'verification.json',result)
    return result

def finish(path,gid,verified,inv):
    counts=verified['available_counts_after']
    remaining={level:max(0,5-counts['levels'][level]['distinct_available_tasks']) for level in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,
            'topic':17592186049481,'generator_path':SCRIPT,'generator_id':gid,'database':'math','lineage':LINEAGE,
            'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],
            'new_questions':verified['new_questions'],'new_by_level':verified['by_level'],
            'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,
            'available_after':counts,'shortage_remaining':remaining,
            'bounded_capabilities':json.loads((HERE/'capabilities.json').read_text()),
            'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
            'source_questions_and_learner_history_preserved':True,
            'note':'Legacy unclassified source questions retained. Hard higher-root level is explicitly authored and validated; no original hard rating is claimed.',
            'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',
                       path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',
                       path/'transaction.edn',path/'native-report.json',HERE/'validation.json',
                       HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json') if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_by_level','shortage_remaining','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    frozen=json.loads((HERE/'hashes.json').read_text())['sha256']
    assert all(sha(ROOT/name)==digest for name,digest in frozen.items())
    assert validation['native']['documented_unresolved_checks']==0
    inventory(OUT/'inventory-pre-generation.json')
    # Execute the existing deterministic generator over its documented domains.
    catalog=[]
    for t,config in g.TEMPLATES.items():
        for i,p in enumerate(g.domain(config['level'],t)):
            catalog.append(g.generate(config['level'],seed=i,template=t,parameters=p))
    known={r['question'][':question/id']:r for r in catalog}
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    lockpath=Path(ENV['LEARNING_REQUEST_DIR'])/'api.lock'
    assert lockpath==ROOT/'.local/learning/requests/math/api.lock'
    with lockpath.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application lock acquired; checking current inventory',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                assert LINEAGE in DB.command('status')
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report,known)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'))
                return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis']
        assert DB.basis()==b and LINEAGE in DB.command('status')
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'source.json').read_text())['record']
        expected={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(expected)<=set(current)
        for mid,q in expected.items(): assert canonical(current[mid])==canonical(q),'Source changed; reclassify '+mid
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        sources=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b)
        assert len(sources)==1
        gen=kp.get(':knowledge-point/question-generator')
        registry=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-identity',b)
        assert len(registry)<=1
        gid=str(gen[':question-generator/id']) if gen else str(registry[0][0][':question-generator/id']) if registry else GENERATOR_ID
        if gen: assert gen[':question-generator/script']==SCRIPT
        if registry: assert str(registry[0][0][':question-generator/id'])==gid
        counts=available_counts(path,kp,b,known)
        jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
        needed={level:max(0,5-counts['levels'][level]['distinct_available_tasks'],jobs.get(level,{}).get('missing',0)) for level in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict): instances=[instances]
        eligible=[];rejected=[]
        for rec in instances:
            try: validate_instance(rec)
            except (AssertionError,ValueError,KeyError,TypeError) as error:
                rejected.append({'question_id':rec.get('question',{}).get(':question/id'),'reason':str(error)})
            else: eligible.append(rec);known[rec['question'][':question/id']]=rec
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated':len(eligible),'rejected':rejected,'generator_error':supplied.get('generatorError')})
        rng=random.Random(int(JOB.name[:8],16));rng.shuffle(catalog)
        records=[];added={level:0 for level in LEVELS}
        for level in LEVELS:
            for rec in eligible+catalog:
                if rec['generation']['level']!=level or added[level]>=needed[level]: continue
                # Preserve the normal rated easy prompt rather than rotating layout.
                if level=='easy' and rec['generation']['template']!='negative_named': continue
                fp=fingerprint(rec['question'])
                if fp in used: continue
                validate_instance(rec);records.append(rec);used.add(fp);added[level]+=1
        save(path/'generated.json',records)
        save(path/'review.json',records)
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        for attr,values in (('question/id',[r['question'][':question/id'] for r in records]),
                            ('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),
                            ('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if values:
                rows=DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in values]],path/'identity-check',attr.replace('/','-'),b)
                assert not rows,'Stable identity collision; reconcile'
        native=[]
        for r in records:
            f=r['question'][':question/answer-fields'][0]
            native.append({'label':r['question'][':question/id'],'record':r,'checks':[
                {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independently differentiated displayed bank'} for a in f[':answer-field/choices']]})
        save(path/'native-input.json',native)
        if native:
            subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
            nr=json.loads((path/'native-report.json').read_text());assert nr['documented_unresolved_checks']==0
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,
             'available_counts':counts,'missing_by_level':needed,'new_by_level':added,
             'distinct_new_integrands':len({fingerprint(r['question']) for r in records}),
             'asset_hashes':[],'source_evidence_unchanged':True,'finite_remaining':{l:max(0,needed[l]-added[l]) for l in LEVELS}})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'by_level':added,'available_counts_after':counts,'no_changes':True}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f: f.write(tx);f.flush();os.fsync(f.fileno())
        pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(pr.stdout);report=loads(pr.stdout)
        assert report[':edb/committed'] is False and report[':edb/db-before-t']==b
        check_report(report,path/'preview-check',sources[0][0])
        assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,
                'source_eid':sources[0][0],'basis':b,'expected_basis':b,
                'request_key':'reciprocal-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),
                'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,
                'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),
                'question_uuids':[r['question'][':question/id'] for r in records],
                'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),
                'lock':str(lockpath),'lock_held_through_submission_and_readback':True}
        save(path/'commit-intent.json',intent)
        print('Validated preview at basis '+str(b)+'; submitting '+str(len(records))+' distinct questions',flush=True)
        report=DB._commit(intent,txpath,path)
        verified=verify(path,intent,report,known)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__': main()
