import copy,collections,json,re,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from independent_math import scalar,canonical,X,Y,Z
I=json.loads((H.parent/'inventory.json').read_text());ids={q for t,k,q in I['links']if k==17592186175972};Q=json.loads((H/'supplement2-proposed-questions.json').read_text());rows=[];P=[];proofs=[]
for q in Q:
 if q[':db/id']not in ids:continue
 cs=canonical(q);free=[]
 for f,a in cs:
  try:e=scalar(a[':answer/value'])
  except Exception:continue
  if e in[X,Y,Z]:free.append((f,a,e))
 rows.append({'question':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'source_or_generated':'source'if q.get(':question/math-academy-id')else'generated','canonical_values':[a[':answer/value']for f,a in cs],'free_component':bool(free),'current_prompt':q[':question/problem'],'resolution':'Dependent component / no interactive free-component bank; no ambiguity of free-coordinate scaling.'if not free else'Whole bank and coordinate coupling inspected below.'})
 if not free:continue
 for f,a,e in free:
  vals=[x[':answer/value']for x in f[':answer-field/choices']]
  if q[':db/id']!=17592186365398:
   rows[-1]['resolution']='Unique listed full-surface component: alternative scaled z inq164455 violates x=12z² because the supplied first component already depends on parameterz; q103992 andq164446 alternatives lose whole-axis coverage or collapse parameter dimension.';continue
  before=q[':question/problem'];after=before+'\n\nUse the free parameter directly as its corresponding Cartesian coordinate.'
  worked=q[':question/worked-solution'];new_worked=worked+'\n\nHere the free parameter is $z$. The stated direct-coordinate convention therefore requires the third component to be $z$.'
  x,z=S.symbols('x z',real=True);f1=S.Matrix([x,6*x*x,z]);f2=S.Matrix([x,6*x*x,6*z]);assert f1[1]-6*f1[0]**2==f2[1]-6*f2[0]**2==0;assert f1.diff(x).cross(f1.diff(z))[1]==-1 and f2.diff(x).cross(f2.diff(z))[1]==-6
  proof={'basis':9837,'question':q[':db/id'],'math_academy_id':q[':question/math-academy-id'],'full_prompt_before':before,'full_solution_before':worked,'field':f[':db/id'],'correct':a[':db/id'],'bank':[{k:v for k,v in aa.items()if k in[':db/id',':answer/id',':answer/value',':answer/type']}for aa in f[':answer-field/choices']],'independent_proof':'F1(x,z)=(x,6x²,z) andF2(x,z)=(x,6x²,6z) both satisfy y=6x². Every(a,6a²,b) is F1(a,b)=F2(a,b/6), proving both surjective. Their tangent cross products(12x,−1,0) and(72x,−6,0) never vanish, proving both regular. Thus original unstated-convention bank had two valid parameterizations. Requiring the free parameter itself as the corresponding Cartesian coordinate selects z. z² excludes all negative third coordinates; x and6x² collapse the free axis (e.g neither reaches(0,0,1));6z fails only the now-explicit direct-coordinate requirement, and is not called an invalid general parameterization.','generator_prevention':'Frozen KP75972 normal renderer already states the direct-coordinate convention and preserves raw evidence replay. No package mutation.','authoring':'Transparent authored clarification of source task scope; all values, IDs, owned canonical links and histories preserved.'};proofs.append(proof)
  for attr,bef,aft in[('question/problem',before,after),('question/worked-solution',worked,new_worked)]:P.append({'entity':q[':db/id'],'attribute':attr,'before':bef,'after':aft,'reason':'Authored source correction: state direct-coordinate convention needed to distinguish canonical z from equally valid general reparametrization6z','evidence':proof,'confidence':'high'});q[':'+attr]=aft
  rows[-1]['resolution']='Two full regular surjective parameterizations in existing bank; transparently clarify intended direct-coordinate task, preserving both values and existing key.'
assert len(P)==2;(H/'free-coordinate-proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'free-coordinate-proofs.json').write_text(json.dumps({'kp':17592186175972,'questions_reviewed':len(rows),'source_generated_counts':dict(collections.Counter(r['source_or_generated']for r in rows)),'records':rows,'authored_proofs':proofs},indent=2)+'\n');(H/'free-coordinate-render-input.json').write_text(json.dumps([{'entity':p['entity'],'attribute':p['attribute'],'value':p['after']}for p in P],indent=2)+'\n');(H/'free-coordinate-prospective.json').write_text(json.dumps(Q,indent=2)+'\n');print('reviewed',len(rows),'free banks',sum(r['free_component']for r in rows),'CAS',len(P))
