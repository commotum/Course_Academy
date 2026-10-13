import sys,json,hashlib,tempfile
from copy import deepcopy
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path('/home/jake/Developer/Course_Academy/reference/mathacademy/capture-audits/2026-10-11-completeness-repairs');sys.path.insert(0,str(root))
import literal_brace_source_supplement as s
s.atomic_json=lambda *args,**kwargs:None
output=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda r:r.abort());page=context.new_page()
 for task,mid in [('14117627','q-214479'),('14117627','q-214481'),('14114807','q-172706')]:
  base=root.parents[1]/'capture/linear'/task/'repairs/completeness-f31ec8f96c25ef6c'
  old,new=(deepcopy(next(q for q in json.loads((base/name).read_text())['questions'] if q['math_academy_id']==mid)) for name in ['originals/content.json','content.json'])
  for f in old['answer_fields']:
   if f.get('evidence',{}).get('kind')!='ma_correct_grade':continue
   path=Path(f['evidence']['source_file']);page.set_content(path.read_text());node=page.locator('[id="step-'+mid.replace('q-','q')+'"], [id="question-'+mid.removeprefix('q-')+'"]');raw=node.evaluate(s.OLD)
   rf=next((v for v in raw['fields'] if v['key']==f['key']),None)
   output.append({'mid':mid,'key':f['key'],'source_sha256':s.sha(path.read_bytes()),'root_count':node.count(),'root_id':node.get_attribute('id'),'raw_result':raw.get('result'),'raw_source_selected':rf.get('source_selected') if rf else None,'raw_source_correct':rf.get('source_correct') if rf else None,'raw_field_result':rf.get('source_result') if rf else None,'raw_choice_rows_exact':rf.get('choices')==f.get('choices') if rf else False,'original_correct_value':f.get('correct_value'),'evidence_value':f['evidence'].get('value')})
  q=s.refresh_source(deepcopy(old),deepcopy(new),page,Path(tempfile.gettempdir()))
  output.append({'mid':mid,'rebind_fields':[v['key'] for v in q['answer_fields'] if v.get('source_serializer_rebind')],'source_paths_preserved':all(v['evidence']['source_file']==next(a for a in old['answer_fields'] if a['key']==v['key'])['evidence']['source_file'] for v in q['answer_fields'] if v.get('source_serializer_rebind'))})
  if mid in ('q-214479','q-172706'):
   # Probe whether physical option HTML is actually validated against the own original DOM.
   # Change both supplied old/new row HTML only, leaving exact own source bytes and IDs intact.
   a,b=deepcopy(old),deepcopy(new);af,bf=a['answer_fields'][2 if mid=='q-214479' else 0],b['answer_fields'][2 if mid=='q-214479' else 0]
   html='<span class="mjpage"><math><mrow><mo>{</mo><mi>z</mi><mo>}</mo></mrow></math></span>'
   af['choices'][0]['html']=bf['choices'][0]['html']=html
   af['choices'][0]['value']='{z}';bf['choices'][0]['value']=r'\{z\}'
   af['correct_value']=bf['correct_value']='{z}';af['evidence']['value']=bf['evidence']['value']='{z}'
   probe=s.refresh_source(a,b,page,Path(tempfile.gettempdir()))
   output.append({'mid':mid,'probe':'same-own-source-but-fabricated-stored-row-html','accepted':bool(probe['answer_fields'][2 if mid=='q-214479' else 0].get('source_serializer_rebind')),'correct_value':probe['answer_fields'][2 if mid=='q-214479' else 0].get('correct_value')})
 browser.close()
print(json.dumps(output,indent=2))
Path('/tmp/literal-brace-independent-qc.json').write_text(json.dumps(output,indent=2))
