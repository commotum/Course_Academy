import copy, hashlib, json, pathlib, sys
sys.path.insert(0, '/home/jake/Developer/Course_Academy/capture')
from playwright.sync_api import sync_playwright
from scripts.browser.adapter import EXTRACT
from scripts.database.evidence import authoritative_question
from scripts.storage import atomic_json

ROOT = pathlib.Path('/home/jake/Developer/Course_Academy')
ERROR = 'Unsupported decorated MathML phantom: hidden geometry attributes'
CAPTURES = [('linear','14132728'),('multivariable','14133043'),('foundations','14134284'),('foundations','14131517')]
report = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page()
    page.route('**/*', lambda route: route.abort())
    for account, task in CAPTURES:
        directory = ROOT / 'reference/mathacademy/capture' / account / task
        content = json.loads((directory/'content.json').read_text())
        for bucket in ['questions','canonical_examples']:
            for original in content.get(bucket,[]):
                if ERROR not in original.get('errors',[]): continue
                repaired = copy.deepcopy(original)
                sources, fresh = [], []
                for key in ['html_path','solution_evidence']:
                    if not original.get(key): continue
                    path = pathlib.Path(original[key]); html = path.read_text()
                    page.set_content(html)
                    item = page.locator('body > *').first.evaluate(EXTRACT, {'history_grade':original.get('result')})
                    fresh.append(item)
                    sources.append({'part':key, 'file':str(path), 'sha256':hashlib.sha256(html.encode()).hexdigest()})
                    if key == 'html_path':
                        repaired['problem'] = item['problem']
                        if item.get('worked_solution'):repaired['worked_solution'] = item['worked_solution']
                    else:
                        repaired['worked_solution'] = item['worked_solution']
                errors = list(dict.fromkeys(e for item in fresh for e in item.get('errors',[])))
                assets = sum(len(item.get('assets',[])) for item in fresh)
                supported = bool(fresh) and not errors and not assets and bool(repaired.get('worked_solution'))
                if supported:
                    repaired['errors'] = [e for e in original['errors'] if e != ERROR]
                    repaired['extraction_error_parts'].pop(ERROR,None)
                    repaired.setdefault('extraction_error_history',[]).append({'errors':[ERROR], 'resolution':'Re-extracted archived HTML with support for fixed phantom operators', 'sources':sources, 'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest()})
                    try:authoritative_question(repaired,example=bucket=='canonical_examples')
                    except Exception as error:supported=False;errors.append(str(error))
                report.append({'account':account,'task_id':task,'bucket':bucket,'question_id':original['math_academy_id'], 'supported':supported,'fresh_errors':errors,'assets':assets,'sources':sources,'before':original,'after':repaired if supported else None})
                print(account,task,original['math_academy_id'],'supported',supported,'errors',errors,'assets',assets,flush=True)
    browser.close()
atomic_json(ROOT/'reference/mathacademy/repairs/fixed-phantom-operators/plan.json',report)
