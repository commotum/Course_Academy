"""Scoped normal-orientation replenishment; exact requests and locked readback."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from capture.scripts.database.preview import preview_executable
from current import DB, ENV, HERE, ROOT, KP, LEARNER, LINEAGE, inventory, discovery, read_kp, save
from edn import dumps, loads, kw
spec=importlib.util.spec_from_file_location('orientation_validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g;s=g.s
from mathcheck_17592186083280 import prompt_curve, value_set, T
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'12bcb62123485b4d3c3ea7dedfd955003b6cfb6c6b98ac1b7a3678b17342ac32'
OUT=HERE/'reference/replenishment'
LEVELS=('easy','moderate','hard')
FAMILIES={'easy':['exponential','logarithmic','quadratic'],'moderate':['cubic','shifted_trig'],'hard':['two_period_trig']}
USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x
def normalized(q):
    result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    if ':question/difficulty' in q:result[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields']=[]
    for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    return result
def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q
def task(q):
    # Canonical example uses quad separators; normalize only the reader input.
    q=copy.deepcopy(q);q[':question/problem']=q[':question/problem'].replace(r'\qquad',r'\,').replace(r'\quad',r'\,')
    x,y,domain=prompt_curve({'question':q});dx,dy=s.diff(x,T),s.diff(y,T)
    horizontal='horizontal' in q[':question/problem'];target=dx if horizontal else dy;other=dy if horizontal else dx
    roots=s.solveset(target,T,domain=domain);assert isinstance(roots,s.FiniteSet)
    roots=sorted(roots,key=lambda z:float(z))
    regular=[s.simplify(other.subs(T,r))!=0 for r in roots]
    incidental=isinstance(domain,s.Interval) and domain.end.is_finite and target.is_polynomial(T) and s.solveset(target,T,domain=s.S.Reals)==s.FiniteSet(*roots)
    data={'orientation':'horizontal' if horizontal else 'vertical','interval':None if incidental else s.srepr(domain),'zero_candidates':[[s.srepr(r),ok] for r,ok in zip(roots,regular)]}
    return g.digest(data),tuple(r for r,ok in zip(roots,regular) if ok)
def source_validation(kp,path,basis):
    # Preserve frozen raw replay and separately validate current checkbox migrations.
    current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert set(g.Q)<=set(current)
    results=[];fixtures=[]
    for name,(level,sid,p) in g.TEMPLATES.items():
        if not sid:continue
        q=current[sid];old=g.Q[sid];fp,roots=task(q)
        assert fp==task(old)[0], 'Source mathematics changed: '+sid
        if sid not in ('q-75278','q-21080'):
            for key in (':question/problem',':question/worked-solution'):assert q.get(key)==old.get(key),(sid,key)
            # The pull adds enum db IDs; compare field-owned IDs, values and keys.
            assert normalized(q)==normalized(old)
            rec=g.generate(level,template=name,parameters=p,profile='observed:'+sid)
            v.shape(rec);fixtures.append(v.fixture(rec,'current:'+sid,True))
            status='historical prompt, solution and complete bank unchanged'
        else:
            candidates=dict(re.findall(r'- \*\*([IVX]+)\.\*\* \$t=(.*?)\$',q[':question/problem']))
            assert len(candidates)==len(q[':question/answer-fields'])
            checks=[]
            for i,f in enumerate(q[':question/answer-fields']):
                assert str(f[':answer-field/type'][':db/ident'])==':answer-field.type/checkbox'
                assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'true','false'}
                candidate=value_set('t='+candidates[f[':answer-field/key']]);assert len(candidate)==1
                expected=str(candidate[0] in roots).lower();assert f[':answer-field/correct'][':answer/value']==expected
                checks.extend([{'field_index':i,'submitted_answer_id':str(a[':answer/id']),'expected':'accepted' if a[':answer/value']==expected else 'rejected','purpose':'current migrated checkbox truth choice'} for a in f[':answer-field/choices']])
            fixtures.append({'label':'current:'+sid,'record':{'question':normalized(q)},'checks':checks})
            status='current checkbox candidates independently solved and truth keys checked; historic radio replay retained separately'
        results.append({'source_id':sid,'mathematical_fingerprint':fp,'status':status,'counted_as_validated_practice':sid not in ('q-122946','q-21080'),'exclusion':{'q-122946':'asks points but key supplies parameters; source preserved','q-21080':'unrated; source preserved'}.get(sid)})
    save(path/'source-native-input.json',fixtures)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'source-native-input.json'),str(path/'source-native-report.json')],check=True)
    report=json.loads((path/'source-native-report.json').read_text());assert report['documented_unresolved_checks']==0
    save(path/'source-validation.json',{'basis':basis,'frozen_generator_source_basis':g.SOURCE['basis'],'source_count':len(results),'sources':results,'new_generation_policy':'Unchanged easy scalar, moderate cubic/shifted-trig and validated authored four-root hard families only. Current checkbox templates classified and validated; no new radio variants of migrated source templates selected.','plot_rating':'none','source_bank_fidelity':'Frozen generator full replay: 8/8 complete banks and 28/28 choices. Current unchanged banks replayed; both migrated checkbox banks have complete candidate truth-key coverage.'})
def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    rows={l:[] for l in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        mid=q.get(':question/math-academy-id')
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or ':question/difficulty' not in q or mid=='q-122946':
            excluded.append(str(q[':question/id']));continue
        if mid is None:
            # Unrecognized authored content requires its retained validation proof.
            found=[]
            for package in OUT.glob('basis-*/generated.json'):
                found.extend(r for r in json.loads(package.read_text()) if r['question'][':question/id']==str(q[':question/id']))
            if not found:excluded.append(str(q[':question/id']));continue
            assert normalized(q)==ordered(found[0]['question']);v.shape(found[0])
        fp,_=task(q);level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        rows[level].append((fp,str(q[':question/id'])))
    result={'basis':basis,'available_by_level':{l:len({fp for fp,_ in rows[l]}) for l in LEVELS},'questions_by_level':{l:[qid for _,qid in rows[l]] for l in LEVELS},'excluded_shown_reserved_unrated_or_response_mismatch':excluded,'distinctness':'complete derivative-zero parameter sets, regularity and assessed interval; seed, option order, nonzero multipliers, translations and phase aliases excluded'}
    save(path/'validated-inventory.json',result);return result
def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms
def check_report(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,src,added in report[':edb/tx-data']:
        assert src==source and added,'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name
def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid']);basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    assert canonical({k:z for k,z in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:z for k,z in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalized(q)==ordered(r['question']);v.shape(r);assert task(q)[0]==r['generation']['mathematical_fingerprint']
    assert not transaction([],kp,intent['generator_id'])
    after=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_existing_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after}
    save(path/'verification.json',result);return result
def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified['available_counts_after'];shortage={l:max(0,5-after['available_by_level'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'source':SOURCE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':verified['new_by_level'],'available_by_level':after['available_by_level'],'shortage_by_level':shortage,'supported_levels':list(LEVELS),'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'note':'Unrated original and points-versus-parameters source remain preserved and excluded from validated inventory. Both current checkbox migrations were validated. Generated instances use unchanged families and the validated authored hard family.','evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'source-validation.json',path/'source-native-report.json',path/'native-report.json',path/'preparation.json',path/'inventory-after.json',path/'generated.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md') if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed with documented raw source limitations' and validation['native']['documented_unresolved_checks']==0
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired.',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');disc=discovery(OUT/'discovery-before.json');basis=DB.basis();assert basis==inv['basis']==disc['basis']
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP[':knowledge-point/id']
        (path/'before.edn').write_text(dumps(kp)+'\n');source_validation(kp,path,basis)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(g.NS,'question-generator'))
        if gen:assert gen[':question-generator/script']==SCRIPT
        c=counts(kp,path,basis);needed={l:max(0,5-c['available_by_level'][l]) for l in LEVELS};selected={l:0 for l in LEVELS}
        used={task(q)[0] for q in kp[':knowledge-point/questions']};used.add(task(kp[':knowledge-point/canonical-example'])[0]);records=[];attempts={l:0 for l in LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        def select(rec):
            v.shape(rec);assert rec['generation']['eligible_for_learning'] is True
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=task(rec['question'])[0];assert fp==rec['generation']['mathematical_fingerprint']
            if selected[level]<needed[level] and fp not in used:records.append(rec);used.add(fp);selected[level]+=1
        for rec in instances:select(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        for level in LEVELS:
            for i in range(400):
                if selected[level]>=needed[level]:break
                name=FAMILIES[level][i%len(FAMILIES[level])];attempts[level]+=1;select(g.generate(level,i,template=name))
        exceptions=[{'level':l,'missing':needed[l]-selected[l],'bounded_attempts':400,'evidence':'No fresh task after bounded generation; exact finite canonical catalog retained in variety.json. No identity, seed or option-order aliases admitted.'} for l in LEVELS if selected[l]<needed[l]]
        print(json.dumps({'basis':basis,'validated_available':c['available_by_level'],'needed':needed,'selected':selected}),flush=True)
        for attr,ids in [('question/id',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,attr.replace('/','-')+'-matches',basis),'Identity collision requires reconciliation'
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
        save(path/'generated.json',records);save(path/'native-input.json',[v.fixture(r,r['question'][':question/id']) for r in records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        (path/'review.md').write_text('# Replenishment variants\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':c,'missing_by_level':needed,'selected_by_level':selected,'sampling_attempts':attempts,'capability_exceptions':exceptions,'source_basis':g.SOURCE['basis'],'current_source_basis':basis,'asset_hashes':[],'generator_sha256':sha(HERE.with_suffix('.py')),'validation_sha256':sha(HERE/'validation.json'),'generator_version':g.VERSION,'difficulty_evidence':'Easy one root; moderate two roots; authored hard four regular roots across two periods with familiar exact phase/frequency and four keyed blanks.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_before':basis,'basis_after':basis,'new_questions':0,'new_by_level':selected,'available_counts_after':c,'passed':True,'no_change':True};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0])
        assert DB.basis()==basis
        precommit=inventory(path/'inventory-precommit.json');assert precommit['basis']==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'normal-orientation-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'generator_version':g.VERSION,'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);print('Validated preview; submitting saved basis-guarded request.',flush=True)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
