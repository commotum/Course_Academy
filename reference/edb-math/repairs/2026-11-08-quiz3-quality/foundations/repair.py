"""Source-backed full six-topic quality repairs; preserve existing entities."""
import copy,json,re,sys,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from question_capture.math_format import normalize_prose,normalize_tex,MATH
from question_capture.edn import dumps,kw
changes=[];forms=[];ensures={};retained=[];templates=[];all_after=[]
def set_braces(tex):
 stack=[];pairs=[]
 for i,ch in enumerate(tex):
  if i and tex[i-1]=='\\':continue
  if ch=='{':stack.append([i,False])
  elif ch==',' and stack:stack[-1][1]=True
  elif ch=='}' and stack:
   start,comma=stack.pop();prev=tex[:start]
   if comma and not re.search(r'(?:\\[A-Za-z]+|[_^])\s*$',prev) and not tex[start:].startswith('{{field-'):pairs.append((start,i))
 for i,j in sorted(pairs,reverse=True):tex=tex[:j]+'\\'+tex[j:];tex=tex[:i]+'\\'+tex[i:]
 return tex

def fonts(value,symbols,bare=False):
 def one(tex):
  tex=set_braces(tex);protected=[];matrices=[]
  tex=re.sub(r'\\(mathbf|mathrm|mathbb|textrm)\s+([A-Za-z0-9])',lambda m:'\\'+m[1]+'{'+m[2]+'}',tex)
  def protect(m):protected.append(m[0]);return 'FONTGUARD'+str(len(protected)-1)+'END'
  tex=re.sub(r'\\(?:mathbf|mathbfit|mathrm|mathit|mathbb|textbf|text|textrm|operatorname)\{[^{}]*\}',protect,tex)
  def matrix(m):matrices.append(m[0]);return 'MATRIXGUARD'+str(len(matrices)-1)+'END'
  tex=re.sub(r'\\begin\{(?:bmatrix|pmatrix|matrix|array)\}.*?\\end\{(?:bmatrix|pmatrix|matrix|array)\}',matrix,tex,flags=re.S)
  token=r'FONTGUARD\d+END|MATRIXGUARD\d+END|\\(?:begin|end)\{[^{}]*\}|\\[A-Za-z]+|\d+|[\s\S]'
  tex=re.sub(token,lambda m:r'\mathbf{'+m[0]+'}'if m[0]in symbols else m[0],tex)
  tex=re.sub(r'MATRIXGUARD(\d+)END',lambda m:matrices[int(m[1])],tex)
  tex=re.sub(r'FONTGUARD(\d+)END',lambda m:protected[int(m[1])],tex)
  return tex
 return one(value)if bare else MATH.sub(lambda m:one(m[0]),value)

