"""Reconstruct a complete mixed SVG title without losing literal outer TeX."""
import re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'scripts'))
from bs4 import NavigableString,Tag
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex
class SourceRenderer(Renderer):
 def m(self,n):
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
