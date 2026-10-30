import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());src=json.loads((H/'source-inventory.json').read_text());pat=re.compile(r'\$\$([\s\S]*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)')
def norm(t):
 t=re.sub(r'\\bbox\[[^\]]*\]|\\color(?:\[[^\]]*\])?\{[^{}]*\}|\\enclose\{[^{}]*\}', '',t);t=t.replace(r'\begin{vmatrix}',r'\begin{array}').replace(r'\end{vmatrix}',r'\end{array}');t=re.sub(r'(\\begin\{array\})\{[clr]+\}',r'\1',t);t=t.replace(r'\{','').replace(r'\}','').replace(r'\Rightarrow','⇒')
 t=re.sub(r'\\(?:hspace|vspace)\{[^{}]*\}','',t);t=re.sub(r'\\(?:mathbf|mathbb|mathrm|mathit|mathsf|mathcal|displaystyle|textstyle|left|right|big|Big|bigg|Bigg)\b','',t);t=t.replace('\\cdot','⋅').replace('\\times','×').replace('\\infty','∞').replace('\\in','∈').replace('\\langle','⟨').replace('\\rangle','⟩').replace('\\Pi','Π').replace('\\pi','π').replace('\\lambda','λ').replace('\\alpha','α').replace('\\beta','β').replace('\\leq','≤').replace('\\le','≤').replace('\\geq','≥').replace('\\ge','≥').replace('\\neq','≠').replace('\\ne','≠');t=re.sub(r'\\[,;! ]|\\quad\b|\\qquad\b','',t);return re.sub(r'[\s{}.,?]','',t).replace('\\{','').replace('\\}','')
changes=[];evidence=[];unmatched=[]
for q in S['questions']:
 mid=q.get(':question/math-academy-id');ss=src.get(mid,[])
 for attr in ['question/problem','question/worked-solution']:
  before=q.get(':'+attr)
  if not before:continue
  ms=list(pat.finditer(before));current=[(m[1]if m[1]!=None else m[2]).strip()for m in ms];candidates=[(v,v['parts'][attr])for v in ss if attr in v['parts']and not v['parts'][attr]['errors']and len(v['parts'][attr]['formulas'])==len(current)]
  eligible=[]
  for path,part in candidates:
   diffs=[(c,t)for c,t in zip(current,part['formulas'])if norm(c)!=norm(t)]
   if not diffs:eligible.append((path,part))
  if eligible:
   v,p=eligible[0];after=before
   for m,tex in reversed(list(zip(ms,p['formulas']))):
    # Keep exact existing spacing/layout where source typography is already complete.
    if m[1] is not None:replacement='$$\n'+tex+'\n$$'
    else:replacement='$'+tex+'$'
    after=after[:m.start()]+replacement+after[m.end():]
   if after!=before:
    changes.append({'entity':q[':db/id'],'attribute':attr,'before':before,'after':after,'reason':'Restore complete archived source math typography and TeX from one-to-one semantically matching formula fragments; preserve prompt prose, diagrams, controls, and mathematical values.'});evidence.append({'entity':q[':db/id'],'attribute':attr,'source_path':v['path'],'formulas':len(ms),'normalized_formula_pairs_equal':True})
  elif candidates:unmatched.append({'entity':q[':db/id'],'identity':mid,'attribute':attr,'diffs':[(c,t)for c,t in zip(current,candidates[0][1]['formulas'])if norm(c)!=norm(t)],'path':candidates[0][0]['path']})
(H/'source-proposals.json').write_text(json.dumps(changes,indent=2)+'\n');(H/'source-restoration-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');(H/'source-unmatched.json').write_text(json.dumps(unmatched,indent=2)+'\n');print('restoration proposals',len(changes),'unmatched candidates',len(unmatched));print([(x['identity'],x['attribute'],x['diffs'][:1])for x in unmatched])
