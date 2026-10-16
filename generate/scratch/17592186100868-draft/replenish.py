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
# Load only the independent checker definitions; do not overwrite frozen review artifacts.
import types,itertools
from generator_publish import KP_QUERY, stable_identities
v=types.ModuleType('matrix_validation');v.__file__=str(HERE/'validate.py')
exec(compile((HERE/'validate.py').read_text().split('source_wrapper=')[0],v.__file__,'exec'),v.__dict__)
g=v.G
KP=g.KP['db_id']
LEVELS=('easy','moderate','hard')
KP_UUID=g.KP['id']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
CASES=json.loads((HERE/'source-cases.json').read_text())
REPLAYS={c['source_id']:g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']) for c in CASES}

LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'd07cd327139b7e6ccb5ee8a51a2c0254fb903b85b89cf64ff9e149da8f2c0631'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
RUNTIME=json.loads((OUT/'runtime.json').read_text())
NATIVE=Path(RUNTIME['inventory_binary'])
QUERY=KP_QUERY
DB.env=database_environment('math')

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
    # Ignore variable spelling, choice banks, solution, IDs, seed, and zero-multiplied entries.
    mats=v.matrices(q[':question/problem'])
    if len(mats)!=2:raise ValueError('Expected two input matrices')
    M=[[v.parse(c) for c in row] for row in mats[0]];V=[v.parse(row[0]) for row in mats[1]]
    expressions=[x if V[j]!=0 else v.S.Integer(0) for row in M for j,x in enumerate(row)]+V
    variables=sorted(set().union(*(x.free_symbols for x in expressions)),key=str)
    keys=[]
    for order in itertools.permutations(variables):
        subst=dict(zip(order,[v.S.Symbol('z'+str(i)) for i in range(len(order))]))
        keys.append(json.dumps([len(M),len(V),[v.S.srepr(v.S.expand(x.xreplace(subst))) for x in expressions]]))
    return min(keys)

def checks(r):
    out=[]
    for fi,f in enumerate(r['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            out += [{'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
        else:
            val=v.field_value(f);row=int(f[':answer-field/key'].split('-')[-1])-1;M,V=v.matrices(r['question'][':question/problem']);eq='+'.join('('+M[row][j]+')('+V[j][0]+')' for j in range(len(V)))
            out += [{'field_index':fi,'submitted':val,'expected':'accepted'},{'field_index':fi,'submitted':eq,'expected':'accepted'},{'field_index':fi,'submitted':v.S.latex(v.parse(val)+1),'expected':'rejected'}]
    return out


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
    known={r['question'][':question/id']:r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text())}
    rows={level:[] for level in LEVELS}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or not q.get(':question/difficulty') or not q.get(':question/worked-solution'):continue
        if not all(f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[])):continue
        mid=q.get(':question/math-academy-id')
        if mid in REPLAYS:
            rec=REPLAYS[mid]
            # Live source equality is checked before this count; replays have independent math and native validation.
        else:
            rec=known.get(str(q[':question/id']))
            if rec is None:continue
            assert normalize(q)==ordered(rec['question'])
        v.check(rec)
        rows[rec['question'][':question/difficulty'].split('/')[-1]].append(q)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for level,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'incomplete_unrated_sources_excluded':True}
    save(path/'available-counts.json',result);return result

def candidate_records():
    for seed in range(500):
        for level in LEVELS:
            yield g.generate(level,seed+2765)

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
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(rec['question']);v.check(rec)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified.get('available_counts_after',prep['available_counts']);remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels_filled':False,'capability_exceptions':[], 'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',path/'native-report.json',OUT/'review-recheck.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'hard-domain.json'] if p.exists()],'note':'All three levels supported. Unrated incomplete original q-13554 is preserved and excluded; its easy derivatives are authored from the canonical example. Finite normal hard domain has 240 tasks; no current shortage. No source or learner facts modified.'}
    result['generator_sha256']=sha(HERE.with_suffix('.py'))
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def main():
    review=json.loads((ROOT/'generate/runs/current/qa/17592186100868.json').read_text());assert review['parent_review']=='passed' and review['generator_sha256']==sha(HERE.with_suffix('.py'))
    for name,hash_value in review['root_artifact_hashes'].items():assert sha(HERE/name)==hash_value,name
    for name,hash_value in RUNTIME['hashes'].items():assert sha(Path(name))==hash_value,name
    for rec in REPLAYS.values():v.check(rec)
    save(OUT/'review-recheck.json',{'parent_review':'passed','frozen_hashes_verified':len(review['root_artifact_hashes'])+1,'current_runtime_hashes_verified':len(RUNTIME['hashes']),'source_replays_checked':len(REPLAYS),'prior_review':str(ROOT/'generate/runs/current/qa/17592186100868.json')})
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=json.loads((HERE/'source.json').read_text())['record'];current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:assert canonical(current[q[':question/math-academy-id']])==canonical(q),'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(captured[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        assert gen is None or gen[':question-generator/script']==SCRIPT
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        # Canonical uses image operands A=[[a,c],[b,d]], x=[3,2]. Evidence in classification/canonical-images.
        cp=copy.deepcopy(next(c['parameters'] for c in CASES if c['source_id']=='q-13554'));cp['vector']=[3,2]
        used.add(fingerprint(g.generate_easy(template='q-13554',parameters=cp)['question']))
        records=[];added={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:v.check(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        for rec in itertools.chain(instances,candidate_records()):
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                v.check(rec);rec=copy.deepcopy(rec);rec['question']=stable_identities(rec['question'],KP_UUID);records.append(rec);used.add(fp);added[level]+=1
            if all(added[l]>=needed[l] for l in LEVELS):break
        # Batch lookup stable question/field/answer identities before creating entities.
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]+[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]+[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing identities require reconciliation'
        save(path/'generated.json',records)
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in list(REPLAYS.values())+records]);subprocess.run([RUNTIME['grader_binary'],str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        native_report=json.loads((path/'native-report.json').read_text());assert native_report['documented_unresolved_checks']==0
        save(path/'mathematics.json',v.math_counts)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':[],'source_evidence_unchanged':True,'source_basis':2275})
        if '--prepare-only' in sys.argv:
            print(json.dumps({'basis':basis,'missing':needed,'generated':added,'directory':str(path)}),flush=True);return
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'matrix-column-variable-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
