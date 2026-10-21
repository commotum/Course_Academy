#!/usr/bin/env python3
"""Read-only content/identity preservation, presentation lint and native grading.

Input plan: {"cases":[{"question":eid,"before":full_pull,"after":full_pull,
"objects":[{"source_label":"I","field_id":eid,"content":"full statement"}]}]}.
--before/--after optionally replace plan snapshots with native preview/readback
Pull results. Every other task-item, field and answer attribute must be unchanged.
"""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'Cargo.toml').is_file())
sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import loads

def module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result
lint=module(ROOT/'skills/radio2checkbox/scripts/lint_presentation.py','presentation_lint')

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n')
def read(path):
    return loads(path.read_text()) if path.suffix=='.edn' else json.loads(path.read_text())
def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(v) for k,v in sorted(value.items())}
    if isinstance(value,(list,tuple,set)):
        return sorted((canonical(v) for v in value),key=lambda v:json.dumps(v,sort_keys=True,default=str))
    if isinstance(value,(str,int,float,bool)) or value is None:return value
    return str(value)
def records(value):
    if isinstance(value,dict):value=value.get('questions',value.get('items',value))
    assert isinstance(value,list),'Expected Pull entities or query rows'
    return [row[-1] if isinstance(row,list) else row for row in value]
def index(value):
    rows=records(value);result={q[':db/id']:q for q in rows}
    assert len(rows)==len(result),'Duplicate entities'
    return result
def ident(v):return v.get(':db/ident') if isinstance(v,dict) else str(v)
def eid(v):return v[':db/id'] if isinstance(v,dict) else v

