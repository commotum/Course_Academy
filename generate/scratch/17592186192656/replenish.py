"""Three-level additive commit with application locking and exact-basis readback."""
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace

H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from db_support import DB, KP, PATTERN, dumps, loads, kw
sys.path.insert(0,str(ROOT/'scripts'))
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
spec=importlib.util.spec_from_file_location('linear_system_validation',H/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine';SCRIPT=str(H.with_suffix('.py').relative_to(ROOT))
LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'259df889715f1a5020cf9b25b25c6a78281161e80feb1fe8b3ca177538f7d9c0'
OUT=H/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def inventory(native,path):
    r=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data']);return x['data']

def read_kp(path,basis):
    return DB.query('[:find (pull ?k '+PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],path,'kp',basis)[0][0]

def normalized(q):
    out={k:str(q[k]) if k==':question/id' else q[k] for k in [':question/id',':question/problem',':question/worked-solution']}
    out[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);out[':question/answer-fields']=[]
    # EDB many-ref traversal has no instructional ordering. Field keys carry
    # the two coordinates, so restore that semantic order before grading QA.
    for f in sorted(q[':question/answer-fields'],key=lambda z:z[':answer-field/key']):
        out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
    return out

def transaction(records,kp):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT,'Existing registered generator requires reconciliation'
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(g.GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def report_checks(report,path,source):
    attrs={eid:str(a) for eid,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question-generator/id',':question-generator/script'}
    for e,a,value,t,s,added in report[':edb/tx-data']:
        assert added and s==source,'Unexpected retraction or attribution'
        name=attrs[a]
        if e==KP:assert name in {':knowledge-point/questions',':knowledge-point/question-generator'}
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected non-scoped datom'

LEVELS=('easy','moderate','hard')

def source_projection(x):
    if isinstance(x,dict):
        return {k:source_projection(z) for k,z in x.items() if not (k==':db/id' and ':db/ident' in x)}
    if isinstance(x,list):return [source_projection(z) for z in x]
    return x

def parameters(q):
    import sympy as sp
    m=re.search(r'solution \$\((\w), ?(\w)\)\$',q[':question/problem']);assert m
    x,y=map(sp.Symbol,m.groups())
    if '\\begin{aligned}' in q[':question/problem']:
        block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)[1]
        rows=[v.equation(z) for z in re.split(r'\s+\\\\\s+',block)]
    else:rows,_=v.printed_system({'question':q})
    p={'variables':m[1]+m[2]}
    for i,(left,right) in enumerate(rows,1):
        assert left==left.coeff(x)*x+left.coeff(y)*y
        for key,z in [('a',left.coeff(x)),('b',left.coeff(y)),('c',right)]:
            assert z.is_Integer;p[key+str(i)]=int(z)
    return p

def fingerprint(q):
    import sympy as sp
    try:
        rows=g.primitive_rows(parameters(q));ratio=sp.Rational(max(z[0] for z in rows),min(z[0] for z in rows))
        return g.digest([sorted(rows),str(ratio)])
    except (AssertionError,ValueError,KeyError,ZeroDivisionError):return None

def record_from_db(q):
    nq=normalized(q);level=nq[':question/difficulty'].split('/')[-1]
    kind=nq[':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
    r=g.generate(level,template=kind+'_solution',parameters=parameters(q))
    r['question']=nq;return r

def counts(kp,path,basis):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    available={level:set() for level in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if level not in LEVELS or q[':db/id'] in shown|reserved:continue
        try:
            source=loads((H/'current-source.edn').read_text())
            known=next((z for z in source[':knowledge-point/questions'] if z[':db/id']==q[':db/id']),None)
            if known:
                assert canonical(q)==canonical(known),'Captured source changed'
                checked=json.loads((H/'current-source-validation.json').read_text())
                assert str(q[':question/id']) in checked['validated_question_ids']
            else:
                r=record_from_db(q);v.validate_record(r)
            available[level].add(fingerprint(q))
        except (KeyError,AssertionError,TypeError,ValueError) as e:
            excluded.append({'question':str(q[':question/id']),'reason':str(e) or type(e).__name__})
    out={'basis':basis,'distinct_available':{level:len(values) for level,values in available.items()},'shown_or_reserved':sorted(shown|reserved),'invalid_or_incomplete':excluded}
    save(path/'available-counts.json',out);return out

def engine_item(r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        if f[':answer-field/type']==':answer-field.type/radio':
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete tuple reinserted in both equations'} for a in f[':answer-field/choices'])
        else:
            value=v.correct_value(f)
            checks.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'Exact scalar'},
                           {'field_index':i,'submitted':f'({value}*3)/3','expected':'accepted','purpose':'Equivalent arithmetic scalar'},
                           {'field_index':i,'submitted':str(v.algebra(value)+1),'expected':'rejected','purpose':'Wrong scalar'}])
    return {'label':r['question'][':question/id'],'record':r,'checks':checks}

def verify(report,path,intent):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    b=report[':edb/db-after-t'];report_checks(report,path/'receipt-check',intent['source_eid'])
    before=loads((path/'before.edn').read_text());after=read_kp(path/'readback',b)
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
    assert all(canonical(q)==canonical(now[e]) for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert canonical({k:z for k,z in before.items() if k not in omit})==canonical({k:z for k,z in after.items() if k not in omit})
    gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert canonical(normalized(q))==canonical(r['question'])
        assert fingerprint(q)==r['generation']['mathematical_fingerprint'];v.validate_record(r)
    assert not transaction([],after),'Repeat preparation must produce no content changes'
    c=counts(after,path/'readback',b)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),
            'distinct_available':c['distinct_available'],'unchanged_source_questions':len(old),
            'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,
            'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,
            'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,verified,inv):
    remaining={level:max(0,5-verified['distinct_available'][level]) for level in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,
            'generator_path':SCRIPT,'generator_id':g.GENERATOR_ID,'lineage':LINEAGE,
            'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],
            'supported_levels':list(LEVELS),'available_after':verified['distinct_available'],
            'shortage_remaining':remaining,'unsupported_levels_filled':False,
            'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
            'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'freeze.json',H/'current-source.json',H/'current-source-validation.json',H/'current-source-native-report.json',path/'generated.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'verification.json',path/'inventory-after.json',path/'native-report.json']],
            'bounded_template_exclusions':[{'template':'current aligned b=13 blank / first-row substitution','reason':'Outside narrower generator presentation policy; valid captured source still counted. This does not restrict the requested variant count.'}],
            'note':'New question ratings follow authored bounds; hard lacks a captured rating. All three current source questions, canonical example, original historical source snapshot, and learner history preserved. Historical opaque bank remains evidence only; new choices use validated authored method errors.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ['outcome','verified_commit_basis','new_questions','available_after','remaining_jobs']}),flush=True)

