from pathlib import Path
import csv,json,yaml,re
R=Path('/home/jake/Developer/study');V=R/'vault/F26';H=Path('/tmp/ingest-256-exams')
paths=json.loads((H/'lesson-paths.json').read_text())
paths['1887']='MA/Test-Preparation/SMF/11. Advanced Algebra - Functions/11.1. Functions/Lessons/11.1.5. The Vertical Line Test.md'
used={}
def link(i):
 if i in used:return used[i]
 p=R/paths[str(i)];assert f'lesson-id: {i}'in p.read_text();used[i]=f'[{p.read_text().splitlines()[0][2:]}](<{p.resolve().as_uri()}>)';return used[i]
class Dumper(yaml.SafeDumper):pass
def rep(d,s):return d.represent_scalar('tag:yaml.org,2002:str',s,style='|' if '\n' in s else None)
Dumper.add_representer(str,rep)
def q(id,prompt,kind,value,feedback):
 return {'id':id,'content':prompt,'fields':[{'key':'answer','type':kind,'correct':{'type':'math'if kind=='blank'else'text','value':value}}],'feedback':feedback}
def checks(id,prompt,selected,feedback,options):
 return {'id':id,'content':prompt,'fields':[{'key':'curves','type':'checkbox','choices':[{'id':c,'type':'text','value':c,'feedback':options[c]}for c in 'ABCDEF'],'correct':list(selected)}],'feedback':feedback}
def mapping(topics,prereq=(),gap=None,components=None):
 text=('No whole-task equivalent verified for '+gap+'. Component coverage: 'if gap else '')+'; '.join(link(i)+(f' ({components[i]})'if components and i in components else '')for i in topics)
 return '**Topics:** '+text+'\n**Prerequisites:** '+('; '.join(link(i)for i in prereq)if prereq else'No additional prerequisite links needed.')+'\n\n\n'
