"""Source-occurrence converter for reviewed bulk repair. Never reads/writes EDB.

Retains mathematical trees, fences, table rows/cells/rules, visible decoration,
zero-rule stacks, and phantom width. Unsupported geometry fails closed.
Font size and inter-row/inter-column spacing may normalize to application defaults.
"""
from pathlib import Path
from contextvars import ContextVar
import hashlib,html,importlib.util,json,re,sys
from bs4 import BeautifulSoup,NavigableString,Tag
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts'))
import reconcile_remaining_ma_instruction as old
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import normalize_source_tex
CONTAINER=re.compile(r'<mjx-container\b[\s\S]*?</mjx-container>')
MML=re.compile(r'<math\b[\s\S]*?</math>')
STYLES={'normal':'mathrm','bold':'mathbf','italic':'mathit','double-struck':'mathbb','script':'mathcal','fraktur':'mathfrak','sans-serif':'mathsf','monospace':'mathtt','bold-italic':'boldsymbol'}
FENCES={'[':']','(':')','{':'}','|':'|','‖':'‖','∥':'∥'}
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def literal(s):return old.text_chars(s).replace(r'\_', '_').replace(r'\#', '#')
def chars(s):return old.tex_chars(s)
def color(c):
 if not re.fullmatch(r'[A-Za-z]+|#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?',c):raise ValueError('Unsupported color '+c)
 return c

_DISPLAYSTYLE=ContextVar('source_displaystyle',default=None)
def tex(node):
 explicit=node.get('displaystyle') if isinstance(node,Tag) else None
 token=_DISPLAYSTYLE.set(explicit=='true') if explicit in ('true','false') else None
 try:value=_tex(node)
 finally:
  if token is not None:_DISPLAYSTYLE.reset(token)
 if explicit in ('true','false') and node.name!='mtable':value='{'+('\\displaystyle ' if explicit=='true' else '\\textstyle ')+value+'}'
 return value

def _tex(node):
 if isinstance(node,NavigableString):
  if not node.strip():return ''
  raise ValueError('Unwrapped MathML text '+repr(str(node)))
 if not isinstance(node,Tag):raise ValueError('Unsupported node')
 if node.name in ('annotation','annotation-xml'):return ''
 if node.name in ('mtd','mtr') and any(a in node.attrs for a in ('columnspan','rowspan','columnalign','rowalign')):raise ValueError('Unsupported per-cell source geometry')
 if node.name=='mtable' and node.get('rowalign') not in (None,'baseline'):raise ValueError('Unsupported table row alignment')
 value=core(node)
 pad_child=None
 styled_children=[x for x in node.children if isinstance(x,Tag)]
 if (node.get('mathbackground') or node.get('style')) and len(styled_children)==1 and styled_children[0].name=='mpadded':
  pad_child=padding(styled_children[0])
  if pad_child:value=join(styled_children[0])
 variant=node.get('mathvariant')
 if variant:
  if variant not in STYLES:raise ValueError('Unsupported mathvariant '+variant)
  value='\\'+STYLES[variant]+'{'+value+'}'
 fg=node.get('mathcolor')
 if fg and fg not in ('inherit','transparent','none'):
  fg=color(fg)
  if fg.startswith('#'):
   hx=fg[1:];hx=''.join(c*2 for c in hx) if len(hx)==3 else hx
   value='{\\color[HTML]{'+hx+'}'+value+'}'
  else:value='{\\color{'+fg+'}'+value+'}'
 # Padding is handled by mpadded itself. This preserves the exact common bbox.
 bg=node.get('mathbackground');style=node.get('style')
 if bg or style:
  opts=[]
  if bg and bg not in ('inherit','transparent','none'):opts.append(color(bg))
  if style:
   match=re.fullmatch(r'\s*border\s*:\s*([^;]+);?\s*',style)
   if not match:raise ValueError('Unsupported source style '+style)
   tokens=match[1].split();widths=[x for x in tokens if re.fullmatch(r'\d+(?:pt|px|em|ex)',x)];colors=[x for x in tokens if re.fullmatch(r'[A-Za-z]+|#[a-fA-F0-9]+',x) and x!='solid']
   if len(tokens)!=3 or tokens.count('solid')!=1 or len(widths)!=1 or len(colors)!=1:raise ValueError('Unsupported border '+style)
   opts.append('border:'+widths[0]+' solid '+color(colors[0]))
  if pad_child:opts.insert(0,pad_child)
  if opts:value='\\bbox['+','.join(opts)+']{'+value+'}'
 return value

