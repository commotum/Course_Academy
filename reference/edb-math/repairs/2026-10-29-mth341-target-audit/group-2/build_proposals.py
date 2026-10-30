import collections,copy,json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import matrices
sys.path.insert(0,str(H.parents[4]/'scripts'));from question_capture.math_format import MATH,ENV,environment,cells,matrix_tex,validate_math_boundaries,validate_matrix_layouts,validate_math_structure
S=json.loads((H/'current.json').read_text());original={};objects={}
def index(o):
 if isinstance(o,list):
  for x in o:index(x)
 elif isinstance(o,dict):
  if ':db/id'in o:objects.setdefault(o[':db/id'],{}).update(o);original.update({(o[':db/id'],k):v for k,v in o.items()if not isinstance(v,(list,dict))})
  for v in o.values():index(v)
index(S);current=dict(original);reasons=collections.defaultdict(list);evidence=[]
def setv(e,attr,value,reason):
 key=(e,':'+attr);current[key]=value;reasons[key].append(reason)
for name in['decoration-proposals','layout-proposals','completion-proposals','full-formula-proposals']:
 for p in json.loads((H/(name+'.json')).read_text()):setv(p['entity'],p['attribute'],p['after'],p['reason'])
def edit_matrix(e,predicate,transform,reason):
 key=(e,':question/worked-solution');text=current[key];matches=[m for m in matrices(text)if predicate(m['matrix'])];assert len(matches)==1,(e,len(matches));m=matches[0];a=m['matrix'];b=transform(a.copy());body=r' \\ '.join(' & '.join(sp.latex(c)for c in row)for row in b.tolist());env=m['environment'];cols=''
 if env=='array':
  cols=re.match(r'\s*\{[^{}]+\}',text[environment(text,m['start'])[0]:])[0]
 replacement='\\begin{'+env+'}'+cols+body+'\\end{'+env+'}';setv(e,'question/worked-solution',text[:m['start']]+replacement+text[m['end']:],reason);evidence.append({'question':e,'before_matrix':a.tolist(),'after_matrix':b.tolist(),'proof':reason})
def changed(a,i,j,v):a[i,j]=v;return a
edit_matrix(17592186338749,lambda a:a.shape==(3,3)and a[0,1]==-2,lambda a:changed(a,0,1,2),'Correct the repeated 3×3 minor: delete row 1 and column 3 of the original matrix; its first row is (1,2,-1). The zero middle row entry makes the determinant coincidentally unchanged.')
for e in[17592186338751,17592186371077]:
 q=objects[e];root=matrices(q[':question/problem'])[0]['matrix'];edit_matrix(e,lambda a:a.shape==(4,4)and a!=root,lambda a:root,'Correct the concluding determinant to repeat the prompt matrix. Exact cofactors and numeric conclusion already agree with the prompt; the printed concluding matrix was copied incorrectly.')
