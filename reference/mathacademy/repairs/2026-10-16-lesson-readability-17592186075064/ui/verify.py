"""Render this complete lesson through the current player, without database writes."""
import argparse
import copy
import functools
import hashlib
import http.server
import json
from pathlib import Path
import threading
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
parser = argparse.ArgumentParser()
parser.add_argument('--changes', type=Path, default=HERE.parent / 'changes.json')
parser.add_argument('--output', type=Path, default=HERE)
parser.add_argument('--reuse', type=Path, help='Prior rendering.json; reuse only identical entity content')
parser.add_argument('--previous-changes', type=Path, help='Exact changes used in prior rendering')
parser.add_argument('--generators', type=Path, help='Fresh generator output records for independent layout checks')
args = parser.parse_args()
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
lesson = json.loads((HERE.parent / 'lesson.json').read_text())
changes_bytes = args.changes.read_bytes()
changes_sha256 = hashlib.sha256(changes_bytes).hexdigest()
changes = json.loads(changes_bytes)
if isinstance(changes, dict):
    changes = changes['changes']
by_entity = {}
for change in changes:
    by_entity.setdefault(change['entity'], []).append(change)
entities = {}
for kp in lesson['topic'][':topic/knowledge-points']:
    for question in kp[':knowledge-point/questions'] + [kp[':knowledge-point/canonical-example']]:
        entities[question[':db/id']] = question
for step in lesson['activity'][':activity/steps']:
    item = step[':step/content']
    if ':tutorial/content' in item:
        entities[item[':db/id']] = item
for change in changes:
    assert entities[change['entity']][change['attribute']] == change['before']
snapshot_entities=copy.deepcopy(entities)
seed_repair=HERE.parent.parent/'2026-10-16-line-definitions-17592186561226'
seed_verification=json.loads((seed_repair/'verification.json').read_text())
assert seed_verification['committed'] and seed_verification['exact_readback']
seed_change=json.loads((seed_repair/'change.json').read_text())
entities[seed_change['entity']][seed_change['attribute']]=seed_change['after']


def enum(value):
    return str(value.get(':db/ident') if isinstance(value, dict) else value).split('/')[-1]


def make_activity(entity, index):
    if ':tutorial/content' in entity:
        step = {'kind': 'tutorial', 'contentId': entity[':db/id'],
                'title': entity.get(':tutorial/title', ''), 'markdown': entity[':tutorial/content'], 'fields': []}
    else:
        fields = []
        for field in entity.get(':question/answer-fields', []):
            choices = [{'id': choice[':answer/id'], 'type': enum(choice[':answer/type']),
                        'value': choice[':answer/value'], 'feedback': choice.get(':answer/feedback', '')}
                       for choice in field.get(':answer-field/choices', [])]
            item = {'id': field[':answer-field/id'], 'key': field[':answer-field/key'],
                    'type': enum(field[':answer-field/type']), 'choices': choices}
            correct = field.get(':answer-field/correct')
            if correct:
                if isinstance(correct,list):
                    correct=next(c for c in field[':answer-field/choices'] if c[':answer/id']==correct[1])
                item['correctAnswer'] = {'id': correct[':answer/id'], 'type': enum(correct[':answer/type']),
                                         'value': correct[':answer/value']}
                item['answerType'] = enum(correct[':answer/type'])
            fields.append(item)
        step = {'kind': 'question', 'contentId': entity[':db/id'], 'status': 'started',
                'problem': entity[':question/problem'], 'solution': entity.get(':question/worked-solution', ''), 'fields': fields}
    return {'activityId': str(index), 'title': 'Lesson readability review', 'type': 'lesson',
            'steps': [step], 'courseId': 'review', 'learner': {'id': 1, 'name': 'Offline review'}}


records = []
for eid, original in sorted(entities.items()):
    versions = ['before', 'after'] if eid in by_entity or ':tutorial/content' in original else ['after']
    for version in versions:
        entity = copy.deepcopy(original)
        for change in by_entity.get(eid, []):
            entity[change['attribute']] = change[version]
        records.append({'entity': eid, 'version': version,
                        'kind': 'tutorial' if ':tutorial/content' in entity else 'question',
                        'changed': eid in by_entity,
                        'activity': make_activity(entity, len(records))})
generated=[]
if args.generators:
    generated=json.loads(args.generators.read_text())
    for index,record in enumerate(generated):
        entity=copy.deepcopy(record['question']);entity[':db/id']=f'generated-{index+1}'
        records.append({'entity':entity[':db/id'],'version':'after','kind':'generated','changed':False,
                        'activity':make_activity(entity,len(records))})

