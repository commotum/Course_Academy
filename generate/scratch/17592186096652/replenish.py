"""Only KP 17592186096652: validate, replenish, commit under application lock."""
import ast, copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment,build_learning
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
spec=importlib.util.spec_from_file_location('vector_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Load the already revalidated pure readback functions without rerunning the suite.
names={'rational','expression','format_check','mathematics'}
tree=ast.parse((HERE/'validate.py').read_text())
v=SimpleNamespace(**vars(g))
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
v.__dict__.update(parse_expr=parse_expr,standard_transformations=standard_transformations,implicit_multiplication_application=implicit_multiplication_application,rationalize=rationalize,g=g)
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(HERE/'validate.py'),'exec'),v.__dict__)
KP=g.KP
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'5d9b794be25fa3b1a21b7a4bb3c7d1189b64c673be328ab08d471e2665653a17'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
LEVELS=('easy','moderate','hard')
Q='[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

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

def replace_paths(obj,mapping):
    if isinstance(obj,dict):return {mapping.get(k,k):replace_paths(val,mapping) for k,val in obj.items()}
    if isinstance(obj,list):return [replace_paths(val,mapping) for val in obj]
    if isinstance(obj,str):
        for old,new in mapping.items():obj=obj.replace(old,new)
    return obj

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def native_checks(rec):
    checks=[]
    for index,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':index,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice'})
        else:
            answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);val=v.rational(answer)
            for submitted,expected in [(answer,'accepted'),(f'{val.p*3}/{val.q*3}','accepted'),(str(val+1),'rejected')]:
                checks.append({'field_index':index,'submitted':submitted,'expected':expected,'purpose':'canonical/equivalent/wrong scalar'})
    return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}

def grade(records,path):
    path.mkdir(parents=True,exist_ok=True)
    save(path/'native-input.json',[native_checks(r) for r in records])
    subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    return report

def fingerprint(q):
    # Conservative mathematical equivalence: names, diagrams, path order,
    # layout, difficulty, banks and choice shuffles never inflate pair variety.
    sol=q[':question/worked-solution']
    pattern=r'\s*=\s*(-?(?:\\frac\{\d+\}\{\d+\}|\d+(?:\.\d+)?))'
    factors=[v.rational(re.findall(r'\\'+key+pattern,sol)[-1]) for key in ('lambda','mu')]
    return g.digest([str(z) for z in factors])

def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def validate_sources(kp,path,basis):
    expected=g.RECORD
    current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    old={q[':question/math-academy-id']:q for q in expected[':knowledge-point/questions']}
    assert set(current)==set(old),'New source evidence requires classification'
    for sid,q in old.items():assert canonical(source_projection(current[sid],q))==canonical(q),sid
    assert canonical(source_projection(kp[':knowledge-point/canonical-example'],expected[':knowledge-point/canonical-example']))==canonical(expected[':knowledge-point/canonical-example'])
    save(path/'source-validation.json',{'passed':True,'current_basis':basis,'source_basis':g.CAPTURE['basis'],'practice_sources_unchanged':len(old),'canonical_unchanged':True,'source_error':'q-275128 exposes scalars instead of placeholders; preserved and excluded from gradable inventory','fidelity_evidence':str((HERE/'validation.json').relative_to(ROOT))})

