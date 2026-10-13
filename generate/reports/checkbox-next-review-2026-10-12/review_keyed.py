"""Evaluate all remaining keyed cases without changing database facts."""
import collections
import hashlib
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
ROM = ['I','II','III','IV','V','VI','VII','VIII','IX','X']
LABEL = r'(?:VIII|VII|VI|IV|III|II|IX|X|V|I|[A-Z])'

# Conclusions from direct review of the full captured problems and solutions.
# Keys are evidence to preserve, not a substitute for these independent checks.
PROOFS = {
 'q-236888': ('II', 'Image review: polygon II crosses itself; the concave polygon I and convex polygon III do not. Only II is complex.'),
 'q-13445': ('I III', 'Image review: M,R,N lie on one straight line; O,S,P lie on another. T lies on the separate T,S,R,Q line and is not collinear with P,S.'),
 'q-155503': ('I III', 'Image review of the grid: I has three points on a line of slope 1; III has three points on a line of slope -1. The three points in II are noncollinear.'),
 'q-53000': ('I II', 'Image shows four equal sides and four right angles: a square. Under the captured inclusive-kite and exclusive-trapezoid definitions, it is a kite and rectangle but not a trapezoid. State these conventions explicitly to avoid the alternative inclusive trapezoid definition.'),
 'q-53010': ('I II', 'Image review: horizontal AB and CD are parallel. The marked angle ABC is right. AD is sloped while BC is vertical, so they are not parallel.'),
 'q-32551': ('III', 'Only III has a unit lower-triangular left factor and an upper-triangular right factor. I has a nonzero below-diagonal right entry; II reverses the required factor order.'),
 'q-42983': ('I', 'The given y=3 forces x=1/2 and k=48. Cramer determinants are D=-8-3k and Dy=24-10k; 3D=Dy yields 48, whereas D=Dy yields 32/7 and D=3Dy yields 80/27. D at 48 is nonzero.'),
 'q-38033': ('III', 'v1-v2 is a nonzero kernel vector. Thus the kernel is not {0}, T is not invertible, and rank(T)<8.'),
 'q-43772': ('IV', 'Trace-one matrices are not closed under addition (trace 2) or scaling (zero multiple has trace 0); hence they are not a subspace.'),
 'q-43774': ('IV', 'Functions with f(0)=3 fail closure under addition (value 6 at zero) and scaling (zero function excluded). Hence D is not a subspace.'),
 'q-71930': ('II', 'The correct rectangle integral is (integral_0^1 sqrt(x) dx)(integral_1^3 y dy)=8/3. II uses these matching limits. I and III integrate over x in [1,3], y in [0,1], giving (3sqrt(3)-1)/3 instead.'),
 'q-124004': ('II', 'The linear matrix is [[-1,1],[1,1]], with determinant -2. It differs from I and reverses orientation, so only II is true.'),
 'q-333079': ('II III', 'Euler update is y_(n+1)=(1-4h)y_n, with no nth power in its multiplier. Decay requires |1-4h|<1, equivalently 0<h<1/2. Both h=0.2 and 0.3 are stable, so III is true and IV false.'),
 'q-37456': ('II', 'Hessian determinant is 2*0-1=-1; f_xx=2>0; negative determinant makes the stationary point a saddle, not a minimum. Missing difficulty remains missing; no authored calibration is inferred.'),
 'q-104930': ('II III', 'P(N) is infinite. The two-element set {Z,pi} has a four-element power set. Integer solutions of sin(x)=0 are {0}, since nonzero integer multiples of pi are irrational, so its power set has two elements.'),
 'q-171334': ('II', 'Under propositional-form equivalence, only not-Q implies not-P is equivalent to P implies Q. Converse and inverse are not equivalent for arbitrary P,Q. Qualify the prompt to make this intended interpretation explicit.'),
 'q-22428': ('I III', 'f prime=1-2/x changes from negative to positive at x=2. Endpoint values are 1/2+2 ln(2) and e-2; the former is the maximum, while f(2)=2-2 ln(2) is the minimum.'),
 'q-8331': ('I II III', 'Swapping coordinates is multiplication by the matrix [[0,1],[1,0]], so homogeneity, additivity and linearity all hold.'),
 'q-42374': ('I II III', 'Shapes A=4x2, B=2x4 and C=2x2 make AB, BA and AC conformable.'),
 'q-154690': ('II', 'f(0)=-1/4 disproves nonnegativity. Integral from 0 to 4 of (x-1)/4 is [x^2/8-x/4]_0^4=1. Negative density values invalidate the PDF.'),
 'q-36792': ('II', 'First Av=v, not 2v. Second Av=0. Scaling an eigenvector preserves its eigenvalue, so A(3v)=2(3v), not 6(3v).'),
 'q-42438': ('I II III', 'The real domain of arctan is all of R; all three supplied numbers are real.'),
 'q-65744': ('II', 'Only (sqrt(3)/2,pi/3) has x=sin(y) with y in [-pi/2,pi/2]. pi/6 is not sin(1/2), and 2pi is outside the principal range.'),
 'q-65828': ('III', 'Only (-sqrt(2)/2,3pi/4) satisfies x=cos(y) and y in [0,pi]. The first x exceeds 1 and the second y is outside that range.'),
 'q-65947': ('II III', 'cos(pi/4)=sqrt(2)/2, not 1/2; arccos(1)=0. Thus II and III satisfy the graph equation and principal range.'),
 'q-65990': ('II III', 'tan(pi/6)=1/sqrt(3), not 1; tan(pi/3)=sqrt(3); tan(-pi/4)=-1. The latter two angles are in the arctan principal range.'),
 'q-29163': ('III', 'sec=1 and sec=2 have solutions in [0,2pi); sec=1/2 would require cos=2, impossible.'),
 'q-43509': ('Q S', 'P requires both a row swap and row scaling. Q is one scaling R2:=7R2; S is one replacement R2:=R2+7R1.'),
 'q-155956': ('I II III IV', 'L={(2t,t):t in R}=span{(2,1)}. It contains zero, is closed under addition and scalar multiplication, and is a subspace. Include IV even though individual radio options omit it.'),
 'q-34153': ('II', 'a2+3a1-3a3=0 gives a nontrivial dependence; the determinant of the three-column matrix is zero. Only the dependence statement holds.'),
 'q-34273': ('I II', 'a2-4a1+3a3=0 gives a nonzero kernel vector. Scaling it gives infinitely many nonzero solutions, so the vectors are dependent.'),
 'q-162747': ('A D', 'Image review: A is the bottom of the valley; B lies on its slope; C is the peak; D is in the flat surrounding plateau. Under the source non-strict local-extremum convention A and D are local minima. Include C as a false selectable point even though the radio bank omits C.'),
 'q-341230': ('III', 'P=1/(x-1), Q=1/(x-1)^3 are not analytic at 1. Weighted P=1 extends analytically but weighted Q=1/(x-1) does not. The point is irregular singular.'),
 'q-36403': ('I II', 'At P=(2,0), y=2x-4, so P is in the closed half-plane and on its boundary. Q=(1,3) fails y<=-2 and is outside.'),
 'q-65127': ('II III', 'Pair I has mixed derivatives x^3 and y^3, unequal on every nonempty open region. Pair II has potential exp(x+y)-2xy. Pair III has potential (2/3)(x-1)^(3/2)-3y on x>1, an admissible open domain.'),
 'q-71882': ('I III', 'Image review: A is on the dashed circumference; B and C are strictly inside the disk. Boundary inclusion does not change boundary-point classification. I and III hold.'),
 'q-97974': ('I', 'Rank(C-5I)=3 implies nullity 0 and invertibility. Thus the nullspace is {0}, the matrix is not singular, and 5 is not an eigenvalue.'),
 'q-108907': ('II', 'Null(A) is perpendicular to Row(A)=Col(A transpose). The other spaces need not even be in the same ambient dimension and are not universally perpendicular.'),
 'q-109854': ('III', 'Apply Null(M) perpendicular to Col(M transpose) with M=XY; (XY) transpose=Y transpose X transpose. Other spaces are not universally orthogonal.'),
 'q-40400': ('U W', 'U dot product is 5-5=0. V has dot products 1 and -1 with its first vector, so is not orthogonal. W dot product is 4-4=0.'),
 'q-40639': ('C', 'A squared=2A, so A is not idempotent. B is not symmetric. C=(1/17)vv transpose with v=(1,4), v transpose v=17, so C is symmetric and idempotent.'),
 'q-73671': ('II III', 'x^2+y^2<=2x is equivalent to (x-1)^2+y^2<=1. Within this shifted disk the paraboloid is the lower surface and the plane the upper surface.'),
 'q-95915': ('III', 'For reduced/thin QR, Q is mxn with orthonormal columns, not necessarily square or triangular; R is nxn upper triangular. Explicitly qualify the factorization and universal must-be-true wording; complete QR would make Q square.'),
 'q-64207': ('I II III', 'Each candidate P depends only on x, so P_y=0=Q_x for Q=4y^3. All are exact on their real open domains; ln(x+1) requires x>-1. The solution incorrectly copies -2 as -3, with no effect on exactness.'),
 'q-108979': ('I III', 'The nonzero chain u->v->w->0 has ranks 3,2,1 for eigenvalue 2. y->0 under A+3I has rank 1 for eigenvalue -3. Correct the solution typo saying w instead of y in the latter chain.'),
 'q-171841': ('II III', 'x-1<x simplifies to -1<0, true for every integer. Its truth set is Z, not empty.'),
 'q-171904': ('I', 'Using the source convention N={1,2,...}, all n satisfy 1<=n, but the predicate forall n m<=n has truth set {1}, not N; m=2,n=1 disproves III.'),
 'q-36477': ('I', 'Dimensions are 6,5,36. The duplicated wrong option II and II only literally represents {II}; preserve that literal subset rather than inventing an intended III.'),
 'q-76219': ('', 'x^2 on R is not injective because f(1)=f(-1), not onto R because -1 is unattained, and therefore not bijective. The correct checkbox set is empty.'),
 'q-76236': ('I', '3^x maps R onto (0,infinity) via log base 3. Squaring Q is not onto Q (2 requires irrational roots); squaring R is not onto R (negative targets are unattained). Repair the solution to acknowledge both irrational roots and x^2>=0 including x=0.'),
 'q-76250': ('III', 'cos on R is not onto R. g on Q is not injective since g(1)=g(-1)=-1; the captured irrational-root example is invalid in domain Q. h has rational inverse (y+3)/8 and is bijective.'),
 'q-76259': ('II', 'x^2/4 is not injective on R, but every y>=0 has preimage 2sqrt(y), so it is onto [0,infinity) and not bijective.'),
 'q-77378': ('III', 'First image is {1,3,9}, missing codomain value 27. The cube on [0,infinity) misses all negative targets. The last function maps 0,1,2 to -1,1,3 and is onto. The solution should call 27 a codomain element, not a range element.'),
 'q-80265': ('I III', 'D has -1<=x<=1 and 0<=y<=1-x^2, contained in R. Zero extensions I and III give integral 32/105; II over R gives 8/3, because the xy term integrates to zero by symmetry. Nonzero values outside D alone would not prove unequal integrals, so replace that incomplete argument.'),
 'q-82109': ('I II III', 'Image review: 0->3, 2->1, 4->4, 6->2. Every target has exactly one preimage, so the function is onto, one-to-one and bijective.'),
 'q-93952': ('III', 'I has no initial conditions. II gives conditions at distinct locations and is a boundary-value problem. III gives y(1),y prime(1) at the same regular location and is an IVP.'),
 'q-80085': ('III', 'Trivial implication proof requires an always-true consequent. n^2>=0 is always true for integer n; n=0 is not, and 0>1 is false.'),
 'q-80089': ('II III', 'Vacuous proof requires an always-false antecedent. 0>1 and n^2<0 are always false for integer n; n<0 is true for some integers.'),
 'q-81053': ('I II', 'De Morgan gives not(A or not B)=(not A) and B. III is the negation of that formula and has the complementary truth table.'),
 'q-96595': ('II III', 'A-A transpose is generally skew-symmetric, with nonsymmetric example [[0,-1],[1,0]]. Sums of symmetric matrices are symmetric, and (A inverse) transpose=(A transpose) inverse=A inverse when A is invertible symmetric.'),
 'q-115479': ('III', 'Image review: slopes are positive on both sides of y=0, vertical near zero and tend to horizontal as |y| increases. 1/y changes sign; y/(y-1) tends to 1 and has a pole at 1; only 1/y^2 fits.'),
 'q-115856': ('I', 'Image review: equilibria at y=0,2 and slope signs +,-,+ across those lines. y(y-2) matches; (y-2)^2 has one zero and no negative region; y(2-y) reverses the signs.'),
 'q-95703': ('I', 'x1^2=6 gives the lines x1=+-sqrt(6). The other left sides are nonnegative and cannot equal negative right sides.'),
 'q-38297': ('III', 'The zero transformation has rank 0, image {0} (not empty), and kernel all of R^2.'),
 'q-161436': ('I', 'Divergences are 0,3y,1. Only the first is identically zero on an open region; a stream function is (x^2+y^2)/2 with F=(psi_y,-psi_x).'),
 'q-94772': ('I III', 'Every 3x2 matrix has at most 2 singular values, so it certainly has at most 3 distinct singular values: I is true. Singular values cannot be negative: II is false. III is also true under either common zero-padding convention. Existing key III only contradicts the problem; neither bank contains I and III only. Hold for an explicit key/solution repair, with no silent key change.'),
 'q-38136': ('II', 'The image spans three independent vectors, so rank=3 and nullity=5-3=2. Rank is not 1 or 5, so the endomorphism is not bijective.'),
 'q-35866': ('I', 'The first half-open rectangle contains boundary point (0,1) but omits limit point (1,0), so is neither open nor closed. The second is an open disk. The third is the intersection of closed inequalities and is closed.'),
 'q-161828': ('II', 'Inverse function theorem gives a C1 local inverse near b, not necessarily a global inverse on U. f(x)=x^2 on U=(-2,2), a=1 is a counterexample to I. The derivative is 1/f prime(a), never -f prime(a) for nonzero real derivative.'),
}

