"""Additive KP-only inventory transaction using the application's EDB integration."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning

spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
KP, LEVELS = g.KP_ID, ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '9601e72ceb4031ff724938c147efe278447f56295be37d761c76f4266eab6fe3'
OUT = HERE / 'reference/replenishment'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
QUERY = '''[:find (pull ?k [* {:knowledge-point/question-generator [*]}
 {:knowledge-point/canonical-example [*]}
 {[:knowledge-point/questions :limit nil] [* {:question/difficulty [:db/ident]}
 {:knowledge-point/_canonical-example [:db/id]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]}])
 :in $ ?k :where [?k :knowledge-point/id _]]'''
USAGE = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
 (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def enum(x): return str(x[':db/ident']) if isinstance(x, dict) else str(x)
def scalar(tex):
    tex = tex.replace(r'\,', '').strip().rstrip('.,:')
    while r'\frac' in tex:
        tex, n = re.subn(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', tex)
        assert n, tex
    tex = tex.replace('{','(').replace('}',')')
    return parse_expr(tex, local_dict={s:sp.Symbol(s) for s in 'abxypquvntd'},
        transformations=standard_transformations+(implicit_multiplication_application,))

def equations(q, allow_context=False):
    text = q[':question/problem']
    group = re.search(r'\\\{\\begin\{aligned\}(.*?)\\end\{aligned\}', text, re.S)
    if group: rows = group[1].split(r'\\')
    else:
        group = re.search(r'\\\{([^$]*)\$', text)
        rows = group[1].split(';') if group else re.findall(r'\$([^$]*=[^$]*)\$', text)
    rows = [r for r in rows if r.count('=') == 1 and r.split('=')[1].strip()]
    if len(rows) != 2 and allow_context:
        group = re.search(r'\\\{\\begin\{aligned\}(.*?)\\end\{aligned\}', q.get(':question/worked-solution',''), re.S)
        if group: rows = group[1].split(r'\\')
    assert len(rows)==2, 'Prompt does not supply two equations'
    eqs = [sp.expand(scalar(r.split('=')[0].replace('&',''))-scalar(r.split('=')[1])) for r in rows]
    names = sorted(set().union(*(e.free_symbols for e in eqs)), key=str)
    assert len(names)==2
    m,b=sp.linear_eq_to_matrix(eqs,names); assert m.det()!=0
    solved=dict(zip(names,m.inv()*b))
    canonical=[]
    for i in range(2):
        row=list(m.row(i))+[-b[i]]; pivot=next(z for z in row[:2] if z)
        canonical.append(tuple(str(sp.cancel(z/pivot)) for z in row))
    # Renaming/swapping coordinates, equation order, scaling, seed and banks
    # cannot create a new mathematical system.
    def norm_swap(rows):
        out=[]
        for row in rows:
            x,y,c=map(sp.Rational,row); vals=[y,x,c];p=next(z for z in vals[:2] if z)
            out.append(tuple(str(z/p) for z in vals))
        return tuple(sorted(out))
    fp=min(tuple(sorted(canonical)), norm_swap(canonical))
    return eqs,names,solved,fp

def normalize(q):
    x={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    x[':question/difficulty']=enum(q[':question/difficulty'])
    x[':question/answer-fields']=[]
    for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
        x[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])})
    return x

def ordered(q):
    x=copy.deepcopy(q);x[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in x[':question/answer-fields']: f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return x

def source_valid(q):
    v.format_check(q[':question/problem']);v.format_check(q[':question/worked-solution'])
    eqs,names,solved,fp=equations(q)
    mid=q.get(':question/math-academy-id')
    response_names = [sp.Symbol(n) for n in ('t','d')] if mid=='q-166761' else names
    fields=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
    for i,f in enumerate(fields):
        values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
        assert values and len(set(values))==len(values)
        assert enum(f[':answer-field/type'])==':answer-field.type/blank', 'Current rated sources are blanks'
        assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        assert f[':answer-field/correct'] in f[':answer-field/choices']
        assert scalar(f[':answer-field/correct'][':answer/value'])==solved[response_names[i]]
    assert len(fields)==2
    # Independently verify every displayed equation in the current solution.
    count=0
    for block in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)',q[':question/worked-solution'],re.S):
        text=''.join(block).strip().removeprefix(r'\{')
        text=re.sub(r'\\(?:begin|end)\{aligned\}','',text)
        previous=None
        # A final inline sentence can give both coordinate assignments. Treat
        # these as separate equations, rather than parsing a SymPy tuple.
        text = re.sub(r',(?:\\,)?\s*(?=[a-z]\s*=)', r'\\\\', text)
        for row in text.split(r'\\'):
            if '=' not in row: continue
            row=row.replace('&','').strip().rstrip('.,')
            parts=row.split('=')
            if not parts[0].strip():parts[0]=previous
            assert parts[0]
            previous=parts[0]
            vals=[scalar(p) for p in parts]
            assert all(sp.simplify((vals[0]-z).subs(solved))==0 for z in vals[1:]),row
            count+=len(vals)-1
    assert count>=8
    rec={'question':normalize(q),'knowledge_point':{'title':g.TITLE},'generation':{'template':'current-source/'+str(mid)}}
    return rec,fp,count

def available(path,kp,basis):
    unseen={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'unavailable',basis)}
    unseen.update(r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    valid={l:[] for l in LEVELS};excluded=[];native=[]
    for q in kp[':knowledge-point/questions']:
        level=enum(q.get(':question/difficulty','')).split('/')[-1]
        reason=None
        try:
            if q[':db/id'] in unseen: reason='Previously shown or reserved, including retained history'
            elif q.get(':knowledge-point/_canonical-example'): reason='Canonical example'
            elif level not in valid:reason='Unrated or unsupported difficulty'
            elif ':question/math-academy-id' in q:
                rec,fp,rows=source_valid(q);native.append({'label':str(q[':question/id']),'record':rec,'checks':v.checks(rec)})
            else:
                rec={'question':normalize(q),'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'generation':{'template':next(r['generation']['template'] for r in json.loads((path.parent/'generated.json').read_text()) if r['question'][':question/id']==str(q[':question/id']))}}
                v.check_record(rec);_,_,_,fp=equations(q)
                native.append({'label':str(q[':question/id']),'record':rec,'checks':v.checks(rec)})
            if reason is None:valid[level].append((q,fp))
        except (AssertionError,ValueError,KeyError,TypeError,StopIteration) as e:reason='Validation exclusion: '+str(e)
        if reason:excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
    save(path/'available-native-input.json',native)
    if native:subprocess.run([str(HERE/'check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True)
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fp for q,fp in items}),'available_question_ids':[str(q[':question/id']) for q,fp in items]} for l,items in valid.items()},'excluded_questions':excluded,'shown_or_reserved':sorted(unseen)}
    save(path/'available-counts.json',result);return result

def inventory(native,path):
    r=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data']);return x['data']
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

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
    if gen is None:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,path,source):
    names={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':'+name for name in ['question/id','question/problem','question/worked-solution','question/difficulty','question/answer-fields','answer-field/id','answer-field/key','answer-field/type','answer-field/choices','answer-field/correct','answer/id','answer/type','answer/value','question-generator/id','question-generator/script']}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=names[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,(e,name)

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t']);old=loads((path/'before.edn').read_text())
    before={q[':db/id']:q for q in old[':knowledge-point/questions']};after={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(after[e]==q for e,q in before.items())
    assert {k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in old.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in after.values()}
    assert len(after)==len(before)+len(records)
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(r['question']);v.check_record(r)
    assert not transaction([],kp,intent['generator_id'])
    counts=available(path/'readback',kp,report[':edb/db-after-t'])
    shortages={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'source_questions_preserved':len(before),'canonical_example_preserved':True,'only_scoped_additive_datoms':True,'learner_history_preserved':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':counts,'shortage_remaining':shortages}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text())
    result={'outcome':'finite-limit' if any(verified['shortage_remaining'].values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':verified['shortage_remaining'],'available_counts_before':prep['available_counts'],'available_counts_after':verified['available_counts_after'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'transaction.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',HERE/'reference/current-classification.md',HERE/'reference/runtime-validation.json'] if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_by_level','shortage_remaining','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'reference/runtime-validation.json').read_text());assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    OUT.mkdir(parents=True,exist_ok=True)
    native=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        # Recover immutable requests before considering any new intent.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn')
                assert intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(native,path/'inventory-after.json'));return
        inv=inventory(native,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        with (path/'before.edn').open('w') as f:f.write(dumps(kp)+'\n');f.flush();os.fsync(f.fileno())
        save(path/'current-source.json',json.loads(json.dumps(kp,default=str)))
        # Verify source evidence is still the freshly classified ten-question bank.
        current=loads((HERE/'reference/classification-source.edn').read_text())
        assert kp==current,'Source bank changed; refresh classification before any write'
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        schemas=DB.query('[:find (pull ?a [*]) :in $ [?i ...] :where [?a :db/ident ?i]]',[[kw('question-generator/id'),kw('question-generator/script'),kw('knowledge-point/question-generator'),kw('question/validate'),kw('answer-field/validate'),kw('answer/validate'),kw('knowledge-point/validate')]],path,'installed-schema',b)
        assert len(schemas)==7
        gen=kp.get(':knowledge-point/question-generator')
        registered=DB.query('[:find ?g ?id :in $ ?script :where [?g :question-generator/script ?script] [?g :question-generator/id ?id]]',[SCRIPT],path,'existing-generator',b)
        assert len(registered)<=1
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][1]) if registered else str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/question-generator/'+g.KP_UUID))
        assert not registered or gen is not None,'Existing orphan generator requires reuse before committing'
        counts=available(path,kp,b);needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used=set();pairs=set()
        for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
            try:
                _,names,solved,fp=equations(q,True);used.add(fp);pairs.add(tuple(sorted(str(solved[n]) for n in names)))
            except (AssertionError,ValueError,KeyError):pass
        supplied=json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {}
        eligible=supplied.get('instances',[]);assert isinstance(eligible,list)
        records=[];added={l:0 for l in LEVELS};rejected=[]
        local=[]
        for l in LEVELS:
            for i in range(50):local.append(g.generate(l,int(JOB.name[:8],16)+i))
        for r in eligible+local:
            l=r['question'][':question/difficulty'].split('/')[-1]
            if l not in LEVELS:rejected.append({'question_id':r['question'][':question/id'],'reason':'Unsupported level'});continue
            v.check_record(r)
            if added[l]>=needed[l]:continue
            _,names,solved,fp=equations(r['question']);pair=tuple(sorted(str(solved[n]) for n in names))
            if fp in used or pair in pairs:continue
            records.append(r);used.add(fp);pairs.add(pair);added[l]+=1
        save(path/'supplied-status.json',{'exists':JOB.with_suffix('.generated').exists(),'instances_validated':len(eligible),'rejected':rejected})
        save(path/'generated.json',records);save(path/'review.json',local)
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in values]],path/'identities',attr.replace('/','-'),b),'Identity collision'
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)} for r in records])
        subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'new_by_level':added,'available_counts':counts,'distinctness':'Normalized complete systems under row scaling, row order and coordinate renaming; also reject repeat solution pairs across all levels. Banks, seed and choice order are excluded.','asset_hashes':[],'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_evidence':'All ten current source questions retained; existing validated template scope reused. New source templates classified with explicit generation coverage limits.'})
        forms=transaction(records,kp,gid);assert forms,'Already stocked and registered; no new transaction needed'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        status=DB.command('status');assert 'lineage='+LINEAGE in status
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'substitution-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(native,path/'inventory-after.json'))

if __name__=='__main__':main()
