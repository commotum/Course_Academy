from pathlib import Path
import csv, shutil, yaml

ROOT=Path('/home/jake/Developer/study')
DEST=ROOT/'vault/F26/341/11-11-26_WHW-6.md'
SOURCE=ROOT/'vault/F26/source/341/WHW-6'
assert not DEST.exists()
SOURCE.mkdir(parents=True,exist_ok=True)
shutil.copy2('/home/jake/Downloads/MTH341-WHW6.pdf',SOURCE/'MTH341-WHW6.pdf')
lessons={}
for file in ['MA/Mathematical-Foundations/catalog.csv','MA/Mathematical-Analysis-&-Modeling/LAL/topics.csv']:
    for r in csv.DictReader(open(ROOT/file)):
        p=Path(r['lesson-path'])
        p=ROOT/p if str(p).startswith('MA/') else ROOT/Path(file).parent/p
        lessons[int(r['topic-id'])]=(r['topic-name'],p)
def link(n):
    name,p=lessons[n]
    assert p.is_file() and f'lesson-id: {n}' in p.read_text()
    return f'[{name}](<{p.resolve().as_uri()}>)'
def blank(key,value):return {'key':key,'type':'blank','correct':{'type':'math','value':value}}
def free(value):return {'key':'response','type':'free','correct':{'type':'text','value':value}}
def quiz(id,content,fields,feedback):return dict(id=id,content=content,fields=fields,feedback=feedback)
items=[]
def add(number,source,blocks,topics,prereqs,gap=None,context=''):
    items.append(dict(number=number,source=source,blocks=blocks,topics=topics,prereqs=prereqs,gap=gap,context=context))

add(1,'Assignment item (1), handout p. 1.',[
 quiz('q-1',r'''Suppose $A$ is a $7\times9$ matrix with $\operatorname{nullity}(A)=2$. What is the dimension of the row space of $A$? Briefly justify your answer. Remember that an example is just an example; it does not cover every possibility.

$\dim\operatorname{Row}(A)=$ {{dimension}}. Give the justification in the written response.''',
 [blank('dimension','7'),free(r'''The rank-nullity theorem uses the number of columns, so $\operatorname{rank}(A)+\operatorname{nullity}(A)=9$. Thus $\operatorname{rank}(A)=9-2=7$. Row rank equals column rank, so $\dim\operatorname{Row}(A)=7$. This applies to every matrix satisfying the hypotheses.''')],
 r'Use the nine columns for rank-nullity. The resulting rank is also the dimension of the row space; the seven rows give a consistent upper bound, not the initial rank-nullity total.')
],[(3836,'rank from nullity'),(2200,'row-space and null-space relationship')],[],
 gap='deducing row-space dimension from nullity with a general justification')

add(2,'Assignment item (2); Kuttler 2017A, Exercise 5.2.4, printed p. 278 (PDF p. 290). The handout recommends Procedure 5.10 and Example 5.11.',[
 quiz('q-2',r'''Suppose $T$ is a linear transformation such that
$$T\!\begin{pmatrix}1\\1\\-8\end{pmatrix}=\begin{pmatrix}1\\3\\1\end{pmatrix},\qquad
T\!\begin{pmatrix}-1\\0\\6\end{pmatrix}=\begin{pmatrix}2\\4\\1\end{pmatrix},\qquad
T\!\begin{pmatrix}0\\-1\\3\end{pmatrix}=\begin{pmatrix}6\\1\\-1\end{pmatrix}.$$
Find the matrix $A$ of $T$, that is, $T(\mathbf x)=A\mathbf x$. Show supporting work.

$A=$ {{matrix}}.''',
 [blank('matrix',r'\begin{pmatrix}52&21&9\\44&23&8\\5&4&1\end{pmatrix}'),free(r'''Put the input vectors in the columns of $P$ and their images in the matching columns of $Q$:
$$P=\begin{pmatrix}1&-1&0\\1&0&-1\\-8&6&3\end{pmatrix},\qquad Q=\begin{pmatrix}1&2&6\\3&4&1\\1&1&-1\end{pmatrix}.$$
The required equation is $AP=Q$. Since $\det P=1$, the inputs form a basis and $A=QP^{-1}$. Here
$$P^{-1}=\begin{pmatrix}6&3&1\\5&3&1\\6&2&1\end{pmatrix},\qquad
A=\begin{pmatrix}52&21&9\\44&23&8\\5&4&1\end{pmatrix}.$$
Checking $AP=Q$ verifies all three prescribed images. For example, the first image is $(52+21-72,44+23-64,5+4-8)^T=(1,3,1)^T$.''')],
 r'The given inputs are not the standard basis: their images are the columns of $AP$, not directly the columns of $A$. Solve $AP=Q$ by right-multiplying by $P^{-1}$, or solve the three corresponding systems for the rows of $A$.')
],[(2211,'standard matrix from standard-basis images'),(865,'extend prescribed images by linearity'),(1196,'matrix product in $AP=Q$')],[1733],
gap='recovering a standard matrix from the images of a nonstandard basis')