def native_build(out):
    pinned=HERE/'pinned-grader'
    if (pinned/'manifest.json').exists():
        manifest=json.loads((pinned/'manifest.json').read_text())
        for name,digest in manifest['files'].items():
            assert Path(name).name==name,'Invalid pinned grader file'
            assert hashlib.sha256((pinned/name).read_bytes()).hexdigest()==digest,('Pinned native grader changed',name)
        build=json.loads((pinned/'grade-build.json').read_text())
        assert build['hashes']==manifest['build_inputs'],'Pinned build inputs changed'
        save(out/'native-grader-version.json',{'mode':'pinned','directory':str(pinned),
            'manifest_sha256':hashlib.sha256((pinned/'manifest.json').read_bytes()).hexdigest(),
            'binary_sha256':manifest['files']['grade-preservation'],'build_inputs':manifest['build_inputs']})
        return pinned/'grade-preservation'
    deps=ROOT/'target/release/deps'
    libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)
          for n in ['course_academy_engine','serde_json']}
    sources=sorted((ROOT/'engine/rust').glob('*.rs'))
    assert all(p.stat().st_mtime_ns <= libs['course_academy_engine'].stat().st_mtime_ns for p in sources), 'Build current engine library before grading'
    inputs=[HERE/'grade-preservation.rs',*libs.values(),*sources]
    manifest={'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
    executable=HERE/'grade-preservation'
    previous=HERE/'grade-build.json'
    if not executable.exists() or not previous.exists() or json.loads(previous.read_text())!=manifest:
        command=['rustc','--edition=2024','-O',str(HERE/'grade-preservation.rs')]
        for name,path in libs.items():command+=['--extern',name+'='+str(path)]
        command+=['-L','dependency='+str(deps),'-o',str(executable)]
        run=subprocess.run(command,text=True,capture_output=True)
        (out/'grade-build.stdout').write_text(run.stdout);(out/'grade-build.stderr').write_text(run.stderr)
        run.check_returncode();save(previous,manifest)
    return executable

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan',type=Path);parser.add_argument('--before',type=Path);parser.add_argument('--after',type=Path)
    parser.add_argument('--items-before',type=Path);parser.add_argument('--items-after',type=Path)
    parser.add_argument('--incoming-before',type=Path);parser.add_argument('--incoming-after',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
    document=read(args.plan);cases=document['cases'];assert cases
    before=index(read(args.before)) if args.before else {c['before'][':db/id']:c['before'] for c in cases}
    after=index(read(args.after)) if args.after else {c['after'][':db/id']:c['after'] for c in cases}
    before_items=index(read(args.items_before)) if args.items_before else {}
    after_items=index(read(args.items_after)) if args.items_after else {}
    assert bool(args.before)==bool(args.after),'Need both before and after snapshots'
    assert bool(args.items_before)==bool(args.items_after),'Need both item snapshots'
    assert canonical(before_items)==canonical(after_items),'Saved task-item state changed'
    assert bool(args.incoming_before)==bool(args.incoming_after),'Need both incoming-use snapshots'
    if args.incoming_before:
        assert canonical(read(args.incoming_before))==canonical(read(args.incoming_after)),'Incoming references changed'
    reports=[];old_findings=[];new_findings=[];native=[];render=[];changes=[]
    for case in cases:
        qid=case.get('question',case.get('question_eid'))
        if isinstance(qid,dict):qid=qid[':db/id']
        if qid is None:qid=case['before'][':db/id']
        b,a=before[qid],after[qid]
        assert canonical(b)==canonical(case['before']),(qid,'Reviewed before differs')
        assert canonical(a)==canonical(case['after']),(qid,'Reviewed after differs')
        bf={f[':db/id']:f for f in b[':question/answer-fields']};af={f[':db/id']:f for f in a[':question/answer-fields']}
        assert bf.keys()==af.keys(),(qid,'Field identities changed')
        expected=copy.deepcopy(b)
        for attr in [':question/problem',':question/worked-solution']:
            if b.get(attr)!=a.get(attr):
                assert attr in b and attr in a,(qid,'Unexpected missing prompt/solution')
                expected[attr]=a[attr];changes.append({'entity':qid,'attribute':attr,'before':b[attr],'after':a[attr]})
        all_answers={}
        for f in expected[':question/answer-fields']:
            fid=f[':db/id'];new=af[fid]
            assert ident(f[':answer-field/type'])==':answer-field.type/checkbox',(qid,'Mixed question needs explicit review')
            choices=f[':answer-field/choices']
            assert len(choices)==2 and {x[':answer/value'] for x in choices}=={'true','false'},(qid,fid,'Boolean bank')
            assert all(ident(x[':answer/type'])==':answer.type/text' for x in choices),(qid,fid,'Answer type')
            assert eid(f[':answer-field/correct']) in {eid(x) for x in choices},(qid,fid,'Unowned correct ref')
            for answer in choices:
                aid=eid(answer);assert aid not in all_answers,(qid,'Shared answer in checkbox fields')
                all_answers[aid]=fid
            if f.get(':answer-field/key')!=new.get(':answer-field/key'):
                changes.append({'entity':fid,'attribute':':answer-field/key','before':f[':answer-field/key'],'after':new[':answer-field/key']})
                f[':answer-field/key']=new[':answer-field/key']
        assert canonical(expected)==canonical(a),(qid,'Changes outside keys, prompt and solution')
        old_findings+=lint.lint_question(b,case['objects'])
        new_findings+=lint.lint_question(a,case['objects'])
        items={i[':db/id']:i for i in b.get(':task-item/_content',[])}
        for item in before_items.values():
            if eid(item.get(':task-item/content',-1))==qid:items[item[':db/id']]=item
        saved=[]
        for iid,item in items.items():
            responses=item.get(':task-item/responses',[])
            paired=[];seen=set()
            for answer in responses:
                aid=eid(answer);assert aid in all_answers,(qid,iid,'Saved response is not owned by current fields',aid)
                fid=all_answers[aid];assert fid not in seen,(qid,iid,'Duplicate response for field')
                seen.add(fid);paired.append([fid,aid])
            saved.append({'item':iid,'responses':paired})
        native.append({'before':b,'after':a,'saved_responses':saved})
        for stage,q in [('before',b),('after',a)]:
            render.append({'id':str(qid),'stage':stage,'label':f'Question {qid} ({stage})',
                'problem':q.get(':question/problem',''),'solution':q.get(':question/worked-solution',''),
                'fields':[{'id':f[':db/id'],'key':f[':answer-field/key'],'type':ident(f[':answer-field/type']),
                    'answerType':'text','choices':[{'id':x[':db/id'],'value':x[':answer/value'],'type':ident(x[':answer/type'])}for x in f[':answer-field/choices']]}
                    for f in sorted(q[':question/answer-fields'],key=lambda f:f[':db/id'])]})
        reports.append({'question':qid,'fields':len(bf),'saved_items':len(saved),'all_other_attributes_preserved':True})
    save(out/'before-presentation-lint.json',{'status':'fail' if old_findings else 'pass','questions':len(cases),'findings':old_findings})
    save(out/'after-presentation-lint.json',{'status':'fail' if new_findings else 'pass','questions':len(cases),'findings':new_findings})
    assert not new_findings,('Presentation lint findings',new_findings[:10])
    save(out/'native-input.json',{'cases':native});save(out/'render-cases.json',render);save(out/'changes.json',changes)
    executable=native_build(out)
    subprocess.run([str(executable),str(out/'native-input.json'),str(out/'native-grading.json')],check=True)
    grade=json.loads((out/'native-grading.json').read_text())
    report={'passed':True,'database_writes':0,'plan_sha256':hashlib.sha256(args.plan.read_bytes()).hexdigest(),
        'questions':len(cases),'fields':sum(x['fields'] for x in reports),'changed_attributes':len(changes),
        'saved_items':sum(x['saved_items']for x in reports),'incoming_use_snapshot_verified':bool(args.incoming_before),
        'explicit_item_snapshot_verified':bool(args.items_before),'identity_boolean_bank_key_and_state_preserved':True,
        'presentation_lint_passed':True,'native_grading_passed':grade['passed'],
        'native_grader_version':json.loads((out/'native-grader-version.json').read_text())if(out/'native-grader-version.json').exists()else {'mode':'working-tree-build'},'cases':reports}
    save(out/'verification.json',report)
    print(json.dumps({k:v for k,v in report.items()if k!='cases'},indent=2))

if __name__=='__main__':main()
