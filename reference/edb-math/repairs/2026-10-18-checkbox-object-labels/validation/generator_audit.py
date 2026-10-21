"""Read-only registration/source-snapshot follow-up inventory at audit basis."""
from pathlib import Path
import hashlib, json, re, sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import loads
from scripts.generator_publish import Publisher
from scripts.generator_packages import resolve_registered_script

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def kind(value):return value.get(':db/ident','')if isinstance(value,dict)else str(value)
def questions(value,pointer=''):
    if isinstance(value,dict):
        if ':question/answer-fields'in value:yield pointer,value
        for k,v in value.items():yield from questions(v,pointer+'/'+k)
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from questions(v,pointer+'/'+str(i))
def path_text(path):
    try:return str(path.relative_to(ROOT))
    except ValueError:return str(path)

def main():
    directory=HERE/'generators';captured=loads((directory/'capture-kps.edn').read_text())
    live=json.loads((HERE.parent/'questions.json').read_text())
    already={r['question']for r in json.loads((HERE.parent/'other-ledger.json').read_text())if r['status']=='already-complete'}
    candidates=[q for q in live if q[':db/id']not in already]
    identities={str(q[k])for q in candidates for k in [':db/id',':question/id',':question/math-academy-id']if k in q}
    pub=Publisher.from_environment(source=':agent/codex')
    registrations=[];snapshot_files=[];seen=set()
    for kp in captured:
        kid=kp[':db/id'];generator=kp.get(':knowledge-point/question-generator')
        item={'kp':kid,'title':kp.get(':knowledge-point/title'),'generator':generator,
            'candidate_questions':[q[':db/id']for q in candidates if any(k[':db/id']==kid for a in [':knowledge-point/_questions',':knowledge-point/_canonical-example']for k in q.get(a,[]))]}
        directories=[ROOT/'generate/scratch'/str(kid),ROOT/'generate/scratch'/(str(kid)+'-draft')]
        if generator:
            reference=generator[':question-generator/script']
            try:
                script=resolve_registered_script(reference,ROOT,pub.config.math_root)
                text=script.read_text();lines=text.splitlines()
                item.update({'script_path':path_text(script),'script_sha256':sha(script),
                    'checkbox_code_present':':answer-field.type/checkbox'in text or '"checkbox"'in text or "'checkbox'"in text,
                    'field_key_code':[{'line':i,'text':line.strip()}for i,line in enumerate(lines,1)if ':answer-field/key'in line],
                    'source_read_code':[{'line':i,'text':line.strip()}for i,line in enumerate(lines,1)if re.search(r'source|SOURCE|CAPTURE|EXTRACTION',line)and ('read_text' in line or 'json.load' in line)]})
                if script.name=='generator.py':directories.append(script.parent)
                elif script.parent!=ROOT/'generate/scratch':directories.append(script.parent)
                directories.append(script.with_suffix(''))
            except Exception as e:item['script_resolution_error']=str(e)
        paths=sorted({p for d in directories if d.is_dir()for p in d.rglob('source*.json')})
        evidence=[]
        for path in paths:
            if path in seen:continue
            seen.add(path)
            try:value=json.loads(path.read_text())
            except (OSError,ValueError):continue
            matched=[]
            for pointer,q in questions(value):
                if not any(str(q.get(k,''))in identities for k in [':db/id',':question/id',':question/math-academy-id']):continue
                fields=q.get(':question/answer-fields',[])
                boxes=[f for f in fields if kind(f.get(':answer-field/type'))==':answer-field.type/checkbox']
                matched.append({'pointer':pointer,'question_eid':q.get(':db/id'),'question_uuid':q.get(':question/id'),
                    'ma_id':q.get(':question/math-academy-id'),'checkbox_fields':len(boxes),
                    'keys':[f.get(':answer-field/key')for f in boxes],
                    'remote_label_keys':[f.get(':answer-field/key')for f in boxes if re.fullmatch(r'(?:[IVXLC]+|[A-Z]|Column\s+\d+)',f.get(':answer-field/key',''))],
                    'prompt_source_list':bool(re.search(r'(?m)^\s*(?:[-*]\s*)?(?:\*\*)?(?:I|II|III|IV|A|B|C)[.)](?:\*\*)?\s',q.get(':question/problem',''))),
                    'radio_fields':sum(kind(f.get(':answer-field/type'))==':answer-field.type/radio'for f in fields)})
            if matched:
                row={'kp':kid,'file':path_text(path),'sha256':sha(path),'captured_basis':value.get('basis')if isinstance(value,dict)else None,'questions':matched,
                    'checkbox_snapshot_needs_presentation_review':any(m['remote_label_keys']for m in matched),
                    'classification':'source snapshot; retained historical evidence is not an instruction to edit this file'}
                evidence.append(row['file']);snapshot_files.append(row)
        item['matching_source_snapshots']=evidence
        if generator:registrations.append(item)
    confirmed=[{'kp':17592186059848,'script':'generate/scratch/17592186059848.py','lines':[293,297,305,309],
                'reason':'Creates a Roman list of full statements in the prompt and checkbox keys I/II/III.'},
               {'kp':17592186124477,'script':'generate/scratch/17592186124477.py','lines':[93,96],
                'reason':'Creates checkbox keys Column N, leaving complete vectors in shared matrix.'},
               {'kp':17592186124478,'script':'generate/scratch/17592186124478.py','lines':[49,51],
                'reason':'Creates checkbox keys Column N without the corresponding complete column vectors.'}]
    report={'basis':3704,'candidate_questions':len(candidates),'candidate_kps':len(captured),
        'registered_generators':len(registrations),'registered_checkbox_code':sum(r.get('checkbox_code_present',False)for r in registrations),
        'matching_snapshot_files':len(snapshot_files),'snapshot_files_with_remote_checkbox_keys':sum(s['checkbox_snapshot_needs_presentation_review']for s in snapshot_files),
        'confirmed_generator_presentation_defects':confirmed,'registrations':registrations,'source_snapshots':snapshot_files,
        'limitations':'Static follow-up inventory, not generation/execution or exhaustive proof that every flagged generator emits the defect. Original radio captures may be valid retained evidence. No generator source or package was changed.',
        'database_writes':0}
    (directory/'audit.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ['registrations','source_snapshots']},indent=2))
if __name__=='__main__':main()
