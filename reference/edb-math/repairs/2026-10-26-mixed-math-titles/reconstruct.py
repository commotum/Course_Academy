"""Reconstruct a complete mixed SVG title without losing literal outer TeX."""
import re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'scripts'))
from bs4 import NavigableString,Tag
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex
class SourceRenderer(Renderer):
 def m(self,n):
  if isinstance(n,Tag)and n.name=='mrow':
   children=n.find_all(recursive=False)
   if len(children)in [2,3]and children[0].name=='mo'and children[0].get_text()=='{'and children[1].name=='mtable'and(len(children)==2 or children[2].name=='mo'and not children[2].get_text()):
    rows=[' & '.join(self.m(c)for c in row.find_all('mtd',recursive=False))for row in children[1].find_all('mtr',recursive=False)]
    return '\\begin{cases}'+' \\\\ '.join(rows)+'\\end{cases}'
  if isinstance(n,Tag)and n.name=='mstyle'and n.find('mphantom')and(n.has_attr('mathbackground')or n.has_attr('style')):
   background=n.get('mathbackground');border=n.get('style','').strip().rstrip(';');options=[]
   padded=n.find(recursive=False)
   if padded.name=='mpadded':
    match=re.fullmatch(r'(\d+)(pt|px|em|ex|in|cm|mm)',padded.get('lspace',''))
    if not match or padded.get('height')!='+'+match[0]or padded.get('depth')!='+'+match[0]or padded.get('width')!='+'+str(2*int(match[1]))+match[2]:raise ValueError('Unsupported decorated phantom padding')
    options.append(match[0]);body=''.join(self.m(c)for c in padded.children)
   elif padded.name=='mrow'and not border:body=''.join(self.m(c)for c in padded.children)
   else:raise ValueError('Unsupported decorated phantom container')
   if background:
    if not re.fullmatch(r'[A-Za-z]+|#[\da-fA-F]{3}(?:[\da-fA-F]{3})?',background):raise ValueError('Unsupported phantom background')
    options.append(background)
   if border:
    if not re.fullmatch(r'border:\s*\d+(?:pt|px|em|ex|in|cm|mm)\s+solid(?:\s+(?:[A-Za-z]+|#[\da-fA-F]{6}))?',border):raise ValueError('Unsupported phantom border')
    options.append(border)
   return '\\bbox['+','.join(options)+']{'+body+'}'
  if isinstance(n,Tag)and n.name=='menclose':
   notation=n.get('notation','longdiv');allowed={'longdiv','actuarial','radical','box','roundedbox','circle','left','right','top','bottom','updiagonalstrike','downdiagonalstrike','verticalstrike','horizontalstrike','madruwb','phasorangle'}
   if not set(notation.split())<=allowed:raise ValueError('Unsupported enclosure notation '+notation)
   return '\\enclose{'+notation+'}{'+''.join(self.m(c)for c in n.children)+'}'
  if isinstance(n,Tag)and n.name=='mphantom':return '\\phantom{'+''.join(self.m(c)for c in n.children)+'}'
  if isinstance(n,Tag)and n.name=='mspace':
   if any(n.get(a)not in [None,'0','0em','0pt']for a in ['height','depth']):raise ValueError('Nontrivial MathML space height/depth requires review')
   width=n.get('width')
   if width:
    if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:em|ex|px|pt|pc|in|cm|mm)',width):raise ValueError('Unsupported MathML space width '+width)
    return '\\hspace{'+width+'}'
  value=super().m(n)
  if isinstance(n,Tag)and n.get('mathvariant'):
   fonts={'normal':'mathrm','bold':'mathbf','italic':'mathit','bold-italic':'mathbfit','double-struck':'mathbb','script':'mathcal','monospace':'mathtt','sans-serif':'mathsf'}
   font=fonts.get(n['mathvariant'])
   if font is None:raise ValueError('Unsupported mathvariant '+n['mathvariant'])
   value='\\'+font+'{'+value+'}'
  if isinstance(n,Tag)and n.get('mathcolor'):
   color=n['mathcolor'];assert re.fullmatch(r'[A-Za-z]+|#[\da-fA-F]{6}',color)
   value='{\\color{'+color+'}{'+value+'}}'
  return value

def reconstruct(title):
 renderer=SourceRenderer(None);parts=[]
 for child in title.children:
  if isinstance(child,NavigableString):parts.append(str(child));continue
  if not isinstance(child,Tag):continue
  if child.name!='mjx-container':raise ValueError('Unsupported mixed-title child '+child.name)
  roots=child.select('mjx-assistive-mml math')
  if len(roots)!=1:raise ValueError('Expected exactly one complete fragment MathML root')
  parts.append(renderer.m(roots[0]))
 if renderer.errors:raise ValueError(renderer.errors)
 return normalize_source_tex(''.join(parts).strip())
