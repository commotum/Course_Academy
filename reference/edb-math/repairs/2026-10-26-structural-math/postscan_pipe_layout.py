"""Recheck literal table serialization against the individually retained cases."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
retained={(d['entity'],d['attribute'],d['before'])for d in json.loads((H/'batch-05/reviewed-nonrepairs.json').read_text())};seen=set();unexpected=[];missing=[];count=0
for line in(W/'final.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v']
 if a not in {'question/worked-solution','question/problem','tutorial/content','answer/value'}or not isinstance(v,str)or'|'not in v and r'\right'not in v:continue
 if a=='answer/value'and re.search(r'\\(?:left|right|middle)\s*$',v):missing.append(d)
 for m in MATH.finditer(v):
  t=m[0];size=2 if t.startswith(('$$',r'\[',r'\('))else 1
  if re.search(r'\\(?:left|right|middle)\s*$',t[size:-size]):missing.append(d)
  s=re.sub(r'\\(?:mid|vert|lvert|rvert)(?![A-Za-z])','|',t)
  if not re.search(r'(?<!\\)\|',t)or r'\begin{'in t:continue
  if ';'in t or(re.search(r'\|\s*(?:=|<|>|\\le|\\ge|\\approx)',t)and len(re.findall(r'(?<!\\)\|',s))%2 and not re.search(r'\|\s*[_^]',s)):
   count+=1
   if(e,a,t)in retained:seen.add((e,a,t))
   else:unexpected.append({'entity':e,'attribute':a,'math':t})
manifest=json.loads((W/'final.manifest.json').read_text());assert manifest['basis_t']>=8666
report={'basis_t':manifest['basis_t'],'candidate_blocks':count,'reviewed_legitimate_blocks_verified':len(seen),'unreviewed_candidate_blocks':len(unexpected),'missing_terminal_delimiter_glyph_fields':len(missing)}
(H/'pipe-postscan-final.json').write_text(json.dumps(report,indent=2)+'\n');(H/'pipe-postscan-unreviewed.json').write_text(json.dumps(unexpected,indent=2)+'\n');print(json.dumps(report,indent=2));assert seen==retained and not unexpected and not missing
