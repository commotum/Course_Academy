"""Render the lesson tutorials, canonical examples, and repaired practice prompts without database writes."""
import argparse
import copy
from collections import Counter
import functools
import hashlib
import http.server
import json
import re
from bs4 import BeautifulSoup
from pathlib import Path
import threading
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'ui/Learning.html').exists())
parser = argparse.ArgumentParser()
parser.add_argument('--lesson', type=Path, required=True)
parser.add_argument('--changes', type=Path)
parser.add_argument('--baseline', type=str, default='', help='Comma-separated diagnostic entity IDs')
parser.add_argument('--output', type=Path)
parser.add_argument('--reuse', type=Path, help='Prior rendering.json; reuse only identical entity content')
parser.add_argument('--generators', type=Path, help='Fresh generator output records for independent layout checks')
args = parser.parse_args()
OUT = (args.output or args.lesson.parent/'ui').resolve()
OUT.mkdir(parents=True, exist_ok=True)
lesson = json.loads(args.lesson.read_text())
changes_bytes = (args.changes or args.lesson.parent/'changes.json').read_bytes()
baseline_ids={int(e) for e in args.baseline.split(',') if e}
changes_sha256 = hashlib.sha256(changes_bytes).hexdigest()
changes = json.loads(changes_bytes)
if isinstance(changes, dict):
    changes = changes['changes']
answer_changes=[c for c in changes if c['attribute']==':answer/value']
content_changes=[c for c in changes if c['attribute']!=':answer/value']
answer_questions={c['question'] for c in answer_changes}
by_entity = {}
for change in content_changes:
    by_entity.setdefault(change['entity'], []).append(change)
entities = {}
for kp in lesson['topic'][':topic/knowledge-points']:
    for question in [kp[':knowledge-point/canonical-example']] + [q for q in kp[':knowledge-point/questions'] if q[':db/id'] in by_entity or q[':db/id'] in answer_questions]:
        entities[question[':db/id']] = question
for step in lesson['topic'][':activity/_scope'][0][':activity/steps']:
    item = step[':step/content']
    if ':tutorial/content' in item:
        entities[item[':db/id']] = item
for change in content_changes:
    assert entities[change['entity']][change['attribute']] == change['before']

def overlay_answers(value, version):
    if isinstance(value,dict):
        for change in answer_changes:
            if value.get(':db/id')==change['entity'] and change['attribute'] in value:
                assert value[change['attribute']]==change['before']
                value[change['attribute']]=change[version]
        for item in value.values():overlay_answers(item,version)
    elif isinstance(value,list):
        for item in value:overlay_answers(item,version)

snapshot_entities=copy.deepcopy(entities)


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
    return {'activityId': str(index), 'title': 'Matrix-vector content review', 'type': 'lesson',
            'steps': [step], 'courseId': 'review', 'learner': {'id': 1, 'name': 'Offline review'}}


records = []
for eid, original in sorted(entities.items()):
    versions = ['before', 'after'] if eid in baseline_ids else ['after']
    for version in versions:
        entity = copy.deepcopy(original)
        for change in by_entity.get(eid, []):
            entity[change['attribute']] = change[version]
        overlay_answers(entity,version)
        records.append({'entity': eid, 'version': version,
                        'kind': 'tutorial' if ':tutorial/content' in entity else 'question',
                        'changed': eid in by_entity or eid in answer_questions,
                        'activity': make_activity(entity, len(records))})
generated=[]
if args.generators:
    generated=json.loads(args.generators.read_text())
    for index,record in enumerate(generated):
        entity=copy.deepcopy(record['question']);entity[':db/id']=f'generated-{index+1}'
        records.append({'entity':entity[':db/id'],'version':'after','kind':'generated','changed':False,
                        'activity':make_activity(entity,len(records))})

reuse = {(r['entity'],r['version'],r['viewport'],r.get('theme','light')):r for r in json.loads(args.reuse.read_text())} if args.reuse else {}