def part(block,topics,pre=(),gap=None,components=None):return block,mapping(topics,pre,gap,components)
def render(block):return '```quiz\n'+yaml.dump(block,Dumper=Dumper,allow_unicode=True,sort_keys=False,width=110).rstrip()+'\n```\n\n'
e1=[]
optsA={c:('The curve follows the field directions, including its turning portions.'if c in'AB'else'The curve follows the field directions on its regular portions.'if c in'CDE'else'The drawn curve cuts across field segments; near x=0 its slope disagrees with the field.')for c in'ABCDEF'}
optsB={c:('The complete curve folds back in x and fails the vertical line test.'if c in'AB'else'This curve is locally a graph y(x), tangent to the field where the ODE is defined.'if c in'CDE'else'This is a graph, but it is not tangent to the field.')for c in'ABCDEF'}
e1.append(('Source question: Problem 1(a–b), PDF page 2 (10 points: 5 per part).',r'''The direction field for

$$y'=\frac{2x}{4y-3y^2}$$

and curves $A$–$F$ are shown below. The source says no supporting work is required for this problem.

![Direction field with curves A through F](../source/256/E-1/direction-field-curves.png)''',[
part(checks('mth256-e1-1a','**(a)** Which curves are integral curves? Select all that apply.','ABCDE',r'''In the source's geometric convention, $A,B,C,D,E$ are integral curves: their tangents follow the field. Curve $F$ does not.

Separating variables gives $(4y-3y^2)\,dy=2x\,dx$, so regular integral-curve pieces lie on levels of $2y^2-y^3-x^2=C$. Differentiating this relation recovers the ODE wherever $y\ne0,4/3$. The displayed folds and loop are allowed for geometric integral curves; they need not each be one graph $y(x)$.''',optsA),[3350],gap='distinguishing geometric integral curves from solution graphs',components={3350:'reading slope signs and tangency; the integral-curve distinction remains uncovered'}),
part(checks('mth256-e1-1b','**(b)** Which curves are solution curves? Select all that apply.','CDE',r'''The indicated solution curves are $C,D,E$. They follow the field and pass the vertical line test on their regular graph portions. Curves $A$ and $B$ follow the field geometrically but fold back and do not represent single-valued functions of $x$; $F$ is not tangent to the field.

The differential equation is undefined on $y=0$ and $y=4/3$. A classical solution is considered only on an open interval where the selected graph avoids those lines; the apparent meeting point at the origin is excluded.''',optsB),[3350],[1887],gap='classifying solution graphs in this singular direction field',components={3350:'tangency and slope signs; global integral-curve classification remains uncovered'})]))
e1.append(('Source question: Problem 2(a–c), PDF page 3 (4, 4, and 2 points); page 6 contains additional handwritten work.','',[
part(q('mth256-e1-2a',r"**(a)** Verify that $y=1/(5-x)$ is a solution of $y'=y^2$.",'free',r'''For $x\ne5$,

$$y'=(5-x)^{-2}=\frac1{(5-x)^2}=y^2.$$

Hence the function solves the ODE on each interval $(-\infty,5)$ and $(5,\infty)$.''',r'''Differentiate the proposed function and compare with the square of the function. The chain rule contributes two minus signs: $\frac{d}{dx}(5-x)^{-1}=-(5-x)^{-2}(-1)$. Merely integrating or rewriting the function does not verify the equation.'''),[1181],[1108]),
part(q('mth256-e1-2b',r"**(b)** Verify that $y=1/(c-x)$, where $c$ is a constant, is a solution of $y'=y^2$.",'free',r'''Treating $c$ as constant, $y'=(c-x)^{-2}=y^2$ for $x\ne c$. Thus every fixed real $c$ gives solutions on intervals not crossing $x=c$.''',r'''Differentiate with respect to $x$ while holding $c$ fixed. Both sides equal $1/(c-x)^2$. The singular value $x=c$ must be excluded.'''),[1181],[1108]),
part(q('mth256-e1-2c',r"**(c)** Solve $y'=y^2$, $y(1)=1$."+'\n\n$y=$ {{answer}}.','blank',r'\frac1{2-x}',r'''The family in part (b) gives $1=1/(c-1)$, so $c=2$ and $y=1/(2-x)$. Its maximal interval containing $x=1$ is $(-\infty,2)$. Check that $y'=1/(2-x)^2=y^2$ and $y(1)=1$. The equilibrium $y=0$ does not satisfy this initial condition.'''),[1179])]))
e1.append(('Source question: Problem 3, PDF page 4 (10 points).','',[
part(q('mth256-e1-3',r"Solve the initial value problem $y'=2\cos x$, $y(0)=3$."+'\n\n$y=$ {{answer}}.','blank',r'2\sin x+3',r'''Integration gives $y=2\sin x+C$. At $x=0$, $3=C$, so $y=2\sin x+3$ on $\mathbb R$. Its derivative is $2\cos x$ and its value at zero is $3$.'''),[1061],[285])]))
e1.append(('Source question: Problem 4(a–b), PDF page 5 (10 points total).',r'''This problem assumes the integrating-factor method from lecture. If you prefer variation of parameters, you may skip part (a); in that case part (b) counts for the full 10 points.''',[
part(q('mth256-e1-4a',r"**(a)** Compute an integrating factor for $y'-y=e^x$."+'\n\n$I(x)=$ {{answer}}.','blank',r'e^{-x}',r'''The standard form is $y'+P(x)y=Q(x)$ with $P(x)=-1$. Thus $I(x)=e^{\int-1\,dx}=e^{-x}$. Any nonzero constant multiple works; the normalized factor is shown.'''),[877]),
part(q('mth256-e1-4b',r"**(b)** Solve $y'-y=e^x$, $y(0)=1$, using the integrating-factor method or the permitted variation-of-parameters alternative."+'\n\n$y=$ {{answer}}.','blank',r'(x+1)e^x',r'''Multiplication by $e^{-x}$ gives $(e^{-x}y)'=1$. Hence $e^{-x}y=x+C$, or $y=e^x(x+C)$. The initial condition gives $C=1$. Differentiation checks $y'-y=e^x$ on $\mathbb R$. Notice that $xe^x+1$ would not satisfy the ODE.'''),[877])]))