reuse = {}
previous = {}
if args.reuse:
    assert args.previous_changes
    reuse = {(r['entity'],r['version'],r['viewport']):r for r in json.loads(args.reuse.read_text())}
    for change in json.loads(args.previous_changes.read_text()):
        previous.setdefault(change['entity'],[]).append(change)


def can_reuse(record, viewport):
    if (record['entity'],record['version'],viewport) not in reuse:return False
    before=copy.deepcopy(snapshot_entities[record['entity']])
    for change in previous.get(record['entity'],[]):before[change['attribute']]=change[record['version']]
    return make_activity(before,0)['steps']==record['activity']['steps']


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        data = None
        if parsed.path == '/api/developer-mode':
            data = {'enabled': True}
        elif parsed.path == '/api/preview':
            data = records[int(parse_qs(parsed.query)['activityId'][0])]['activity']
        if data is not None:
            body = json.dumps(data).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def translate_path(self, path):
        parsed = urlparse(path)
        if parsed.path == '/learn':
            return str(ROOT / 'ui/Learning.html')
        if parsed.path == '/api/asset':
            return str(Path('/media/jake/SSD/EDB/math') / parse_qs(parsed.query)['path'][0])
        return super().translate_path(path)

    def do_POST(self):
        self.send_error(405, 'Read-only local render fixture')


STATE = r'''root => {
 const rect = n => {const r=n.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width,height:r.height};};
 const display=[...root.querySelectorAll('mjx-container[display="true"]')].map(n=>({
     ...rect(n),clientWidth:n.clientWidth,scrollWidth:n.scrollWidth,overflow:getComputedStyle(n).overflowX,
     contentWidth:n.querySelector('svg')?.getBoundingClientRect().width||0,
     clipped:n.scrollWidth>n.clientWidth+2&&!['auto','scroll'].includes(getComputedStyle(n).overflowX)
 }));
 const tables=[];
 for (const item of MathJax.startup.document.math) {
     item.root.walkTree(n=>{if(n.kind==='mtable')tables.push({tex:item.math,display:item.display,rows:n.childNodes.length,columns:n.childNodes[0]?.childNodes.length});});
 }
 const plain=root.cloneNode(true);plain.querySelectorAll('mjx-container,pre,code').forEach(n=>n.remove());
 return {
   tables,display,mathCount:root.querySelectorAll('mjx-container').length,
   errors:[...root.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error,[data-mjx-error]')].map(n=>n.textContent),
   residualTex:/\$|\\(?:begin|end|left|right|text|frac)\b/.test(plain.textContent),
   bodyOverflow:document.body.scrollWidth>window.innerWidth+2,
   contentOverflow:root.scrollWidth>root.clientWidth+2,
   images:[...root.querySelectorAll('img')].map(n=>({src:n.getAttribute('src'),loaded:n.complete&&n.naturalWidth>0,...rect(n)})),
   controls:[...root.querySelectorAll('select,input,textarea,math-field')].map(n=>({tag:n.tagName,type:n.type||'',name:n.name||'',disabled:n.disabled||false,
     options:n.tagName==='SELECT'?[...n.options].map(o=>({value:o.value,text:o.textContent,disabled:o.disabled})):null})),
   orderedLists:[...root.querySelectorAll('ol')].map(n=>({start:n.start,items:n.querySelectorAll(':scope>li').length})),
   paragraphCount:root.querySelectorAll('.prose p').length,
   fonts:document.fonts.status
 };
}'''

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
results = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
        for viewport, width, height in [('desktop', 1280, 1000), ('mobile', 390, 844)]:
            page = browser.new_page(viewport={'width': width, 'height': height})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(origin + '/') else route.abort())
            for index, record in enumerate(records):
                source_sha256=hashlib.sha256(json.dumps(record['activity']['steps'],sort_keys=True).encode()).hexdigest()
                if can_reuse(record,viewport):
                    result=copy.deepcopy(reuse[record['entity'],record['version'],viewport])
                    result['changed']=record['changed'];result['source_sha256']=source_sha256;result['reused_equivalent_source']=True
                    results.append(result)
                    continue
                errors.clear()
                page.goto(origin + f'/learn?activityId={index}', wait_until='domcontentloaded')
                page.locator('.lesson-content').wait_for()
                page.wait_for_function("typeof window.MathJax?.typesetPromise === 'function'")
                page.evaluate('''async () => {
                    for (const d of document.querySelectorAll('details.worked-solution')) d.open=true;
                    for (const image of document.images) image.loading='eager';
                    await MathJax.startup.promise;
                    await MathJax.typesetPromise();
                    await document.fonts.ready;
                    await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));
                    await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
                }''')
                result = page.locator('.lesson-content').evaluate(STATE)
                result.update({key: record[key] for key in ['entity', 'version', 'kind', 'changed']})
                result.update({'viewport': viewport, 'javascriptErrors': errors[:], 'source_sha256':source_sha256,'reused_equivalent_source':False})
                if record['kind'] in ['tutorial','generated'] or record['entity'] in [17592186073480, 17592186074060, 17592186073481, 17592186074057, 17592186542465, 17592186542491]:
                    stem = OUT / f'{record["entity"]}-{record["version"]}-{viewport}'
                    page.screenshot(path=str(stem) + '.png', full_page=True, animations='disabled')
                    Path(str(stem) + '.html').write_text(page.content())
                    result['screenshot'] = str(stem.relative_to(ROOT)) + '.png'
                interactions=[]
                for control in page.locator('.lesson-content select,.lesson-content input:not([type=hidden]),.lesson-content textarea,.lesson-content math-field').all():
                    if control.is_disabled():continue
                    tag=control.evaluate('n=>n.tagName');kind=control.get_attribute('type')
                    if tag=='SELECT':
                        value=control.locator('option:not([disabled])').last.get_attribute('value');control.select_option(value=value);ok=control.input_value()==value
                    elif kind in ['radio','checkbox']:
                        control.locator('xpath=ancestor::label[1]').click();ok=control.is_checked()
                    elif tag=='MATH-FIELD':
                        control.click();control.press('2');ok=control.evaluate("n=>n.value==='2'")
                    else:
                        control.fill('2');ok=control.input_value()=='2'
                    interactions.append({'tag':tag,'changed':ok})
                result['interactions']=interactions
                result['passed']=not any([errors,result['errors'],result['residualTex'],result['bodyOverflow'],result['contentOverflow'],
                     any(not i['loaded'] for i in result['images']),any(d['clipped'] for d in result['display']),result['fonts']!='loaded',
                     any(not i['changed'] for i in interactions)])
                results.append(result)
                if (index+1)%10==0:print(f'Rendered {index+1}/{len(records)} {viewport}',flush=True)
            page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()

