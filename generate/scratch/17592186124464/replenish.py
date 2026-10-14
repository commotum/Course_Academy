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
s = g.S
KP = g.KP
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'0fa66d12fe4270e681768a838d04687ea8099d8c999340fd698b83a351c837f5'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True,exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = max((ROOT/'.local/graph-explorer').glob('learning-*'),key=lambda p:p.stat().st_mtime)
DISCOVERY = max((ROOT/'.local/generate').glob('find-candidates-*'),key=lambda p:p.stat().st_mtime)
LEVELS = ('easy','moderate','hard')
Q = '[* {:question/difficulty [:db/id :db/ident]}\n {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/ident]}\n {:answer-field/correct [* {:answer/type [:db/ident]}]}\n {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]}]}]'
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
    request={'database':'math','learner':LEARNER,'topics':[17592186050027],'activity_type':'lesson','after_basis':None,'lineage':None,'at':None}
    r = subprocess.run([str(DISCOVERY)],input=json.dumps(request),env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout)
    assert x['cursor']['lineage']==LINEAGE
    save(path,x)
    pools=[kp for t in x['topics'] for kp in t['knowledge_points'] if kp['db/id']==KP]
    assert len(pools)==1
    return x['basis'],pools[0]['inventory']['available']

def read_kp(path,basis):
    return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

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




def plain(obj):
    if isinstance(obj,dict):
        if ':db/ident' in obj:return str(obj[':db/ident'])
        return {str(k):plain(a) for k,a in obj.items()}
    if isinstance(obj,list):return [plain(a) for a in obj]
    if isinstance(obj,uuid.UUID):return str(obj)
    return obj

def as_record(q):
    q=plain(q)
    for f in q[':question/answer-fields']:
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
    return {'knowledge_point':{'db_id':KP,'id':g.SRC[':knowledge-point/id'],'title':g.SRC[':knowledge-point/title']},'question':q,'generation':{'template':q.get(':question/math-academy-id','easy_quadratic' if q[':question/difficulty']==':question.difficulty/easy' else 'existing')}}

def parametric_line(value):
    coords=[]
    for coord in g.V:
        match=re.search(str(coord)+r'\s*=\s*(.*?)(?=,|$)',value)
        assert match,('missing parametric coordinate',value)
        coords.append(g.parse(match[1].replace(r'\sqrt',r' \sqrt')))
    point=tuple(s.simplify(a.subs(g.t,0)) for a in coords)
    direction=tuple(s.simplify(s.diff(a,g.t)) for a in coords)
    assert all(not a.free_symbols for a in point+direction)
    assert all(v.same(a,p+g.t*d) for a,p,d in zip(coords,point,direction))
    return point,direction

def source_check(rec):
    q=rec['question']
    if rec['generation']['template']!='q-37231':return v.verify(rec,True)
    v.formatting(q);P,F,residual,G=v.parts(q)
    assert v.same(residual.subs(dict(zip(g.V,P))),0)
    assert any(a!=0 for a in G) and all(a.is_real and a.is_finite for a in P+G)
    gradient=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[1]
    symbolic=numeric=formal=0
    for row in gradient.split(r'\\'):
        if '∂' in row:
            assert all(v.same(a,F) for a in v.operands(row));formal+=1
        else:
            components=g.vector_parts(row)
            if any(a.free_symbols for a in components):
                assert all(v.same(a,s.diff(F,b)) for a,b in zip(components,g.V));symbolic+=1
            else:
                assert all(v.same(a,b) for a,b in zip(components,G));numeric+=1
    assert formal==symbolic==1 and numeric>=1
    # Preserve and inspect all three general point-plus-partial construction rows.
    for coordinate in 'xyz':
        assert coordinate+r' & ={'+coordinate+r'}_{0}+{f}_{'+coordinate+r'}({x}_{0},{y}_{0},{z}_{0})t' in q[':question/worked-solution']
    conclusion=q[':question/worked-solution'].split('$$')[-2].strip()
    assert g.equivalent(parametric_line(conclusion),(P,G))
    for field in q[':question/answer-fields']:
        validity=[g.equivalent(parametric_line(a[':answer/value']),(P,G)) for a in field[':answer-field/choices']]
        assert sum(validity)==1
        keyed=next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1])
        assert validity[keyed]
    return {'formal_rows':formal,'symbolic_rows':symbolic,'numeric_rows':numeric,'line_stages':4,'banks':1}

