"""One guarded content, generator, and learner-activity repair.

Publication inputs are reviewed before preparation. A saved exact request is
recovered before any fresh preparation; preview IDs never enter logical forms.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher, normalized_question, validate_question
from scripts.generator_packages import resolve_registered_script
from capture.scripts.database.edn import dumps, loads, kw, Tagged

HERE = Path(__file__).resolve().parent
SOURCE = ':agent/gpt-6.1-sol-high'
KP, BAD, RELEVEL = 17592186119771, 17592186487475, 17592186487471
PUBLISHER = Publisher.from_environment(source=SOURCE)
DB = PUBLISHER.client
NATIVE = ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
QUESTION_PULL = '[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]'
KP_PULL = '[:db/id :knowledge-point/id {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/question-generator [:db/id]}]'

def save(path, value):
    path.write_text(json.dumps(value, indent=2, default=str)+'\n')

def canonical(v):
    if isinstance(v, dict): return {str(k): canonical(x) for k,x in v.items()}
    if isinstance(v, (list,tuple)): return sorted((canonical(x) for x in v), key=lambda x:json.dumps(x,sort_keys=True))
    return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)

def read_forms(path, snapshot):
    forms = loads(path.read_text())
    instant = {str(a) for _,a,t in snapshot['attributes'] if str(t)==':db.type/instant'}
    for f in forms:
        if isinstance(f,list) and len(f)>3 and str(f[2]) in instant:
            for i in range(3,len(f)):
                if f[i] is not None: f[i]=Tagged('inst',f[i])
    return forms

def prepare(out, fragment, records_path):
    assert not (out/'commit-intent.json').exists(), 'Recover saved request before preparation'
    package=json.loads((HERE/'published-package.json').read_text())
    assert package['verified']
    resolve_registered_script(package['reference'],ROOT,PUBLISHER.config.math_root)
    records=json.loads(records_path.read_text())
    assert len(records)==4
    for record in records: validate_question(record['question'])
    prepared=PUBLISHER.prepare(KP,records,package['reference'],package['digest'],out/'publication',
        expected_registered_generator='generate/scratch/17592186119771.py')
    refresh=subprocess.run([sys.executable,str(fragment/'prepare.py'),'--basis',str(prepared['basis'])],
        env=DB.environment,capture_output=True,text=True,timeout=150)
    (out/'activity-refresh.stdout').write_text(refresh.stdout)
    (out/'activity-refresh.stderr').write_text(refresh.stderr)
    refresh.check_returncode()
    fragment_plan=json.loads((fragment/'fragment-plan.json').read_text())
    assert fragment_plan['basis']==prepared['basis'], 'Refresh activity replay at current basis'
    snapshot=loads(prepared['snapshot_edn'])
    batch=loads(prepared['batch_edn'])
    kp=loads(prepared['before_edn'])
    ids=sorted(q[':db/id'] for q in kp[':knowledge-point/questions'])
    assert BAD in ids and RELEVEL in ids and prepared['new_questions']==4 and prepared['duplicates']==0
    original=loads((HERE/'capture-3438/snapshot.edn').read_text())
    assert ids==sorted(q[':db/id'] for [q] in original['questions']), 'Reviewed pool changed'
    questions={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    for [q] in original['questions']:
        assert normalized_question(q)==normalized_question(questions[q[':db/id']]), 'Reviewed question changed'
    assert questions[RELEVEL][':question/difficulty'][':db/ident']==':question.difficulty/moderate'
    old_generator=kp[':knowledge-point/question-generator'][':db/id']
    forms=batch['forms']
    for i,f in enumerate(forms):
        if f[:3]==[kw('db/add'),KP,kw('knowledge-point/question-generator')]:
            forms[i]=[kw('db/cas'),KP,kw('knowledge-point/question-generator'),old_generator,f[3]]
    forms.extend([[kw('db/retract'),KP,kw('knowledge-point/questions'),BAD],
        [kw('db/cas'),RELEVEL,kw('question/difficulty'),kw('question.difficulty/moderate'),kw('question.difficulty/easy')],
        [kw('db/ensure'),RELEVEL,kw('question/validate')]])
    forms.extend(read_forms(fragment/'transaction-fragment.edn',snapshot))
    groups=loads((fragment/'native-pulls.edn').read_text())
    groups += [['existing-questions',QUESTION_PULL,ids],['kp',KP_PULL,[KP]],['old-generator','[*]',[old_generator]]]
    (out/'transaction.edn').write_text(dumps(forms)+'\n')
    (out/'native-pulls.edn').write_text(dumps(groups)+'\n')
    sha=hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()
    plan={'database':prepared['database'],'lineage':prepared['lineage'],'basis':prepared['basis'],
        'source':SOURCE,'endpoint':DB.config.endpoint,'snapshot':snapshot,'sha256':sha,
        'transaction_file':str(out/'transaction.edn'),'request_key':f'triangular-quality-b{prepared["basis"]}-{sha}',
        'retired_question':BAD,'releveled_question':RELEVEL,'new_questions':4,'package':package,
        'fragment':str(fragment),'fragment_plan':fragment_plan,'old_generator':old_generator}
    save(out/'plan.json',plan)
    print(json.dumps({'prepared':True,'basis':plan['basis'],'forms':len(forms),'new_questions':4}))

def resolve(v,report,plan):
    idents={str(i):e for e,i in plan['snapshot']['idents']}
    return report[':edb/tempids'].get(v,idents.get(v,v)) if isinstance(v,str) else v

def verify_report(report,plan,committed,forms):
    assert report[':edb/committed'] is committed and report[':edb/db-before-t']==plan['basis']
    attrs={e:str(a) for e,a,t in plan['snapshot']['attributes']}
    types={str(a):str(t) for e,a,t in plan['snapshot']['attributes']}
    source=resolve(SOURCE,report,plan)
    def triple(e,a,v,added):
        a=str(a)
        if types[a]==':db.type/ref':v=resolve(v,report,plan)
        return resolve(e,report,plan),a,dumps(v),added
    expected=set()
    for f in forms:
        op,e,a=str(f[0]),f[1],str(f[2])
        if op==':db/add':expected.add(triple(e,a,f[3],True))
        elif op==':db/retract':expected.add(triple(e,a,f[3],False))
        elif op==':db/cas':
            if f[3] is not None:expected.add(triple(e,a,f[3],False))
            if f[4] is not None:expected.add(triple(e,a,f[4],True))
        else:assert op==':db/ensure',op
    observed=set()
    for e,a,v,tx,s,added in report[':edb/tx-data']:
        assert s==source
        if attrs[a]==':db/txInstant':assert added
        else:observed.add(triple(e,attrs[a],v,added))
    assert observed==expected,(observed-expected,expected-observed)

def expected_after(before,forms,report,plan):
    result=copy.deepcopy(before)
    types={str(a):str(t) for _,a,t in plan['snapshot']['attributes']}
    idents={e:str(i) for e,i in plan['snapshot']['idents']}
    def walk(v):
        if isinstance(v,list):
            for x in v:walk(x)
        elif isinstance(v,dict):
            eid=v.get(':db/id')
            for f in forms:
                op,e,a=str(f[0]),resolve(f[1],report,plan),str(f[2])
                if op==':db/ensure' or eid!=e:continue
                old=v.get(a)
                if op==':db/retract':
                    if isinstance(old,list):
                        v[a]=[x for x in old if x.get(':db/id')!=resolve(f[3],report,plan)]
                        if not v[a]:v.pop(a)
                    elif a in v:v.pop(a)
                elif op==':db/cas' and a in v:
                    value=f[4]
                    if value is None:v.pop(a)
                    elif types[a]==':db.type/ref':
                        rid=resolve(value,report,plan);v[a]={':db/id':rid}
                        if isinstance(old,dict) and ':db/ident' in old:v[a][':db/ident']=idents[rid]
                    else:v[a]=value
                elif op==':db/add' and a in v and isinstance(old,list) and types[a]==':db.type/ref':
                    old.append({':db/id':resolve(f[3],report,plan)})
            for x in v.values():walk(x)
    walk(result)
    return result

def preview(out):
    plan=json.loads((out/'plan.json').read_text());forms=loads((out/'transaction.edn').read_text())
    run=subprocess.run([str(NATIVE),str(out),SOURCE,str(plan['basis'])],env=DB.environment,capture_output=True,text=True,timeout=150)
    (out/'preview.stderr').write_text(run.stderr);run.check_returncode();(out/'preview.edn').write_text(run.stdout)
    report=loads(run.stdout);verify_report(report,plan,False,forms)
    for name,_,_ in loads((out/'native-pulls.edn').read_text()):
        before=loads((out/f'preview-{name}-before.edn').read_text());after=loads((out/f'preview-{name}-after.edn').read_text())
        assert canonical(expected_after(before,forms,report,plan))==canonical(after),name
    save(out/'preview-verification.json',{'passed':True,'only_planned_datoms':True,'existing_content_and_archived_responses_preserved':True})
    print('Native data preview passed')

def commit(out):
    plan=json.loads((out/'plan.json').read_text());forms=loads((out/'transaction.edn').read_text())
    assert json.loads((out/'preview-verification.json').read_text())['passed']
    app=json.loads((out/'application-preview.json').read_text())
    assert app['passed'] and app['basis_before']==plan['basis'] and app['transaction_sha256']==plan['sha256']
    assert hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()==plan['sha256']
    assert DB.status()['lineage']==plan['lineage']
    intent=out/'commit-intent.json'
    if intent.exists():assert json.loads(intent.read_text())==plan
    else:save(intent,plan)
    receipt=out/'receipt.edn'
    if not receipt.exists():receipt.write_text(DB.command('transact','--source',SOURCE,'--file',plan['transaction_file'],
        '--basis',plan['basis'],'--endpoint',plan['endpoint'],'--request-key',plan['request_key'],'--timeout-ms','120000',timeout=150))
    report=loads(receipt.read_text());verify_report(report,plan,True,forms)
    after_basis=report[':edb/db-after-t']
    def check(group):
        name,pattern,ids=group
        for basis,stage in [(plan['basis'],'before'),(after_basis,'after')]:
            rows=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[ids],out/'readback',name+'-'+stage,basis) if ids else []
            assert canonical([e for [e] in rows])==canonical(loads((out/f'preview-{name}-{stage}.edn').read_text())),name
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(check,loads((out/'native-pulls.edn').read_text())))
    prepared=json.loads((out/'publication/preparation.json').read_text())
    question_ids=[report[':edb/tempids'][r['question'][':question/id']] for r in prepared['records']]
    rows=DB.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[question_ids],out/'readback','new-questions',after_basis)
    assert canonical([normalized_question(q) for [q] in rows])==canonical([normalized_question(r['question']) for r in prepared['records']])
    generator_id=report[':edb/tempids']['generator']
    registration=DB.query('[:find (pull ?g [*]) :in $ ?g :where [?g :question-generator/id _]]',[generator_id],out/'readback','new-generator',after_basis)[0][0]
    assert registration[':question-generator/script']==plan['package']['reference'] and str(registration[':question-generator/id'])==prepared['generator_id']
    result={'committed':True,'basis_before':plan['basis'],'basis_after':after_basis,
        'retired_question':BAD,'releveled_question':RELEVEL,'new_questions':question_ids,
        'new_generator':generator_id,'package':plan['package']['reference'],
        'activity_repaired':True,'accuracy_replayed':True,'original_records_retained':True,
        'exact_committed_and_historical_readback':True,'request_key':plan['request_key']}
    save(out/'verification.json',result);save(HERE/'verification.json',result);print(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','preview','commit']);p.add_argument('--attempt',required=True)
    p.add_argument('--fragment',type=Path);p.add_argument('--records',type=Path);a=p.parse_args()
    out=HERE/a.attempt;out.mkdir(exist_ok=True)
    if a.action=='prepare':prepare(out,a.fragment,a.records)
    else:globals()[a.action](out)
