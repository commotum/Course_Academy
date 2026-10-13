"""Compare an extractor candidate against frozen reviewed owning archive roots."""
from pathlib import Path
import argparse, hashlib, json
from playwright.sync_api import sync_playwright
from scripts.storage import read_json, atomic_json

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--candidate', type=Path, required=True)
parser.add_argument('--tag', default='decorated-phantom')
args=parser.parse_args()
baseline=(ROOT/'literal-brace-final-extract-frozen.js').read_text()
candidate=args.candidate.read_text()
digest=lambda value: hashlib.sha256(value.encode() if isinstance(value,str) else value).hexdigest()
latest={}
for path in ROOT.glob('later-source-review-literal-braces*.json'):
    for row in read_json(path,[]):
        key=(row['account'],row['task_id'])
        if row.get('completed_at',0)>latest.get(key,{}).get('completed_at',0):latest[key]=row
sources=[]
for row in read_json(ROOT/'literal-brace-final-apply-candidates.json'):
    task=Path(row['directory']).parents[1].name
    stage=latest[(row['account'],task)]
    content=read_json(Path(stage['repair'])/'content.json')
    for bucket in ['questions','canonical_examples']:
        for record in content.get(bucket,[]):
            path=record.get('html_path')
            if path:
                sources.append({'account':row['account'],'task_id':task,'id':record['math_academy_id'],
                                'kind':'own_source','path':path,'dom_id':record.get('dom_id'),
                                'options':{'history_grade':record.get('grade') or record.get('result')}})
            external=record.get('solution_evidence')
            if isinstance(external,str) and Path(external).suffix=='.html' and Path(external).is_file():
                sources.append({'account':row['account'],'task_id':task,'id':record['math_academy_id'],
                                'kind':'own_external_solution','path':external,
                                'dom_id':'questionExplanation-'+record['math_academy_id'].removeprefix('q-'), 'options':{}})
results=[];seen=set()
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
    for source in sources:
        key=(source['path'],source['dom_id'],json.dumps(source['options'],sort_keys=True))
        if key in seen:continue
        seen.add(key);result={**source}
        try:
            markup=Path(source['path']).read_bytes();result['source_html_sha256']=digest(markup)
            page.set_content(markup.decode())
            node=page.locator('[id='+json.dumps(source['dom_id'])+']') if source['dom_id'] else page.locator('body')
            if node.count()!=1:raise ValueError('No unique owning source root')
            old=node.evaluate(baseline,source['options']);new=node.evaluate(candidate,source['options'])
            result.update(equivalent=old==new, baseline_output_sha256=digest(json.dumps(old,sort_keys=True)),
                          candidate_output_sha256=digest(json.dumps(new,sort_keys=True)))
            if old!=new:
                result.update(changed_keys=[k for k in set(old)|set(new) if old.get(k)!=new.get(k)],before=old,after=new)
        except Exception as error:result.update(equivalent=False,error=str(error))
        results.append(result)
    browser.close()
output={'baseline_extractor_sha256':digest(baseline),'candidate_extractor_sha256':digest(candidate),
        'candidate_file':str(args.candidate),'captures':len(latest),'roots':len(results),
        'all_equivalent':all(v['equivalent'] for v in results),'records':results,
        'review_reuse':'Exact full output equality; frozen reviewed source generation remains attributed separately',
        'network':'All browser network requests aborted; no completed packages/outboxes or database mutated'}
atomic_json(ROOT/(args.tag+'-archive-extractor-equivalence.json'),output)
print(json.dumps({'roots':len(results),'all_equivalent':output['all_equivalent'],
                  'failures':[{k:v for k,v in r.items() if k not in ('before','after')} for r in results if not r['equivalent']]}))