add(3,'Assignment item (3); Kuttler 2017A, Exercise 5.2.8(a)–(b), printed p. 279 (PDF p. 291). The handout cites p. 280; the assigned parts are on the preceding page.',[
 quiz('q-3a',r'''**(a)** $T\!\begin{pmatrix}x\\y\\z\end{pmatrix}=\begin{pmatrix}x+2y+3z\\2y-3x+z\end{pmatrix}$.

Show that $T$ is linear and determine $A$ such that $T(\mathbf x)=A\mathbf x$.

$A=$ {{matrix}}. Give the linearity justification in the written response.''',
 [blank('matrix',r'\begin{pmatrix}1&2&3\\-3&2&1\end{pmatrix}'),free(r'''In the variable order $x,y,z$, the coefficient rows are $(1,2,3)$ and $(-3,2,1)$. Thus
$$T(\mathbf x)=A\mathbf x,\qquad A=\begin{pmatrix}1&2&3\\-3&2&1\end{pmatrix}.$$
For arbitrary $\mathbf u,\mathbf v\in\mathbb R^3$ and $\alpha,\beta\in\mathbb R$,
$$T(\alpha\mathbf u+\beta\mathbf v)=A(\alpha\mathbf u+\beta\mathbf v)=\alpha A\mathbf u+\beta A\mathbf v=\alpha T(\mathbf u)+\beta T(\mathbf v).$$
This proves linearity, including both additivity and homogeneity.''')],
 r'Reorder the second component as $-3x+2y+z$ before reading its coefficients. A $2\times3$ matrix has three input components and two output components; distributivity proves linearity.'),
 quiz('q-3b',r'''**(b)** $T\!\begin{pmatrix}x\\y\\z\end{pmatrix}=\begin{pmatrix}7x+2y+z\\3x-11y+2z\end{pmatrix}$.

Show that $T$ is linear and determine $A$ such that $T(\mathbf x)=A\mathbf x$.

$A=$ {{matrix}}. Give the linearity justification in the written response.''',
 [blank('matrix',r'\begin{pmatrix}7&2&1\\3&-11&2\end{pmatrix}'),free(r'''Reading coefficients in the order $x,y,z$ gives
$$A=\begin{pmatrix}7&2&1\\3&-11&2\end{pmatrix},\qquad T(\mathbf x)=A\mathbf x.$$
For all $\mathbf u,\mathbf v\in\mathbb R^3$ and scalars $\alpha,\beta$,
$$T(\alpha\mathbf u+\beta\mathbf v)=A(\alpha\mathbf u+\beta\mathbf v)=\alpha A\mathbf u+\beta A\mathbf v=\alpha T(\mathbf u)+\beta T(\mathbf v).$$
Therefore $T$ is linear.''')],
 r'Keep the coefficient $-11$ in the second row and second column. Writing a formula as $A\mathbf x$ and applying matrix distributivity provides a general proof, rather than testing a few vectors.')
],[(907,None),(865,None)],[1195],context=r'For each assigned function $T:\mathbb R^3\to\mathbb R^2$, show that it is a linear transformation and determine its matrix. Only parts (a) and (b) are assigned.')

