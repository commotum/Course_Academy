"""Scoped additive ODE inventory replenishment with saved basis-guarded requests."""
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('ode_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
c = g
s = g.sp
KP = g.KP["db_id"]
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'28b82fe3e92616b33697de1bf8816b60fa3e414864893e3be21676c84cd637ae'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True,exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
NATIVE = ROOT/'.local/graph-explorer/learning-0ee7e7bd24d378f7'
DISCOVERY = ROOT/'.local/generate/find-candidates-b13a7928a9573a2f'
LEVELS = ('easy','moderate','hard')
FAMILIES = {'easy':['linear','quadratic','cubic','logarithmic','reciprocal'],'moderate':['cubic','exponential'],'hard':['cubic','exponential']}
Q = '''[* {:question/difficulty [:db/id :db/ident]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'''
QUERY = '[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data'])
    return x['data']

def counts(path):
    request={'database':'math','learner':LEARNER,'topics':[17592186049380],'activity_type':'lesson','after_basis':None,'lineage':None,'at':None}
    r = subprocess.run([str(DISCOVERY)],input=json.dumps(request),env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout)
    assert x['cursor']['lineage']==LINEAGE
    save(path,x)
    pools=[kp for t in x['topics'] for kp in t['knowledge_points'] if kp['db/id']==KP]
    assert len(pools)==1
    return x['basis'],pools[0]['inventory']['available']

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



def fingerprint(q):
    prompt=q[':question/problem']
    if r'\frac{\text{d}y}{\text{d}x}' in prompt:
        derivative=v.ode(prompt)
    else:
        match=re.search(r"y'\s*=\s*(.*?)\$",prompt)
        assert match, prompt
        derivative=v.parse(match[1].strip().rstrip(',.'))
    return g.digest([s.srepr(s.expand(s.simplify(derivative))), 'x>0' if 'x>0' in prompt else 'real'])

def replace_paths(obj,mapping):
    if isinstance(obj,dict):return {mapping.get(k,k):replace_paths(val,mapping) for k,val in obj.items()}
    if isinstance(obj,list):return [replace_paths(val,mapping) for val in obj]
    if isinstance(obj,str):
        for old,new in mapping.items():obj=obj.replace(old,new)
    return obj

