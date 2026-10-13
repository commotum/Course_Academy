"""Prepare and natively preview reviewed incomplete captures. No submit API."""
import copy,hashlib,importlib.util,json,re,shutil,subprocess,sys
from pathlib import Path
from types import SimpleNamespace

OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'Cargo.toml').exists())
AUDIT=ROOT/'generate/reports/checkbox-next-review-2026-10-12'
spec=importlib.util.spec_from_file_location('previous_preview_verifier',OUT.parent/'discovery-next/prepare.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
edb=previous.edb;edb.OUT=OUT;edb.DB.args.capture_only=True

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,default=str)+'\n')

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def plain(value):return json.loads(json.dumps(value,default=str))
def normalized(text):
    text=re.sub(r'(?m)^(?:-\s+|(?:VIII|VII|VI|IV|V|III|II|I)\.\s+)','',text)
    return re.sub(r'\s+','',text.replace('\\{','{').replace('\\}','}'))
def refs(value):return [value] if isinstance(value,dict) else value

def reviewed_rows():
    review=json.loads((AUDIT/'keyed-resolutions.json').read_text());rows=copy.deepcopy(review['questions'])
    q=next(r for r in rows if r['math_academy_id']=='q-94772')
    old=q['atomic_options'][0]['text']
    new='The maximum possible number of distinct singular values of a $3\\times 2$ matrix $A$ is $3$.'
    q.update(decision='convert',independently_correct_labels=['III'],existing_key_preserved=True,
        resolution='Preserve the Math Academy III-only key as requested. Make the intended sharp-bound reading explicit in statement I; no key repair.',
        prompt_qualifications=['Statement I explicitly asks for the maximum possible count, consistent with the stored solution and key.'],
        proof='A 3x2 matrix has maximum possible count two, not three; negative singular values are impossible; the 2x3 upper bound of three holds. Preserve the existing III-only selection.')
    q['atomic_options'][0]['text']=new
    for atom in q['atomic_options']:atom.update(truth=atom['label']=='III',proof=q['proof'])
    prompt=q['problem_before'].replace(old,new)
    markers=list(re.finditer(r'(?m)^\s*-\s+',prompt))
    for m,atom in reversed(list(zip(markers,q['atomic_options']))):prompt=prompt[:m.start()]+'- **'+atom['label']+'.** '+prompt[m.end():]
    q['problem_after']=prompt+'\n\nSelect all that apply.'
    assert all(r['decision']=='convert' for r in rows)
    save(OUT/'resolutions.json',dict(basis=review['basis'],database_writes=0,questions=rows,withdrawn_key_repair_question_ids=[q['question_eid']],existing_keys_preserved=True))
    return rows