add(4,'Assignment item (4); Kuttler 2017A, Exercise 5.2.9(a) only, printed p. 280 (PDF p. 292).',[
 quiz('q-4',r'''Consider $T:\mathbb R^3\to\mathbb R^2$ defined by
$$T\!\begin{pmatrix}x\\y\\z\end{pmatrix}=\begin{pmatrix}x+2y+3z+1\\2y-3x+z\end{pmatrix}.$$
Explain why $T$ is not linear.''',
 [free(r'''Every linear map sends the zero vector to the zero vector, because $T(\mathbf0)=T(0\mathbf v)=0T(\mathbf v)=\mathbf0$. Here
$$T\!\begin{pmatrix}0\\0\\0\end{pmatrix}=\begin{pmatrix}1\\0\end{pmatrix}\ne\begin{pmatrix}0\\0\end{pmatrix}.$$
Therefore this $T$ is not linear. This single counterexample disproves a property that a linear map must satisfy for every input.''')],
 r'Test a necessary linearity property. The constant $+1$ makes the zero input produce a nonzero output. A counterexample disproves linearity; checking a few successful inputs would not prove it.')
],[(865,'test homogeneity; the zero-vector test is the scalar-zero case')],[],gap='the affine-map counterexample in $\mathbb R^3\to\mathbb R^2$')

add(5,'Assignment item (5); Kuttler 2017A, Exercise 5.3.2, printed p. 285 (PDF p. 297).',[
 quiz('q-5',r'''Let $T$ be the linear transformation induced by
$$A=\begin{pmatrix}3&1\\-1&2\end{pmatrix},$$
and let $S$ be the linear transformation induced by
$$B=\begin{pmatrix}0&-2\\4&2\end{pmatrix}.$$
Find the matrix of $S\circ T$ and find $(S\circ T)(\mathbf x)$ for $\mathbf x=\begin{pmatrix}2\\-1\end{pmatrix}$. Show supporting work.

Matrix of $S\circ T$: {{matrix}}.

$(S\circ T)(\mathbf x)=$ {{image}}.''',
 [blank('matrix',r'\begin{pmatrix}2&-4\\10&8\end{pmatrix}'),blank('image',r'\begin{pmatrix}8\\12\end{pmatrix}'),free(r'''The composition applies $T$ first, then $S$, so $(S\circ T)(\mathbf x)=B(A\mathbf x)=(BA)\mathbf x$. Thus
$$BA=\begin{pmatrix}0&-2\\4&2\end{pmatrix}\begin{pmatrix}3&1\\-1&2\end{pmatrix}=\begin{pmatrix}2&-4\\10&8\end{pmatrix}.$$
Then
$$\begin{pmatrix}2&-4\\10&8\end{pmatrix}\begin{pmatrix}2\\-1\end{pmatrix}=\begin{pmatrix}8\\12\end{pmatrix}.$$
Independently, $T(2,-1)^T=(5,-4)^T$, and $S(5,-4)^T=(8,12)^T$, confirming the order and result.''')],
 r'Composition is read from right to left: $T$ acts first, so $A$ is the right-hand matrix in $BA$. Check the result by evaluating $T(\mathbf x)$ and then $S(T(\mathbf x))$ separately.')
],[(1985,'order of function composition'),(1196,'multiply the transformation matrices'),(1195,'evaluate the resulting matrix on a vector')],[],gap='forming and evaluating the matrix of a composite linear transformation')