def counts(kp,path,basis):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    available={l:set() for l in LEVELS};records=[];excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        fields=q.get(':question/answer-fields',[])
        if level not in available or not q.get(':question/worked-solution') or not fields or not all(f.get(':answer-field/correct',{}).get(':answer/id') in {a[':answer/id'] for a in f.get(':answer-field/choices',[])} and (str(f[':answer-field/type'][':db/ident']).endswith('/radio') or '{{'+f[':answer-field/key']+'}}' in q[':question/problem']) for f in fields):
            excluded.append({'id':q[':db/id'],'reason':'Unrated/incomplete/missing answer placeholder; preserved'});continue
        rec={'knowledge_point':{'db_id':KP,'id':str(g.NS),'title':g.RECORD[':knowledge-point/title']},'question':normalize(q)}
        records.append(rec)
        if q[':db/id'] not in shown|reserved:available[level].add(fingerprint(q))
    if records:grade(records,path/'inventory-grading')
    result={'basis':basis,'distinct_available':{l:len(z) for l,z in available.items()},'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'excluded_source_questions':excluded,'distinctness':'Exact ordered scalar pair; source duplicates conservatively coalesced'}
    save(path/'available-counts.json',result);return result

def check(rec):
    meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
    replay=g.generate(level,meta['seed'],template=meta['template'],field_type=rec['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1],parameters=meta['parameters'],profile=meta['bank_profile'])
    assert ordered(replay['question'])==ordered(rec['question'])
    v.mathematics(rec)
    assert fingerprint(rec['question'])==g.digest([str(g.sp.Rational(meta['parameters'][k])) for k in ('lambda','mu')])

def publish(records,path):
    save(path/'generated-local.json',records)
    library=ImageLibrary(Path(ENV['EDB_MATH_ROOT']),HERE)
    published=copy.deepcopy(records)
    for r in published:
        for key in (':question/problem',':question/worked-solution'):r['question'][key]=library.text(r['question'][key])
    save(path/'assets.json',library.saved);save(path/'generated.json',published)
    for a in library.saved.values():assert sha(Path(ENV['EDB_MATH_ROOT'])/a['path'])==a['sha256']
    return published

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    assert canonical({k:val for k,val in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:val for k,val in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());local=json.loads((path/'generated-local.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec,original in zip(records,local):
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);check(original)
        assert fingerprint(q)==rec['generation']['inventory_fingerprint']
    for a in json.loads((path/'assets.json').read_text()).values():assert sha(Path(ENV['EDB_MATH_ROOT'])/a['path'])==a['sha256']
    assert not transaction([],kp,intent['generator_id'])
    available=counts(kp,path/'readback',report[':edb/db-after-t'])['distinct_available']
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'distinct_available_after':available}
    save(path/'verification.json',result);return result

def inventory(path):
    native=build_learning(ROOT.parent/'EDB')
    r=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data']);return x['data']

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());available=verified['distinct_available_after'];shortage={l:max(0,5-available[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'source':SOURCE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':available,'shortage_by_level':shortage,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':prep['capability_exceptions'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'source-validation.json',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'assets.json',path/'generated.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md')]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)

def main():
    frozen=json.loads((HERE/'freeze.json').read_text())
    for name in (HERE.with_suffix('.py'),HERE/'templates.json',HERE/'render_plot.py',HERE/'validate.py'):
        assert sha(name)==frozen['hashes'][str(name.relative_to(ROOT))]
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed'] and validation['complete_source_banks_matched']==21 and validation['native']['documented_unresolved_checks']==0
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    # Only the application serialization lock is held through preparation,
    # submission and exact-basis readback. Unknown saved intent is recovered first.
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired.',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                inv=inventory(path/'inventory-after.json');finish(path,intent['generator_id'],verified,inv);return
        inv=inventory(OUT/'inventory-before-locked.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==str(g.NS)
        validate_sources(kp,path,b);(path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(g.NS,'question-generator'))
        if gen:assert gen[':question-generator/script']==SCRIPT
        available=counts(kp,path/'current-inventory',b)['distinct_available']
        needed={l:max(0,5-available[l]) for l in LEVELS};selected={l:0 for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];attempts={l:0 for l in LEVELS};supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(instances,dict):instances=[instances]
        def select(rec):
            check(rec);level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if selected[level]<needed[level] and fp not in used:
                rec=copy.deepcopy(rec);rec['generation']['inventory_fingerprint']=fp
                records.append(rec);used.add(fp);selected[level]+=1
        for rec in instances:select(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances)})
        # Explicit enumeration establishes bounded coverage without seed aliases.
        domains={'easy':[g.sp.Rational(i) for i in range(1,5)],'moderate':[g.sp.Rational(i,2) for i in range(-8,9) if i], 'hard':sorted({sign*g.sp.Rational(n,d) for d in (2,3,4) for n in range(1,4*d) if g.sp.Rational(n,d).q>1 for sign in (-1,1)})}
        for level in LEVELS:
            pairs=[(a,z) for a in domains[level] for z in domains[level]]
            g.random.Random(20261014).shuffle(pairs)
            for a,z in pairs:
                if selected[level]>=needed[level]:break
                if level=='moderate' and a>0 and z>0 and a.q==z.q==1:continue
                if g.digest([str(a),str(z)]) in used:continue
                rec=g.generate(level,seed=20261014,parameters={'lambda':str(a),'mu':str(z)});attempts[level]+=1;select(rec)
        exceptions=[{'level':l,'missing':needed[l]-selected[l],'evidence':'Entire documented exact rational domain enumerated; source-equivalent tasks excluded. No seed, label, layout, path-order or choice-bank aliases counted.'} for l in LEVELS if selected[l]<needed[l]]
        print(json.dumps({'basis':b,'available':available,'needed':needed,'selected':selected}),flush=True)
        for attribute,ids in (('question/id',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[ids],path,attribute.replace('/','-')+'-collisions',b)
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
        records=publish(records,path);native=grade(records,path)
        (path/'review.md').write_text('# Replenishment variants\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_by_level':available,'missing_by_level':needed,'selected_by_level':selected,'sampling_attempts':attempts,'capability_exceptions':exceptions,'new_questions':len(records),'source_evidence_unchanged':True,'difficulty_evidence':'Easy positive integer ratios; moderate source sign/fractional ratios; hard authored two noninteger ratios plus reversed path. No new vector operation. See classification.md.','distinctness':'Exact ordered scalar pair excludes all source/canonical/current pairs across levels; seeds/IDs/choice order not counted','native':native,'generator_sha256':sha(HERE.with_suffix('.py')),'renderer_sha256':sha(HERE/'render_plot.py'),'dependencies':{'sympy':g.sp.__version__},'assets':json.loads((path/'assets.json').read_text())})
        if "--prepare-only" in sys.argv:
            print("Prepared and validated; review " + str(path),flush=True);return
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'by_level':{l:0 for l in LEVELS},'distinct_available_after':available}
            save(path/'verification.json',{'passed':True,'no_change':True,**verified});finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0])
        assert counts(read_kp(path/'precommit',b),path/'precommit',b)['distinct_available']==available and DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'vector-pair-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'generator_version':g.VERSION,'asset_hashes':json.loads((path/'assets.json').read_text()),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);print('Validated preview; submitting exact guarded request.',flush=True)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        inv=inventory(path/'inventory-after.json');assert inv['basis']==verified['basis_after'];finish(path,gid,verified,inv)

if __name__=='__main__':main()
