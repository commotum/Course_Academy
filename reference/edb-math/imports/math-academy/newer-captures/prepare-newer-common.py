import collections
import copy
import hashlib
import json
import re
import sys
import uuid
from pathlib import Path

sys.path.insert(0,'/home/jake/Developer/Course_Academy/scripts/question_capture')
from edn import dumps, loads, kw
OUT=Path('/tmp/newer-captures-prepared')
SNAP=Path('/tmp/newer-live-snapshot')
MATH=Path('/media/jake/SSD/EDB/math')
def ident(kind,value):
    return uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy:ma:{kind}:{value}')
def load(name):return json.loads((OUT/name).read_text())
def save(name,obj):
    path=OUT/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
existing={}
for file in sorted(SNAP.glob('questions-*-result.edn')):
    for row in loads(file.read_text()):
        q=row[0];existing[q[kw('question/math-academy-id')]]=q
topics={};kps={}
for file in sorted(SNAP.glob('topics-*-result.edn')):
    for row in loads(file.read_text()):
        t=row[0];tid=t[kw('topic/math-academy-id')];topics[tid]=t
        for kp in t.get(kw('topic/knowledge-points'),[]):
            e=kp.get(kw('knowledge-point/canonical-example'),{}).get(kw('question/math-academy-id'))
            if e:kps[(tid,e[2:])]=kp[kw('knowledge-point/id')]
records=load('source-occurrences.json')['records']
latest={q['math_academy_id']:q for q in sorted(records,key=lambda x:(x['basis'],int(x['task']),x['stream']))}
qids={mid:existing[mid][kw('question/id')] if mid in existing else ident('example' if mid.startswith('e-') else 'question',mid[2:]) for mid in latest}
assets={}
def image(path):
    if path.startswith('images/'):
        assert (MATH/path).is_file(),path
        return path
    if path not in assets:
        p=Path(path);assert p.is_file(),path
        data=p.read_bytes();assert data.startswith(b'\x89PNG\r\n\x1a\n'),path
        digest=hashlib.sha256(data).hexdigest();relative=f'images/{digest[:2]}/{digest}.png'
        target=OUT/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if not (MATH/relative).exists() and not target.exists():target.write_bytes(data)
        assets[path]={'source_path':path,'path':relative,'sha256':digest}
    return assets[path]['path']
def rewrite(text):
    return re.sub(r'(!\[[^\]]*\]\()([^\s)]+)\)',lambda m:m[1]+image(m[2])+')',text)
def field_forms(mid,fields,version):
    result=[]
    for f in fields:
        fid=ident('capture-field-version',f'{mid}:{f["key"]}:{version}')
        temp=f'field-{fid}';choices=[];seen={}
        correct=f.get('correct')
        if correct is None:
            matches=[c for c in f['choices'] if c['value']==f['correct_value']]
            assert len(matches)==1,(mid,f['key'],f.get('correct_value'))
            correct=matches[0]
        for c in f['choices']:
            kind=c['type'];value=image(c['value']) if kind=='image' else rewrite(c['value'])
            pair=(kind,value)
            if pair in seen:continue
            aid=ident('capture-answer-version',f'{fid}:{len(choices)}')
            atemp=f'answer-{aid}';seen[pair]=atemp
            choices.append({kw('db/id'):atemp,kw('answer/id'):aid,kw('answer/type'):kw('answer.type/'+kind),kw('answer/value'):value,kw('db/ensure'):kw('answer/validate')})
        value=image(correct['value']) if correct['type']=='image' else rewrite(correct['value'])
        assert (correct['type'],value) in seen,(mid,f['key'],'correct answer not in choices')
        result.append({kw('db/id'):temp,kw('answer-field/id'):fid,kw('answer-field/key'):f['key'],kw('answer-field/type'):kw('answer-field.type/'+f['type']),kw('answer-field/choices'):choices,kw('answer-field/correct'):seen[(correct['type'],value)],kw('db/ensure'):kw('answer-field/validate')})
    return result
def field_ids(mid,fields,version):return [ident('capture-field-version',f'{mid}:{f["key"]}:{version}') for f in fields]
def write_edn(name,forms,comment):
    path=OUT/name;path.parent.mkdir(parents=True,exist_ok=True)
    text='[\n'+'\n'.join(' '+dumps(f) for f in forms)+'\n]\n'
    assert loads(text)==forms,name
    assert len(text.encode())<16*1024*1024,name
    path.write_text(comment+'\n'+text)
    return {'file':name,'bytes':path.stat().st_size,'forms':len(forms)}
def serialized_fields(q):
    return [{'key':f['key'],'type':f['type'],'choices':f['choices'],'correct_value':f.get('correct_value')} for f in q.get('answer_fields',[])]

def corrections():
    events=load('correction-events.json')['events'];previous={};manifest=[]
    grouped=collections.defaultdict(list)
    for e in events:grouped[e['old_basis']].append(e)
    for number,(basis,group) in enumerate(sorted(grouped.items()),1):
        forms=[]
        for event in group:
            mid=event['question'];qid=qids[mid]
            original=event['original_content'];corrected=event['corrected_content']
            form={kw('db/id'):[kw('question/id'),qid],kw('question/id'):qid,kw('db/ensure'):kw('question/validate')}
            for key in ['problem','worked_solution']:
                if original.get(key)!=corrected.get(key):
                    form[kw('question/'+key.replace('_','-'))]=rewrite(corrected[key])
            if serialized_fields(original)!=serialized_fields(corrected):
                old=previous.get(mid)
                if old is None:
                    old=field_ids(mid,latest[mid]['answer_fields'],'original') if latest[mid]['answer_fields'] else [f[kw('answer-field/id')] for f in existing.get(mid,{}).get(kw('question/answer-fields'),[])]
                for fid in old:
                    forms.append([kw('db/retract'),[kw('question/id'),qid],kw('question/answer-fields'),[kw('answer-field/id'),fid]])
                version=f'correction-{basis}'
                form[kw('question/answer-fields')]=field_forms(mid,corrected['answer_fields'],version)
                previous[mid]=field_ids(mid,corrected['answer_fields'],version)
            forms.append(form)
        name=f'2-corrections/{number:03d}-old-basis-{basis}.edn'
        entry=write_edn(name,forms,';; PREPARED ONLY. Apply after ALL original MA batches.\n;; Source: assistant entity to be created later; do not use :person/jake or :org/Math-Academy.\n;; Retractions remove ownership links; original field and answer entities remain in history.')
        entry.update({'old_basis':basis,'questions':[e['question'] for e in group],'source':None,'requires_assistant_source':True})
        manifest.append(entry)
    save('correction-batches.json',{'transacted':False,'source':None,'source_required':'Assistant source entity to be created later','requires_all_originals_first':True,'batches':manifest})
    save('asset-map.json',assets)
    print(json.dumps({'correction_batches':len(manifest),'correction_events':len(events),'correction_images':len(assets)},indent=2))
if __name__=='__main__':corrections()
