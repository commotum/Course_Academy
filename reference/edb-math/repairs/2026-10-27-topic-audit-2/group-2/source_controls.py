import json,re,sys,collections
from pathlib import Path
from bs4 import BeautifulSoup,Tag
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';s=p.read_text();ns={'__file__':str(p)};exec(compile(s.split('parents=json.loads')[0]+s[s.index('def roots(s):'):s.index('def visible(tex):')],str(p),'exec'),ns)
from question_capture.math_format import validate_math_structure
class ControlRenderer(ns['CompleteSourceRenderer']):
 def __init__(self):super().__init__(None);self.controls=[]
 def render(self,n,extract_fields=False):
  if not isinstance(n,Tag):return super().render(n,extract_fields)
  cs=n.get('class',[])
  if extract_fields and ('selectList'in cs or'freeResponseTextbox'in cs):
   key='field-'+str(len(self.controls)+1);values=[]
   for option in n.find_all(class_='selectListOption'):
    v=self.text(option);v=v[1:-1]if v.startswith('$')and v.endswith('$')and not v.startswith('$$')else v
    if v not in values:values.append(v)
   self.controls.append({'key':key,'values':values,'dom_id':n.get('id'),'html':str(n)});return'{{'+key+'}}'
  if n.name in ['svg','math','mjx-container']or'mjpage'in cs:
   fs=ns['formulas'](str(n))
   if len(fs)==1 and isinstance(fs[0],str):
    display=n.get('display')in['true','block']or'mjpage__block'in cs or(n.parent and'mjpage__block'in n.parent.get('class',[]));return'\n\n$$\n'+fs[0]+'\n$$\n\n'if display else'$'+fs[0]+'$'
   if fs:self.errors.append({'formula_count':len(fs),'formulas':fs});return''
  return super().render(n,extract_fields)
D=json.loads((H/'current.json').read_text());src=collections.defaultdict(list)
for s in json.loads((H/'sources.json').read_text()):
 if s['attribute']=='question/problem':src[s['identity']].append(s)
out=[]
for q in D['questions']:
 if'{{'not in q[':question/problem']:continue
 opts=[]
 for s in src[q.get(':question/math-academy-id')]:
  r=ControlRenderer()
  try:text=r.text(BeautifulSoup(s['html'],'html.parser'),True);validate_math_structure(text)
  except Exception as ex:opts.append({'path':s['path'],'error':str(ex)});continue
  if r.controls:opts.append({'path':s['path'],'problem':text,'controls':r.controls,'errors':r.errors})
 out.append({'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'existing_fields':[{'entity':f[':db/id'],'key':f[':answer-field/key'],'values':[a[':answer/value']for a in f.get(':answer-field/choices',[])]}for f in q.get(':question/answer-fields',[])],'options':opts})
(H/'source-control-reconstructions.json').write_text(json.dumps(out,indent=2)+'\n');print('clozequestions',len(out),'withsourcecontrols',sum(any(o.get('controls')for o in d['options'])for d in out))
for d in out:
 if d['entity']in[17592186217762,17592186217792,17592186217793,17592186217794,17592186217795,17592186217796,17592186217797,17592186167223,17592186167224]:
  print('\n',d['entity'],d['identity']);print([(o.get('path'),len(o.get('controls',[])),o.get('error'),o.get('errors'))for o in d['options']]);o=next((o for o in d['options']if o.get('controls')),{});print(o.get('problem',''));print([(c['key'],c['values'])for c in o.get('controls',[])])