def check(rec):
    assert rec['knowledge_point']==g.KP
    meta=rec['generation'];assert meta['bank_profile']=='authored-five-family' and meta['eligible_for_learning'] and not meta['evidence_only']
    replay=g.generate(meta['level'],meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
    assert ordered(replay['question'])==ordered(rec['question'])
    assert meta['mathematical_fingerprint']==replay['generation']['mathematical_fingerprint']
    v.verify(rec)

def validate_sources(kp,path,basis):
    old=json.loads((HERE/'source.json').read_text())['record']
    current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    expected={q[':question/math-academy-id']:q for q in old[':knowledge-point/questions']}
    assert set(current)==set(expected),'New source evidence requires reclassification'
    for sid,q in expected.items():assert source_projection(current[sid],q)==q, sid
    assert source_projection(kp[':knowledge-point/canonical-example'],old[':knowledge-point/canonical-example'])==old[':knowledge-point/canonical-example']
    banks=options=0
    for case in g.CASES:
        rec=g.generate(case['level'],17,template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        v.verify(rec,False)
        src=g.SPECS[case['template']]['source'];q=rec['question']
        assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution']
        for sf,rf in zip(src[':question/answer-fields'],q[':question/answer-fields']):
            assert {a[':answer/value'] for a in sf[':answer-field/choices']}=={a[':answer/value'] for a in rf[':answer-field/choices']}
            banks+=1;options+=len(rf[':answer-field/choices'])
            if ':answer-field/correct' in sf:
                correct=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
                assert correct==sf[':answer-field/correct'][':answer/value']
    save(path/'source-validation.json',{'passed':True,'current_basis':basis,'source_basis':1356,'source_questions_unchanged':len(current),'complete_image_banks_replayed':banks,'image_values_matched':options,'raw_metric_uncertainties_excluded_from_learning':True,'raw_replay_is_not_proof_of_inferred_metric_coefficients':True})

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:val for k,val in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:val for k,val in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assets=json.loads((path/'assets.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for asset in assets.values():assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question'])
        assert fingerprint(q)==rec['generation']['inventory_fingerprint']
        check(replace_paths(rec,{a['path']:local for local,a in assets.items()}))
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'asset_bytes_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv,available):
    prep=json.loads((path/'preparation.json').read_text());shortage={l:max(0,5-available[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'source':SOURCE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':available,'shortage_by_level':shortage,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'capability_exceptions':prep['capability_exceptions'],'excluded_profiles':'Raw raster-inference banks are evidence-only; authored-five-family bank is exact and learner-graded.','evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'source-validation.json',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',path/'discovery-after.json',path/'assets.json',path/'generated.json',HERE/'frozen-artifacts.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md')]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level')}),flush=True)

def main():
    frozen=json.loads((HERE/'frozen-artifacts.json').read_text())
    for filename,key in [(HERE.with_suffix('.py'),'generator_sha256'),(HERE/'render.py','renderer_sha256'),(HERE/'validate.py','validator_sha256')]:assert sha(filename)==frozen[key]
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='passed_supported_generation_with_explicit_raw_geometry_uncertainty'
    assert validation['source_field_banks_exact']==12 and validation['source_choice_values_exact']==60
    assert validation['native_report']['documented_unresolved_checks']==0
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application lock acquired.',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                inv=inventory(path/'inventory-after.json');b,available=counts(path/'discovery-after.json');assert inv['basis']==b
                finish(path,intent['generator_id'],verified,inv,available);return
        inv=inventory(OUT/'inventory-before.json');b,available=counts(OUT/'discovery-before.json');assert DB.basis()==inv['basis']==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP['id']
        validate_sources(kp,path,b);(path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP['id']),'question-generator'))
        if gen:assert gen.get(':question-generator/script',SCRIPT)==SCRIPT
        needed={l:max(0,5-available[l]) for l in LEVELS};selected={l:0 for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];attempts={l:0 for l in LEVELS};supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        def select(rec):
            check(rec);level=rec['generation']['level'];fp=fingerprint(rec['question'])
            if selected[level]<needed[level] and fp not in used:
                rec=copy.deepcopy(rec);rec['generation']['inventory_fingerprint']=fp
                records.append(rec);used.add(fp);selected[level]+=1
        for rec in instances:select(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        for level in LEVELS:
            for i in range(400):
                if selected[level]>=needed[level]:break
                template=FAMILIES[level][i%len(FAMILIES[level])]
                rec=g.generate(level,seed=i,template=template);attempts[level]+=1;select(rec)
        exceptions=[{'level':l,'missing':needed[l]-selected[l],'attempt_limit':400,'evidence':'Bounded search exhausted; finite sampler documented in validation.json; no aliases admitted.'} for l in LEVELS if selected[l]<needed[l]]
        print(json.dumps({'basis':b,'available':available,'needed':needed,'selected':selected}),flush=True)
        for attribute,ids in (('question/id',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
            if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attribute+' ?id]]',[ids],path,attribute.replace('/','-')+'-collisions',b)
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT
        save(path/'generated-local.json',records)
        subprocess.run(['/usr/bin/python3',str(HERE/'publish_assets.py'),str(path)],check=True)
        records=json.loads((path/'generated.json').read_text())
        save(path/'native-input.json',[v.normal_native(r,r['question'][':question/id']) for r in records])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        native=json.loads((path/'native-report.json').read_text());assert native['documented_unresolved_checks']==0
        (path/'review.md').write_text('# Replenishment variants\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_by_level':available,'missing_by_level':needed,'selected_by_level':selected,'sampling_attempts':attempts,'capability_exceptions':exceptions,'new_questions':len(records),'source_evidence_unchanged':True,'assets':json.loads((path/'assets.json').read_text()),'difficulty_evidence':'Easy/moderate observed; hard authored nonunit rational primitive scale and signed rational exponential rate, direct integration plus graph discrimination. See classification.md.','distinctness':'Printed ODE derivative and real/positive domain; constant choices, seed, order, IDs, plot-bank variations excluded. Current and canonical tasks excluded.'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'by_level':{l:0 for l in LEVELS}}
            save(path/'verification.json',{'passed':True,'no_change':True,**verified});finish(path,gid,verified,inv,available);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0])
        b2,available2=counts(path/'discovery-precommit.json');assert b2==b and available2==available and DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'curve-family-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'generator_version':g.VERSION,'asset_hashes':json.loads((path/'assets.json').read_text()),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);print('Validated preview; saving and submitting exact guarded request.',flush=True)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        inv=inventory(path/'inventory-after.json');after,available=counts(path/'discovery-after.json');assert after==inv['basis']==verified['basis_after']
        finish(path,gid,verified,inv,available)

if __name__=='__main__':main()
