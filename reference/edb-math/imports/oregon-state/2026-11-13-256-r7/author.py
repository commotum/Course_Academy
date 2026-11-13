from pathlib import Path
import json,shutil,yaml
root=Path('/home/jake/Developer/study')
lessons={r['id']:r for r in json.load(open('/tmp/rec7-lessons.json'))}
def link(n):
 r=lessons[str(n)];return f"[{r['name']}](<{(root/r['path']).as_uri()}>)"
def links(t,p=()):
 return '**Topics:** '+'; '.join(link(n) for n in t)+'.\n**Prerequisites:** '+('; '.join(link(n) for n in p)+'.' if p else 'No additional prerequisite links needed.')+'\n\n\n'
def block(n,prompt,answer,feedback,free=False):
 q={'id':f'q-{n}','content':prompt,'fields':[{'key':'response' if free else 'answer','type':'free' if free else 'blank','correct':{'type':'text' if free else 'math','value':answer}}],'feedback':feedback}
 return '```quiz\n'+yaml.safe_dump(q,allow_unicode=True,sort_keys=False,width=110)+'```\n\n'
# One response per original problem. All required work remains in its prompt.
items=[
(1,2,r'''The set of functions $\{x^{-3},x\}$ solve
$$x^2y''+4xy'-y=0.$$
Show that $\{x^{-3},x\}$ form a fundamental set of solutions for $0<x<\infty$. Your solution must include a Wronskian calculation.

**Source conflict:** The worksheet and key print different equations here. The assertion is inconsistent with both printed versions. Preserve the requested Wronskian work and explain what the calculation actually establishes.''',r'''The requested conclusion is false for the printed ODE. With $y_1=x^{-3}$ and $y_2=x$, the derivatives are $y_1'=-3x^{-4}$ and $y_2'=1$, so
$$W=y_1y_2'-y_1'y_2=x^{-3}-(-3x^{-4})x=4x^{-3}\ne0\quad(x>0).$$
Thus the functions are linearly independent. But for $L[y]=x^2y''+4xy'-y$,
$$L[x^{-3}]=12x^{-3}-12x^{-3}-x^{-3}=-x^{-3},\qquad L[x]=4x-x=3x.$$
Neither function solves the printed equation, so they cannot be its fundamental set.

The key instead prints $x^2y''+3xy'-y=0$; its residuals are $2x^{-3}$ and $2x$, so that version also fails. The equation $x^2y''+3xy'-3y=0$ does have these two solutions, and the same nonzero Wronskian proves they form a fundamental set on $(0,\infty)$. This last equation is an authored possible correction, not a confirmed instructor correction.''',r'''A nonzero Wronskian proves independence; membership in the ODE's solution set must also hold. The key's Wronskian is correct, but it does not establish the claimed solution property. The instructor's intended correction remains unconfirmed.''',True,[2547],[35,1181]),
(2,2,r'''The set of functions $\{e^{3x},xe^{3x}\}$ solve
$$y''-6y'+9y=0.$$
Show that $\{e^{3x},xe^{3x}\}$ form a fundamental set of solutions for $0<x<\infty$. Your solution must include a Wronskian calculation.''',r'''For $y_1=e^{3x}$ and $y_2=xe^{3x}$,
$$y_1'=3e^{3x},\qquad y_2'=(1+3x)e^{3x}.$$
Hence
$$W=e^{3x}(1+3x)e^{3x}-(3e^{3x})(xe^{3x})=e^{6x}>0.$$
Both functions solve the ODE: $y_1''=9e^{3x}$ gives $(9-18+9)e^{3x}=0$, and $y_2''=(6+9x)e^{3x}$ gives $[(6+9x)-6(1+3x)+9x]e^{3x}=0$.
The coefficients are continuous on $(0,\infty)$, and the two solutions have nonzero Wronskian there. They therefore form a fundamental set on the required interval.''',r'''Apply the product rule to $xe^{3x}$; its derivative contains both $e^{3x}$ and $3xe^{3x}$. The $3xe^{6x}$ terms then cancel in the Wronskian.''',True,[2547],[1109,1007]),
(3,3,r'''Find the characteristic polynomial of the homogeneous second-order linear equation with constant coefficients
$$8y''-7y'+5y=0.$$
$p(r)=$ {{answer}}.''',r'8r^2-7r+5',r'''Substituting $y=e^{rx}$ yields $(8r^2-7r+5)e^{rx}=0$. The characteristic polynomial is $p(r)=8r^2-7r+5$; keep the coefficients and signs from the ODE.''',False,[614],[]),
(4,3,r'''Find the characteristic polynomial of the homogeneous second-order linear equation with constant coefficients
$$-3y''+7y=0.$$
$p(r)=$ {{answer}}.''',r'-3r^2+7',r'''The coefficients of $y''$, $y'$, and $y$ are $-3$, $0$, and $7$. Thus $p(r)=-3r^2+0r+7=-3r^2+7$. The absence of a $y'$ term gives a zero linear coefficient.''',False,[614],[]),
(5,3,r'''The homogeneous second-order linear equation $y''-4y'+4y=0$ has characteristic polynomial $p(r)=r^2-4r+4$. Find the solution(s) to $p(r)=0$.
$r=$ {{answer}}.''',r'2',r'''Factor $r^2-4r+4=(r-2)^2$. Therefore $r=2$ is the only distinct root, with multiplicity two. Substitution gives $4-8+4=0$.''',False,[375],[1425]),
(6,3,r'''The homogeneous second-order linear equation $y''-9y=0$ has characteristic polynomial $p(r)=r^2-9$. Find the solution(s) to $p(r)=0$.
$r=$ {{answer}}.''',r'\pm3',r'''Factor $r^2-9=(r-3)(r+3)$; either factor may be zero. The roots are $3$ and $-3$, written $\pm3$. Both square to $9$.''',False,[394],[]),
(7,4,r'''The characteristic equation $r^2-4r+4=0$ for $y''-4y'+4y=0$ has a single real solution $r=2$. Find the general solution to
$$y''-4y'+4y=0.$$
$y(x)=$ {{answer}}.''',r'(C_1+C_2x)e^{2x}',r'''The root $r=2$ is repeated. Two independent solutions are $e^{2x}$ and $xe^{2x}$, so $y=(C_1+C_2x)e^{2x}$, with arbitrary constants. Their Wronskian is $e^{4x}\ne0$, and each has residual zero in $y''-4y'+4y$. Repeating $e^{2x}$ without the factor $x$ would provide only one independent solution.''',False,[879],[]),
(8,4,r'''The characteristic equation $r^2+36=0$ for $y''+36y=0$ has solutions $r=\pm6i$. Find the general solution to
$$y''+36y=0.$$
$y(x)=$ {{answer}}.''',r'C_1\cos(6x)+C_2\sin(6x)',r'''For roots $\lambda\pm i\omega$, the real solution is $e^{\lambda x}(C_1\cos(\omega x)+C_2\sin(\omega x))$. Here $\lambda=0$ and $\omega=6$, so the exponential factor is $1$. Twice differentiating either trigonometric term multiplies it by $-36$, which verifies the ODE.''',False,[880],[]),
(9,5,r'''The indicial polynomial for
$$2x^2y''-3xy'+y=0$$
is $p(r)=2r(r-1)-3r+1$. Find the solutions $r$ to the indicial equation $p(r)=0$.
$r=$ {{answer}}.''',r'\frac{5\pm\sqrt{17}}{4}',r'''Expand first: $2r(r-1)-3r+1=2r^2-5r+1$. The quadratic formula gives $r=(5\pm\sqrt{25-8})/4=(5\pm\sqrt{17})/4$. Their sum is $5/2$ and product is $1/2$, agreeing with the coefficients of the quadratic.''',False,[422],[]),
(10,5,r'''The source states that the indicial equation
$$r^2+2r-3=0$$
for the Euler equation
$$y''+3xy'-3y=0$$
has solutions $r_1=-1$ and $r_2=3$. Find the general solution to
$$x^2y''+3xy'-3y=0.$$

**Source conflict:** The first displayed ODE omits the $x^2$ multiplying $y''$, and the stated roots do not solve the printed indicial equation. For the study answer, solve the final displayed ODE on $(0,\infty)$, using the Euler-theorem interval from page 1.

$y(x)=$ {{answer}}.''',r'C_1x+C_2x^{-3}',r'''Substitute $y=x^r$ into the final ODE to get $r(r-1)+3r-3=r^2+2r-3=(r-1)(r+3)=0$. Its actual roots are $1$ and $-3$, so $y=C_1x+C_2x^{-3}$ on $(0,\infty)$. Each term has residual zero in the final ODE.

The key follows the erroneous stated roots and gives $C_1x^{-1}+C_2x^3$. These terms have residuals $-4x^{-1}$ and $12x^3$, respectively, so that expression is not the general solution of the final printed equation. It would instead solve $x^2y''-xy'-3y=0$. The original wording is retained above; no instructor correction has been assumed.''',False,[2528],[375,1181])]
intro=r'''
**MTH 256 — Recitation 7: Quiz 3 Review**

Due: unknown
Date imported: 2026-11-13
Source: [MTH 256 F 2026 Recitation 7 Quiz 3 Review.pdf](<../source/256/R-7/MTH 256 F 2026 Recitation 7 Quiz 3 Review.pdf>)
Answer key: [MTH 256 F 2026 Recitation 7 Quiz 3 Review Key.pdf](<../source/256/R-7/MTH 256 F 2026 Recitation 7 Quiz 3 Review Key.pdf>)

Study answers and explanations are authored additions, independently checked against the downloaded key. Problems 1 and 10 contain source inconsistencies; their original wording is preserved and the verified conclusions are explained in the answer reveals. The instructor's intended corrections remain unconfirmed. Neither PDF specifies a due date.

## Topics

TOPICS

## Prerequisites

PREREQS

## Instructions

The recitation this week serves as a review for quiz three, which will be taken in the latter half of recitation time. It also prepares you for the wording on the quiz. The quiz covers Sections 5.1 and 5.2 and Euler equations from Section 7.4. The following definition and theorems will be provided on the quiz (source PDF p. 1).

### Wronskian definition

For two functions $\{y_1(x),y_2(x)\}$,
$$W(x)=y_1y_2'-y_1'y_2.$$

WRONSKIAN_LINKS
### Theorem 5.2.1 — Constant coefficients

Let $p(r)=ar^2+br+c$ be the characteristic polynomial of
$$ay''+by'+cy=0.\tag{5.2.20}$$

(a) If $p(r)=0$ has distinct real roots $r_1,r_2$, then the general solution is
$$y=c_1e^{r_1x}+c_2e^{r_2x}.$$

(b) If it has a repeated root $r_1$, then the general solution is
$$y=e^{r_1x}(c_1+c_2x).$$

(c) If it has complex conjugate roots $r_1=\lambda+i\omega$ and $r_2=\lambda-i\omega$, where $\omega>0$, then the general solution is
$$y=e^{\lambda x}(c_1\cos\omega x+c_2\sin\omega x).$$

CONSTANT_LINKS
### Theorem 7.4.3 — Euler equations

Suppose the roots of the indicial equation
$$ar(r-1)+br+c=0\tag{7.4.11}$$
are $r_1,r_2$. Then the general solution of the Euler equation
$$ax^2y''+bxy'+cy=0\tag{7.4.12}$$
on $(0,\infty)$ is

- $y=c_1x^{r_1}+c_2x^{r_2}$ if $r_1,r_2$ are distinct real numbers;
- $y=x^{r_1}(c_1+c_2\ln x)$ if $r_1=r_2$;
- $y=x^\lambda[c_1\cos(\omega\ln x)+c_2\sin(\omega\ln x)]$ if $r_1,r_2=\lambda\pm i\omega$ with $\omega>0$.

EULER_LINKS'''
topics=list(dict.fromkeys([2547,614,879,880,2528,2544,2545]+[n for i in items for n in i[-2]]))
prereqs=list(dict.fromkeys(n for i in items for n in i[-1]))
intro=intro.replace('TOPICS','\n'.join('- '+link(n) for n in topics)).replace('PREREQS','\n'.join('- '+link(n) for n in prereqs)).replace('WRONSKIAN_LINKS',links([2547])).replace('CONSTANT_LINKS',links([614,879,880])).replace('EULER_LINKS',links([2528,2544,2545]))
text=intro
for n,page,prompt,answer,feedback,free,t,p in items:
 text+='---\n\n'+f'## Problem {n}\n\nSource question: PDF p. {page}, Problem {n}.\n\n'+block(n,prompt,answer,feedback,free)+links(t,p)
path=root/'vault/F26/256/Undated_R-7.md';assert not path.exists();path.write_text(text.rstrip()+'\n')
dest=root/'vault/F26/source/256/R-7';dest.mkdir(parents=True,exist_ok=True)
for name in ['MTH 256 F 2026 Recitation 7 Quiz 3 Review.pdf','MTH 256 F 2026 Recitation 7 Quiz 3 Review Key.pdf']:shutil.copy2(Path('/home/jake/Downloads')/name,dest/name)
print(path);print('10 problems, 10 quiz blocks; topic union',len(set(topics+prereqs)),sorted(set(topics+prereqs)))