def capture(ids,basis):
    status=edb.DB.command('status');lineage=json.loads((AUDIT/'status.json').read_text())['lineage'];assert 'lineage='+lineage in status
    questions=edb.batches('[:find (pull ?q '+edb.QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',ids,'questions',basis,64)
    assert {q[':db/id'] for q, in questions}==set(ids)
    items=edb.batches('[:find ?q (pull ?item '+edb.ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',ids,'items',basis,128)
    fields=sorted({f[':db/id'] for q, in questions for f in q[':question/answer-fields']})
    answers=sorted({a[':db/id'] for q, in questions for f in q[':question/answer-fields'] for a in f[':answer-field/choices']})
    users=edb.batches('[:find ?a (pull ?item '+edb.ITEM+') :in $ [?a ...] :where [?item :task-item/responses ?a]]',answers,'response-users',basis,256)
    field_owners=edb.batches('[:find ?f (pull ?f [{[:question/_answer-fields :limit nil] [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',fields,'field-owners',basis,128)
    answer_owners=edb.batches('[:find ?a (pull ?a [{[:answer-field/_choices :limit nil] [:db/id]}]) :in $ [?a ...] :where [?a :answer/id _]]',answers,'answer-owners',basis,256)
    source=edb.read('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',[edb.kw(edb.SOURCE)],'source',basis);assert len(source)==1
    kp_ids=sorted({k[':db/id'] for q, in questions for k in q[':knowledge-point/_questions']})
    topics=edb.batches('[:find (pull ?kp [:db/id {[:topic/_knowledge-points :limit nil] [:db/id :topic/title :topic/math-academy-id]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',kp_ids,'topics-by-kp',basis,64)
    data=dict(basis=basis,lineage=lineage,questions=questions,items=items,response_users=users,field_owners=[[f,q[':db/id']] for f,d in field_owners for q in refs(d.get(':question/_answer-fields',[]))],answer_owners=[[a,f[':db/id']] for a,d in answer_owners for f in refs(d.get(':answer-field/_choices',[]))],attributes=edb.DB.attributes(OUT/'evidence',basis),source=source,topics=topics)
    (OUT/'snapshot.edn').write_text(edb.dumps(data)+'\n');save(OUT/'snapshot.json',data)
    assert not items and not users,'New learner uses require reviewed migration before preparation'
    print(json.dumps(dict(captured_basis=basis,questions=len(ids),presentations=len(items),response_links=len(users))),flush=True)
    return data

def write_batch(number,forms,changes,retained,basis,lineage,counts):
    directory=OUT/f'batch-{number:02d}';directory.mkdir(exist_ok=True)
    path=directory/'transaction.edn';path.write_text('[\n'+'\n'.join(' '+edb.dumps(form) for form in forms)+'\n]\n')
    sha=digest(path)
    manifest=dict(basis=basis,captured_basis=basis-(number-1),source=edb.SOURCE,transaction_sha256=sha,counts=counts,questions=changes,responses=[],retained_original_entities=sorted(retained))
    save(directory/'plan.json',manifest)
    request=dict(state='prepared_not_submitted',database='math',endpoint=edb.DB.args.endpoint,lineage=lineage,basis=basis,source=edb.SOURCE,sha256=sha,request_key=f'discovery-keyed-incomplete-v1-{basis}-{number}-{sha}',transaction_file=str(path),must_use_basis_guard=True,previous_batch_required=number-1 if number>1 else None)
    save(directory/'prepared-request.json',request)
    return dict(number=number,directory=str(directory),basis_guard=basis,request_key=request['request_key'],sha256=sha,bytes=path.stat().st_size,forms=len(forms),**counts)

def build(rows,snapshot):
    basis=snapshot['basis'];qs={q[':db/id']:q for q, in snapshot['questions']}
    fowners={f:{q for ff,q in snapshot['field_owners'] if ff==f} for f,_ in snapshot['field_owners']}
    aowners={a:{f for aa,f in snapshot['answer_owners'] if aa==a} for a,_ in snapshot['answer_owners']}
    forms=[];changes=[];retained=set();field_uuids=[];answer_uuids=[]
    for row in rows:
        qid=row['question_eid'];q=qs[qid];assert q[':question/problem']==row['problem_before'],('Prompt changed; preserve and re-review',qid)
        assert q.get(':question/worked-solution')==row['worked_solution'],('Solution changed; re-review',qid)
        assert q.get(':question/difficulty')==row['difficulty']
        assert {k[':db/id'] for k in q[':knowledge-point/_questions']}=={k[':db/id'] for k in row['kps']}
        assert not q.get(':knowledge-point/_canonical-example')
        assert plain(q[':question/answer-fields'])==row['old_fields'],('Fields or keys changed',qid)
        fields=q[':question/answer-fields'];bank={a[':db/id']:a for f in fields for a in f[':answer-field/choices']}
        mapping={a['old_answer']:a for a in row['choice_mapping']};assert set(mapping)==set(bank)
        key=set(row['database_key']['selected_labels']);assert key==set(row['independently_correct_labels'])
        assert all(set(mapping[a[':db/id']]['selected_labels'])==key for f in fields if (a:=f.get(':answer-field/correct')))
        labels=[a['label'] for a in row['atomic_options']];assert len(set(labels))==len(labels)
        links=[];targets={}
        for label in labels:
            token=row['math_academy_id']+'/authored-checkbox-v1/'+label;field='field-'+token;owned=[];field_uuids.append(edb.stable_id('field',token))
            for value in ('false','true'):
                answer='answer-'+token+'/'+value;uuid=edb.stable_id('answer',token+'/'+value);answer_uuids.append(uuid)
                forms.append({edb.kw('db/id'):answer,edb.kw('answer/id'):uuid,edb.kw('answer/type'):edb.kw('answer.type/text'),edb.kw('answer/value'):value,edb.kw('db/ensure'):edb.kw('answer/validate')});owned.append(answer);targets[(label,value)]=answer
            forms.append({edb.kw('db/id'):field,edb.kw('answer-field/id'):field_uuids[-1],edb.kw('answer-field/key'):label,edb.kw('answer-field/type'):edb.kw('answer-field.type/checkbox'),edb.kw('answer-field/choices'):owned,edb.kw('answer-field/correct'):owned[int(label in key)],edb.kw('db/ensure'):edb.kw('answer-field/validate')});links.append(field)
        for f in fields:
            fid=f[':db/id'];assert fowners[fid]=={qid};assert f[':answer-field/type'][':db/ident']==':answer-field.type/radio'
            assert set(f)<=set((':db/id',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct'))
            forms.append([edb.kw('db/retract'),qid,edb.kw('question/answer-fields'),fid]);retained.add(fid)
            for a in f[':answer-field/choices']:
                assert aowners[a[':db/id']]=={fid};assert a[':answer/type'][':db/ident']==':answer.type/text';retained.add(a[':db/id'])
                assert set(a)<=set((':db/id',':answer/id',':answer/type',':answer/value'))
        forms.append([edb.kw('db/cas'),qid,edb.kw('question/problem'),q[':question/problem'],row['problem_after']])
        forms.append({edb.kw('db/id'):qid,edb.kw('question/answer-fields'):links,edb.kw('db/ensure'):edb.kw('question/validate')})
        kps=[dict(id=k[':db/id'],title=k[':knowledge-point/title']) for k in row['kps']]
        changes.append(dict(id=qid,ma_id=row['math_academy_id'],kps=kps,labels=labels,correct=[l for l in labels if l in key],atomic_options=row['atomic_options'],old_fields=[f[':db/id'] for f in fields],new_field_tempids=links,problem_before=q[':question/problem'],problem_after=row['problem_after'],worked_solution=q[':question/worked-solution'],difficulty=q.get(':question/difficulty',{}).get(':db/ident'),choice_mapping=[dict(old_answer=a['old_answer'],old_value=a['old_value'],selected=a['selected_labels'],new_answer_tempids=[targets[(l,str(l in a['selected_labels']).lower())] for l in labels]) for a in row['choice_mapping']],prompt_qualifications=row['prompt_qualifications']))
    assert len(set(field_uuids))==len(field_uuids) and len(set(answer_uuids))==len(answer_uuids)
    collisions=[]
    for attr,uuids in [('answer-field/id',field_uuids),('answer/id',answer_uuids)]:collisions+=edb.batches('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',uuids,'identity-'+attr.split('/')[0],basis,256)
    assert not collisions
    save(OUT/'identity-check.json',dict(basis=basis,field_uuids=len(field_uuids),answer_uuids=len(answer_uuids),collisions=[]))
    common=dict(new_checkbox_fields=len(field_uuids),new_boolean_answers=len(answer_uuids),saved_responses_mapped=0,presentations=0)
    counts=dict(questions=len(rows),knowledge_points=len({k['id'] for q in changes for k in q['kps']}),**common)
    first=write_batch(1,forms,changes,retained,basis,snapshot['lineage'],counts)
    proposed=json.loads((AUDIT/'proposed-solution-repairs.json').read_text())['repairs'];repair_forms=[]
    for r in proposed:
        assert qs[r['question_eid']][':question/worked-solution']==r['before']
        repair_forms.extend([[edb.kw('db/cas'),r['question_eid'],edb.kw('question/worked-solution'),r['before'],r['after']],[edb.kw('db/ensure'),r['question_eid'],edb.kw('question/validate')]])
    second=write_batch(2,repair_forms,proposed,[],basis+1,snapshot['lineage'],dict(questions=len(proposed),new_checkbox_fields=0,new_boolean_answers=0,knowledge_points=len({k[':db/id'] for r in proposed for k in qs[r['question_eid']][':knowledge-point/_questions']}),presentations=0,saved_responses_mapped=0))
    save(OUT/'plan.json',dict(state='prepared_not_submitted',basis=basis,lineage=snapshot['lineage'],source=edb.SOURCE,database_writes=0,counts=dict(**counts,solution_corrections=len(proposed),unrated_questions=sum(q['difficulty'] is None for q in changes),prompt_qualifications=sum(bool(q['prompt_qualifications']) for q in changes),retained_original_entities=len(retained)),batches=[first,second],existing_keys_preserved=True,retained_entities=sorted(retained),snapshot_sha256=digest(OUT/'snapshot.edn'),commit_workflow='Capture/preview/commit conversions as one group, verify receipt, then refresh and preview the separate solution-repair group. No submit operation is provided by this preparation script.'))
    (OUT/'question-pattern.edn').write_text(edb.QUESTION)
    (OUT/'field-pattern.edn').write_text('[* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]')
    (OUT/'question-ids.txt').write_text('\n'.join(map(str,sorted(qs))))
    (OUT/'field-ids.txt').write_text('\n'.join(map(str,sorted({f[':db/id'] for q in qs.values() for f in q[':question/answer-fields']}))))
    print(json.dumps(dict(prepared=True,basis=basis,**counts,solution_corrections=len(proposed))),flush=True)

def helper():
    from capture.scripts.database.preview import _library
    library=_library(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math')));source=OUT/'preview.rs';binary=OUT/'native-preview'
    paths=[source,library,ROOT/'engine/edb/answer_fields.rs',ROOT/'engine/edb/configuration.rs',ROOT/'engine/edb/progress.rs'];hashes={str(p):digest(p) for p in paths}
    command=['rustc','--edition=2024','-O',str(source),'--extern','edb_core='+str(library),'-L','dependency='+str(library.parent),'-o',str(binary)]
    subprocess.run(command,check=True);assert hashes=={str(p):digest(p) for p in paths}
    save(OUT/'native-preview-build.json',dict(inputs=hashes,command=command,binary_sha256=digest(binary),database_writes=0));return binary

def verify_report(directory,report,snapshot,solutions):
    manifest=json.loads((directory/'plan.json').read_text())
    assert report[':edb/committed'] is False and report[':edb/speculative'] is True
    assert report[':edb/db-before-t']==manifest['basis'] and report[':edb/db-after-t']==manifest['basis']+1
    assert digest(directory/'transaction.edn')==manifest['transaction_sha256']
    ids=report[':edb/tempids'];assert len(set(ids.values()))==manifest['counts']['new_checkbox_fields']*3
    assert set(ids.values()).isdisjoint(manifest['retained_original_entities'])
    names=dict(snapshot['attributes']);source=snapshot['source'][0][0][':db/id']
    enums={str(ident):eid for eid,ident in edb.read('[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]',[[edb.kw('answer-field.type/checkbox'),edb.kw('answer.type/text')]],'preview-enums',snapshot['basis'])}
    def resolve(value):
        if isinstance(value,edb.kw('x').__class__):return enums[str(value)]
        if isinstance(value,str) and value in ids:return ids[value]
        return value
    additions=set();retractions=set()
    for form in edb.loads((directory/'transaction.edn').read_text()):
        if isinstance(form,dict):
            eid=resolve(form[':db/id'])
            for attr,values in form.items():
                if attr in (':db/id',':db/ensure'):continue
                for value in values if isinstance(values,list) else [values]:additions.add((eid,str(attr),resolve(value)))
        elif form[0]==':db/retract':retractions.add((form[1],str(form[2]),resolve(form[3])))
        elif form[0]==':db/cas':
            additions.add((form[1],str(form[2]),resolve(form[4])));retractions.add((form[1],str(form[2]),resolve(form[3])))
        elif form[0]==':db/ensure':
            assert solutions and form[2]==':question/validate'
        else:raise AssertionError(('Unexpected form',form))
    actual_additions=set();actual_retractions=set();instants=0
    for eid,attr,value,tx,contributor,added in report[':edb/tx-data']:
        assert contributor==source
        name=str(names[attr])
        if name==':db/txInstant':assert added;instants+=1;continue
        (actual_additions if added else actual_retractions).add((eid,name,value))
    assert instants==1 and additions==actual_additions and retractions==actual_retractions
    result=dict(passed=True,committed=False,speculative=True,basis=manifest['basis'],basis_after=report[':edb/db-after-t'],source=edb.SOURCE,sha256=manifest['transaction_sha256'],datoms=len(report[':edb/tx-data']),counts=manifest['counts'],exact_datom_scope_verified=True,all_datom_sources_verified=True,native_validators_passed=True)
    save(directory/'preview.json',result);return result

def verify(snapshot):
    plan=json.loads((OUT/'plan.json').read_text());results=[]
    for batch in plan['batches']:
        directory=Path(batch['directory']);report=edb.loads((directory/'preview.edn').read_text())
        results.append(verify_report(directory,report,snapshot,batch['number']==2))
        after=edb.loads((directory/'questions-after.edn').read_text());before={q[':db/id']:q for q, in snapshot['questions']};changes={q['id']:q for q in json.loads((OUT/'batch-01/plan.json').read_text())['questions']}
        repairs={r['question_eid']:r['after'] for r in json.loads((OUT/'batch-02/plan.json').read_text())['questions']} if batch['number']==2 else {}
        for q in after:
            original=before[q[':db/id']];change=changes[q[':db/id']]
            preserve=lambda d:{k:v for k,v in d.items() if k not in (':question/problem',':question/answer-fields',':question/worked-solution')}
            assert preserve(q)==preserve(original)
            assert q[':question/problem']==change['problem_after']
            assert q[':question/worked-solution']==repairs.get(q[':db/id'],original[':question/worked-solution'])
            fs={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(fs)==set(change['labels'])
            for label,f in fs.items():
                assert f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
                token=change['ma_id']+'/authored-checkbox-v1/'+label
                assert f[':answer-field/id']==edb.stable_id('field',token)
                bank={a[':answer/value']:a for a in f[':answer-field/choices']};assert set(bank)=={'false','true'}
                for value,a in bank.items():assert a[':answer/id']==edb.stable_id('answer',token+'/'+value) and a[':answer/type'][':db/ident']==':answer.type/text'
                assert f[':answer-field/correct']==bank[str(label in change['correct']).lower()]
        originals={f[':db/id']:f for q, in snapshot['questions'] for f in q[':question/answer-fields']}
        after_fields={f[':db/id']:f for f in edb.loads((directory/'fields-after.edn').read_text())}
        assert originals==after_fields,'Detached original field/answer entities changed'
    save(OUT/'preview.json',dict(passed=True,committed=False,speculative=True,captured_basis=plan['basis'],predicted_final_basis=plan['basis']+2,source=edb.SOURCE,database_writes=0,batches=results,counts=plan['counts'],db_after_readback_verified=True,all_existing_keys_preserved=True))
    save(OUT/'status.json',{**plan,'state':'prepared_previewed_not_submitted','preview':str(OUT/'preview.json'),'live_submission_authorized':False})
    print(json.dumps(dict(preview_passed=True,basis=plan['basis'],**plan['counts'])),flush=True)

def main():
    assert not list(OUT.glob('batch-*/commit*')),'Resolve retained submitted requests before preparing'
    assert not (OUT/'plan.json').exists(),'Preserve the prior preparation; refresh in a separate directory'
    rows=reviewed_rows();binary=helper()
    process=subprocess.Popen([str(binary),str(OUT),edb.SOURCE],env=edb.DB.env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        line=process.stdout.readline();assert line.startswith('CAPTURED_BASIS '),line;basis=int(line.split()[1])
        snapshot=capture(sorted(r['question_eid'] for r in rows),basis);build(rows,snapshot)
        stdout,stderr=process.communicate('PREVIEW\n',timeout=180);assert process.returncode==0,stderr
        (OUT/'preview.log').write_text(line+stdout);assert stdout.splitlines()==['PREVIEWED_BATCH 1','PREVIEWED_BATCH 2']
        verify(snapshot)
    finally:
        if process.poll() is None:process.kill();process.wait()

if __name__=='__main__':main()
