import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import normalize_source_tex
D=json.loads((H/'source-differences.json').read_text())
def canon(s):
 s=normalize_source_tex(s)
 # Canonical comparison only; retained content is not rewritten this way.
 s=re.sub(r'\\(?:left|right)\s*','',s)
 s=re.sub(r'\{?\[\s*\{?\\begin\{array\}\{[clr]+\}([\s\S]*?)\\end\{array\}\s*\}?\]\s*\}?',lambda m:r'\begin{bmatrix}'+m[1]+r'\end{bmatrix}',s)
 s=re.sub(r'\{?\|\s*\{?\\begin\{array\}\{[clr]+\}([\s\S]*?)\\end\{array\}\s*\}?\|\s*\}?',lambda m:r'\begin{vmatrix}'+m[1]+r'\end{vmatrix}',s)
 s=re.sub(r'\\color\{[^{}]*\}','',s)
 # Invisible alignment and explicit spacing differences do not change values.
 def drop_group(m):
  start=m.start();i=m.end();depth=1
  while i<len(s)and depth:
   if s[i]=='\\':i+=2;continue
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return start,i
 for m in list(re.finditer(r'\\phantom\{',s))[::-1]:
  start,end=drop_group(m);s=s[:start]+s[end:]
 for _ in range(5):s=re.sub(r'\\(?:mathbf|mathit|mathrm|textrm|text|operatorname)\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\(?:displaystyle|textstyle|quad|qquad)\b|\\[,;!]|\\hspace\{[^{}]*\}','',s)
 s=s.replace(r'\times',r'\cdot').replace(r'\dfrac',r'\frac').replace('⁡','').replace('−','-').replace('⋯',r'\cdots').replace('⋮',r'\vdots').replace('…',r'\ldots').replace('↔',r'\leftrightarrow').replace('⇒',r'\Rightarrow')
 return re.sub(r'\s|[{}]','',s)

out=[];style=[]
for d in D:
 fs=d['source']['formulas'];ms=d['math']
 if len(fs)!=len(ms):out.append({**d,'differences':'count'});continue
 diffs=[{'index':i,'before':a,'after':b}for i,(a,b)in enumerate(zip(ms,fs))if canon(a)!=canon(b)]
 if diffs:out.append({**d,'differences':diffs})
 elif any(a!=b and(r'\color'in b or r'\mathbf'in b)for a,b in zip(ms,fs)):style.append(d)
(H/'semantic-differences.json').write_text(json.dumps(out,indent=2)+'\n');(H/'style-differences.json').write_text(json.dumps(style,indent=2)+'\n')
print('semantic',len(out),'style',len(style));print(collections.Counter(d['attribute']for d in out))
for d in out:
 if d['attribute']=='answer/value':continue
 print('\n',d['entity'],d['attribute'],d['identity'],d['math_count'],len(d['source']['formulas']))
 if d['differences']=='count':print('COUNT');continue
 for x in d['differences']:print(x['index'],repr(x['before'])[:260],'=>',repr(x['after'])[:260])
