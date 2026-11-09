import sys,json,copy,re,hashlib,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import kw,dumps
from question_capture.math_format import normalize_prose
from mathcheck import expr
allbefore=[];allafter=[];changes=[];extra=[];completion=[];detached=[];corrections=[]
def fix(q,attr,new,why):
 old=q.get(':'+attr)
 if old!=new:q[':'+attr]=new;changes.append({'entity':q[':db/id'],'attribute':attr,'old':old,'new':new,'rationale':why})
def select(f,value,why):
 aa=[a for a in f[':answer-field/choices']if a[':answer/value']==value];assert len(aa)==1,(f[':db/id'],value)
 a=aa[0];old=f.get(':answer-field/correct',{}).get(':db/id')
 if old!=a[':db/id']:changes.append({'entity':f[':db/id'],'attribute':'answer-field/correct','old':old,'new':a[':db/id'],'rationale':why});f[':answer-field/correct']=a
manual={
'q-65109':'I, II and III','q-79728':'I and III only','q-64955':r'y_{2}(x) = \sin x','q-64956':'xu^{″} + u^{′} = 0','q-332724':r'Ae^{-3x}',
'q-65095':'I and II only','q-65175':'I, II and III','q-65118':r'y = A\cos 5x + B\sin 5x','q-65119':r'y = Ae^{4t} + Be^{-3t}','q-65105':r'y = Ax + Bx\ln x','q-342710':r'-\frac{2}{x}W(x)'}
solutions={
'q-65109':r'''The superposition principle applies because the equation is linear and homogeneous. Every function $c_1e^{-t}+c_2te^{-t}$ is a solution. Statement I uses $(c_1,c_2)=(0,-3)$, statement II uses $(1,-1)$, and statement III uses $(1/2,0)$. Thus all three statements are true.''',
'q-79728':r'''Every constant multiple $ce^{-x}$ is a solution by the superposition principle. Statements I and III use $c=2$ and $c=-9$, respectively. For statement II, let $y=xe^{-x}$. Then $y'=(1-x)e^{-x}$ and $y''=(x-2)e^{-x}$, so $y''-y=-2e^{-x}\ne0$. Therefore the answer is I and III only.''',
'q-64955':r'''Set $y_2=u(x)\cos x$ on an interval where $\cos x\ne0$. Differentiating gives
$$
y_2'=u'\cos x-u\sin x,\qquad y_2''=u''\cos x-2u'\sin x-u\cos x.
$$
Substitution into $y''+y=0$ yields $u''\cos x-2u'\sin x=0$. Setting $w=u'$ gives $w'=2w\tan x$, hence $w=C\sec^2x$ and $u=C\tan x+D$. Choosing $C=1,D=0$ gives $y_2=\sin x$. This expression extends across the zeros of $\cos x$ and satisfies the original equation everywhere. Since $W(\cos x,\sin x)=1$, the second solution is independent of the first.''',
'q-64956':r'''With $y_2=ux$, we have $y_2'=u'x+u$ and $y_2''=u''x+2u'$. Substitution gives
$$
\begin{aligned}
x^2y_2''-xy_2'+y_2
&=x^2(u''x+2u')-x(u'x+u)+ux\\
&=x^3u''+x^2u'\\
&=x^2(xu''+u').
\end{aligned}
$$
Because $x>0$, division by $x^2$ gives $xu''+u'=0$.''',
'q-332724':r'''To find the complementary solution, solve the associated homogeneous equation $y_c'+3y_c=0$. For $y_c\ne0$, separating and integrating gives $\ln|y_c|=-3x+C$, hence $y_c=Ae^{-3x}$. The zero solution is included by taking $A=0$, so $A$ may be any real constant.''',
'q-332773':r'''The complementary solution is $y_c=Ae^{-3x}$. Since the forcing term is constant, try $y_p=\beta$. Substituting into $y'+3y=6$ gives $3\beta=6$, so $y_p=2$. Thus $y=Ae^{-3x}+2$. The initial condition gives $-2=A+2$, hence $A=-4$. Therefore
$$
y(x)=-4e^{-3x}+2.
$$
Indeed, $y'=12e^{-3x}$, so $y'+3y=6$ and $y(0)=-2$.''',
'q-65095':r'''Both $e^{2x}$ and $e^{2x+3}=e^3e^{2x}$ satisfy $y''-y'-2y=0$. However, they are constant multiples of one another, so $Ae^{2x}+Be^{2x+3}=(A+Be^3)e^{2x}$ contains only one independent homogeneous solution. The characteristic equation $(r-2)(r+1)=0$ also gives $e^{-x}$, and the general solution is $C_1e^{2x}+C_2e^{-x}$. Therefore I and II are true, and III is false.''',
'q-65175':r'''On an interval where $x\ne0$, direct substitution shows that $x$ and $x^2$ both satisfy $x^2y''-2xy'+2y=0$. Their Wronskian is $x(2x)-x^2=x^2\ne0$ on that interval. They form a fundamental set, so the general solution is $y=Ax+Bx^2$. All three statements are true.''',
'q-65118':r'''Set $y_2=u(x)\cos5x$ on an interval where $\cos5x\ne0$. Differentiation and substitution give
$$
y_2''+25y_2=u''\cos5x-10u'\sin5x=0.
$$
Letting $w=u'$ yields $w'=10w\tan5x$, so $w=C\sec^2 5x$ and $u=\frac C5\tan5x+D$. Choosing $C=5,D=0$ gives $y_2=\sin5x$, which extends across the zeros of $\cos5x$ and solves the original equation on $\mathbb R$. Since $W(\cos5x,\sin5x)=5\ne0$, the general solution is
$$
y=A\cos5x+B\sin5x.
$$''',
'q-65119':r'''Set $y_2=u(t)e^{4t}$. Then
$$
y_2'=e^{4t}(u'+4u),\qquad y_2''=e^{4t}(u''+8u'+16u).
$$
Substitution into $y''-y'-12y=0$ gives $e^{4t}(u''+7u')=0$. Since $e^{4t}\ne0$, let $w=u'$ and solve $w'+7w=0$: $w=Ce^{-7t}$ and $u=-\frac C7e^{-7t}+D$. Taking $C=-7,D=0$ gives $y_2=e^{-3t}$. The Wronskian is $-7e^t\ne0$, so
$$
y=Ae^{4t}+Be^{-3t}.
$$''',
'q-65105':r'''Set $y_2=u(x)x$. We have $y_2'=u'x+u$ and $y_2''=u''x+2u'$, so substitution yields $x^2(xu''+u')=0$. Since $x>0$, set $w=u'$ and solve $xw'+w=0$. This gives $w=C/x$ and $u=C\ln x+D$. Choosing $C=1,D=0$ yields $y_2=x\ln x$. The Wronskian of $x$ and $x\ln x$ is $x\ne0$ on $(0,\infty)$, so
$$
y=Ax+Bx\ln x.
$$''',
'q-342710':r'''Because $x>0$, divide the equation by $2x$ to obtain
$$
y''+\frac2x y'+\frac12y=0.
$$
Thus $P(x)=2/x$. Abel's identity gives
$$
W'(x)=-P(x)W(x)=-\frac2xW(x).
$$'''}
for out in sorted(HERE.glob('175*')):
 qs=json.loads((out/'questions.json').read_text());before=copy.deepcopy(qs);topic=json.loads((out/'topic.json').read_text());kps={q[':db/id']:kp for kp in topic[':topic/knowledge-points']for q in [kp[':knowledge-point/canonical-example']]+kp.get(':knowledge-point/questions',[])}
 for q in qs:
  mid=q[':question/math-academy-id'];fs=q.get(':question/answer-fields',[])
  # Duplicate memberships came from initial seed+recapture; retain the complete existing source role.
  groups={}
  for f in fs:groups.setdefault(f[':answer-field/key'],[]).append(f)
  for key,group in groups.items():
   if len(group)>1:
    keep=next(f for f in group if f.get(':answer-field/correct'))
    for f in group:
     if f is not keep:
      extra.append([kw('db/retract'),q[':db/id'],kw('question/answer-fields'),f[':db/id']]);fs.remove(f);detached.append({'question':q[':db/id'],'field':f[':db/id'],'kept':keep[':db/id'],'reason':'Duplicate same logical source response; retain complete existing keyed field. Detached entity and choices/history retained.'})
  if mid in manual:
   target=manual[mid];f=fs[0]
   if not any(a[':answer/value']==target for a in f.get(':answer-field/choices',[])):
    # Equivalent formatting is allowed, not an inferred new bank.
    def canon(v):return re.sub(r'\s|[{}]|\\operatorname|⁡','',v).replace('ln','ln')
    aa=[a for a in f.get(':answer-field/choices',[])if canon(a[':answer/value'])==canon(target)];assert len(aa)==1,(mid,target,[a[':answer/value']for a in f.get(':answer-field/choices',[])]);target=aa[0][':answer/value']
   select(f,target,'Independently derived from actual givens; canonical and nearby template reviewed')
  if mid in solutions:
   fix(q,'question/worked-solution',normalize_prose(solutions[mid]),'Locally authored completion from owning canonical and matching nearby question')
   completion.append({'question':q[':db/id'],'mid':mid,'canonical':kps[q[':db/id']][':knowledge-point/canonical-example'][':db/id'],'nearby':[v[':db/id']for v in kps[q[':db/id']].get(':knowledge-point/questions',[])if v.get(':question/worked-solution')][:2],'template':'Preserve the KP method; substitute target givens, derive all answer fields and check the original equation.'})
  if mid=='q-332773':
   f=fs[0];temp='answer-quiz3-q332773';aid=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/quiz3-quality/q-332773/answer'))
   answer={':db/id':temp,':answer/id':aid,':answer/type':{':db/ident':':answer.type/math'},':answer/value':r'-4e^{-3x}+2'}
   extra += [{kw('db/id'):temp,kw('answer/id'):uuid.UUID(aid),kw('answer/type'):kw('answer.type/math'),kw('answer/value'):r'-4e^{-3x}+2'},[kw('db/add'),f[':db/id'],kw('answer-field/choices'),temp]]
   fix(f,'answer-field/correct',temp,'Independently solved initial value problem; one new answer for existing blank')
   f[':answer-field/choices']=[answer];f[':answer-field/correct']=answer
  if mid in ['q-343294','q-343299']:
   f=next(f for f in fs if f[':answer-field/key']=='field-1');select(f,r'-\operatorname{sin}⁡(x)'if mid=='q-343294'else r'-\frac{3}{x}','Abel identity W\'= -P W; old key belongs to another response role')
   bad=[a for a in f[':answer-field/choices']if '$'in a[':answer/value']]
   for a in bad:
    f[':answer-field/choices'].remove(a);extra.append([kw('db/retract'),f[':db/id'],kw('answer-field/choices'),a[':db/id']]);detached.append({'question':q[':db/id'],'field':f[':db/id'],'answer':a[':db/id'],'reason':'Foreign conclusion artifact does not appear in source coefficient choice bank; retain detached entity/history.'})
  if mid=='e-6578':
   fix(q,'question/problem',q[':question/problem'].replace("y'' - 2y - 3y","y'' - 2y' - 3y"),'Source typo: roots -1 and3 require y\'\' -2y\'-3y=0')
   fix(q,'question/worked-solution',q[':question/worked-solution'].replace('y(t) = c_1 e^{-x}','y(x) = c_1 e^{-x}'),'Use the same independent variable as the problem')
   corrections.append(mid)
  if mid=='q-102792':
   fix(q,'question/worked-solution',q[':question/worked-solution'].replace('-6{u}^{′}{e}^{-6t}','-6{u}^{′}{e}^{-3t}'),'Product rule: differentiating u e^-3t keeps e^-3t in every term');corrections.append(mid)
  if mid=='q-332547':
   for attr in ['question/problem','question/worked-solution']:fix(q,attr,q[':'+attr].replace('{e}^{-6x}',r'{e}^{-6x/5}'),'Retain source coefficient5; homogeneous rate is-6/5')
   for f in fs:
    for a in f[':answer-field/choices']:
     if '{e}^{-6x}'in a[':answer/value']:fix(a,'answer/value',a[':answer/value'].replace('{e}^{-6x}',r'{e}^{-6x/5}'),'Correct actual equation5y\'+6y=-30')
   fix(q,'question/worked-solution',q[':question/worked-solution']+'\n\nCheck: $y_c\'=-(6/5)Ae^{-6x/5}$, so $5y_c\'+6y_c=0$. Also $y_p=-5$ gives $5y_p\'+6y_p=-30$.','Explicit derivative check of corrected homogeneous rate')
   corrections.append(mid)
  if mid=='q-79930':
   for f in fs:fix(f,'answer-field/key',f[':answer-field/key'].replace('-t','-x').replace('1-t','1-x'),'Repair source x/t mismatch; functions are of x')
   fix(q,'question/worked-solution',q[':question/worked-solution'].replace('-t','-x').replace('1-t','1-x'),'Repair source independent-variable mismatch');corrections.append(mid)
  # Roman-option references require visible Roman labels in examples and unconverted seed radio questions.
  if not fs or(fs[0][':answer-field/type'][':db/ident']==':answer-field.type/radio'and any(a[':answer/type'][':db/ident']==':answer.type/text'for a in fs[0].get(':answer-field/choices',[]))):
   p=q[':question/problem'];n=[0]
   def roman(m):n[0]+=1;return ['I. ','II. ','III. '][n[0]-1]+m[1]
   p=re.sub(r'(?m)^(?:- |[123]\. )(\$.*)$',roman,p)
   fix(q,'question/problem',p,'Restore source Roman statement labels used by solution and choice bank')
  # Explain singular-interval divisions before carrying out reduction of order.
  if out.name in ['17592186049102','17592186050522'] and 'reduction of order'in q[':question/problem'].lower()and ('cos'in q[':question/problem']or'sin'in q[':question/problem'])and mid not in solutions:
   sol=q.get(':question/worked-solution','');var='t'if '(t)'in q[':question/problem']else'x'
   note=f'Work first on an interval where the given solution $y_1({var})$ is nonzero. After simplifying $y_2$, verify it in the original equation to extend it across zeros of $y_1$ when the simplified function is defined there.\n\n'
   if sol:fix(q,'question/worked-solution',note+sol,'State interval restriction before dividing by a trigonometric known solution')
  if out.name=='17592186050895'and q.get(':question/worked-solution')and r'\frac{\text{d}W}{W}'in q[':question/worked-solution']:
   sol=q[':question/worked-solution'];note='The separated calculation below treats $W\\ne0$. The solution $W\equiv0$ must also be included; allowing $C=0$ in the final formula supplies it.\n\n';fix(q,'question/worked-solution',note+sol,'Do not lose the zero Wronskian when separating variables, especially when W(x0)=0')
  if out.name=='17592186050150':
   p=q[':question/problem'];p=p.replace('functions ${1, \\sin (x)}$',r'functions $\{1, \sin(x)\}$').replace('functions ${{e}^{x},\\,x}$',r'functions $\{e^x,x\}$').replace('functions ${\\operatorname{sin}⁡x,\\,{e}^{x},\\,3\\operatorname{sin}⁡x}$',r'functions $\{\sin x,e^x,3\sin x\}$').replace('functions ${y_{1}(x), y_{2}(x)}$',r'functions $\{y_1(x),y_2(x)\}$').replace('set ${{y}_{1}(x),{y}_{2}(x)}$',r'set $\{y_1(x),y_2(x)\}$')
   fix(q,'question/problem',p,'Restore visible set braces lost in the import')
  # Repair run-together source prose without modifying its mathematical response roles.
  p=q[':question/problem'];p=re.sub(r'(reasoning(?: below)?\.)(?=(?:For all|Suppose|The Wronskian))',r'\1\n\n',p);fix(q,'question/problem',p,'Restore paragraph separation between instructions and reasoning')
  if mid=='q-65175':fix(q,'question/problem',q[':question/problem'].replace('Which of the following statements','Work on an interval where $x\\ne0$. Which of the following statements'),'Specify a regular interval for the general-solution claim')
  if mid=='q-130003':fix(q,'question/problem',q[':question/problem'].replace('Which of the following statements','For $x>0$, which of the following statements'),'Real logarithm and fundamental-solution claim require x>0')
  # Source radio-to-checkbox conversion is intentional. Do not restore source radio markup.
 (out/'questions-after.json').write_text(json.dumps(qs,indent=2));allbefore+=before;allafter+=qs
