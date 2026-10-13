"""Write review evidence and proposed content repairs; never submit."""
import collections
import hashlib
import json
import re
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]

def save(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2)+'\n')

def main():
    snapshot=json.loads((OUT/'snapshot.json').read_text())
    review=json.loads((OUT/'keyed-resolutions.json').read_text())
    rows={r['math_academy_id']:r for r in review['questions']}
    repairs=[]
    def replace(ma,before,after,reason):
        r=rows[ma];solution=r['worked_solution']
        assert before in solution,(ma,before)
        new=solution.replace(before,after)
        repairs.append(dict(question_eid=r['question_eid'],math_academy_id=ma,attribute=':question/worked-solution',before=solution,after=new,reason=reason,existing_key_unchanged=True,state='proposed_not_transacted'))
    replace('q-64207',r'\operatorname{ln}⁡(x+1)-3',r'\operatorname{ln}⁡(x+1)-2','The problem says -2; copy that constant accurately throughout the solution. Both candidates still have P_y=0.')
    replace('q-108979','i.e. $A+3I$ maps $w$ to $0$ in $1$ step','i.e. $A+3I$ maps $y$ to $0$ in $1$ step','The eigenvector in the A+3I chain is y, not w.')
    replace('q-95915','$Q$ should be an orthogonal matrix, not necessarily an upper triangular matrix.','$Q$ has orthonormal columns and is not necessarily upper triangular.','In thin QR, Q may be rectangular; orthogonal matrix is reserved for a square matrix with orthonormal rows and columns.')
    replace('q-76236','The only number $x$ that satisfies $g(x)={x}^{2}=2$ is $x=\\sqrt{2}\\notin Q.$','The only real solutions of $g(x)={x}^{2}=2$ are $x=\\pm\\sqrt{2}$, and neither belongs to $Q$.','Include both real square roots when excluding rational preimages.')
    # Combine the second correction for this question with the first into one CAS candidate.
    r=repairs[-1]
    old='In fact, ${x}^{2}>0$ for all $x\\in R.$'
    assert old in r['after']
    r['after']=r['after'].replace(old,'In fact, ${x}^{2}\\ge 0$ for all $x\\in R$, with equality at $x=0$.')
    r['reason']+=' Also replace x^2>0 by x^2>=0 to include zero.'
    replace('q-76250','Notice that $g$ has two roots, $x=\\pm \\sqrt{2}.$ So, we have $g(-\\sqrt{2})=0=g(\\sqrt{2}),$ while $-\\sqrt{2}\\ne \\sqrt{2}.$','For example, $1$ and $-1$ are distinct elements of $Q$, but $g(1)=-1=g(-1)$.','The original counterexample uses irrational inputs outside domain Q. Use rational inputs 1 and -1.')
    replace('q-77378','choose $27$ from the range','choose $27$ from the codomain','27 is precisely the omitted codomain value; it is not in the range.')
    replace('q-80265','The function is not identically zero for all points in $R\\,∖D.$ For example, $(x,y)=(1,1)\\in R\\,∖\\,D,$ but the function is nonzero at this point.','The $xy$ term integrates to zero over both regions by symmetry. Over $D$, the integral of $y^2$ is $\\int_{-1}^{1}(1-x^2)^3/3\\,\\mathrm{d}x=32/105$. Over $R$, it is $4\\int_{-1}^{1}y^2\\,\\mathrm{d}y=8/3$. These values are different, so function II does not satisfy the required equality.','Being nonzero somewhere outside D alone does not rule out cancellation; direct integral comparison proves the claimed inequality.')
    save('proposed-solution-repairs.json',dict(basis=snapshot['basis'],database_writes=0,counts=dict(questions=len(repairs)),repairs=repairs))
    held=rows['q-94772']
    save('proposed-key-repair.json',dict(basis=snapshot['basis'],database_writes=0,question_eid=held['question_eid'],math_academy_id='q-94772',state='withdrawn_do_not_prepare_key_repair',existing_key=held['database_key'],preserve_selection=['III'],reason='Preserve the Math Academy key as directed by the user. Clarify statement I to express the intended maximum-possible-count reading; no key or solution replacement for this question.'))
    images=[]
    for row in review['questions']:
        for relative in re.findall(r'!\[[^]]*\]\((images/[^)]+)\)',row['problem_before']):
            path=Path('/media/jake/SSD/EDB/math')/relative
            assert path.exists()
            images.append(dict(question_eid=row['question_eid'],math_academy_id=row['math_academy_id'],path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),role='problem_diagram_not_answer_option',inspection='Direct visual inspection' if row['math_academy_id'] in {'q-162747','q-71882','q-82109','q-115479','q-115856','q-236888','q-13445','q-155503','q-53000','q-53010'} else 'Formula in captured problem establishes selection independently of the illustrative graph'))
    save('image-evidence.json',dict(images=images,answer_option_images=0,first_answer_filename_convention_needed=False))
    pending=json.loads((OUT/'next-queue.json').read_text())
    unkeyed={q[':db/id']:q for q, in snapshot['questions'] if q[':db/id'] in pending['not_yet_evaluated_ids']}
    assert len(unkeyed)==1007 and all(not q.get(':question/worked-solution') and not q.get(':question/difficulty') for q in unkeyed.values())
    historical={q['id']:q for q in json.loads((OUT/'historical-candidates.json').read_text())}
    counts=dict(questions=len(unkeyed),kps=len({k[':db/id'] for q in unkeyed.values() for k in q.get(':knowledge-point/_questions',[])}),missing_keys=len(unkeyed),missing_solutions=len(unkeyed),missing_difficulties=len(unkeyed),problem_images=sum('![' in q.get(':question/problem','') for q in unkeyed.values()),historical_review_flags=dict(collections.Counter(f for eid in unkeyed for f in historical[eid]['review_flags'])))
    save('unkeyed-queue-summary.json',dict(basis=snapshot['basis'],database_writes=0,counts=counts,next_action='Choose bounded KP/topic groups, recover original capture evidence and missing keys, independently verify mathematics or diagrams, and consult study only when database keys are missing. Do not infer a difficulty rating from the format.'))
    status=json.loads((OUT/'status.json').read_text())
    status.update(state='keyed_group_evaluated_not_prepared',evaluated=review['counts'],remaining_unkeyed=counts,proposed_solution_repairs=len(repairs),source_for_future_authored_transactions=':agent/gpt-6.1-sol-high',transactions_prepared=False,previewed=False,committed=False)
    save('status.json',status)
    print(json.dumps(dict(reviewed=review['counts'],solution_repairs=len(repairs),remaining=counts)),flush=True)

if __name__=='__main__':main()
