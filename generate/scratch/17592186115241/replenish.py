"""KP-scoped inventory replenishment through existing EDB transport and app lock."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,tempfile,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(HERE));import validate as v;g=v.g
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment
from inventory_jobs import save
KP=g.KP;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LEVELS=('easy','moderate','hard')
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'a29b1bebe0e27fe3c3ee546a4b0586550cd3d4a431c759038e1941d0bcd11826'
OUT=HERE/'reference/replenishment';LOCK=ROOT/'.local/learning/requests/math/api.lock'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
BUILD=json.loads((OUT/'native-build.json').read_text());NATIVE=Path(BUILD['learning'])
QUERY=(HERE/'source-query.edn').read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,b):return DB.query(QUERY,[[KP]],p,'kp',b)[0][0]
def inventory(p):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    inv=json.loads(r.stdout);assert inv['ok'] and inv['data']['lineage']==LINEAGE;save(p,inv['data'])
    with tempfile.TemporaryDirectory(prefix='kp-17592186115241-') as tmp:
        snapshot=Path(tmp)/'snapshot.json'
        r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"export-test-snapshot"}',env={**DB.env,'LEARNING_SNAPSHOT_PATH':str(snapshot)},capture_output=True,text=True,check=True,timeout=55)
        assert json.loads(r.stdout)['ok']
        countfile=p.with_name(p.stem+'-counts.json')
        subprocess.run([str(OUT/'inspect-inventory'),str(snapshot),str(countfile)],check=True,timeout=55)
    counts=json.loads(countfile.read_text());assert counts['basis']==inv['data']['basis']==DB.basis(),'Basis advanced; repeat captured reads'
    return inv['data'],counts

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def normalize(q):
    return ordered({':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':[{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]} for f in q[':question/answer-fields']]})

def matrix_from_prompt(text):
    text=v.algebra_layout(text)
    blocks=[m[1] for m in g.INNER.finditer(text) if '=' in m[1]]
    assert len(blocks)==1
    eqs=[]
    for line in blocks[0].split(chr(92)*2):
        left,right=line.replace('&','').split('=')
        eqs.append(v.sp.expand(g.load_expr(left)-g.load_expr(right)))
    used=set().union(*(e.free_symbols for e in eqs));assert used and used<=set(g.VARS)
    n=max(g.VARS.index(x) for x in used)+1
    return v.sp.Matrix([[e.coeff(x) for x in g.VARS[:n]]+[-e.subs({x:0 for x in g.VARS})] for e in eqs])

def fingerprint(q):
    # Same affine solution set is one task despite row scaling, order, redundant
    # rows, seed, choice order, bank profile, formatting or identity changes.
    try:M=matrix_from_prompt(q[':question/problem'])
    except (AssertionError,ValueError):
        # Canonical prompt is mathematical SVG; first printed solution matrix
        # is its captured augmented matrix, independently inspected in extraction.
        assert q.get(':question/math-academy-id')==g.RECORD[':knowledge-point/canonical-example'][':question/math-academy-id']
        matrices=v.printed_matrices(q[':question/worked-solution']);assert matrices
        M=matrices[0]
    canonical=[row for row in g.serialize(M.rref()[0]) if any(v.sp.Rational(x)!=0 for x in row)]
    return g.fingerprint({'rref':canonical,'n':M.cols-1})

def engine_case(label,r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual learner grading of every owned radio answer'} for a in f[':answer-field/choices']]}


def native(records,p):
    p.mkdir(parents=True,exist_ok=True);save(p/'input.json',[engine_case(r['question'][':question/id'],r) for r in records])
    subprocess.run([str(OUT/'check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,timeout=55)
    report=json.loads((p/'report.json').read_text());assert report['documented_unresolved_checks']==0

def source_check(kp,p,b):
    captured=loads((OUT/'initial/kp.edn').read_text())[0][0]
    # Retain the fresh source snapshot including later formatting and q-42040 completion.
    assert {q[':db/id']:q for q in captured[':knowledge-point/questions']}=={q[':db/id']:q for q in kp[':knowledge-point/questions']},'Source evidence changed; reclassify'
    assert captured[':knowledge-point/canonical-example']==kp[':knowledge-point/canonical-example']
    assert str(kp[':knowledge-point/id'])==g.RECORD[':knowledge-point/id']

def validated_counts(kp,raw):
    ids=set(raw['available_questions']);seen={l:set() for l in LEVELS};excluded=[];records=[]
    known={r['question'][':question/id']:r for path in OUT.glob('basis-*/generated.json') for r in json.loads(path.read_text())}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] not in ids:
            excluded.append({'id':str(q[':question/id']),'source_id':q.get(':question/math-academy-id'),'reason':'previously shown/reserved' if q[':db/id'] in raw['excluded_seen_or_reserved'] else 'unrated or incomplete; retained unchanged'})
            continue
        l=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        mid=q.get(':question/math-academy-id')
        if mid in g.QUESTIONS:
            r=g.generate('easy',profile=mid,parameters={'scale':1,'offsets':[0]*(len(g.BASE[mid][0])-1)})
            r['question']=normalize(q)
        else:
            r=copy.deepcopy(known[str(q[':question/id'])]);assert normalize(q)==ordered(r['question'])
            r['question']=normalize(q)
        v.check_record(r);records.append(r);seen[l].add(fingerprint(q))
    # Native pool already excludes unrated, incomplete, canonical, seen/reserved.
    return {'available_by_level':{l:len(seen[l]) for l in LEVELS},'excluded':excluded,'native_available_by_level':raw['available_by_level'],'validated_questions':len(records)}


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

def check_datoms(report,p,source):
    attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=str(attrs[a])
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

def verify(p,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_datoms(report,p/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items());skip={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in skip}=={k:v for k,v in kp.items() if k not in skip}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
    used={fingerprint(q) for q in old.values()};used.add(fingerprint(before[':knowledge-point/canonical-example']))
    readback_records=[]
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);v.check_record(r)
        fp=fingerprint(q);assert fp not in used;used.add(fp)
        readback_records.append({'question':normalize(q),'knowledge_point':r['knowledge_point'],'generation':r['generation']})
    native(readback_records,p/'readback/grading');assert transaction([],kp,intent['generator_id'])==[]
    inv,raw=inventory(p/'inventory-after.json');counts=validated_counts(kp,raw)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':counts,'inventory_recheck_basis':inv['basis']};save(p/'verification.json',result)
    return result

def finish(p,intent,verified):
    prep=json.loads((p/'preparation.json').read_text());after=verified['available_counts_after'];remaining={l:max(0,5-after['available_by_level'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':17592186048445,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'preparation_basis':intent['basis'],'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy'],'authored_levels':['moderate','hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'remaining_shortages':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after,'source_questions_and_learner_history_preserved':True,'inventory_recheck_basis':verified['inventory_recheck_basis'],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'generated.md',p/'inventory-after.json',p/'inventory-after-counts.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',OUT/'initial/current-source-bank-replay.json',OUT/'initial/current-native-report.json',HERE/'reference-validation.log',OUT/'native-build.json',OUT/'freeze.json'] if f.exists()],'note':'Only distinct validated gradable affine solution sets counted. Incomplete source remains excluded and preserved. Moderate and hard are documented curriculum-bounded authored levels. App api.lock held through basis recheck, submission and readback. Exact request and receipt retained.'}
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','new_by_level','verified_commit_basis','remaining_shortages')},indent=2),flush=True)

def main():
    for f,expected in BUILD['executables'].items():assert sha(Path(f))==expected
    frozen=json.loads((OUT/'freeze.json').read_text());assert frozen['passed']
    for rel,expected in frozen['hashes'].items():assert sha(ROOT/rel)==expected
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        # Resolve an exact saved request before planning any new work.
        for p in sorted(OUT.glob('basis-*')):
            if not (p/'commit-intent.json').exists():continue
            intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            assert intent['exact_edn']==(p/'transaction.edn').read_text() and intent['sha256']==sha(p/'transaction.edn')
            assert inventory(p/'recovery-inventory.json')[0]['lineage']==intent['lineage']
            finish(p,intent,verify(p,intent,DB._commit(intent,p/'transaction.edn',p)));return
        inv,raw=inventory(OUT/'inventory-before.json');b=inv['basis'];p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True)
        for name in ('inventory-before.json','inventory-before-counts.json'):(p/name).write_bytes((OUT/name).read_bytes())
        kp=read(p,b);source_check(kp,p,b);(p/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.RECORD[':knowledge-point/id']),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
        counts=validated_counts(kp,raw);needed={l:max(0,5-counts['available_by_level'][l]) for l in LEVELS};print(json.dumps({'basis':b,'available':counts,'needed':needed}),flush=True)
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
        for r in instances:v.check_record(r)
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];added={l:0 for l in LEVELS};rejected=0
        for l in LEVELS:
            candidates=[r for r in instances if r['question'][':question/difficulty']==':question.difficulty/'+l]
            for i in range(2000):
                if added[l]>=needed[l]:break
                r=candidates.pop(0) if candidates else g.generate(l,seed=int(JOB.name[:8],16)+i)
                v.check_record(r);fp=fingerprint(r['question']);assert fp==r['generation']['mathematical_fingerprint']
                if fp in used:rejected+=1;continue
                r['generation']['preparation_basis']=b;r['generation']['source_snapshot']='generate/scratch/17592186115241/reference/replenishment/initial/kp.edn'
                records.append(r);used.add(fp);added[l]+=1
        ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
        save(p/'generated.json',records);(p/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records)))
        native(records,p/'selected-grading')
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'available_counts':counts,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(records),'duplicate_candidates_rejected':rejected,'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-added[l] for l in LEVELS if needed[l]>added[l]}})
        if '--prepare-only' in sys.argv:return
        forms=transaction(records,kp,gid);assert forms,'No changes: retain existing verified registration receipt'
        tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout)
        pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_datoms(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'consistent-system-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK)}
        save(p/'commit-intent.json',intent)
        finish(p,intent,verify(p,intent,DB._commit(intent,txpath,p)))
if __name__=='__main__':main()
