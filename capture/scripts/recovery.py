"""Source-only historical recovery; never replay activities or account ledgers."""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shutil
import threading
import time
from urllib.parse import urljoin

from .activity.capture import ActivityCapture
from .activity.evidence import capture_gaps, merge_question, finalize_answers, question_key
from .activity.solver import SolverClient
from .browser.adapter import EXTRACT
from .browser.assets import replace_markers, solution_image_bindings, standalone_svg, recover_original_raster
from .browser.parsing import parse_dashboard
from .config import Config
from .database.evidence import authoritative_question, UnsupportedContent
from .database.pipeline import DatabasePipeline
from .outbox import enqueue, target_id
from .progress import compare_progress
from .storage import atomic_json, atomic_text, file_lock, read_json


def version():
    root = Path(__file__).parent
    paths = ['browser/extract.js', 'browser/assets.py', 'activity/capture.py', 'activity/evidence.py', 'database/evidence.py',
             'recovery.py', 'database/text.py']
    return hashlib.sha256(b''.join((root/name).read_bytes() for name in paths)).hexdigest()


def archive(directory, repair):
    original = repair / 'originals'
    for name in ['checkpoint.json', 'content.json', 'history-content.json', 'capture-complete.json',
                 'import-status.json', 'post-activity.json', 'progress-comparison.json',
                 'database/result.json', 'database/preparation.json']:
        path = directory / name
        if path.exists() and not (original/name).exists():
            (original/name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, original/name)
    atomic_json(repair/'original-hashes.json', {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in original.rglob('*') if p.is_file()})


def _verified_recovery_identity(record, parsed, actual_dom_id, *, history=False):
    """Only a stable, matching source root can bind a historical reread."""
    expected = record.get('dom_id')
    if expected and actual_dom_id != expected or parsed.get('dom_id') != actual_dom_id:
        raise ValueError('Saved source root identity changed during recovery')
    saved = record.get('math_academy_id')
    if saved is not None and not re.fullmatch(r'[qe]-\d+', str(saved)):
        raise ValueError('Saved question has an invalid source identity')
    root = actual_dom_id or ''
    match = re.fullmatch(r'step-([qe])(\d+)', root)
    identity = match[1] + '-' + match[2] if match else None
    if not identity:
        match = re.fullmatch(r'questionExplanation-(\d+)', root)
        if not match and (history or saved):
            match = re.fullmatch(r'question-(\d+)', root)
        if match:
            identity = 'q-' + match[1]
    if identity and saved and identity != saved:
        raise ValueError('Saved question source identity conflicts with its DOM root: ' + str(saved) + ' versus ' + identity)
    return identity


