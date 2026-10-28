import json,re,sys,collections
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import MATH,normalize_source_tex
H=Path(__file__).resolve().parent;S=json.loads((H/'source-records.json').read_text());F={(f['entity'],f['attribute']):f for f in json.loads((H/'fields.json').read_text())}
def texs(v):return [m[0][2:-2]if m[0].startswith(('$$',r'\[',r'\('))else m[0][1:-1]for m in MATH.finditer(v)]
def nums(v):
 v=re.sub(r'\\(?:hspace|vspace|kern|mkern)\{[^{}]*\}|\\(?:phantom)\{[^{}]*\}', '', v)
 return re.findall(r'(?<![A-Za-z])\d+(?:\.\d+)?',v)
out=[]
for s in S:
 f=F[(s['entity'],s['attribute'])];old=texs(f['value']);new=s['formulas']
 diffs=[{'index':i,'old':x,'source':y,'same_numbers':nums(x)==nums(y)}for i,(x,y)in enumerate(zip(old,new))if re.sub(r'\s+','',x)!=re.sub(r'\s+','',y)]
 out.append({k:v for k,v in s.items()if k not in ('html','formulas')}|{'stored':len(old),'source':len(new),'number_equal':nums(' '.join(old))==nums(' '.join(new)),'diffs':diffs})
(H/'source-differences.json').write_text(json.dumps(out,indent=2))
for x in out:
 if x['attribute']=='tutorial/content':
  print('\n',x['entity'],'COUNTS',x['stored'],x['source'],'NUMBERS',x['number_equal'])
  for d in x['diffs']:print(d['index'],'OLD',d['old'][:600],'SOURCE',d['source'][:600])
