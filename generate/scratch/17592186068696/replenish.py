"""Additive, basis-guarded replenishment for KP68696 only.

Retains historical generator evidence and validates the current checkbox migration
separately. Does not replace a source question or write any learner facts.
"""
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
sys.path[:0] = [str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('kp_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'67eb1bac6fea38c2355c8ded7ef7b9d1b95598caed58d55a62ad72d0fe201e29'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY = (OUT/'source-query.edn').read_text()
USAGE = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
LEVELS = ('easy', 'moderate', 'hard')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def canonical(x):
    if isinstance(x, dict):
        return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x, (tuple,list)):
        return sorted([canonical(z) for z in x], key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def inventory(p):
    r = subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=55)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(p,x['data'])
    return x['data']

def read_kp(path,basis):
    return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

def normalize(q):
    out = {k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    out[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    out[':question/answer-fields'] = []
    for f in sorted(q.get(':question/answer-fields',[]),key=lambda f:f[':answer-field/key']):
        out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    return out

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def shape(q):
    """Compare every displayed value/key while ignoring generated identity."""
    q=copy.deepcopy(q);q.pop(':question/id',None)
    for f in q[':question/answer-fields']:
        f.pop(':answer-field/id',None)
        correct=f[':answer-field/correct'][1]
        f[':answer-field/correct']=next({k:z for k,z in a.items() if k!=':answer/id'} for a in f[':answer-field/choices'] if a[':answer/id']==correct)
        for a in f[':answer-field/choices']:a.pop(':answer/id',None)
    return canonical(q)

def source_fingerprint(mid):
    family = g.infer_family(mid)
    target = [str(g.sp.Rational(x)) for x in g.BREAKS.get(mid,[g.SELECT.get(mid,0)])]
    return g.digest({'criterion':'graph-selection' if family=='select_graph' else 'coordinate-set','target':target,'scale_reading':1,'break_count':len(target)})

def grade(records,path):
    path.mkdir(parents=True,exist_ok=True)
    save(path/'input.json',[v.grade_checks(r,str(i)) for i,r in enumerate(records)])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'input.json'),str(path/'report.json')],check=True)
    report=json.loads((path/'report.json').read_text())
    assert report['documented_unresolved_checks']==0

def current_sources(kp,path,basis):
    """Full current source-bank replay and independent graphical checkbox keys."""
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    rows=[]; native=[]; available={l:set() for l in LEVELS}; used=set()
    initial=loads((OUT/'initial.edn').read_text())[0][0]
    expected={q[':db/id']:q for q in initial[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in expected.items()), 'Source changed; reclassify'
    assert canonical(kp[':knowledge-point/canonical-example'])==canonical(initial[':knowledge-point/canonical-example'])
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id')
        if mid not in g.QUESTIONS:
            raise AssertionError('Unexpected new practice question; reclassify before generating')
        old=g.QUESTIONS[mid]
        assert q[':question/worked-solution']==old[':question/worked-solution']
        assert str(q[':question/difficulty'][':db/ident'])==':question.difficulty/easy'
        fields=q.get(':question/answer-fields',[])
        checkbox=bool(fields) and all(str(f[':answer-field/type'][':db/ident'])==':answer-field.type/checkbox' for f in fields)
        fp=source_fingerprint(mid);used.add(fp)
        valid=False;status='preserved missing plotted widget or field; excluded'
        if checkbox:
            prefix=q[':question/problem'].split('\n\nSelect all that apply.')[0]
            assert prefix==old[':question/problem']
            plots=re.findall(r'!\[\]\(([^)]+)\)',prefix);assert len(plots)==1
            breaks=v.graph_readback(plots[0]);assert breaks==frozenset(map(g.sp.Rational,g.BREAKS[mid]))
            options=dict(re.findall(r'- \*\*([IVX]+)\.\*\* \$x=(-?\d+)\$',q[':question/problem']))
            assert set(options)=={f[':answer-field/key'] for f in fields}
            for f in fields:
                assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'true','false'}
                assert f[':answer-field/correct'][':answer/value']==str(g.sp.Rational(options[f[':answer-field/key']]) in breaks).lower()
            valid=True;status='current checkbox bank: full field/Boolean replay and graph-derived truth'
        elif g.infer_family(mid)=='select_graph':
            replay=g.generate('easy',profile='observed:'+mid,parameters={'scale':1,'shift':0})
            assert shape(normalize(q))==shape(ordered(replay['question']))
            v.validate_record(replay)
            valid=True;status='unchanged five-image radio bank: full replay and graph-derived key'
        elif fields:
            # Missing captured graph is intentionally excluded even when gradeable.
            replay=g.generate('easy',profile='observed:'+mid,parameters={'scale':1,'shift':0})
            assert shape(normalize(q))==shape(ordered(replay['question']))
        row={'source_id':q[':db/id'],'math_academy_id':mid,'difficulty':'easy','profile':('current-checkbox:' if checkbox else 'observed:')+mid,'field_types':[str(f[':answer-field/type'][':db/ident']) for f in fields], 'complete_field_banks':len(fields),'displayed_answer_values':sum(len(f[':answer-field/choices']) for f in fields),'plot_rating':'heavy','validation':status,'eligible':valid,'fingerprint':fp}
        rows.append(row)
        if fields:
            native.append({'knowledge_point':{'title':g.TITLE},'question':normalize(q),'generation':{'template':row['profile']}})
        if valid and q[':db/id'] not in shown|reserved:
            available['easy'].add(fp)
    grade(native,path/'source-grading')
    evidence={'basis':basis,'lineage':LINEAGE,'source_questions':rows,'distinct_available':{l:len(available[l]) for l in LEVELS},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'canonical_example_excluded':True,'all_source_questions_preserved':True,'checkbox_records':sum(r['profile'].startswith('current-checkbox:') for r in rows),'historical_generator_source_basis':1356,'historical_bank_fidelity':'retained; current checkbox banks assessed separately, no radio migration reversal'}
    save(path/'current-classification.json',evidence)
    return evidence,used

