import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;ns={'__file__':str(H/'prepare_source_proposals.py')};exec((H/'prepare_source_proposals.py').read_text().split('options=collections')[0],ns);props={(r['entity'],r['attribute']):r for r in json.loads((H/'proposals.json').read_text())};resolved=[]
for r in json.loads((H/'source-proposal-unresolved.json').read_text()):
 key=(r['entity'],r['attribute']);before=ns['F'][key]['value'];old=ns['mathvalues'](before);sources=[s for s in ns['S']if(s['entity'],s['attribute'])==key and len(s['formulas'])==len(old)and all(ns['core'](x)==ns['core'](y)for x,y in zip(old,s['formulas']))];assert sources,key;variants={}
 for s in sources:
  ms=list(ns['MATH'].finditer(before));after=before;indices=[]
  for i in reversed(range(len(old))):
   y=s['formulas'][i]
   if not ns['role_missing'](old[i],y):continue
   m=ms[i];after=after[:m.start()]+('$$\n'+y+'\n$$'if m[0].startswith('$$')else'$'+y+'$')+after[m.end():];indices.append(i)
  variants[after]={'path':s['path'],'source_identity':s['source_identity'],'formula_indices':sorted(indices)}
 assert len(variants)==1,(key,len(variants));after,ev=next(iter(variants.items()));props[key]={'entity':key[0],'attribute':key[1],'before':before,'after':after,'reason':'Restore source font roles and instructional highlighting using the retained capture whose complete mathematical formula sequence matches the current owned explanation. Preserve the current teaching stages.','evidence':{**ev,'resolution':'Exact complete sequence match preferred over older archive stages or appended history formulas.','source_conflict_details':'source-conflict-details.json'},'confidence':'high'};resolved.append({'entity':key[0],'attribute':key[1],**ev,'classification':'resolved source presentation variant; no numeric/parameter change','all_matching_sources':[s['path']for s in sources]})
# This source-origin arity typo is mathematical notation, independently checked against its stated f(x,y,z).
key=(17592186179587,'question/worked-solution');r=props[key];assert r['after'].count('f(x,y)')==2;r['after']=r['after'].replace('f(x,y)','f(x,y,z)');r['reason']+=' Correct two source-origin function-arity labels to match the stated three-variable function.';r['evidence']['authored_math_correction']='completion-proofs/e-9487-arity.json'
proof={'entity':key[0],'source_identity':'e-9487','classification':'authored correction of source-origin mathematical notation','given_function':'f(x,y,z)=x^2+y-z','path':'r(t)=(-t,t+1,t-3), 0<=t<=1','independent_substitution':'f(r(t))=t^2+4','independent_speed':'sqrt(3)','integral_if_evaluated':'13*sqrt(3)/3','correction':'Only the two f(x,y) labels become f(x,y,z). Existing setup method and all calculations remain unchanged.'};(H/'completion-proofs/e-9487-arity.json').write_text(json.dumps(proof,indent=2))
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));(H/'source-conflict-resolutions.json').write_text(json.dumps(resolved,indent=2));(H/'source-proposal-unresolved.json').write_text('[]');print('source conflicts resolved',len(resolved),'content',len(props))