# Tutorials: retain existing derivations while stating the hypotheses and correcting terminology.
tutorialchanges=[]
for out in sorted(HERE.glob('175*')):
 lessons=json.loads((out/'lessons.json').read_text())
 for aa in lessons:
  for step in aa[0][':activity/steps']:
   c=step[':step/content'];eid=c[':db/id'];v=c.get(':tutorial/content')
   if v is None:continue
   nv=v
   if eid==17592186153328:
    nv=v.replace('If $W = 0$ and it’s known that $y_1$ and $y_2$ are solutions to the same second-order linear differential equation, then $y_1$ and $y_2$ are linearly dependent.','If $y_1$ and $y_2$ solve the same homogeneous equation $y\'\'+p(x)y\'+q(x)y=0$ with $p$ and $q$ continuous on $I$, and $W(x_0)=0$ at one point $x_0\in I$, then they are linearly dependent on $I$. The continuity and common-interval assumptions are essential.')
    nv=nv.replace('We cannot deduce any information from $W = 0$ in cases where $y_1$ and $y_2$ are not known to be solutions to the same second-order linear differential equation.','For arbitrary differentiable functions, an identically zero Wronskian alone does not establish linear dependence. Extra hypotheses are needed.')
   if eid==17592186153329:nv=nv.replace('equation of degree $n$','equation of order $n$').replace('equation is of degree two','equation is of order two').replace('are the solutions to the equation','are solutions to the equation')
   if eid==17592186218358:nv=nv.replace('on some interval $I.$','on an interval $I$ where $P$ and $Q$ are continuous.').replace('Solving this equation via separation of variables gives','Solving this equation with an integrating factor (which includes $W\equiv0$) gives')
   if eid==17592186218359:nv='Assume $p$ and $q$ are continuous on a common interval $I$, and both solutions are defined there.\n\n'+nv
   if eid==17592186218360:nv='Throughout this argument, the normalized coefficients are continuous on one common interval $I$.\n\n'+nv
   if eid==17592186125812:
    nv=nv.replace('It works like this:', 'Work on an interval where the leading coefficient and the known solution are nonzero. It works like this:').replace('We can choose any values for $c_1$ and $c_2$ to yield a second solution.', 'To obtain a linearly independent second solution, choose $c_1\\ne0$. The choice $c_1=0$ only reproduces a multiple of the known solution.')
    nv+='\n\nThe divisions by $\sin4t$ and the formula for $u$ are valid between consecutive zeros of $\sin4t$. The simplified result $y_2=\cos4t$ is defined on $\mathbb R$ and directly satisfies the original equation there, so it extends across those zeros.'
   if eid==17592186230179:nv=nv.replace('For example, if the forcing function $f(x)$ is a polynomial of degree $n,$ we guess a particular solution that is also a polynomial of degree $n.$','For a first-order equation with constant coefficients $ay\'+by=f(x)$ and $b\ne0$, if $f(x)$ is a polynomial of degree $n$, try a general polynomial of degree $n$. If $b=0$, integrate $ay\'=f(x)$ instead; the trial generally needs degree $n+1$.')
   if eid==17592186230226:nv+='\n\nSeparating variables divided by $y_c$, so the zero solution must be restored explicitly. Taking $A=0$ includes it in $y_c=Ae^{-10x}$.'
   if eid==17592186230199:nv='Work on an interval where $a(x)\ne0$ and the normalized coefficients $b/a$ and $f/a$ are continuous.\n\n'+nv
   if eid==17592186230238:nv=nv.replace('e^{-2/3x}',r'e^{-(2/3)x}')
   if eid in [17592186153382,17592186153335]:nv='Work throughout on one interval where the leading coefficient is nonzero and all normalized coefficients are continuous.\n\n'+nv
   if eid==17592186153364:nv=nv.replace('The **superposition principle**','All solutions and their linear combinations are considered on a common interval where they are defined.\n\nThe **superposition principle**',1)
   if nv!=v:tutorialchanges.append({'entity':eid,'attribute':'tutorial/content','old':v,'new':normalize_prose(nv),'rationale':'Correct order terminology, theorem hypotheses, zero-solution loss, or interval restrictions while preserving the lesson derivation'});c[':tutorial/content']=normalize_prose(nv)
 (out/'lessons-after.json').write_text(json.dumps(lessons,indent=2))
