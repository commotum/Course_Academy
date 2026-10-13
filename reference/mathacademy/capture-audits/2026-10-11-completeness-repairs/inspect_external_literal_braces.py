from pathlib import Path
import hashlib,json,re
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from scripts.browser.adapter import EXTRACT
from scripts.storage import read_json,atomic_json
R=Path(__file__).resolve().parent
OLD=EXTRACT.replace('literalFence(n.textContent)','n.textContent').replace("literalFence(n.getAttribute('open') || '(')","(n.getAttribute('open') || '(')").replace("literalFence(n.getAttribute('close') || ')')","(n.getAttribute('close') || ')')").replace("[')',']','}','\\\\}']","[')',']','}']")
rows=read_json(R/'later-source-candidates.json')+[{'directory':str(R.parents[1]/'capture/multivariable/14120884/repairs/source-candidates-v1')}]+read_json(R/'later-finite-additional-candidates.json');out=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
 for row in rows:
  d=Path(row['directory']).parents[1];c=read_json(d/'content.json')
  for bucket in ['questions','canonical_examples']:
   for q in c.get(bucket,[]):
    f=q.get('solution_evidence');p=Path(f) if isinstance(f,str) else None
    if not p or not p.is_file() or p.suffix!='.html':continue
    markup=p.read_text()
    if not re.search(r'<mo\b[^>]*>\s*[{}]\s*</mo>|<mfenced\b[^>]*(?:open|close)=["\'][{}]["\']',markup,re.I):continue
    r={'directory':str(d),'id':q['math_academy_id'],'bucket':bucket,'source_file':str(p),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    try:
     page.set_content(markup);node=page.locator('#questionExplanation-'+q['math_academy_id'].removeprefix('q-'))
     if node.count()!=1:raise ValueError('No unique original same-ID explanation root')
     old=node.evaluate(OLD);new=node.evaluate(EXTRACT)
     def boundtext(parsed):
      text=parsed['worked_solution']
      for a in parsed['assets']:
       url=urljoin(q.get('source_url') or 'https://mathacademy.com/',a.get('source_url') or '')
       matches=[a0 for a0 in q.get('assets',[]) if a0.get('path') and a0.get('tag')==a.get('tag') and (urljoin(q.get('source_url') or 'https://mathacademy.com/',a0.get('source_url') or '')==url if a.get('source_url') else a0.get('html')==a.get('html'))]
       bindings={(a0['path'],a0.get('sha256')) for a0 in matches}
       if len(bindings)!=1:raise ValueError('External solution asset has no unique original bytes binding')
       name,digest=next(iter(bindings));path=Path(name);assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest
       text=text.replace('@asset-'+str(a['index'])+'@',str(path))
      return text
     before,after=boundtext(old),boundtext(new);r.update(changed=before!=after,old_matches_saved=before==q.get('worked_solution'),old_errors=old['errors'],new_errors=new['errors'])
     if before!=after:r.update(before=before,after=after)
    except Exception as e:r['error']=str(e)
    out.append(r)
 browser.close()
atomic_json(R/'external-literal-brace-source-change-inventory.json',{'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(),'records':out})
print(json.dumps({'candidates':len(out),'changed':len([r for r in out if r.get('changed')]),'matching_old':len([r for r in out if r.get('changed') and r.get('old_matches_saved')]),'errors':[ {k:v for k,v in r.items() if k not in ('before','after')} for r in out if r.get('error') or not r.get('old_matches_saved')]}))
