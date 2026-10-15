"""KP-scoped additive inventory publication, using the application's EDB integration."""
import ast
import collections
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

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('scalar_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
KP=g.KP_ID
LEVELS=('easy','moderate','hard')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'68170beec22a1aa27332972c5378c53f42e6d2e5c1bfdbe7c0ac2814c36ae27d'
LINEAGE=g.SOURCE['lineage']
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
OUT=HERE/'reference/replenishment'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
QUERY=(HERE/'reference/source-query.edn').read_text()
# Reuse only the frozen validator's definitions, without executing its output-writing suite.
tree=ast.parse((HERE/'validate.py').read_text())
ns={'g':g,'sp':sp,'re':re,'uuid':uuid,'checks':collections.Counter(),'engine':[]}
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ('independent_prompt','formatting','verify')],type_ignores=[]),str(HERE/'validate.py'),'exec'),ns)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(x):
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items() if k!=':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(x,(list,tuple)):return sorted([clean(v) for v in x],key=lambda v:json.dumps(v,sort_keys=True))
    if isinstance(x,uuid.UUID):return str(x)
    return x

def frozen():
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert freeze['status']=='pass'
    for p,h in freeze['sha256'].items():assert sha(ROOT/p)==h, p
    assert json.loads((HERE/'validation.json').read_text())['status']=='pass'
    return freeze

def inventory(path):
    r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data']);return x['data']

def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