add(6,'Assignment item (6); Kuttler 2017A, Exercise 5.3.5, printed p. 286 (PDF p. 298).',[
 quiz('q-6',r'''Let $T$ be the linear transformation induced by
$$A=\begin{pmatrix}2&1\\5&2\end{pmatrix}.$$
Find the matrix of $T^{-1}$. Show supporting work.

Matrix of $T^{-1}$: {{matrix}}.''',
 [blank('matrix',r'\begin{pmatrix}-2&1\\5&-2\end{pmatrix}'),free(r'''The determinant is $\det A=2\cdot2-1\cdot5=-1\ne0$, so the inverse transformation exists. It is induced by
$$A^{-1}=\frac1{-1}\begin{pmatrix}2&-1\\-5&2\end{pmatrix}=\begin{pmatrix}-2&1\\5&-2\end{pmatrix}.$$
Multiplying in either order gives $AA^{-1}=A^{-1}A=I_2$, so $\mathbf x\mapsto A^{-1}\mathbf x$ reverses $T$.''')],
 r'The matrix of the inverse transformation is the inverse matrix. Check the determinant before using the $2\times2$ inverse formula, and distribute its negative reciprocal to every entry.')
],[(864,'compute the inverse matrix'),(1962,'inverse transformation and bijectivity')],[],gap='computing the matrix of an inverse linear transformation')

add(7,'Assignment item (7); Kuttler 2017A, Exercise 5.4.6, printed p. 291 (PDF p. 303).',[
 quiz('q-7',r'''Find the matrix for the linear transformation which rotates every vector in $\mathbb R^2$ through an angle of $2\pi/3$ and then reflects across the $x$ axis. Show supporting work.

Matrix: {{matrix}}.''',
 [blank('matrix',r'\begin{pmatrix}-\frac12&-\frac{\sqrt3}{2}\\-\frac{\sqrt3}{2}&\frac12\end{pmatrix}'),free(r'''Using the standard positive (counterclockwise) rotation convention,
$$R=\begin{pmatrix}\cos(2\pi/3)&-\sin(2\pi/3)\\\sin(2\pi/3)&\cos(2\pi/3)\end{pmatrix}=\begin{pmatrix}-\frac12&-\frac{\sqrt3}{2}\\\frac{\sqrt3}{2}&-\frac12\end{pmatrix}.$$
Reflection across the $x$ axis has matrix $F=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$. Since rotation occurs first, the required matrix is
$$FR=\begin{pmatrix}-\frac12&-\frac{\sqrt3}{2}\\-\frac{\sqrt3}{2}&\frac12\end{pmatrix}.$$
For a check, $e_1$ rotates to $(-1/2,\sqrt3/2)^T$, then reflects to $(-1/2,-\sqrt3/2)^T$, the first column. The second column follows from $e_2$ in the same way.''')],
 r'Write one matrix for each action and multiply in application order, with the first action on the right. Left multiplication by the $x$-axis reflection negates the second row of the rotation matrix.')
],[(932,'construct the rotation matrix'),(867,'construct the axis-reflection matrix'),(1196,'multiply the two matrices')],[1985],gap='composing a non-right-angle rotation with an axis reflection')

add(8,'Assignment item (8), handout p. 1.',[
 quiz('q-8',r'''Let $S$ and $T$ be linear transformations from $\mathbb R^n$ to $\mathbb R^n$, and let $\{\mathbf v_1,\ldots,\mathbf v_n\}$ be a basis for $\mathbb R^n$. Suppose $S(\mathbf v_i)=T(\mathbf v_i)$ for all $i=1,\ldots,n$. Show that $S=T$. (This says that a linear transformation is determined by a basis!)''',
 [free(r'''Let $\mathbf x\in\mathbb R^n$ be arbitrary. Since the $\mathbf v_i$ form a basis, there are scalars $c_1,\ldots,c_n$ with $\mathbf x=\sum_{i=1}^n c_i\mathbf v_i$. By linearity and the assumed equality on basis vectors,
$$S(\mathbf x)=S\!\left(\sum_{i=1}^n c_i\mathbf v_i\right)=\sum_{i=1}^n c_iS(\mathbf v_i)=\sum_{i=1}^n c_iT(\mathbf v_i)=T\!\left(\sum_{i=1}^n c_i\mathbf v_i\right)=T(\mathbf x).$$
Thus $S$ and $T$ agree on every vector in their common domain, so $S=T$. Spanning supplies the expansion; the proof does not require computing its coefficients.''')],
 r'Start with an arbitrary vector and expand it in the given basis. Apply linearity to both maps and use the hypothesis term by term. Agreement on the basis must be extended to every input before concluding that the functions are equal.')
],[(865,'linearity on sums and scalar multiples'),(1864,'express arbitrary vectors in a basis')],[],gap='proving equality of two linear transformations from agreement on a basis')