def reextract_record(record, page, repair, *, history=False, prior=None):
    markup = record.get('html')
    if not markup and record.get('html_path') and Path(record['html_path']).is_file():
        markup = Path(record['html_path']).read_text()
    if not markup:
        return deepcopy(record)
    page.set_content(markup)
    selector = '[id='+json.dumps(record['dom_id'])+']' if record.get('dom_id') else 'body'
    node = page.locator(selector)
    if node.count() != 1:
        raise ValueError('Saved source node is ambiguous: '+selector)
    parsed = node.evaluate(EXTRACT, {'history_grade': record.get('grade') or record.get('result')} if history else {})
    placement_type = node.get_attribute('steptype')
    placement_content = node.get_attribute('contentid')
    if placement_type in ('example', 'tutorial') and re.fullmatch(r'step-\d+', node.get_attribute('id') or ''):
        identity = ('e-' if placement_type == 'example' else '') + str(placement_content)
        if (node.get_attribute('id') != record.get('dom_id') or not str(placement_content).isdigit()
                or str(record.get('math_academy_id')) != identity):
            raise ValueError('Saved lesson placement conflicts with its content identity')
    else:
        identity = _verified_recovery_identity(record, parsed, node.get_attribute('id') or '', history=history)
    if identity:
        parsed['math_academy_id'] = identity
    replacements = {}
    for asset in parsed['assets']:
        if asset.get('source_url'):
            asset['source_url'] = urljoin(record.get('source_url') or 'https://mathacademy.com/', asset['source_url'])
    recovered_images = solution_image_bindings(parsed, prior)
    for asset in parsed['assets']:
        source = urljoin(record.get('source_url') or 'https://mathacademy.com/', asset.get('source_url') or '')
        matches = [old for old in record.get('assets', []) if old.get('path') and old.get('tag') == asset['tag'] and
            old.get('extraction_part') == asset.get('extraction_part') and
            (asset.get('source_url') and urljoin(record.get('source_url') or 'https://mathacademy.com/',old.get('source_url') or '') == source
             or old.get('html') == asset['html'])]
        if asset['tag'] == 'svg' and not matches:
            # Reparse the actual saved SVG, retaining its original bytes and
            # any exact shared definitions found in this saved source page.
            original = asset['html'].encode()
            data, definitions = standalone_svg(asset['html'], page)
            source_digest = hashlib.sha256(original).hexdigest()
            source_path = repair/'source'/(source_digest+'.svg')
            atomic_text(source_path, asset['html'])
            target = repair/'assets'/(hashlib.sha256(data).hexdigest()+'.svg')
            from .storage import atomic_bytes
            atomic_bytes(target, data)
            old = {'path':str(target.resolve()), 'sha256':hashlib.sha256(data).hexdigest(),
                'content_type':'image/svg+xml', 'representation':'standalone_svg',
                'original_svg_path':str(source_path.resolve()), 'original_svg_sha256':source_digest,
                'standalone_definitions':definitions}
        elif asset['index'] in recovered_images:
            old = recovered_images[asset['index']]
            asset['recovered_from'] = {'reason':'Verified complete solution and matching solution image occurrence',
                'source_url':old.get('source_url'), 'original_image_validation':old['original_image_validation']}
        elif matches:
            old = matches[0]
        else:
            raise ValueError('No original asset binding for '+str(asset.get('source_url') or asset['index']))
        if not Path(old['path']).is_file() or old.get('sha256') and hashlib.sha256(Path(old['path']).read_bytes()).hexdigest() != old['sha256']:
            raise ValueError('Original asset bytes unavailable or hash mismatch: '+old['path'])
        asset.update({k:deepcopy(v) for k,v in old.items() if k not in ('index','html','dom_index','extraction_part','source_url')})
        recover_original_raster(parsed, asset)
        replacements['@asset-'+str(asset['index'])+'@'] = old['path']
    parsed = replace_markers(parsed, replacements)
    source_hash = hashlib.sha256(markup.encode()).hexdigest()
    evidence = repair/'source'/(source_hash+'.html')
    if not evidence.exists(): atomic_text(evidence, markup)
    parsed.update(html_path=str(evidence.resolve()), source_file=str(evidence.resolve()),
        source_url=record.get('source_url'), captured_at=record.get('captured_at'),
        recovery={'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(), 'original_source':record.get('html_path'), 'source_sha256':source_hash})
    old_fields = {f.get('key'):f for f in record.get('answer_fields',record.get('fields',[]))}
    for field in parsed['fields']:
        observed = field.get('source_correct')
        if observed and observed.get('value') is not None:
            field.update(correct_value=observed['value'], evidence={'kind':'ma_answer','value':observed['value'],'source_file':str(evidence.resolve())})
        else:
            old = old_fields.get(field['key'],{})
            signature = lambda f: (f.get('type'),sorted((c.get('type'),c.get('value')) for c in f.get('choices',[])))
            if signature(old) == signature(field):
                for key in ['correct_value','correct_type','value_type','evidence','correct_evidence']:
                    if old.get(key) is not None:field[key]=deepcopy(old[key])
    # Preserve solution-only evidence that lives outside this question's HTML.
    if record.get('worked_solution') and not parsed.get('worked_solution'):
        parsed.pop('worked_solution',None)
    return merge_question(record,parsed)


def repair_saved_capture(config, directory, page, *, apply=True):
    """Repair saved source structure; retain judgments and use the normal batch queue."""
    directory = Path(directory).resolve()
    if directory.parent != config.output_root or not (directory/'capture-complete.json').exists():
        raise ValueError('Source repair requires a completed capture for this account')
    repair = directory/'repairs'/('source-health-'+version()[:16])
    with file_lock(config.database_lock):
        active = read_json(config.state_root/'active.json',{}) or {}
        if active.get('directory') == str(directory):
            raise ValueError('Do not rewrite an active capture')
        if (directory/'database/request.json').exists():
            raise ValueError('Recover the exact pending request before repairing its source')
        for pointer in config.spool_root.glob('batches/*/active.json'):
            for path in (read_json(pointer,{}) or {}).get('spool_paths',[]):
                if (read_json(Path(path),{}) or {}).get('capture_directory') == str(directory):
                    raise ValueError('Wait for the active batch outcome before repairing its source')
        archive(directory,repair)
    checkpoint = read_json(repair/'originals/checkpoint.json')
    original = read_json(repair/'originals/content.json')
    if not checkpoint or not original:
        raise ValueError('Completed source repair requires its original checkpoint and content')
    history = deepcopy(checkpoint['history'])
    records = list(checkpoint['presentations'].values())
    for bucket in ('questions','canonical_examples','tutorials'):
        for index, question in enumerate(history.get(bucket,[])):
            if not question.get('errors'):
                continue
            if bucket == 'questions':
                identity = question.get('math_academy_id')
                prior = next((r['question'] for r in records if r['question'].get('math_academy_id') == identity),None)
                source = question.get('solution_evidence')
                if not source:
                    candidates = sorted((directory/'observations').glob('history-solution-'+str(identity)+'-*.html'))
                    source = str(candidates[-1]) if candidates else None
                if not source:
                    raise ValueError('No saved solution source for '+str(identity))
                fragment = {**question, 'dom_id':'questionExplanation-'+identity.removeprefix('q-'),
                    'html':Path(source).read_text(), 'html_path':source,
                    'assets':[a for a in question.get('assets',[]) if a.get('extraction_part')=='solution']}
                recovered = reextract_record(fragment,page,repair,history=True,prior=prior)
                history[bucket][index] = merge_question(question,recovered)
            else:
                history[bucket][index] = reextract_record(question,page,repair)
                if bucket == 'tutorials':
                    history[bucket][index]['content'] = history[bucket][index]['problem']
    if history.get('lesson_definition'):
        definition = history['lesson_definition']
        by_placement = {str(q.get('dom_id')):q for bucket in ('canonical_examples','tutorials') for q in history.get(bucket,[])}
        definition['issues'] = [issue for issue in definition.get('issues',[]) if
            issue.get('reason') != 'Incomplete lesson content or source extraction errors' or
            by_placement.get('step-'+str(issue.get('step')),{}).get('errors') or
            'step-'+str(issue.get('step')) not in by_placement]
        definition['complete'] = bool(definition.get('steps')) and not definition['issues']
    checkpoint['history'] = history
    capture = ActivityCapture.__new__(ActivityCapture)
    capture.activity, capture.state = checkpoint['activity'], checkpoint
    capture.exposures = None
    capture._save = lambda: atomic_json(repair/'checkpoint.json',capture.state)
    merged = capture._merge_history(history)
    content = {**original, **merged}
    judgments = list(checkpoint['judgments'].values())
    # Recheck an earlier repair judgment against the current source rather than
    # asking for the same mathematics again when only recovery code changed.
    for saved in directory.glob('repairs/source-health-*/content.json'):
        if saved.parent == repair:
            continue
        earlier = read_json(saved,{}) or {}
        for bucket in ('questions','canonical_examples'):
            for question in earlier.get(bucket,[]):
                judgment = question.get('answer_validation',{}).get('previous_judgment')
                if judgment and judgment.get('question_id') == question.get('math_academy_id'):
                    judgments.append(judgment)
    for bucket in ('questions','canonical_examples'):
        finalized = []
        for question in content.get(bucket,[]):
            mid = question.get('math_academy_id')
            candidates = [j for j in judgments if j.get('record_kind',bucket)==bucket and
                (str(j.get('question_id'))==str(mid) or j.get('capture_key')==question.get('source_id') or
                 str(j.get('capture_key','')).endswith(str(question.get('dom_id'))))]
            judgment = max(candidates,key=lambda j:(
                sum(a.get('ma_basis') not in (None,'none') and a.get('ma_value') is not None for a in j.get('answers',[])),
                len(j.get('answers',[])),j.get('status') != 'unavailable'),default={'answers':[]})
            presentations = capture._question_presentations(question)
            try:
                supported = authoritative_question(finalize_answers(question,presentations,judgment),example=bucket=='canonical_examples')
            except UnsupportedContent as error:
                if question.get('errors') or not question.get('math_academy_id'):
                    raise  # A mathematical judgment cannot repair missing source structure.
                from .activity.task_payload import task_payload
                payload = task_payload('judge_question',{'question':question,'presentations':presentations,
                    'gap':str(error),'previous_judgment':judgment,
                    'recovery':'The saved source has been repaired and its identity checked. Judge the current full source and fields. Use exact contiguous Math Academy solution quotations when confirming the answer key; retain any authored mathematical error separately.'})
                judgment = SolverClient(config,repair,threading.Event()).request('judge_question',payload)
                judgment.update(question_id=mid,capture_key=question_key(question),record_kind=bucket,final=True)
                supported = authoritative_question(finalize_answers(question,presentations,judgment),example=bucket=='canonical_examples')
                judgments.append(judgment)
            supported['answer_validation'] = {'status':'supported','version':1,
                'recovery_source':str(repair.resolve()), 'previous_judgment':judgment}
            finalized.append(supported)
        content[bucket] = finalized
    content['judgments'] = judgments
    content['source_limitations'] = merged.get('source_limitations',[])
    content['source_repair'] = {'directory':str(repair.resolve()),'version':version(),'prepared_at':time.time()}
    gaps = capture_gaps(content)
    if gaps:
        atomic_json(repair/'remaining-gaps.json',gaps)
        raise ValueError('Saved source repair remains incomplete; original capture retained')
    atomic_json(repair/'content.json',content)
    result = {'status':'prepared','directory':str(directory),'repair':str(repair),'gaps':[]}
    if apply:
        with file_lock(config.database_lock):
            if list(config.spool_root.glob('batches/*/active.json')) or (directory/'database/request.json').exists():
                raise ValueError('Wait for the current database batch before queuing source repairs')
            atomic_json(directory/'content.json',content)
            atomic_json(directory/'history-content.json',history)
            spool = enqueue(config,directory)
            item = read_json(spool)
            item.update(status='pending',next_attempt_at=0,source_repair=str(repair.resolve()))
            item.pop('error',None)
            atomic_json(spool,item)
            atomic_json(directory/'import-status.json',item)
            result['status'] = 'queued'
    atomic_json(repair/'result.json',result)
    return result


def reprocess(config, directory, page, *, apply=True):
    directory=Path(directory).resolve()
    if directory.parent != config.output_root or not (directory/'capture-complete.json').exists():
        raise ValueError('Recovery requires a completed capture in the account output directory')
    active=read_json(config.state_root/'active.json',{}) or {}
    if active.get('directory') == str(directory):raise ValueError('Do not rewrite an active capture')
    repair=directory/'repairs'/('completeness-'+version()[:16]);repair.mkdir(parents=True,exist_ok=True)
    saved=read_json(repair/'result.json')
    if saved and saved.get('status')=='verified':return saved
    with file_lock(config.database_lock):
        if (directory/'database/request.json').exists():
            if not apply:
                raise ValueError('An original database request must be recovered before preparing a revision')
            outcome=DatabasePipeline(config,threading.Event()).process(directory,apply=True)
            if (directory/'database/request.json').exists():raise ValueError('An original database request remains unresolved: '+str(outcome.get('reason')))
        archive(directory,repair)
        checkpoint=read_json(repair/'originals/checkpoint.json')
        if not checkpoint:raise ValueError('No historical checkpoint')
    for record in checkpoint.get('presentations',{}).values():
        record['question']=reextract_record(record['question'],page,repair)
    for step in checkpoint.get('steps',[]):
        if step.get('question'):step['question']=reextract_record(step['question'],page,repair)
    history=checkpoint['history']
    for bucket in ['questions','canonical_examples']:
        history[bucket]=[reextract_record(q,page,repair,history=bucket=='questions') for q in history.get(bucket,[])]
    checkpoint['source_recovery_attempted']=True
    capture=ActivityCapture(config,None,threading.Event(),solver=SolverClient(config,repair,threading.Event()))
    capture.activity=checkpoint['activity'];capture.directory=directory;capture.state=checkpoint
    capture.checkpoint_path=repair/'checkpoint.json'
    content=capture._review()
    original=read_json(repair/'originals/content.json')
    for key in ['completion','base_xp','captured_at','policy','topic_context','pipeline','capture_version']:
        if key in original:content[key]=deepcopy(original[key])
    content['attempts']=list(checkpoint['presentations'].values())
    content['judgments']=list(checkpoint['judgments'].values())
    content['recovery_version']=version()
    content['reprocessed_at']=time.time()
    atomic_json(repair/'content.json',content)
    atomic_json(repair/'validation.json',{'gaps':capture_gaps(content),'answers':[
        {'id':q.get('math_academy_id'),'capture_key':q.get('source_id'),'validation':q.get('answer_validation')}
        for q in content.get('questions',[])+content.get('canonical_examples',[])]})
    if not apply:return {'status':'prepared','directory':str(directory),'repair':str(repair)}
    with file_lock(config.database_lock):
        # The account checkpoints and ledgers remain untouched. Only its finished
        # package and corresponding outbox entry are revised under the DB lock.
        atomic_json(directory/'content.json',content)
        atomic_json(directory/'history-content.json',history)
        spool=enqueue(config,directory);item=read_json(spool)
        if not (repair/'outbox-original.json').exists():atomic_json(repair/'outbox-original.json',item)
        if item.get('capture_only') or config.capture_only:
            result={'status':'capture_only','directory':str(directory),'repair':str(repair),
                'database_writes':0,'questions':len(content.get('questions',[]))}
            atomic_json(repair/'result.json',result)
            return result
        item.update(status='pending',next_attempt_at=0,recovery_version=version())
        item.pop('error',None)
        atomic_json(spool,item);atomic_json(directory/'import-status.json',item)
        result={'status':'queued','directory':str(directory),'repair':str(repair),
            'questions':len(content.get('questions',[])),'version':version(),'prepared_at':time.time(),
            'minimum_questions':config.database_batch_questions}
        atomic_json(repair/'result.json',result)
        return result


def backfill_progress(config, directory):
    directory=Path(directory);post=read_json(directory/'post-activity.json')
    if not post:return {'status':'unavailable','reason':'No saved post-activity observations'}
    repair=directory/'repairs'/'historical-progress-v1';archive(directory,repair)
    observations=post.get('observations',{});dashboard=observations.get('dashboard',{})
    source=Path(dashboard['html_path']) if dashboard.get('html_path') else None
    if source and source.is_file():
        dashboard['course_progress']=parse_dashboard(source.read_text(),directory.name).get('course_progress')
        dashboard['course_progress_recovery']={'source_file':str(source),'method':'saved Learn page #coursePercentComplete'}
    baseline=read_json(directory/'progress-before.json',{})
    comparison=compare_progress(baseline,observations)
    comparison.update(task_id=directory.name,baseline_source='progress-before.json',recovered_from_saved_evidence=True)
    atomic_json(directory/'progress-comparison.json',comparison)
    post['progress_comparison']=comparison
    for entry in post.get('observation_history',[]):
        obs=entry.get('observations',{});dash=obs.get('dashboard',{})
        path=Path(dash['html_path']) if dash.get('html_path') else None
        if path and path.is_file():dash['course_progress']=parse_dashboard(path.read_text(),directory.name).get('course_progress')
        entry['progress_comparison']=compare_progress(baseline,obs)
    atomic_json(directory/'post-activity.json',post)
    result={'status':'recovered','course_progress':dashboard.get('course_progress'),
        'comparison_available':comparison['comparison_available'],'observed_at':post.get('observed_at')}
    atomic_json(repair/'result.json',result);return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['reprocess','sources','progress']);parser.add_argument('--account',required=True)
    parser.add_argument('directories',nargs='+',type=Path);parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args();config=Config(account=args.account)
    if args.action=='progress':
        for directory in args.directories:print(json.dumps({'directory':str(directory),**backfill_progress(config,directory)}),flush=True)
    else:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True);context=browser.new_context()
            context.route('**/*',lambda route:route.abort());page=context.new_page()
            operation = repair_saved_capture if args.action=='sources' else reprocess
            for directory in args.directories:print(json.dumps(operation(config,directory,page,apply=not args.prepare_only)),flush=True)
            browser.close()

if __name__=='__main__':main()
