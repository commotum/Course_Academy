import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0,'scripts');from import_historical_question_content import Renderer
from question_capture.math_format import MATH,normalize_source_tex,validate_math_structure
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};M=json.loads((H/'source-manifest.json').read_text());C=json.loads((H/'checkbox-labels-current.json').read_text());labels=C['labels'];cached={};reports=[];proposals=[];errors=[];sourcecache=[]
def canon(s,ignore_fonts=False):
 s=normalize_source_tex(s).replace('−','-').replace('∈',r'\in').replace('∞',r'\infty');s=re.sub(r'\\(?:displaystyle|,|;|!|quad|qquad|left|right)','',s)
 if ignore_fonts:s=re.sub(r'\\(?:mathbf|mathrm|mathbb|mathcal|mathit|textrm|text)','',s)
 return re.sub(r'[{}\s$]','',s).strip('.').lower()
def candidates(q):
 sid=q.get(':question/math-academy-id');paths=[p for p in M.get(sid,[])if p.endswith('.json')];out=[]
 if not paths:return []
 # Captures for the same immutable source identity have the same statement bank.
 # Keep one before/after raw DOM with complete fields, plus provenance.
 p=next((p for p in paths if p.endswith('-after.json')),paths[0]);d=json.loads(Path(p).read_text());soup=BeautifulSoup(d.get('html')or d.get('raw_html')or'','html.parser');rr=Renderer(None)
 for n in soup.select('.questionStatements > li'):
  value=re.sub(r'^-\s*','',rr.text(n));out.append({'value':value,'path':p,'role':'original listed statement','html':str(n)})
 for f in d.get('fields',[]):
  for choice in f.get('choices',[]):
   value=rr.text(BeautifulSoup(choice['html'],'html.parser'))if choice.get('html')else choice.get('value','');out.append({'value':value,'path':p,'role':'original answer choice','html':choice.get('html')})
 sourcecache.append({'question':q[':db/id'],'source_identity':sid,'path':p,'candidates':out,'renderer_errors':rr.errors});return out
for f in labels:
 q=Q[f['question']];sid=q.get(':question/math-academy-id');key=f['value']
 try:validate_math_structure(key)
 except Exception as ex:errors.append({'entity':f['entity'],'error':str(ex),'value':key})
 if f['question']not in cached:cached[f['question']]=candidates(q)
 ss=cached[f['question']];row={'entity':f['entity'],'question':f['question'],'source_identity':sid,'label':key,'basis_t':C['basis_t']}
 exact=[s for s in ss if canon(s['value'])==canon(key)]
 if exact:row.update({'status':'source statement/choice matches','evidence':exact[0]})
 elif key.lower()=='none of the above'and any(re.search(r'\bnone\b',s['value'],re.I)for s in ss):row.update({'status':'source none-choice equivalent','evidence':next(s for s in ss if re.search(r'\bnone\b',s['value'],re.I))})
 elif re.fullmatch(r'\$[A-Za-z]=[-+]?\d+\$',key):
  value=key[1:-1].split('=')[1];hits=[s for s in ss if re.search(r'\$\s*'+re.escape(value)+r'\s*\$',s['value'])]
  if hits:row.update({'status':'source numerical subset member matches','evidence':hits[0]})
  else:row['status']='original source absent'if sid and not ss else'generated label; no original source identity'if not sid else'source comparison needs review'
 elif ss:
  near=[s for s in ss if canon(s['value'],True)==canon(key,True)]
  candidates_by_after={s['value']:s for s in near if re.search(r'\\(?:mathbf|mathbb|mathcal|mathrm|mathit)',s['value'])}
  if len(candidates_by_after)==1:
   after,evidence=next(iter(candidates_by_after.items()));validate_math_structure(after);proposals.append({'entity':f['entity'],'attribute':'answer-field/key','before':key,'after':after,'reason':'Restore the original statement mathematical font role lost from the checkbox label.','evidence':{'path':evidence['path'],'question':q[':db/id'],'source_identity':sid,'source_statement':evidence['value']},'confidence':'high'});row.update({'status':'source-backed font repair proposed','evidence':evidence})
  else:row.update({'status':'source comparison needs review','candidates':ss})
 else:row['status']='original source absent'if sid else'generated label; no original source identity'
 reports.append(row)
(H/'checkbox-label-fields.json').write_text(json.dumps([{'entity':f['entity'],'attribute':'answer-field/key','value':f['value'],'question':f['question'],'bare':False}for f in labels],indent=2));(H/'checkbox-label-source-comparison.json').write_text(json.dumps(reports,indent=2));(H/'checkbox-label-source-cache.json').write_text(json.dumps(sourcecache,indent=2));(H/'checkbox-label-proposals.json').write_text(json.dumps(proposals,indent=2));(H/'checkbox-label-syntax-errors.json').write_text(json.dumps(errors,indent=2));print('basis',C['basis_t'],'labels',len(labels),'source statuses',collections.Counter(r['status']for r in reports),'proposals',len(proposals),'errors',len(errors))
for r in reports:
 if r['status']=='source comparison needs review':print(r['entity'],r['source_identity'],r['label'])
