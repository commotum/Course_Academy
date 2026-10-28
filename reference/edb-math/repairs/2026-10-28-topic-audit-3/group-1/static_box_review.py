import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,validate_math_structure
ns={'__file__':str(H/'propose_formulas.py')};exec((H/'propose_formulas.py').read_text().split('props=[];reject=[]')[0],ns);canon=ns['canonical'];nums=ns['nums'];D=json.loads((H/'current.json').read_text());by={q[':db/id']:q for q in D['questions']};sources=json.loads((H/'sources.json').read_text());props=json.loads((H/'source-reviewed-proposals.json').read_text());pby={(p['entity'],p['attribute']):p for p in props};out=[]
def c(v):
 v=re.sub(r'\\(?:boxed\{\\phantom\{[A-Za-z]+\}\}|enclose\{box\}\{\\phantom\{[A-Za-z]+\}\}|bbox\[[^\]]+\]\{\\phantom\{[A-Za-z]+\}\}|boxed\{\})','STATICBOX',v)
 v=canon(v);v=re.sub(r'_(?:\(([^()]+)\))',r'_\1',v);return v
for r in json.loads((H/'comparison.json').read_text()):
 if r['attribute']!='question/problem'or r['entity']not in by:continue
 b=r['best']
 if not b or len(b['formulas'])!=len(r['current']):continue
 for i,(old,new)in enumerate(zip(r['current'],b['formulas'])):
  if r'\boxed{}'not in old or r'\phantom{'not in new:continue
  source=next(s for s in sources if s['identity']==r['identity']and s['attribute']==r['attribute']and s['path']==b['path']and s['formulas']==b['formulas']);soup=BeautifulSoup(source['html'],'html.parser');controls=soup.select('.selectList,.freeResponseTextbox,input,select');ok=c(old)==c(new)and nums(old)==nums(new)and not controls
  out.append({'identity':r['identity'],'entity':r['entity'],'index':i,'source_path':source['path'],'before_tex':old,'source_tex':new,'static_source_box_without_controls':not controls,'outside_box_mathematics_equal':c(old)==c(new),'canonical_old':c(old),'canonical_source':c(new),'proposed':ok})
  if not ok:continue
  k=(r['entity'],r['attribute']);p=pby.get(k)
  if p is None:p={'entity':r['entity'],'attribute':r['attribute'],'before':by[r['entity']][':'+r['attribute']],'after':None,'reason':'Restore original static boxed hidden width without adding an input or changing the response frame.','evidence':{'basis_t':9837,'identity':r['identity'],'source_path':source['path'],'formula_changes':[]},'confidence':'high'};pby[k]=p;props.append(p)
  if any(ch['index']==i for ch in p['evidence']['formula_changes']):continue
  p['evidence']['formula_changes'].append({'index':i,'before_tex':old,'after_tex':new,'independent_check':'Source has no actual input/select in this formula; same ordered integrand/bounds outside one static source box, with hidden glyph width retained.'})
for p in props:
 spans=list(MATH.finditer(p['before']));after=p['before']
 for ch in sorted(p['evidence']['formula_changes'],key=lambda x:x['index'],reverse=True):
  m=spans[ch['index']];display=m[0].startswith(('$$',r'\[',r'\('));wrapped='$$\n'+ch['after_tex']+'\n$$'if display else'$'+ch['after_tex']+'$';after=after[:m.start()]+wrapped+after[m.end():]
 p['after']=after;validate_math_structure(after)
(H/'source-reviewed-proposals.json').write_text(json.dumps(props,indent=2)+'\n');(H/'static-box-review.json').write_text(json.dumps(out,indent=2)+'\n');print('static box source fields',len(out),'checked',sum(r['proposed']for r in out),'unresolved',[(r['identity'],r['index'])for r in out if not r['proposed']],'totalprops',len(props))
