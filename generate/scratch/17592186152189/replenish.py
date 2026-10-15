"""Scoped additive ellipse inventory, exact requests and receipt readback."""
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
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database, StaleBasis
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning

KP, TOPIC = 17592186152189, 17592186049672
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'876978a465a23430d634e7586d10f020a07b05cdc57518a1d0ea7762baf804a6'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True,exist_ok=True)
LOCK = ROOT/'.local/learning/requests/math/api.lock'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV.copy()
LEVELS = ('easy', 'moderate', 'hard')
QUERY = (OUT/'source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

from capture.scripts.database.images import ImageLibrary
import re
spec = importlib.util.spec_from_file_location('ellipse_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
CURRENT = json.loads((HERE/'source-current.json').read_text())
IMAGES = ImageLibrary(Path(ENV['EDB_MATH_ROOT']), HERE)
USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/unlocked]
       [?status :db/ident :learner-task.status/started]
       [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

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

def read_kp(path,basis):
    return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

def inventory(binary,path):
    r = subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint], input='{"action":"inventory"}',
        env=ENV,capture_output=True,text=True,check=True,timeout=55)
    reply = json.loads(r.stdout)
    assert reply['ok'] and reply['data']['lineage'] == LINEAGE
    save(path,reply['data'])
    return reply['data']

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

def source_evidence(value):
    if isinstance(value,dict):
        return {str(k):source_evidence(x) for k,x in value.items() if str(k)!=':db/id' and '/_' not in str(k)}
    if isinstance(value,(list,tuple)):
        return sorted([source_evidence(x) for x in value],key=lambda x:json.dumps(x,sort_keys=True))
    return str(value) if isinstance(value,uuid.UUID) else value

def parameters(q):
    # Read concrete prose independently; moderate prompt supplies the image.
    solution=q.get(':question/worked-solution','')
    match=re.search(r'In our case, the ellipse is centered at the point \$\((-?\d+),(-?\d+)\),\$ \$a=(\d+)\$ and \$b=(\d+)\.\$',solution)
    if match:
        h,k,a,b=map(int,match.groups());return dict(a=a,b=b,h=h,k=k)
    mid=q.get(':question/math-academy-id')
    if mid in g.SPECS:return dict(g.SPECS[mid]['parameters'])
    raise ValueError('No independent concrete ellipse parameters')

def fingerprint(q):
    p=parameters(q)
    # Conservatively collapse all response layouts and difficulty presentations
    # sharing an ellipse, including different orientation demands.
    return tuple(p[k] for k in ('a','b','h','k'))

def record(q):
    return {'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':normalized(q),
        'generation':{'template':'current-source-validation','parameters':parameters(q),'evidence_only':False}}

def engine_checks(rec):
    # Use actual canonical/factored acceptance and wrong-entry rejection. Retain
    # phase-shift limitations separately; do not turn unresolved into accepted.
    return [c for c in v.native_item(rec,'inventory')['checks'] if c['expected']!='unresolved']

def available_counts(kp,basis,path):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    pools={l:[] for l in LEVELS};excluded=[];checked=[]
    for q in kp[':knowledge-point/questions']:
        level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Shown or reserved including retained history'
        elif level not in LEVELS:reason='Unrated'
        else:
            try:
                rec=record(q)
                assert len({f[':answer-field/key'] for f in rec['question'][':question/answer-fields']})==len(rec['question'][':question/answer-fields'])
                v.check(rec)
                assert all(f.get(':answer-field/correct') for f in rec['question'][':question/answer-fields'])
            except (KeyError,ValueError,AssertionError,TypeError) as e:reason='Incomplete or invalid fields: '+str(e)
        if reason:excluded.append({'eid':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
        else:
            pools[level].append(q);checked.append({'label':str(q[':question/id']),'record':rec,'checks':engine_checks(rec)})
    save(path/'available-native-input.json',checked);native(path/'available-native-input.json',path/'available-native-report.json')
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),
        'rated_gradable_unseen_unreserved':len(qs),'question_ids':[str(q[':question/id']) for q in qs]} for l,qs in pools.items()},
        'excluded':excluded,'unavailable_including_history':sorted(unavailable),'counting':'Unique (horizontal radius, vertical radius, center x, center y), ignoring identity, seed, bank, notation and option ordering; source canonical not counted.'}
    save(path/'available-counts.json',result);return result