changes+=tutorialchanges
# Source-bank artifacts: remove only duplicate equivalent values or cross-role records absent from the actual menu.
for q in allafter:
 for f in q.get(':question/answer-fields',[]):
  bank=f.get(':answer-field/choices',[]);correct=f.get(':answer-field/correct',{});seen=[]
  # Prefer correctly typed text entries and existing canonical answers.
  ordered=sorted(bank,key=lambda a:(a[':answer/type'][':db/ident']==':answer.type/math'and('$'in a[':answer/value']or a[':answer/value']in ['is',"isn't"]),a[':db/id']!=correct.get(':db/id')))
  for a in ordered:
   def textcanon(v):return re.sub(r'\s|\$', '',v).replace(r'\mathbb{R}','R').replace('⁡','')
   dup=None
   for b in seen:
    if textcanon(a[':answer/value'])==textcanon(b[':answer/value']):dup=b;break
    if a[':answer/type'][':db/ident']==b[':answer/type'][':db/ident']==':answer.type/math':
     try:
      if expr(a[':answer/value'])==expr(b[':answer/value']):dup=b;break
     except Exception:pass
   if dup:
    bank.remove(a)
    if a[':db/id']==correct.get(':db/id'):select(f,dup[':answer/value'],'Use equivalent properly typed source menu item')
    extra.append([kw('db/retract'),f[':db/id'],kw('answer-field/choices'),a[':db/id']]);detached.append({'question':q[':db/id'],'field':f[':db/id'],'answer':a[':db/id'],'kept':dup[':db/id'],'reason':'Duplicate source menu value or type-corrupted duplicate; detached entity and history retained.'})
   else:seen.append(a)
