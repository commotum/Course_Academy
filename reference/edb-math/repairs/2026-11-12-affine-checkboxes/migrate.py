"""Prepare, preview, submit, and verify the authorized affine checkbox migration."""
import argparse, copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from audit import ROOT, HERE, QUESTION, ITEM, KP
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from scripts.generator_publish import Publisher
from scripts.question_capture.core import stable_id
from capture.scripts.database.edn import dumps, loads, kw, Tagged

SOURCE=':agent/codex'
DB=Publisher.from_environment(source=SOURCE).client
LABELS=['T1','T2','T3']
# Independently transcribed coordinate functions, checked against each source below.
FUNCTIONS={
 'q-124007':[('u+v','v-u'),('u**2','-v'),('u+2','u-v+1')],
 'q-124255':[('v-7*u+3','3*v-u+1'),('u*v+1','u-2*v'),('9*u','u-v')],
 'q-124236':[('u+v','sqrt(v)'),('u+1','v**3'),('3*u-2','8-v')],
 'q-124237':[('v-6*u+7','4*u+3*v-5'),('-7*u-2*v','5*u+v'),('2*u+v','u*v+1')],
 'q-124245':[('7*u-v+6','-7'),('8*v-9*u','4*u-v'),('u-5','8*u')],
 'q-124247':[('9*u+v','2*u+8*v'),('u','1-v**3'),('u*(v-1)','u-1')],
 'q-124251':[('u**2-v**2','v-u'),('6*v-4*u','3*u+3*v'),('u+v+9','v-9')],
 'q-124253':[('u-1','exp(v)'),('8*u+2*v+2','u-2*v+4'),('u+v','log(u+v)')],
 'q-124240':[('u*(u+1)','v+1'),('v-2','5*u-7'),('-v','-v')],
 'q-124232':[('u*v','u+v'),('v','2*v-u'),('-u**2','2*u+v')],
}
def save(path,value):path.write_text(json.dumps(value,indent=2,default=str)+'\n')
def canon(value):
    if isinstance(value,dict):return {str(k):canon(v) for k,v in sorted(value.items())}
    if isinstance(value,list):return sorted([canon(v) for v in value],key=lambda v:json.dumps(v,sort_keys=True,default=str))
    return str(value) if isinstance(value,uuid.UUID) else value
