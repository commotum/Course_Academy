"""Scoped circulation inventory, additive EDB publication and exact receipt recovery."""
import copy,fcntl,hashlib,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate as v;g=v.g
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.WRAPPER['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'63c2d0c10bf1af79b002328dc80d2599213b010cd841d9194c305233e72a4358'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY=(HERE/'reference/source-query.edn').read_text()
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7';POOL=ROOT/'generate/scratch/17592186110754/check-pool'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def inventory(p):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def fingerprint(q):
    values,signs=v.read_prompt(q[':question/problem'])
    return json.dumps([str(values[0]),signs[0],sorted((str(a),b) for a,b in zip(values[1:],signs[1:]))])
def publish(rec):
    rec=copy.deepcopy(rec);lib=ImageLibrary()
    for key in (':question/problem',':question/worked-solution'):
        def replace(m):
            original=Path(m[1]); original=original if original.is_absolute() else lib.math_root/original
            rel=lib.put_file(original);assert sha(original)==sha(lib.math_root/rel);return '![]('+rel+')'
        rec['question'][key]=re.sub(r'!\[\]\((.*?)\)',replace,rec['question'][key])
    return rec
def validate(rec):
    m=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and m['eligible_for_learning'] and not m['evidence_only']
    replay=g.generate(level,m['seed'],template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
    assert m==replay['generation']
    assert ordered(rec['question']) in (ordered(replay['question']),ordered(publish(replay)['question']))
    v.check_record(rec);v.check_prose(rec)
def native(records,p):
    p.mkdir(parents=True,exist_ok=True);fixtures=[]
    for r in records:
        f=r['question'][':question/answer-fields'][0]
        fixtures.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete native radio bank'} for a in f[':answer-field/choices']]})
    save(p/'input.json',fixtures)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,capture_output=True,text=True,timeout=55)
def source_math(q):
    values,signs=v.read_prompt(q[':question/problem']);total=sum(a*b for a,b in zip(values,signs))
    sol=q[':question/worked-solution'];rows=sol.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\')
    assert len(rows)==3
    symbolic=rows[0].split('& =',1)[1].strip()
    terms=re.findall(r'([+-]?)\{∮\}_\{\{C\}_\{([123])\}\}F\\cdot \\text\{d\}r',symbolic)
    assert [int(i) for _,i in terms]==[1,2,3] and [-1 if op=='-' else 1 for op,_ in terms]==signs
    text=rows[1].split('& =',1)[1].strip();matcher=re.compile(r'([+-]?)(\(-?\d+\)|-?\d+)');pos=0;parts=[]
    while pos<len(text):
        m=matcher.match(text,pos);assert m,(text,pos);parts.append((-1 if m[1]=='-' else 1)*v.parse(m[2]));pos=m.end()
    assert parts==[a*b for a,b in zip(values,signs)]
    assert v.parse(rows[-1].split('& =',1)[1].strip().removesuffix('.'))==total
    f=q[':question/answer-fields'][0];bank=[v.parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(bank))==5 and bank.count(total)==1 and v.parse(f[':answer-field/correct'][':answer/value'])==total
    return str(total)

def normalize(q):
    return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def scoped(kp,b,seen):
    entities={};enums={}
    def enum(value):
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            e=len(enums)+1;enums[name]=e;entities[str(e)]={'db/ident':name}
        return enums[name]
    for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
        r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=r
        if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
        for f in q.get(':question/answer-fields',[]):
            r['question/answer-fields'].append(f[':db/id']);field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=field
            if ':answer-field/correct'in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
            for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
    entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}

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

