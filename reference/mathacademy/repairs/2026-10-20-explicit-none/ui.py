"""Render source-backed None choices through the real checkbox UI."""
import importlib.util
from repair import *
if __name__=='__main__':
 number=int(sys.argv[1]);base=HERE/f'batch-{number:02}';plan=json.loads((base/'plan.json').read_text());qmap={q[':db/id']:q for q in json.loads((base/'speculative.json').read_text())['questions']}
 selected=[]
 for p in plan['questions']:
  if p['id']==17592186272199 or p['reuse_field']:selected.append(p['id'])
 for predicate in [lambda p:p['none_correct'],lambda p:not p['none_correct'],lambda p:p['key']!='None of the above']:
  p=next((p for p in plan['questions']if predicate(p)and p['id']not in selected),None)
  if p:selected.append(p['id'])
 records=[{'question':qmap[qid]}for qid in selected];save(base/'ui-records.json',records)
 spec=importlib.util.spec_from_file_location('render_preview',ROOT/'generate/pipeline/render_preview.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 config=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-19-fraction-fences-corpus/generator-ui/browser-config.json').read_text())
 args=([ROOT,Path(DB.config.math_root),'/'],config['browser'],config['playwright'],config['node'])
 module.render(records,base/'ui',*args)
 module.BROWSER_SCRIPT=module.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844')
 module.render(records,base/'ui-narrow',*args)
 for name in ('ui','ui-narrow'):
  rendered=json.loads((base/name/'rendering.json').read_text());assert rendered['passed']
  for case,qid in zip(rendered['cases'],selected):
   p=next(p for p in plan['questions']if p['id']==qid);assert p['key']in case['text'];assert 'leave all boxes unchecked'not in case['text']
 save(base/'ui-verification.json',{'passed':True,'questions':selected,'widths':[1280,390],'visible_none_labels':True})
 print((base/'ui-verification.json').read_text())