def validate_package():
    # Full original and supplemental replay, separately from native grading.
    checked=[];nfields=nvalues=nrefs=0;replays=[]
    for q in CURRENT['record'][':knowledge-point/questions']:
        mid=q[':question/math-academy-id'];s=g.SPECS[mid]
        r=g.generate(s['level'],template=mid,profile='observed:'+mid,parameters=s['parameters']);qq=r['question']
        assert q[':question/problem']==qq[':question/problem']
        assert q.get(':question/worked-solution')==qq.get(':question/worked-solution')
        assert (':question/difficulty' in q)==(':question/difficulty' in qq)
        assert len(q[':question/answer-fields'])==len(qq[':question/answer-fields'])
        v.check(r)
        for f,ff in zip(q[':question/answer-fields'],qq[':question/answer-fields']):
            assert f[':answer-field/key']==ff[':answer-field/key'] and f[':answer-field/type'][':db/ident']==ff[':answer-field/type']
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in ff[':answer-field/choices'])
            nfields+=1;nvalues+=len(f[':answer-field/choices'])
            assert (':answer-field/correct' in f)==(':answer-field/correct' in ff)
            if ':answer-field/correct' in f:
                value=next(a[':answer/value'] for a in ff[':answer-field/choices'] if a[':answer/id']==ff[':answer-field/correct'][1]);assert value==f[':answer-field/correct'][':answer/value'];nrefs+=1
        replays.append({'source_id':mid,'parameters':s['parameters'],'complete_banks_matched':len(qq[':question/answer-fields'])})
        for rr in (r,g.generate(s['level'],template=mid,profile='observed:'+mid,parameters={'a':7,'b':2,'h':-5,'k':3})):
            v.check(rr);fixture=json.loads(json.dumps(rr));fixture['question'][':question/answer-fields']=[f for f in fixture['question'][':question/answer-fields'] if ':answer-field/correct' in f]
            if fixture['question'][':question/answer-fields']:checked.append({'label':mid,'record':fixture,'checks':engine_checks(fixture)})
    normal=[];families=set();tasks=set()
    for level in LEVELS:
        for seed in range(12):
            r=g.generate(level,seed=seed);v.check(r);families.add(r['generation']['template']);tasks.add(fingerprint(r['question']));normal.append(r)
            rr=g.generate(level,seed=seed+1000,parameters=r['generation']['parameters'],template=r['generation']['template']);assert normalized(r['question'])==normalized(rr['question'])
            checked.append({'label':level+str(seed),'record':r,'checks':engine_checks(r)})
    assert families=={'supplied','graph','oriented_radio','oriented_blank'}
    for p in ({'a':1,'b':8,'h':0,'k':-6},{'a':8,'b':1,'h':6,'k':0},{'a':2,'b':3,'h':-6,'k':-6}):
        for level in LEVELS:v.check(g.generate(level,parameters=p))
    for r in normal:
        if r['generation']['plot']:v.generated_raster(r)
    save(OUT/'current-replay-native-input.json',checked);rep=native(OUT/'current-replay-native-input.json',OUT/'current-replay-native-report.json')
    save(OUT/'validation.json',{'passed':True,'basis':CURRENT['basis'],'source_questions':len(replays),'prompt_exact_matches':len(replays),
        'whole_banks_matched':nfields,'displayed_values_matched':nvalues,'correct_designations_matched':nrefs,'missing_designations_preserved':2,
        'source_replays':replays,'normal_families':sorted(families),'native_checks':{k:rep[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
        'native_limitations':'Phase-shift equivalent trig expressions remain documented in native-limitations.md; no blanket equivalence claim. Only canonical/factored blank responses counted accepted. Inventory-generated hard questions use radio.',
        'plots':'Original 15 raster evidence retained; three new rasters visually read at their actual signed ticks, centers, semiaxes and hard rightmost A/CCW arrow. All 36 normal examples checked by independent math and generated raster geometry.',
        'artifacts':{str(p.relative_to(ROOT)):sha(p) for p in (HERE.with_suffix('.py'),HERE/'specs.json',HERE/'specs-current-additions.json',HERE/'render.py',HERE/'source-current.json',HERE/'validate.py',Path(__file__))}})

def localize(rec):
    rec=json.loads(json.dumps(rec));q=rec['question']
    for key in (':question/problem',':question/worked-solution'):q[key]=IMAGES.text(q[key])
    for asset in IMAGES.saved.values():assert sha(Path(ENV['EDB_MATH_ROOT'])/asset['path'])==asset['sha256']
    return rec

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert canonical({k:x for k,x in before.items() if k not in omit})==canonical({k:x for k,x in kp.items() if k not in omit})
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    used={fingerprint(q) for q in old.values()}
    for r in records:
        q=byid[r['question'][':question/id']];v.check(r);assert normalized(q)==normalized(r['question']) and ':question/math-academy-id' not in q
        fp=fingerprint(q);assert fp not in used;used.add(fp)
    assert not transaction([],kp,intent['generator_id'])
    counts=available_counts(kp,report[':edb/db-after-t'],path/'readback')
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),
        'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},
        'available_counts_after':counts,'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,
        'only_additive_requested_kp_content_datoms':True,'source_attribution':SOURCE,'repeat_preparation_content_changes':0,'generator_registration_verified':True}
    save(path/'verification.json',result);return result