def counts(kp,b,p):
    shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
    reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
    save(p/'scoped-snapshot.json',scoped(kp,b,{r[0] for r in shown+reserved}))
    subprocess.run([str(POOL),str(p/'scoped-snapshot.json'),str(p/'pool.json')],check=True,capture_output=True,text=True,timeout=55)
    pool=json.loads((p/'pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs}
    levels={l:set() for l in LEVELS};records=[];excluded=[];checks=[]
    known={r['question'][':question/id']:r for path in OUT.glob('basis-*/generated.json') for r in json.loads(path.read_text())}
    for q in kp[':knowledge-point/questions']:
        if ':question/math-academy-id' in q:total=source_math(q)
        else:
            r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);validate(r);total=r['generation']['total']
        fp=fingerprint(q);l=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        checks.append({'id':str(q[':question/id']),'level':l,'total':total,'fingerprint':fp})
        if q[':db/id'] not in ids:excluded.append({'id':str(q[':question/id']),'reason':'native pool excludes canonical, unrated, ungradable, shown or reserved'});continue
        levels[l].add(fp);records.append({'question':normalize(q)})
    native(records,p/'grading')
    result={'basis':b,'levels':{l:len(x) for l,x in levels.items()},'checks':checks,'excluded':excluded,'native_pool':pool,'deduplication':'outer operand/orientation and unordered hole operand/orientation pairs; ignores bank, diagram, identity, seed and option order'}
    save(p/'counts.json',result);return result

def verify(p,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    exclude={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:v for k,v in kp.items() if k not in exclude}=={k:v for k,v in before.items() if k not in exclude}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
        for asset in re.findall(r'!\[\]\((.*?)\)',q[':question/problem']+q[':question/worked-solution']):
            path=Path('/media/jake/SSD/EDB/math')/asset;assert path.is_file() and sha(path)==path.stem
    assert not transaction([],kp,intent['generator_id'])
    after=counts(kp,b,p/'readback');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
    c=verified['available_counts_after'];remaining={l:max(0,5-c['levels'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'shortage_remaining':remaining,'available_counts_after':c['levels'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':[],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'inventory-after.json',HERE/'reference/current-source-addendum.md',HERE/'reference/package-validation.json',HERE/'validation.json']]}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
    qa=json.loads((ROOT/'generate/runs/current/qa/17592186133899.json').read_text());assert qa['parent_review']=='passed' and sha(HERE.with_suffix('.py'))==qa['generator_sha256']
    assert all(sha(ROOT/p)==d for p,d in qa['root_artifact_hashes'].items())
    save(HERE/'reference/package-validation.json',{'parent_review':'passed','all_frozen_artifact_hashes_verified':True,'generator_sha256':sha(HERE.with_suffix('.py')),'qa_report':'generate/runs/current/qa/17592186133899.json','finite_meaningful_variation':json.loads((HERE/'validation.json').read_text())['finite_meaningful_variation']})
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
        assert kp==loads((HERE/'reference/initial/kp.edn').read_text())[0][0],'Source or generator changed: reclassify'
        (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['levels'][l]) for l in LEVELS};print(json.dumps({'basis':b,'available':c['levels'],'needed':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:validate(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        # Canonical values 10,-8,3; orientations reverse outer and C2, retain C3.
        used.add(json.dumps(['10',-1,sorted([('-8',-1),('3',1)])]))
        records=[];added={l:0 for l in LEVELS};seed=int(JOB.name[:8],16)
        for l in LEVELS:
            candidates=[r for r in instances if r['question'][':question/difficulty']==':question.difficulty/'+l]
            for n in range(1000):
                if added[l]>=needed[l]:break
                rec=candidates[n] if n<len(candidates) else g.generate(l,seed=seed+n)
                fp=fingerprint(rec['question'])
                if fp in used:continue
                validate(rec);rec=publish(rec);validate(rec);records.append(rec);used.add(fp);added[l]+=1
            assert added[l]==needed[l], 'Bounded sampling exhausted: retain explicit shortage'
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)));native(records,p/'selected-grading')
        assets=sorted(set(a for r in records for key in (':question/problem',':question/worked-solution') for a in re.findall(r'!\[\]\((.*?)\)',r['question'][key])))
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'asset_hashes':{a:sha(Path('/media/jake/SSD/EDB/math')/a) for a in assets},'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'available_counts_after':c};finish(p,gid,verified,inv);return
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'circulation-holes-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()
