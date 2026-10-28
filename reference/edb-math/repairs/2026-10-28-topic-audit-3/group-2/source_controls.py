import json,re,sys,collections
from pathlib import Path
from bs4 import BeautifulSoup,Tag
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';s=p.read_text();ns={'__file__':str(p)};exec(compile(s.split('parents=json.loads')[0]+s[s.index('def roots(s):'):s.index('def visible(tex):')],str(p),'exec'),ns)
from question_capture.math_format import validate_math_structure
class ControlRenderer(ns['CompleteSourceRenderer']):
 def __init__(self):super().__init__(None);self.controls=[]
 def register(self,n):
  known={c['dom_id']:c for c in self.controls}
  for node in n.find_all(class_='selectList'):
   ident=node.get('id')
   if ident in known:continue
   values=[]
   for option in node.find_all(class_='selectListOption'):
    fs=ns['formulas'](str(option));v=fs[0]if len(fs)==1 and isinstance(fs[0],str)else option.get_text(' ',strip=True)
    if v not in values:values.append(v)
   key='field-'+str(len(self.controls)+1);item={'key':key,'values':values,'dom_id':ident,'html':str(node)};self.controls.append(item);known[ident]=item
 def m(self,n):
  if isinstance(n,Tag)and n.name=='msub':
   cs=n.find_all(recursive=False)
   if len(cs)==2:
    marker=re.fullmatch(r'\(S(\d+)\)',cs[1].get_text('',strip=True))
    if marker:
     index=int(marker[1]);assert index<len(self.controls),(index,len(self.controls));return'{{'+self.controls[index]['key']+'}}'
  if isinstance(n,Tag)and n.name=='mrow':
   cs=n.find_all(recursive=False)
   if len(cs)==3 and cs[0].get_text()=='{'and cs[-1].get_text()=='}'and cs[1].name=='msub':
    inner=cs[1].find_all(recursive=False)
    if len(inner)==2 and re.fullmatch(r'\(S\d+\)',inner[1].get_text('',strip=True)):return self.m(cs[1])
  return super().m(n)
 def render(self,n,extract_fields=False):
  if not isinstance(n,Tag):return super().render(n,extract_fields)
  cs=n.get('class',[])
  if extract_fields and 'selectList'in cs:
   ident=n.get('id');item=next(c for c in self.controls if c['dom_id']==ident);return'{{'+item['key']+'}}'
  if extract_fields and 'freeResponseTextbox'in cs:
   key='field-'+str(len(self.controls)+1);self.controls.append({'key':key,'values':[],'dom_id':n.get('id'),'html':str(n)});return'{{'+key+'}}'
  if n.name in ['svg','math','mjx-container']or'mjpage'in cs:
   if extract_fields and n.find(class_='selectList'):
    roots=n.find_all('mjx-assistive-mml',recursive=False);assert len(roots)==1,('direct-assistive-roots',len(roots));math=roots[0].find('math');assert math is not None;tex=ns['normalize_source_tex'](self.m(math));display=n.get('display')in['true','block'];return'\n\n$$\n'+tex+'\n$$\n\n'if display else'$'+tex+'$'
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
  try:
   soup=BeautifulSoup(s['html'],'html.parser');r.register(soup);text=r.text(soup,True);validate_math_structure(text)
  except Exception as ex:opts.append({'path':s['path'],'error':str(ex)});continue
  if r.controls:opts.append({'path':s['path'],'problem':text,'controls':r.controls,'errors':r.errors})
 out.append({'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'existing_fields':[{'entity':f[':db/id'],'key':f[':answer-field/key'],'values':[a[':answer/value']for a in f.get(':answer-field/choices',[])]}for f in q.get(':question/answer-fields',[])],'options':opts})
(H/'source-control-reconstructions.json').write_text(json.dumps(out,indent=2)+'\n');print('clozequestions',len(out),'withsourcecontrols',sum(any(o.get('controls')for o in d['options'])for d in out))
