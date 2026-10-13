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
KP = g.ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '5b8b7b3b26a69c32a07186e861c6c5af2c837d848988bff055bfc579be983f82'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY = (HERE / 'reference/source-query.edn').read_text()
LEVELS = ('easy','moderate','hard')
GENERATOR_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, 'kp'+str(KP)+':generator'))
from capture.scripts.database.images import ImageLibrary
from capture.scripts.storage import atomic_text
import re
import sympy as S

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
    return hashlib.sha256(json.dumps(ordered(q),sort_keys=True).encode()).hexdigest()

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

def task(rec):
    p=rec['generation']['parameters'];a=g.vec(p['a']);b=g.vec(p.get('b',[0,0]));z=g.add(a,b)
    # Collapse reflections, rotations, renaming and choice order. Sum tasks also
    # retain the two leg magnitudes and their dot product (head-to-tail shape).
    return (rec['generation']['template'], tuple(sorted(str(abs(x)) for x in z)), tuple(sorted(str(sum(x*x for x in t)) for t in (a,b))), str(sum(x*y for x,y in zip(a,b))))

def check(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.REC[':knowledge-point/id']
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS
    gen=rec['generation'];replay=g.generate(level,gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
    assert ordered(replay['question'])==ordered(rec['question']), 'Instance differs from deterministic replay'
    v.independent(rec)

def native(rec):
    f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'all generated choices'} for a in f[':answer-field/choices']]}

