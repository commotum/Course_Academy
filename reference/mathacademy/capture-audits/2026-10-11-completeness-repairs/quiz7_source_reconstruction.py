"""Exact original live sources replace defective same-ID normalized history locally."""
from copy import deepcopy
from pathlib import Path
import hashlib,json,re
from scripts.storage import read_json,atomic_json
from historical_solution_supplement import typed_fields
SOURCES={
 'q-331821':{'key':'diagnostic-12','live_sha256':'5d8b1c44451cd704b8da47916c93cbea63778bf2db6e37221ccb377ade507cd8','history_sha256':'d0d93e4d0545c8b0816fb5f844ddfb94ef22db2ed194be65d553f5d87d039863','defect':'Original live authored prose literally joins below.By; history inserts a paragraph boundary. Both originals preserved; canonical prompt is the original live text.'},
 'q-37456':{'key':'diagnostic-58','live_sha256':'6f192f2662aa00b2467860ba039cc30a765537d443c4c4e8a49eae72631d20a5','history_sha256':'2c22432a31873d19a8d37a3cfe17cd9cf794e447f917eb8b2f0fdf09eb360490','defect':'History rendered an authored red literal \\boldsymbol command before the Hessian; live original has valid bold-italic f. Canonical source is the original live prompt, controls and worked solution; malformed history preserved separately.'}}
GRADE_KEYS={'grade','source_grade','result','source_result','field_grades','proof_feedback'}
FIELD_GRADE_KEYS={'source_selected','source_correct','source_result','correct_value','correct_option','correct_origin','correct_evidence','evidence'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def reconstruct_quiz7(record,question,page,repair,reextract):
 identity=record.get('math_academy_id')
 if identity not in SOURCES or repair.parents[1].name!='14111253':return question
 cfg=SOURCES[identity];state=read_json(repair/'originals/checkpoint.json');live_original=state['presentations'][cfg['key']]['question'];history_original=[q for q in state['history']['questions'] if q.get('math_academy_id')==identity]
 if len(history_original)!=1 or live_original.get('math_academy_id')!=identity:raise ValueError('Original reconstruction identity is not unique')
 history_original=history_original[0]
 if sha(live_original['html_path'])!=cfg['live_sha256'] or sha(history_original['html_path'])!=cfg['history_sha256']:raise ValueError('Original reconstruction HTML hash changed')
 markup=Path(live_original['html_path']).read_text();number=identity[2:]
 if identity=='q-331821':
  if {str(i) for i in range(4)}!={x for x in re.findall(r'id="selectList-'+number+r'-(\d+)"',markup)}:raise ValueError('Original select identity proof changed')
 else:
  if set('abcde')!={x for x in re.findall(r'id="questionWidget-choiceLetterCircle-'+number+r'-([a-e])"',markup)}:raise ValueError('Original radio identity proof changed')
  if '<mi mathvariant="bold-italic">f</mi>' not in markup:raise ValueError('Original Hessian variant proof changed')
 # Use this live source's OWN worked solution and unselected controls, not the history grade.
 live=reextract(live_original,page,repair)
 if not live.get('worked_solution') or live.get('answer_fields_complete') is not True or live.get('errors'):raise ValueError('Original live authored source remains incomplete')
 hist=reextract(history_original,page,repair,history=True)
 if identity=='q-331821':
  if live['problem'].replace('below.By definition','below.\n\nBy definition')!=hist['problem'] or typed_fields(live)!=typed_fields(hist):raise ValueError('Source pair differs beyond verified joined-prose defect')
 else:
  if hist['problem'].replace('\\text{\\boldsymbol}','')!=live['problem']:raise ValueError('Source pair differs beyond verified Hessian rendering defect')
  if len(live.get('answer_fields',live.get('fields',[])))!=1 or len(live.get('answer_fields',live.get('fields',[]))[0].get('choices',[]))!=5:raise ValueError('Original five radio choices are incomplete')
  # Preserve the actual live MathML bold-italic variant in normalized math.
  if live['problem'].count('{f}^{″}')!=1:raise ValueError('Hessian replacement is not unique')
  live['problem']=live['problem'].replace('{f}^{″}','\\boldsymbol{f}^{″}')
 certificate={'question_id':identity,'canonical_authored_source':'original live prompt, original typed controls and original live worked solution','grade_transfer':False,'original_defect':cfg['defect'],'live_html':live_original['html_path'],'live_html_sha256':cfg['live_sha256'],'history_html':history_original['html_path'],'history_html_sha256':cfg['history_sha256'],'original_checkpoint_sha256':sha(repair/'originals/checkpoint.json'),'original_live_json_sha256':hashlib.sha256(json.dumps(live_original,sort_keys=True).encode()).hexdigest(),'original_history_json_sha256':hashlib.sha256(json.dumps(history_original,sort_keys=True).encode()).hexdigest(),'original_history_problem':hist['problem'],'original_live_problem':reextract(live_original,page,repair)['problem'],'canonical_problem':live['problem'],'typed_fields':typed_fields(live),'canonical_solution_sha256':hashlib.sha256(live['worked_solution'].encode()).hexdigest(),'extractor_sha256':live['recovery']['extractor_sha256']}
 proof=repair/'same-id-source-reconstruction'/identity;proof.mkdir(parents=True,exist_ok=True)
 atomic_json(proof/'certificate.json',certificate);atomic_json(proof/'original-live.json',live_original);atomic_json(proof/'original-history.json',history_original)
 live['source_reconstruction']=certificate
 if record.get('dom_id')=='questionContainer':
  question['problem']=live['problem'];question['source_reconstruction']=certificate
  return question
 # Reconstruction substitutes only the normalized source review, not original history/checkpoints.
 clean=deepcopy(live)
 # The exact own-ID history header remains valid authored topic/KP evidence
 # even where its problem rendering is defective. Do not discard it when
 # replacing the normalized prompt and controls with the original live source.
 header=Path(history_original['html_path']).read_text()
 title=history_original.get('knowledge_point')
 topic=history_original.get('topic_id')
 if title and topic:
  from bs4 import BeautifulSoup
  link=BeautifulSoup(header,'html.parser').select_one(f'#question-{number} > .questionHeader a.questionKP')
  if not link or link.get_text(strip=True)!=title or not str(link.get('href','')).startswith('/topics/'+str(topic)+'#'):raise ValueError('Original authored KP header does not match retained metadata')
  clean['knowledge_point']=title;clean['topic_id']=topic
  certificate['original_authored_kp_header']={'title':title,'topic_id':topic,'href':link['href'],'source_file':history_original['html_path'],'source_sha256':cfg['history_sha256'],'grade_transfer':False}
  atomic_json(proof/'certificate.json',certificate)
 for key in GRADE_KEYS:clean.pop(key,None)
 for bucket in ['fields','answer_fields']:
  for field in clean.get(bucket,[]):
   for key in FIELD_GRADE_KEYS:field.pop(key,None)
 clean['historical_source_defect']={'reason':cfg['defect'],'source':history_original['html_path'],'source_sha256':cfg['history_sha256'],'raw_original_preserved':str(proof/'original-history.json')}
 return clean
