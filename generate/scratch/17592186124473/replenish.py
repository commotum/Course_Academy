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
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '82ca9ac70fd95580c039d442dbc6d71c42a83c364bf7a6f213036d82ee709864'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent / 'EDB')
QUERY = (HERE / 'reference/source-query.edn').read_text()

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

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID): return str(value)
    return value

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

LEVELS=('easy','moderate','hard')
USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def checks(rec):
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],
             'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
             'purpose':'Correct and incorrect owned choices through actual learner grade_field'}
            for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def strong_fingerprint(rec):
    from fractions import Fraction
    m=rec['generation'];p=m['parameters'];template=m['template']
    return json.dumps([template,str(Fraction(p['right'],p['left'])),
        str(Fraction(p['mid'],p['left'])) if template in ('two_turns','union_ranges','disconnected_ranges','plateau_union') else None,
        p['closure'] if template!='plateau_union' else None],separators=(',',':'))

def validate_instance(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.REC[':knowledge-point/id']
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    assert rec['generation']['version']==g.VERSION
    v.normalcheck(rec)
    # Replay all rendered content and owned identities from exact saved inputs.
    m=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
    replay=g.generate(level,m['seed'],template=m['template'],parameters=m['parameters'])
    rp=replay['question']
    expected=copy.deepcopy(q)
    expected[':question/problem']=expected[':question/problem'].replace(m.get('published_plot',m['plot']),m['plot'])
    assert ordered(rp)==ordered(expected),'Replay mismatch'
    return strong_fingerprint(rec)

def source_check(q):
    mid=q.get(':question/math-academy-id')
    assert mid in g.QUESTIONS
    fields=q[':question/answer-fields'];requested=v.promptsets(q)
    if requested:
        assert len(fields)==3
        bits=[v.independent_hlt(g.LANDMARKS[mid],ss) for ss in requested]
        bykey={f[':answer-field/key']:f for f in fields}
        assert set(bykey)=={'I','II','III'}
        for key,bit in zip(('I','II','III'),bits):
            f=bykey[key];assert str(f[':answer-field/type'][':db/ident'])==':answer-field.type/checkbox'
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
            assert f[':answer-field/correct'][':answer/value']==str(bit).lower()
    else:
        f=fields[0];values=[a[':answer/value'] for a in f[':answer-field/choices']]
        sets=[v.parse(x) for x in values];valid=[v.independent_hlt(g.LANDMARKS[mid],ss) for ss in sets]
        eligible=[valid[i] and all(not valid[j] or g.spset(t).is_subset(g.spset(ss)) for j,t in enumerate(sets)) for i,ss in enumerate(sets)]
        assert len(values)==5 and sum(eligible)==1
        assert values[eligible.index(True)]==f[':answer-field/correct'][':answer/value']
    assert q[':question/worked-solution']

def counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage-history',basis,history=True))
    byid={r['question'][':question/id']:r for d in OUT.glob('basis-*') if (d/'generated.json').exists() for r in json.loads((d/'generated.json').read_text())}
    available={x:set() for x in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or level not in LEVELS:
            excluded.append({'db_id':q[':db/id'],'reason':'Shown, reserved, canonical or unrated'});continue
        try:
            if q.get(':question/math-academy-id'):
                if q[':question/math-academy-id'] in ('q-108791','q-108795','q-36061'):
                    raise ValueError('Largest-domain/interval wording has incomparable global injective alternatives; original preserved, excluded from conservative validated reserve')
                source_check(q);fp='source:'+q[':question/math-academy-id']
            else:
                r=copy.deepcopy(byid[str(q[':question/id'])]);assert normalize(q)==ordered(r['question']);fp=validate_instance(r)
            available[level].add(fp)
        except (AssertionError,ValueError,KeyError,TypeError) as e:
            excluded.append({'db_id':q[':db/id'],'reason':'Unvalidated current content: '+str(e)})
    result={'basis':basis,'distinct_available':{k:len(s) for k,s in available.items()},'fingerprints':{k:sorted(s) for k,s in available.items()},'unavailable':sorted(unavailable),'excluded':excluded}
    save(path/'available-counts.json',result);return result

def freeze_check():
    proof=json.loads((HERE/'validation.json').read_text())
    assert proof['status']=='pass_with_explicit_source_limits'
    freeze=json.loads((HERE/'replenishment-freeze.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in freeze['hashes'].items())


def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items()),'Existing question changed'
    ignore={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in ignore}=={k:v for k,v in kp.items() if k not in ignore}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);validate_instance(rec)
    assert not transaction([],kp,intent['generator_id'])
    stock=counts(path/'readback',kp,report[':edb/db-after-t'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),
        'by_level':{x:sum(r['question'][':question/difficulty']==':question.difficulty/'+x for r in records) for x in LEVELS},
        'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,
        'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,
        'available_counts_after':stock}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    after=verified.get('available_counts_after') or counts(path/'readback',read_kp(path/'readback',verified['basis_after']),verified['basis_after'])
    shortages={x:max(0,5-after['distinct_available'][x]) for x in LEVELS}
    caps=json.loads((HERE/'capabilities.json').read_text())
    result={'outcome':'finite-limit' if any(shortages.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,
        'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],
        'new_questions_by_level':verified.get('by_level',{}),'supported_levels':list(LEVELS),'unsupported_levels':[],
        'available_by_level':after['distinct_available'],'shortage_by_level':shortages,'capability_exceptions':caps['exceptions'],
        'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
        'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'validation.json',HERE/'current-source-validation.json',HERE/'replenishment-freeze.json',HERE/'capabilities.json',path/'generated.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'native-report.json',path/'inventory-after.json') if p.exists()],
        'note':'Exact affine graph questions; checkbox subset fields match current sources. Underidentified raster reconstructions remain ineligible. Current source questions, canonical example and learner history preserved. Label permutations, shifts, reflections, seed changes and choice order do not establish distinct tasks.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level','remaining_jobs')}),flush=True)