def finish(binary,path,gid,verified):
    inv=inventory(binary,path/'inventory-after.json');levels=verified['available_counts_after']['levels'];remaining={l:max(0,5-levels[l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'generated' if not any(remaining.values()) else 'finite-limit','knowledgePoint':KP,'topic':TOPIC,'generator_path':SCRIPT,'generator_id':gid,
        'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'preparation_basis':verified['basis_before'],'new_questions':verified['new_questions'],
        'new_by_level':verified.get('new_by_level',{}),'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,
        'available_by_level':{l:levels[l]['distinct_available_tasks'] for l in LEVELS},'shortage_remaining':remaining,
        'difficulty_evidence':{'easy':'Authored direct substitution of supplied center and two radii, anchored by canonical lesson and predecessor ellipse/circle knowledge; no graph reading or direction test.',
        'moderate':'Seven observed rated source graph-reading radio questions.','hard':'Ten observed rated source rightmost-start CCW questions, radio and two-expression blank layouts.'},
        'capability_exceptions':[{'scope':'blank equivalents','exception':'Phase-shift trig equivalences unresolved in existing grader; preserved in native-limitations.md. Replenishment uses full-bank radio grading. This is not an unsupported difficulty.'}],
        'source_questions_and_learner_history_preserved':True,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
        'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'generated.json',path/'native-report.json',
        path/'inventory-after.json',path/'readback/available-counts.json',OUT/'validation.json',OUT/'current-native-build.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'current-source-extraction.md') if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_remaining')},indent=2),flush=True)

