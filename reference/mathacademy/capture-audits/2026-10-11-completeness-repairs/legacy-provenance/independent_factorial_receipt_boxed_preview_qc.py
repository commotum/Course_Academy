import json,hashlib,uuid,collections,re
from scripts.database.images import extension
from scripts.browser.assets import replace_markers
from urllib.parse import urljoin
from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.database.edn import loads
from scripts.database.text import markdown
from scripts.database.evidence import authoritative_question
from scripts.legacy_recovery import source_record,current_supported_reviews
from scripts.browser.adapter import EXTRACT
F=Path('reference/mathacademy/factorials-13831129/repairs/fieldless-original-content-inputs');P=F/'native-fieldless-content';source=json.loads((F/'source-inputs.json').read_text());questions={q['math_academy_id']:q for q in source['questions']};after={row[0][':question/math-academy-id']:row[0] for row in loads((P/'after/questions.edn').read_text())};assert set(after)==set(questions)
request=next((P/'requests').iterdir());receipt=loads((request/'receipt.edn').read_text());req=json.loads((request/'request.json').read_text());assert receipt[':edb/committed'] and receipt[':edb/db-before-t']==1155 and receipt[':edb/db-after-t']==1156;assert req['source']==':org/Math-Academy';assert hashlib.sha256((request/'transaction.edn').read_bytes()).hexdigest()==req['transaction_sha256'];assert (request/'transaction.edn').read_bytes()==(P/'transaction.edn').read_bytes();assert len(receipt[':edb/tx-data'])==36 and all(row[4]==17592186045417 and row[5] is True for row in receipt[':edb/tx-data']);assert {row[1] for row in receipt[':edb/tx-data']}=={50,1038,1069,1071,1072,1074}
for mid,q in questions.items():
 actual=after[mid];assert str(actual[':question/id'])==q['question_uuid'];assert actual[':question/problem']==markdown(q['problem']);assert actual[':question/worked-solution']==markdown(q['worked_solution']);assert not actual.get(':question/answer-fields');assert q['knowledge_point_uuid'] in {str(k[':knowledge-point/id']) for k in actual[':knowledge-point/_questions']}
old=loads((P/'snapshot.edn').read_text());oldpoints={e[':db/id']:e for e in old['entities'] if e.get(':knowledge-point/id') and str(e[':knowledge-point/id']) in {q['knowledge_point_uuid'] for q in questions.values()}};points={r[0][':db/id']:r[0] for r in loads((P/'after/knowledge-points.edn').read_text())};assert set(points)==set(oldpoints)
for eid,point in points.items():
 prior=oldpoints[eid];wanted={e[':db/id'] for e in prior[':knowledge-point/questions']};wanted|={after[mid][':db/id'] for mid,q in questions.items() if str(point[':knowledge-point/id'])==q['knowledge_point_uuid']};assert {e[':db/id'] for e in point[':knowledge-point/questions']}==wanted
 for k,v in prior.items():
  if k==':knowledge-point/questions':continue
  scalar=lambda x:x.get(':db/id') if isinstance(x,dict) else x
  assert scalar(v)==scalar(point.get(k)),(eid,k)