def transaction(records,kp,gid):
    forms=[]
    for rec in records:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    if kp.get(':knowledge-point/question-generator'):
        reg=kp[':knowledge-point/question-generator']
        assert str(reg[':question-generator/id'])==gid and reg[':question-generator/script']==SCRIPT
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:
        forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert added and s==source,'Unexpected retraction or attribution'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    assert canonical({k:z for k,z in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:z for k,z in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    assets=json.loads((path/'assets.json').read_text())
    for asset in assets:assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question'])
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'new_questions_by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'source_questions_unchanged':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'only_scoped_additive_content_datoms':True,'contributor_verified':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    stock=json.loads((path/'current-classification.json').read_text())['distinct_available']
    result['verified_available_by_level']={l:stock[l]+result['new_questions_by_level'][l] for l in LEVELS}
    result['shortage_by_level']={l:max(0,5-result['verified_available_by_level'][l]) for l in LEVELS}
    assert not any(result['shortage_by_level'].values())
    save(path/'verification.json',result)
    return result

def finish(path,gid,verified):
    inv=inventory(path/'inventory-after.json')
    jobs=[j for j in inv['jobs'] if j['knowledgePoint']==KP]
    result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'inventory_recheck_basis':inv['basis'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['new_questions_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'remaining_jobs':jobs,'capability_exceptions':[],'finite_catalog_tasks':json.loads((HERE/'validation.json').read_text())['finite_authorable_coordinate_tasks'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'current-classification.json',path/'generated.json',path/'native-grading/report.json',path/'inventory-after.json',HERE/'validation.json',HERE/'capabilities.json')],'note':'Easy source inventory was validated independently, including seven migrated checkbox records. Added genuinely new authored moderate/hard graph-reading tasks with distinct coordinate sets. Current source questions and learner history are unchanged.'}
    result['available_by_level']=verified['verified_available_by_level']
    result['shortage_by_level']=verified['shortage_by_level']
    assert inv['basis']==verified['basis_after'], 'Fresh inventory advanced; recount before claiming stock'
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','new_questions_by_level','verified_commit_basis','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
    parent=json.loads((ROOT/'generate/runs/current/qa/17592186068696.json').read_text())
    assert parent['parent_review']=='passed' and parent['generator_sha256']==sha(HERE.with_suffix('.py'))
    assert validation['native']['documented_unresolved_checks']==0
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                return finish(path,intent['generator_id'],verify(path,intent,report))
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis']
        assert DB.basis()==basis and LINEAGE in DB.command('status')
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
        kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        stock,used=current_sources(kp,path,basis)
        needed={l:max(0,5-stock['distinct_available'][l]) for l in LEVELS}
        reg=kp.get(':knowledge-point/question-generator')
        gid=str(reg[':question-generator/id']) if reg else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        identities=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not identities or (reg and len(identities)==1 and identities[0][0][':db/id']==reg[':db/id'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        supplied=JOB.with_suffix('.generated')
        payload=json.loads(supplied.read_text()) if supplied.exists() else {}
        instances=payload.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:
            assert r['knowledge_point']['db_id']==KP
            v.validate_record(r)
        save(path/'supplied-status.json',{'exists':supplied.exists(),'validated_instances':len(instances)})
        records=[];selected={l:0 for l in LEVELS}
        def admit(rec):
            v.validate_record(rec)
            assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
            level=rec['question'][':question/difficulty'].split('/')[-1]
            fp=rec['generation']['mathematical_fingerprint']
            if selected[level]<needed[level] and fp not in used:
                records.append(copy.deepcopy(rec));used.add(fp);selected[level]+=1
        for r in instances:admit(r)
        for level in LEVELS:
            for seed in range(20261014,20261214):
                if selected[level]>=needed[level]:break
                # Execute the existing validated generator after the locked read.
                r=g.generate(level,seed=seed)
                admit(r)
        assert selected==needed,'Bounded distinct variants exhausted; retain explicit shortage'
        if '--prepare-only' not in sys.argv:
            review=json.loads((OUT/'visual-review.json').read_text())
            assert review['passed'] and review['generator_sha256']==sha(HERE.with_suffix('.py'))
            assert {r['question'][':question/id'] for r in records}==set(review['question_ids'])
            assert all(sha(Path(p))==digest for p,digest in review['local_asset_hashes'].items())
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :question/id ?id]]',[ids],path,'question-identities',basis)
        grade(records+instances,path/'native-grading')
        save(path/'local-generated.json',records)
        assets=[];library=ImageLibrary(Path('/media/jake/SSD/EDB/math'))
        for rec in records:
            def publish(ref):
                local=Path(ref) if not ref.startswith('images/') else Path('/media/jake/SSD/EDB/math')/ref
                data=local.read_bytes();relative=library.put_bytes(data,content_type='image/png')
                assert (Path('/media/jake/SSD/EDB/math')/relative).read_bytes()==data
                assets.append({'local':str(local),'path':relative,'sha256':hashlib.sha256(data).hexdigest()})
                return relative
            q=rec['question']
            for key in (':question/problem',':question/worked-solution'):
                q[key]=re.sub(r'!\[\]\(([^)]+)\)',lambda m:'![]('+publish(m[1])+')',q[key])
            for f in q[':question/answer-fields']:
                for a in f[':answer-field/choices']:
                    if a[':answer/type']==':answer.type/image':a[':answer/value']=publish(a[':answer/value'])
        save(path/'assets.json',assets);save(path/'generated.json',records)
        grade(records,path/'published-grading')
        forms=transaction(records,kp,gid);assert forms
        tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'validated_available':stock['distinct_available'],'missing_by_level':needed,'selected_by_level':selected,'distinctness':'coordinate sets plus graphical workload; ignores seed, identity, bank order, and reflection','all_source_questions_preserved':True,'asset_hashes':assets})
        pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(pr.stdout);preview_report=loads(pr.stdout)
        assert preview_report[':edb/committed'] is False and preview_report[':edb/db-before-t']==basis
        check_report(preview_report,path/'preview-check',source[0][0]);assert DB.basis()==basis
        if '--prepare-only' in sys.argv:
            print(json.dumps({'prepared':str(path),'selected_by_level':selected}),flush=True)
            return
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'graph-discontinuity-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'exact_edn':tx,'transaction_sha256':sha(txpath),'sha256':sha(txpath),'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report))

if __name__=='__main__':main()