def subset(value, labels):
    text = re.sub(r'[$*]', '', value).strip().rstrip('.')
    if text.lower().startswith(('none','neither')):
        return []
    if text.lower().startswith('all'):
        return labels[:]
    tokens = re.findall(r'\b'+LABEL+r'\b', text)
    rest = re.sub(r'\b'+LABEL+r'\b|\b(?:and|or|only|both|statements?)\b|[,\s&]', '', text, flags=re.I)
    assert tokens and not rest and set(tokens)<=set(labels), (value, labels, rest)
    return [label for label in labels if label in tokens]

def universe(q):
    problem = q[':question/problem']
    if q[':question/math-academy-id'] in ('q-236888','q-155503'):
        noun='Polygon' if q[':question/math-academy-id']=='q-236888' else 'Diagram'
        return [dict(label=k,text=noun+' '+k+' in the displayed figure') for k in ROM[:3]], 'image_labeled_cases'
    if q[':question/math-academy-id']=='q-162747':
        return [dict(label=k,text='Point $'+k+'$ in the displayed graph') for k in 'ABCD'], 'image_named_points'
    marker = re.compile(r'(?m)^\s*(?:[-•]\s+|(?:\*\*)?('+LABEL+r')[.)](?:\*\*)?\s+)')
    matches = list(marker.finditer(problem))
    if len(matches)>=2:
        bank = [a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
        names = {k for value in bank for k in re.findall(r'\b'+LABEL+r'\b', re.sub(r'[$*]','',value))}
        out = []
        for i,m in enumerate(matches):
            text = problem[m.end():matches[i+1].start() if i+1<len(matches) else len(problem)].strip()
            label = m.group(1)
            if label is None:
                named = re.match(r'\$?('+LABEL+r')(?=[:=(\s$])',text)
                label = named.group(1) if not names<=set(ROM) and named else ROM[i]
            out.append(dict(label=label,text=text))
        return out,'source_line_list'
    matrices = list(re.finditer(r'\b([A-Z])\s*=\s*\[\\begin\{aligned\}.*?\\end\{aligned\}\]',problem,re.S))
    assert len(matrices)>=2, q[':question/math-academy-id']
    return [dict(label=m.group(1),text='$'+m.group(0)+'$') for m in matrices], 'source_named_matrices'

def main():
    snap=json.loads((OUT/'snapshot.json').read_text())
    candidates=[q for q, in snap['questions'] if any(f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[]))]
    assert {q[':question/math-academy-id'] for q in candidates}==set(PROOFS)
    assert not snap['items'] and not snap['response_users']
    refs=lambda value:[value] if isinstance(value,dict) else value
    field_owners={eid:{r[':db/id'] for r in refs(data.get(':question/_answer-fields',[]))} for eid,data in snap['field_owners']}
    answer_owners={eid:{r[':db/id'] for r in refs(data.get(':answer-field/_choices',[]))} for eid,data in snap['answer_owners']}
    rows=[]
    for q in sorted(candidates,key=lambda q:q[':db/id']):
        ma=q[':question/math-academy-id'];fields=q[':question/answer-fields']
        assert len(fields) in (1,2) and all(f[':answer-field/type'][':db/ident']==':answer-field.type/radio' and f[':answer-field/key']=='selection' for f in fields)
        atoms,kind=universe(q);labels=[a['label'] for a in atoms];assert len(set(labels))==len(labels)
        mappings=[];banks=[];keys=[]
        for f in fields:
            assert field_owners[f[':db/id']]=={q[':db/id']}
            bank=[]
            for a in f[':answer-field/choices']:
                assert a[':answer/type'][':db/ident']==':answer.type/text'
                assert answer_owners[a[':db/id']]=={f[':db/id']}
                selected=subset(a[':answer/value'],labels)
                mappings.append(dict(old_field=f[':db/id'],old_answer=a[':db/id'],old_value=a[':answer/value'],selected_labels=selected))
                bank.append(tuple(selected))
            banks.append(collections.Counter(bank))
            if f.get(':answer-field/correct'):
                key=f[':answer-field/correct'];assert key[':db/id'] in {a[':db/id'] for a in f[':answer-field/choices']}
                keys.append(dict(field=f[':db/id'],answer=key[':db/id'],value=key[':answer/value'],selected_labels=subset(key[':answer/value'],labels)))
        assert len(banks)==1 or banks[0]==banks[1],ma
        assert len(keys)==1,ma
        independently_correct,proof=PROOFS[ma];truth=independently_correct.split()
        assert set(truth)<=set(labels)
        agrees=set(keys[0]['selected_labels'])==set(truth)
        assert agrees==(ma!='q-94772'),ma
        for atom in atoms:atom.update(truth=atom['label'] in truth,proof=proof)
        prompt=q[':question/problem'];qualifications=[]
        if ma=='q-171334':
            extra='Compare the logical forms for arbitrary truth values of the antecedent and consequent.'
            prompt+='\n\n'+extra;qualifications.append(extra)
        if ma=='q-95915':
            prompt=prompt.replace('a QR factorization','a reduced (thin) QR factorization').replace('which of the following statements are true?', 'which of the following statements must be true for every such factorization?')
            qualifications.append('Specify reduced/thin QR and distinguish necessarily true properties from special square or triangular cases.')
        if ma=='q-53000':
            extra='Use the convention that a kite has at least two pairs of equal adjacent sides and a trapezoid has exactly one pair of parallel sides.'
            prompt+='\n\n'+extra;qualifications.append(extra)
        marker=list(re.finditer(r'(?m)^\s*[-•]\s+',prompt))
        if kind=='source_line_list' and len(marker)==len(atoms) and labels==ROM[:len(atoms)]:
            for m,a in reversed(list(zip(marker,atoms))):prompt=prompt[:m.start()]+'- **'+a['label']+'.** '+prompt[m.end():]
        if not re.search(r'select all (?:that apply|applicable|correct)',prompt,re.I):prompt+='\n\nSelect all that apply.'
        if any(not m['selected_labels'] for m in mappings):prompt+=' If none apply, leave all boxes unchecked.'
        rows.append(dict(question_eid=q[':db/id'],math_academy_id=ma,captured_basis=snap['basis'],captured_lineage=snap['lineage'],decision='convert' if agrees else 'hold_content_repair',classification=kind,kps=q.get(':knowledge-point/_questions',[]),canonical_memberships=q.get(':knowledge-point/_canonical-example',[]),difficulty=q.get(':question/difficulty'),old_fields=fields,atomic_options=atoms,database_key=keys[0],independently_correct_labels=truth,existing_key_preserved=agrees,choice_mapping=mappings,problem_before=q[':question/problem'],problem_after=prompt if agrees else None,prompt_qualifications=qualifications,worked_solution=q.get(':question/worked-solution'),proof=proof,learner_uses=[],ownership_verified=True,duplicate_banks_semantically_equal=True if len(fields)==2 else None,key_evidence='Existing database key, checked against worked solution and independent mathematics/image inspection. No study key consulted.',commit_status='unsubmitted'))
    overrides=OUT/'review-overrides.json'
    if overrides.exists():
        by_id={r['question_eid']:r for r in rows}
        for override in json.loads(overrides.read_text())['questions']:
            assert by_id[override['question_eid']]['database_key']==override['database_key']
            by_id[override['question_eid']]=override
        rows=[by_id[i] for i in sorted(by_id)]
    ready=[r for r in rows if r['decision']=='convert']
    counts=dict(reviewed=len(rows),resolved_for_conversion=len(ready),held_content_repairs=len(rows)-len(ready),reviewed_kps=len({k[':db/id'] for r in rows for k in r['kps']}),conversion_kps=len({k[':db/id'] for r in ready for k in r['kps']}),proposed_checkbox_fields=sum(len(r['atomic_options']) for r in ready),old_fields_to_detach=sum(len(r['old_fields']) for r in ready),old_entities_to_retain=sum(1+len(f[':answer-field/choices']) for r in ready for f in r['old_fields']),mapped_old_answers=sum(len(r['choice_mapping']) for r in ready),canonical_examples=0,learner_uses=0,prompt_qualifications=sum(bool(r['prompt_qualifications']) for r in ready))
    counts['unrated_conversions']=sum(not r['difficulty'] for r in ready)
    counts['duplicate_questions']=sum(len(r['old_fields'])==2 for r in rows)
    counts['single_field_questions']=sum(len(r['old_fields'])==1 for r in rows)
    data=dict(state='evaluated_not_prepared',basis=snap['basis'],lineage=snap['lineage'],database_writes=0,scope='All currently keyed cases in the remaining historical strong shortlist',counts=counts,questions=rows)
    (OUT/'keyed-resolutions.json').write_text(json.dumps(data,indent=2)+'\n')
    pending=[q[':db/id'] for q, in snap['questions'] if q[':db/id'] not in {r['question_eid'] for r in rows}]
    (OUT/'next-queue.json').write_text(json.dumps(dict(basis=snap['basis'],not_yet_evaluated_ids=sorted(pending),held_content_repair_ids=[r['question_eid'] for r in rows if r['decision']!='convert'],evaluated_conversion_ids=[r['question_eid'] for r in ready],database_writes=0),indent=2)+'\n')
    print(json.dumps(counts),flush=True)

if __name__=='__main__':main()
