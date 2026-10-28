import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;P=json.loads((H/'proposals.json').read_text());F=json.loads((H/'fields.json').read_text());count=0;affected=[]
pattern=re.compile(r'(\\begin\{aligned\})(?=\s*\[(?!\s*[tbc]\s*\]))')
for e,a,original,ident,bare in F:
 p=next((p for p in P if p['entity']==e and p['attribute']==a),None);v=p['after']if p else original;after=pattern.sub(lambda m:m[1]+'{}',v)
 if after==v:continue
 evidence={'source_identity':ident,'reproducer':r'\begin{aligned}[A\,|\,I] &= \begin{bmatrix}1&0&1&0\\0&1&0&1\end{bmatrix}\end{aligned}','source_semantics':'The visible augmented-matrix label is a math operand. MathJax silently consumes it as the optional aligned positioning argument; an empty group ends the optional-argument scan. Genuine [t], [b], [c] placement is retained.','visual_evidence':'screens/17592186116501-tutorial-content-before.png and revised after screenshot'}
 if p:p['after']=after;p['reason']+=',visible-leading-aligned-bracket';p['evidence']=p['evidence']+[evidence]if isinstance(p['evidence'],list)else[p['evidence'],evidence]
 else:P.append({'entity':e,'attribute':a,'before':original,'after':after,'reason':'visible-leading-aligned-bracket','evidence':evidence,'confidence':'high'})
 count+=1;affected.append([e,a])
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'aligned-prefix-candidates.json').write_text(json.dumps(affected,indent=2)+'\n');print('protected',count,'fields;total proposed',len(P))
