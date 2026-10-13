"""Bind older original same-question solution graphics without relabeling failed aliases."""
from copy import deepcopy
from pathlib import Path
import hashlib,json,re,shutil
from scripts.storage import atomic_json,atomic_text,read_json

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
OLD=REPO/'reference/mathacademy/question-capture/14072804'
QUESTION='q-181775'
ALIASES=['https://mathacademy.com/graphics/q-181775-e-1','https://mathacademy.com/graphics/q-181775-e-2']

def normalized_solution(text):
    return re.sub(r'\s+',' ',re.sub(r'!\[[^]]*\]\([^)]*\)','@diagram@',str(text))).strip()

def typed_fields(question):
    result=[]
    for f in question.get('answer_fields',question.get('fields',[])):
        choices=[]
        for c in f.get('choices',[]):
            value=c.get('value')
            if c.get('type')=='image':
                path=Path(value)
                if not path.is_file():raise ValueError('Missing field-choice original image')
                value=hashlib.sha256(path.read_bytes()).hexdigest()
            choices.append((c.get('type'),value))
        result.append((f.get('key'),f.get('type'),sorted(choices)))
    return sorted(result)

def supplement_q181775(question,repair):
    if question.get('math_academy_id')!=QUESTION or not any(alias in str(question.get('errors',[])) for alias in ALIASES):return question
    before=read_json(OLD/'q-181775-before.json');solution=read_json(OLD/'history-q-181775.json')
    if before.get('dom_id')!='step-q181775' or solution.get('dom_id')!='questionExplanation-181775':raise ValueError('Older source identity changed')
    baseline_path=repair/'originals/content.json'
    baseline=read_json(baseline_path,{})
    candidates=[q for q in baseline.get('questions',[]) if q.get('math_academy_id')==QUESTION]
    if len(candidates)!=1:raise ValueError('No unique completed-capture source for typed-field binding')
    bound=candidates[0]
    if question.get('problem')!=before.get('problem') or bound.get('problem')!=before.get('problem') or typed_fields(bound)!=typed_fields(before):raise ValueError('Older source problem or completed-capture typed choice bytes do not match')
    if question.get('answer_fields',question.get('fields',[])) and typed_fields(question)!=typed_fields(before):raise ValueError('Current source record typed choice bytes do not match')
    if normalized_solution(question.get('worked_solution'))!=normalized_solution(solution.get('worked_solution')):raise ValueError('Older source solution text or mathematics differ')
    q=deepcopy(question);supplement=repair/'historical-solution-q181775-v1';supplement.mkdir(parents=True,exist_ok=True)
    old_problem=(OLD/'q-181775-before.json');old_solution=(OLD/'history-q-181775.json')
    for label,record,path in [('problem',before,old_problem),('solution',solution,old_solution)]:
        if not (supplement/(label+'-original.json')).exists():shutil.copyfile(path,supplement/(label+'-original.json'))
        atomic_text(supplement/(label+'-original.html'),record['html'])
    bindings=[];old_assets=[];worked=solution['worked_solution'];capture=repair.parents[1]
    for index,asset in enumerate(solution.get('assets',[])):
        source=Path(asset['path']);data=source.read_bytes();sha=hashlib.sha256(data).hexdigest()
        if sha!=asset.get('sha256'):raise ValueError('Older source original bytes fail SHA-256 check')
        target=capture/'assets'/source.name
        if target.exists() and target.read_bytes()!=data:raise ValueError('Existing original asset differs')
        if not target.exists():shutil.copyfile(source,target)
        recovered=deepcopy(asset);recovered.update(path=str(target.resolve()),representation='original',
            historical_source={'task_id':'14072804','question_id':QUESTION,'json_file':str(old_solution),'html_file':str(supplement/'solution-original.html')})
        recovered.pop('unavailable',None);recovered.pop('render_unavailable',None)
        old_assets.append(recovered);worked=worked.replace(asset['path'],str(target.resolve()))
        bindings.append({'older_source_url':asset['source_url'],'older_asset_sha256':sha,
            'older_asset_path':str(source),'recovered_original_path':str(target.resolve()),
            'unavailable_newer_alias':ALIASES[index-1] if index in (1,2) else None})
    original_errors=deepcopy(q.get('errors',[]));original_failed_assets=[deepcopy(a) for a in q.get('assets',[]) if a.get('source_url') in ALIASES]
    q['worked_solution']=worked
    q['assets']=[a for a in q.get('assets',[]) if a.get('extraction_part')!='solution']+old_assets
    q['errors']=[error for error in original_errors if not any(alias in str(error) for alias in ALIASES)]
    q.setdefault('extraction_error_history',[]).append({'errors':[e for e in original_errors if any(a in str(e) for a in ALIASES)],
        'parts':['solution'],'retired_by':'Older same-question authored solution with matching text/math and verified original graphic bytes',
        'source_file':question.get('html_path'),'historical_supplement':str(supplement/'provenance.json')})
    q['extraction_parts']=list(set(q.get('extraction_parts',[]))|{'solution'})
    q['solution_evidence']=str(supplement/'solution-original.html')
    provenance={'question_id':QUESTION,'older_problem_dom_id':before['dom_id'],'older_solution_dom_id':solution['dom_id'],
        'completed_capture_field_binding_file':str(baseline_path),'completed_capture_field_binding_sha256':hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        'problem_exact_match':True,'typed_fields_and_image_choice_bytes_match':True,'nonimage_worked_solution_text_math_match':True,
        'older_problem_json_sha256':hashlib.sha256(old_problem.read_bytes()).hexdigest(),
        'older_solution_json_sha256':hashlib.sha256(old_solution.read_bytes()).hexdigest(),
        'older_problem_html_sha256':hashlib.sha256(before['html'].encode()).hexdigest(),
        'older_solution_html_sha256':hashlib.sha256(solution['html'].encode()).hexdigest(),
        'newer_source_file':question.get('html_path'),'newer_source_sha256':hashlib.sha256(Path(question['html_path']).read_bytes()).hexdigest(),
        'failed_newer_assets':original_failed_assets,'failed_newer_errors':original_errors,'asset_bindings':bindings,
        'statement':'Older original authored solution evidence supplements failed newer aliases; no claim that current aliases were fetched or their bytes match.'}
    atomic_json(supplement/'provenance.json',provenance)
    q['historical_solution_supplement']=str(supplement/'provenance.json')
    return q