def normalize(q):
    out={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    out[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    out[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return out

def math_task(q):
    # Normalize canonical bold notation only for reading the mathematics.
    p=q[':question/problem'].replace('\\dfrac','\\frac')
    p=re.sub(r'\\mathbf\{([a-z])\}',r'\1',p)
    M,ang,_,_=ns['independent_prompt']({':question/problem':p})
    return (str(sp.simplify(M)) if sp.cos(ang)!=0 else 'incidental_at_right_angle',str(sp.simplify(ang)))

def validate(rec):
    assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
    ns['verify'](rec)
    return ns['engine'][-1] if ':answer-field/correct' in rec['question'][':question/answer-fields'][0] else None

def refresh_sources(kp,path,basis):
    captured=g.SOURCE['record'];byid={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
    for q in captured[':knowledge-point/questions']:assert clean(q)==clean(byid[q[':question/math-academy-id']]), 'Prior source changed'
    assert clean(captured[':knowledge-point/canonical-example'])==clean(kp[':knowledge-point/canonical-example'])
    extra=[];replayed=[];banks=options=0
    for q in kp[':knowledge-point/questions']:
        sid=q.get(':question/math-academy-id')
        if not sid:continue
        profile='observed_'+sid
        if profile not in g.OBSERVED:
            M,ang,a,b=ns['independent_prompt'](q)
            rad=2 if M.has(sp.sqrt(2)) else 3 if M.has(sp.sqrt(3)) else 1
            f=q[':question/answer-fields'][0];kind=str(f[':answer-field/type'][':db/ident']).split('/')[-1]
            s=q.get(':question/worked-solution');style='legacy' if s is None else 'plain_have' if 'we have' in s else 'plain' if 'cos\\,' in s else 'operator'
            meta={'source_id':sid,'template':'legacy_radio' if style=='legacy' else kind+'_'+style,'parameters':{'coefficient':str(sp.simplify(M/sp.sqrt(rad))),'radicand':rad,'angle':int(ang*180/sp.pi),'unit':'radians' if 'pi' in q[':question/problem'] else 'degrees','a':a,'b':b},'ratios':[str(sp.simplify(g.parse_scalar(v[':answer/value'])/M)) for v in f[':answer-field/choices']],'field_key':f[':answer-field/key'],'kind':kind,'style':style,'has_solution':s is not None,'has_difficulty':':question/difficulty' in q,'has_correct':':answer-field/correct' in f,'difficulty':str(q.get(':question/difficulty',{}).get(':db/ident')),'raw_q':q}
            g.OBSERVED[profile]=meta;extra.append(meta)
        rec=g.generate('easy',profile=profile)
        # Complete mathematical bank, presence, exact prompt and solution replay.
        x=rec['question'];assert x[':question/problem']==q[':question/problem'] and x.get(':question/worked-solution')==q.get(':question/worked-solution')
        f=q[':question/answer-fields'][0];gf=x[':question/answer-fields'][0]
        assert gf[':answer-field/type']==f[':answer-field/type'][':db/ident'] and gf[':answer-field/key']==f[':answer-field/key']
        assert sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
        assert (':answer-field/correct' in gf)==(':answer-field/correct' in f)
        if ':answer-field/correct' in gf:
            correct=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert correct==f[':answer-field/correct'][':answer/value']
        validate(rec);banks+=1;options+=len(gf[':answer-field/choices']);replayed.append(rec)
    save(path/'source-refresh.json',{'basis':basis,'lineage':LINEAGE,'old_source_payloads_unchanged':17,'current_sources':banks,'complete_banks_matched':banks,'options_matched':options,'additional_profiles':[{k:v for k,v in m.items() if k!='raw_q'} for m in extra],'new_template_count':0,'plots':'none','historical_profiles_evidence_only':True})
    save(path/'source-replays.json',replayed)
    return {q[':question/math-academy-id'] for q in kp[':knowledge-point/questions'] if q.get(':question/math-academy-id') and q.get(':question/difficulty') and q.get(':question/worked-solution') and all(f.get(':answer-field/correct') for f in q[':question/answer-fields'])}

USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
(or-join [?q ?l]
 (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
  (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
  [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def counts(kp,path,basis,valid_sources,known):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    rows={l:[] for l in LEVELS};tasks={l:set() for l in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        if q.get(':question/math-academy-id') not in valid_sources:
            rec=known.get(str(q[':question/id']))
            if rec is None:excluded.append(str(q[':question/id']));continue
            assert clean(normalize(q))==clean(rec['question']);validate(rec)
        level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        tasks[level].add(math_task(q));rows[level].append(str(q[':question/id']))
    c={'basis':basis,'levels':{l:{'distinct_available_tasks':len(tasks[l]),'available_question_ids':rows[l]} for l in LEVELS},'excluded_shown_or_reserved':sorted(unavailable),'excluded_unrated_incomplete_or_unrecognized':excluded}
    save(path/'available-counts.json',c);return c

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

def report_check(report,path,source):
    attrs=dict((e,str(a)) for e,a in DB.attributes(path,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added, 'Unexpected retraction or attribution'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed, name

def native_check(path):
    source=ROOT/'generate/runs/current/check-engine.rs';deps=ROOT/'target/release/deps'
    libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
    binary=OUT/'check-current-engine'
    if not binary.exists():
        command=['rustc','--edition=2024','-O',str(source),'-L','dependency='+str(deps),'-o',str(binary)]
        for name,p in libs.items():command.extend(['--extern',name+'='+str(p)])
        subprocess.run(command,check=True)
    save(path/'native-input.json',ns['engine'])
    subprocess.run([str(binary),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    save(path/'grader-build.json',{'source':str(source.relative_to(ROOT)),'source_sha256':sha(source),'binary_sha256':sha(binary),'libraries':{n:{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for n,p in libs.items()}})

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    report_check(report,path/'receipt-check',intent['source_eid'])
    b=report[':edb/db-after-t'];kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());known={r['question'][':question/id']:r for r in records};byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert clean(normalize(q))==clean(rec['question']);validate(rec)
    valid=refresh_sources(kp,path/'readback',b)
    c=counts(kp,path/'readback',b,valid,known)
    assert not transaction([],kp,intent['generator_id'])
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified['available_counts_after'];remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'capability_exceptions':[],'unsupported_levels_filled':False,'authored_level_extensions':['moderate','hard'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'source-refresh.json',path/'native-report.json',path/'grader-build.json',path/'inventory-after.json',HERE/'freeze.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json'] if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    save(HERE/'registration.json',{'generator_id':gid,'generator_path':SCRIPT,'version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'verified_basis':verified['basis_after']})
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True);frozen()
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event()) if '--commit' in sys.argv else None
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired',flush=True)
        if '--commit' in sys.argv:
            for path in sorted(OUT.glob('basis-*')):
                if (path/'commit-intent.json').exists():
                    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
                    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n');valid=refresh_sources(kp,path,b)
        existing_records=[]
        for p in OUT.glob('basis-*/generated.json'):existing_records.extend(json.loads(p.read_text()))
        known={r['question'][':question/id']:r for r in existing_records}
        c=counts(kp,path,b,valid,known);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        print(json.dumps({'basis':b,'distinct_available':{l:c['levels'][l]['distinct_available_tasks'] for l in LEVELS},'needed':needed}),flush=True)
        if '--commit' not in sys.argv:return
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        registered=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'registered-generator',b)
        gen=kp.get(':knowledge-point/question-generator') or (registered[0][0] if registered else None);assert len(registered)<=1
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        used={math_task(q) for q in kp[':knowledge-point/questions']};used.add(math_task(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied;assert isinstance(instances,list)
        for rec in instances:validate(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        records=[];added={l:0 for l in LEVELS}
        for level in LEVELS:
            for i in range(2000):
                if added[level]>=needed[level]:break
                rec=g.generate(level,b+i);fp=math_task(rec['question'])
                if fp in used:continue
                assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
                validate(rec);records.append(rec);used.add(fp);added[level]+=1
            assert added[level]==needed[level], 'Bounded generator exhausted; capability exception required'
        ids=[uuid.UUID(i) for rec in records for i in [rec['question'][':question/id'],rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        matches=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',b) if ids else []
        assert not matches,'Identity collision requires reconciliation'
        save(path/'generated.json',records);(path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n');native_check(path)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_new_tasks':len({math_task(r['question']) for r in records}),'asset_hashes':[],'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'frozen_validation_unchanged':True,'source_current_basis':b,'finite_domain_sizes':json.loads((HERE/'validation.json').read_text())['enumerated_mathematical_tasks']})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;report_check(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'scalar-angle-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