second={row[0][':question/math-academy-id']:row[0] for row in loads((P/'second-prepare/questions-0.edn').read_text())};assert second==after
factorial={'status':'independent_pinned_after_and_receipt_qc_pass','basis_before':1155,'basis_after':1156,'original_questions':7,'question_uuid_and_authored_texts_exact':True,'original_KP_links_and_prior_KP_memberships_metadata_preserved':True,'answer_fields':0,'receipt_content_assertions':35,'retractions':0,'source_eid':17592186045417,'only_source_content_attributes_plus_automatic_transaction_time':True,'repeat_pinned_questions_equal':True,'database_writes':0};(F/'independent-committed-readback-qc.json').write_text(json.dumps(factorial,indent=2)+'\n')
R=Path('reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance');preview=json.loads((R/'boxed-phantom-preview.json').read_text());D=Path(preview['directory']);evidence=json.loads((D/'source-evidence.json').read_text());content=json.loads((D/'content.json').read_text());assert hashlib.sha256(json.dumps(content,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==evidence['content_sha256'];reviewed=current_supported_reviews(R);native={row[0][':question/math-academy-id']:row[0] for row in loads((Path(preview['readback_directory'])/'before-0.edn').read_text())};tx=loads((D/'database/transaction.edn').read_text());by_eid={e[':db/id']:e for e in tx};assert len(tx)==11 and len(by_eid)==11 and all(isinstance(e,dict) and set(e)-{':db/id',':db/ensure'}<={':question/problem',':question/worked-solution'} and e[':db/ensure']==[':question/validate'] for e in tx)
def published_text(value):
 def localize(m):
  path=Path(m[2]);data=path.read_bytes();digest=hashlib.sha256(data).hexdigest();relative=f'images/{digest[:2]}/{digest}.{extension(data)}';targets=[Path('/media/jake/SSD/EDB/math')/relative];assert targets and all(t.read_bytes()==data for t in targets),(str(path),'published_bytes');return '!['+m[1]+']('+relative+')'
 return markdown(re.sub(r'!\[([^\]]*)\]\(([^\s)]+)\)',localize,value))
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);ctx=browser.new_context();ctx.route('**/*',lambda r:r.abort());page=ctx.new_page()
 for q in content['questions']:
  mid=q['math_academy_id'];binding=next(b for b in evidence['bindings'] if b['id']==mid);statefile=Path(binding['state_file']);assert hashlib.sha256(statefile.read_bytes()).hexdigest()==binding['state_sha256'];state=json.loads(statefile.read_text());fresh=source_record(Path(binding['directory']),mid);assert hashlib.sha256(json.dumps(fresh,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==binding['source_hash'];assert q==authoritative_question(reviewed[mid]['question']);assert reviewed[mid]['source_hash']==binding['source_hash'];stored=native[mid];edit=by_eid[stored[':db/id']];parts=[]
  reconstruct=json.loads(Path(fresh['source_reconstruction']['source_file']).read_text())
  for part,attr in [('problem',':question/problem'),('worked_solution',':question/worked-solution')]:
   if attr not in edit:continue
   assert edit[attr]==published_text(q[part]), (mid,part,'transaction_text');rec=next(p for p in reconstruct['parts'] if p['part']==part);record=state['questions'][mid][rec['original_record']];assert hashlib.sha256(record['html'].encode()).hexdigest()==rec['original_html_sha256'],(mid,part,'html_sha');assert rec['extractor_sha256']==hashlib.sha256(EXTRACT.encode()).hexdigest(),(mid,part,'extractor_sha',rec['extractor_sha256'],hashlib.sha256(EXTRACT.encode()).hexdigest());page.set_content(record['html']);root=page.locator('[id='+json.dumps(record['dom_id'])+']').first;parsed=root.evaluate(EXTRACT);assert parsed['errors']==[],(mid,part,'extraction_errors',parsed['errors']);replacements={}
   for a in parsed['assets']:
    matches=[old for old in record.get('assets',[]) if old.get('path') and old.get('tag')==a['tag'] and (old.get('html')==a['html'] or a.get('source_url') and urljoin(record.get('source_url') or 'https://mathacademy.com/',old.get('source_url') or '')==urljoin(record.get('source_url') or 'https://mathacademy.com/',a['source_url']))];assert len(matches)==1,(mid,part,'asset_binding');old=matches[0];assert hashlib.sha256(Path(old['path']).read_bytes()).hexdigest()==old['sha256'];replacements['@asset-'+str(a['index'])+'@']=old['path']
   parsed=replace_markers(parsed,replacements);assert parsed[part]==q[part],(mid,part,'raw_equal',parsed[part],q[part]);parts.append(part)
  wanted=q['answer_fields'];held=stored[':question/answer-fields'];assert len(wanted)==len(held)
  for field in wanted:
   before=next(f for f in held if f[':answer-field/key']==field['key']);typed=lambda a:(a[':answer/type'][':db/ident'].split('/')[-1],a[':answer/value']);assert before[':answer-field/type'][':db/ident'].split('/')[-1]==field['type'];assert {typed(a) for a in before[':answer-field/choices']}=={(a['type'],a['value']) for a in field['choices']};assert typed(before[':answer-field/correct'])==(field['correct_type'],field['correct_value'])
  results.append({'id':mid,'native_question_eid':stored[':db/id'],'question_uuid':str(stored[':question/id']),'own_raw_authored_parts_equal':parts,'fields_and_correct_unchanged':True,'native_prior_box_or_phantom_present':any('\\boxed{' in stored.get(k,'') or '\\phantom{' in stored.get(k,'') for k in (':question/problem',':question/worked-solution'))})
 ctx.close();browser.close()
sources=[row for file in Path(preview['readback_directory']).glob('active-sources-*.edn') if '-inputs' not in file.name and '-query' not in file.name for row in loads(file.read_text())];assert {str(row[-1]) for row in sources}=={':org/Math-Academy'};boxed={'status':'independent_boxed11_preview_source_qc_pass','basis':1156,'source':':org/Math-Academy','questions':11,'transaction_maps':11,'field_answer_uuid_choice_correct_learner_changes':False,'native_removed_choice_ownership':[],'omissions':[],'own_raw_reextraction_and_hash_checks':results,'database_writes':0};out=R/'boxed-phantom-independent-preview-qc.json';out.write_text(json.dumps(boxed,indent=2)+'\n');print(json.dumps({'factorial':factorial,'boxed':boxed},indent=2))
