"""Approved repair-local same-ID solution and physical-choice serializer refreshes."""
from copy import deepcopy
from pathlib import Path
import hashlib,re
from urllib.parse import urljoin
from scripts.browser.adapter import EXTRACT
from scripts.storage import atomic_json
from scripts.activity.policy import answer_fields
OLD=EXTRACT.replace('literalFence(n.textContent)','n.textContent').replace("literalFence(n.getAttribute('open') || '(')","(n.getAttribute('open') || '(')").replace("literalFence(n.getAttribute('close') || ')')","(n.getAttribute('close') || ')')").replace("[')',']','}','\\\\}']","[')',']','}']")
BRACES=re.compile(r'<mo\b[^>]*>\s*[{}]\s*</mo>|<mfenced\b[^>]*(?:open|close)=["\'][{}]["\']',re.I)
def sha(value):return hashlib.sha256(value.encode() if isinstance(value,str) else value).hexdigest()
def bound_solution(parsed,record):
 text=parsed['worked_solution'];proof=[]
 for a in parsed['assets']:
  url=urljoin(record.get('source_url') or 'https://mathacademy.com/',a.get('source_url') or '')
  matches=[v for v in record.get('assets',[]) if v.get('path') and v.get('tag')==a['tag'] and (urljoin(record.get('source_url') or 'https://mathacademy.com/',v.get('source_url') or '')==url if a.get('source_url') else v.get('html')==a.get('html'))]
  bindings={(v['path'],v.get('sha256')) for v in matches}
  if len(bindings)!=1:raise ValueError('No unique exact original solution asset bytes')
  path,digest=next(iter(bindings));p=Path(path)
  if not p.is_file() or sha(p.read_bytes())!=digest:raise ValueError('Original solution asset SHA mismatch')
  text=text.replace('@asset-'+str(a['index'])+'@',path);proof.append({'index':a['index'],'source_url':url,'path':path,'sha256':digest,'tag':a['tag']})
 return text,proof

def refresh_source(record,question,page,repair):
 identity=record.get('math_academy_id');certs=[]
 if not identity or identity!=question.get('math_academy_id'):return question
 path=record.get('solution_evidence');p=Path(path) if isinstance(path,str) else None
 if p and p.is_file() and p.suffix=='.html' and BRACES.search(p.read_text()):
  markup=p.read_text();page.set_content(markup);node=page.locator('#questionExplanation-'+identity.removeprefix('q-'))
  if node.count()==1:
   old=node.evaluate(OLD);new=node.evaluate(EXTRACT)
   try:
    before,assets=bound_solution(old,record);after,newassets=bound_solution(new,record)
    if before==record.get('worked_solution') and before!=after and old['errors']==new['errors'] and assets==newassets:
     certificate={'kind':'same_id_external_authored_solution_brace_refresh','id':identity,'original_source_file':str(p),'original_source_sha256':sha(p.read_bytes()),'root_id':node.get_attribute('id'),'old_rendered_solution_sha256':sha(before),'new_rendered_solution_sha256':sha(after),'before_extractor_sha256':sha(OLD),'current_extractor_sha256':sha(EXTRACT),'old_rendered_solution_matches_original':True,'asset_bindings':assets,'source_errors_preserved':old['errors'],'grade_transfer':False}
     question['worked_solution']=after;question['solution_evidence']=str(p);question['external_solution_source_refresh']=certificate;certs.append(certificate)
   except ValueError as error:
    atomic_json(repair/'literal-brace-source-proofs'/('external-unavailable-'+identity+'.json'),{'id':identity,'source_file':str(p),'source_sha256':sha(p.read_bytes()),'reason':str(error),'original_retained':True})
 oldfields={f.get('key'):f for f in answer_fields(record)}
 for f in answer_fields(question):
  old=oldfields.get(f.get('key'))
  if not old or old.get('type')!=f.get('type') or f.get('type') not in ['radio','select'] or not old.get('choices_complete') or not f.get('choices_complete'):continue
  value=f.get('correct_value');choices=f.get('choices',[]);prior=old.get('choices',[])
  if value is None or any(c.get('value')==value for c in choices) or len(prior)!=len(choices):continue
  evidence=f.get('evidence',{});grade=evidence.get('kind')=='ma_correct_grade'
  if not grade or evidence.get('value')!=value or old.get('correct_value')!=value:continue
  selected=[i for i,c in enumerate(prior) if c.get('value')==value]
  if len(selected)!=1:continue
  rows=[];valid=True
  for a,b in zip(prior,choices):
   html=a.get('html','')
   if not a.get('dom_id') or any(a.get(k)!=b.get(k) for k in ['dom_id','option','type']) or not html or sha(html)!=sha(b.get('html','')):valid=False;break
   if a.get('value')!=b.get('value'):
    if not BRACES.search(html):valid=False;break
    page.set_content('<div id="brace-choice-proof"><div class="questionWidget-text">'+html+'</div></div>');node=page.locator('#brace-choice-proof');before=node.evaluate(OLD)['problem'];after=node.evaluate(EXTRACT)['problem']
    def bare(v):return v[1:-1] if v.startswith('$') and v.endswith('$') and not v.startswith('$$') else v
    if bare(before)!=a.get('value') or bare(after)!=b.get('value'):valid=False;break
   rows.append({'dom_id':a['dom_id'],'option':a.get('option'),'type':a.get('type'),'original_html_sha256':sha(html),'old_value':a.get('value'),'current_value':b.get('value')})
  if not valid:continue
  index=selected[0];replacement=choices[index]['value'];certificate={'kind':'same_own_choice_serializer_key_rebind','id':identity,'field_key':f['key'],'field_type':f['type'],'all_original_rows_complete':True,'same_physical_choices_order_and_html':True,'rows':rows,'selected_index':index,'original_value':value,'current_value':replacement,'original_evidence':deepcopy(evidence),'current_extractor_sha256':sha(EXTRACT),'before_extractor_sha256':sha(OLD),'grade_transfer':False,'source_file_preserved':True}
  f['correct_value']=replacement;f['evidence']={**evidence,'value':replacement};f['source_serializer_rebind']=certificate;certs.append(certificate)
 for index,cert in enumerate(certs):atomic_json(repair/'literal-brace-source-proofs'/(identity+'-'+str(index)+'.json'),cert)
 return question