solutions={
17592186079163:r"""The operator has constant coefficients. Applying it to $y=e^{4x}$ gives
$$
\begin{aligned}D(y)&=y''-4y'\\&=16e^{4x}-4(4e^{4x})\\&=0.\end{aligned}
$$""",
17592186079223:r"""For $y=e^x+x,$ the required derivatives are $y'=e^x+1,$ $y''=e^x,$ and $y'''=e^x.$ Hence
$$
\begin{aligned}D(y)&=y'''-2y''+2y'\\&=e^x-2e^x+2(e^x+1)\\&=e^x+2.\end{aligned}
$$""",
17592186079164:r"""For $y=x^3,$ we have $y'=3x^2,$ $y''=6x,$ and $y'''=6.$ Applying the variable-coefficient operator gives
$$
\begin{aligned}D(y)&=x^2y'''-xy''+y'\\&=6x^2-x(6x)+3x^2\\&=3x^2.\end{aligned}
$$""",
17592186229709:r"""A linear differential operator $L$ satisfies
$$
L(ay_1+by_2)=aL(y_1)+bL(y_2)
$$
for all suitable functions $y_1,y_2$ and constants $a,b.$ For the given operator $D(y)=y''+yy',$
$$
\begin{aligned}
D(ay_1+by_2)&=ay_1''+by_2''+(ay_1+by_2)(ay_1'+by_2')\\
&=ay_1''+by_2''+a^2y_1y_1'+b^2y_2y_2'+ab(y_1y_2'+y_2y_1').
\end{aligned}
$$
By contrast,
$$
aD(y_1)+bD(y_2)=ay_1''+by_2''+ay_1y_1'+by_2y_2'.
$$
These expressions are not identical for all functions and constants. For example, $D(x)=x$ while $D(2x)=4x\ne2D(x).$ Thus $D$ is nonlinear.""",
17592186229749:r"""A linear differential operator is a sum of terms consisting of a function of $x$ times $y$ or one of its derivatives.

- Operator I, $D_1(y)=xyy',$ is nonlinear because the coefficient $xy$ depends on $y.$ For example, $D_1(2x)=4x^2\ne2D_1(x).$
- Operator II, $D_2(y)=x^3y''-2x^2y',$ is linear: differentiation and multiplication by the fixed coefficient functions $x^3$ and $-2x^2$ preserve linear combinations.
- Operator III, $D_3(y)=x^2y''-y,$ is linear for the same reason.

Therefore the correct answer is **II and III only**.""",
17592186229708:r"""A linear differential operator has coefficients that depend only on $x.$

- Operator I, $D_1(y)=y'+2y,$ is linear, with constant coefficients.
- Operator II, $D_2(y)=(\sin x)y''+3x^2y'+2y,$ is linear, since its coefficients $\sin x,$ $3x^2,$ and $2$ depend only on $x.$
- Operator III, $D_3(y)=y'''+x\cos(xy)y',$ is nonlinear because the coefficient $x\cos(xy)$ depends on $y.$

Therefore the correct answer is **I and II only**.""",
17592186229750:r"""Since $L$ is linear,
$$
\begin{aligned}L(y_1-2y_2)&=L(y_1)-2L(y_2)\\&=\left(x+4-\frac2x\right)-2\left(2-\frac3x\right)\\&=x+\frac4x\\&=\frac{x^2+4}{x}.\end{aligned}
$$
The identity holds wherever the given expressions are defined, so $x\ne0.$""",
17592186152627:r"""A second-order ODE is linear when the coefficients of $y'',$ $y',$ and $y$ depend only on $x,$ and $y$ and its derivatives occur to the first power.

- Equation I, $y''+2y'+5y=0,$ is linear, with constant coefficients.
- Equation II, $3y''+y^2y'+4=0,$ is nonlinear because the coefficient $y^2$ of $y'$ depends on $y.$
- Equation III, $y''-xy=x,$ is linear: its coefficients $1,$ $0,$ and $-x$ depend only on $x.$

Therefore the correct answer is **I and III only**.""",
17592186152631:r"""A second-order ODE is linear when it has the form $a(x)y''+b(x)y'+c(x)y=f(x),$ with coefficients depending only on $x$ and with $a(x)\ne0$ on the interval considered.

- Equation I, $xy''+2y'+(\cos x)y=0,$ is linear on any interval avoiding $x=0.$
- Equation II, $3y''+x^2y'+xy=4,$ is linear, since all its coefficients depend only on $x.$
- Equation III, $y''-yy'=x,$ is nonlinear because the coefficient $-y$ of $y'$ depends on $y.$

Therefore the correct answer is **I and II only**."""}
keys={17592186079163:17592186077759,17592186079223:17592186078120,17592186079164:17592186077767,17592186229709:17592186228431,17592186229749:17592186228706,17592186229708:17592186228428,17592186229750:17592186228714,17592186152627:17592186150272,17592186152631:17592186150297,
17592186310953:17592186309521,17592186311402:17592186309429,17592186311094:17592186309034,17592186311440:17592186308857,17592186311224:17592186310484,17592186311381:17592186309942}
aliens={17592186310953:{17592186309909},17592186311402:{17592186310270},17592186311094:{17592186309721},17592186311440:{17592186309186},17592186311224:{17592186309071},17592186311381:{17592186310598}}
for d in sorted(HERE.glob('175*')):
 before=json.loads((d/'questions-before.json').read_text());after=copy.deepcopy(before);manifest={r['entity']:r for r in json.loads((d/'source-manifest.json').read_text())};fresh={r['entity']:r for r in json.loads((d/'reextracted.json').read_text())}
 for q in after:
  eid=q[':db/id'];syms=set()
  for role in ['prompt_sources','solution_sources']:
   for s in manifest[eid][role]:
    soup=BeautifulSoup(s['html'],'html.parser')
    syms.update(n.get_text().strip()for n in soup.select('[mathvariant="bold"]')if re.fullmatch('[A-Za-z0]',n.get_text().strip()))
  # Source marks vector letters; numerical matrix entries and scalar coefficients remain ordinary.
  syms&=set('avwubABCO')|{'0'}
  if eid in solutions:
   q[':question/worked-solution']=solutions[eid];templates.append({'entity':eid,'kind':'locally authored completion','kp_canonical_examples':[kp.get(':knowledge-point/canonical-example',{}).get(':db/id')for kp in json.loads((d/'topic-before.json').read_text())[':topic/knowledge-points']if any(x[':db/id']==eid for x in kp.get(':knowledge-point/questions',[]))],'derivation':solutions[eid]})
  if eid==17592186229709:q[':question/problem']=fresh[eid]['prompt_sources']['problem']+'\n\nUse this condition to determine whether $D$ is linear.'
  if eid==17592186265866:
   q[':question/worked-solution']=q[':question/worked-solution'].replace(r'D(\operatorname{cos}⁡2x)',r'D({\sin}^{2}x)')
  if eid==17592186265878:
   q[':question/worked-solution']=q[':question/worked-solution'].replace(r'+a{x}^{2}{y}_{1}+a{x}^{2}{y}_{2}',r'+a{x}^{2}{y}_{1}+b{x}^{2}{y}_{2}')
  for attr in [':question/problem',':question/worked-solution']:
   if q.get(attr):q[attr]=normalize_prose(fonts(q[attr],syms))
  for f in q.get(':question/answer-fields',[]):
   fid=f[':db/id'];wanted=keys.get(fid,keys.get(eid))
   if wanted:f[':answer-field/correct']=next(a for a in f[':answer-field/choices']if a[':db/id']==wanted)
   if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':f[':answer-field/key']=normalize_prose(fonts(f[':answer-field/key'],syms))
   if fid in aliens:
    f[':answer-field/choices']=[a for a in f[':answer-field/choices']if a[':db/id']not in aliens[fid]]
   # Homogeneity banks contain duplicated historical captured answers. Keep canonical IDs and one option per value.
   if f[':answer-field/type'][':db/ident']==':answer-field.type/select' and set(a[':answer/value']for a in f[':answer-field/choices'])=={'homogeneous','inhomogeneous'}:
    keep=[]
    for value in ['homogeneous','inhomogeneous']:
     candidates=[a for a in f[':answer-field/choices']if a[':answer/value']==value];correct=f.get(':answer-field/correct',{})
     keep.append(next((a for a in candidates if a[':db/id']==correct.get(':db/id')),candidates[0]))
    f[':answer-field/choices']=keep
    for a in keep:a[':answer/type']={':db/id':17592186045499,':db/ident':':answer.type/text'}
   for a in f[':answer-field/choices']:
    if a[':answer/type'][':db/ident']==':answer.type/math':a[':answer/value']=normalize_tex(fonts(a[':answer/value'],syms,True))
  if eid==17592186152571:q[':question/answer-fields']=[f for f in q[':question/answer-fields']if f[':db/id']not in [17592186149883,17592186149886]]
 for old,new in zip(before,after):
  for attr in [':question/problem',':question/worked-solution']:
   if old.get(attr)!=new.get(attr):changes.append({'entity':old[':db/id'],'attribute':attr,'old':old.get(attr),'new':new[attr]});ensures[old[':db/id']]='question/validate'
  oldfs={f[':db/id']:f for f in old.get(':question/answer-fields',[])};newfs={f[':db/id']:f for f in new.get(':question/answer-fields',[])}
  for fid in oldfs.keys()-newfs.keys():
   forms.append([kw('db/retract'),old[':db/id'],kw('question/answer-fields'),fid]);retained.append({'question':old[':db/id'],'detached_legacy_field':fid,'entities_retained':True});ensures[old[':db/id']]='question/validate'
  for fid,f in newfs.items():
   prev=oldfs[fid]
   for attr in [':answer-field/key',':answer-field/correct']:
    a,b=prev.get(attr),f.get(attr)
    if attr.endswith('/correct'):a=a.get(':db/id')if a else None;b=b.get(':db/id')if b else None
    if a!=b:changes.append({'entity':fid,'attribute':attr,'old':a,'new':b});ensures[fid]='answer-field/validate'
   oldas={a[':db/id']:a for a in prev[':answer-field/choices']};newas={a[':db/id']:a for a in f[':answer-field/choices']}
   for aid in oldas.keys()-newas.keys():
    forms.append([kw('db/retract'),fid,kw('answer-field/choices'),aid]);retained.append({'field':fid,'detached_duplicate_or_alien_answer':aid,'entities_retained':True});ensures[fid]='answer-field/validate'
   for aid,a in newas.items():
    for attr in [':answer/value',':answer/type']:
     v,w=oldas[aid][attr],a[attr]
     if attr==':answer/type':v=v[':db/id'];w=w[':db/id']
     if v!=w:changes.append({'entity':aid,'attribute':attr,'old':v,'new':w});ensures[aid]='answer/validate'
 # tutorials: preserve native data tables, eliminate the literal empty-bold header.
 ls=json.loads((d/'lessons-before.json').read_text());als=copy.deepcopy(ls)
 for a in als:
  for s in a[0].get(':activity/steps',[]):
   c=s[':step/content']
   if c.get(':tutorial/content'):
    prev=c[':tutorial/content'];value=normalize_prose(c[':tutorial/content'].replace('>****</td>','></td>'))
    if prev!=value:changes.append({'entity':c[':db/id'],'attribute':':tutorial/content','old':prev,'new':value});c[':tutorial/content']=value;ensures[c[':db/id']]='tutorial/validate'
 (d/'questions-after.json').write_text(json.dumps(after,indent=2));(d/'lessons-after.json').write_text(json.dumps(als,indent=2));all_after+=after
