"""Use immutable source column declarations, not the damaged matrix conversion."""
import json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts/question_capture'));from math_format import MATH,normalize_math_boundaries,source_multiplication_tex

def blocks(text):
 out=[];offset=0
 while (start:=text.find('[MATH:',offset))>=0:
  depth,end=1,start+6
  while depth and end<len(text):depth+=(text[end]=='[')-(text[end]==']');end+=1
  assert not depth;body=text[start+6:end-1].strip()
  if re.search(r';\s*[×⋅]\|\d',body):out.append(body)
  offset=end
 return out

def repair_arithmetic(entity,attribute,before):
 example={17592186138213:15667,17592186203769:15668}[entity];data=json.loads((HERE/f'arithmetic-source-{example}.json').read_text());kind='example_question' if attribute=='question/problem' else 'example_explanation';section=next(s for s in data['sections'] if s['section_type']==kind);decls=blocks(section['readable_text']);spans=[m for m in MATH.finditer(before) if m[0].startswith('$$')];assert len(decls)==len(spans),(entity,attribute,len(decls),len(spans));after=before
 for match,body in reversed(list(zip(spans,decls))):after=after[:match.start()]+'$$\n'+source_multiplication_tex(body)+'\n$$'+after[match.end():]
 return normalize_math_boundaries(after)
