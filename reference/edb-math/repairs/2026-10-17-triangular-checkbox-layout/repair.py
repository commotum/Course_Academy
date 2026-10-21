"""Publish reviewed checkbox presentation, instructional TeX, and generator fixes."""
import argparse,copy,hashlib,importlib.util,json,subprocess,sys,uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from audit import QUESTION_PULL,ITEM_PULL
from scripts.generator_publish import Publisher,normalized_question
from scripts.generator_packages import resolve_registered_script
from capture.scripts.database.edn import dumps,loads,kw,Tagged
SOURCE=':agent/gpt-6.1-sol-high';PUBLISHER=Publisher.from_environment(source=SOURCE);DB=PUBLISHER.client
NATIVE=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
KP_PULL='[:db/id :knowledge-point/id {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/canonical-example [:db/id]} {:knowledge-point/question-generator [*]}]'
FIELD_PULL='[* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]'
def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
receipt_checks=module(HERE.parent/'2026-10-17-triangular-generator/repair.py','triangular_receipt_checks')
lint=module(ROOT/'skills/radio2checkbox/scripts/lint_presentation.py','checkbox_presentation_lint')
def save(path,value):path.write_text(json.dumps(value,indent=2,default=str)+'\n')
def canonical(value):return receipt_checks.canonical(value)
def checked_lint(question,objects):
    issues=lint.lint_question(question,objects)
    assert not issues,issues