alltopics=list(dict.fromkeys(n for i in items for n,_ in i['topics']))
allpre=list(dict.fromkeys(n for i in items for n in i['prereqs']))
header='''
**MTH 341 — Written Homework 6**

Due: 2026-11-11
Due time: 23:59:00 America/Los_Angeles (PST).
Date imported: 2026-11-11
Source: [MTH341-WHW6.pdf](../source/341/WHW-6/MTH341-WHW6.pdf)
Deadline and rubric: [Canvas — Written Homework #6](https://canvas.oregonstate.edu/courses/2064363/assignments/10695099), verified 2026-11-11. Canvas displays Wednesday at 11:59 p.m.; availability ends November 12 at 11:59 p.m.

Question source: [Kuttler, *A First Course in Linear Algebra*, 2017A](../source/341/Kuttler-LinearAlgebra-AFirstCourse-2017A.pdf). Printed-page and PDF-page positions are distinguished below. The handout's reference to p. 280 for Exercise 5.2.8(a)–(b) points one page after those parts.

Study answers and explanations are independently authored additions, not publisher-provided solutions. Historical dates in the handout's hidden text layer do not set the current deadline.

## Topics

'''
header+='\n'.join('- '+link(n) for n in alltopics)+'\n\n## Prerequisites\n\n'
header+='\n'.join('- '+link(n) for n in allpre)+'''

## Instructions

Write solutions on separate letter-size (8.5 × 11 in.) or A4 paper and use the handout as a cover sheet, including your name and student ID. Canvas also permits writing on the PDF with a tablet or typesetting the work. Show all work and write neatly. Scan or export the completed work as a PDF and upload it to this Canvas assignment by the posted deadline. The general Canvas description mentions Gradescope; its numbered instructions and submission control specify uploading here. Late homework is not accepted; turn in completed work by the deadline even if some problems remain unfinished.

Technology such as WolframAlpha may be used to row-reduce matrices unless a problem says otherwise. The rubric awards 8 points for completion and 2 points for correctness of Problem 1.
'''
out=header
for i in items:
    out+='\n---\n\n## Problem '+str(i['number'])+'\n\nSource question: '+i['source']+'\n\n'
    if i['context']:out+=i['context']+'\n\n'
    for b in i['blocks']:
        out+='```quiz\n'+yaml.safe_dump(b,sort_keys=False,allow_unicode=True,width=110)+'```\n\n'
        if i['gap']:
            out+='**Topics:** No whole-task equivalent verified for '+i['gap']+'. Component coverage: '
            out+='; '.join(link(n)+' ('+coverage+')'for n,coverage in i['topics'])+'.\n'
        else:out+='**Topics:** '+'; '.join(link(n)for n,_ in i['topics'])+'.\n'
        out+='**Prerequisites:** '+('; '.join(link(n)for n in i['prereqs'])+'.'if i['prereqs']else'No additional prerequisite links needed.')+'\n\n\n'
DEST.write_text(out.rstrip()+'\n')
print(DEST)
print('Problems:',len(items),'Quiz blocks:',sum(len(i['blocks'])for i in items))
