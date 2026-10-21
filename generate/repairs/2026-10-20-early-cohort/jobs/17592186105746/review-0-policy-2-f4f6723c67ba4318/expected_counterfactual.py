"""Independent expected fixture for a missing decision role; does not repair code."""
import sys,copy,uuid,json
sys.dont_write_bytecode=True
import review as R
base=R.g.generate('easy',7331,'q-42157',{'rhs_scale':1});after=copy.deepcopy(base);q=after['question'];q[':question/id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'independent-review/q42157/consistent-counterfactual'))
q[':question/problem']=q[':question/problem'].replace('=-10.','=-8.')
q[':question/worked-solution']=r'''First, we set up the augmented matrix:
$$M=\begin{bmatrix}1 & -6 & 2 \\ -4 & 24 & -8\end{bmatrix}.$$
Apply $R_2:=R_2+4R_1$:
$$M\sim\begin{bmatrix}1 & -6 & 2 \\ 0 & 0 & 0\end{bmatrix}.$$
The corresponding system is
$$\left\{\begin{aligned}x-6y&=2\\0x+0y&=0.\end{aligned}\right.$$
The second equation is redundant. The basic variable is $x$ and $y$ is free. Solving the first equation gives $x=2+6y$. Thus the general solution is
$$\begin{bmatrix}x\\y\end{bmatrix}=\begin{bmatrix}2+6y\\y\end{bmatrix},\quad y\in(-\infty,\infty).$$'''
f=q[':question/answer-fields'][0];f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][1][':answer/id']]
after['generation']={'template':'independent-expected-consistency-counterfactual','seed':7331,'parameters':{'second_rhs':-8},'review_fixture':True,'provenance':'Independently authored expected output, not an output claimed from the current generator. Reuses q-42157 complete bank, changes second RHS and derives new solution/key.'}
assert R.mathcheck(after)['passed'];R.save('expected-counterfactual-records.json',[base,after]);R.save('expected-counterfactual-results.json',{'before':R.mathcheck(base),'after':R.mathcheck(after),'generator_supports_after':False,'meaning':'Holding all coefficients and the first RHS fixed, second RHS -10 to -8 must change classification and selected bank answer. The independent expected fixture supplies the strict grader/rendering oracle for a future repair.'})
cases=R.json.load(open(R.ROOT/'grader-input.json'))
for tag,records in [('delivered-domain',json.load(open('delivery-domain/accepted.json'))),('delivered-batch',json.load(open('delivery-batch/accepted.json'))),('expected-consistency-pair',[base,after])]:
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0];idx=R.correct_index(r)
  cases.append({'label':tag+' '+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if j==idx else 'rejected','purpose':'Expected independently derived key; reject all alternative radio submissions'} for j,c in enumerate(f[':answer-field/choices'])]})
R.save('grader-complete-input.json',cases)
print('Prepared expected pair and',len(cases),'complete native-grader cases')
