"""Resolve the 48 disjoint structural text exceptions from current capture."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[7]
ROMAN = ["I","II","III","IV","V"]

# Truth is the prompt's selection predicate (e.g. 'cannot be positive definite'),
# rather than an unconditional truth value of the displayed formula.
PROOFS = {
"q-48352": ([1,1,0],["x^3 is continuous on [1,5] and differentiable on (1,5).","|x|=x throughout [1,5], so it meets both MVT hypotheses.","ln(x-1) is undefined at x=1, failing continuity on the closed interval."]),
"q-181536": ([1,0,1],["(n-2)(n-3)>0 holds for infinitely many integers n<=1 or n>=4.","(m-2)(m-3)<0 requires 2<m<3, containing no integers.","There are infinitely many rationals strictly between 2 and 3."]),
"q-181722": ([1,1,1],["Integers with |n|>5/2 include all n>=3, an infinite family.","Rationals with |q|>5/2 include the infinite integer family n>=3.","Reals with |x|>5/2 include the same infinite integer family."]),
"q-115206": ([0,0,1],["1/(x^2-4) is continuous on [-1,1], so the integral is proper.","The infinite lower endpoint makes it first kind under the source's finite-domain second-kind convention; poles +/-2 are outside (-infinity,-3].","At the finite lower endpoint -2, 1/(x^2-4) is unbounded; this is second kind."]),
"q-141209": ([0,1,0],["x^3-8 is nonzero on [0,1], so the integral is proper.","The finite lower endpoint -2 is a zero of x^3+8 and produces an unbounded integrand.","The infinite lower endpoint makes this an infinite-domain integral in the source taxonomy. It also has an interior pole at 0; the original key uses an exclusive finite-domain definition of second kind."]),
"q-141212": ([0,0,1],["The upper endpoint infinity makes this an infinite-domain integral in the source taxonomy. There is additionally a pole at x=1; the source classifies finite-domain second-kind integrals separately.","1-sqrt(x) does not vanish on [2,4], so the integral is proper.","At the finite lower endpoint 1, 1/sqrt(x-1) is unbounded; second kind."]),
"q-141218": ([1,0,0],["csc(x) tends to -infinity as x->0- on the finite interval [-pi/2,0]; second kind.","The infinite upper endpoint makes this an infinite-domain integral in the source taxonomy. Sec(x) also has poles in this domain; the source uses a finite-domain criterion for second kind.","On [0,pi/4], 1-sin(x)>=1-sqrt(2)/2>0; the integral is proper."]),
"q-181643": ([0,1,1],["Every derivative of e^(x-1) equals the same function, so A has one element.","The nth derivative is (-2)^n e^(-2x); the coefficients have distinct magnitudes, giving infinitely many functions.","The nth derivative is (1/2)^n e^(x/2); all coefficients are distinct."]),
"q-181650": ([1,0,1],["The even derivatives of cos(2x) are (-4)^m cos(2x), with distinct magnitudes.","Derivatives of -sin(x) cycle through four distinct functions, a finite set.","Sec(x) has a simple pole at pi/2; its nth derivative has a pole of order n+1 with nonzero leading coefficient. Different pole orders establish infinitely many distinct functions."]),
"q-181652": ([1,1,0],["Tan(x) has a simple pole at pi/2; its nth derivative has a pole of order n+1, so the derivatives are distinct.","The even derivatives of sin(3x) are (-9)^m sin(3x), with distinct magnitudes.","The derivatives of 3sin(x) cycle through four functions, a finite set."]),
"q-181674": ([1,1,1],["tan(n*pi/2)=0 precisely for even integers n; there are infinitely many.","The even integers are also an infinite family of rational solutions.","The same even integers are an infinite family of real solutions."]),
"q-181721": ([0,1,1],["|n|<=4/5 allows only the integer 0, a finite set.","The rational interval [-4/5,4/5] contains infinitely many rationals.","The real interval [-4/5,4/5] contains infinitely many reals."]),
"q-40116": ([1,0,0],["a!=0 implies a dot a=||a||^2>0.","The premise gives 6(a dot a)=9(b dot a), so b dot a=(2/3)||a||^2. Half this is (1/3)||a||^2, not ||a||^2.","b dot a=(2/3)||a||^2>0, hence it cannot equal -4."]),
"q-49928": ([1,0,0],["The finite upper endpoint 3 is a pole of 1/(x^2-9), so this is second kind.","The lower endpoint is infinite and poles +/-3 lie outside (-infinity,-4]; this is first kind.","1/x^2 is continuous throughout [1,3], so this is proper."]),
"q-81109": ([0,1,1],["U's first vector has squared norm 1+25+4=30, so U cannot be orthonormal.","Both V vectors have squared norm (4+9)/13=1, and their dot product is (-6+6)/13=0.","W's squared norms are (1+4+1)/6=1 and (1+1+1)/3=1, with dot product (1-2+1)/sqrt(18)=0."]),
"q-38300": ([0,1,0],["(1,3) is not on y=-3x, so it is not in the specified range.","For the intended linear map R^2 onto a line, rank=1 and rank-nullity gives nullity=1; the kernel is nontrivial.","The range is a line containing nonzero vectors, not the zero subspace."]),
"q-38305": ([0,1,0],["At (6/5,1), 5y=5 differs from 6x=36/5, so the point is not in the range line.","For the intended linear map R^2 onto a line, rank=1 and nullity=2-1=1; the kernel is nontrivial.","Rank-nullity gives nullity 1, not 0."]),
"q-216886": ([0,1,0],["For x=1 there are two outputs y=1 and y=-1 satisfying x=y^2; it is not functional on R.","For each x>0, xy^3=1 has the unique positive output y=x^(-1/3), so S is functional.","For x=1, both y=1 and y=2 divide 2x=2, so output is not unique."]),
"q-42481": ([1,1,0],["For the 3x3 identity, det(3I)=3^3=27; 14-27=-13.","det(A^T)=det(A)=14 and det(I)=1, so -14+1=-13.","det(A)-det(A^T)=14-14=0, not -28."]),
"q-330333": ([0,0,1],["Counterexample: A=I_3, x1=e^t e1, x2=e^t e2 are solutions, but x1 cross x2=e^(2t)e3 has derivative twice itself, whereas A times it equals itself.","Counterexample: A=0 and x2=e1 is a solution, but sin(t)e1 has derivative cos(t)e1!=0.","For any solution x2, (-3x2)'=-3Ax2=A(-3x2); constant scalar multiples remain solutions."]),
"q-213246": ([0,1,0],["Reflexivity would require x=2x mod 7 for every integer. At x=1 this fails.","x=x mod 9 holds for every integer, so S is reflexive.","x=x+2 mod 6 would require 6|2, false for every x."]),
"q-213240": ([0,1,0],["At x=3, x+x=6 does not divide 10, so reflexivity fails.","For every x, x^2-x^2=0 is divisible by 4, so S is reflexive.","At x=2, 2 does not divide x+1=3, so reflexivity fails."]),
"q-213599": ([1,1,1],["Congruence modulo 3 is symmetric: 3|(x-y) implies 3|(y-x).","x+y=0 implies y+x=0 by commutativity.","|X|=|Y| implies |Y|=|X| by symmetry of equality."]),
"q-213600": ([0,0,1],["2 R 4 holds because 4=2^2, but 4 R 2 fails because 2!=4^2.","{0} is a proper subset of {0,1}, but the reverse proper-subset relation fails.","4|(x+y) iff 4|(y+x), so T is symmetric."]),
"q-214002": ([1,0,1],["If y=ax and z=by for integers a,b, then z=abx; divisibility is transitive (including zero cases).","Counterexample: 3+0<4 and 0+3<4, but 3+3 is not <4.","If 4|(x-y) and 4|(y-z), then 4|(x-z); congruence is transitive."]),
"q-181669": ([0,1,1],["cos(2n*pi)=1 for every integer n, so A is empty.","q=1/4+k/2 for every integer k gives cos(2q*pi)=0; infinitely many distinct rational solutions.","The same family is an infinite family of real solutions."]),
"q-181641": ([1,0,0],["The nth derivative of e^(1-2x) is (-2)^n e^(1-2x), with distinct magnitudes.","All derivatives of 3e^x equal 3e^x, so B is a singleton.","The derivatives of 4e^(-x) alternate between 4e^(-x) and -4e^(-x), so C has two elements."]),
"q-181667": ([1,1,1],["sin(n*pi/2)=0 precisely for even integers n, an infinite set.","All even integers also give rational solutions, so B is infinite.","All even integers also give real solutions, so C is infinite."]),
"q-181706": ([1,1,1],["On x>0 the function equals x^(2/5). The nth derivative is c_n x^(2/5-n), with c_n!=0 and distinct powers; hence infinitely many functions.","On x>0 the nth derivative of -x^(1/2) is c_n x^(1/2-n), with c_n!=0 and distinct powers.","The nth derivative of x^(-2) is (-1)^n(n+1)!x^(-n-2), with distinct powers and nonzero coefficients."]),
"q-181771": ([1,0,1],["-n^2+n+12=-(n-4)(n+3)<=0 holds for infinitely many integers n<=-3 or n>=4.","The opposite inequality confines integer m to [-3,4], a finite set.","The real interval [-3,4] contains infinitely many rationals satisfying the inequality."]),
"q-40288": ([0,0,0],["The first two U vectors have dot product -2*3-1*2=-8!=0.","The V vectors have dot product 0*1+5*2=10!=0.","The first two W vectors have dot product 6*2+1*3-1*1=14!=0."]),
"q-140479": ([0,1,0],["The U vectors have dot product -3-2+2=-3!=0.","For V, the three pairwise dot products are 4-4=0, 2-4+2=0, and 6-4-2=0.","The W vectors have dot product 2+2+4=8!=0."]),
"q-82399": ([1,0,1],["The U vectors each have squared norm 1 and their dot product is 1/2-1/2=0.","The first V vector has squared norm 1+16+9=26!=1, so not orthonormal.","The W vectors each have squared norm (16+9)/25=1, and dot product (12-12)/25=0."]),
"q-152832": ([1,1,1,1],["f(1)=2-1=1 exists.","The left limit is 2(1)-1=1 and the right limit is 2-1=1.","Both one-sided limits and f(1) equal 1.","The finite limit exists and equals the defined value, so f is continuous at 1."]),
"q-155957": ([0,0,0,1],["L=(-2,2,-2)+t(5,-6,4). Its first coordinate is zero only at t=2/5, where the second coordinate is -2/5, so the zero vector is absent.","Let p=(-2,2,-2). Then 2p=(-4,4,-4) is not on L: its first coordinate forces t=-2/5, whose second coordinate is 22/5 rather than 4. Addition closure fails.","Multiplication of any point by zero gives the zero vector, which is absent, so scalar closure fails.","Every subspace contains zero; L does not, so L is not a subspace."]),
"q-94462": ([1,0,0],["At x=(1,-2), R=1+4-10=-5<0. A positive-definite form must be positive at every nonzero vector, so R cannot be positive definite.","At the specified vector S=45>0. This single evaluation does not rule out positive definiteness, so it is not selected under the 'cannot' predicate.","At the specified vector T=1+4-2=3>0. This does not rule out positive definiteness, so it is not selected."]),
"q-125636": ([1,0,0,0],["On the segment r=(t,t), F=(t,-t), dr=(1,1)dt, so the integral is 0.","On r=(t,t^2), 0<=t<=1, F dot r'=t^2-2t^2=-t^2; the integral is -1/3, not 0.","Two paths have different integrals, so it is path dependent.","For F=(P,Q)=(y,-x), P_y=1 differs from Q_x=-1; it is not conservative."]),
"q-125792": ([1,0,0,0],["On y=ln(x), dy=dx/x, so F dot dr=dx+x*dy=2dx; the integral from 1 to e is 2(e-1).","On the segment, dy=dx/(e-1), so the integral is (e-1)+(e^2-1)/(2(e-1))=(3e-1)/2. Its difference from 2(e-1) is (3-e)/2!=0.","The two integrals differ; alternatively P_y=0 and Q_x=1, so path independence fails.","For F=(1,x), P_y=0!=1=Q_x on R^2, so it is not conservative."]),
"q-152913": ([1,1,0,0],["f(0)=0 is defined.","The left limit of x+1 and right limit of e^(-x) both equal 1.","The limit is 1 but f(0)=0, so they differ.","The limit differs from f(0), so f is not continuous at 0."]),
"q-152926": ([1,1,0,0],["f(0)=1 is defined.","The left limit of 2x and right limit of 3x both equal 0.","The limit is 0 but f(0)=1, so they differ.","The limit differs from f(0), so continuity fails."]),
}

SUBSPACE_IDS = {"q-156596","q-156628","q-156653","q-157300","q-157374","q-157375","q-157463","q-157464"}
RELATION_IDS = {"q-216886","q-213246","q-213240","q-213599","q-213600","q-214002"}

def extract(q):
    problem=q[":question/problem"]
    markers=list(re.finditer(r"^(?:- |(?:I|II|III|IV|V)\. )",problem,re.M))
    if len(markers)==1:
        # Source typography has I as a bullet, then II/III on the same line.
        markers=list(re.finditer(r"(?:^|(?<=\s))(?:- |(?:I|II|III)\. )",problem,re.M))
    assert len(markers) in (3,4), (q[":question/math-academy-id"],len(markers))
    texts=[problem[m.end():markers[i+1].start() if i+1<len(markers) else len(problem)].strip()for i,m in enumerate(markers)]
    labels=["R","S","T"] if q[":question/math-academy-id"] in RELATION_IDS else ROMAN[:len(texts)]
    alias={l:l for l in labels}
    if q[":question/math-academy-id"] not in RELATION_IDS:
        for label,text in zip(labels,texts):
            named=re.match(r"\$([ABC]|[UVW])=",text)
            if named:alias[named[1]]=label
    return problem[:markers[0].start()].rstrip(), list(zip(labels,texts)), alias

def parse(value,labels,alias,ma_id):
    if ma_id=="q-94462" and value=="None of the forms could be positive-definite":
        return labels[:]
    if re.match(r"none\b",value,re.I):return []
    if re.match(r"all\b",value,re.I):return labels[:]
    normal=value.replace("$", "")
    tokens=re.findall(r"\b(?:IV|III|II|I|[A-Z])\b",normal)
    assert tokens and all(t in alias for t in tokens),(ma_id,value,tokens,alias)
    rest=re.sub(r"\b(?:IV|III|II|I|[A-Z]|and|only)\b|[ ,.]","",normal)
    assert not rest,(ma_id,value,rest)
    result=[alias[t]for t in tokens]
    assert len(set(result))==len(result)
    return [l for l in labels if l in result]

def main():
    snapshot_path=OUT.parent/"review-snapshot.json"
    current={q[":db/id"]:q for chunk in json.loads(snapshot_path.read_text())["questions"] for q in chunk}
    source=json.loads((OUT/"text-cases.json").read_text())
    unresolved=[q for q in source["questions"] if q["decision"]=="needs_evidence"]
    assert len(unresolved)==48
    reviews=[]
    for old in unresolved:
        q=current[old["id"]];ma_id=q[":question/math-academy-id"]
        prefix,objects,alias=extract(q)
        labels=[l for l,t in objects]
        if ma_id in SUBSPACE_IDS:
            negative="**not** a subspace"in q[":question/problem"]
            truth=[1,1,1,int(not negative)]
            proofs=["The line/plane is defined by a homogeneous linear equation or spans a nonzero vector from the origin, so it contains zero.",
                    "For a homogeneous equation, adding two solutions gives another; equivalently the sum of scalar multiples of the spanning vector is another multiple.",
                    "Multiplying a solution of a homogeneous linear equation by any real scalar preserves the equation; equivalently scalar multiples remain in the span.",
                    "The homogeneous solution space/span is a subspace. Therefore the negated subspace statement is false."if negative else"Containing zero and closure under addition and scalar multiplication establish that it is a subspace."]
        else:truth,proofs=PROOFS[ma_id]
        assert len(truth)==len(proofs)==len(objects)
        atoms=[{"label":l,"text":t,"truth":bool(v),"proof":p}for(l,t),v,p in zip(objects,truth,proofs)]
        field=q[":question/answer-fields"][0]
        assert len(q[":question/answer-fields"])==1
        mapping=[{"answer_eid":a[":db/id"],"value":a[":answer/value"],"labels":parse(a[":answer/value"],labels,alias,ma_id)}for a in field[":answer-field/choices"]]
        key=field[":answer-field/correct"]
        correct=next(a["labels"]for a in mapping if a["answer_eid"]==key[":db/id"])
        assert correct==[a["label"]for a in atoms if a["truth"]],(ma_id,correct,truth)
        assert len({tuple(a["labels"])for a in mapping})==len(mapping),(ma_id,mapping)
        instruction="Select all that apply."
        if not correct:instruction+=" If none apply, leave all boxes unchecked."
        prompt=prefix+"\n\n"+instruction+"\n\n"+"\n\n".join(f"- **{l}.** {t}"for l,t in objects)
        content_repairs=[];proposed_solution=None
        if ma_id=="q-330333":
            solution=q[":question/worked-solution"]
            assert 'correct answer is "I and III only"'in solution
            proposed_solution=solution.replace('correct answer is "I and III only"','correct answer is "III only"')
            content_repairs=[{"kind":"solution_final_answer_typo","required_for_consistent_solution":True,"description":"The body rejects I/II and proves III. Change the final answer from I and III only to III only, matching the independently verified existing database key."}]
        if ma_id in {"q-141209","q-141212","q-141218"}:
            content_repairs.append({"kind":"mixed_improper_integral_classification_qualification","required_for_consistent_solution":False,"description":"The source distinguishes second-kind integrals with finite bounds from infinite-domain integrals. The latter option also has singularities and would be called mixed kind in a nonexclusive taxonomy. Preserve the existing key and source taxonomy; make the finite-domain convention explicit in a separate content repair if desired."})
        if ma_id in {"q-38300","q-38305"}:
            content_repairs.append({"kind":"implicit_linear_map_assumption","required_for_consistent_solution":False,"description":"The kernel/nullity question and worked solution assume T is linear. The prompt says only maps; explicitly adding linear would remove that implicit context in a separate content repair."})
        row={"id":old["id"],"question_eid":old["id"],"ma_id":ma_id,"decision":"convert",
             "classification":"resolved_inline_integral_list"if old["classification"]=="unresolved_source_universe"else"resolved_named_or_positional_statement_list",
             "atomic_options":atoms,"correct_labels":correct,"choice_mapping":mapping,"source_choice_to_checked_labels":mapping,
             "proposed_prompt":prompt,"problem_after":prompt,"problem":q[":question/problem"],"fields":q[":question/answer-fields"],
             "worked_solution":q[":question/worked-solution"],"current_source":q,
             "reason":"Recovered the complete source universe and every old-choice subset using explicit Roman positions or named-object aliases. Independent predicate proofs agree with the stored database key; no key change.",
             "key_evidence":{"source":"current database capture","field_eid":field[":db/id"],"answer_eid":key[":db/id"],"value":key[":answer/value"],"proofs":"See each atomic option; no study-vault key used.","worked_solution":q[":question/worked-solution"]},
             "content_repairs":content_repairs,"key_change":False,"source_aliases":alias,"historical_exception_reason":old["reason"],
             "source_evidence":{"path":str(snapshot_path.relative_to(ROOT)),"sha256":hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),"question_eid":old["id"]},
             "preview_status":"not_prepared","commit_status":"not_submitted","unavailable_evidence":[]}
        if ma_id=="q-94462":row["special_option_mapping_proof"]="The prompt selects forms that cannot be positive-definite. 'None of the forms could be positive-definite' asserts that every form satisfies that predicate, so it maps to I/II/III all selected. It does not map to the empty subset."
        if proposed_solution:row["proposed_worked_solution"]=proposed_solution
        reviews.append(row)
    counts={"reviewed":48,"convert":48,"needs_evidence":0,"key_changes":0,"classes":dict(Counter(r["classification"]for r in reviews)),"atomic_options":sum(len(r["atomic_options"])for r in reviews),"old_choices_mapped":sum(len(r["choice_mapping"])for r in reviews),"required_solution_repairs":1,"taxonomy_qualifications":3,"implicit_context_qualifications":2}
    result={"database_writes":0,"counts":counts,"scope":"Disjoint overrides for all 48 text_cases structural exceptions, using the exact current capture. Stored keys preserved.","questions":reviews}
    (OUT/"held-exceptions.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    (OUT/"held-exceptions.md").write_text("# Structural text exception review\n\nResolved all 48 exceptions: 158 atomic options and 240 complete old-choice mappings. Existing keys remain unchanged.\n\nThe source universes are complete. Roman labels are positions for bullet lists; named sets and relations map through explicit aliases; five integral lists had II/III embedded on the same line.\n\nq-330333 needs a separately proposed worked-solution final-answer correction to III only. q-94462's option 'None of the forms could be positive-definite' maps to all three selections because the predicate is cannot be positive-definite. q-40288's None option maps to an empty subset.\n\nThree mixed improper-integral cases preserve the source's exclusive finite-domain second-kind taxonomy, and record the additional singularities. Two range/kernel cases preserve the source's implicit linear-map context. These qualifications are recorded separately from conversion-only prompts.\n\nNo live database mutations, missing keys, or unavailable source evidence. Root must reconcile ownership, canonical membership and learner uses before preparing transactions.\n")
    print(json.dumps(counts,indent=2))

if __name__=="__main__":main()
