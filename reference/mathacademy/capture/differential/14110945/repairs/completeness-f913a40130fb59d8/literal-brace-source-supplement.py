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

def refresh_own_polynomial_phantom(record,question,page,repair):
 # One independently compared external explanation needs its original hidden
 # width retained. No grades, controls, or visible mathematical values move.
 if record.get('math_academy_id')!='q-114506':return question,None
 source=Path(record.get('solution_evidence') or '')
 if not source.is_file() or sha(source.read_bytes())!='0a3daec48c92703e9e876e9918dd4cd19d356368d9c09b928cc3f191c1ef6195':return question,None
 baseline_file=Path(__file__).resolve().parent/'literal-brace-final-extract-frozen.js'
 baseline=baseline_file.read_bytes()
 if sha(baseline)!='1591183da328a4140792793d2cc113fd535ab5f25bc7f284ceb1b6f251efad18':raise ValueError('Original phantom baseline extractor changed')
 page.set_content(source.read_text());node=page.locator('#questionExplanation-114506')
 if node.count()!=1:return question,None
 hidden=node.locator('menclose:not([notation]) mphantom, menclose[notation="longdiv"] mphantom')
 if hidden.count()!=1 or hidden.text_content()!='8':return question,None
 old=node.evaluate(baseline.decode());new=node.evaluate(EXTRACT)
 try:before,assets=bound_solution(old,record);after,newassets=bound_solution(new,record)
 except ValueError:return question,None
 old_span=r'\enclose{longdiv}{\,\,6{x}^{4}-6{x}^{3}+5{x}^{2}-x+7\,\,}'
 new_span=r'\enclose{longdiv}{\,\,6{x}^{4}-6{x}^{3}+5{x}^{2}-\phantom{8}x+7\,\,}'
 if before!=record.get('worked_solution') or before.count(old_span)!=1 or after!=before.replace(old_span,new_span) or old['errors']!=new['errors'] or assets!=newassets:return question,None
 (repair/'decorated-phantom-old-extract.js').write_bytes(baseline)
 certificate={'kind':'same_id_original_external_hidden_width_restoration','id':'q-114506',
  'root_id':'questionExplanation-114506','original_source_file':str(source),'original_source_sha256':sha(source.read_bytes()),
  'baseline_extractor_sha256':sha(baseline),'current_extractor_sha256':sha(EXTRACT),
  'full_original_rendered_solution_matches_saved':True,'original_rendered_solution_sha256':sha(before),
  'current_rendered_solution_sha256':sha(after),'original_phantom_html':hidden.evaluate('el=>el.outerHTML'),
  'original_phantom_html_sha256':sha(hidden.evaluate('el=>el.outerHTML')),
  'exact_original_longdiv_span':old_span,'exact_restored_longdiv_span':new_span,
  'only_change':'Original hidden width8 retained under its own longdiv; visible mathematical text unchanged',
  'source_errors_preserved':old['errors'],'asset_bindings':assets,'grade_transfer':False}
 question['worked_solution']=after;question['solution_evidence']=str(source)
 question['decorated_phantom_solution_source_refresh']=certificate
 return question,certificate

