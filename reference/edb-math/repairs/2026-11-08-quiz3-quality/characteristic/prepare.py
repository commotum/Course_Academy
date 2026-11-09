import json,re,copy,sys,hashlib
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import kw,dumps
from question_capture.math_format import normalize_tex,normalize_prose
base=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic')
solutions={
'q-64660':r'''Assuming $y=e^{\lambda x}$ gives the characteristic equation
$$\lambda^2+2\lambda+1=(\lambda+1)^2=0.$$
Thus $\lambda=-1$ is a repeated root.''',
'q-64794':r'''Assuming $y=e^{\lambda x}$ gives
$$\lambda^2-16\lambda+64=(\lambda-8)^2=0.$$
Thus $\lambda=8$ is a repeated root.''',
'q-7791':r'''Assuming $y=e^{\lambda x}$ gives the characteristic equation
$$\lambda^2+6\lambda+9=(\lambda+3)^2=0.$$
The repeated root is $\lambda=-3,$ so the general solution is
$$y=Ae^{-3x}+Bxe^{-3x}.$$''',
'q-64662':r'''The characteristic equation is
$$\lambda^2-4\lambda+4=(\lambda-2)^2=0.$$
The repeated root $\lambda=2$ gives the general solution
$$y=Ae^{2x}+Bxe^{2x}.$$
All the given functions have this form except $2e^x.$ Substitution of $y=2e^x$ gives
$$y''-4y'+4y=2e^x-8e^x+8e^x=2e^x\ne0.$$
Therefore, $2e^x$ is the only non-solution.''',
'q-79610':r'''The characteristic equation is
$$\lambda^2+1=0,$$
so $\lambda=\pm\mathrm{i}.$ The general real-valued solution is
$$y=P\cos x+Q\sin x.$$''',
'q-64697':r'''The characteristic equation is
$$\lambda^2-2\lambda+17=(\lambda-1)^2+16=0,$$
so the roots are $1\pm4\mathrm{i}.$ Hence every solution has the form
$$y=e^x(P\cos4x+Q\sin4x).$$
The only listed function outside this form is $5e^{2x}\sin4x.$ Indeed,
$$y''-2y'+17y=5e^{2x}(\sin4x+8\cos4x)\ne0.$$
Therefore, $5e^{2x}\sin4x$ is the only non-solution.''',
'q-64699':r'''The characteristic equation is
$$\lambda^2-10\lambda+29=(\lambda-5)^2+4=0,$$
so the roots are $5\pm2\mathrm{i}.$ Thus every solution has the form
$$y=e^{5t}(P\cos2t+Q\sin2t).$$
The only listed function outside this form is $5\sin2t.$ Substitution gives
$$y''-10y'+29y=125\sin2t-100\cos2t\ne0.$$
Therefore, $5\sin2t$ is the only non-solution.''',
'q-7817':r'''The characteristic equation is
$$\lambda^2-4\lambda+13=(\lambda-2)^2+9=0.$$
Its roots are $2\pm3\mathrm{i},$ so the general solution is
$$y=e^{2x}(P\cos3x+Q\sin3x).$$''',
'q-7814':r'''The characteristic equation is
$$\lambda^2+10\lambda+25=(\lambda+5)^2=0.$$
The repeated root $-5$ gives $y=Ae^{-5x}+Bxe^{-5x}.$ From $y(0)=5,$ we obtain $A=5.$ Differentiating gives
$$y'=-5Ae^{-5x}+Be^{-5x}-5Bxe^{-5x}.$$
Using $y'(0)=17$ yields $-5A+B=17,$ so $B=42.$ Therefore,
$$y=5e^{-5x}+42xe^{-5x}.$$''',
'q-130365':r'''The characteristic roots are $\lambda=\pm\sqrt{11}\mathrm{i},$ giving
$$y=P\cos(\sqrt{11}x)+Q\sin(\sqrt{11}x).$$
The first condition gives $P=7.$ Differentiating,
$$y'=-\sqrt{11}P\sin(\sqrt{11}x)+\sqrt{11}Q\cos(\sqrt{11}x).$$
Thus $y'(0)=-4\sqrt{11}$ gives $\sqrt{11}Q=-4\sqrt{11},$ so $Q=-4.$ Therefore,
$$y=7\cos(\sqrt{11}x)-4\sin(\sqrt{11}x).$$''',
'q-130534':r'''The characteristic equation is
$$\lambda^2+2\lambda+5=(\lambda+1)^2+4=0,$$
with roots $-1\pm2\mathrm{i}.$ Therefore,
$$y=e^{-x}(P\cos2x+Q\sin2x).$$
The condition $y(0)=3$ gives $P=3.$ Differentiating gives
$$y'=-e^{-x}(P\cos2x+Q\sin2x)+e^{-x}(-2P\sin2x+2Q\cos2x).$$
Using $y'(0)=-5$ gives $-P+2Q=-5,$ hence $Q=-1.$ Therefore,
$$y=e^{-x}(3\cos2x-\sin2x).$$''',
'q-7895':r'''The characteristic roots are $3\pm5\mathrm{i},$ so
$$y=e^{3x}(P\cos5x+Q\sin5x).$$
The first condition gives $P=5.$ Differentiating,
$$y'=3e^{3x}(P\cos5x+Q\sin5x)+e^{3x}(-5P\sin5x+5Q\cos5x).$$
Using $y'(0)=10$ gives $3P+5Q=10,$ hence $Q=-1.$ Therefore,
$$y=e^{3x}(5\cos5x-\sin5x).$$''',
'q-64779':r'''A second-order Cauchy-Euler equation has the form
$$ax^2y''+bxy'+cy=f(x),$$
where $a,b,c$ are constants and $a\ne0.$ The listed equation
$$3x^2y''-2xy'+2y=2\ln x$$
has $a=3,$ $b=-2,$ $c=2,$ and $f(x)=2\ln x.$ Each other option has a derivative or $y$ coefficient with the wrong power of $x.$ Therefore, this is the only listed Cauchy-Euler equation.''',
'q-64715':r'''For a Cauchy-Euler equation, use the trial solution $y=x^\lambda.$ Then $y'=\lambda x^{\lambda-1}$ and $y''=\lambda(\lambda-1)x^{\lambda-2}.$ Substitution gives the characteristic equation
$$\lambda(\lambda-1)-\lambda-3=\lambda^2-2\lambda-3=(\lambda-3)(\lambda+1)=0.$$
The distinct roots are $3$ and $-1.$ Therefore, for $x>0,$
$$y(x)=c_1x^3+c_2x^{-1}.$$''',
'q-64876':r'''Using $y=t^\lambda$ in the Cauchy-Euler equation gives
$$3\lambda(\lambda-1)-15\lambda+27=3\lambda^2-18\lambda+27=3(\lambda-3)^2=0.$$
The repeated root is $\lambda=3.$ Therefore, for $t>0,$
$$y(t)=c_1t^3+c_2t^3\ln t.$$''',
'q-64778':r'''The characteristic equation is
$$\lambda(\lambda-1)+7\lambda+9=\lambda^2+6\lambda+9=(\lambda+3)^2=0.$$
The repeated root $-3$ gives
$$y=c_1x^{-3}+c_2x^{-3}\ln x.$$
The condition $y(1)=3$ gives $c_1=3.$ Differentiating,
$$y'=-3c_1x^{-4}+c_2x^{-4}-3c_2x^{-4}\ln x.$$
Using $y'(1)=-8$ gives $-3c_1+c_2=-8,$ so $c_2=1.$ Therefore, for $x>0,$
$$y(x)=\frac{3+\ln x}{x^3}.$$''',
'q-64881':r'''The characteristic equation is
$$2\lambda(\lambda-1)-6\lambda+8=2\lambda^2-8\lambda+8=2(\lambda-2)^2=0.$$
The repeated root $2$ gives
$$y=c_1t^2+c_2t^2\ln t.$$
The first condition gives $c_1=0.$ Differentiating,
$$y'=2c_1t+c_2t+2c_2t\ln t.$$
The second condition gives $2c_1+c_2=3,$ so $c_2=3.$ Therefore, for $t>0,$
$$y(t)=3t^2\ln t.$$'''}
replacements={
'e-6589': [('and $B=-1.$','and $B=-4.$')],
'e-6596': [(r'y = e^{\lambda x}',r'y = e^{\lambda t}')],
'e-6861': [("y'' + y - 2y", "y'' + y' - 2y"),(r"y' = Ae^x - 2Be^{-x}.",r"y' = Ae^x - 2Be^{-2x}.")],
'e-7051': [(r'({\lambda }^{2}-3)^{2}+16',r'(\lambda -3)^{2}+16'),(r'\lambda -3 & =4\text{i}',r'\lambda -3 & =\pm 4\text{i}'),(r', \quad t\gt 0.','.')],
'q-7790': [(r'{y}^{′}(0)=2',r'{y}^{′}(1)=5')],
'q-7815': [(r'$\lambda =\frac{3}{2}$',r'$\lambda =-\frac{3}{2}$')],
'q-7798': [(r'Substituting ${y}^{′}(1)=1$',r'Substituting ${y}^{′}(1)=-1$')],
'q-7893': [(r'({\lambda }^{2}+2\lambda +1)^{2}-1+10',r'({\lambda }^{2}+2\lambda +1)-1+10')],
'q-130533': [(r'condition ${y}^{′}(0)=4.$',r'condition ${y}^{′}(0)=-4.$')],
'q-64897': [(r'y(x)={c}_{1}t+{c}_{2}{t}^{3}',r'y(t)={c}_{1}t+{c}_{2}{t}^{3}')],
'q-64903': [(r'y(x)={c}_{1}{t}^{-2}+{c}_{2}{t}^{3/2}',r'y(t)={c}_{1}{t}^{-2}+{c}_{2}{t}^{3/2}')],
'q-64841': [(r'Substituting ${y}^{′}(1)=1$',r'Substituting ${y}^{′}(1)=2$')],
'q-64884': [(r'y(t)=\frac{3+15\operatorname{ln}⁡t}{{t}^{8}}',r'y(t)=\frac{3+15\operatorname{ln}⁡t}{{t}^{4}}')],
'q-93910': [(r'{y}^{′}(1)=1',r'{y}^{′}(1)=4')],
'q-64811': [(r'{y}^{′}(1)=1',r'{y}^{′}(1)=4')],
'q-93915': [(r'{t}^{2}{y}^{″}-17t{y}^{′}+81y,',r'{t}^{2}{y}^{″}-17t{y}^{′}+81y=0,')]
}
changes=[];forms=[];affectedq=set();affecteda=set();affectedf=set();complete=[];corrections=[];detached=[]
for d in sorted(base.glob('175*')):
 before=json.loads((d/'questions.json').read_text());after=copy.deepcopy(before);math={r['mid']:r for r in json.loads((d/'mathematics.json').read_text())}
 for old,q in zip(before,after):
  mid=q[':question/math-academy-id'];eid=q[':db/id']
  if mid in solutions:
   assert not q.get(':question/worked-solution')
   recovered=[e['worked_solution']for r in json.loads((d/'source-extractions.json').read_text())if r['mid']==mid for e in r['extractions']if e.get('worked_solution')]
   q[':question/worked-solution']=normalize_prose(recovered[0]if mid in ['q-64876','q-64881']and recovered else solutions[mid]);complete.append(mid)
  if mid in replacements:
   for src,dst in replacements[mid]:
    count=0
    for attr in [':question/problem',':question/worked-solution']:
     if src in q.get(attr,''):q[attr]=q[attr].replace(src,dst);count+=1
    assert count,(mid,src)
   corrections.append(mid)
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):
    if a[':answer/type'][':db/ident']==':answer.type/math':
     val=a[':answer/value'];val=re.sub(r'\\\\(?=[A-Za-z])',r'\\',val).replace(r'\u2061','\u2061');a[':answer/value']=normalize_tex(val)
   if not f.get(':answer-field/correct'):
    # Independent all-choice check identifies unique answer; identification-only question handled explicitly.
    if mid=='q-64779':candidates=[a for a in f[':answer-field/choices']if a[':answer/value'].startswith("3x^{2}y^{″} - 2xy^{′} + 2y")]
    elif mid in ['q-64716','q-64811']:continue # detach the redundant old membership below
    else:
     good={c['eid']for c in math[mid]['choices']if c.get('mathematically_correct')};candidates=[a for a in f[':answer-field/choices']if a[':db/id']in good]
    assert len(candidates)==1,(mid,candidates);f[':answer-field/correct']=copy.deepcopy(candidates[0])
  if mid in ['q-64716','q-64811']:
   duplicate=[f for f in q[':question/answer-fields']if not f.get(':answer-field/correct')];assert len(duplicate)==1
   f=duplicate[0];q[':question/answer-fields'].remove(f);forms.append([kw('db/retract'),eid,kw('question/answer-fields'),f[':db/id']]);detached.append({'question':eid,'mid':mid,'field':f[':db/id'],'preserved_entities':[f[':db/id']]+[a[':db/id']for a in f[':answer-field/choices']]});affectedq.add(eid)
  for attr in [':question/problem',':question/worked-solution']:
   if old.get(attr)!=q.get(attr):changes.append({'entity':eid,'attribute':attr[1:],'old':old.get(attr),'new':q[attr]});affectedq.add(eid)
  for f in q.get(':question/answer-fields',[]):
   oldf=next(o for o in old[':question/answer-fields']if o[':db/id']==f[':db/id'])
   oc=oldf.get(':answer-field/correct',{}).get(':db/id');nc=f.get(':answer-field/correct',{}).get(':db/id')
   if oc!=nc:changes.append({'entity':f[':db/id'],'attribute':'answer-field/correct','old':oc,'new':nc});affectedf.add(f[':db/id']);affectedq.add(eid)
   for a in f[':answer-field/choices']:
    oa=next(o for o in oldf[':answer-field/choices']if o[':db/id']==a[':db/id'])
    if oa[':answer/value']!=a[':answer/value']:changes.append({'entity':a[':db/id'],'attribute':'answer/value','old':oa[':answer/value'],'new':a[':answer/value']});affecteda.add(a[':db/id']);affectedf.add(f[':db/id']);affectedq.add(eid)
 (d/'questions-after.json').write_text(json.dumps(after,indent=2))