def fingerprint(q):
    match=re.search(r'(?:level )?surface \$(.*?)\$ at the point \$(.*?)\$',q[':question/problem']);assert match
    left,right=match[1].split('=');residual=s.expand(g.parse(left)-g.parse(right))
    point_text=match[2].rstrip('.,').replace(r'\left','').replace(r'\right','').strip()
    assert point_text[0]=='(' and point_text[-1]==')'
    P=tuple(g.parse(a) for a in g.components(point_text[1:-1]))
    if residual.is_polynomial(*g.V):canonical=s.Poly(residual,*g.V).monic().as_expr()
    else:
        _,canonical=residual.as_content_primitive()
        if canonical.could_extract_minus_sign():canonical=-canonical
    values=[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])]
    response='parametric' if 'parametric equations' in q[':question/problem'] else ('vector' if any('⟨' in a for a in values) else 'symmetric')
    return g.digest({'surface_relation':str(canonical),'P':[str(a) for a in P],'response':response,'t0':'parameter $t=0$' in q[':question/problem']})

def check(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.SRC[':knowledge-point/id']
    meta=rec['generation'];assert meta['version']==g.VERSION and meta['eligible_for_learning'] and not meta['evidence_only']
    level=rec['question'][':question/difficulty'].split('/')[-1]
    replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
    assert ordered(replay['question'])==ordered(rec['question'])
    assert meta['mathematical_fingerprint']==replay['generation']['mathematical_fingerprint']
    v.verify(rec)
    assert fingerprint(rec['question'])==meta['mathematical_fingerprint']

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def validated_counts(kp,path,basis):
    unavailable={row[0] for row in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable|={row[0] for row in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historical-unavailable',basis,history=True)}
    rows={level:[] for level in LEVELS};excluded=[];native=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable:continue
        if q.get(':question/math-academy-id') in ('q-131124','q-37515'):
            excluded.append({'id':q[':question/math-academy-id'],'reason':'Known false worked equality or missing field correct ref; originals preserved.'});continue
        if not q.get(':question/difficulty') or not q.get(':question/worked-solution') or not q.get(':question/answer-fields') or not all(f.get(':answer-field/correct') for f in q[':question/answer-fields']):
            excluded.append({'id':str(q[':question/id']),'reason':'Incomplete or unrated'});continue
        rec=as_record(q);source_check(rec)
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        rows[level].append(q);native.append(v.engine_fixture(rec,str(q[':question/id'])))
    if native:
        save(path/'available-native-input.json',native)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True,capture_output=True,text=True)
    result={'basis':basis,'distinct_available':{l:len({fingerprint(q) for q in qs}) for l,qs in rows.items()},'available_ids':{l:[str(q[':question/id']) for q in qs] for l,qs in rows.items()},'excluded':excluded,'excluded_shown_or_reserved':sorted(unavailable)}
    save(path/'validated-counts.json',result);return result

def validate_sources(kp,path,basis):
    captured=g.SRC;current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    expected={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
    for sid,q in expected.items():assert source_projection(current[sid],q)==q,('Changed frozen source',sid)
    assert source_projection(kp[':knowledge-point/canonical-example'],captured[':knowledge-point/canonical-example'])==captured[':knowledge-point/canonical-example']
    refreshed=loads((HERE/'reference/initial/kp.edn').read_text())[0][0]
    expected_current={q[':question/math-academy-id']:q for q in refreshed[':knowledge-point/questions']}
    assert set(current)==set(expected_current),'New source set requires renewed classification'
    for sid,q in expected_current.items():assert source_projection(current[sid],q)==q
    evidence=[]
    for sid in sorted(set(current)-set(expected)):
        rec=as_record(current[sid]);detail=source_check(rec);P,F,residual,G=v.parts(current[sid])
        evidence.append({'id':sid,'difficulty':g.enum(current[sid][':question/difficulty']).split('/')[-1],'point':list(map(str,P)),'level_function':str(F),'gradient':list(map(str,G)),'answer_shape':'parametric' if sid=='q-37231' else 'vector','source_math':detail,'full_bank_values':[a[':answer/value'] for f in current[sid][':question/answer-fields'] for a in f[':answer-field/choices']],'generation_scope':'New source retained and validated for inventory. Frozen v1 generation families unchanged; see current-evidence.md.'})
    save(path/'source-validation.json',{'passed':True,'current_basis':basis,'source_basis':1356,'frozen_questions_unchanged':len(expected),'current_source_questions':len(current),'newly_classified':evidence,'source_bank_replay':json.loads((HERE/'validation.json').read_text())['source'],'no_source_mutations':True})


def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:val for k,val in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:val for k,val in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(rec['question']);check(rec)
    assert not transaction([],kp,intent['generator_id'])
    available=validated_counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'validated_counts_after':available}
    save(path/'verification.json',result);return result


def finish(path,gid,verified,inv,available):
    shortage={l:max(0,5-available['distinct_available'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'source':SOURCE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'observed_levels':['moderate','hard'],'authored_levels':['easy'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':available['distinct_available'],'shortage_by_level':shortage,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':json.loads((path/'preparation.json').read_text())['capability_exceptions'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'source-validation.json',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'discovery-after.json',path/'generated.json',HERE/'current-evidence.md',HERE/'validation.json') if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)


def main():
    frozen=json.loads((HERE/'step-7-freeze.json').read_text())
    assert sha(HERE.with_suffix('.py'))==frozen['script_sha256'] and sha(HERE/'source.json')==frozen['source_sha256']
    validation=json.loads((HERE/'validation.json').read_text());assert validation['pass'] and validation['source']['exact_complete_banks']==15 and validation['source']['value_matches']==75
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired.',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                inv=inventory(path/'inventory-after.json');b,available=counts(path/'discovery-after.json');assert inv['basis']==b
                finish(path,intent['generator_id'],verified,inv,verified['validated_counts_after']);return
        inv=inventory(OUT/'inventory-before.json');b,nominal=counts(OUT/'discovery-before.json');assert DB.basis()==inv['basis']==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.SRC[':knowledge-point/id'];validate_sources(kp,path,b)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.SRC[':knowledge-point/id']),'question-generator'))
        if gen:assert gen.get(':question-generator/script',SCRIPT)==SCRIPT
        available=validated_counts(kp,path,b);needed={l:max(0,5-available['distinct_available'][l]) for l in LEVELS}
        selected={l:0 for l in LEVELS};used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];attempts={l:0 for l in LEVELS};supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        def select(rec):
            check(rec);level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if selected[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);selected[level]+=1
        for rec in instances:select(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        for level in LEVELS:
            for i in range(400):
                if selected[level]>=needed[level]:break
                attempts[level]+=1;select(g.generate(level,seed=int(JOB.name[:8],16)+i))
        exceptions=[{'level':l,'missing':needed[l]-selected[l],'attempt_limit':400,'evidence':'Bounded search exhausted; see integer-isometry bounds in template-extraction.md; no aliases admitted.'} for l in LEVELS if selected[l]<needed[l]]
        print(json.dumps({'basis':b,'nominal':nominal,'validated':available['distinct_available'],'needed':needed,'selected':selected}),flush=True)
        for attribute,ids in (('question/id',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[ids],path,attribute.replace('/','-')+'-collisions',b)
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
        save(path/'generated.json',records);save(JOB.with_suffix('.generated'),{'request':json.loads(JOB.with_suffix('.json').read_text())['request'],'instances':records})
        save(path/'native-input.json',[v.engine_fixture(r,r['question'][':question/id']) for r in records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True,text=True)
        (path/'review.md').write_text('# Replenishment variants\n\n'+'\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+r['question'][':question/worked-solution'] for r in records)+'\n')
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'nominal_available_by_level':nominal,'validated_available_by_level':available['distinct_available'],'missing_by_level':needed,'selected_by_level':selected,'sampling_attempts':attempts,'capability_exceptions':exceptions,'new_questions':len(records),'source_evidence_unchanged':True,'assets':[],'difficulty_evidence':'Moderate/hard observed; easy authored supplied quadratic-level, three single-term partials, integer evaluation and full vector line. See classification.md.','distinctness':'Printed surface relation, actual point and response criterion; seed, IDs, banks and order excluded. Existing/canonical tasks excluded.','generator_sha256':sha(HERE.with_suffix('.py')),'runtime':{'sympy':s.__version__,'python':sys.version},'family_scope':'Frozen 14 source families and authored easy. Current three new source families classified separately; no claim of generated coverage beyond frozen package.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'by_level':{l:0 for l in LEVELS},'validated_counts_after':available};save(path/'verification.json',{'passed':True,'no_change':True,**verified});finish(path,gid,verified,inv,available);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0])
        b2,nominal2=counts(path/'discovery-precommit.json');assert b2==b and nominal2==nominal and DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'normal-surface-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'generator_version':g.VERSION,'asset_hashes':[],'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);print('Validated preview; saved exact basis-guarded request.',flush=True)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        inv=inventory(path/'inventory-after.json');after,nominal=counts(path/'discovery-after.json');assert after==inv['basis']==verified['basis_after']
        finish(path,gid,verified,inv,verified['validated_counts_after'])

if __name__=='__main__':main()
