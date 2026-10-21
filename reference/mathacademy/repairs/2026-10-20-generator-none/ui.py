import importlib.util
from read import *
from scripts.generator_policy import checkbox_selection
if __name__=='__main__':
 examples=json.loads((HERE/'grading-examples.json').read_text());special=json.loads((HERE/'special-records.json').read_text());selected=[]
 for kp,truth in [(17592186100888,True),(17592186100888,False),(17592186147456,True),(17592186119848,True),(17592186054815,True),(17592186124472,False)]:
  r=next(r for r in special+examples if r.get('knowledge_point',{}).get('db_id')==kp and checkbox_selection(r)and checkbox_selection(r)[-1]==truth)
  selected.append(r)
 save('render-records.json',selected)
 spec=importlib.util.spec_from_file_location('render_preview',ROOT/'generate/pipeline/render_preview.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 config=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-19-fraction-fences-corpus/generator-ui/browser-config.json').read_text());args=([ROOT,DB.config.math_root,'/'],config['browser'],config['playwright'],config['node'])
 m.render(selected,HERE/'ui',*args);m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844');m.render(selected,HERE/'ui-narrow',*args)
 for dirname in ('ui','ui-narrow'):
  report=json.loads((HERE/dirname/'rendering.json').read_text());assert report['passed']
  for c in report['cases']:assert 'None of the above'in c['text']and 'leave all boxes unchecked'not in c['text']
 save('ui-verification.json',{'passed':True,'questions':len(selected),'pages':len(selected)*2,'widths':[1280,390],'visible_none_labels':True})
 print((HERE/'ui-verification.json').read_text())