# State the homogeneous scope and positive-variable domain explicitly in Cauchy tutorials.
for d in base.glob('175*'):
 lessons=json.loads((d/'lessons.json').read_text());after_lessons=copy.deepcopy(lessons)
 for activity in after_lessons:
  for step in activity[0][':activity/steps']:
   c=step[':step/content'];old=c.get(':tutorial/content')
   if c[':db/id']==17592186148748:
    c[':tutorial/content']=old.replace('where $a,b,$ and $c$ are constants.','where $a,b,$ and $c$ are constants and $a\\ne0.$ We work on $x>0.$').replace('Cauchy-Euler equations can be solved using a trial solution','The corresponding homogeneous equation ($f(x)=0$) can be solved using a trial solution')
   if c[':db/id']==17592186148754:
    c[':tutorial/content']=old.replace('When the characteristic equation','For $x>0,$ when the characteristic equation',1)
   if old is not None and old!=c.get(':tutorial/content'):
    changes.append({'entity':c[':db/id'],'attribute':'tutorial/content','old':old,'new':c[':tutorial/content']});forms.append([kw('db/ensure'),c[':db/id'],kw('tutorial/validate')])
 (d/'lessons-after.json').write_text(json.dumps(after_lessons,indent=2))
# CAS guards on each changed cardinality-one old value; no global basis guard.
forms[:0]=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['old'],c['new']]for c in changes]
for e in sorted(affectedq):forms.append([kw('db/ensure'),e,kw('question/validate')])
for e in sorted(affectedf):forms.append([kw('db/ensure'),e,kw('answer-field/validate')])
for e in sorted(affecteda):forms.append([kw('db/ensure'),e,kw('answer/validate')])
(base/'transaction.edn').write_text(dumps(forms)+'\n');(base/'changes.json').write_text(json.dumps(changes,indent=2));(base/'detached-duplicates.json').write_text(json.dumps(detached,indent=2));(base/'repair-plan.json').write_text(json.dumps({'completions':complete,'mathematical_corrections':corrections,'changed_attributes':len(changes),'affected_questions':len(affectedq),'changed_answers':len(affecteda),'changed_fields':len(affectedf),'detached_duplicates':detached},indent=2))
print((base/'repair-plan.json').read_text())
