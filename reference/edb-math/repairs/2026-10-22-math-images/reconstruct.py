"""Recover TeX from MathJax's retained semantic SVG tree; require render roundtrip."""
import collections,importlib.util,json,re,unicodedata
from pathlib import Path
from bs4 import BeautifulSoup,Tag
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22'
spec=importlib.util.spec_from_file_location('converter',ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/secondary/convert_source.py');conv=importlib.util.module_from_spec(spec);spec.loader.exec_module(conv)
conv.old.CAPTURE.MATHML_TEX_OPERATOR_NAMES.update({'sech','csch'})
FENCE={'239B':'(','239C':'(','239D':'(','239E':')','239F':')','23A0':')','23A1':'[','23A2':'[','23A3':'[','23A4':']','23A5':']','23A6':']','23A7':'{','23A8':'{','23A9':'{','23AA':'{','23AB':'}','23AC':'}','23AD':'}','23B7':'√','E001':'√'}
def glyphs(n):
 # MathJax builds a stretched arrow from an arrowhead and a clipped minus
 # glyph. They are drawing pieces of ONE mo, not two mathematical tokens.
 if stretched_right_arrow(n):return '→'
 parts=[FENCE.get(x['data-c'],chr(int(x['data-c'],16))) for x in n.find_all(['path','use'],attrs={'data-c':True})]
 if not parts:parts=[x.get_text() for x in n.find_all('text')]
 if parts and all(0xE150<=ord(c)<=0xE156 for c in parts):return '⏟' if n.parent.get('data-mml-node')=='munder' else '⏞'
 if len(parts)>1 and len(set(parts))==1 and parts[0] in '()[]{}|‖':parts=parts[:1]
 return ''.join(parts)
def stretched_right_arrow(n):
 if n.get('data-mml-node')!='mo':return False
 pieces=n.find_all(['path','use'],attrs={'data-c':True})
 return (len(pieces)==2 and [p['data-c'].upper() for p in pieces]==['2192','2212']
         and pieces[0].parent is n and pieces[1].parent.name=='svg'
         and pieces[1].parent.parent is n and pieces[1].parent.has_attr('viewbox'))
def children(n):
 out=[]
 for child in n.children:
  if not isinstance(child,Tag):continue
  if child.get('data-mml-node'):out.append(child)
  elif child.name=='g':out.extend(children(child))
 return out
def node(n,soup):
 name=n.get('data-mml-node');cs=children(n)
 if name in ('mi','mo','mn','mtext','text'):
  name='mtext' if name=='text' else name;m=soup.new_tag(name);text=glyphs(n)
  if name!='mtext':
   # Unicode mathematical alphabets explicitly identify the source font.
   values=[];styles=[]
   for c in text:
    uname=unicodedata.name(c,'');base=unicodedata.normalize('NFKD',c)
    if uname.startswith('MATHEMATICAL '):
     style='bold-italic' if 'BOLD ITALIC' in uname else 'bold' if 'BOLD' in uname else 'double-struck' if 'DOUBLE-STRUCK' in uname else 'script' if 'SCRIPT' in uname else 'fraktur' if 'FRAKTUR' in uname else 'sans-serif' if 'SANS-SERIF' in uname else 'monospace' if 'MONOSPACE' in uname else 'italic'
     styles.append(style);values.append(base)
    else:styles.append(None);values.append(c)
   text=''.join(values)
   style=set(styles)-{None}
   if len(style)>1:raise ValueError('Mixed mathematical font within token')
   if style:
    variant=next(iter(style))
    if variant=='bold-italic':text=glyphs(n) # exact mathematical Unicode is supported by the player
    elif variant!='italic':m['mathvariant']=variant
   elif name=='mi' and len(text)==1 and text.isalpha() and text not in 'ℝℕℚℤℂ':m['mathvariant']='normal'
  if name=='mo' and text in conv.old.CAPTURE.MATHML_TEX_OPERATOR_NAMES:m.name='mi'
  m.string=text
  if stretched_right_arrow(n):m['stretchy']='true'
 elif name=='mspace':m=soup.new_tag('mspace')
 elif name=='mphantom':m=soup.new_tag('mphantom')
 else:
  name='mrow' if name=='TeXAtom' else name
  if name=='mpadded':name='mrow' # spacing only; visible content still roundtrips
  m=soup.new_tag(name)
  if name=='msqrt':
   # SVG adds a generated radical glyph after the radicand; TeX supplies it.
   cs=[c for c in cs if not(c.get('data-mml-node')=='mo' and glyphs(c)=='√')]
  if name=='mroot':
   # Inspect and fail closed if ordering differs; handled after roundtrip.
   cs=[c for c in cs if not(c.get('data-mml-node')=='mo' and glyphs(c)=='√')]
  if name=='msubsup':
   # SVG output orders the upper script before the lower script.
   if len(cs)!=3:raise ValueError('Invalid SVG msubsup arity')
   cs=[cs[0],cs[2],cs[1]]
  if name=='menclose':
   lines=n.find_all('line',recursive=False)
   notation=[]
   for l in lines:
    dx=float(l.get('x2',0))-float(l.get('x1',0));dy=float(l.get('y2',0))-float(l.get('y1',0))
    if dx and dy:notation.append('updiagonalstrike' if dx*dy>0 else 'downdiagonalstrike')
    else:raise ValueError('Non-diagonal enclosure requires source recovery')
   if not notation:raise ValueError('Missing enclosure lines')
   m['notation']=' '.join(notation)
  if name=='mfrac' and not n.find('rect',recursive=False):m['linethickness']='0'
  if name=='mtable':
   rules=[x for x in n.children if isinstance(x,Tag) and x.name in ('line','rect')]
   if rules:
    if len(rules)!=2 or [x.get('data-line') for x in rules]!=['v','h']:raise ValueError('Table rule geometry requires source recovery')
    # This source has one divider between its two columns and one below its header.
    m['columnlines']='solid';m['rowlines']='solid '+' '.join('none' for _ in cs[1:])
    for row in cs:
     cells=children(row)
     while cells and not glyphs(cells[-1]) and not children(cells[-1]):cells[-1].decompose();cells.pop()
  for c in cs:m.append(node(c,soup))
 bg=n.find('rect',attrs={'data-bgcolor':True},recursive=False)
 if bg:m['mathbackground']=bg.get('fill')
 # Preserve instructional foreground colors.
 color=n.get('fill') or n.get('color') or n.get('stroke')
 if color and color not in ('currentColor','none','inherit','black','#000000'):m['mathcolor']=color
 return m

def main():
 source=json.loads((RAW/'repair-source-svgs.json').read_text());missing=json.loads((HERE/'unmatched-assets.json').read_text());
 if (HERE/'remaining-assets.json').exists():missing=sorted(set(missing)|set(json.loads((HERE/'remaining-assets.json').read_text())))
 if (HERE/'reconstructed-candidates.json').exists():missing=sorted(set(missing)|set(json.loads((HERE/'reconstructed-candidates.json').read_text())))
 out={};errors=[]
 for path in missing:
  soup=BeautifulSoup(source[path],'html.parser');math=soup.find(attrs={'data-mml-node':'math'})
  if not math:continue
  try:
   result=node(math,soup);tex=conv.mathml(str(result))
   tex=re.sub(r'\\(int|iint|iiint) _',lambda m:'\\'+m[1]+'\\limits _',tex)
   if 'data-c="2C6"' in source[path]:tex=tex.replace('\\hat{','\\widehat{')
   out[path]={'tex':tex,'method':'retained-svg-semantic-tree','mathml':str(result)}
  except Exception as exc:errors.append({'path':path,'error':str(exc)})
 (HERE/'reconstructed-candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');(HERE/'reconstruction-errors.json').write_text(json.dumps(errors,indent=2)+'\n')
 print('candidates',len(out),'errors',collections.Counter(r['error'] for r in errors))
if __name__=='__main__':main()