def prepare_drafts():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
    assert all(sha(ROOT/p)==digest for p,digest in validation['sha256'].items())
    supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
    if isinstance(instances,dict):instances=[instances]
    assert isinstance(instances,list)
    used={task({'generation':{'parameters':p,'template':'single' if sid=='q-20407' else 'sum'}}) for sid,p in g.SOURCE_PARAMS.items()}
    used.add(task({'generation':{'parameters':{'a':[3,2]},'template':'single'}}))
    records=[];counts={level:0 for level in LEVELS}
    for rec in instances:
        check(rec);level=rec['question'][':question/difficulty'].split('/')[-1];t=task(rec)
        if t not in used and counts[level]<5:records.append(rec);counts[level]+=1;used.add(t)
    for level in LEVELS:
        for offset in range(200):
            if counts[level]==5:break
            rec=g.generate(level,1432901+offset);check(rec);t=task(rec)
            if t not in used:records.append(rec);counts[level]+=1;used.add(t)
        assert counts[level]==5, 'Bounded capability exhausted; no duplicate padding allowed'
    save(OUT/'drafts.json',records);save(OUT/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError') if isinstance(supplied,dict) else None})
    save(OUT/'native-input.json',[native(r) for r in instances+records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(OUT/'native-input.json'),str(OUT/'native-report.json')],check=True)
    save(HERE/'capabilities.json',{'generator_id':GENERATOR_UUID,'script':SCRIPT,'version':g.VERSION,'supported_levels':list(LEVELS),'exceptions':[],'sampling':'Bounded to documented integer/half-grid domains; complete authored method banks. Two opaque observed banks remain evidence-only.','difficulty_evidence':'classification.md','duplicate_equivalence':'Exact geometry modulo reflections/rotations, vector names, profile, seed and choice order; original and canonical tasks excluded.'})
    print('Prepared',counts,'distinct drafts',flush=True)
    return records

def publish(records,path):
    library=ImageLibrary(Path('/media/jake/SSD/EDB/math'),path);result=copy.deepcopy(records)
    for rec in result:
        q=rec['question']
        for key in (':question/problem',':question/worked-solution'):
            for source in re.findall(r'!\[\]\(([^)]+)\)',q[key]):
                asset=Path(source);assert asset.is_relative_to(HERE/'assets') and asset.is_file()
                relative=library.store(asset.read_bytes(),source);assert sha(Path('/media/jake/SSD/EDB/math')/relative)==library.saved[source]['sha256']
                q[key]=q[key].replace(source,relative)
    save(path/'asset-manifest.json',library.saved);save(path/'generated.json',result)
    return result

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()), 'Existing source question altered'
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());raw=json.loads((path/'selected-raw.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec,original in zip(records,raw):
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(rec['question']);check(original)
    for asset in json.loads((path/'asset-manifest.json').read_text()).values():assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
    assert not transaction([],kp,intent['generator_id'])
    verified={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',verified);return verified

def finish(path,gid,verified,inv):
    result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'capability_exceptions':[],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'legacy_unrated_questions_preserved':2,'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'asset-manifest.json',OUT/'native-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json')],'note':'All supported bands replenished with new validated gradable content. Existing unrated source records are retained unchanged; any remaining unclassified trigger refers to those legacy records.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
    if '--drafts-only' in sys.argv:prepare_drafts();return
    records=json.loads((OUT/'drafts.json').read_text());[check(r) for r in records]
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and all(sha(ROOT/p)==d for p,d in validation['sha256'].items())
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Acquiring application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.REC[':knowledge-point/id'];atomic_text(path/'before.edn',dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        # Confirm the immutable source math and metadata are still the captured evidence.
        def plain(x):
            if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
            if isinstance(x,list):return [plain(v) for v in x]
            return x if isinstance(x,(str,int,float,bool)) or x is None else str(x)
        current={q[':question/math-academy-id']:plain(q) for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
        def strip_extra(q,expected):
            if isinstance(expected,dict):return {k:strip_extra(q[k],v) for k,v in expected.items()}
            if isinstance(expected,list):
                # Source answer banks are ordered in immutable EDN traversal.
                return [strip_extra(a,c) for a,c in zip(q,expected)]
            return q
        assert all(strip_extra(current[sid],q)==q for sid,q in g.SOURCES.items()), 'Source evidence changed; reclassify'
        gen=kp.get(':knowledge-point/question-generator');registered=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b);assert len(registered)<=1
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else GENERATOR_UUID
        jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
        existing_levels={str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1] for q in kp[':knowledge-point/questions'] if q.get(':question/answer-fields') and all(f.get(':answer-field/correct') for f in q[':question/answer-fields']) and q.get(':question/worked-solution')}
        needed={level:jobs.get(level,{}).get('missing',0) if level in existing_levels else 5 for level in LEVELS}
        existing_ids={str(q[':question/id']) for q in kp[':knowledge-point/questions']};used=set()
        for prior in OUT.glob('basis-*/selected-raw.json'):
            for rec in json.loads(prior.read_text()):
                if rec['question'][':question/id'] in existing_ids:used.add(task(rec))
        selected=[];counts={l:0 for l in LEVELS}
        for rec in records:
            level=rec['question'][':question/difficulty'].split('/')[-1];t=task(rec)
            if counts[level]<needed[level] and t not in used and rec['question'][':question/id'] not in existing_ids:selected.append(rec);counts[level]+=1;used.add(t)
        assert counts==needed,'Fresh pool changed; regenerate distinct drafts at latest basis'
        ids=[uuid.UUID(r['question'][':question/id']) for r in selected];assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'identity-collisions',b) if ids else True
        identity=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-id',b);assert not identity or identity[0][0][':question-generator/script']==SCRIPT
        save(path/'selected-raw.json',selected);published=publish(selected,path)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':counts,'new_questions':len(selected),'source_evidence_unchanged':True,'inventory_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'new_supported_band_minimum':5,'distinctness':'geometry modulo reflections, rotations, names, seed and choice order; original and canonical geometries excluded'})
        forms=transaction(published,kp,gid);assert forms,'No new changes; use existing verification'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n';atomic_text(txpath,tx)
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);atomic_text(path/'preview.edn',r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'diagram-unit-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in selected],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(path/'commit-intent.json',intent)
        print('Submitting',len(selected),'questions at basis',b,flush=True);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()
