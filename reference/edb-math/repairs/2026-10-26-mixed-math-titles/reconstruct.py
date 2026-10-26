"""Reconstruct a complete mixed SVG title without losing literal outer TeX."""
import re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'scripts'))
from bs4 import NavigableString,Tag
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex
class SourceRenderer(Renderer):
 def m(self,n):
  value=super().m(n)
  if isinstance(n,Tag)and n.name=='mstyle'and n.get('mathcolor'):
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
