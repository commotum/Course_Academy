"""Scoped additive replenishment with retained requests and exact-basis readback."""
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP
g.SUPPORTED_LEVELS = ("easy", "moderate", "hard")
g.GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(g.R[":knowledge-point/id"]), "question-generator"))
g.NAMESPACE = g.R[":knowledge-point/id"]
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'b042b2524fc4fcadf58bd9572c2fede37892816b362e7703316e9660b1409ab5'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env = database_environment('math')
NATIVE = ROOT / '.local/graph-explorer/learning-c9743ced043e1fd7'
QUERY = (HERE / 'reference/source-query.edn').read_text()

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

def fingerprint(q):
    import re
    import sympy as sp
    blocks=re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',q[':question/problem'])
    blocks=[a or b for a,b in blocks]
    mapping=next(t for t in blocks if 'u' in t and 'v' in t and '=' in t)
    mapping=mapping.replace(r'\,','').replace(r'\quad','').replace(r'\qquad','')
    left,right=mapping.strip().rstrip(',').split(',')
    U,V=[g.parse(t.split('=',1)[1]) for t in [left,right]]
    equations=[]
    for t in re.findall(r'\$([^$]+)\$',q[':question/problem'].split('bounded by',1)[1]):
        a,b=t.rstrip(',.').split('=');expr=sp.expand(g.parse(a)-g.parse(b))
        equations.append(str(sp.Poly(expr,g.x,g.y).monic().as_expr()))
    return g.digest({'maps':[str(U),str(V)],'boundaries':sorted(equations)})

def checks(rec):
    field=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'actual learner radio grading'} for a in field[':answer-field/choices']]

def validate(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['generation']['eligible_for_learning']
    local=copy.deepcopy(rec)
    # The mathematical readback also checks the original render's PNG sidecar.
    import re
    local['question'][':question/worked-solution']=re.sub(r'!\[\]\([^)]+\)',lambda _: '![]('+rec['generation']['plot']+')',local['question'][':question/worked-solution'])
    return v.math_readback(local)

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

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    rows={level:[] for level in g.SUPPORTED_LEVELS};fixtures=[];excluded=[]
    committed={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    known={**{r['question'][':question/id']:r for r in candidate_records()},**committed}
    # Independently checked source questions, including original image inspection.
    trusted={'q-160885','q-83943','q-160710','q-38132'}
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id');qid=str(q[':question/id'])
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or ':question/difficulty' not in q:
            excluded.append({'id':qid,'reason':'shown/reserved, canonical, or unrated'});continue
        if mid in trusted:
            source_math(q)
            rec={'question':normalize(q)}
        elif qid in known:
            rec=known[qid];assert normalize(q)==ordered(rec['question']);validate(rec)
        else:
            excluded.append({'id':qid,'source':mid,'reason':'source defect or outside this validated package'});continue
        fixtures.append({'label':qid,'record':rec,'checks':checks(rec)})
        rows[str(q[':question/difficulty'][':db/ident']).split('/')[-1]].append(q)
    save(path/'inventory-native-input.json',fixtures)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'inventory-native-input.json'),str(path/'inventory-native-report.json')],check=True)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]}for level,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded':excluded,'unrated_and_canonical_excluded':True}
    save(path/'available-counts.json',result);return result