def refresh_source(record,question,page,repair):
 identity=record.get('math_academy_id');certs=[]
 if not identity or identity!=question.get('math_academy_id'):return question
 question,phantom_certificate=refresh_own_polynomial_phantom(record,question,page,repair)
 if phantom_certificate:certs.append(phantom_certificate)
 path=record.get('solution_evidence');p=Path(path) if isinstance(path,str) else None
 if p and p.is_file() and p.suffix=='.html' and BRACES.search(p.read_text()):
  markup=p.read_text();page.set_content(markup);node=page.locator('#questionExplanation-'+identity.removeprefix('q-'))
  if node.count()==1:
   old=node.evaluate(OLD);new=node.evaluate(EXTRACT)
   try:
    before,assets=bound_solution(old,record);after,newassets=bound_solution(new,record)
    old_match=before==record.get('worked_solution');list_proof=None
    if not old_match and identity in {'q-214483','q-214479','q-214481'}:
     lists=node.evaluate("el => [...el.querySelectorAll('ol')].map(n => ({html:n.outerHTML,type:n.getAttribute('type'),start:n.getAttribute('start'),count:n.children.length,values:[...n.children].map(c=>c.getAttribute('value')),nested:!!n.querySelector('ol,ul')}))")
     labels=re.findall(r'(?m)^([123])\\\. ',before)
     if len(lists)==1 and lists[0]['count']==3 and lists[0]['type'] in (None,'1') and lists[0]['start'] in (None,'1') and lists[0]['values']==[None,None,None] and not lists[0]['nested'] and labels==['1','2','3']:
      legacy=re.sub(r'(?m)^([123])\\\. ','- ',before)
      if legacy==record.get('worked_solution'):
       old_match=True;list_proof={'original_ordered_list_html':lists[0]['html'],'html_sha256':sha(lists[0]['html']),'literal_labels':['1','2','3'],'legacy_rendering_exactly_matches_saved':True,'restoration':'Original ordered-list labels replace the previous three bullet prefixes only'}
    if old_match and before!=after and old['errors']==new['errors'] and assets==newassets:
     certificate={'kind':'same_id_external_authored_solution_brace_refresh','id':identity,'original_source_file':str(p),'original_source_sha256':sha(p.read_bytes()),'root_id':node.get_attribute('id'),'old_rendered_solution_sha256':sha(before),'new_rendered_solution_sha256':sha(after),'before_extractor_sha256':sha(OLD),'current_extractor_sha256':sha(EXTRACT),'old_rendered_solution_matches_original':True,'asset_bindings':assets,'source_errors_preserved':old['errors'],'grade_transfer':False}
     if list_proof:certificate['explicit_original_ordered_list_restoration']=list_proof
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
  # Stored field dictionaries cannot establish source facts jointly: reconstruct
  # every typed row and the selected Correct marker from the immutable artifact.
  source=Path(old.get('evidence',{}).get('source_file',''))
  if not source.is_file() or source.suffix!='.html':continue
  page.set_content(source.read_text());number=identity.removeprefix('q-')
  root=page.locator('[id="step-q'+number+'"], [id="question-'+number+'"]')
  if root.count()!=1:continue
  raw_before=root.evaluate(OLD);raw_after=root.evaluate(EXTRACT)
  previous=[v for v in raw_before['fields'] if v.get('key')==old['key'] and v.get('type')==old['type']]
  current=[v for v in raw_after['fields'] if v.get('key')==f['key'] and v.get('type')==f['type']]
  if len(previous)!=1 or len(current)!=1:continue
  previous,current=previous[0],current[0]
  def raw_rows_match(stored,actual):
   return len(stored)==len(actual) and all(all(a.get(k)==b.get(k) for k in ['option','dom_id','type','html','value']) for a,b in zip(stored,actual))
  if not previous.get('choices_complete') or not current.get('choices_complete') or not raw_rows_match(prior,previous['choices']) or not raw_rows_match(choices,current['choices']):continue
  if f['type']=='select':
   if not old.get('dom_id') or not old.get('frame_id') or any(old.get(k)!=f.get(k) or old.get(k)!=previous.get(k) or f.get(k)!=current.get(k) for k in ['dom_id','frame_id']):continue
   control=root.locator('[id="'+old['dom_id']+'"]')
   if control.count()!=1 or control.locator('[id="'+old['frame_id']+'"]').count()!=1:continue
   selected_source=previous.get('source_correct');selected_now=current.get('source_correct')
   if previous.get('source_result')!='Correct' or current.get('source_result')!='Correct' or selected_source!={'type':prior[selected[0]]['type'],'value':value} or selected_now!={'type':choices[selected[0]]['type'],'value':choices[selected[0]]['value']}:continue
   physical={'question_root':root.get_attribute('id'),'dom_id':old['dom_id'],'frame_id':old['frame_id'],'control_outer_html_sha256':sha(control.evaluate('el=>el.outerHTML')),'complete_ordered_options':len(prior),'raw_correct_selection_before':selected_source,'raw_correct_selection_current':selected_now}
  else:
   if root.locator('.questionWidget-result').count()!=1 or root.locator('.questionWidget-result').inner_text().strip()!='Correct':continue
   accepted=root.locator('[id^="questionWidget-choiceLetterCircle-"]').evaluate_all("nodes=>nodes.filter(n=>n.style.backgroundColor==='rgb(64, 64, 64)' && ['white','rgb(255, 255, 255)'].includes(n.style.color)).map(n=>n.id)")
   if accepted!=[prior[selected[0]]['dom_id']]:continue
   physical={'question_root':root.get_attribute('id'),'unique_inline_selected_circle':accepted[0],'own_raw_result':'Correct','complete_ordered_options':len(prior)}
  control_binding={**physical,'original_source_file':str(source),'same_source_html_sha256':sha(source.read_bytes()),'old_and_current_typed_rows_reconstructed_from_raw':True,'raw_option_html_sha256':[sha(v['html']) for v in previous['choices']]}
  rows=[];valid=True
  for a,b in zip(prior,choices):
   html=a.get('html','')
   if (not a.get('dom_id') and not control_binding) or any(a.get(k)!=b.get(k) for k in ['dom_id','option','type']) or not html or sha(html)!=sha(b.get('html','')):valid=False;break
   if a.get('value')!=b.get('value'):
    if not BRACES.search(html):valid=False;break
    page.set_content('<div id="brace-choice-proof"><div class="questionWidget-text">'+html+'</div></div>');node=page.locator('#brace-choice-proof');before=node.evaluate(OLD)['problem'];after=node.evaluate(EXTRACT)['problem']
    def bare(v):return v[1:-1] if v.startswith('$') and v.endswith('$') and not v.startswith('$$') else v
    if bare(before)!=a.get('value') or bare(after)!=b.get('value'):valid=False;break
   rows.append({'dom_id':a.get('dom_id'),'option':a.get('option'),'type':a.get('type'),'original_html_sha256':sha(html),'old_value':a.get('value'),'current_value':b.get('value')})
  if not valid:continue
  index=selected[0];replacement=choices[index]['value'];certificate={'kind':'same_own_choice_serializer_key_rebind','id':identity,'field_key':f['key'],'field_type':f['type'],'all_original_rows_complete':True,'same_physical_choices_order_and_html':True,'rows':rows,'selected_index':index,'original_value':value,'current_value':replacement,'original_evidence':deepcopy(evidence),'current_extractor_sha256':sha(EXTRACT),'before_extractor_sha256':sha(OLD),'grade_transfer':False,'source_file_preserved':True}
  certificate['original_evidence']=deepcopy(old['evidence'])
  if control_binding:certificate['exact_own_source_control']=control_binding
  if f['type']=='select':certificate['exact_own_custom_select_control']=control_binding
  f['correct_value']=replacement;f['evidence']={**old['evidence'],'value':replacement};f['source_serializer_rebind']=certificate;certs.append(certificate)
 for index,cert in enumerate(certs):atomic_json(repair/'literal-brace-source-proofs'/(identity+'-'+str(index)+'.json'),cert)
 return question
