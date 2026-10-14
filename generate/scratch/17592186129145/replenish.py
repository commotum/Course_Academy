"""Additive graph-polynomial replenishment using native inventory and EDB integration."""
import argparse, copy, fcntl, hashlib, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment,build_learning
import validate as v
g=v.g
KP=g.KP_ID
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.SOURCE['lineage']
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'27e0e052e14fcac03557660751562c50dad4a7108e12bb1277657df698c136ff'
OUT=HERE/'reference/replenishment'
LEVELS=('easy','moderate','hard')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env=database_environment('math')
QUERY=(HERE/'reference/source-query.edn').read_text()
UNAVAILABLE='''[:find ?q :in $ ?learner ?kp
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


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    return str(value) if isinstance(value,uuid.UUID) else value

def normalize(q):
    result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    level=q[':question/difficulty'];result[':question/difficulty']=str(level[':db/ident']) if isinstance(level,dict) else level
    result[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        typ=f[':answer-field/type'];correct=f[':answer-field/correct']
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(typ[':db/ident']) if isinstance(typ,dict) else typ,':answer-field/correct':[':answer/id',str(correct[':answer/id']) if isinstance(correct,dict) else correct[1]],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']) if isinstance(a[':answer/type'],dict) else a[':answer/type'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    result[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in result[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return result

def math_fp(poly):
    sig,sign=v.sig(poly)
    task={'roots':[r for r,c in sig],'categories':[c for r,c in sig],'leading_sign':sign,'assessed_information':'unscaled graph local root behavior'}
    return hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()

def local_record(r):
    r=copy.deepcopy(r)
    for published in r['generation'].get('published_assets',{}).values():
        assert sha(Path(DB.env['EDB_MATH_ROOT'])/published['reference'])==published['sha256']
        for k in (':question/problem',':question/worked-solution'):
            r['question'][k]=r['question'][k].replace(published['reference'],published['local'])
    return r

def validate(r):
    local=local_record(r)
    assert local['knowledge_point']['db_id']==KP and local['knowledge_point']['id']==g.KP_UUID
    assert local['generation']['eligible_default'] and not local['generation']['evidence_only']
    v.check(local)
    gen=local['generation'];level=local['question'][':question/difficulty'].split('/')[-1]
    replay=g.generate(level,seed=gen['seed'],profile=gen['profile'],parameters=gen['parameters'])
    assert normalize(local['question'])==normalize(replay['question'])
    f=local['question'][':question/answer-fields'][0]
    key=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert math_fp(v.read(key))==gen['math_fingerprint']
    return True

def native(r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':str(r['question'][':question/id']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual learner radio grading'} for a in f[':answer-field/choices']]}

def inventory(binary,path):
    proc=subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    response=json.loads(proc.stdout);assert response['ok'] and response['data']['lineage']==LINEAGE
    save(path,response['data']);return response['data']

def validate_sources(kp):
    def source_shape(value):
        if isinstance(value,dict):
            return {k:source_shape(z) for k,z in value.items()
                    if not k.startswith(':knowledge-point/_')
                    and not (k==':db/id' and ':db/ident' in value)}
        if isinstance(value,(list,tuple)):return [source_shape(z) for z in value]
        return value
    captured=g.SOURCE['record']
    current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    old={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
    assert canonical(source_shape(current))==canonical(source_shape(old)),'Source changed: reopen classification'
    assert canonical(source_shape(kp[':knowledge-point/canonical-example']))==canonical(source_shape(captured[':knowledge-point/canonical-example']))

def source_fp(q):
    sid=q.get(':question/math-academy-id')
    if sid in g.DATA:
        level,roots,mults,c=g.DATA[sid]
        return math_fp(g.polynomial(c,roots,mults))
    final=re.findall(r'\$(y\s*=.*?)\$',q[':question/worked-solution'])[-1].rstrip('.')
    return math_fp(v.read(final))

def counts(kp,path,basis,records=()):
    unavailable={r[0] for r in DB.query(UNAVAILABLE,[LEARNER,KP],path,'unavailable',basis)}
    known={r['question'][':question/id']:r for r in records}
    for manifest in OUT.glob('basis-*/generated.json'):
        for r in json.loads(manifest.read_text()):known[r['question'][':question/id']]=r
    used={source_fp(kp[':knowledge-point/canonical-example'])};available={l:{} for l in LEVELS};excluded=[];fixtures=[]
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id');ident=str(q[':question/id'])
        if sid in g.QS:fp=source_fp(q)
        else:
            assert ident in known,'Unknown generated content requires reconciliation'
            r=known[ident];assert normalize(q)==normalize(r['question']);validate(r);fp=r['generation']['math_fingerprint']
        used.add(fp)
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        fields=q.get(':question/answer-fields',[])
        if level not in LEVELS or not q.get(':question/worked-solution') or not fields or not all(f.get(':answer-field/correct') and f.get(':answer-field/choices') for f in fields):
            excluded.append({'id':q[':db/id'],'source_id':sid,'reason':'unrated or incomplete'});continue
        if sid:
            replay=g.generate(level,profile=sid,parameters={'h':0,'s':1,'v':'1'});v.check(replay)
            f=fields[0];assert v.read(f[':answer-field/correct'][':answer/value'])==g.polynomial(g.DATA[sid][3],g.DATA[sid][1],g.DATA[sid][2])
        if q[':db/id'] not in unavailable and not q.get(':knowledge-point/_canonical-example'):
            available[level][fp]=ident
            # Native fixture uses existing UUIDs, answer values and correct designation.
            fixtures.append(native({'question':normalize_for_native(q)}))
    if fixtures:
        save(path/'available-native-input.json',fixtures)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True,capture_output=True)
    result={'basis':basis,'available_by_level':{l:len(a) for l,a in available.items()},'available_question_ids':{l:sorted(a.values()) for l,a in available.items()},'excluded_sources':excluded,'shown_or_reserved_ids':sorted(unavailable),'distinctness':'Root locations, simple/even/odd-multiple categories and leading sign; excludes seed, identity, option order, amplitude, exact exponent within category.'}
    save(path/'validated-inventory.json',result);return result,used

def normalize_for_native(q):
    return normalize(q)
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

def check_datoms(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')}|{':answer-field/'+s for s in ('id','key','type','choices','correct')}|{':answer/'+s for s in ('id','type','value')}|{':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected existing entity change'


def verify(path,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:z for k,z in before.items() if k not in omit}=={k:z for k,z in kp.items() if k not in omit}
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        validate(r);q=byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q)==normalize(r['question'])
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    assert not transaction([],kp,intent['generator_id'])
    stock,_=counts(kp,path/'post-inventory',basis,records)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_existing_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'inventory':stock}
    save(path/'verification.json',result);return result

def finish(path,intent,verified,binary):
    inv=inventory(binary,path/'inventory-after.json');kp=read_kp(path/'final-inventory',inv['basis']);validate_sources(kp)
    stock,_=counts(kp,path/'final-inventory',inv['basis'])
    shortage={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
    caps=json.loads((HERE/'validation.json').read_text())['finite_mathematical_tasks']
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['new_by_level'],'supported_levels':list(LEVELS),'hard_is_authored_extension':True,'available_by_level':stock['available_by_level'],'shortage_remaining':shortage,'unsupported_levels_filled':False,'finite_distinct_task_capacity':caps,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':[{'type':'legacy-source-omissions','filled':False,'sources':stock['excluded_sources'],'reason':'Original unrated/fieldless records remain excluded and unchanged; generated completions do not revise originals.'}]+([{'type':'finite-domain','filled':False,'shortage':shortage,'capacity':caps,'reason':'All bounded validated distinct task slots exhausted.'}] if any(shortage.values()) else []),'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'final-inventory/validated-inventory.json',HERE/'validation.json',HERE/'reference/frozen-generator-validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md') if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions_by_level','available_by_level','shortage_remaining','remaining_jobs')}),flush=True)

def main():
    a=argparse.ArgumentParser();a.add_argument('--prepare-only',action='store_true');args=a.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    qa=json.loads((ROOT/'generate/runs/current/qa'/f'{KP}.json').read_text())
    assert qa['parent_review']=='passed' and qa['generator_sha256']==sha(HERE.with_suffix('.py'))
    assert all(sha(ROOT/p)==h for p,h in qa['root_artifact_hashes'].items())
    save(HERE/'reference/frozen-generator-validation.json',qa)
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report),binary);return
        inv=inventory(binary,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);validate_sources(kp)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n');stock,used=counts(kp,path,b)
        needed={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b);assert len(registered)<=1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        collisions=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not collisions or collisions[0][0][':question-generator/script']==SCRIPT
        selected={l:0 for l in LEVELS};records=[];checked=[]
        supplied_path=JOB.with_suffix('.generated');supplied_exists=supplied_path.exists()
        supplied=json.loads(supplied_path.read_text()) if supplied_exists else {}
        instances=supplied.get('instances',[]);assert isinstance(instances,list)
        def consider(r):
            validate(r);checked.append(r)
            l=r['question'][':question/difficulty'].split('/')[-1];fp=r['generation']['math_fingerprint']
            if selected[l]<needed[l] and fp not in used:records.append(copy.deepcopy(r));used.add(fp);selected[l]+=1
        for r in instances:consider(r)
        for l in LEVELS:
            profiles=[sid for sid,data in g.DATA.items() if data[0]==l and sid not in g.RAW_COLLISION_PROFILES]
            for h in range(-3,4):
                for s in ([1] if l=='hard' else [1,2]):
                    for sid in profiles:
                        if selected[l]>=needed[l]:break
                        consider(g.generate(l,seed=int(JOB.name[:8],16),profile=sid,parameters={'h':h,'s':s,'v':'1'}))
        library=ImageLibrary();assets=[]
        for r in records:
            local=re.search(r'!\[\]\((.*?)\)',local_record(r)['question'][':question/problem']).group(1)
            ref=library.put_bytes(Path(local).read_bytes());assert sha(library.math_root/ref)==sha(local)
            for k in (':question/problem',':question/worked-solution'):r['question'][k]=local_record(r)['question'][k].replace(local,ref)
            asset={'local':local,'reference':ref,'sha256':sha(local)};r['generation']['published_assets']={'prompt':asset};assets.append(asset)
        save(path/'generated.json',records)
        save(JOB.with_suffix('.generated'),{'request':json.loads(JOB.with_suffix('.json').read_text())['request'],'instances':records,'preparation_basis':b})
        save(path/'native-input.json',[native(r) for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        ids=[uuid.UUID(qid) for r in records for qid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'generated-identities',b)
        save(path/'preparation.json',{'basis':b,'original_job_basis':2188,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'unproduced_by_level':{l:needed[l]-selected[l] for l in LEVELS},'available_before':stock,'source_evidence_unchanged':True,'asset_hashes':assets,'supplied_generated_exists':supplied_path.exists(),'supplied_instances_validated':len(instances),'generator_sha256':sha(HERE.with_suffix('.py'))})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'new_by_level':selected};save(path/'verification.json',{'passed':True,'no_changes':True,**verified});finish(path,{'generator_id':gid},verified,binary);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        proc=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(proc.stdout);pr=loads(proc.stdout);assert not pr[':edb/committed'] and pr[':edb/db-before-t']==b
        check_datoms(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        print(json.dumps({'prepared_basis':b,'needed':needed,'selected':selected,'directory':str(path)}),flush=True)
        if args.prepare_only:return
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'factored-polynomial-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report),binary)
if __name__=='__main__':main()
