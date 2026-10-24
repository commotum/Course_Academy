import json,re,collections
from pathlib import Path
H=Path('reference/edb-math/repairs/2026-10-23-tex-boundaries');P=Path('.local/edb/tex-boundary-current.jsonl')
math=re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')
prose={'question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions'}
items={};environments=collections.Counter();flags=collections.Counter()
for r in map(json.loads,P.open()):
 if r['a'] not in prose or not isinstance(r['v'],str):continue
 s=r['v'];outside=math.sub(lambda m:' '*len(m[0]),s);bad=[]
 for m in re.finditer(r'\\(?:begin|end)\{([^{}]+)\}',outside):
  environments[m[1]]+=1;bad.append({'kind':'bare-environment','start':m.start(),'text':m[0]})
 for m in re.finditer(r'\\(?:eqalign|matrix|cases|pmatrix|displaylines|halign|eqalignno|leqalignno)\b',outside):bad.append({'kind':'bare-layout-command','start':m.start(),'text':m[0]})
 for m in re.finditer(r'\\\[[ \t]*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:pt|em|ex|cm|mm)\]',s):
  if m.start()==0 or s[m.start()-1]!='\\':bad.append({'kind':'single-slash-spacing','start':m.start(),'text':m[0]})
 for m in re.finditer(r'(?m)^(?: {4}|\t).*(?:\\(?:frac|begin|dfrac)|\$)',s):bad.append({'kind':'indented-math','start':m.start(),'text':m[0][:150]})
 if bad:
  r={**r,'flags':bad};items[r['e'],r['a']]=r
for r in items.values():flags.update({f['kind'] for f in r['flags']})
(H/'inventory.json').write_text(json.dumps(list(items.values()),indent=2,ensure_ascii=False)+'\n');print('fields',len(items),'flags',flags,'environments',environments)
for r in list(items.values())[:8]:print(r['e'],r['a'],[x['text'] for x in r['flags'][:4]])
