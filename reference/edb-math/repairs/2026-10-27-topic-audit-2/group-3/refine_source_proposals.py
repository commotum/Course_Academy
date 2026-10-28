import json,re,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import MATH,validate_math_structure
H=Path(__file__).resolve().parent
# Load only pure definitions, avoiding preparation side effects.
code=(H/'prepare_source_proposals.py').read_text().split('options=collections.defaultdict(dict)')[0];exec(code)
props={(r['entity'],r['attribute']):r for r in json.loads((H/'proposals.json').read_text())}
for s in S:
 e,a=s['entity'],s['attribute'];text=props.get((e,a),{}).get('after',F[e,a]['value']);old=mathvalues(text)
 if len(old)==len(s['formulas']):continue
 changes={}
 for i,x in enumerate(old):
  candidates={y for y in s['formulas']if core(x)==core(y)and role_missing(x,y)and len(re.findall(FONT,y))+len(re.findall(r'\\[{}]',y))>len(re.findall(FONT,x))+len(re.findall(r'\\[{}]',x))}
  if len(candidates)==1:changes[i]=next(iter(candidates))
 for i in reversed(sorted(changes)):
  m=list(MATH.finditer(text))[i];text=text[:m.start()]+('$$\n'+changes[i]+'\n$$'if m[0].startswith('$$')else'$'+changes[i]+'$')+text[m.end():]
 if changes:propose(e,a,text,'Recover source font roles or visible set braces by unique equivalent formula match despite source control segmentation.',{'path':s['path'],'source_identity':s['source_identity'],'formula_indices':list(changes),'matching':'unique equivalent full source formula; do not infer source control outer formulas'})
e=17592186167994;a='tutorial/content';text=props.get((e,a),{}).get('after',F[e,a]['value']);r=next(s for s in S if s['entity']==e);ms=list(MATH.finditer(text));m=ms[2];after=text[:m.start()]+'$'+r['formulas'][2]+'$'+text[m.end():];propose(e,a,after,'Recover the original bold vector-valued function symbol.',{'path':r['path'],'source_formula_index':2,'source_notation':r'\boldsymbol{f}'})
# Bare arcsec/arccsc/arccot strings otherwise render as a product of italic letters.
for (e,a),f in F.items():
 text=props.get((e,a),{}).get('after',f['value']);pattern=r'(?<![a-zA-Z\\{])arc(sec|csc|cot)(?=[(0-9a-z])'
 transform=lambda t:re.sub(pattern,lambda m:r'\operatorname{arc'+m[1]+'} ',t)
 after=transform(text)if f['bare']else MATH.sub(lambda m:transform(m[0]),text)
 if after!=text:propose(e,a,after,'Restore upright inverse-trigonometric function roles in bare imported arcsec/arccsc/arccot spellings.',{'classification':'authored notation repair','supported_by':'Existing integral, canonical tutorial inverse-function convention, and preserved answer expression; numeric operands and branch convention unchanged.'})
# Root T9129 retained canonical prose answer and detached this duplicate. Repair only retained canonical typography.
detached=props.pop((17592186307410,'answer/value'),None)
if detached:
 canonical=17592186306650;before=F[canonical,'answer/value']['value'];after=detached['after'];validate_math_structure(after,bare_math=False);props[canonical,'answer/value']={**detached,'entity':canonical,'before':before,'evidence':{**detached['evidence'],'post_type_repair_transaction':9129,'retained_canonical_answer':True}}
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));print('proposals',len(props))