comparisons=[]
for eid in by_entity:
    for viewport in ['desktop','mobile']:
        before,after=[r for r in results if r['entity']==eid and r['viewport']==viewport]
        comparisons.append({'entity':eid,'viewport':viewport,'controls_identical':before['controls']==after['controls']})
summary={
    'passed':all(r['passed'] for r in results if r['version']=='after') and all(r['controls_identical'] for r in comparisons),
    'changes_sha256':changes_sha256,
    'database_writes':0,'question_count':sum(':question/problem' in e for e in entities.values()),
    'tutorial_count':sum(':tutorial/content' in e for e in entities.values()),'changed_fields':len(changes),
    'generated_examples':len(generated),'snapshot_overlays':[{'entity':seed_change['entity'],'attribute':seed_change['attribute'],'basis_after':seed_verification['basis_after'],'source':str(seed_repair/'verification.json')}],
    'rendered_entity_viewports':len(results),'reused_equivalent_source_cases':sum(r.get('reused_equivalent_source',False) for r in results),'renderer':'Unmodified current Learning.html, learning.js, question-fields.js and MathJax',
    'control_comparisons':comparisons,'failures':[{k:r[k] for k in ['entity','version','viewport','errors','residualTex','bodyOverflow','contentOverflow','javascriptErrors']} for r in results if not r['passed']],
    'scrollable_display_equations':[{'entity':r['entity'],'version':r['version'],'viewport':r['viewport'],'count':sum(d['scrollWidth']>d['clientWidth']+2 for d in r['display'])} for r in results if r['version']=='after' and any(d['scrollWidth']>d['clientWidth']+2 for d in r['display'])],
    'ui_hashes':{name:hashlib.sha256((ROOT/'ui'/name).read_bytes()).hexdigest() for name in ['Learning.html','learning.js','question-fields.js','mathjax-config.js','learning.css']}}
(OUT/'rendering.json').write_text(json.dumps(results,indent=2)+'\n')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(OUT/'tested-changes.json').write_bytes(changes_bytes)
print(json.dumps(summary,indent=2))
assert summary['passed']