theorem=r'''The supplied Theorem 2.3.1 concerns $y'=f(x,y)$, $y(x_0)=y_0$:

- If $f$ is continuous on an open rectangle $R=\{(x,y):a<x<b,\ c<y<d\}$ containing $(x_0,y_0)$, at least one solution exists on some open subinterval of $(a,b)$ containing $x_0$.
- If both $f$ and $f_y$ are continuous on $R$, the solution is unique on some such open subinterval.

Consider

$$y'=(xy)^{3/5},\qquad y(x_0)=y_0.$$

Hint: $h(s)=s^{1/5}$ is continuous for every real $s$. You need not identify all rectangles. For full credit, clearly identify $f(x,y)$ and $f_y(x,y)$ and state where each is continuous.'''
e2=[]
e2.append(('Source question: Problem 1(a–c), printed/PDF page 2; page 3 is spare workspace.',r'''Consider $y'=3e^{-y}x^2$. Hint: $\ln(1)=0$.''',[
part(q('mth256-e2-1a','**(a)** Find all implicit solutions.\n\nWrite an equivalent relation in the form {{answer}} $=C$.','blank',r'e^y-x^3',r'''Multiply by $e^y$ and integrate: $e^y\,dy=3x^2\,dx$, giving $e^y=x^3+C$. Thus $e^y-x^3=C$. The relation is used where $x^3+C>0$. No equilibrium solutions are lost because $e^{-y}$ is never zero.'''),[466],[308]),
part(q('mth256-e2-1b','**(b)** Find all solutions to the equation.','free',r'''For any $C\in\mathbb R$,

$$y(x)=\ln(x^3+C),\qquad x\in(-\sqrt[3]{C},\infty).$$

These are the maximal real solution intervals; restrictions to smaller open intervals are also solutions.''',r'''Apply the natural logarithm to $e^y=x^3+C$. Its argument must be positive, so $x>\sqrt[3]{-C}=-\sqrt[3]{C}$. Differentiating gives $y'=3x^2/(x^3+C)=3x^2e^{-y}$. Do not put absolute values inside the logarithm: the separated relation has $e^y>0$.'''),[466],[818],gap='listing all logarithmic solution branches with maximal domains',components={466:'separating variables and converting an implicit exponential relation to a logarithm'}),
part(q('mth256-e2-1c',r'**(c)** Solve the IVP with $y(2)=0$.'+'\n\n$y=$ {{answer}}.','blank',r'\ln(x^3-7)',r'''Substitute into $e^y=x^3+C$: $1=8+C$, so $C=-7$. Therefore $y=\ln(x^3-7)$ on $(\sqrt[3]{7},\infty)$. This interval contains $2$, and $y(2)=\ln1=0$.'''),[1179],[818])]))
e2.append(('Source question: Problem 2(a–b), printed/PDF page 4; page 5 is handwritten continuation.',theorem,[
part(q('mth256-e2-2a',r'**(a)** Find every $(x_0,y_0)$ for which Theorem 2.3.1 guarantees at least one local solution. Identify $f$ and $f_y$ and their continuity sets as directed above.','free',r'''Every $(x_0,y_0)\in\mathbb R^2$ qualifies for existence. Here $f(x,y)=(xy)^{3/5}$ is continuous on all of $\mathbb R^2$: it is the composition of the continuous product $xy$, the real fifth-root function, and cubing.

For $y\ne0$,

$$f_y(x,y)=\frac35x^{3/5}y^{-2/5}.$$

This partial derivative is continuous on the open set $y\ne0$. At $(0,0)$ the partial derivative exists and equals $0$, but it is not continuous there. At $y=0$, $x\ne0$, the partial derivative does not exist. Existence requires continuity of $f$ only.''',r'''The odd denominator in the exponent allows negative arguments: $(xy)^{3/5}$ is real and continuous everywhere. Do not discard the axes for existence. Part (a) uses condition (a) of the theorem, not the stronger derivative condition for uniqueness.'''),[1931,4096],[1600,1108],gap='applying Theorem 2.3.1 to guarantee local existence',components={1931:'continuity of a multivariable function',4096:'computing the partial derivative; the ODE theorem itself remains uncovered'}),
part(q('mth256-e2-2b',r'**(b)** Find every $(x_0,y_0)$ for which Theorem 2.3.1 guarantees a unique local solution. Identify $f$ and $f_y$ and their continuity sets as directed above.','free',r'''The guaranteed set is $\{(x_0,y_0)\in\mathbb R^2:y_0\ne0\}$. The function $f(x,y)=(xy)^{3/5}$ is continuous everywhere, while $f_y=\frac35x^{3/5}y^{-2/5}$ is continuous on $y\ne0$.

If $y_0\ne0$, choose a small open rectangle that avoids $y=0$. Both continuity hypotheses then hold. If $y_0=0$, every open rectangle contains points $(x,0)$ with $x\ne0$, where $f_y$ does not exist, so the theorem does not guarantee uniqueness. The value $f_y(0,0)=0$ alone does not give continuity on a rectangle.''',r'''A theorem's sufficient hypotheses must hold throughout a neighborhood, not merely at the initial point. In particular, $x_0=0$ does not rescue $y_0=0$. Failure of the theorem's hypotheses means no uniqueness guarantee from this theorem; it is not by itself a proof of nonuniqueness.'''),[1931,4096],[1108],gap='applying Theorem 2.3.1 to guarantee local uniqueness',components={1931:'continuity on an open neighborhood',4096:'computing and locating singularities of the partial derivative; the theorem application remains uncovered'})]))
e2.append(('Source question: Problem 3, printed/PDF page 6.',r'''Find all implicit solutions of

$$y'=\frac{12x^3+9x^2+1}{10y^4+6y^2+2y+3}.$$''',[
part(q('mth256-e2-3','Write the implicit relation as {{answer}} $=C$.','blank',r'2y^5+2y^3+y^2+3y-3x^4-3x^3-x',r'''Separate and integrate:

$$\int(10y^4+6y^2+2y+3)\,dy=\int(12x^3+9x^2+1)\,dx,$$

so $2y^5+2y^3+y^2+3y=3x^4+3x^3+x+C$. Differentiating recovers the ODE. Its denominator is positive for all real $y$, since

$$10y^4+6y^2+2y+3=10y^4+6(y+1/6)^2+17/6>0.$$

Thus no denominator-zero values must be removed from this implicit family.'''),[466],[308,3769])]))
e2.append(('Source question: Problem 4(a–c), printed/PDF page 7; page 8 is spare workspace.',r'''Consider $y'=2x^3/y$.''',[
part(q('mth256-e2-4a','**(a)** Find all implicit solutions.\n\nWrite the relation as {{answer}} $=C$.','blank',r'y^2-x^4',r'''On any solution interval $y\ne0$, multiply by $y$ and integrate: $\frac12y^2=\frac12x^4+K$. Renaming $C=2K$ gives $y^2-x^4=C$. The ODE excludes the points with $y=0$.'''),[466],[308]),
part(q('mth256-e2-4b','**(b)** Find all solutions to the equation.','free',r'''All real solutions are restrictions of

$$y(x)=\varepsilon\sqrt{x^4+C},\qquad \varepsilon\in\{-1,1\},$$

with fixed $C\in\mathbb R$ and fixed sign on a connected interval where $x^4+C>0$. The maximal intervals are:

- $C>0$: $\mathbb R$;
- $C=0$: $(-\infty,0)$ or $(0,\infty)$;
- $C<0$: $(-\infty,-(-C)^{1/4})$ or $((-C)^{1/4},\infty)$.

There is no $y=0$ solution because the equation is undefined there.''',r'''Solving $y^2=x^4+C$ gives both signs. Require strict positivity, because equality would give $y=0$ and make the original equation undefined. A continuous nonzero solution cannot change sign inside its interval. Differentiate either branch to check $y'=2x^3/y$.'''),[466],[430,802],gap='classifying both radical solution branches and every maximal interval',components={466:'separation and the implicit solution family'}),
part(q('mth256-e2-4c',r'**(c)** Solve the IVP with $y(1)=-2$.'+'\n\n$y=$ {{answer}}.','blank',r'-\sqrt{x^4+3}',r'''The condition gives $(-2)^2=1+C$, hence $C=3$. The negative initial value selects the negative branch: $y=-\sqrt{x^4+3}$ on all of $\mathbb R$. The positive branch would give $y(1)=2$ and fails the initial condition. Differentiation gives $y'=-2x^3/\sqrt{x^4+3}=2x^3/y$.'''),[1179],[430])]))

