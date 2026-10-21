import importlib.util,copy
from read import *
if __name__=='__main__':
 records=json.loads((HERE/'replacements.json').read_text());kp=json.loads((HERE/'kp.json').read_text())
 for patch in json.loads((HERE/'solution-updates.json').read_text()):
  q=copy.deepcopy(next(q for q in kp[':knowledge-point/questions']if q[':db/id']==patch['entity']));q[patch['attribute']]=patch['after'];records.append({'question':q})
 save('render-records.json',records);spec=importlib.util.spec_from_file_location('render_preview',ROOT/'generate/pipeline/render_preview.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);config=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-19-fraction-fences-corpus/generator-ui/browser-config.json').read_text());args=([ROOT,DB.config.math_root,'/'],config['browser'],config['playwright'],config['node']);m.render(records,HERE/'ui',*args);m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844');m.render(records,HERE/'ui-narrow',*args)
 for name in ('ui','ui-narrow'):assert json.loads((HERE/name/'rendering.json').read_text())['passed']
 save('ui-verification.json',{'passed':True,'questions':len(records),'pages':2*len(records),'widths':[1280,390]});print((HERE/'ui-verification.json').read_text())
