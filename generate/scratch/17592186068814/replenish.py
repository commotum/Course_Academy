"""Scoped additive replenishment with retained requests and exact-basis readback."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '98f5f44ad1972a9f5929b7fd3f2fbc5f2719f8711ea0b32e48d61b7c77038322'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY = (OUT / 'source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

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

def fingerprint(q):
    return str(v.printed({**q, ':question/problem':q[':question/problem'].replace('\\dfrac','\\frac')}))

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
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
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

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every field-owned graph choice'} for a in f[':answer-field/choices']]

def native(records,path,name):
    save(path/(name+'-input.json'),[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/(name+'-input.json')),str(path/(name+'-report.json'))],check=True)
    x=json.loads((path/(name+'-report.json')).read_text())
    assert x['documented_unresolved_checks']==0 and x['accepted_checks']==len(records) and x['rejected_checks']==4*len(records)
    return x

def supplemental(kp,path):
    from fractions import Fraction
    from PIL import Image
    import re
    supplement=json.loads((OUT/'source-supplement.json').read_text())
    qs={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
    report=[]
    for mid,old in supplement['questions'].items():
        q=qs[mid];assert canonical(q)==canonical(old)
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        profile=supplement['profiles'][mid];p=supplement['parameters'][mid]
        r=g.generate(level,2745,parameters=p,profile=profile);v.check(r)
        actual=[Fraction(c) for c in supplement['coefficients'][mid]]
        generated=list(map(Fraction,r['generation']['plot_coefficients'].values()))
        assert sorted(actual)==sorted(generated) and len(set(actual))==5
        f=q[':question/answer-fields'][0];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        assert actual[ci]==v.printed(q)==v.printed(r['question'])
        assets=[]
        for link in [a[':answer/value'] for a in f[':answer-field/choices']]+re.findall(r'!\[\]\(([^)]+)\)',q[':question/worked-solution']):
            asset=Path('/media/jake/SSD/EDB/math')/link
            assert asset.exists() and Image.open(asset).size==(360,304)
            assets.append({'path':link,'sha256':sha(asset)})
        save(path/(mid+'-replay.json'),{'source':canonical(q),'generated':r,'source_coefficients_in_stored_order':list(map(str,actual)),'all_five_mathematical_objects_and_correct_designation_match':True,'assets':assets})
        report.append({'source':mid,'template':r['generation']['template'],'profile':profile,'complete_banks_matched':1,'options_matched':5,'distractors_matched':4,'prompt_form':'same negative reciprocal graph selection','solution_stages':'negative unit reciprocal then positive vertical scaling','native_pixel_review':'reference/replenishment/new-sources.png; final -5/x solution image also viewed'})
    save(path/'supplemental-validation.json',{'passed':True,'source_basis':2745,'new_sources':report,'total_source_banks_with_original_validation':11,'total_source_options_with_original_validation':55,'unsupported_hard_excluded':True})

def counts(kp,path,basis):
    # Current task membership reserves questions, and retained presentations never
    # return to inventory even if detached from a current task later.
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    hist='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
      [?l :learner/activity ?t] [?t :learner-task/items ?i]
      [?i :task-item/content ?q] [?kp :knowledge-point/questions ?q]]'''
    unavailable.update(r[0] for r in DB.query(hist,[KP,LEARNER],path,'historical-presentations',basis,history=True))
    rows={l:[] for l in g.SUPPORTED_LEVELS}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if level not in rows or not q.get(':question/worked-solution'):continue
        fs=q.get(':question/answer-fields',[])
        if len(fs)!=1 or not fs[0].get(':answer-field/correct'):continue
        rows[level].append(q)
    c={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fingerprint(q) for q in qs}),'question_uuids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'unrated_and_incomplete_excluded':True}
    save(path/'available-counts.json',c);return c

def publish(records,path):
    from capture.scripts.database.images import ImageLibrary
    import re
    lib=ImageLibrary(Path('/media/jake/SSD/EDB/math'),ROOT)
    mapping={}
    for rec in records:
        q=rec['question'];paths=[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
        paths+=re.findall(r'!\[\]\(([^)]+)\)',q[':question/worked-solution'])
        for value in paths:
            mapping[value]=lib.resolve(value)
    def rewrite(x):
        if isinstance(x,dict):return {mapping.get(k,k):rewrite(vv) for k,vv in x.items()}
        if isinstance(x,list):return [rewrite(y) for y in x]
        if isinstance(x,str):
            for old,new in mapping.items():x=x.replace(old,new)
        return x
    result=rewrite(records)
    for data in lib.saved.values():assert sha(Path('/media/jake/SSD/EDB/math')/data['path'])==data['sha256']
    save(path/'asset-map.json',lib.saved)
    save(path/'asset-rewrites.json',mapping)
    return result

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(canonical(now[e])==canonical(q) for e,q in old.items())
    assert canonical({k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);v.check(rec)
    for item in json.loads((path/'asset-map.json').read_text()).values():assert sha(Path('/media/jake/SSD/EDB/math')/item['path'])==item['sha256']
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());caps=json.loads((HERE/'capabilities.json').read_text())
    after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(g.SUPPORTED_LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels_filled':False,'unsupported_nominal_shortage':{'hard':5},'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'source-native-report.json',path/'generated-native-report.json',path/'supplemental-validation.json',path/'inventory-after.json',HERE/'classification-current.md',HERE/'validation.json',HERE/'capabilities.json'] if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass'
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    # One serial application worker owns basis-dependent preparation, publication,
    # submission, receipt verification and inventory readback through this lock.
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured=loads((OUT/'initial-kp.edn').read_text());current={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
        for q in captured[':knowledge-point/questions']:assert canonical(current[str(q[':question/id'])])==canonical(q),'Source changed; reclassify'
        assert canonical(kp[':knowledge-point/canonical-example'])==canonical(captured[':knowledge-point/canonical-example'])
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        assert gid==g.GENERATOR_UUID
        supplemental(kp,path)
        sources=[{'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':normalize(q),'generation':{'source':q.get(':question/math-academy-id')}} for q in kp[':knowledge-point/questions'] if q.get(':question/difficulty') and q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/correct')]
        native(sources,path,'source-native')
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));records=[];added={l:0 for l in g.SUPPORTED_LEVELS}
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for rec in instances:v.check(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        candidates=list(instances)
        for level in g.SUPPORTED_LEVELS:
            if not needed[level]:continue
            for seed in range(200):
                if len({fingerprint(r['question']) for r in candidates if r['question'].get(':question/difficulty')==':question.difficulty/'+level})>=needed[level]+len(used):break
                candidates.append(g.generate(level,seed+2745))
        for rec in candidates:
            level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            if level in added and added[level]<needed[level] and fp not in used:
                assert not rec['generation'].get('evidence_only');v.check(rec);records.append(rec);used.add(fp);added[level]+=1
        save(path/'drafts.json',records)
        records=publish(records,path)
        ids=[uuid.UUID(qid) for rec in records for qid in [rec['question'][':question/id'],rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        existing=DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing,'Existing identities require reconciliation'
        save(path/'generated.json',records);native(records,path,'generated-native')
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),'asset_hashes':json.loads((path/'asset-map.json').read_text()),'source_evidence_unchanged':True,'source_basis':2745,'generator_sha256':sha(HERE.with_suffix('.py')),'validated_script_sha256':sha(HERE/'validate.py'),'source_bank_replay':'9 original complete banks plus 2 supplemental complete banks; 55/55 options, 9/9 present correct designations; 2 missing designations preserved','hard_excluded':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'negative-reciprocal-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