# The source menu itself has two equivalent complementary families under swapped arbitrary constants.
q=next(q for q in allafter if q[':question/math-academy-id']=='q-339878')
f=next(f for f in q[':question/answer-fields']if f[':answer-field/key']=='field-3')
a=next(a for a in f[':answer-field/choices']if a[':db/id']==17592186313893)
f[':answer-field/choices'].remove(a);extra.append([kw('db/retract'),f[':db/id'],kw('answer-field/choices'),a[':db/id']]);detached.append({'question':q[':db/id'],'field':f[':db/id'],'answer':a[':db/id'],'reason':'Both swapped-constant families describe identical complementary solutions. Retain one active canonical option and preserve detached ID/history.'});corrections.append('q-339878')
# Re-save after bank cleanup.
for out in sorted(HERE.glob('175*')):
 ids={q[':db/id']for q in json.loads((out/'questions.json').read_text())};(out/'questions-after.json').write_text(json.dumps([q for q in allafter if q[':db/id']in ids],indent=2))
consolidated={}
for c in changes:
 key=(c['entity'],c['attribute'])
 if key in consolidated:
  consolidated[key]['new']=c['new'];consolidated[key]['rationale']+='; '+c['rationale']
 else:consolidated[key]=copy.deepcopy(c)
changes=list(consolidated.values())
forms=[]
for c in changes:
 old=c['old'];new=c['new']
 if c['attribute']=='answer-field/correct'and isinstance(old,dict):old=old.get(':db/id')
 forms.append([kw('db/cas'),c['entity'],kw(c['attribute']),old,new])