edit_matrix(17592186269208,lambda a:a.shape==(4,8)and a[3,7]==0,lambda a:changed(a,3,7,1),'R4 := R4 - 2R2 preserves the final augmented entry 1 because R2 has final entry 0. Verify E*A equals the displayed left block.')
edit_matrix(17592186269210,lambda a:a.shape==(4,8)and a[3,3]==0,lambda a:changed(a,3,3,1),'The initial augmented matrix must repeat A from the prompt: its (4,4) entry is 1. R2 := R2 + R1 does not alter row 4.')
edit_matrix(17592186269210,lambda a:a.shape==(4,8)and a[3,5]==3,lambda a:changed(a,3,5,0),'R1 := R1 + 2R3 changes only row 1; the final row of the augmented right block remains (0,0,0,1). Both inverse products equal I.')
edit_matrix(17592186402002,lambda a:a.shape==(2,2)and a[1,1]==1 and a[0,0]==-1,lambda a:changed(a,1,1,-1),'The final augmented right block and inverse formula give D^-1=[[-1,1],[2,-1]]. The printed conclusion had +1 in entry (2,2); both inverse products verify -1.')
edit_matrix(17592186660326,lambda a:a.shape==(4,8)and a[3,5]==3,lambda a:changed(a,3,5,0),'R3 := R3 - 5R2 changes only row 3; row 4 remains (0,0,0,1 | 0,0,0,1). Both inverse products verify the existing correct inverse and -34 key.')
e=17592186442272
old=current[(e,':question/worked-solution')];wrong=r'+(5+\lambda )';right=r'-(5+\lambda )';assert old.count(wrong)==1
setv(e,'question/worked-solution',old.replace(wrong,right),'Correct the third cofactor contribution: a13=-1 multiplies minor determinant 5+lambda, so this term is -(5+lambda). The previous + sign made the expanded line disagree with the determinant and the subsequent polynomial.')
evidence.append({'question':e,'before_term':wrong,'after_term':right,'proof':'The first-row terms are (3-lambda)*(lambda^2+5lambda), +(-5-lambda), and -(5+lambda). Their sum is -lambda^3-2lambda^2+13lambda-10, agreeing with det(A-lambda I), the next line, and the existing eigenvalue key {-5,1,2}.'})
# The archived radio bank contains equivalent evaluated values because M43=0.
e=17592186370926
prompt=current[(e,':question/problem')]
new='Which expression is the unsimplified cofactor expansion along the $3$rd column? Retain a term for each nonzero entry of that column, with the sign supplied by $(-1)^{i+j}$, even if a minor has determinant $0$.\n\n'+prompt.replace('=\n$$','\n$$')
setv(e,'question/problem',new,'Disambiguate three numerically equivalent choices by asking for the unsimplified source cofactor expansion with both nonzero-entry terms and their cofactor signs; preserve the existing bank and correct identity.')
evidence.append({'question':e,'numerically_equivalent_answer_ids':[17592186370929,17592186370930,17592186370932],'M43':0,'M23':12,'unchanged_correct_answer':17592186370930,'proof':'Column 3 has entries 0,sqrt(2),0,sqrt(3). Both nonzero terms have negative cofactor signs. Only the keyed option retains both such terms and signs; all three evaluate to -12 sqrt(2) because M43=0.'})
# Preserve the source vertical separator between A and the transformed identity.
augmented_repairs=[]
for key,text in list(current.items()):
 e,attr=key
 if attr not in[':question/problem',':question/worked-solution',':tutorial/content']or not isinstance(text,str):continue
 edits=[]
 for m in ENV.finditer(text):
  if m[1]!='begin'or m[2]!='bmatrix':continue
  span=environment(text,m.start());body=text[span[0]:span[1]];grid=cells(body)
  if len(grid)in[2,4]and all(len(row)==2*len(grid)for row in grid):
   n=len(grid);replacement=r'\left[\begin{array}{'+'c'*n+'|'+'c'*n+'}'+body+r'\end{array}\right]';edits.append((m.start(),span[2],replacement))
 new=text
 for a,b,v in reversed(edits):new=new[:a]+v+new[b:]
 if new!=text:setv(e,attr[1:],new,'Restore the archived vertical separator between the coefficient and identity blocks of each augmented matrix.');augmented_repairs.append({'entity':e,'attribute':attr[1:],'source_augmented_separators_restored':len(edits)})
(H/'augmented-separator-evidence.json').write_text(json.dumps(augmented_repairs,indent=2)+'\n')
# Normalize operator semantics and repair the aligned optional-argument trap.
for key,value in list(current.items()):
 e,attr=key
 if attr not in[':question/problem',':question/worked-solution',':tutorial/content',':answer/value',':answer-field/key']or not isinstance(value,str):continue
 new=value;new=re.sub(r'\\begin\{aligned\}(?=\[)',r'\\begin{aligned}{}',new);new=new.replace('\ufeff','')
 # Source scalar emphasis and math fonts are preserved above; det is a math operator.
 def mathfix(m):
  t=m[0];t=re.sub(r'\\(?:textrm|mathrm|text)\{det\}',r'\\det',t);t=re.sub(r'(?<![A-Za-z\\])det(?=\s*\(|\s*\\begin|\s*\\left)',r'\\det',t);return t
 bare=attr==':answer/value'and objects[e].get(':answer/type',{}).get(':db/ident')==':answer.type/math'
 new=mathfix(re.match(r'[\s\S]*',new))if bare else MATH.sub(mathfix,new)
 if attr==':answer/value'and not bare and new.startswith('det\\begin')and'$'not in new:new='$\\'+new+'$'
 if attr==':question/worked-solution'and e in{q for t,k,q in S['links']if t==17592186050376}:new=new.replace('$x=',r'$\lambda =')
 if e==17592186115851 and attr==':question/problem':new=new.replace('$2 \\cdot 2$','$2\\times2$')
 if new!=value:setv(e,attr[1:],new,'Preserve proper determinant-operator typesetting and protect the initial literal bracket in aligned; remove invisible capture BOM characters where present.')
proposals=[]
for key,after in sorted(current.items()):
 before=original.get(key)
 if before==after:continue
 e,a=key
 if a not in[':question/problem',':question/worked-solution',':tutorial/content',':answer/value',':answer-field/key',':answer-field/correct']:continue
 proposals.append({'entity':e,'attribute':a[1:],'before':before,'after':after,'reason':' '.join(dict.fromkeys(reasons[key]))})
# Missing reference values use a null CAS against absence rather than the stub Pull map.
for p in proposals:
 if p['attribute']=='answer-field/correct':p['before']=objects[p['entity']].get(':answer-field/correct',{}).get(':db/id')
(H/'proposals.json').write_text(json.dumps(proposals,default=str,indent=2)+'\n');(H/'mathematical-correction-evidence.json').write_text(json.dumps(evidence,default=str,indent=2)+'\n')
print('Proposals',len(proposals),'mathematical matrices corrected',len(evidence),dict(collections.Counter(p['attribute']for p in proposals)))