def padding(n):
 attrs={k:str(v) for k,v in n.attrs.items() if k in ('width','height','depth','lspace','voffset')}
 if not attrs:return None
 p=re.fullmatch(r'(\d+)(pt|px|em|ex)',attrs.get('lspace',''))
 if p and attrs=={'width':'+'+str(2*int(p[1]))+p[2],'height':'+'+p[0],'depth':'+'+p[0],'lspace':p[0]}:return p[0]
 raise ValueError('Unsupported mpadded geometry '+json.dumps(attrs,sort_keys=True))
def join(n):return ' '.join(tex(c) for c in n.children).strip()
def bare_fence(node):
 # MathJax wraps explicitly sized OPEN/CLOSE fence glyphs in mrow nodes.
 # Unwrap only grouping metadata; do not discard an instructional decoration.
 while node.name=='mrow':
  children=[c for c in node.children if isinstance(c,Tag)]
  if len(children)!=1 or any(not k.startswith('data-mjx-') for k in node.attrs):return None
  node=children[0]
 if node.name!='mo' or node.get('stretchy')=='false' or any(k in node.attrs for k in ('mathcolor','mathbackground','style','mathvariant')):return None
 value=node.get_text().strip()
 return value if value in set(FENCES)|set(FENCES.values()) else None