def save_exam(n,day,problems):
 allmaps=''.join(m for _,_,parts in problems for _,m in parts);topic_ids=set();pre_ids=set()
 for line in allmaps.splitlines():
  target=topic_ids if line.startswith('**Topics:**')else pre_ids if line.startswith('**Prerequisites:**')else None
  if target is not None:
   for i,label in list(used.items()):
    if label in line:target.add(i)
 # A topic may be a prerequisite in another part; keep the summaries disjoint.
 pre_ids-=topic_ids
 intro=f'\n**MTH 256 — E{n} (source title: Quiz {n})**\n\nDue: 2026-10-{day}\nExam date: 2026-10-{day}\nDate source: user-provided exam date; no submission time supplied\nDate imported: 2026-11-08\nSource: [256-E-{n}.pdf](<../source/256/E-{n}/256-E-{n}.pdf>)\n\nThe complete scan preserves the student’s handwritten work. Quiz answers, worked explanations, and branch/domain corrections in this note are independently authored study additions, not an instructor key.\n\n## Topics\n\n'
 intro+='\n'.join('- '+link(i)for i in sorted(topic_ids))+'\n\n## Prerequisites\n\n'+'\n'.join('- '+link(i)for i in sorted(pre_ids))
 intro+='\n\n## Instructions\n\nThe original assessment contains four problems worth 40 points and allows 40 minutes. Wait for the TA to begin and start the timer. Only a writing implement and eraser are permitted; calculators are not allowed. Complete all four problems.'
 if n==1:intro+=' Problem 1 requires no supporting work. Problem 4 allows the stated variation-of-parameters alternative.'
 else:intro+=' The source provides blank pages after Problems 1, 2, and 4 for additional work. Problem 2 requires the supplied existence-and-uniqueness theorem and explicit continuity statements.'
 intro+=('\n\nStudy-link coverage is partial for distinguishing geometric integral curves from solution graphs. The vertical-line-test supporting link is outside the normal route (Test Preparation).\n' if n==1 else '\n\nStudy-link coverage is partial for applying the existence-and-uniqueness theorem and for full branch/domain classifications. The continuity and partial-derivative links supply verified components from Multivariable Calculus, outside the normal course route.\n')
 for j,(source,context,parts)in enumerate(problems,1):
  intro+=f'\n---\n\n## Problem {j}\n\n{source}\n\n'+(context+'\n\n'if context else'')
  for block,m in parts:intro+=render(block)+m
 path=V/f'256/10-{day}-26_E-{n}.md';assert not path.exists();path.write_text(intro)
 return {'source':str(path.relative_to(R/'vault')),'exam':n,'date':f'2026-10-{day}','problems':4,'quizzes':sum(len(parts)for _,_,parts in problems),'source_pages':6 if n==1 else 8}
meta=[save_exam(1,'06',e1),save_exam(2,'20',e2)];(H/'inventory.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