forms+=extra
forms.append([kw('db/ensure'),'answer-quiz3-q332773',kw('answer/validate')])
qids={q[':db/id']for q in allafter};fids={f[':db/id']for q in allafter for f in q.get(':question/answer-fields',[])};aids={a[':db/id']for q in allafter for f in q.get(':question/answer-fields',[])for a in f.get(':answer-field/choices',[])}
tids={c['entity']for c in tutorialchanges}
changed={c['entity']for c in changes}|{m[1]for m in extra if isinstance(m,list)}
# Ensure full owners when child values/memberships change.
for q in allafter:
 if q[':db/id']in changed or any(f[':db/id']in changed or any(a[':db/id']in changed for a in f.get(':answer-field/choices',[]))for f in q.get(':question/answer-fields',[])):
  forms.append([kw('db/ensure'),q[':db/id'],kw('question/validate')])
for e in sorted(changed-frozenset(qids)-tids,key=str):
 if e in fids:forms.append([kw('db/ensure'),e,kw('answer-field/validate')])
 elif e in aids:forms.append([kw('db/ensure'),e,kw('answer/validate')])
(HERE/'changes.json').write_text(json.dumps(changes,indent=2));(HERE/'detached-memberships.json').write_text(json.dumps(detached,indent=2));(HERE/'completion-templates.json').write_text(json.dumps(completion,indent=2));(HERE/'mathematical-corrections.json').write_text(json.dumps(corrections,indent=2));(HERE/'transaction.edn').write_text(dumps(forms)+'\n')
print(json.dumps({'changes':len(changes),'detached_memberships':len(detached),'completions':len(completion),'forms':len(forms),'corrections':corrections},indent=2))