def main():
    freeze_check()
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    from capture.scripts.database.images import ImageLibrary
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.REC[':knowledge-point/id']
        captured=json.loads((HERE/'current-source.json').read_text())['record']
        old={q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
        current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for mid,q in old.items():assert canonical(q)==canonical(current[mid]),'Current source changed; reclassify '+mid
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        registered=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-identity',b)
        if registered:
            assert len(registered)==1
            if gen:assert gen==registered[0][0]
            else:gid=str(registered[0][0][':question-generator/id'])
        stock=counts(path,kp,b);jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
        needed={x:max(0,5-stock['distinct_available'][x],jobs.get(x,{}).get('missing',0)) for x in LEVELS}
        used=set().union(*[set(s) for s in stock['fingerprints'].values()])
        # Exclude all previously authored mathematics, even if exhausted.
        for d in OUT.glob('basis-*'):
            if (d/'generated.json').exists():used.update(strong_fingerprint(r) for r in json.loads((d/'generated.json').read_text()))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        eligible=[];rejected=[]
        for rec in instances:
            try:validate_instance(rec);eligible.append(rec)
            except (AssertionError,ValueError,KeyError,TypeError) as e:rejected.append({'question_id':rec.get('question',{}).get(':question/id'),'reason':str(e)})
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated':len(eligible),'rejected':rejected,'generator_error':supplied.get('generatorError')})
        local=json.loads((HERE/'replenishment-candidates.json').read_text());added={x:0 for x in LEVELS};records=[]
        for rec in eligible+local:
            fp=validate_instance(rec);level=rec['question'][':question/difficulty'].split('/')[-1]
            if added[level]<needed[level] and fp not in used:
                records.append(copy.deepcopy(rec));used.add(fp);added[level]+=1
        images=ImageLibrary(Path('/media/jake/SSD/EDB/math'),HERE)
        for rec in records:
            q=rec['question'];original=rec['generation']['plot']
            for key in (':question/problem',':question/worked-solution'):q[key]=images.text(q[key])
            rec['generation']['published_plot']=images.resolve(original)
            validate_instance(rec)
        save(path/'generated.json',records);save(path/'asset-manifest.json',images.saved)
        # All stable question, field and field-owned answer UUIDs are looked up at the guarded basis.
        for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(x) for x in values]],path/'identity-check',attr.replace('/','-'),b),'Unexpected identity collision'
        native=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
        save(path/'native-input.json',native);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_path':SCRIPT,'missing_by_level':needed,'new_by_level':added,'available_counts':stock,'distinct_generated_tasks':len({strong_fingerprint(r) for r in records}),'assets':images.saved,'current_source_unchanged':True,'finite_remaining':{x:max(0,needed[x]-added[x]) for x in LEVELS}})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'available_counts_after':stock,'passed':True,'no_changes':True};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'invertibility-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()
