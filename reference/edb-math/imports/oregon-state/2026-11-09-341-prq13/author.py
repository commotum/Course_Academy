from pathlib import Path
import csv,json,yaml,re
R=Path('/home/jake/Developer/study');T=Path('/tmp/ingest-prq13');T.mkdir(exist_ok=True);paths={}
for file in ['MA/Mathematical-Foundations/catalog.csv','MA/Mathematical-Analysis-&-Modeling/LAL/topics.csv']:
 for row in csv.DictReader((R/file).open()):
  p=Path(row['lesson-path']);paths.setdefault(int(row['topic-id']),R/p if str(p).startswith('MA/')else R/Path(file).parent/p)
def link(i):
 p=paths[i];assert f'lesson-id: {i}'in p.read_text();return f'[{p.read_text().splitlines()[0][2:]}](<{p.resolve().as_uri()}>)'
class D(yaml.SafeDumper):pass
D.add_representer(str,lambda d,s:d.represent_scalar('tag:yaml.org,2002:str',s,style='|'if '\n'in s else None))
def choice(id,kind,value,feedback):return {'id':str(id),'type':kind,'value':value,'feedback':feedback}
def question(id,content,choices,correct,feedback):return {'id':'canvas-'+str(id),'content':content,'fields':[{'key':'answer','type':'radio','choices':choices,'correct':str(correct)}],'feedback':feedback}
qs=[question(59459051,'What is a defining characteristic of a eigenvalue/eigenvector pair?',[
 choice(3650,'math',r'A\vec{v}=\lambda\vec{v}',r'This is the defining relation, with the additional requirement that $\vec v\ne\vec0$.'),
 choice(9450,'math',r'A\vec{v}=\vec{0}',r'This is the special case $\lambda=0$ for a nonzero eigenvector; it does not characterize every eigenvalue/eigenvector pair.'),
 choice(3718,'math',r'A\vec{v}\ne\vec{0}',r'This excludes the valid eigenvalue $\lambda=0$. It also does not require $A\vec v$ to be a scalar multiple of $\vec v$.'),
 choice(9261,'text',r'$\vec{v}$ is the zero vector',r'Eigenvectors are required to be nonzero. The zero vector satisfies the equation for every scalar and therefore cannot identify an eigenvalue.')
 ],3650,r'''An eigenvalue/eigenvector pair satisfies $A\vec v=\lambda\vec v$ with $\vec v\ne\vec0$. The matrix sends the eigenvector to a scalar multiple of itself. The eigenvalue may be zero; the eigenvector may not.'''),
 question(59459052,r'If we know that $A\vec{v}=\lambda\vec{v}$ does $A$ need to be a square matrix?',[
 choice(1242,'text','Not enough info given.',r'The equality supplies the needed dimensional information: $A\vec v$ and $\lambda\vec v$ must have the same number of components.'),
 choice(4458,'text','Yes',r'If $A$ is $m\times n$, then $\vec v$ has $n$ components and $A\vec v$ has $m$; equality with $\lambda\vec v$ requires $m=n$.')
 ],4458,r'''Write $A$ as an $m\times n$ matrix. For $A\vec v$ to be defined, $\vec v$ is $n\times1$, so $A\vec v$ is $m\times1$. Scalar multiplication leaves the dimensions of $\vec v$ unchanged, so $\lambda\vec v$ is $n\times1$. Equality of the two vectors requires $m=n$. Thus $A$ is square.'''),
 question(59459053,r'What name do we give to $\det(A-\lambda I)=0$?',[
 choice(5312,'text','Homogeneous Equation',r'The associated vector equation $(A-\lambda I)\vec v=\vec0$ is homogeneous. The determinant equation is specifically the characteristic equation.'),
 choice(7747,'text','Charlie','This is not a mathematical name for the determinant equation.'),
 choice(84,'text','Characteristic Polynomial',r'This is the closest supplied choice and the source’s intended label. Precisely, $p_A(\lambda)=\det(A-\lambda I)$ is the characteristic polynomial, while $p_A(\lambda)=0$ is the characteristic equation.'),
 choice(7366,'text','Fundamental Polynomial','This is not the standard name for this object; the relevant terms are characteristic polynomial and characteristic equation.')
 ],84,r'''**Source terminology issue:** Among the original options, “Characteristic Polynomial” is the intended choice, but the displayed equality is more precisely the **characteristic equation**. The expression $p_A(\lambda)=\det(A-\lambda I)$ is a polynomial in $\lambda$; setting it equal to zero gives the equation whose roots are the eigenvalues.

Indeed, $A\vec v=\lambda\vec v$ is equivalent to $(A-\lambda I)\vec v=\vec0$. A nonzero solution exists exactly when $A-\lambda I$ is singular, which is equivalent to $\det(A-\lambda I)=0$.''')]
meta=[([1375],[1195],'The linked lesson defines the eigenpair relation and verifies it in worked examples.'),([1198],[862],'The linked lesson supplies the matrix-product dimension rule. No whole-task equivalent was verified for inferring squareness specifically from the eigenpair identity; this is component coverage.'),([1964],[862],'The linked lesson defines and uses the characteristic equation; it distinguishes the mathematical object from the source’s imprecise option label. This is concept coverage rather than an exact source-label match.')]
out='\n**MTH 341 — Post-reading Questions: §§7.1.1–7.1.3**\n\nDue: 2026-11-10\nDue time: 11:59 p.m. PST\nDate imported: 2026-11-09\nSource: [Canvas — Post-reading Questions -Sections 7.1.1-7.1.3](https://canvas.oregonstate.edu/courses/2064363/quizzes/3193301)\n\nStudy answers and explanations are independently authored additions. Original choice text and ordering are retained. Question 3 has a source terminology issue; its feedback distinguishes the characteristic polynomial from the characteristic equation.\n\n## Topics\n\n'
out+='\n'.join('- '+link(i)for i in [1375,1198,1964])+'\n\n## Prerequisites\n\n'+'\n'.join('- '+link(i)for i in [1195,862])+'\n\n## Instructions\n\nAnswer all three multiple-choice questions. Canvas specifies no time limit.\n'
for n,(q,(topics,pre,note))in enumerate(zip(qs,meta),1):
 out+=f'\n---\n\n## Problem {n}\n\nSource question: Canvas Question {n} (question_{59459050+n}).\n\n```quiz\n'+yaml.dump(q,Dumper=D,allow_unicode=True,sort_keys=False,width=110).rstrip()+'\n```\n\n**Topics:** '+'; '.join(link(i)for i in topics)+' — '+note+'\n**Prerequisites:** '+'; '.join(link(i)for i in pre)+'\n\n\n'
p=R/'vault/F26/341/11-10-26_PRQ-13.md';assert not p.exists();p.write_text(out)
(T/'source-inventory.json').write_text(json.dumps({'url':'https://canvas.oregonstate.edu/courses/2064363/quizzes/3193301','title':'Post-reading Questions -Sections 7.1.1-7.1.3','due':'2026-11-10T23:59:00-08:00','questions':3,'source_ids':[59459051,59459052,59459053],'choice_ids':[[3650,9450,3718,9261],[1242,4458],[5312,7747,84,7366]],'wording_issue':'Question 3 displays the characteristic equation; its closest option says Characteristic Polynomial.'},indent=2))
print(p)