def source_math(q):
    import re
    import sympy as sp
    snap=json.loads((HERE/'reference/initial/kp.json').read_text())
    original=next(z for z in snap[':knowledge-point/questions']if z[':question/id']==str(q[':question/id']))
    assert canonical(q)==canonical(original),'Source changed; repeat source review'
    pr,sol=q[':question/problem'],q[':question/worked-solution']
    m=re.search(r'\$\$\nu=(.*?),\\,v=(.*?),\n\$\$',pr);assert m
    U,V=map(g.parse,m.groups());mat=sp.Matrix([[sp.diff(z,t)for t in [g.x,g.y]]for z in [U,V]])
    det=mat.det();inv=sp.solve([g.u-U,g.v-V],(g.x,g.y))
    dom=re.search(r'Δ=\\\{\(u,v\)\\,:\\,(.*?)\\le u\\le (.*?),\\,(.*?)\\le v\\le (.*?)\\\}\.',sol);assert dom
    lo,hi,low,high=map(g.parse,dom.groups());assert hi>lo
    boundaries=[]
    for t in re.findall(r'\$([^$]+)\$',pr.split('bounded by',1)[1]):
        a,b=t.rstrip(',.').split('=');boundaries.append(sp.expand(g.parse(a)-g.parse(b)).subs(inv,simultaneous=True))
    if len(boundaries)==3:
        assert any(g.eq(z.subs(g.u,lo),0)for z in boundaries)
        assert any(g.eq(z.subs(g.v,low),0)for z in boundaries)
        assert any(g.eq(z.subs(g.v,high),0)for z in boundaries)
        assert g.eq(low.subs(g.u,hi),high.subs(g.u,hi))
    else:
        assert g.eq(boundaries[0].subs(g.v,low),0) and g.eq(boundaries[1].subs(g.v,high),0)
        assert all(g.eq(low.subs(g.u,t),high.subs(g.u,t)) for t in [lo,hi])
    assert float((high-low).subs(g.u,(lo+hi)/2))>0
    area=sp.simplify(abs(1/det)*sp.integrate(high-low,(g.u,lo,hi)))
    f=q[':question/answer-fields'][0];bank=[g.parse(a[':answer/value'])for a in f[':answer-field/choices']]
    assert len(bank)==5 and all(not g.eq(a,b)for i,a in enumerate(bank)for b in bank[i+1:])
    assert g.eq(area,g.parse(f[':answer-field/correct'][':answer/value']))
    final=sol.rsplit('& =',1)[-1].split(r'\end{aligned}')[0].rstrip('.')
    assert g.eq(g.parse(final),area)
    for asset in re.findall(r'!\[\]\(([^)]+)\)',sol):
        ap=Path(DB.env['EDB_MATH_ROOT'])/asset;assert sha(ap)==ap.stem
    return area

def candidate_records():
    return json.loads((HERE/'reference/candidates.json').read_text())

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question']);validate(rec)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text())
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(g.SUPPORTED_LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels':[],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'reference/current-classification.md',HERE/'reference/freeze.json']if p.exists()],'note':'All supported difficulty reserves verified. Historical unrated source remains unchanged and may keep the unclassified scheduler job visible. New source template limitations are recorded in current-classification.md.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k]for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def main():
    validation=json.loads((HERE/'reference/freeze.json').read_text());assert validation['status']=='pass' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==str(g.NAMESPACE)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'reference/initial/kp.json').read_text())
        current={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:assert canonical(current[q[':question/id']])==canonical(q),'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(captured[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        orphan=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not orphan or gen and orphan[0][0][':db/id']==gen[':db/id'], 'Existing identity requires reconciliation'
        assert gid==g.GENERATOR_UUID
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));records=[];added={l:0 for l in g.SUPPORTED_LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:validate(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        for rec in instances+candidate_records():
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                validate(rec);records.append(rec);used.add(fp);added[level]+=1
        # Batch lookup stable question/field/answer identities before creating entities.
        ids=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id']]+[f[':answer-field/id'] for f in rec['question'][':question/answer-fields']]+[a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing identities require reconciliation'
        save(path/'generated.json',records)
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        import re
        from capture.scripts.database.images import ImageLibrary
        images=ImageLibrary(Path(DB.env['EDB_MATH_ROOT']),HERE)
        asset_hashes=[]
        for rec in records:
            local=rec['generation']['plot'];rel=images.resolve(local)
            asset=Path(DB.env['EDB_MATH_ROOT'])/rel;assert sha(asset)==asset.stem
            rec['question'][':question/worked-solution']=rec['question'][':question/worked-solution'].replace(local,rel)
            asset_hashes.append({'local':local,'reference':rel,'sha256':sha(asset),'verified_available':True})
            validate(rec)
        save(path/'generated.json',records)
        save(path/'preparation.json' ,{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':asset_hashes,'source_evidence_unchanged':True,'source_basis':2715})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'type-I-area-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