def main():
    val=json.loads((H/'validation.json').read_text());assert val['status']=='passed'
    freeze=json.loads((H/'freeze.json').read_text());assert all(sha(ROOT/p)==s for p,s in freeze['files'].items())
    native=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    # Inventory is captured before any generation; the application lock covers
    # the fresh read, planning, preview, durable submission and exact readback.
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent)
                finish(path,verified,inventory(native,path/'inventory-after.json'));return
        inv=inventory(native,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path/'locked-source',b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        captured=loads((H/'current-source.edn').read_text());current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(canonical(source_projection(q))==canonical(source_projection(current[q[':db/id']])) for q in captured[':knowledge-point/questions']),'Source evidence changed; reclassify'
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        if gen:assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
        orphan=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(g.GENERATOR_ID)],path,'generator-identity',b)
        assert not orphan or len(orphan)==1 and orphan[0][0][':question-generator/script']==SCRIPT
        c=counts(kp,path,b);needed={level:max(0,5-c['distinct_available'][level]) for level in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];accepted={level:0 for level in LEVELS}
        supplied=json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        def consider(r):
            assert r['knowledge_point']['db_id']==KP and r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
            v.validate_record(r)
            level=r['question'][':question/difficulty'].split('/')[-1]
            replay=g.generate(level,r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
            assert canonical(replay)==canonical(r),'Instance does not replay'
            key=fingerprint(r['question']);assert key==r['generation']['mathematical_fingerprint']
            if accepted[level]<needed[level] and key not in used:
                records.append(r);used.add(key);accepted[level]+=1
        for r in instances:consider(r)
        # Run the registered generator CLI protocol, then deduplicate mathematical
        # systems across source, canonical example, fields, aliases and banks.
        for level in LEVELS:
            if accepted[level]>=needed[level]:continue
            p=subprocess.run([sys.executable,SCRIPT,'--difficulty',level,'--count','32','--seed',str(int(JOB.name[:8],16)),'--format','json'],cwd=ROOT,capture_output=True,text=True,check=True)
            for r in json.loads(p.stdout):
                consider(r)
                if accepted[level]>=needed[level]:break
        assert accepted==needed,'Bounded sample insufficient; no partial commit'
        for kind,ids in [('question',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            assert len(ids)==len(set(ids))
            if ids:assert not DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]',[ids],path,'identity-'+kind,b),'Existing identity requires reconciliation'
        save(path/'generated.json',records);save(path/'native-input.json',[engine_item(r) for r in records])
        subprocess.run([str(H/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_evidence_unchanged':True,'available_before':c,'needed':needed,'new_questions':len(records),'distinct_tasks':len({r['generation']['mathematical_fingerprint'] for r in records}),'supplied_generated_file_exists':JOB.with_suffix('.generated').exists(),'supplied_instances_validated':len(instances),'generator_version':g.VERSION,'generator_sha256':sha(H.with_suffix('.py')),'asset_hashes':[],'levels_are_authored':True})
        forms=transaction(records,kp)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'distinct_available':c['distinct_available']};finish(path,verified,inv);return
        txpath=path/'transaction.edn';text=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        report_checks(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'first-variable-one-transform-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'generator_id':g.GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(report,path,intent)
        finish(path,verified,inventory(native,path/'inventory-after.json'))

if __name__=='__main__':main()

