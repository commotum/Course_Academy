"""Individually checked visual issues missed by merror-only checks."""
import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());src=json.loads((H/'sources.json').read_text());F=json.loads((H/'fields.json').read_text())
def put(e,a,before,after,reason,evidence):
 if before==after:return
 p=next((p for p in P if p['entity']==e and p['attribute']==a),None)
 if p:p['after']=after;p['reason']+=','+reason;p.setdefault('additional_evidence',[]).append(evidence)
 else:P.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':reason,'evidence':evidence})
# This proof imported nested math commands inside \text; MathJax rendered those commands literally without merror.
q=next(q for q in D['questions']if q[':db/id']==17592186184065)
for a in ['question/problem','question/worked-solution']:
 original=q[':'+a];p=next((p for p in P if p['entity']==q[':db/id']and p['attribute']==a),None);current=p['after']if p else original;ss=next(s for s in src if s['identity']=='e-4792'and s['attribute']==a and'/DATA/Lessons/'in s['path']);ms=list(MATH.finditer(current));index=0 if a.endswith('worked-solution')else 4;assert len(ss['formulas'])==len(ms);m=ms[index];new=ss['formulas'][index];assert r'\begin{aligned}'in new;after=current[:m.start()]+'$$\n'+new+'\n$$'+current[m.end():];put(q[':db/id'],a,original,after,'source-restoration-math-outside-text',{'source_path':ss['path'],'formula_index':index,'proof':'Same w+w=w cancellation proof and A2/A3 missing labels; math symbols and colored axiom names moved out of prose text macros exactly as retained source DOM.'})
# Text answer values can themselves contain malformed mathematical set notation.
for e,a,original,ident,bare in F:
 if a!='answer/value'or bare:continue
 p=next((p for p in P if p['entity']==e and p['attribute']==a),None);current=p['after']if p else original;after=current.replace(r'\text{{}',r'\left\{').replace(r'\text{}}',r'\right\}')
 if after!=current:put(e,a,original,after,'display-only-visible-set-delimiters-in-text-answer',{'identity':ident,'source_paths':sorted({s['path']for s in src if s['identity']==ident and s['attribute']=='answer/value'}),'proof':'The answer remains the identical assertion that the same named vector set is not a column-space basis. Only malformed text-macro braces become visible math set fences; vector indices/order, sentence, identity, bank and correct link are unchanged.'})
# Plain det/Null/Col used as math identifiers lost their operator role during extraction.
for e,a,original,ident,bare in F:
 if bare or a not in ['tutorial/content','question/problem','question/worked-solution','answer-field/key']:continue
 p=next((p for p in P if p['entity']==e and p['attribute']==a),None);current=p['after']if p else original;after=current
 for m in reversed(list(MATH.finditer(current))):
  tex=m[0];new=re.sub(r'(?<![\\A-Za-z])det\(',lambda _:r'\det(',tex);new=re.sub(r'(?<![\\A-Za-z])(?:Null|Col)\(',lambda z:r'\operatorname{'+z[0][:-1]+'}(',new)
  if new!=tex:after=after[:m.start()]+new+after[m.end():]
 put(e,a,original,after,'source-operator-role',{'identity':ident,'proof':'det is the determinant function, and Null/Col denote the named null/column spaces; use upright operator commands, preserving every argument and value.'})
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'answer-display-proposals.json').write_text(json.dumps([p for p in P if p['attribute']=='answer/value'and'display-only'in p['reason']],indent=2)+'\n');print('Proposals',len(P))
