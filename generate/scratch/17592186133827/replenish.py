"""Additive, exact-basis replenishment for scalar substitution KP only."""
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

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('scalar_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.CAPTURE['lineage']
SOURCE = ':application/ca-engine'
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'47329fb7cd9a66a9c8d029339f33db2e87474d9172d52b94d9fe7d1aa0182a03'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-0402b744f6358693'
QUERY = (OUT/'source-query.edn').read_text()

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def relative(path): return str(path.relative_to(ROOT))
def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID): return str(value)
    return value

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=ENV, capture_output=True, text=True, check=True, timeout=90)
    result = json.loads(r.stdout); assert result['ok']
    inv = result['data']; assert inv['lineage'] == LINEAGE
    save(path, inv)
    return inv

def read_kp(path, basis): return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def counts(inv, kp):
    jobs = {j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint'] == KP}
    observed = {str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1] for q in kp[':knowledge-point/questions']}
    # Native inventory omits bands at or above target and all unobserved bands.
    return {level: jobs[level]['available'] if level in jobs else (5 if level in observed else 0) for level in LEVELS}

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']: f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def normalize(q):
    result = {k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in q[':question/answer-fields']:
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':[{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return ordered(result)

def fingerprint(q):
    if q.get(':question/math-academy-id') in g.SOURCE_TEMPLATE:
        family = g.SOURCE_TEMPLATE[q[':question/math-academy-id']]
        m = g.mathematics(family, g.ANCHORS[family]); f,r,a,b=m['f'],m['r'],m['low'],m['high']
    else:
        f,r,a,b = v.prompt_object(q)
    return g.digest([[str(c) for c in r],str(f),str(a),str(b)])

def validate(rec):
    md = rec['generation']; q = rec['question']
    assert md['eligible_for_learning'] and not md['evidence_only'] and md['profile']=='method'
    assert rec['knowledge_point']['db_id']==KP
    assert rec['knowledge_point']['id']==g.KP[':knowledge-point/id']
    level = q[':question/difficulty'].split('/')[-1]
    assert level in LEVELS and g.LEVELS[md['template']]==level
    replay = g.generate(level, md['seed'], template=md['template'], parameters=md['parameters'], profile=md['profile'])
    assert ordered(q)==ordered(replay['question']) and md==replay['generation']
    v.audit(rec)
    assert fingerprint(q)==md['mathematical_fingerprint']
    # Independent numerical quadrature from parsed learner-visible inputs.
    import mpmath as mp
    f,r,a,b=v.prompt_object(q); fr=f.subs(dict(zip((g.x,g.y,g.z),r)),simultaneous=True)
    speed=g.S.sqrt(sum(g.S.diff(c,g.t)**2 for c in r)); integrand=g.S.simplify(fr*speed)
    mp.mp.dps=35; aa,bb=[mp.mpf(str(g.S.N(c,35))) for c in (a,b)]
    fn=g.S.lambdify(g.t,integrand,'mpmath'); numeric=mp.quad(fn,[aa,(aa+bb)/2,bb])
    expected=mp.mpf(str(g.S.N(g.S.sympify(md['solution_components']['answer']),35)))
    assert abs(numeric-expected)<mp.mpf('1e-25')

def replay_sources(path):
    evidence=[]
    for sid,source in g.SOURCES.items():
        family=g.SOURCE_TEMPLATE[sid]
        q=g.generate(g.LEVELS[family],template=family,profile='raw:'+sid,parameters={'scale':1})['question']
        assert q[':question/problem']==source[':question/problem']
        assert q.get(':question/worked-solution')==source.get(':question/worked-solution')
        assert (':question/difficulty' in q)==(':question/difficulty' in source)
        if ':question/difficulty' in source: assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
        f=q[':question/answer-fields'][0]; original=source[':question/answer-fields'][0]
        assert f[':answer-field/key']==original[':answer-field/key'] and f[':answer-field/type']==original[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
        assert (':answer-field/correct' in f)==(':answer-field/correct' in original)
        if ':answer-field/correct' in f:
            assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==original[':answer-field/correct'][':answer/value']
        evidence.append({'source':sid,'complete_bank_values_matched':5,'prompt_exact':True,'solution_presence_and_text_exact':True,'designation_presence_and_value_exact':True})
    save(path,evidence)

def transaction(records, kp, gid):
    forms=[]
    for rec in records:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if not gen:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else: assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records: forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms: forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP: assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant': assert e in new and name in allowed,name

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}; now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    ignore=(':knowledge-point/questions',':knowledge-point/question-generator')
    assert {k:v for k,v in before.items() if k not in ignore}=={k:v for k,v in kp.items() if k not in ignore}
    records=json.loads((path/'generated.json').read_text()); assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q)==ordered(rec['question'])
        assert fingerprint(q)==rec['generation']['mathematical_fingerprint']
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result)
    return result,kp