def validate_cached_graphics(question,repair):
    """Use verified original bytes to retire display-only failures; preserve failure history."""
    from PIL import Image
    q=deepcopy(question);retired=[];audits=[]
    for error in q.get('errors',[]):
        prefix='Graphic rendering unavailable: '
        if not str(error).startswith(prefix):continue
        url=str(error)[len(prefix):]
        assets=[a for a in q.get('assets',[]) if a.get('source_url')==url and a.get('path') and a.get('sha256') and not a.get('unavailable')]
        if len(assets)!=1:continue
        asset=assets[0]
        if asset.get('extraction_part')!='solution' or asset['path'] not in str(q.get('worked_solution','')):continue
        path=Path(asset['path']);data=path.read_bytes()
        if hashlib.sha256(data).hexdigest()!=asset['sha256']:continue
        try:
            with Image.open(path) as image:image.verify()
            with Image.open(path) as image:image.load();size=list(image.size);fmt=image.format
        except Exception:continue
        audit={'source_url':url,'original_path':str(path),'original_sha256':asset['sha256'],
            'dimensions':size,'format':fmt,'retired_error':error,
            'original_render_unavailable':asset.get('render_unavailable'),
            'statement':'Original image bytes fully decode and match exact saved source URL/hash; this does not claim a browser redisplay or a new fetch.'}
        auditpath=repair/'cached-original-graphics'/(asset['sha256']+'.json');atomic_json(auditpath,audit)
        asset['original_image_validation']=str(auditpath);asset.pop('render_unavailable',None)
        retired.append(error);audits.append(str(auditpath))
    if retired:
        q['errors']=[e for e in q.get('errors',[]) if e not in retired]
        q.setdefault('extraction_error_history',[]).append({'errors':retired,'parts':['solution'],
            'retired_by':'Hash-verified and fully decoded original image bytes for identical saved source URLs',
            'original_image_validation':audits,'source_file':question.get('html_path')})
    return q
