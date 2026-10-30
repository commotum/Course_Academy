"""Restore source teaching colors in matching table cells, preserving mathematics."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;P=H.parent;R=P.parents[3];sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer,reconstruct
from question_capture.math_format import MATH,ENV,environment,cells,normalize_source_tex,validate_math_boundaries,validate_matrix_layouts,validate_math_structure
sources=json.loads((H/'source-inventory.json').read_text());qs=json.loads((H/'proposed-questions.json').read_text());ss=[json.loads((P/'lesson.json').read_text()),json.loads((P/'expanded-scope/current.json').read_text())];objs={q[':question/math-academy-id']:q for q in qs};objs.update({'tutorial:'+str(c[':tutorial/math-academy-id']):c for s in ss for c in s['contents']if ':tutorial/content'in c});index=collections.defaultdict(list)
for r in sources:index[r['identity'],r['attribute']].append(r)
def source_formulas(html):
 s=BeautifulSoup(html,'html.parser');ns=s.select('.mjpage,mjx-container,math');ids={id(n)for n in ns};tex=[]
 for n in ns:
  if any(id(p)in ids for p in n.parents):continue
  title=n.find('title')
  if title:t=reconstruct(title)
  else:
   r=SourceRenderer(None);math=n if n.name=='math'else n.find('math');assert math is not None;t=normalize_source_tex(r.m(math));assert not r.errors,r.errors
  tex.append(t)
 return tex
def source_tex(html):return '\n'.join(source_formulas(html))
def canonical(v):
 v=re.sub(r'\\bbox(?:\[[^]]*\])?','',v);v=re.sub(r'\\color(?:\[[^]]*\])?\{[^{}]*\}','',v);v=re.sub(r'\\(?:hspace|vspace)\{[^{}]*\}','',v);v=re.sub(r'\\(?:text|textrm|mathrm)\{[\s\u00a0]*\}','',v)
 v=v.replace(r'\text{det}','det').replace('✓',r'\checkmark');v=re.sub(r'\\(?:quad|qquad)(?![A-Za-z])','',v)
 v=re.sub(r'\\(?:mathbf|mathit|mathrm|textrm|operatorname|displaystyle|textstyle|left|right)\b','',v);v=re.sub(r'\\[,;! ]','',v)
 return re.sub(r'[\s{}]','',v).replace('−','-').replace('∗',r'\ast').replace("′",r'\prime')
def tables(text):
 out=[]
 for m in ENV.finditer(text):
  if m[1]!='begin':continue
  span=environment(text,m.start());assert span
  body=text[span[0]:span[1]];base=span[0]
  if ENV.search(body):continue
  if m[2]=='array':
   cols=re.match(r'\s*\{[^{}]+\}',body)
   if not cols:continue
   base+=cols.end();body=body[cols.end():]
  grid=cells(body)
  if not grid:continue
  key=tuple(tuple(canonical(c)for c in row)for row in grid)
  out.append({'key':key,'grid':grid,'body':body,'start':base,'end':span[1]})
 return out
proposals=[];review=[];verified=[]
for c in json.loads((H/'color-candidates.json').read_text()):
 mid,attr=c['identity'],c['attribute'];obj=objs[mid];old=obj.get(':'+attr,'');ct=tables(old);options=[];notes=[]
 for src in index[mid,attr]:
  try:st=tables(source_tex(src['html']))
  except Exception as e:notes.append({'path':src['path'],'error':str(e)});continue
  pairs=[];valid=True
  keys={t['key']for t in st if any(r'\color'in cell or r'\bbox'in cell for row in t['grid']for cell in row)}
  for key in keys:
   srcs=[t for t in st if t['key']==key];currents=[t for t in ct if t['key']==key]
   if len(srcs)!=len(currents):valid=False;break
   pairs.extend(zip(srcs,currents))
  if not valid:notes.append({'path':src['path'],'source_tables':len(st),'current_tables':len(ct),'unmatched_colored_key':key});continue
  edits=[];painted=0
  for a,b in pairs:
   offset=0
   for sr,cr in zip(a['grid'],b['grid']):
    for sc,cc in zip(sr,cr):
     pos=b['body'].find(cc,offset);assert pos>=0;offset=pos+len(cc)
     if (r'\color'in sc or r'\bbox'in sc)and canonical(sc)==canonical(cc)and sc!=cc:
      edits.append((b['start']+pos,b['start']+offset,sc));painted+=1
  new=old
  for a,b,value in sorted(edits,reverse=True):new=new[:a]+value+new[b:]
  # Outside matrices, restore source emphasis only when the complete scalar
  # formula has the same mathematical tokens. Preserve current math boundaries.
  sf=[t for t in source_formulas(src['html'])if not ENV.search(t)]
  cm=list(MATH.finditer(new));cm=[m for m in cm if not ENV.search(m[0])]
  scalar_edits=[]
  for key in {canonical(t)for t in sf if r'\color'in t or r'\bbox'in t}:
   ss=[t for t in sf if canonical(t)==key];mm=[m for m in cm if canonical(m[0][2:-2]if m[0].startswith(('$$',r'\(',r'\['))else m[0][1:-1])==key]
   if len(ss)!=len(mm):continue
   for value,m in zip(ss,mm):
    if r'\color'not in value and r'\bbox'not in value:continue
    edge=2 if m[0].startswith(('$$',r'\(',r'\['))else 1
    old_body=m[0][edge:-edge]
    if canonical(old_body)!=canonical(value):raise AssertionError('Scalar mathematical content changed')
    scalar_edits.append((m.start()+edge,m.end()-edge,value))
  for a,b,value in sorted(scalar_edits,reverse=True):new=new[:a]+value+new[b:]
  assert[t['key']for t in tables(new)]==[t['key']for t in ct]
  for fn in[validate_math_boundaries,validate_matrix_layouts,validate_math_structure]:fn(new)
  options.append({'path':src['path'],'after':new,'colored_cells':painted,'scalar_formulas_restored':len(scalar_edits)})
 if not options:review.append({**c,'notes':notes});continue
 assert len({o['after']for o in options})==1,(mid,attr,'Source colors disagree')
 o=options[0]
 if o['after']!=old:proposals.append({'entity':obj[':db/id'],'attribute':attr,'before':old,'after':o['after'],'reason':'Restore archived explanatory cell colors after verifying every ordered table cell is mathematically unchanged.'})
 verified.append({'entity':obj[':db/id'],'identity':mid,'attribute':attr,'matched_source':o['path'],'colored_cells_restored':o['colored_cells'],'scalar_formulas_restored':o['scalar_formulas_restored'],'all_table_cells_mathematically_unchanged':True})
(H/'color-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'color-verification.json').write_text(json.dumps({'passed':not review,'checks':verified,'review':review},indent=2)+'\n');print('Color repairs',len(proposals),'verified candidates',len(verified),'review',len(review));print([(r['identity'],r['attribute'])for r in review])