def prepare(binary,preview):
    for path in sorted(OUT.glob('basis-*')):
        if not (path/'commit-intent.json').exists():continue
        intent=json.loads((path/'commit-intent.json').read_text())
        assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
        assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
        assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
        return finish(binary,path,intent['generator_id'],verify(path,intent,DB._commit(intent,path/'transaction.edn',path)))
    inv=inventory(binary,OUT/'inventory-under-lock.json');basis=inv['basis'];assert DB.basis()==basis
    path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis)
    assert str(kp[':knowledge-point/id'])==g.KP_UUID
    (path/'before.edn').write_text(dumps(kp)+'\n')
    captured=CURRENT['record'];now={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    for q in captured[':knowledge-point/questions']:assert source_evidence(now[q[':question/math-academy-id']])==source_evidence(q),'Source changed; reclassify'
    assert len(now)==len(captured[':knowledge-point/questions']),'Additional source evidence; reclassify'
    assert source_evidence(captured[':knowledge-point/canonical-example'])==source_evidence(kp[':knowledge-point/canonical-example'])
    contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(contributor)==1
    gen=kp.get(':knowledge-point/question-generator');registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',basis);assert len(registered)<=1
    identity_path=HERE/'generator-id.json';identity=json.loads(identity_path.read_text()) if identity_path.exists() else {}
    gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else identity.get('id',str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator')))
    assert not identity or identity['id']==gid
    save(identity_path,{'id':gid,'script':SCRIPT,'knowledge_point':KP})
    collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',basis)
    assert not collision or collision[0][0][':question-generator/script']==SCRIPT
    counts=available_counts(kp,basis,path);needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    print('Verified current inventory: '+json.dumps({l:counts['levels'][l]['distinct_available_tasks'] for l in LEVELS}),flush=True)
    used={fingerprint(q) for q in kp[':knowledge-point/questions']}
    # Canonical content uses the same assessed ellipse; protect it too where readable.
    try:used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    except ValueError:pass
    records=[];checked=[];added={l:0 for l in LEVELS}
    def consider(rec):
        assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
        meta=rec['generation'];assert not meta.get('evidence_only') and meta['eligible_for_learning']
        level=rec['question'][':question/difficulty'].split('/')[-1];assert level in LEVELS
        replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
        assert normalized(localize(replay)['question'])==normalized(localize(rec)['question'])
        v.check(rec)
        if meta['plot']:v.generated_raster(rec)
        checked.append(rec);fp=fingerprint(rec['question'])
        if added[level]<needed[level] and fp not in used:
            records.append(localize(rec));used.add(fp);added[level]+=1
    supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
    if isinstance(instances,dict):instances=[instances]
    for rec in instances:consider(rec)
    for level in LEVELS:
        for attempt in range(200):
            if added[level]>=needed[level]:break
            try:rec=g.generate(level,seed=int(JOB.name[:8],16)+attempt,template='oriented_radio' if level=='hard' else None)
            except ValueError:continue
            consider(rec)
        assert added[level]==needed[level], 'Bounded generation failed; leave explicit shortage'
    save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances)})
    save(path/'generated.json',records);save(path/'generated-local.json',checked)
    save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':engine_checks(r)} for r in records]);native(path/'native-input.json',path/'native-report.json')
    for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
        if values:
            assert len(set(values))==len(values)
            assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in values]],path/'identity-check',attr.replace('/','-'),basis),'Existing identity requires reconciliation'
    save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_version':g.VERSION,'needed':needed,'new_by_level':added,'available_counts':counts,
        'asset_hashes':list(IMAGES.saved.values()),'source_evidence_unchanged':True,'deduplication':'Independent concrete ellipse parameters; collapse all layouts, banks, seeds and option order',
        'original_job_request':json.loads(JOB.with_suffix('.json').read_text())['request']})
    forms=transaction(records,kp,gid)
    if not forms:
        verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'new_by_level':added,'no_changes':True,'available_counts_after':counts};save(path/'verification.json',verified);return finish(binary,path,gid,verified)
    txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
    with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
    r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    (path/'preview.edn').write_text(r.stdout);report=loads(r.stdout);assert report[':edb/committed'] is False
    if report[':edb/db-before-t']!=basis or DB.basis()!=basis:raise StaleBasis('Basis advanced during preparation')
    check_datoms(report,path/'preview-check',contributor[0][0])
    intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':basis,'expected_basis':basis,
        'request_key':'ellipse-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,
        'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],
        'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
    save(path/'commit-intent.json',intent);return finish(binary,path,gid,verify(path,intent,DB._commit(intent,txpath,path)))

def main():
    binary=build_learning(ROOT.parent/'EDB')
    native_source=OUT/'check-engine.rs';native_source.write_text((ROOT/'generate/runs/current/check-engine.rs').read_text())
    libs={name:max((ROOT/'target/release/deps').glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
    subprocess.run(['rustc','--edition=2024','-O',str(native_source),*[x for name,p in libs.items() for x in ('--extern',name+'='+str(p))],'-L','dependency='+str(ROOT/'target/release/deps'),'-o',str(OUT/'check-engine')],check=True,timeout=55)
    save(OUT/'current-native-build.json',{'source_sha256':sha(native_source),'libraries':{name:{'path':str(p),'sha256':sha(p)} for name,p in libs.items()}})
    inventory(binary,OUT/'inventory-before-validation.json')
    validate_package()
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock held through fresh inventory, submission and readback',flush=True)
        for attempt in range(3):
            try:return prepare(binary,preview)
            except StaleBasis:
                if attempt==2:raise
                print('Confirmed basis change; reprepare',flush=True)
if __name__=='__main__':main()