def core(n):
 name=n.name;cs=[c for c in n.children if isinstance(c,Tag)]
 if name in ('math','mrow','mtd','mstyle'):
  result=[];i=0
  while i<len(cs):
   c=cs[i]
   # A source zero-rule fraction is a stack/binomial. Its paired source
   # fences must enclose the full stack, including wrappers around the glyphs.
   opening=bare_fence(c)
   if opening in FENCES and i+2<len(cs) and cs[i+1].name=='mfrac' and re.fullmatch(r'0(?:\.0+)?(?:px|pt|em|ex|%)?',cs[i+1].get('linethickness','')) and bare_fence(cs[i+2])==FENCES[opening]:
    result.append('\\left'+chars(opening)+' '+tex(cs[i+1])+' \\right'+chars(FENCES[opening]));i+=3;continue
   if c.name=='mo' and c.get_text().strip() in FENCES and i+1<len(cs) and cs[i+1].name=='mtable':
    opening=c.get_text().strip();closing=cs[i+2].get_text().strip() if i+2<len(cs) and cs[i+2].name=='mo' else ''
    if closing==FENCES[opening] or opening=='{' and closing=='':
     result.append('\\left'+chars(opening)+' '+tex(cs[i+1])+' \\right'+(chars(closing) if closing else '.'))
     i+=3 if closing else 2;continue
   result.append(tex(c));i+=1
  return ' '.join(result)
 if name=='semantics':return tex(cs[0])
 if name=='mphantom':return '\\phantom{'+join(n)+'}'
 if name=='mpadded':
  if n.attrs=={'width':'0'} and len(cs)==1 and cs[0].name=='mphantom':return '\\vphantom{'+join(cs[0])+'}'
  p=padding(n)
  return ('\\bbox['+p+']{'+join(n)+'}') if p else join(n)
 if name=='mspace':
  width=n.get('width','')
  if width and not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:em|ex|px|pt)',width):raise ValueError('Unsupported mspace '+width)
  return '\\hspace{'+width+'}' if width and width not in ('0em','0px','0pt') else ''
 if name in ('mi','mn','mo','mtext','ms'):
  v=n.get_text()
  if name in ('mtext','ms'):
   if '[math]' in v or '[/math]' in v:
    parts=re.split(r'(\[math\][\s\S]*?\[/math\])',v);out=[]
    for part in parts:
     if part.startswith('[math]') and part.endswith('[/math]'):
      body=part[6:-7]
      if '[math]' in body or '[/math]' in body:raise ValueError('Nested source math markers')
      depth=0
      for token in re.findall(r'\\.|[{}]',body):
       depth+=1 if token=='{' else -1 if token=='}' else 0
       if depth<0:raise ValueError('Unbalanced source embedded TeX')
      if depth:raise ValueError('Unbalanced source embedded TeX')
      out.append('{'+normalize_source_tex(body)+'}')
     else:
      if '[math]' in part or '[/math]' in part:raise ValueError('Unbalanced source math markers')
      if part:out.append('\\text{'+literal(part)+'}')
    return ' '.join(out)
   return '\\text{'+literal(v)+'}' if v else ''
  if name=='mi' and v in old.CAPTURE.MATHML_TEX_OPERATOR_NAMES:return '\\'+v+' '
  return chars(v)
 if name=='mfrac' and len(cs)==2:
  thickness=n.get('linethickness','')
  if thickness and not re.fullmatch(r'0(?:\.0+)?(?:px|pt|em|ex|%)?',thickness) and thickness not in ('medium','1px'):raise ValueError('Unsupported nonstandard fraction thickness '+thickness)
  cmd='\\genfrac{}{}{0pt}{}' if re.fullmatch(r'0(?:\.0+)?(?:px|pt|em|ex|%)?',thickness) else '\\frac'
  return cmd+'{'+tex(cs[0])+'}{'+tex(cs[1])+'}'
 if name in ('msup','msub','msubsup') and len(cs)==(3 if name=='msubsup' else 2):
  marks=('_','^') if name=='msubsup' else ('^' if name=='msup' else '_',)
  return '{'+tex(cs[0])+'}'+''.join(mark+'{'+tex(c)+'}' for mark,c in zip(marks,cs[1:]))
 if name=='msqrt':return '\\sqrt{'+join(n)+'}'
 if name=='mroot' and len(cs)==2:return '\\sqrt['+tex(cs[1])+']{'+tex(cs[0])+'}'
 if name in ('mover','munder','munderover') and len(cs)==(3 if name=='munderover' else 2):
  base=tex(cs[0]);dec=cs[1].get_text().strip()
  if name=='mover' and cs[1].name=='mo' and dec=='→' and cs[1].get('stretchy')=='true':return '\\overrightarrow{'+base+'}'
  accents={'¯':'overline','‾':'overline','―':'overline','^':'hat','ˆ':'hat','→':'vec','˙':'dot','.':'dot','~':'tilde','˜':'tilde','⏞':'overbrace','⏟':'underbrace'}
  if name=='munder' and dec=='⏟':return '\\underbrace{'+base+'}'
  if name=='mover' and (n.get('accent')=='true' or dec in ('⏞','⏟','^','ˆ','¯','‾','―','→')) and dec in accents:return '\\'+accents[dec]+'{'+base+'}'
  if name=='munderover':return base+'_{'+tex(cs[1])+'}^{'+tex(cs[2])+'}'
  if cs[0].get_text().strip() in ('∑','∏','∫','lim','max','min'):return base+('_' if name=='munder' else '^')+'{'+tex(cs[1])+'}'
  return ('\\underset' if name=='munder' else '\\overset')+'{'+tex(cs[1])+'}{'+base+'}'
 if name=='menclose':
  notation=n.get('notation','longdiv').split();body=join(n)
  if notation==['updiagonalstrike']:return '\\cancel{'+body+'}'
  if notation==['downdiagonalstrike']:return '\\bcancel{'+body+'}'
  if set(notation)=={'updiagonalstrike','downdiagonalstrike'}:return '\\xcancel{'+body+'}'
  if notation==['box']:return '\\boxed{'+body+'}'
  if not set(notation)<=set('longdiv actuarial radical box roundedbox circle left right top bottom updiagonalstrike downdiagonalstrike verticalstrike horizontalstrike madruwb'.split()):raise ValueError('Unsupported enclosure '+str(notation))
  return '\\enclose{'+' '.join(notation)+'}{'+body+'}'
 if name=='mtable':
  if any(c.name!='mtr' for c in cs):raise ValueError('Unsupported labeled MathML row')
  rows=[[x for x in r.children if isinstance(x,Tag)] for r in cs]
  if not rows:return '' # Empty source table has no visible cells or rules.
  if any(c.name!='mtd' for row in rows for c in row):raise ValueError('Unsupported table cells')
  width=max(map(len,rows))
  rows=[row+[None]*(width-len(row)) for row in rows]
  align=n.get('columnalign','center').split() or ['center'];lines=n.get('columnlines','none').split() or ['none'];rl=n.get('rowlines','none').split() or ['none'];frame=n.get('frame','none')
  if any(x not in ('none','solid') for x in lines+rl+[frame]):raise ValueError('Unsupported table rules')
  at=lambda seq,i:seq[min(i,len(seq)-1)]
  spec='|' if frame=='solid' else ''
  for i in range(width):
   spec+={'center':'c','left':'l','right':'r'}[at(align,i)]
   if i<width-1 and at(lines,i)=='solid' or i==width-1 and frame=='solid':spec+='|'
  body='\\hline ' if frame=='solid' else ''
  for i,row in enumerate(rows):
   cellstyle='\\displaystyle ' if _DISPLAYSTYLE.get() is True else '\\textstyle ' if _DISPLAYSTYLE.get() is False else ''
   body+=' & '.join((cellstyle+tex(c)) if c is not None else '' for c in row)
   if i<len(rows)-1:body+=' \\\\ '+('\\hline ' if at(rl,i)=='solid' else '')
  if frame=='solid':body+=' \\\\ \\hline'
  return '\\begin{array}{'+spec+'}'+body+'\\end{array}'
 if name=='mfenced':
  sep=n.get('separators',',');body=''.join((chars(sep[min(i-1,len(sep)-1)]) if i and sep else '')+tex(c) for i,c in enumerate(cs))
  return '\\left'+chars(n.get('open','('))+body+'\\right'+chars(n.get('close',')'))
 raise ValueError('Unsupported MathML '+name)

