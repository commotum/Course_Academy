"""Add only validated distinct content, holding api.lock through receipt readback."""
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

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture'),str(HERE)]
import validate as v
g=v.g
from database import Database, StaleBasis
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment

KP=g.KP_ID
LEVELS=('easy','moderate')
# These source banks support corrected template replay, but their existing
# presentations do not meet the same reserve validation as new instances.
PRESENTATION_EXCLUSIONS={'q-108911':'Unbalanced prompt math delimiters and unterminated solution quote',
                         'q-108916':'Second worked-solution classification names Equation I instead of II'}
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
GENERATOR_UUID=g.uid('question-generator')
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'05b82113800b33be127066c08b4cb4b234e233c3c1ad3a03c6360ec1dcb26ea6'
OUT=HERE/'reference/replenishment'
OUT.mkdir(parents=True,exist_ok=True)
env=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=env['EDB_ENDPOINT']))
DB.env=env
QUERY=(HERE/'reference/initial/kp-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
HISTORY='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q _ _ true] [?kp :knowledge-point/questions ?q]]'''

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=90)
    result=json.loads(r.stdout);assert result['ok'] and result['data']['lineage']==LINEAGE
    save(path,result['data']);return result['data']

def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(v) for k,v in value.items()}
    if isinstance(value,list):return sorted((canonical(v) for v in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def ordered(q):
    q=canonical(q)
    q[':question/answer-fields'].sort(key=lambda f:g.LABELS.index(f[':answer-field/key']))
    return q

def math_fingerprint(q):
    # Read rendered math rather than trust seed or generator metadata.
    eqs=v.prompt_equations(q[':question/problem'])
    return g.digest(sorted(v.sp.srepr(v.sp.expand(e.subs(g.D,0)/v.sp.diff(e,g.D))) for e in eqs))

def validate_record(rec):
    v.inspect(rec)
    assert rec['generation']['eligible_for_learning']
    assert rec['generation']['version']==g.VERSION
    assert math_fingerprint(rec['question'])==rec['generation']['parameter_fingerprint']

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'shown-reserved',basis)}
    unavailable|={r[0] for r in DB.query(HISTORY,[KP,LEARNER],path,'historical-presentations',basis,history=True)}
    captured={q[':db/id']:q for q in g.SOURCE[':knowledge-point/questions']}
    known={r['question'][':question/id']:r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text())}
    rows={level:[] for level in LEVELS};gradable=[];excluded=[]
    for q in kp[':knowledge-point/questions']:
        difficulty=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
        if difficulty not in LEVELS or q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        if q.get(':question/math-academy-id') in PRESENTATION_EXCLUSIONS:
            excluded.append({'question_id':str(q[':question/id']),'source_id':q[':question/math-academy-id'],'reason':PRESENTATION_EXCLUSIONS[q[':question/math-academy-id']]})
            continue
        if q[':db/id'] in captured:
            assert canonical(q)==canonical(captured[q[':db/id']]), 'Source changed; reclassify'
            mid=q[':question/math-academy-id'];assert mid in g.CASES
            normalized=v.normalize_source(q)
            eqs=v.prompt_equations(q[':question/problem']);assert [v.independent_truth(e) for e in eqs]==v.flags(normalized)
            rec={'question':normalized,'knowledge_point':{'title':kp[':knowledge-point/title']},'generation':{'template':mid}}
        else:
            rec=known.get(str(q[':question/id']));assert rec, 'Unrecognized rated content must be validated'
            assert ordered(v.normalize_source(q))==ordered(rec['question'])
            validate_record(rec)
        rows[difficulty].append(q);gradable.append(rec)
    v.native_checks(gradable,path/'inventory-grading')
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({math_fingerprint(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for level,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_defective_source_presentations':excluded,'unrated_incomplete_and_canonical_excluded':True}
    save(path/'available-counts.json',result);return result

def transaction(records,kp,gid):
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
    else:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    attrs={a:str(name) for a,name in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added, 'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed, 'Unexpected entity/attribute mutation'

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    assert canonical({k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert ordered(v.normalize_source(q))==ordered(rec['question']);validate_record(rec)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    caps=json.loads((HERE/'capabilities.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_counts_after':after,'shortage_remaining':{**remaining,'hard':5},'unsupported_levels':['hard'],'unsupported_levels_filled':False,'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'generated.json',path/'preparation.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'native-report.json',path/'inventory-after.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'review.md',HERE/'frozen.json',HERE/'capabilities.json'] if p.exists()],'note':'Supported easy/moderate reserves replenished with mathematically distinct and native-graded checkbox questions. Hard is unsupported within this bounded package, remains explicitly short, and is not called filled. Two unrated incomplete sources remain unchanged.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
    frozen=json.loads((HERE/'frozen.json').read_text())
    for rel,h in frozen['sha256'].items():assert sha(ROOT/rel)==h, 'Frozen package changed'
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    inventory(OUT/'inventory-before-generation.json')
    preview=preview_executable(SimpleNamespace(math_root=Path(DB.env['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-under-lock.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        by_script=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-script',basis)
        assert len(by_script)<=1
        if by_script:gid=str(by_script[0][0][':question-generator/id'])
        matches=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert len(matches)<=1 and (not matches or matches[0][0][':question-generator/script']==SCRIPT)
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or by_script),'generator_sha256':sha(HERE.with_suffix('.py'))})
        available=counts(kp,path/'current-inventory',basis)
        needed={l:max(0,5-available['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={math_fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(math_fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:validate_record(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        records=[];added={l:0 for l in LEVELS}
        candidates=iter(instances)
        for rec in candidates:
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=math_fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:records.append(rec);used.add(fp);added[level]+=1
        for level in LEVELS:
            # 200 deterministic attempts; finite bounded failures stay explicit.
            for i in range(200):
                if added[level]>=needed[level]:break
                rec=g.generate(level,int(JOB.name[:8],16)+i);fp=math_fingerprint(rec['question'])
                if fp in used:continue
                validate_record(rec);records.append(rec);used.add(fp);added[level]+=1
        identities=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id']]+[f[':answer-field/id'] for f in rec['question'][':question/answer-fields']]+[a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        existing=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[identities],path,'identity-matches',basis) if identities else []
        assert not existing, 'Identity collision requires reconciliation'
        save(path/'generated.json',records)
        (path/'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        v.native_checks(records,path)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'source_basis':g.SOURCE_BASIS,'available_counts':available,'missing_by_level':needed,'new_by_level':added,'remaining_supported_shortage':{l:needed[l]-added[l] for l in LEVELS},'finite_attempt_bound':200,'source_evidence_preserved':True,'distinct_generated_tasks':len({math_fingerprint(r['question']) for r in records}),'asset_hashes':[]})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':available};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as file:file.write(tx);file.flush();os.fsync(file.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'bernoulli-recognition-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[rec['question'][':question/id'] for rec in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()