def equal(a,b):return canon(a)==canon(b)
def by_id(rows):return {q[':db/id']:q for q in rows}
def lint(q,objects):
    spec=importlib.util.spec_from_file_location('presentation_lint',ROOT/'skills/radio2checkbox/scripts/lint_presentation.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    errors=m.lint_question(q,objects);assert not errors,errors
def read(name,query,inputs,out,basis):return DB.query(query,inputs,out/'evidence',name,basis)
def subset(text):
    found=re.findall(r'\{T\}_\{([123])\}',text)
    assert found and len(found)==len(set(found)),text
    rest=re.sub(r'\{T\}_\{[123]\}','',text)
    assert re.fullmatch(r'[\s$,]*(?:(?:and|only)[\s$,]*)*',rest),rest
    return ['T'+x for x in found]
def objects_from(q):
    body=q[':question/problem'].split('Which of the following are affine transformations?',1)[1].strip()
    chunks=re.split(r'(?m)^\s*(?:- |I{1,3}\. )',body)
    assert not chunks[0].strip() and len(chunks)==4,body
    result=[]
    for i,chunk in enumerate(chunks[1:],1):
        text=chunk.strip()
        if text.startswith('$$'):
            assert text.endswith('$$');text='$'+text[2:-2].strip().removeprefix('\\displaystyle').strip()+'$'
        assert text.startswith('${T}_{'+str(i)+'}:'),text
        assert text.endswith('$') and text.count('\\begin{bmatrix}')==2,text
        result.append(text)
    return result
def mathematical_proof(mid):
    import sympy as s
    u,v=s.symbols('u v',real=True);proof=[]
    for pair in FUNCTIONS[mid]:
        expressions=[s.sympify(x,locals={'u':u,'v':v}) for x in pair]
        affine=all(s.simplify(s.diff(x,a,b))==0 for x in expressions for a,b in [(u,u),(u,v),(v,v)])
        entry={'functions':pair,'affine':affine}
        if affine:
            entry['A']=[[str(s.diff(x,z)) for z in (u,v)] for x in expressions]
            entry['b']=[str(x.subs({u:0,v:0})) for x in expressions]
            assert all(s.simplify(x-s.diff(x,u)*u-s.diff(x,v)*v-x.subs({u:0,v:0}))==0 for x in expressions)
        else:entry['nonzero_second_derivatives']=[str(s.diff(x,a,b)) for x in expressions for a,b in [(u,u),(u,v),(v,v)] if s.simplify(s.diff(x,a,b))!=0]
        proof.append(entry)
    return proof
def prepare(out):
    assert not (out/'commit-intent.json').exists(),'Recover the retained request first'
    captured=json.loads((HERE/'capture.json').read_text());original=loads((Path(captured['directory'])/'snapshot.edn').read_text())
    identity=DB.status();basis=identity['basis'];assert identity['lineage']==original['lineage']
    ids=sorted(q[':db/id'] for [q] in original['questions']);kids=sorted(k[':db/id'] for [k] in original['kps'])
    specs={
      'questions':('[:find (pull ?q '+QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',[ids]),
      'items':('[:find ?q (pull ?i '+ITEM+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids]),
      'kps':('[:find (pull ?k '+KP+') :in $ [?k ...] :where [?k :knowledge-point/id _]]',[kids]),
      'source':('[:find (pull ?s [*]) :in $ ?ident :where [?s :db/ident ?ident]]',[kw(SOURCE)]),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending={name:pool.submit(read,name,*args,out,basis) for name,args in specs.items()}
        data={name:f.result() for name,f in pending.items()}
    assert equal(data['questions'],original['questions']),'Question changes need renewed review'
    assert equal(data['kps'],original['kps']),'Question pool or generator changed'
    assert len(data['source'])==1
    assert all(not k.get(':knowledge-point/question-generator') for [k] in data['kps'])
    questions=by_id([q for [q] in data['questions']]);selected=[q for q in questions.values() if q.get(':question/math-academy-id') in FUNCTIONS]
    assert len(selected)==10
    old_fields={f[':db/id']:q[':db/id'] for q in selected for f in q[':question/answer-fields']}
    old_answers={a[':db/id']:f[':db/id'] for q in selected for f in q[':question/answer-fields'] for a in f[':answer-field/choices']}
    targets=sorted(set(old_fields)|set(old_answers))
    incoming=read('incoming','[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]',[[Tagged('edb/ref',e) for e in targets]],out,basis)
    attrs={a:ident for a,ident,_ in original['attributes']}
    uses={(i[':db/id'],a[':db/id']) for q,i in data['items'] for a in i.get(':task-item/responses',[]) if q in {x[':db/id'] for x in selected}}
    response_users=set()
    for e,a,target in incoming:
        name=str(attrs[a])
        assert ((name==':question/answer-fields' and old_fields.get(target)==e) or
            (name in (':answer-field/choices',':answer-field/correct') and old_answers.get(target)==e) or
            (name==':task-item/responses' and (e,target) in uses)),(e,name,target)
        if name==':task-item/responses':response_users.add((e,target))
    assert response_users==uses
    forms=[];cases=[];new_uuids=[];response_changes=[]
    def add(e,a,v):forms.append([kw('db/add'),e,kw(a),v])
    def ensure(e,spec):forms.append([kw('db/ensure'),e,kw(spec)])
    for q in sorted(selected,key=lambda q:q[':db/id']):
        qid=q[':db/id'];mid=q[':question/math-academy-id'];old=q[':question/answer-fields']
        assert len(old)==1 and old[0][':answer-field/type'][':db/ident']==':answer-field.type/radio'
        assert not q.get(':knowledge-point/_canonical-example')
        old=old[0];assert set(old)=={':db/id',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct'}
        assert all(':answer/feedback' not in a for a in old[':answer-field/choices'])
        objects=objects_from(q);proof=mathematical_proof(mid);truth=[p['affine'] for p in proof]
        mapping=[{'old_answer':a[':db/id'],'text':a[':answer/value'],'selected':subset(a[':answer/value'])} for a in old[':answer-field/choices']]
        correct=next(c for c in mapping if c['old_answer']==old[':answer-field/correct'][':db/id'])
        assert correct['selected']==[label for label,t in zip(LABELS,truth) if t],(mid,correct,truth)
        after=copy.deepcopy(q);after[':question/problem']='Which of the following are affine transformations? Select all that apply.'
        after[':question/answer-fields']=[];reviewed=[];answer_refs={}
        forms.append([kw('db/cas'),qid,kw('question/problem'),q[':question/problem'],after[':question/problem']])
        forms.append([kw('db/retract'),qid,kw('question/answer-fields'),old[':db/id']])
        for label,content,key in zip(LABELS,objects,truth):
            token=mid+'/authored-checkbox-v1/'+label;fid=stable_id('field',token);ft=token+'/field';new_uuids.append(fid)
            answers=[]
            for val in ('false','true'):
                aid=stable_id('answer',token+'/'+val);at=token+'/answer/'+val;new_uuids.append(aid)
                add(at,'answer/id',aid);add(at,'answer/type',kw('answer.type/text'));add(at,'answer/value',val);ensure(at,'answer/validate')
                answers.append({':db/id':at,':answer/id':aid,':answer/type':{':db/ident':kw('answer.type/text')},':answer/value':val})
                answer_refs[label,val]=at
            add(ft,'answer-field/id',fid);add(ft,'answer-field/key',content);add(ft,'answer-field/type',kw('answer-field.type/checkbox'))
            for a in answers:add(ft,'answer-field/choices',a[':db/id'])
            correct_answer=next(a for a in answers if a[':answer/value']==str(key).lower())
            add(ft,'answer-field/correct',correct_answer[':db/id']);add(qid,'question/answer-fields',ft);ensure(ft,'answer-field/validate')
            after[':question/answer-fields'].append({':db/id':ft,':answer-field/id':fid,':answer-field/key':content,':answer-field/type':{':db/ident':kw('answer-field.type/checkbox')},':answer-field/choices':answers,':answer-field/correct':correct_answer})
            reviewed.append({'source_label':label,'field_id':str(fid),'content':content,'source_fragment':content})
        ensure(qid,'question/validate');lint(after,reviewed)
        for item_q,item in data['items']:
            if item_q!=qid or not item.get(':task-item/responses'):continue
            responses=item[':task-item/responses'];assert len(responses)==1
            oid=responses[0][':db/id'];choice=next(c for c in mapping if c['old_answer']==oid)
            status=item[':task-item/status'][':db/ident']
            if status in (':task-item.status/correct',':task-item.status/incorrect'):
                assert (status==':task-item.status/correct')==(oid==old[':answer-field/correct'][':db/id'])
            new=[answer_refs[label,str(label in choice['selected']).lower()] for label in LABELS]
            forms.append([kw('db/retract'),item[':db/id'],kw('task-item/responses'),oid])
            for aid in new:add(item[':db/id'],'task-item/responses',aid)
            ensure(item[':db/id'],'task-item/validate')
            response_changes.append({'item':item[':db/id'],'question':qid,'old':oid,'selected':choice['selected'],'new':new})
        cases.append({'question_id':qid,'ma_id':mid,'decision':'convert','before':q,'after':after,'objects':reviewed,'mathematics':proof,'choice_mapping':mapping,'old_key':old[':answer-field/correct'][':db/id'],'source':SOURCE})
    collisions=read('collisions','[:find ?e ?uuid :in $ [?uuid ...] :where (or-join [?e ?uuid] [?e :answer-field/id ?uuid] [?e :answer/id ?uuid])]',[new_uuids],out,basis)
    assert not collisions,'New stable identities already exist'
    (out/'transaction.edn').write_text(dumps(forms)+'\n')
    snapshot={**identity,**data,'attributes':original['attributes'],'idents':original['idents'],'incoming':incoming}
    (out/'snapshot.edn').write_text(dumps(snapshot)+'\n')
    sha=hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()
    plan={**identity,'source':SOURCE,'source_id':data['source'][0][0][':db/id'],'cases':cases,'response_changes':response_changes,
      'retained_entities':targets,'converted_ids':[c['question_id'] for c in cases],
      'counts':{'questions':len(cases),'checkbox_fields':len(new_uuids)//3,'boolean_answers':len(new_uuids)*2//3,'mapped_saved_attempts':len(response_changes),'old_choices_mapped':sum(len(c['choice_mapping']) for c in cases)},
      'transaction_file':str((out/'transaction.edn').resolve()),'sha256':sha,'endpoint':DB.config.endpoint,'request_key':f'affine-checkboxes-b{basis}-{sha}',
      'generators':{'registered':0,'repository_sources_found':0,'updates_required':0},
      'retained_examples':[q[':db/id'] for q in questions.values() if q.get(':knowledge-point/_canonical-example')],
      'retained_radio_reason':'Other practice questions request one numerical value. Canonical examples have no answer fields and remain worked examples.',
      'known_unrelated_content_issue':'q-124232 worked solution says T1 is linear after deriving T2; database key correctly selects T2. Preserve solution during this representation migration.'}
    save(out/'plan.json',plan);save(HERE/'case-ledger.json',plan)
    groups=[['questions',QUESTION,ids],['retained','[*]',targets],['items',ITEM,sorted(i[':db/id'] for _,i in data['items'])],['kps',KP,kids]]
    (out/'native-pulls.edn').write_text(dumps(groups)+'\n')
    save(out/'proposed-presentation.json',{'cases':[{'question':c['after'],'objects':c['objects']} for c in cases]})
    save(HERE/'status.json',{'stage':'prepared','directory':str(out),'basis':basis,'selected_ids':plan['converted_ids'],'committed_ids':[],'counts':plan['counts']})
    print(json.dumps({'stage':'prepared','basis':basis,'forms':len(forms),**plan['counts']}))

def resolve(x,report):return report[':edb/tempids'].get(x,x) if isinstance(x,str) else x
def verify_report(report,plan,snapshot,forms,committed):
    assert report[':edb/committed'] is committed
    assert report[':edb/db-before-t']==plan['basis'] and report[':edb/db-after-t']==plan['basis']+1
    attrs={str(name):(a,str(typ)) for a,name,typ in snapshot['attributes']}
    idents={str(ident):e for e,ident in snapshot['idents']}
    def value(a,v):
        if attrs[str(a)][1]==':db.type/ref':return idents[str(v)] if str(v) in idents else resolve(v,report)
        return v
    expected=[]
    for op,e,a,*args in forms:
        if op==':db/ensure':continue
        eid=resolve(e,report);aid=attrs[str(a)][0]
        if op==':db/cas':
            old,new=args;expected.extend([[eid,aid,value(a,old),False],[eid,aid,value(a,new),True]])
        else:expected.append([eid,aid,value(a,args[0]),op==':db/add'])
    txattr=attrs[':db/txInstant'][0];actual=[];instants=0
    for e,a,v,tx,s,added in report[':edb/tx-data']:
        assert s==plan['source_id'],'Unexpected contributor'
        if a==txattr:instants+=1;continue
        actual.append([e,a,v,added])
    assert instants==1 and equal(expected,actual),'Unexpected transaction scope'

def verify_pulls(out,report,plan):
    cases={c['question_id']:c for c in plan['cases']};saved={r['item']:r for r in plan['response_changes']}
    before_q=by_id(loads((out/'preview-questions-before.edn').read_text()))
    after_q=by_id(loads((out/'preview-questions-after.edn').read_text()))
    snap=loads((out/'snapshot.edn').read_text())
    assert equal(list(before_q.values()),[q for [q] in snap['questions']])
    for eid,before in before_q.items():
        after=after_q[eid]
        if eid not in cases:assert equal(before,after);continue
        c=cases[eid];omit=lambda q:{k:v for k,v in q.items() if k not in (':question/problem',':question/answer-fields')}
        assert equal(omit(before),omit(after)) and after[':question/problem']==c['after'][':question/problem']
        af={str(f[':answer-field/id']):f for f in after[':question/answer-fields']}
        assert set(af)=={str(f[':answer-field/id']) for f in c['after'][':question/answer-fields']}
        for expected in c['after'][':question/answer-fields']:
            f=af[str(expected[':answer-field/id'])]
            assert f[':answer-field/key']==expected[':answer-field/key'] and f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
            assert len(f[':answer-field/choices'])==2
            assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
            assert all(a[':answer/type'][':db/ident']==':answer.type/text' for a in f[':answer-field/choices'])
            assert str(f[':answer-field/correct'][':answer/id'])==str(expected[':answer-field/correct'][':answer/id'])
        lint(after,c['objects'])
    for group in ('retained','kps'):
        assert equal(loads((out/f'preview-{group}-before.edn').read_text()),loads((out/f'preview-{group}-after.edn').read_text())),group
    before_items=by_id(loads((out/'preview-items-before.edn').read_text()));after_items=by_id(loads((out/'preview-items-after.edn').read_text()))
    for eid,b in before_items.items():
        a=after_items[eid];omit=lambda i:{k:v for k,v in i.items() if k!=':task-item/responses'}
        assert equal(omit(b),omit(a))
        if eid not in saved:assert equal(b,a);continue
        assert {r[':db/id'] for r in a[':task-item/responses']}=={resolve(x,report) for x in saved[eid]['new']}
    save(out/'preview-presentation.json',{'cases':[{'question':after_q[c['question_id']],'objects':c['objects']} for c in plan['cases']]})

def grading(out,plan):
    after=by_id(loads((out/'preview-questions-after.edn').read_text()));records=[]
    for case in plan['cases']:
        q=after[case['question_id']];source=case['after'][':question/answer-fields'];fields=[];checks=[];new={}
        fs={str(f[':answer-field/id']):f for f in q[':question/answer-fields']}
        for i,(label,p) in enumerate(zip(LABELS,source)):
            f=fs[str(p[':answer-field/id'])];choices=[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]
            correct=str(f[':answer-field/correct'][':answer/id'])
            fields.append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
            for a in choices:
                new[label,a[':answer/value']]=a[':answer/id'];checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Owned Boolean answer from native preview'})
        mapped=[{'old_answer':m['old_answer'],'answer_ids':[new[l,str(l in m['selected']).lower()] for l in LABELS],'expected':m['old_answer']==case['old_key']} for m in case['choice_mapping']]
        records.append({'label':case['ma_id'],'record':{'question':{':question/problem':q[':question/problem'],':question/answer-fields':fields},'knowledge_point':{'title':'Identifying Affine Transformations'},'generation':{'template':'native-preview-db-after'}},'checks':checks,'mapped_responses':mapped})
    save(out/'engine-input.json',records)
    subprocess.run([str(HERE/'native/check-checkbox-engine'),str(out/'engine-input.json'),str(out/'engine-report.json')],check=True)

def preview(out):
    plan=json.loads((out/'plan.json').read_text());snap=loads((out/'snapshot.edn').read_text());forms=loads((out/'transaction.edn').read_text())
    result=subprocess.run([str(HERE/'native/preview'),str(out),SOURCE,str(plan['basis'])],env=DB.environment,capture_output=True,text=True,timeout=180)
    (out/'preview.stderr').write_text(result.stderr);result.check_returncode();(out/'preview.edn').write_text(result.stdout)
    report=loads(result.stdout);verify_report(report,plan,snap,forms,False);verify_pulls(out,report,plan);grading(out,plan)
    save(out/'preview-verification.json',{'passed':True,'exact_allowed_datoms':True,'provenance':SOURCE,'solutions_difficulty_memberships_preserved':True,'original_fields_answers_retained':True,'saved_task_state_preserved':True,'presentation_lint_passed':True,'native_grading_passed':True})
    print('Preview, exact datom checks, preservation checks, presentation lint, and native grading passed.')

def commit(out):
    plan=json.loads((out/'plan.json').read_text());snapshot=loads((out/'snapshot.edn').read_text());forms=loads((out/'transaction.edn').read_text())
    assert json.loads((out/'preview-verification.json').read_text())['passed']
    rendered=json.loads((HERE/'rendering-verification.json').read_text())
    assert rendered['passed'] and rendered['transaction_sha256']==plan['sha256']
    assert hashlib.sha256((out/'transaction.edn').read_bytes()).hexdigest()==plan['sha256']
    assert DB.status()['lineage']==plan['lineage']
    intent=out/'commit-intent.json'
    if intent.exists():assert json.loads(intent.read_text())==plan
    else:save(intent,plan)
    receipt=out/'receipt.edn'
    if not receipt.exists():
        text=DB.command('transact','--source',SOURCE,'--file',plan['transaction_file'],'--basis',plan['basis'],'--endpoint',plan['endpoint'],'--request-key',plan['request_key'],'--timeout-ms','120000',timeout=150)
        receipt.write_text(text)
    report=loads(receipt.read_text());verify_report(report,plan,snapshot,forms,True);after=report[':edb/db-after-t']
    predicted=loads((out/'preview.edn').read_text());remap={eid:report[':edb/tempids'][key] for key,eid in predicted[':edb/tempids'].items()}
    def durable(x):
        if isinstance(x,int) and not isinstance(x,bool):return remap.get(x,x)
        if isinstance(x,list):return [durable(v) for v in x]
        if isinstance(x,dict):return {k:durable(v) for k,v in x.items()}
        return x
    def check(group):
        name,pattern,ids=group
        for basis,stage in [(plan['basis'],'before'),(after,'after')]:
            rows=read(name+'-'+stage,'[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e _ _]]',[ids],out/'readback',basis)
            expected=loads((out/f'preview-{name}-{stage}.edn').read_text())
            if stage=='after':expected=durable(expected)
            assert equal([e for [e] in rows],expected),name+'-'+stage
            if name=='questions' and stage=='after':
                by=by_id([e for [e] in rows]);save(out/'committed-presentation.json',{'cases':[{'question':by[c['question_id']],'objects':c['objects']} for c in plan['cases']]})
                for c in plan['cases']:lint(by[c['question_id']],c['objects'])
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(check,loads((out/'native-pulls.edn').read_text())))
    result={'committed':True,'verified':True,'basis_before':plan['basis'],'basis_after':after,'lineage':plan['lineage'],'source':SOURCE,'counts':plan['counts'],'converted_ids':plan['converted_ids'],'request_key':plan['request_key'],'sha256':plan['sha256'],'exact_committed_and_historical_readback':True,'native_grading_passed':True,'presentation_verified':True,'learner_responses_and_state_preserved':True,'original_entities_retained':len(plan['retained_entities']),'generator_updates_required':0}
    save(out/'verification.json',result);save(HERE/'verification.json',result);save(HERE/'status.json',{**result,'stage':'committed_verified','directory':str(out),'unsubmitted_ids':[]})
    ledger=copy.deepcopy(plan)
    for case in ledger['cases']:
        case.update(commit_status='committed_verified',committed_basis=after,receipt=str(receipt),preview_status='passed')
    ledger['verification']=result;save(HERE/'case-ledger.json',ledger)
    print(json.dumps(result))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','preview','commit']);p.add_argument('--attempt',required=True);a=p.parse_args();out=HERE/a.attempt;out.mkdir(exist_ok=True);globals()[a.action](out)