def finish(path,gid,verified,inv,kp):
    prep=json.loads((path/'preparation.json').read_text()); after=counts(inv,kp);shortage={l:max(0,5-after[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'generated_counts':prep['generated_counts'],'available_counts_before':prep['available_counts'],'available_counts_after':after,'supported_levels':list(LEVELS),'supported_shortage_remaining':shortage,'capability_exceptions':[],'unsupported_levels_filled':False,'legacy_unclassified':{'question':'q-76187','preserved':True,'counted_as_available':False,'reason':'Missing source difficulty, solution and correct reference; authored variants carry complete validated content.'},'finite_variant_limit':json.loads((HERE/'domain-counts.json').read_text()),'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[relative(path/n) for n in ('verification.json','preparation.json','inventory-after.json','generated.json','source-replay.json','native-report.json','transaction.edn','commit-intent.json','preview.edn','commit.edn') if (path/n).exists()]}
    assert not any(shortage.values()),'Supported shortage remains; inspect before declaring generated'
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','new_questions','available_counts_after','verified_commit_basis','remaining_jobs')}),flush=True)

def main():
    prior=json.loads((ROOT/'generate/runs/current/qa/17592186133827.json').read_text())
    assert prior['parent_review']=='passed' and prior['generator_sha256']==sha(HERE.with_suffix('.py'))
    for name,digest in prior['root_artifact_hashes'].items(): assert sha(ROOT/name)==digest,name
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    initial=inventory(OUT/'inventory-before-generation.json');basis=initial['basis'];kp=read_kp(OUT/'initial',basis)
    c=counts(initial,kp);need={l:max(0,5-c[l]) for l in LEVELS}
    used={fingerprint(q) for q in kp[':knowledge-point/questions']}
    used.add(g.digest([[str(g.t**2),str(g.t),'1'],str(g.x/(g.y*g.z)),'0',str(g.S.sqrt(2))]))
    supplied_path=JOB.with_suffix('.generated'); candidates=[]
    if supplied_path.exists():
        supplied=json.loads(supplied_path.read_text()); candidates=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(candidates,dict): candidates=[candidates]
        for rec in candidates: validate(rec)
    save(OUT/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(candidates)})
    generated=[]
    for level in LEVELS:
        n=0
        for rec in [r for r in candidates if r['question'][':question/difficulty'].endswith('/'+level)]:
            fp=fingerprint(rec['question'])
            if fp not in used and n<need[level]: generated.append(rec);used.add(fp);n+=1
        for seed in range(int(JOB.name[:8],16),int(JOB.name[:8],16)+200):
            if n>=need[level]: break
            rec=g.generate(level,seed);fp=fingerprint(rec['question'])
            if fp in used: continue
            validate(rec); generated.append(rec);used.add(fp);n+=1
        assert n==need[level], 'Bounded domain exhausted; document finite-limit before committing'
    save(OUT/'validated-candidates.json',generated)
    print(json.dumps({'validated_candidates':len(generated),'needed':need}),flush=True)
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        assert LINEAGE in DB.command('status')
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path); verified,kp=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'),kp);return
        inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.KP[':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        expected={q[':question/math-academy-id']:q for q in g.KP[':knowledge-point/questions']}
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for mid,q in expected.items(): assert canonical(current[mid])==canonical(q),'Source changed; reclassify '+mid
        assert canonical(g.KP[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        replay_sources(path/'source-replay.json')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        registered=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b)
        assert len(registered)<=1
        identity_path=HERE/'generator-identity.json'
        saved=json.loads(identity_path.read_text()) if identity_path.exists() else None
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else saved['id'] if saved else str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/question-generator/'+str(KP)))
        if saved: assert saved['id']==gid
        save(identity_path,{'id':gid,'script':SCRIPT,'knowledge_point':KP})
        assert not registered or str(registered[0][0][':question-generator/id'])==gid
        occupied=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not occupied or occupied[0][0][':question-generator/script']==SCRIPT
        available=counts(inv,kp);needed={l:max(0,5-available[l]) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};records=[];added={l:0 for l in LEVELS}
        for r in generated:
            l=r['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(r['question'])
            if fp not in used and added[l]<needed[l]: records.append(r);used.add(fp);added[l]+=1
        assert added==needed,'Inventory changed; regenerate at fresh basis'
        for attribute,key,values in (('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if values: assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[values],path,'identity-'+key,b)
        save(path/'generated.json',records);save(path/'native-input.json',[v.engine(r,r['question'][':question/id']) for r in records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        native=json.loads((path/'native-report.json').read_text());assert native['documented_unresolved_checks']==0 and native['accepted_checks']==len(records) and native['rejected_checks']==len(records)*4
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'needed':needed,'generated_counts':added,'available_counts':available,'new_questions':len(records),'source_evidence_unchanged':True,'asset_hashes':[],'plot_requirements':'none','distinct_mathematical_tasks':len({fingerprint(r['question']) for r in records}),'generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(HERE/'validate.py'),'native_grader_sha256':sha(ROOT/'generate/runs/current/check-engine'),'printed_math_audits':v.COUNTS,'quadrature_precision_digits':35,'quadrature_absolute_tolerance':'1e-25','prior_qa':relative(ROOT/'generate/runs/current/qa/17592186133827.json'),'inventory_count_evidence':'Native inventory under application api.lock; absent unobserved easy band explicitly classified by validated generator.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0};save(path/'verification.json',verified);finish(path,gid,verified,inv,kp);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream: stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'scalar-substitution-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified,kp=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'),kp)
if __name__=='__main__':main()