def mathml(source):
 soup=BeautifulSoup(source,'html.parser');math=soup.find('math')
 if math is None:raise ValueError('Missing MathML')
 return tex(math)
def interpolate_text_wrappers(body,fragments):
 """Keep source math fragments in math mode inside literal text wrappers."""
 marker=re.compile(r'BULKMATHFRAGMENT\d+END')
 command=re.compile(r'\\(textrm|text|textsf|texttt|textbf|textit|fbox)\s*\{')
 # Process innermost wrappers first. A new literal chunk has no marker and is
 # therefore not revisited; no TeX token or mathematical fragment is reordered.
 for match in reversed(list(command.finditer(body))):
  opening=match.end()-1;depth=1;i=opening+1
  while i<len(body) and depth:
   if body[i]=='\\' and i+1<len(body):i+=2;continue
   if body[i]=='{':depth+=1
   elif body[i]=='}':depth-=1
   i+=1
  if depth:raise ValueError('Unbalanced source text-mode wrapper')
  payload=body[opening+1:i-1]
  if not marker.search(payload):continue
  payload=re.sub(r'\{\s*(BULKMATHFRAGMENT\d+END)\s*\}',r'\1',payload)
  parts=[];pos=0
  for m in marker.finditer(payload):
   literal_part=payload[pos:m.start()]
   if literal_part:
    if '{' in literal_part or '}' in literal_part:raise ValueError('Unsupported grouped literal around mixed math fragment')
    parts.append('\\'+('textrm' if match[1]=='fbox' else match[1])+'{'+literal_part+'}')
   parts.append('{'+fragments[m[0]]+'}');pos=m.end()
  literal_part=payload[pos:]
  if literal_part:
   if '{' in literal_part or '}' in literal_part:raise ValueError('Unsupported grouped literal around mixed math fragment')
   parts.append('\\'+('textrm' if match[1]=='fbox' else match[1])+'{'+literal_part+'}')
  replacement=('\\boxed{' if match[1]=='fbox' else '{')+' '.join(parts)+'}'
  body=body[:match.start()]+replacement+body[i:]
 return body