def can_reuse(record, viewport, theme):
    prior=reuse.get((record['entity'],record['version'],viewport,theme))
    return prior and prior['source_sha256']==hashlib.sha256(json.dumps(record['activity']['steps'],sort_keys=True).encode()).hexdigest()


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
 const tables=[]; const math=[];
 for (const item of MathJax.startup.document.math) {
     math.push({tex:item.math, display:item.display, text:item.typesetRoot?.textContent||null});
     item.root.walkTree(n=>{if(n.kind==='mtable')tables.push({tex:item.math,display:item.display,rows:n.childNodes.length,columns:n.childNodes[0]?.childNodes.length});});
 }
 const plain=root.cloneNode(true);plain.querySelectorAll('mjx-container,pre,code').forEach(n=>n.remove());
 return {
   math,tables,display,mathCount:root.querySelectorAll('mjx-container').length,
   errors:[...root.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error,[data-mjx-error]')].map(n=>n.textContent),
   residualTex:/\$|\\(?:begin|end|left|right|text|frac)\b/.test(plain.textContent),
   bodyOverflow:document.body.scrollWidth>window.innerWidth+2,
   contentOverflow:root.scrollWidth>root.clientWidth+2,
   images:[...root.querySelectorAll('img')].map(n=>({src:n.getAttribute('src'),loaded:n.complete&&n.naturalWidth>0,...rect(n)})),
   answerMatrices:[...root.querySelectorAll('.matrix-answer')].map(n=>({rows:[...n.querySelectorAll('tr')].map(row=>[...row.querySelectorAll('td')].map(cell=>[...cell.querySelectorAll('[data-field-key]')].map(slot=>({key:slot.dataset.fieldKey,fieldIds:[...slot.querySelectorAll('[data-field-id]')].map(f=>f.dataset.fieldId),inputCount:slot.querySelectorAll('input,math-field,textarea,select').length}))))})),
   controls:[...root.querySelectorAll('select,input,textarea,math-field')].map(n=>({tag:n.tagName,type:n.type||'',name:n.name||'',choiceId:['radio','hidden'].includes(n.type)?n.value:null,checked:n.type==='checkbox'?n.checked:null,disabled:n.disabled||false,
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
        for viewport, width, height, theme in [('desktop', 1280, 1000, 'light'), ('mobile', 390, 844, 'light'), ('desktop', 1280, 1000, 'dark'), ('mobile', 390, 844, 'dark')]:
            page = browser.new_page(viewport={'width': width, 'height': height})
            page.add_init_script(f"localStorage.setItem('course-academy.theme', '{theme}')")
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(origin + '/') else route.abort())
            for index, record in enumerate(records):
                if theme=='dark' and not (record['kind']=='tutorial' and record['changed'] and any(c in record['activity']['steps'][0].get('markdown','') for c in ['\\color','\\bbox'])): continue
                source_sha256=hashlib.sha256(json.dumps(record['activity']['steps'],sort_keys=True).encode()).hexdigest()
                if can_reuse(record,viewport,theme):
                    result=copy.deepcopy(reuse[record['entity'],record['version'],viewport,theme])
                    result['changed']=record['changed'];result['theme']=theme;result['source_sha256']=source_sha256;result['reused_equivalent_source']=True
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
                step=record['activity']['steps'][0]
                result.update({key: record[key] for key in ['entity', 'version', 'kind', 'changed']})
                result.update({'viewport': viewport, 'theme': theme, 'javascriptErrors': errors[:], 'source_sha256':source_sha256,'reused_equivalent_source':False})
                if True:
                    stem = OUT / f'{record["entity"]}-{record["version"]}-{viewport}-{theme}'
                    page.screenshot(path=str(stem) + '.png', full_page=True, animations='disabled')
                    Path(str(stem) + '.html').write_text(page.content())
                    result['screenshot'] = str(stem.relative_to(ROOT)) + '.png'
                if record['version']=='after':
                    result['scroll_checks']=page.locator('.lesson-content').evaluate('''root => [...root.querySelectorAll('mjx-container[display="true"]')].filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>{const max=n.scrollWidth-n.clientWidth;n.scrollLeft=max;return {max,actual:n.scrollLeft,overflow:getComputedStyle(n).overflowX,passed:Math.abs(n.scrollLeft-max)<=1&&['auto','scroll'].includes(getComputedStyle(n).overflowX)};})''')
                    if result['scroll_checks']:
                        page.screenshot(path=str(stem)+'-scrolled-right.png',full_page=True,animations='disabled')
                        result['scroll_screenshot']=str(stem.relative_to(ROOT))+'-scrolled-right.png'

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
                    interaction={'tag':tag,'type':kind,'name':control.get_attribute('name'),'changed':ok}
                    if kind=='checkbox':
                        interaction['encodedValue']=control.locator('xpath=ancestor::label[1]').locator('input[type=hidden]').input_value()
                    interactions.append(interaction)
                result['interactions']=interactions
                results.append(result)
                if (index+1)%10==0:print(f'Rendered {index+1}/{len(records)} {viewport}',flush=True)
            page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()

(OUT/'rendering-capture.json').write_text(json.dumps(results,indent=2)+'\n')

def checkbox_encoding_exact(field, result):
    yes=next(choice['id'] for choice in field['choices'] if choice['value']=='true')
    no=next(choice['id'] for choice in field['choices'] if choice['value']=='false')
    controls=[control for control in result['controls'] if control['name']==field['id']]
    initial=any(control['type']=='hidden' and control['choiceId']==no for control in controls)
    initial=initial and sum(control['type']=='checkbox' and control['checked'] is False for control in controls)==1
    selected=any(interaction.get('name')==field['id'] and interaction.get('encodedValue')==yes and interaction['changed'] for interaction in result['interactions'])
    return initial and selected


# Validate captured DOM against the UI's complete preview sequence. Correct values
# are rendered between the prompt and worked solution by previewContent(). EDB's
# cardinality-many answer-fields collection is unordered; vector rows are keyed.
for result in results:
    record=next(r for r in records if r['entity']==result['entity'] and r['version']==result['version'])
    step=record['activity']['steps'][0]
    parse_math=lambda text:[next(part for part in match if part) for match in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$',text)]
    expected_math=parse_math(step.get('markdown','')+step.get('problem',''))
    for field in step.get('fields',[]):
        if field['type']=='checkbox':expected_math+=parse_math(field['key'])
        if field['type'] in ['radio','select']:
            for choice in field.get('choices',[]):
                expected_math.extend([choice['value']] if choice['type']=='math' else parse_math(choice['value']))
    for field in step.get('fields',[]):
        answer=field.get('correctAnswer')
        if answer:expected_math.extend([answer['value']] if answer['type']=='math' else parse_math(answer['value']))
    expected_math+=parse_math(step.get('solution',''))
    normalize=lambda text:re.sub(r'\s+','',text)
    result['input_math_count']=len(expected_math)
    result['all_input_math_rendered']=Counter(map(normalize,expected_math))==Counter(normalize(m['tex']) for m in result['math'])
    result['input_table_count']=sum(len(re.findall(r'\\begin\{(?:[bBpPvV]?matrix|smallmatrix|aligned|alignedat|array|cases|gathered|split)\}',tex)) for tex in expected_math)
    result['all_input_tables_rendered']=result['input_table_count']==len(result['tables'])
    matrices=result['answerMatrices']
    expected_matrices=BeautifulSoup(step.get('problem',''),'html.parser').select('.matrix-answer')
    fields={f['key']:f for f in step.get('fields',[])}
    expected_rows=[[[re.findall(r'\{\{(?:answer-field:)?([^}]+)\}\}',cell.get_text()) for cell in row.select(':scope > td')] for row in matrix.select('tr')] for matrix in expected_matrices]
    actual_rows=[[[[slot['key'] for slot in cell] for cell in row] for row in matrix['rows']] for matrix in matrices]
    slots=[slot for matrix in matrices for row in matrix['rows'] for cell in row for slot in cell]
    result['matrix_fields_exact']=expected_rows==actual_rows and all(slot['key'] in fields and slot['fieldIds']==[fields[slot['key']]['id']] and slot['inputCount']==1 for slot in slots)
    result['expected_matrix_shape']=expected_rows
    result['answer_choice_ids_exact']=all(sorted(c['choiceId'] for c in result['controls'] if c['name']==field['id'] and c['type']=='radio')==sorted(choice['id'] for choice in field['choices']) for field in fields.values() if field['type']=='radio')
    result['checkbox_encodings_exact']=all(checkbox_encoding_exact(field,result) for field in fields.values() if field['type']=='checkbox')
    result['all_fields_mounted']=all(sum(control['name']==field['id'] for control in result['controls'])==1 for field in fields.values() if field['type'] in ['blank','free','select'])
    result['passed']=not any([result['javascriptErrors'],result['errors'],result['residualTex'],result['bodyOverflow'],result['contentOverflow'],any(not i['loaded'] for i in result['images']),any(d['clipped'] for d in result['display']),result['fonts']!='loaded',any(not i['changed'] for i in result['interactions']),not result['all_input_math_rendered'],not result['all_input_tables_rendered'],not result['matrix_fields_exact'],not result['all_fields_mounted'],not result['answer_choice_ids_exact'],not result['checkbox_encodings_exact'],any(not c['passed'] for c in result.get('scroll_checks',[]))])

comparisons=[]
for eid in by_entity:
    for viewport in ['desktop','mobile']:
        for theme in ['light','dark']:
            pair=[r for r in results if r['entity']==eid and r['viewport']==viewport and r['theme']==theme]
            if len(pair)!=2: continue
            before,after=pair
            comparisons.append({'entity':eid,'viewport':viewport,'theme':theme,'controls_identical':before['controls']==after['controls']})
summary={
    'passed':all(r['passed'] for r in results if r['version']=='after') and all(r['controls_identical'] for r in comparisons),
    'changes_sha256':changes_sha256,
    'database_writes':0,'canonical_example_count':len(lesson['topic'][':topic/knowledge-points']),'practice_question_count':sum(':question/problem' in e and not e.get(':knowledge-point/_canonical-example') for e in entities.values()),'question_count':sum(':question/problem' in e for e in entities.values()),
    'tutorial_count':sum(':tutorial/content' in e for e in entities.values()),'changed_fields':len(changes),'content_changed_fields':len(content_changes),'answer_changed_fields':len(answer_changes),
    'generated_examples':len(generated),'snapshot_basis':lesson['identity']['basis'],
    'themes':sorted({r['theme'] for r in results}),'rendered_entity_viewports':len(results),'reused_equivalent_source_cases':sum(r.get('reused_equivalent_source',False) for r in results),'renderer':'Unmodified current Learning.html, learning.js, question-fields.js and MathJax',
    'control_comparisons':comparisons,'failures':[{k:r[k] for k in ['entity','version','viewport','theme','errors','residualTex','bodyOverflow','contentOverflow','javascriptErrors','all_input_math_rendered','all_input_tables_rendered','matrix_fields_exact','all_fields_mounted','answer_choice_ids_exact','checkbox_encodings_exact']} for r in results if not r['passed']],
    'scrollable_display_equations':[{'entity':r['entity'],'version':r['version'],'viewport':r['viewport'],'theme':r['theme'],'count':sum(d['scrollWidth']>d['clientWidth']+2 for d in r['display'])} for r in results if r['version']=='after' and any(d['scrollWidth']>d['clientWidth']+2 for d in r['display'])],
    'scroll_checks':[{'entity':r['entity'],'viewport':r['viewport'],'theme':r['theme'],'checks':r['scroll_checks']} for r in results if 'scroll_checks' in r],
    'ui_hashes':{name:hashlib.sha256((ROOT/'ui'/name).read_bytes()).hexdigest() for name in ['Learning.html','learning.js','question-fields.js','mathjax-config.js','learning.css']}}
(OUT/'rendering.json').write_text(json.dumps(results,indent=2)+'\n')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(OUT/'tested-changes.json').write_bytes(changes_bytes)
print(json.dumps(summary,indent=2))
assert summary['passed']
