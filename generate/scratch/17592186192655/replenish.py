"""Scoped additive replenishment; exact requests and readback retained under api.lock."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
KP, LEVELS = g.KP_ID, ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.PROVENANCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'030513d0fdc517d26af06057ea332998d69000075e013622ef4ee201dd87fe32'
OUT = HERE/'reference/replenishment'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-54c748c3d1efebc6'
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
def inventory(p):
    r = subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint], input='{"action":"inventory"}', env=ENV, capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout); assert x['ok'] and x['data']['lineage']==LINEAGE
    save(p,x['data']); return x['data']
def read_kp(p,b): return DB.query(QUERY,[KP],p,'kp',b)[0][0]

def normalized(q):
    return {':question/id':str(q[':question/id']), ':question/problem':q[':question/problem'], ':question/worked-solution':q[':question/worked-solution'], ':question/difficulty':enum(q[':question/difficulty']), ':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':enum(f[':answer-field/type']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':enum(a[':answer/type']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}
def ordered(q):
    q=copy.deepcopy(q); q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']: f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def parameters(q):
    system=re.search(r'\$\\?\{([^$]+)\$',q[':question/problem']).group(1)
    names=list(dict.fromkeys(re.findall('[a-z]',system))); assert len(names)==2
    rows=[v.coefficients(r,names) for r in system.split(';')]; assert len(rows)==2
    p={k:int(n) for k,n in zip(('a1','b1','c1','a2','b2','c2'),sum(rows,()))}
    assert all(sp.Integer(p[k])==n for k,n in zip(('a1','b1','c1','a2','b2','c2'),sum(rows,())))
    p['variables']=names; return p

def fingerprint(q):
    p=parameters(q); common=int(abs(sp.igcd(*(p[k] for k in ('a1','b1','c1','a2','b2','c2')))))
    return g.digest({'ordered_target_coefficients_up_to_global_scaling':[abs(p['b1'])//common,p['b2']*int(sp.sign(p['b1']))//common], 'target_variable_index':1, 'smaller_is_unit':min(abs(p['b1']),abs(p['b2']))//common==1, 'integer_multiplier_only':True})

def validate_record(r):
    v.check_record(r); assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
    assert fingerprint(r['question'])==r['generation']['mathematical_fingerprint']
    m=r['generation']; replay=g.generate(m['level'],m['seed'],template=m['template'],profile=m['profile'],parameters=m['parameters'])
    assert ordered(r['question'])==ordered(replay['question']), 'Generated identity/content replay mismatch'

def native(r,label):
    return {'label':label,'record':r,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every displayed choice through actual learner grader'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}
def grade(records,p):
    save(p/'native-input.json',[native(r,str(i)) for i,r in enumerate(records)])
    if records: subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'native-input.json'),str(p/'native-report.json')],check=True)

def available(kp,p,b):
    used={r[0] for r in DB.query(USAGE,[KP,LEARNER],p,'unavailable',b)}
    used.update(r[0] for r in DB.query(USAGE,[KP,LEARNER],p,'historically-unavailable',b,history=True))
    tasks={l:set() for l in LEVELS}; excluded=[]; records=[]
    for q in kp[':knowledge-point/questions']:
        reason=None; level=enum(q.get(':question/difficulty','')).split('/')[-1]
        if q[':db/id'] in used: reason='Shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'): reason='Canonical example'
        elif level not in LEVELS: reason='Unrated'
        else:
            try:
                pms=parameters(q); template='spaced' if 'equations.\n\n' in q[':question/problem'] else 'compact'
                matches=[]
                for profile in (['difference'] if level=='easy' else ['difference','coefficient']):
                    r=g.generate(level,0,template=template,profile=profile,parameters=pms)
                    if normalized(q)==ordered(r['question']): matches.append(r)
                assert len(matches)==1,'Current rated question does not match validated generator'
                validate_record(matches[0]); records.append(matches[0]); tasks[level].add(fingerprint(q))
            except (AssertionError,ValueError,KeyError,AttributeError) as e: reason='Validation exclusion: '+str(e)
        if reason: excluded.append({'entity':q[':db/id'],'reason':reason})
    grade(records,p/'available-grading')
    result={'basis':b,'distinct_available':{l:len(tasks[l]) for l in LEVELS},'excluded':excluded,'shown_or_reserved':sorted(used)}
    save(p/'validated-inventory.json',result); return result


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
    else: assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records: forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms: forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,p,source):
    attrs={e:str(a) for e,a in DB.attributes(p,report[':edb/db-before-t'])}; new=set(report[':edb/tempids'].values())
    allowed={':'+n for n in ['question/id','question/problem','question/worked-solution','question/difficulty','question/answer-fields','answer-field/id','answer-field/key','answer-field/type','answer-field/choices','answer-field/correct','answer/id','answer/type','answer/value','question-generator/id','question-generator/script']}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected contributor or retraction'
        name=attrs[a]
        if e==KP: assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant': assert e in new and name in allowed,(e,name)

def verify(p,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,p/'receipt-check',intent['source_eid'])
    kp=read_kp(p/'readback',report[':edb/db-after-t']);before=loads((p/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((p/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalized(q)==ordered(r['question']);validate_record(r)
    assert not transaction([],kp,intent['generator_id'])
    counts=available(kp,p/'verified-inventory',report[':edb/db-after-t'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['generation']['level']==l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'distinct_available':counts['distinct_available']}
    save(p/'verification.json',result);return result

def finish(p,gid,verified):
    inv=inventory(p/'inventory-after.json');remaining=[j for j in inv['jobs'] if j['knowledgePoint']==KP]
    shortage={l:max(0,5-verified['distinct_available'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'supported_levels':list(LEVELS),'difficulty_evidence':'Authored one-transformation workloads; source practice questions are unrated and incomplete.','unsupported_levels':[],'unsupported_levels_filled':False,'remaining_shortage':shortage,'remaining_jobs':remaining,'inventory_recheck_basis':inv['basis'],'capability_exceptions':[],'evidence':[str(z.relative_to(ROOT)) for z in [p/'verification.json',p/'commit-intent.json',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'inventory-after.json',p/'native-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'bank-mapping.json']]}
    assert not remaining or any(shortage.values()),'Native inventory unexpectedly still pending'
    if any(shortage.values()):result['capability_exceptions']=[{'kind':'finite-task-limit','bounded_attempts':3000,'task_catalog':json.loads((HERE/'validation.json').read_text())['finite_task_catalog'],'note':'Incidental coefficients, variables, profiles, seed and option order do not replenish exhausted assessed tasks.'}]
    save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','by_level','distinct_available') if k in result}|{'remaining_shortage':shortage,'remaining_jobs':remaining}),flush=True)

def main():
    assert json.loads((HERE/'validation.json').read_text())['passed']
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    OUT.mkdir(parents=True,exist_ok=True)
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for p in sorted(OUT.glob('basis-*')):
            if (p/'commit-intent.json').exists():
                intent=json.loads((p/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,p/'transaction.edn',p)
                finish(p,intent['generator_id'],verify(p,intent,report));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis']; assert DB.basis()==b
        p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True)
        kp=read_kp(p,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (p/'before.edn').write_text(dumps(kp)+'\n')
        historic=read_kp(p/'historical-source',g.PROVENANCE['basis'])
        current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(current[q[':db/id']]==q for q in historic[':knowledge-point/questions']), 'Source evidence changed; reclassify'
        assert historic[':knowledge-point/canonical-example']==kp[':knowledge-point/canonical-example']
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        byscript=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],p,'generator-by-script',b)
        assert len(byscript)<=1
        gid=str(gen[':question-generator/id']) if gen else str(byscript[0][0][':question-generator/id']) if byscript else str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+SCRIPT))
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],p,'generator-identity',b)
        assert not registered or (len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        counts=available(kp,p,b);needed={l:max(0,5-counts['distinct_available'][l]) for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances;assert isinstance(instances,list)
        records=[];selected={l:0 for l in LEVELS}
        for r in instances:
            validate_record(r);level=r['generation']['level'];fp=fingerprint(r['question'])
            if selected[level]<needed[level] and fp not in used:records.append(r);used.add(fp);selected[level]+=1
        save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        for level in LEVELS:
            for offset in range(3000):
                if selected[level]==needed[level]:break
                r=g.generate(level,int(JOB.name[:8],16)+offset);validate_record(r);fp=fingerprint(r['question'])
                if fp not in used:records.append(r);used.add(fp);selected[level]+=1
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        assert not ids or not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],p,'generated-identities',b),'Generated identity collision requires reconciliation'
        save(p/'generated.json',records);grade(instances+records,p)
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'hashes':{str(z.relative_to(ROOT)):sha(z) for z in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'validation.json',p/'generated.json']},'missing_by_level':needed,'selected_by_level':selected,'new_questions':len(records),'asset_hashes':[],'source_evidence_unchanged':True,'distinctness':'Ordered signed target division operands normalized under global common scaling; excludes incidental coefficient changes, variables, whitespace, seed, choice order and bank profile.','finite_task_catalog':json.loads((HERE/'validation.json').read_text())['finite_task_catalog']})
        forms=transaction(records,kp,gid);assert forms,'No changes needed; reconcile previous registration receipt'
        txpath=p/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'second-variable-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(p/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,p);finish(p,gid,verify(p,intent,report))

if __name__=='__main__':main()