def convert_source(record):
 source=record['source_html'];out={'id':record['id'],'source_sha256':digest(source),'errors':[]}
 try:
  if source.startswith('<title'):
   body=re.sub(r'^<title\b[^>]*>|</title>\s*$','',source)
   # Source nested MathML is a math payload, while fbox is text mode in TeX.
   body=re.sub(r'\\fbox(?=\s*\{\s*<mjx-container\b)',lambda m:r'\boxed',body)
   fragments={}
   def fragment(value):
    token='BULKMATHFRAGMENT'+str(len(fragments))+'END';fragments[token]=value;return token
   def replace_container(m):
    maths=MML.findall(m[0])
    if not maths:raise ValueError('Rendered container lacks MathML')
    # Duplicate assistive representations are allowed only if identical trees.
    values={mathml(s) for s in maths}
    if len(values)!=1:raise ValueError('Container has differing math representations')
    return fragment(next(iter(values)))
   body=CONTAINER.sub(replace_container,body)
   body=MML.sub(lambda m:fragment(mathml(m[0])),body)
   body=interpolate_text_wrappers(body,fragments)
   for token,fragment_tex in fragments.items():body=body.replace(token,'{'+fragment_tex+'}')
   if re.search(r'</?[A-Za-z][^>]*>',body):raise ValueError('Unconverted source HTML in title')
   body=html.unescape(body)
   body=re.sub(r'\\require\s*\{(?:cancel|color|bbox|enclose)\}','',body)
   value=normalize_source_tex(body)
  else:value=mathml(source)
  marker_repairs={
   '6053:step-572517:521517':('80339e03930158a44b837001f5ab48c7e1cd42dad0725d651c9326323fd8d8f1',1),
   '6646:step-576872:91350':('168e2fbb607b979806f52f3aac0136f0f24a1f285f662600c4e7687d45ad54d4',4),
   '6663:step-576843:88652':('d89fdf1ebd653bab2b6f8db9fc485fd09e78fe5b6f536ae3aaddc4c9b4618308',4)}
  if record['id'] in marker_repairs:
   expected_hash,expected_count=marker_repairs[record['id']];assert digest(source)==expected_hash
   # These archived equations visibly retain malformed source [math] markers.
   # Original SVG confirms these exact failed markers are currency dollars.
   # Restore only that exact glyph sequence. Every operand,
   # equality, cancellation, percent, and final result stays source-derived.
   prefix=r'{\color{red}\text{\textbackslash{}[}} '
   failed=[prefix+'m a t h ]',prefix+'/ m a t h ]']
   assert sum(value.count(token) for token in failed)==expected_count
   for token in failed:value=value.replace(token,r'\$')
  if record['id']=='3428:step-182411:340346':
   assert digest(source)=='bbeddc3e9d075e843663cacac8422f074f66322bb0e943e651223fd7afc65d65'
   # The preceding source sentence defines A=\{0.2,0.5,0.99\}; this is
   # the same finite-set condition, with source-marker escaping lost.
   old_set=r'\in { 0.2,\, 0.5,\, 0.99 }';new_set=r'\in \{ 0.2,\, 0.5,\, 0.99 \}'
   assert value.count(old_set)==1
   value=value.replace(old_set,new_set)
  value=re.sub(r'\{(?=\{)', '{ ',value)
  out['tex']=value.strip()
  out['features']={'source_mathml':len(MML.findall(source)),'matrix_tables':source.count('<mtable'),'zero_rule_stacks':len(re.findall(r'linethickness="0(?:\.0+)?(?:px|pt|em|ex|%)?"',source)), 'source_phantoms':source.count('<mphantom'),'literal_percent':bool(re.search(r'(?<!\\)%',value))}
 except Exception as exc:out['errors']=[str(exc)]
 return out

if __name__=='__main__':
 p=ROOT/'reference/mathacademy/repairs/2026-10-16-import-root-cause/source/occurrences.jsonl'
 q=ROOT/'reference/mathacademy/repairs/2026-10-16-import-root-cause/database/secondary-source-backed-candidates.jsonl'
 ids={s['id'] for r in map(json.loads,q.open()) for s in r['source_occurrences']}
 rows=[convert_source(r) for r in map(json.loads,p.open()) if r['id'] in ids]
 dest=Path(__file__).with_name('conversions.jsonl');dest.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 from collections import Counter
 print(json.dumps({'occurrences':len(rows),'ok':sum(not r['errors'] for r in rows),'errors':dict(Counter(e for r in rows for e in r['errors']))},indent=2))
