"""Restore the lesson definition invalidated by the repaired phantom example."""
import copy
import hashlib
import json
import pathlib
import sys
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'capture'))
from playwright.sync_api import sync_playwright
from scripts.browser.adapter import EXTRACT
from scripts.browser.parsing import parse_lesson_structure
from scripts.config import Config
from scripts.database.pipeline import DatabasePipeline
from scripts.storage import atomic_json, file_lock
from scripts.outbox import target_id

config = Config(account='multivariable')
capture = config.output_root / '14133043'
archive = pathlib.Path(__file__).resolve().parent / 'multivariable/14133043'
with file_lock(config.database_lock):
    content = json.loads((capture / 'content.json').read_text())
    previous = content['lesson_definition']
    source = pathlib.Path(previous['source_file'])
    html = source.read_text()
    definition = parse_lesson_structure(html, content['topic_id'])
    if not definition['complete']:
        raise ValueError('Saved source does not have a complete authored lesson route')
    if [(s['math_academy_id'],s['type'],s['content_id']) for s in definition['steps']] != [
            (s['math_academy_id'],s['type'],s['content_id']) for s in previous['steps']]:
        raise ValueError('Authored lesson route changed')
    checked = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.route('**/*', lambda route: route.abort())
        page.set_content(html)
        for step in definition['steps']:
            item = page.locator(f'div.step[stepid="{step["math_academy_id"]}"]').evaluate(EXTRACT)
            if item['errors'] or not item['problem'] or (step['type']=='example' and not item['worked_solution']):
                raise ValueError('Lesson step still has incomplete extraction: ' + str(step['math_academy_id']))
            records = content['tutorials' if step['type']=='tutorial' else 'canonical_examples']
            mid = step['content_id'] if step['type']=='tutorial' else 'e-'+str(step['content_id'])
            record = next(r for r in records if str(r['math_academy_id'])==str(mid))
            # The pure extractor emits graphic markers. Bind each to the
            # same captured SVG and verified local bytes before comparing.
            for asset in item.get('assets', []):
                saved = next(a for a in record.get('assets', []) if a['index']==asset['index'])
                if asset['html'] != saved['html'] or hashlib.sha256(pathlib.Path(saved['path']).read_bytes()).hexdigest()!=saved['sha256']:
                    raise ValueError('Lesson graphic does not match the captured source')
                for key in ('problem','worked_solution'):
                    item[key] = item[key].replace('@asset-'+str(asset['index'])+'@',saved['path'])
            if record.get('errors') or record['problem']!=item['problem'] or (
                    step['type']=='example' and record['worked_solution']!=item['worked_solution']):
                raise ValueError('Saved record does not agree with full source definition')
            checked.append(step['math_academy_id'])
        browser.close()
    repaired = copy.deepcopy(previous)
    repaired['complete'] = True
    repaired.pop('issues',None)
    repaired['extraction_repair'] = {'previous_issues': previous.get('issues',[]),
        'source_file':str(source), 'source_sha256':hashlib.sha256(html.encode()).hexdigest(),
        'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(), 'verified_steps':checked}
    content['lesson_definition'] = repaired
    atomic_json(archive / 'definition-repair.json', {'before':previous,'after':repaired})
    atomic_json(capture / 'content.json', content)
    item_path = next(p for p in config.spool_root.glob('*.json')
        if (item:=json.loads(p.read_text())).get('capture_directory')==str(capture)
        and item.get('target_id')==target_id(config))
    item=json.loads(item_path.read_text());item.update(status='pending',next_attempt_at=0)
    item.pop('result',None);item.pop('error',None);atomic_json(item_path,item)
    result=DatabasePipeline(config,threading.Event()).process(capture)
    atomic_json(archive/'result.json',result)
    item.update(status=result['status'] if result['status'] in ('verified','no_changes') else 'pending',
        result=result,last_attempt_at=time.time(),attempts=item.get('attempts',0)+1)
    atomic_json(item_path,item);atomic_json(capture/'import-status.json',item)
    print(result['status'],'omissions',result.get('omissions'),flush=True)
    if result['status'] not in ('verified','no_changes') or result.get('omissions'):
        raise ValueError('Complete lesson repair was not verified: '+str(result))
