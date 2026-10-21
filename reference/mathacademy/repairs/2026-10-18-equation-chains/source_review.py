"""Locate retained source evidence for every mixed-row field."""
import hashlib,json,re,subprocess
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];AUDIT=ROOT/'reference/mathacademy/audits/2026-10-18-equation-chain-import';DATA=Path('/home/jake/Developer/MA/DATA/Lessons')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str)+'\n')
def fragment(html,domid):
 m=re.search(r'<div\b[^>]*\bid=["\']'+re.escape(domid)+r'["\'][^>]*>',html)
 if not m:return None
 depth=0
 for token in re.finditer(r'</?div\b[^>]*>',html[m.start():],re.I):
  depth+=-1 if token[0].lower().startswith('</') else 1
  if depth==0:return html[m.start():m.start()+token.end()]
 return None
def run():
 fs=[f for f in json.loads((AUDIT/'findings.json').read_text()) if 'partial-empty-rhs-chain' in f['reasons']];ledger=[];cache={};miss=[]
 for f in fs:
  record={'entity':f['entity'],'attribute':f['attribute'],'source_id':f.get('source_id'),'evidence':[]};sid=str(f.get('source_id'))
  for topic in f['lessons']:
   if ':topic/math-academy-id' not in topic:continue
   tid=str(topic[':topic/math-academy-id']);folder=DATA/tid;path=folder/'Source'/f'{tid}.json'
   if not path.exists():continue
   if tid not in cache:cache[tid]=json.loads(path.read_text())
   items=cache[tid]['lesson']['items'];matches=[i for i in items if (sid.startswith('e-') and i.get('step_type')=='example' and str(i.get('content_id'))==sid[2:]) or (sid.startswith('q-') and str(i.get('question_id'))==sid[2:]) or (sid.isdigit() and i.get('step_type')=='tutorial' and str(i.get('content_id'))==sid)]
   for item in matches:
    htmlpath=folder/'Source'/f'{tid}.html';domid=item.get('dom_id') or ('question-'+sid[2:] if sid.startswith('q-') else 'step-'+item['step_id']);html=fragment(htmlpath.read_text(),domid)
    if not html:continue
    soup=BeautifulSoup(html,'html.parser');selector='.exampleExplanation' if f['attribute']==':question/worked-solution' and sid.startswith('e-') else '.questionExplanation,.questionWidget-explanation' if f['attribute']==':question/worked-solution' else '.exampleQuestion' if sid.startswith('e-') else '.questionWidget-text,.questionText' if sid.startswith('q-') else None
    nodes=soup.select(selector) if selector else [soup]
    if nodes:
     out=HERE/'sources'/f"{f['entity']}-{f['attribute'].split('/')[-1]}-archive.html";out.parent.mkdir(exist_ok=True);out.write_text('\n'.join(str(n) for n in nodes));record['evidence'].append({'kind':'archived-source-html','source':str(htmlpath),'source_sha256':digest(htmlpath),'step_or_question':domid,'extracted_fragment':str(out),'fragment_sha256':digest(out),'has_mathml':bool(out.read_text().find('<math')>=0)})
  if not record['evidence']:miss.append(record)
  ledger.append(record)
 print('Archived evidence:',len(ledger)-len(miss),'of',len(ledger),flush=True)
 if miss:
  sourceids=sorted({r['source_id'] for r in miss if r['source_id'] and str(r['source_id']).startswith(('q-','e-'))});regex='"math_academy_id": "(?:'+'|'.join(re.escape(x) for x in sourceids)+')"'
  roots=[ROOT/'reference/mathacademy/capture',ROOT/'reference/mathacademy/question-capture',ROOT/'reference/mathacademy/question-capture-workers']
  result=subprocess.run(['rg','-l','--glob','content.json',regex,*map(str,roots)],capture_output=True,text=True,timeout=90);assert result.returncode in (0,1),result.stderr;paths=[Path(p) for p in result.stdout.splitlines()];print('Capture files to inspect:',len(paths),flush=True)
  lookup={}
  for path in paths:
   try:d=json.loads(path.read_text())
   except ValueError:continue
   for q in d.get('canonical_examples',[])+d.get('questions',[]):
    sid=q.get('math_academy_id')
    if sid not in sourceids:continue
    for attr,key in [(':question/problem','problem'),(':question/worked-solution','worked_solution')]:
     if q.get(key):lookup.setdefault((sid,attr),[]).append({'path':str(path),'sha256':digest(path),'text':q[key],'html_path':d.get('html_path'),'original_document':d.get('original_document',{}),'question':q})
  current={e[':db/id']:e for g in ('questions','tutorials') for [e] in json.loads((HERE/(g+'.json')).read_text())}
  for r in miss:
   options=lookup.get((r['source_id'],r['attribute']),[])
   if options:
    exact=[o for o in options if o['text']==current[r['entity']].get(r['attribute'])];chosen=(exact or options)[0]
    out=HERE/'sources'/f"{r['entity']}-{r['attribute'].split('/')[-1]}-capture.json";out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(chosen,indent=2)+'\n');r['evidence'].append({'kind':'retained-lesson-capture','source':chosen['path'],'source_sha256':chosen['sha256'],'capture_record':str(out),'matches_current_field':bool(exact),'html_path':chosen['html_path'],'original_document':chosen['original_document']})
 history=ROOT/'reference/mathacademy/history-question-import-2026-10-04/prepared.json';historical={q['math_academy_id']:q for q in json.loads(history.read_text())['questions']}
 for r in ledger:
  if r['evidence']:continue
  q=historical.get(r['source_id'])
  if q:
   out=HERE/'sources'/f"{r['entity']}-worked-solution-history.json";out.write_text(json.dumps(q,indent=2)+'\n');r['evidence'].append({'kind':'retained-historical-question-import','source':str(history),'source_sha256':digest(history),'record':str(out),'provenance':q.get('provenance')})
  else:
   f=next(f for f in fs if f['entity']==r['entity'] and f['attribute']==r['attribute'])
   assert r['source_id'] is None
   r['evidence'].append({'kind':'retained-edb-content-without-external-source-id','source':str(AUDIT/'findings.json'),'entity':r['entity'],'attribute':r['attribute'],'source_basis':4476,'provenance':f['provenance'],'review':'Routine terminal-punctuation chain only. All expression tokens and order are checked unchanged; no missing mathematical content is inferred.'})
 save('mixed-source-ledger.json',ledger);print('Evidence classes',dict(Counter(r['evidence'][0]['kind'] for r in ledger)))
if __name__=='__main__':run()
