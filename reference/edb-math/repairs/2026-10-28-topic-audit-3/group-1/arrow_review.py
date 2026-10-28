import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,validate_math_structure
D=json.loads((H/'current.json').read_text());by={q[':db/id']:q for q in D['questions']};props=json.loads((H/'source-reviewed-proposals.json').read_text());pby={(p['entity'],p['attribute']):p for p in props};checks=[]
for row in json.loads((H/'comparison.json').read_text()):
 if row['identity']not in['q-1323','q-1386']or row['attribute']!='question/problem':continue
 src=row['best'];assert src and len(src['formulas'])==len(row['current']);changes=[]
 for i,(old,new)in enumerate(zip(row['current'],src['formulas'])):
  if '^(→)'not in old:continue
  assert r'\overset{\to'in new
  changes.append({'index':i,'before_tex':old,'after_tex':new,'independent_check':'Restore observed source vector arrow rather than an accidental superscript parenthesis/arrow. Same vector letters, components, operation and scalar factors; independent component calculation in authored-completion-proofs.json.'})
 p=pby.get((row['entity'],row['attribute']))
 if not p:p={'entity':row['entity'],'attribute':row['attribute'],'before':by[row['entity']][':'+row['attribute']],'after':None,'reason':'Restore genuine source vector-arrow notation lost into literal AsciiMath-like superscripts.','evidence':{'basis_t':9837,'identity':row['identity'],'source_path':src['path'],'formula_changes':[]},'confidence':'high'};props.append(p)
 p['evidence']['formula_changes']+=changes;checks.append({'identity':row['identity'],'source_path':src['path'],'changes':changes})
for p in props:
 spans=list(MATH.finditer(p['before']));after=p['before']
 for ch in sorted(p['evidence']['formula_changes'],key=lambda x:x['index'],reverse=True):
  m=spans[ch['index']];display=m[0].startswith(('$$',r'\[',r'\('));wrapped='$$\n'+ch['after_tex']+'\n$$'if display else'$'+ch['after_tex']+'$';after=after[:m.start()]+wrapped+after[m.end():]
 p['after']=after;validate_math_structure(after)
q=by[17592186059526];before=q[':question/worked-solution'];after=re.sub(r'([ab])\^\(→\)',lambda m:r'\vec{'+m[1]+'}',before);assert after!=before;assert 21==-3+6*4 and 32==2+6*5
extra=[{'entity':q[':db/id'],'attribute':'question/worked-solution','before':before,'after':after,'reason':'Use the vector-arrow notation already defined in this example instead of malformed literal superscript arrows.','evidence':{'basis_t':9837,'identity':'e-4295','classification':'Authored notation consistency repair; original HTML unavailable','full_problem':q[':question/problem'],'independent_math':'Actual retained graph visually shows a=(−3,2),b=(4,5). Thus a+6b=(21,32), preserving every existing arithmetic step. Problem and first two solution equations already use vec{a},vec{b}.','source_image':'images/56/56b10e759084da6fb21c8421bc9ff6d74aac2602df28f6c8e478bd874d7d6e9f.png','repair_scope':'Only two vector-symbol annotations; graph, coordinates, operation, worked arithmetic and IDs unchanged.'},'confidence':'high'}]
(H/'source-reviewed-proposals.json').write_text(json.dumps(props,indent=2)+'\n');(H/'arrow-notation-proposals.json').write_text(json.dumps(extra,indent=2)+'\n');(H/'arrow-notation-proof.json').write_text(json.dumps({'source_restorations':checks,'authored_consistency':extra[0]['evidence']},indent=2)+'\n');print('source-arrowfields',len(checks),'authored',len(extra))