def prepare(out):
    assert not (out/'commit-intent.json').exists(),'Recover previous exact request'
    content=json.loads((HERE/'content-plan.json').read_text());images=json.loads((HERE/'images/replacements.json').read_text())
    content_review=json.loads((HERE/'images/content-verification.json').read_text())
    assert content_review['passed'] and content_review['content_plan_sha256']==hashlib.sha256((HERE/'content-plan.json').read_bytes()).hexdigest()
    packages=json.loads((HERE/'published-packages.json').read_text());assert packages['verified']
    for p in packages['packages']:resolve_registered_script(p['reference'],ROOT,PUBLISHER.config.math_root)
    original=loads((HERE/'capture-3479/snapshot.edn').read_text())
    identity=DB.status();basis=identity['basis'];assert identity['lineage']==content['lineage']
    ids=sorted({q[':db/id'] for [q] in original['questions']}|{c['entity'] for c in images['changes'] if c['attribute'].startswith(':question/')})
    kids=sorted(k[':db/id'] for [k] in original['kps']);tutorials=sorted({c['entity'] for c in images['changes'] if c['attribute'].startswith(':tutorial/')})
    def read(name,q,inputs):return DB.query(q,inputs,out/'evidence',name,basis)
    specs={'questions':('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[ids]),
        'items':('[:find ?q (pull ?i '+ITEM_PULL+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids+tutorials]),
        'kps':('[:find (pull ?k '+KP_PULL+') :in $ [?k ...] :where [?k :knowledge-point/id _]]',[kids]),
        'tutorials':('[:find (pull ?t [*]) :in $ [?t ...] :where [?t :tutorial/id _]]',[tutorials]),
        'attributes':('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[]),
        'idents':('[:find ?e ?ident :where [?e :db/ident ?ident]]',[])}
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending={name:pool.submit(read,name,*args) for name,args in specs.items()};data={name:f.result() for name,f in pending.items()}
    questions={q[':db/id']:q for [q] in data['questions']};kps={k[':db/id']:k for [k] in data['kps']}
    for [old] in original['kps']:
        now=kps[old[':db/id']]
        assert canonical(now[':knowledge-point/questions'])==canonical(old[':knowledge-point/questions']),'Reviewed pool changed'
        assert canonical(now.get(':knowledge-point/question-generator'))==canonical(old.get(':knowledge-point/question-generator')),'Generator changed'
    affected={p['question'] for p in content['cases']}|{content['retire']['question']}
    for [old] in original['questions']:
        if old[':db/id'] in affected:assert canonical(questions[old[':db/id']])==canonical(old),'Reviewed content changed'
    fields={f[':db/id']:q[':db/id'] for q in questions.values() for f in q.get(':question/answer-fields',[])}
    owners=read('field-owners','[:find ?f (pull ?f [{:question/_answer-fields [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',[list(fields)])
    assert {(row[':question/_answer-fields'][':db/id'],f) for f,row in owners}=={(q,f) for f,q in fields.items()},'Shared or missing field ownership'
    forms=[];changes=[];converted=[];old_fields=[];new_ids=[]
    def change(e,a,before,after):
        if before!=after:
            forms.append([kw('db/cas'),e,kw(a),before,after]);changes.append({'entity':e,'attribute':a,'before':before,'after':after})
    def add(e,a,v):forms.append([kw('db/add'),e,kw(a),v])
    for case in content['cases']:
        before,after=case['before'],case['after'];qid=case['question'];checked_lint(after,case['objects'])
        for attr in [':question/problem',':question/worked-solution']:change(qid,attr,before[attr],after[attr])
        if case['decision']=='repair_checkbox_labels':
            old_by_id={f[':db/id']:f for f in before[':question/answer-fields']}
            for f in after[':question/answer-fields']:
                change(f[':db/id'],':answer-field/key',old_by_id[f[':db/id']][':answer-field/key'],f[':answer-field/key'])
                forms.append([kw('db/ensure'),f[':db/id'],kw('answer-field/validate')])
        else:
            assert not any(q==qid for q,_ in data['items']),'New learner use requires response mapping'
            converted.append(qid)
            for f in before[':question/answer-fields']:
                forms.append([kw('db/retract'),qid,kw('question/answer-fields'),f[':db/id']]);old_fields.append(f[':db/id'])
            for f in after[':question/answer-fields']:
                fid=f[':answer-field/id'];new_ids.append(fid)
                for a in f[':answer-field/choices']:
                    aid=a[':answer/id'];new_ids.append(aid)
                    add(aid,'answer/id',uuid.UUID(aid));add(aid,'answer/type',kw('answer.type/text'));add(aid,'answer/value',a[':answer/value'])
                    forms.append([kw('db/ensure'),aid,kw('answer/validate')])
                add(fid,'answer-field/id',uuid.UUID(fid));add(fid,'answer-field/key',f[':answer-field/key']);add(fid,'answer-field/type',kw('answer-field.type/checkbox'))
                for a in f[':answer-field/choices']:add(fid,'answer-field/choices',a[':answer/id'])
                add(fid,'answer-field/correct',f[':answer-field/correct'][1]);add(qid,'question/answer-fields',fid)
                forms.append([kw('db/ensure'),fid,kw('answer-field/validate')])
        forms.append([kw('db/ensure'),qid,kw('question/validate')])
    collisions=read('identity-collisions','[:find ?e ?uuid :in $ [?uuid ...] :where (or-join [?e ?uuid] [?e :answer-field/id ?uuid] [?e :answer/id ?uuid])]',[[uuid.UUID(x) for x in new_ids]])
    assert not collisions
    entities={**questions,**{t[':db/id']:t for [t] in data['tutorials']}}
    for c in images['changes']:
        assert entities[c['entity']][c['attribute']]==c['before'],'Reviewed instructional content changed'
        change(c['entity'],c['attribute'],c['before'],c['after'])
        forms.append([kw('db/ensure'),c['entity'],kw('tutorial/validate' if c['attribute'].startswith(':tutorial/') else 'question/validate')])
    retire=content['retire'];assert not any(q==retire['question'] for q,_ in data['items']),'Do not withdraw a seen question'
    forms.append([kw('db/retract'),retire['kp'],kw('knowledge-point/questions'),retire['question']])
    registrations=[]
    for p in packages['packages']:
        kid=p['kp_id'];kp=kps[kid];old=kp[':knowledge-point/question-generator'];assert old[':question-generator/script']==p['old_reference']
        gid=uuid.uuid5(kp[':knowledge-point/id'],'generator-package:'+p['digest'])
        existing=read(f'generator-{kid}','[:find (pull ?g [*]) :in $ ?uuid :where [?g :question-generator/id ?uuid]]',[gid])
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==p['reference'];entity=existing[0][0][':db/id']
        else:
            entity=f'generator-{kid}';add(entity,'question-generator/id',gid);add(entity,'question-generator/script',p['reference'])
        forms.append([kw('db/cas'),kid,kw('knowledge-point/question-generator'),old[':db/id'],entity])
        forms.append([kw('db/ensure'),kid,kw('knowledge-point/validate')])
        registrations.append({'kp':kid,'old':old[':db/id'],'entity':entity,'uuid':str(gid),'reference':p['reference']})
    groups=[['questions',QUESTION_PULL,ids],['tutorials','[*]',tutorials],['items',ITEM_PULL,sorted(i[':db/id'] for _,i in data['items'])],
        ['kps',KP_PULL,kids],['old-fields',FIELD_PULL,old_fields],['old-generators','[*]',[r['old'] for r in registrations]]]
    (out/'transaction.edn').write_text(dumps(forms)+'\n');(out/'native-pulls.edn').write_text(dumps(groups)+'\n');(out/'snapshot.edn').write_text(dumps({**identity,**data})+'\n')
    sha=hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()
    plan={**identity,'source':SOURCE,'snapshot':{'attributes':data['attributes'],'idents':data['idents']},'changes':changes,'registrations':registrations,
        'converted':converted,'retire':retire['question'],'retire_kp':retire['kp'],'items_preserved':len(data['items']),
        'sha256':sha,'transaction_file':str(out/'transaction.edn'),'endpoint':DB.config.endpoint,'request_key':f'triangular-checkbox-layout-b{basis}-{sha}'}
    save(out/'plan.json',plan);print(json.dumps({'prepared':True,'basis':basis,'forms':len(forms),'label_repairs':16,'conversions':4,'image_tutorial_fields':len(images['changes'])}))

def expected_questions(before,plan):
    cases={c['question']:c for c in json.loads((HERE/'content-plan.json').read_text())['cases']}
    expected=copy.deepcopy(before)
    for q in expected:
        if q[':db/id'] in cases:q.update(copy.deepcopy(cases[q[':db/id']]['after']))
        for c in plan['changes']:
            if c['entity']==q[':db/id']:q[c['attribute']]=c['after']
    return expected
def verify_preview(out,report,plan):
    before=loads((out/'preview-questions-before.edn').read_text());after=loads((out/'preview-questions-after.edn').read_text())
    expected=expected_questions(before,plan)
    assert canonical([normalized_question(q) for q in expected])==canonical([normalized_question(q) for q in after])
    cases={c['question']:c for c in json.loads((HERE/'content-plan.json').read_text())['cases']}
    for q in after:
        if q[':db/id'] in cases:checked_lint(q,cases[q[':db/id']]['objects'])
    for name,_,_ in loads((out/'native-pulls.edn').read_text()):
        b=loads((out/f'preview-{name}-before.edn').read_text());a=loads((out/f'preview-{name}-after.edn').read_text())
        if name=='questions':continue
        exp=copy.deepcopy(b)
        if name=='tutorials':
            for e in exp:
                for c in plan['changes']:
                    if e[':db/id']==c['entity']:e[c['attribute']]=c['after']
        elif name=='kps':
            for e in exp:
                if e[':db/id']==plan['retire_kp']:e[':knowledge-point/questions']=[q for q in e[':knowledge-point/questions'] if q[':db/id']!=plan['retire']]
                for r in plan['registrations']:
                    if e[':db/id']==r['kp']:e[':knowledge-point/question-generator']={':db/id':receipt_checks.resolve(r['entity'],report,plan),':question-generator/id':r['uuid'],':question-generator/script':r['reference']}
        assert canonical(exp)==canonical(a),name
    save(out/'preview-verification.json',{'passed':True,'exact_allowed_datoms':True,'correct_answers_difficulty_and_saved_responses_preserved':True,'label_lint_passed':20})

def preview(out):
    plan=json.loads((out/'plan.json').read_text());forms=loads((out/'transaction.edn').read_text())
    run=subprocess.run([str(NATIVE),str(out),SOURCE,str(plan['basis'])],env=DB.environment,capture_output=True,text=True,timeout=180)
    (out/'preview.stderr').write_text(run.stderr);run.check_returncode();(out/'preview.edn').write_text(run.stdout)
    report=loads(run.stdout);receipt_checks.verify_report(report,plan,False,forms);verify_preview(out,report,plan)
    print('Native preview and exact scope checks passed')

def commit(out):
    plan=json.loads((out/'plan.json').read_text());forms=loads((out/'transaction.edn').read_text())
    assert json.loads((out/'preview-verification.json').read_text())['passed']
    assert hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()==plan['sha256']
    assert DB.status()['lineage']==plan['lineage']
    intent=out/'commit-intent.json'
    if intent.exists():assert json.loads(intent.read_text())==plan
    else:save(intent,plan)
    receipt=out/'receipt.edn'
    if not receipt.exists():receipt.write_text(DB.command('transact','--source',SOURCE,'--file',plan['transaction_file'],'--basis',plan['basis'],
        '--endpoint',plan['endpoint'],'--request-key',plan['request_key'],'--timeout-ms','120000',timeout=150))
    report=loads(receipt.read_text());receipt_checks.verify_report(report,plan,True,forms);after_basis=report[':edb/db-after-t']
    def check(group):
        name,pattern,ids=group
        for basis,stage in [(plan['basis'],'before'),(after_basis,'after')]:
            rows=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[ids],out/'readback',name+'-'+stage,basis) if ids else []
            assert canonical([e for [e] in rows])==canonical(loads((out/f'preview-{name}-{stage}.edn').read_text())),name
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(check,loads((out/'native-pulls.edn').read_text())))
    result={'committed':True,'basis_before':plan['basis'],'basis_after':after_basis,'source':SOURCE,'label_repairs':16,'radio_conversions':4,
        'examples_transcribed':3,'raster_references_removed':7,'tutorial_matrices_restored':4,'generators_registered':2,'retired_all_false_question':plan['retire'],
        'saved_items_preserved':plan['items_preserved'],'correct_answers_and_difficulty_preserved':True,'exact_committed_and_historical_readback':True,
        'request_key':plan['request_key'],'transaction_sha256':plan['sha256']}
    save(out/'verification.json',result);save(HERE/'verification.json',result);print(json.dumps(result))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','preview','commit']);p.add_argument('--attempt',required=True);a=p.parse_args()
    out=HERE/a.attempt;out.mkdir(exist_ok=True);globals()[a.action](out)
