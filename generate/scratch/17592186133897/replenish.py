"""Scoped Green area inventory publication through the existing EDB integration."""
import copy, fcntl, hashlib, json, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import validate as v
g = v.g
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
from image_library import ImageLibrary
KP = g.KP
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'59d4fc6185ed0055048743831491cde87578bad171be3386724d4185a23c08c3'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env = database_environment('math')
NATIVE = Path((HERE/'reference/initial/native-path.txt').read_text())
POOL = ROOT/'generate/scratch/17592186110754/check-pool'
QUERY = (HERE/'reference/source-query.edn').read_text()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p, b): return DB.query(QUERY, [KP], p, 'kp', b)[0][0]
def inventory(p):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=DB.env, text=True, capture_output=True, check=True, timeout=55)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(p, x['data'])
    return x['data']
def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']: f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q
def normalize(q):
    return ordered({':question/id':str(q[':question/id']), ':question/problem':q[':question/problem'], ':question/worked-solution':q[':question/worked-solution'], ':question/difficulty':str(q[':question/difficulty'][':db/ident']), ':question/answer-fields':[{':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':[{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]} for f in q[':question/answer-fields']]})
def segments(q):
    # Canonical example uses bold coordinate notation and \left interval delimiters.
    q = copy.deepcopy(q)
    s = q[':question/problem']
    s = re.sub(r'\\mathbf\{([rij])\}', r'\1', s).replace(r'\left','').replace(r'\right','').replace(r'\:', '')
    s = re.sub(r't\s*\\in', lambda m:r't\in', s)
    q[':question/problem'] = s
    return v.prompt_segments({'question':q})
def fingerprint(q):
    """Normalize segment speed, cyclic start and traversal reversal; ignore banks/IDs."""
    seg = segments(q)
    z = v.sp.Symbol('s', real=True)
    routes=[]
    for reverse in (False, True):
        route=[]
        for x,y,l,h in (list(reversed(seg)) if reverse else seg):
            param = h+(l-h)*z if reverse else l+(h-l)*z
            route.append(tuple(str(v.sp.trigsimp(v.sp.expand_trig(e.subs(v.t,param)))) for e in (x,y)))
        routes += [route[i:]+route[:i] for i in range(len(route))]
    return min(json.dumps(r) for r in routes)
def source_math(q):
    seg=segments(q)
    for (x,y,l,h),(nx,ny,nl,nh) in zip(seg,seg[1:]+seg[:1]):
        assert v.sp.simplify(x.subs(v.t,h)-nx.subs(v.t,nl))==0 and v.sp.simplify(y.subs(v.t,h)-ny.subs(v.t,nl))==0
    area=abs(v.sp.simplify(sum(v.sp.integrate(x*v.sp.diff(y,v.t)-y*v.sp.diff(x,v.t),(v.t,l,h))/2 for x,y,l,h in seg)))
    assert q.get(':question/worked-solution'), 'missing worked solution'
    for f in q[':question/answer-fields']:
        assert ':answer-field/correct' in f, 'missing correct designation'
        assert v.sp.simplify(v.expr(f[':answer-field/correct'][':answer/value'])-area)==0
        vals=[v.expr(a[':answer/value']) for a in f[':answer-field/choices']]
        assert len(set(vals))==len(vals)
    return str(area)
def publish(rec):
    rec=copy.deepcopy(rec)
    library=ImageLibrary()
    for key in (':question/problem', ':question/worked-solution'):
        def replace(m):
            relative=library.put_file(m[1]); assert sha(library.math_root/relative)==sha(Path(m[1]));return '![]('+relative+')'
        rec['question'][key]=re.sub(r'!\[\]\((.*?)\)',replace,rec['question'][key])
    return rec
def validate(rec):
    m=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
    assert rec['knowledge_point']['db_id']==KP and m['eligible_for_learning'] and not m['evidence_only'] and level in LEVELS
    replay=g.generate(level,m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
    assert ordered(rec['question']) in (ordered(replay['question']),ordered(publish(replay)['question']))
    assert replay['generation']==m
    v.check_record(rec)
def native(records,p):
    p.mkdir(parents=True,exist_ok=True)
    checks=[]
    for r in records:
        for f in r['question'][':question/answer-fields']:
            x=copy.deepcopy(r);x['question'][':question/answer-fields']=[copy.deepcopy(f)]
            checks.append({'label':str(r['question'][':question/id'])+f[':answer-field/key'],'record':x,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete native bank'} for a in f[':answer-field/choices']]})
    save(p/'input.json',checks)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,capture_output=True,text=True,timeout=55)
def counts(kp,b,p):
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    seen={r[0] for r in shown+reserved}
    entities={};enums={}
    def enum(x):
        name=str(x[':db/ident']).lstrip(':')
        if name not in enums:
            e=len(enums)+1;enums[name]=e;entities[str(e)]={'db/ident':name}
        return enums[name]
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=r
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id']);field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f[':answer-field/choices']]};entities[str(f[':db/id'])]=field
            if ':answer-field/correct' in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            for a in f[':answer-field/choices']:entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    save(p/'snapshot.json',{'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)})
    subprocess.run([str(POOL),str(p/'snapshot.json'),str(p/'pool.json')],check=True,capture_output=True,text=True,timeout=55)
    pool=json.loads((p/'pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    levels={l:set() for l in LEVELS};excluded=[];checked=[];checks=[]
    known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    for q in kp[':knowledge-point/questions']:
        try:
            assert q[':db/id'] in ids,'native pool excludes ungradable, shown or reserved'
            # Retain the source sign error, but do not count its worked solution as validated.
            assert q.get(':question/math-academy-id')!='q-42239','source Green theorem substitution equality omits orientation minus sign'
            area=source_math(q);fp=fingerprint(q);l=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
            r=known.get(str(q[':question/id']))
            if r:assert normalize(q)==ordered(r['question']);validate(r)
            else:r={'question':normalize(q),'generation':{'template':'current-source'}}
            checked.append(r);levels[l].add(fp);checks.append({'id':str(q[':question/id']),'area':area,'level':l,'fingerprint':fp})
        except (AssertionError,ValueError,KeyError) as e:excluded.append({'id':str(q[':question/id']),'reason':str(e)})
    native(checked,p/'grading')
    result={'basis':b,'levels':{l:len(levels[l]) for l in LEVELS},'validated':checks,'excluded':excluded,'native_pool':pool,'deduplication':'curve and exact area task; normalized segment speeds, cyclic starts and reversed traversal; no seed, bank or identity'}
    save(p/'counts.json',result);return result

def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,p,source):
    attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution/retraction'
        name=str(attrs[a])
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

def verify(p,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_report(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
    gen=kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question'])
        validate(r)
        for path in re.findall(r'!\[\]\((.*?)\)',q[':question/problem']):
            assert (Path('/media/jake/SSD/EDB/math')/path).is_file()
    assert not transaction([],kp,intent['generator_id'])
    after=counts(kp,b,p/'readback')
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after}
    save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_counts_after':after['levels'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':json.loads((HERE/'capabilities.json').read_text()),'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'inventory-after.json',HERE/'reference/current-classification.md',HERE/'validation.json',HERE/'freeze.json'] if f.exists()],'note':'Only new generated questions and generator registration were asserted. Source questions, canonical example and learner history are unchanged. The application may retain an unclassified job for incomplete legacy source questions; these have not been relabeled or counted.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','shortage_remaining')}),flush=True)

def candidates():
    b=DB.basis();p=OUT/'pre-generation';kp=read(p,b);c=counts(kp,b,p)
    needed={l:max(0,5-c['levels'][l]) for l in LEVELS}
    save(p/'inventory.json',inventory(p/'application-inventory.json'))
    print(json.dumps({'basis':b,'available':c['levels'],'needed':needed}),flush=True)
    supplied_path=JOB.with_suffix('.generated')
    supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
    if isinstance(instances,dict):instances=[instances]
    for r in instances:validate(r)
    save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
    used={fingerprint(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]}
    records=[];added={l:0 for l in LEVELS};mathematical=set()
    for l in LEVELS:
        families=[f for f,level in g.FAMILY_LEVEL.items() if level==l]
        for r in instances:
            if added[l]>=needed[l]:break
            if r['question'][':question/difficulty']!=':question.difficulty/'+l:continue
            fp=fingerprint(r['question'])
            mf=r['generation']['mathematical_fingerprint']
            if fp in used or mf in mathematical:continue
            validate(r);used.add(fp);mathematical.add(mf);records.append(publish(r));added[l]+=1
        for seed in range(200):
            if added[l]>=needed[l]:break
            r=g.generate(l,seed+16133897,template=families[seed%len(families)])
            fp=fingerprint(r['question'])
            mf=r['generation']['mathematical_fingerprint']
            if fp in used or mf in mathematical:continue
            validate(r);used.add(fp);mathematical.add(mf);records.append(publish(r));added[l]+=1
        assert added[l]==needed[l], 'Bounded family exhausted; document finite-limit before submission'
    native(records,p/'selected-grading')
    save(OUT/'candidates.json',records)
    return records

def main():
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert all(sha(ROOT/p)==digest for p,digest in freeze['sha256'].items())
    assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    # Recover a saved durable request before any new generation or changed intent.
    pending=sorted(p for p in OUT.glob('basis-*') if (p/'commit-intent.json').exists())
    records=None if pending else candidates()
    lockpath=ROOT/'.local/learning/requests/math/api.lock'
    with lockpath.open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in pending:
            intent=json.loads((p/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
        p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
        initial=loads((OUT/'pre-generation/kp.edn').read_text())[0][0]
        assert kp==initial,'KP changed after generation; revalidate against new evidence'
        (p/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.RECORD[':knowledge-point/id']),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT
            gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]) for l in LEVELS};selected=[]
        used={fingerprint(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]}
        for r in records:
            l=r['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(r['question'])
            if needed[l] and fp not in used:selected.append(r);needed[l]-=1;used.add(fp)
        assert not any(needed.values()),'Fresh inventory changed; return to generation'
        records=selected
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records)
        assets=[{'path':path,'sha256':sha(Path('/media/jake/SSD/EDB/math')/path)} for r in records for path in re.findall(r'!\[\]\((.*?)\)',r['question'][':question/problem'])]
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'asset_hashes':assets,'mathematics_validated':True,'actual_grader_validated':True,'generator_sha256':sha(HERE.with_suffix('.py'))})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();__import__('os').fsync(f.fileno())
        pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55)
        (p/'preview.edn').write_text(pr.stdout);pr=loads(pr.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'green-area-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(lockpath)}
        save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()