# Guard memberships through stable owner scalar values as well as changed cardinality-one attrs.
for row in retained:
 eid=row.get('question',row.get('field'))
 if not any(c['entity']==eid for c in changes):
  if 'question'in row:
   q=next(q for q in all_after if q[':db/id']==eid);forms.append([kw('db/cas'),eid,kw('question/problem'),q[':question/problem'],q[':question/problem']])
  else:
   f=next(f for q in all_after for f in q.get(':question/answer-fields',[])if f[':db/id']==eid);forms.append([kw('db/cas'),eid,kw('answer-field/correct'),f[':answer-field/correct'][':db/id'],f[':answer-field/correct'][':db/id']])
forms+=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['old'],c['new']]for c in changes]
forms+=[[kw('db/ensure'),eid,kw(spec)]for eid,spec in sorted(ensures.items())]
(HERE/'changes.json').write_text(json.dumps(changes,indent=2));(HERE/'retained-history-entities.json').write_text(json.dumps(retained,indent=2));(HERE/'completion-templates.json').write_text(json.dumps(templates,indent=2));(HERE/'transaction.edn').write_text(dumps(forms)+'\n')
print(json.dumps({'changes':len(changes),'membership_repairs':len(retained),'ensured':len(ensures),'authored_completions':len(templates)},indent=2))
