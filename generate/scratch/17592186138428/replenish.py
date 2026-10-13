"""Scoped graphical-system inventory; additive EDB writes serialized by api.lock."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('graph_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '606072538b9164176eae2531fa81032c931e678ad58f3f10ce73941ff158b76d'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent / 'EDB')
QUESTION = '''[* {:question/difficulty [:db/id :db/ident]}
 {:knowledge-point/_questions [:knowledge-point/id :knowledge-point/title]}
 {:knowledge-point/_canonical-example [:knowledge-point/id :knowledge-point/title]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'''
QUERY = '[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION+'} {[:knowledge-point/questions :limit nil] '+QUESTION+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
UNAVAILABLE = '''[:find ?q :in $ ?learner ?kp
 :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
   (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
   (and [?l :learner/activity ?t] [?t :learner-task/activity ?a]
     (or [?t :learner-task/status :learner-task.status/started]
         [?t :learner-task/status :learner-task.status/paused])
     (or [?a :activity/type :activity.type/lesson]
         [?a :activity/type :activity.type/review]
         [?a :activity/type :activity.type/assessment])
     [?a :activity/steps ?st] [?st :step/content ?q]))]'''
MATH_ROOT = Path('/media/jake/SSD/EDB/math')

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis): return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

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
    for f in q[':question/answer-fields']: f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def rows(q):
    text = q[':question/problem']
    if r'\begin{array}' in text:
        body = re.search(r'\\begin\{array\}\{l\}(.*?)\\end\{array\}',text,re.S).group(1)
        equations = body.split(r'\\')
    elif r'\begin{aligned}' in text:
        body = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S).group(1)
        equations = body.split(r'\\')
    else:
        equations = re.search(r'\$\{([^$]+)\$',text).group(1).split(';')
    assert len(equations)==2
    result=[]
    for equation in equations:
        lhs,rhs=equation.replace('&','').split('=')
        e=sp.expand(v.expr(lhs)-v.expr(rhs)); poly=sp.Poly(e,v.X,v.Y);assert poly.total_degree()==1
        vals=[e.coeff(v.X),e.coeff(v.Y),-e.subs({v.X:0,v.Y:0})]
        scale=sp.ilcm(*[a.q for a in vals]); nums=[int(a*scale) for a in vals]
        divisor=sp.igcd(*nums); nums=[n//divisor for n in nums]
        if next(n for n in nums if n)<0:nums=[-n for n in nums]
        result.append(nums)
    matrix=sp.Matrix([r[:2] for r in result]);assert matrix.det()!=0
    answer=list(matrix.inv()*sp.Matrix([r[2] for r in result]))
    return result,answer

def fingerprint(q, tick=1):
    return g.digest({'lines':sorted(rows(q)[0]),'major_tick_increment':tick,'minor_grid_increment':1})

def checks(q):
    values=rows(q)[1];out=[]
    for i,value in enumerate(values):
        out.extend([{'field_index':i,'submitted':str(value),'expected':'accepted','purpose':'canonical coordinate'},
                    {'field_index':i,'submitted':f'({3*value})/3','expected':'accepted','purpose':'equivalent coordinate'},
                    {'field_index':i,'submitted':str(value+1),'expected':'rejected','purpose':'wrong coordinate'}])
    return out

def validate_question(q):
    _,values=rows(q)
    fields=q[':question/answer-fields'];assert len(fields)==2
    for i,f in enumerate(sorted(fields,key=lambda x:x[':answer-field/key'])):
        assert f[':answer-field/key']==f'field-{i+1}' and f[':answer-field/type']==':answer-field.type/blank'
        assert q[':question/problem'].count('{{'+f[':answer-field/key']+'}}')==1
        assert len(f[':answer-field/choices'])==1
        a=f[':answer-field/choices'][0];assert a[':answer/type']==':answer.type/math'
        assert sp.Rational(a[':answer/value'])==values[i]
        assert f[':answer-field/correct']==[':answer/id',a[':answer/id']]
    points=re.findall(r'\$\((-?\d+),(-?\d+)\)\.?\$',q[':question/worked-solution'])
    assert len(points)==2 and all([int(x),int(y)]==values for x,y in points)
    for key in (':question/problem',':question/worked-solution'):
        refs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',q[key]);assert len(refs)==1
        p=Path(refs[0]);p=p if p.is_absolute() else MATH_ROOT/p
        assert p.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
        if refs[0].startswith('images/'):assert sha(p)==p.stem


def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(UNAVAILABLE,[LEARNER,KP],path,'unavailable',basis)}
    used=set();available={l:set() for l in g.LEVELS};validated=[];excluded=[];fixtures=[]
    # Original absent difficulty/correct facts stay untouched; no inference turns
    # those two source questions into available inventory.
    for q in kp[':knowledge-point/questions']:
        tick=2 if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/hard' else 1
        fp=fingerprint(q,tick);used.add(fp)
        if ':question/difficulty' not in q or ':question/worked-solution' not in q or any(':answer-field/correct' not in f for f in q[':question/answer-fields']):
            excluded.append({'id':q[':db/id'],'reason':'Unrated/incomplete original; preserved'});continue
        n=normalize(q);validate_question(n)
        if ':question/math-academy-id' not in q:
            # Verify this package's question against its saved rendered evidence.
            saved=[r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text()) if r['question'][':question/id']==n[':question/id']]
            assert saved and ordered(saved[0]['question'])==n
            tick=saved[0]['generation']['plot_data']['tick_increment']
            assert fingerprint(n,tick)==saved[0]['generation']['mathematical_fingerprint']
        lv=n[':question/difficulty'].split('/')[-1];assert lv in g.LEVELS
        fixtures.append({'label':n[':question/id'],'record':{'question':n,'knowledge_point':{'title':g.TITLE},'generation':{'template':'current-inventory'}},'checks':checks(n)})
        validated.append(q[':db/id'])
        if q[':db/id'] not in unavailable:available[lv].add(fp)
    save(path/'inventory-engine-input.json',fixtures)
    if fixtures:subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'inventory-engine-input.json'),str(path/'inventory-engine-report.json')],check=True)
    result={'basis':basis,'validated_practice_ids':validated,'excluded_source_questions':excluded,'unavailable_ids':sorted(unavailable),'distinct_available':{lv:len(pool) for lv,pool in available.items()},'missing':{lv:max(0,5-len(pool)) for lv,pool in available.items()},'deduplication':'Unordered primitive line equations plus assessed grid scale; seed/layout/color/identity excluded'}
    save(path/'validated-inventory.json',result)
    return result,used


def publish(records):
    lib=ImageLibrary(MATH_ROOT);published=[];assets=[]
    for r in records:
        v.check(r);rec=copy.deepcopy(r)
        for role,src in r['generation']['plot_assets'].items():
            data=Path(src).read_bytes();dst=lib.put_bytes(data,content_type='image/png')
            assert (MATH_ROOT/dst).read_bytes()==data
            for key in (':question/problem',':question/worked-solution'):rec['question'][key]=rec['question'][key].replace(src,dst)
            assets.append({'question':rec['question'][':question/id'],'role':role,'source':src,'path':dst,'sha256':sha(src)})
        # Identity is retained when publishing byte-identical assets; local
        # content digest and task identity are explicitly separate from storage.
        rec['generation']['published_assets']=[a for a in assets if a['question']==rec['question'][':question/id']]
        validate_question(rec['question']);published.append(rec)
    return published,assets


def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms


def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name


def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:x for k,x in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:x for k,x in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(r['question']);validate_question(normalize(q))
        assert fingerprint(q,r['generation']['plot_data']['tick_increment'])==r['generation']['mathematical_fingerprint']
        for a in r['generation']['published_assets']:assert sha(MATH_ROOT/a['path'])==a['sha256']
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result


def finish(path,gid,verified,inv):
    stock,_=counts(read_kp(path/'post-inventory',inv['basis']),path/'post-inventory',inv['basis'])
    shortages={k:x for k,x in stock['missing'].items() if x}
    result={'outcome':'finite-limit' if shortages else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(g.LEVELS),'supported_inventory':stock,'supported_shortages_remaining':shortages,'capability_exceptions':[],'finite_variant_limits':json.loads((HERE/'validation.json').read_text())['finite_unique_line_and_scale_tasks'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'preparation.json',path/'inventory-after.json',path/'post-inventory/validated-inventory.json',HERE/'validation.json',HERE/'classification-refresh.md',HERE/'review.md',path/'native-report.json')],'note':'Four immutable source questions and canonical example preserved; two incomplete unrated sources remain excluded. Authored bounded E/M/H peers validated and gradable. Mathematical tasks deduplicated independently of seed, layout, color and identities.'}
    for name in ('commit-intent.json','transaction.edn','commit.edn','preview.edn'):
        if (path/name).exists():result['evidence'].append(str((path/name).relative_to(ROOT)))
    if shortages:result['capability_exceptions']=[{'level':lv,'shortage':need,'filled':False,'reason':'Bounded distinct domain exhausted; retain pending shortage'} for lv,need in shortages.items()]
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','supported_shortages_remaining','remaining_jobs')}),flush=True)


def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
    assert sha(HERE.with_suffix('.py'))==validation['script_sha256'] and sha(HERE/'render.py')==validation['renderer_sha256']
    preview=preview_executable(SimpleNamespace(math_root=MATH_ROOT,repo_root=ROOT,preview_bin=None),threading.Event())
    # Recover retained requests under the same lock before generating fresh work.
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn')
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['endpoint']==DB.args.endpoint
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        # New source evidence must be explicitly included in refreshed classification.
        frozen=loads((HERE/'reference/current-kp.edn').read_text())
        old_source={str(q[':question/id']):q for q in frozen[':knowledge-point/questions']}
        current_source={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
        assert current_source==old_source,'Source changed since classification; refresh first'
        assert frozen[':knowledge-point/canonical-example']==kp[':knowledge-point/canonical-example']
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');identity=HERE/'generator-identity.json'
        gid=str(gen[':question-generator/id']) if gen else (json.loads(identity.read_text())['id'] if identity.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator')))
        if identity.exists():assert gid==json.loads(identity.read_text())['id']
        save(identity,{'id':gid,'script':SCRIPT,'knowledgePoint':KP})
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or gen and registered[0][0][':db/id']==gen[':db/id']
        stock,used=counts(kp,path,b)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied;assert isinstance(instances,list)
        for r in instances:
            assert r['knowledge_point']['db_id']==KP;v.check(r)
            replay=g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
            assert ordered(replay['question'])==ordered(r['question'])
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances)})
        records=[];native=[]
        # Exhaustively enumerate bounded candidates; randomization only chooses
        # order. Coordinate diversity is preferred, never used as an identity.
        for level in g.LEVELS:
            need=stock['missing'][level];chosen=[];coordinates=set()
            candidates=[]
            for t in g.TEMPLATES:
                for p in g.domain(level,t):
                    task=g.digest({'lines':sorted(g.equations(p,t)[0]),'major_tick_increment':2 if level=='hard' else 1,'minor_grid_increment':1})
                    if task not in used:candidates.append((t,p,task))
            random.Random(138428).shuffle(candidates)
            for r in instances:
                if len(chosen)>=need:break
                if r['question'][':question/difficulty']!=':question.difficulty/'+level:continue
                task=fingerprint(r['question'],r['generation']['plot_data']['tick_increment'])
                if task not in used:chosen.append(r);used.add(task);coordinates.add(tuple(rows(r['question'])[1]))
            for diversity in (True,False):
                for t,p,task in candidates:
                    if len(chosen)>=need:break
                    point=(p['x'],p['y'])
                    if task in used or (diversity and point in coordinates):continue
                    r=g.generate(level,seed=138428,template=t,parameters=p,profile='authored');v.check(r)
                    assert task==fingerprint(r['question'],r['generation']['plot_data']['tick_increment'])==r['generation']['mathematical_fingerprint']
                    chosen.append(r);used.add(task);coordinates.add(point)
                if len(chosen)>=need:break
            records.extend(chosen)
        save(path/'local-generated.json',records)
        published,assets=publish(records);save(path/'generated.json',published)
        for r in published:native.append({'label':r['question'][':question/id'],'record':r,'checks':checks(r['question'])})
        save(path/'native-input.json',native)
        if native:subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        else:save(path/'native-report.json',{'records':0,'no_changes':True})
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'generator_id':gid,'generator_path':SCRIPT,'asset_hashes':assets,'validated_inventory':stock,'new_questions':len(published),'distinct_generated_tasks':len({r['generation']['mathematical_fingerprint'] for r in published}),'source_evidence_unchanged':True,'lock':str(ROOT/'.local/learning/requests/math/api.lock')})
        if '--prepare-only' not in sys.argv and published:
            qa=json.loads((HERE/'reference/selected-visual-review.json').read_text());assert qa['passed']
            assert {r['question'][':question/id'] for r in published} <= set(qa['reviewed_question_uuids']), 'New selection needs visual review'
            for r in records:
                for asset in r['generation']['plot_assets'].values():assert qa['reviewed_asset_hashes'][asset]==sha(asset)
        forms=transaction(published,kp,gid)
        if not forms:
            save(path/'verification.json',{'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'generator_registration_verified':True})
            finish(path,gid,json.loads((path/'verification.json').read_text()),inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        if '--prepare-only' in sys.argv:
            print(json.dumps({'prepared_basis':b,'new_questions':len(published),'path':str(path),'database_writes':0}),flush=True);return
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'graphical-system-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in published],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
