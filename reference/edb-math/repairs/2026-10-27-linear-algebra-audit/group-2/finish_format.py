import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,validate_math_structure,validate_tex
helper=(H/'propose_format.py').read_text();exec(helper[helper.index('def neutral(s):'):helper.index('props=[];proof=[]')]);props=json.loads((H/'proposals.json').read_text());fields=json.loads((H/'fields.json').read_text());sources=json.loads((H/'sources.json').read_text());src=collections.defaultdict(list)
for s in sources:src[s['identity'],s['attribute']].append(s)
def put(e,a,before,after,reason,evidence):
 if before==after:return
 p=next((p for p in props if p['entity']==e and p['attribute']==a),None)
 if p:p['after']=after;p['reason']+=','+reason;p['evidence']=p['evidence']+[evidence]if isinstance(p['evidence'],list)else[p['evidence'],evidence]
 else:props.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':reason,'evidence':evidence,'confidence':'high'})
for e,a,original,ident,bare in fields:
 p=next((p for p in props if p['entity']==e and p['attribute']==a),None);v=p['after']if p else original
 # The current dimension importer used a scalar dot where the retained source uses the ordered row/column symbol.
 pattern=r'\$((?:\{?\d+\}?|n)\s*)\\cdot\s*((?:\{?\d+\}?|n))\$(?=\s+(?:identity\s+)?matri(?:x|ces))'
 after=re.sub(pattern,lambda m:'$'+m[1]+r'\times '+m[2]+'$',v)
 if after!=v:put(e,a,original,after,'matrix-dimension-notation',{'identity':ident,'source_paths':sorted({s['path']for s in src[ident,a if a!='answer-field/key'else'question/problem'] if any(isinstance(t,str)and r'\times'in t for t in s['formulas'])}),'review':'Only ordered dimensions immediately qualifying matrix/matrices/identity matrix.'});v=after
 if a!='answer-field/key':continue
 matches=list(MATH.finditer(v));edits=[]
 for i,m in enumerate(matches):
  old=m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1];options=[]
  for s in src[ident,'question/problem']:
   for new in s['formulas']:
    if not isinstance(new,str)or neutral(new)!=neutral(old):continue
    flags=[]
    if r'\{'in new and r'\{'not in old:flags.append('visible-set-braces')
    if r'\mathbb'in new and r'\mathbb'not in old:flags.append('real-number-domain-font')
    if r'\mathbf'in new and r'\mathbf'not in old:flags.append('source-vector-notation')
    if flags:options.append((source_tex(old,new),flags,s['path']))
  unique={o[0]:o for o in options}
  if len(unique)==1:edits.append((i,*next(iter(unique.values()))))
 after=v
 for i,new,flags,path in sorted(edits,reverse=True):
  m=matches[i];after=after[:m.start()]+'$'+new+'$'+after[m.end():]
 if after!=v:put(e,a,original,after,'source-checkbox-statement-notation',{'identity':ident,'source_math_edits':[{'index':i,'after':new,'features':flags,'path':path}for i,new,flags,path in edits]})
# One migrated checkbox solution repeats statement II's label before evaluating statement III.
e=17592186120427;a='question/worked-solution';original=next(f[2]for f in fields if f[:2]==[e,a]);p=next((p for p in props if p['entity']==e and p['attribute']==a),None);v=p['after']if p else original
needle='- Statement $2\\text{det}({A}^{T})=25$ is false. We have\n\n$$\n\\text{det}(A)-3\\text{det}(I)'
replacement='- Statement $\\text{det}(A)-3\\text{det}(I)=8$ is false. We have\n\n$$\n\\text{det}(A)-3\\text{det}(I)'
assert v.count(needle)==1;after=v.replace(needle,replacement);put(e,a,original,after,'mismatched-third-statement-label',{'source_identity':'q-42468','derived':'det(A)-3det(I)=5-3=2, so the third statement is false; current label incorrectly repeats the second statement.'})
for p in props:
 validate_math_structure(p['after']);assert re.findall(r'\{\{[^{}]+\}\}',p['before']or'')==re.findall(r'\{\{[^{}]+\}\}',p['after']),p['entity']
(H/'proposals.json').write_text(json.dumps(props,indent=2)+'\n');print('proposed fields',len(props),collections.Counter(p['attribute']for p in props))
