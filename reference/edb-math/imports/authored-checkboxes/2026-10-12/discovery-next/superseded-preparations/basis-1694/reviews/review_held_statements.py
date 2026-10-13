"""Independent review of historical held statements; never opens or writes EDB."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
REPORT = ROOT / "generate/reports/checkbox-discovery-2026-10-12"
OUT = Path(__file__).resolve().parent

# Each row is independently derived from the problem, in source statement order.
# The source worked solution is evidence, not the authority for these verdicts.
PROOFS = {
    "q-2459": ("second_derivative", [
        "f'(x)=12x(1-x), f''(x)=12-24x, so f''(0)=12>0.",
        "f'(0)=0 and f''(0)=12>0 imply a strict relative minimum at 0.",
        "f''(1)=12-24=-12<0.",
        "f'(1)=0 and f''(1)=-12<0 imply a strict relative maximum at 1."], [1,1,1,1]),
    "q-35534": ("level_curve", [
        "f=c gives (c-2)x^2+cy^2=1; c=1 gives y^2-x^2=1, a hyperbola.",
        "c=2 gives 2y^2=1, two horizontal lines, rather than a parabola.",
        "c=3 gives x^2+3y^2=1, an ellipse. None of these loci contains the excluded origin."], [1,0,1]),
    "q-36829": ("level_curve", [
        "f=xy(x^2-y). No nonzero level contains an affine line: on x=at+b,y=dt+e with a*d!=0 its t^4 coefficient is a^3*d; vertical/horizontal lines have nonconstant quadratic/cubic terms unless x=0 or y=0, where f=0. Thus level -1 is not a line.",
        "xy(x^2-y)=0 is exactly x=0, y=0, or y=x^2: the two axes and a parabola.",
        "The same affine-line coefficient argument rules out even one line on level +1, hence rules out two lines."], [0,1,0]),
    "q-71892": ("region_both", [
        "D={-2<=x<=2, -3<=y<=1-x^2}; every vertical section is an interval.",
        "D={-3<=y<=1, -sqrt(1-y)<=x<=sqrt(1-y)}; every horizontal section is an interval.",
        "Both interval descriptions apply, so 'neither' is false."], [1,1,0]),
    "q-71895": ("region_neither", [
        "The region is inside the radius-2 circle and outside the radius-1 circle centered at (0,1). At x=3/4 the outer section spans +/-sqrt(55)/4, but the interior interval (1-sqrt(7)/4,1+sqrt(7)/4) is removed. It has two components, so is not type I.",
        "At y=1 the section is [-sqrt(3),-1] union [1,sqrt(3)], so is not type II.",
        "The disconnected vertical and horizontal sections establish neither type I nor type II."], [0,0,1]),
    "q-129405": ("path_limit", [
        "Along y=0, (2x^2-y^2)/(x^2+2y^2)=2 for x!=0.",
        "Along y=x, the ratio is x^2/(3x^2)=1/3 for x!=0.",
        "The two domain-valid paths have different limits, 2 and 1/3; the two-variable limit does not exist."], [1,1,1]),
    "q-168841": ("region_both", [
        "The triangle has vertices (0,-1),(0,1),(1,0) and D={0<=x<=1, x-1<=y<=1-x}, with interval vertical sections.",
        "D={-1<=y<=1, 0<=x<=1-|y|}, with interval horizontal sections.",
        "The triangle is both type I and type II, so 'neither' is false."], [1,1,0]),
    "q-170647": ("linear_transformation", [
        "For v=(1,0), k=2: T(2v)=(4,0), whereas 2T(v)=(2,0). Homogeneity fails.",
        "For v1=v2=(1,0): T(v1+v2)=(4,0), whereas T(v1)+T(v2)=(2,0). Additivity fails.",
        "A linear map must satisfy homogeneity and additivity; the counterexamples prove T is not linear."], [0,0,1]),
    "q-2469": ("second_derivative", [
        "f''(0)=12>0, so f''(0)<0 is false.",
        "f'(x)=12x(1-x), f'(0)=0 and f''(0)=12>0 give a relative minimum at 0.",
        "f''(1)=12-24=-12<0, so f''(1)>0 is false.",
        "f'(1)=0 and f''(1)=-12<0 give a relative maximum at 1."], [0,1,0,1]),
    "q-2471": ("second_derivative", [
        "f'(x)=15x(x+2), f''(x)=30x+30; f''(0)=30>0.",
        "f'(0)=0 and f''(0)>0 make 0 a relative minimum, so the maximum statement is false.",
        "f''(-2)=-60+30=-30<0.",
        "f'(-2)=0 and f''(-2)<0 make -2 a relative maximum, so the minimum statement is false."], [1,0,1,0]),
    "q-334851": ("big_o", [
        "f(x)=3x^5-2x tends to 0 as x->0 and is bounded near 0, hence O(1).",
        "|f(x)/x^2|=|3x^3-2/x| is unbounded as x->0; equivalently |f|~2|x|. Hence not O(x^2).",
        "|f(x)/x^3|=|3x^2-2/x^2| tends to infinity as x->0, hence not O(x^3)."], [1,0,0]),
    "q-335020": ("big_o", [
        "f/x^5=2/x+5/x^3+10/x^5 tends to 0 at +infinity; the ratio is bounded, hence O(x^5).",
        "f/x^2=2x^2+5+10/x^2 tends to +infinity, hence not O(x^2).",
        "f/1=2x^4+5x^2+10 tends to +infinity, hence not O(1)."], [1,0,0]),
    "q-48167": ("discontinuity", [
        "At 1, the left limit is 1^2+3=4, the right limit is 1-1^3=0, and f(1)=0. Distinct finite one-sided limits establish a jump.",
        "A removable discontinuity requires equal finite one-sided limits; 4!=0.",
        "The two-sided limit fails to exist, so the function is not continuous at 1."], [1,0,0]),
    "q-71391": ("level_curve_domain_qualification", [
        "On the domain y!=0, f=c gives 2x^2+(3-c)y^2=4. At c=3 this is x=+/-sqrt(2), with y!=0: two punctured vertical lines, not a hyperbola.",
        "At c=0 the implicit conic is 2x^2+3y^2=4, an ellipse. The actual level set omits (+/-sqrt(2),0) because y!=0; the source key uses the standard classification by implicit conic shape.",
        "At c=1 the implicit conic is x^2+y^2=2, a circle. The actual level set omits (+/-sqrt(2),0); the source key classifies its conic shape."], [0,1,1]),
    "q-71395": ("level_curve", [
        "For nonnegative c, sqrt(x^2-2y^2)=c iff x^2-2y^2=c^2. At c=1 it is a hyperbola, not a line.",
        "At c=2, x^2-2y^2=4 is a hyperbola.",
        "At c=0, x^2-2y^2=0 factors into the two lines y=+/-x/sqrt(2); these lie in the square-root domain."], [0,1,1]),
    "q-72185": ("region_both", [
        "D={-1<=x<=1, -sqrt(1-x^2)<=y<=sqrt(1-x^2)} has interval vertical sections.",
        "D={-1<=y<=1, -sqrt(1-y^2)<=x<=sqrt(1-y^2)} has interval horizontal sections.",
        "The disk is both types, so 'neither' is false."], [1,1,0]),
    "q-72186": ("region_type_i", [
        "4-x^2>=2-|x| iff |x|<=2. Thus D={-2<=x<=2, 2-|x|<=y<=4-x^2} has interval vertical sections.",
        "At y=1 the inequalities give 1<=|x|<=sqrt(3), so the section [-sqrt(3),-1] union [1,sqrt(3)] is disconnected. Not type II.",
        "It is type I, so 'neither' is false."], [1,0,0]),
    "q-72187": ("region_neither", [
        "For 1<=x^2+y^2<=2, x=1/2 gives sqrt(3)/2<=|y|<=sqrt(7)/2: two disjoint intervals. Not type I.",
        "At y=1/2 the same bounds hold for |x|, giving two intervals. Not type II.",
        "Both required interval properties fail, so 'neither' is true."], [0,0,1]),
    "q-73549": ("region_neither", [
        "For 1<=4x^2+y^2<=4, x=1/4 gives sqrt(3)/2<=|y|<=sqrt(15)/2, two disjoint intervals. Not type I.",
        "At y=1/2, sqrt(3)/4<=|x|<=sqrt(15)/4, two disjoint intervals. Not type II.",
        "Both interval properties fail, so 'neither' is true."], [0,0,1]),
    "q-74964": ("path_limit", [
        "Along y=x, the ratio simplifies to 2x/(2x-1), whose limit is 0. The path is in the domain for sufficiently small nonzero x.",
        "Along y=x^2, the ratio is 2x^2/x^2=2 for x!=0.",
        "Different path limits 0 and 2 show the overall limit does not exist; it cannot exist and equal 2."], [1,1,0]),
    "q-8022": ("linear_transformation", [
        "T(v)=Av for A=[[1,1],[0,2]], so T(kv)=A(kv)=kAv=kT(v).",
        "Matrix distributivity gives T(v1+v2)=Av1+Av2=T(v1)+T(v2).",
        "Both defining linearity identities hold for every real vector/scalar, so T is linear."], [1,1,1]),
    "q-71402": ("level_curve", [
        "9x+3y-4=c iff y=-3x+(c+4)/3. At c=0 this is a line, not an ellipse.",
        "At c=-4 the locus is y=-3x, a line.",
        "At c=5 the locus is y=-3x+3, a line rather than a hyperbola."], [0,1,0]),
    "q-35538": ("level_curve", [
        "4x-3y-1=c iff y=(4/3)x-(c+1)/3. At c=-1 it is the line y=(4/3)x.",
        "At c=0 it is y=(4/3)x-1/3, a single line, not the union of the axes.",
        "At c=2 it is y=(4/3)x-1, a line rather than a parabola."], [1,0,0]),
    "q-71398": ("level_curve", [
        "For c>=0, sqrt(x^2+2y)=c iff y=(c^2-x^2)/2. At c=0 this is a parabola, not a circle.",
        "At c=1, y=(1-x^2)/2 is a parabola, not a hyperbola.",
        "At c=2, y=(4-x^2)/2 is a parabola. Each of these curves lies in the square-root domain."], [0,0,1]),
    "q-71401": ("level_curve", [
        "On (x,y)!=(0,0), f=c gives cx^2+(c-2)y^2=1. At c=1, x^2-y^2=1 is a hyperbola, not an ellipse.",
        "At c=2, 2x^2=1 gives the two vertical lines x=+/-1/sqrt(2); neither contains the excluded origin.",
        "At c=3, 3x^2+y^2=1 is an ellipse, not a hyperbola, and does not contain the excluded origin."], [0,1,0]),
    "q-7639": ("ellipse", [
        "Completing squares gives (x-1)^2+2(y+3)^2=8, so the center is (1,-3).",
        "The semiaxes are sqrt(8)=2sqrt(2) and 2. The major axis length is 4sqrt(2), not 2sqrt(2).",
        "The minor axis length is twice its semiaxis 2, hence 4."], [1,0,1]),
    "q-168921": ("region_neither", [
        "The region is inside x^2+y^2<=4 and outside 4x^2+(y+1)^2<1. At x=2/5 the outer section is +/-4sqrt(6)/5 and the inner interval (-8/5,-2/5) is removed, leaving two intervals. Not type I.",
        "At y=-1 the section is [-sqrt(3),-1/2] union [1/2,sqrt(3)], so not type II.",
        "The disconnected sections establish neither type I nor type II."], [0,0,1]),
    "q-35527": ("level_curve", [
        "xy=1 becomes a rectangular hyperbola (under rotated coordinates, a difference of two squares equals a nonzero constant).",
        "xy=-1 is also a rectangular hyperbola, not a parabola.",
        "xy=0 iff x=0 or y=0, exactly the two axes."], [1,0,1]),
    "q-38715": ("discontinuity", [
        "At 0 the left limit of (x-1)^3 is -1 and the right limit of x^6+1 is 1; unequal one-sided limits exclude a removable discontinuity.",
        "The one-sided limits -1 and 1 are finite and unequal, establishing a jump at 0.",
        "f(0)=1, but the two-sided limit does not exist, so continuity fails."], [0,1,0]),
    "q-48144": ("discontinuity", [
        "Both one-sided limits at -1 are 3(-1)-1=-4, whereas f(-1)=4. The finite limit/value mismatch is removable.",
        "Equal one-sided limits rule out a jump.",
        "The limiting value -4 differs from the function value 4, so continuity fails."], [1,0,0]),
    "q-72345": ("region_both", [
        "In the first quadrant the bounded region is D={0<=x<=1, x^3<=y<=x}, giving interval vertical sections.",
        "Equivalently D={0<=y<=1, y<=x<=cuberoot(y)}, giving interval horizontal sections.",
        "Both type descriptions hold, so 'neither' is false."], [1,1,0]),
    "q-73552": ("region_neither", [
        "The inner ellipse is contained in the outer one: on its boundary x=1+cos(t), y=sin(t)/2, x^2+4y^2=2+2cos(t)<=4. At x=1 the outer section spans +/-sqrt(3)/2 and the inner interval (-1/2,1/2) is removed. Not type I.",
        "At y=1/4 the outer section is [-sqrt(15)/2,sqrt(15)/2], and the inner interval (1-sqrt(3)/2,1+sqrt(3)/2) is removed strictly inside it, leaving two intervals. Not type II.",
        "Both interval properties fail, so 'neither' is true."], [0,0,1]),
    "q-72160": ("region_both", [
        "In the first quadrant the bounded region is D={0<=x<=1, x^3<=y<=cuberoot(x)}, giving interval vertical sections.",
        "Equivalently D={0<=y<=1, y^3<=x<=cuberoot(y)}, giving interval horizontal sections.",
        "Both type descriptions hold, so 'neither' is false."], [1,1,0]),
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def subset(value):
    # All five options in every held case are explicit Roman-label subsets.
    assert not re.search(r"\b(?:or|none|all)\b", value, re.I), value
    labels = re.findall(r"\b(?:IV|III|II|I)\b", value)
    assert labels and len(labels) == len(set(labels)), value
    rest = re.sub(r"\b(?:IV|III|II|I|and|only)\b|[ ,.]", "", value)
    assert not rest, (value, rest)
    return labels

def repairs(ma_id, solution):
    notes = []
    proposed = solution
    if ma_id in {"q-2459", "q-2469", "q-2471"}:
        proposed = re.sub(r"\bVI\b", "IV", proposed)
        notes.append({"kind":"solution_label_typo", "required_for_consistent_solution":True,
                      "description":"Replace the out-of-universe label VI with IV. Source statement order, exact derivative proof and final answer all establish IV."})
    elif ma_id == "q-334851":
        notes.append({"kind":"solution_mathematical_errors", "required_for_consistent_solution":True,
                      "description":"Remove the stray +1 in the restated function, change statement II verdict to false, and replace incorrect signed/two-sided infinity claims with absolute-ratio unboundedness. Existing prompt and key are correct."})
        proposed = "For $f(x)=3x^5-2x$, we have $f(x)\\to0$ as $x\\to0$, so $f$ is bounded near zero and is $O(1)$.\n\nFor statement II, $|f(x)/x^2|=|3x^3-2/x|$ is unbounded near zero, so $f$ is not $O(x^2)$. For statement III, $|f(x)/x^3|=|3x^2-2/x^2|\\to\\infty$, so $f$ is not $O(x^3)$.\n\nTherefore, statement I is true, and statements II and III are false. The correct answer is \"I only.\""
    elif ma_id == "q-335020":
        proposed = proposed.replace("Statement III is true.", "Statement III is false.")
        notes.append({"kind":"solution_verdict_typo", "required_for_consistent_solution":True,
                      "description":"Change statement III's introductory verdict from true to false. Its displayed divergent ratio and conclusion already prove not O(1), agreeing with the existing I-only key."})
    elif ma_id == "q-71892":
        before = r"-\sqrt{1-y}\le y\le \sqrt{1-y}"
        assert before in proposed
        proposed = proposed.replace(before, r"-\sqrt{1-y}\le x\le \sqrt{1-y}")
        notes.append({"kind":"solution_bound_variable_typo", "required_for_consistent_solution":True,
                      "description":"In the type-II description replace the middle y in -sqrt(1-y)<=y<=sqrt(1-y) with x. The horizontal interval is for x."})
    elif ma_id == "q-71402":
        assert r"\frac{c+4}{9}" in proposed and r"\frac{4}{9}" in proposed
        proposed = proposed.replace(r"\frac{c+4}{9}",r"\frac{c+4}{3}").replace(r"\frac{4}{9}",r"\frac{4}{3}")
        notes.append({"kind":"solution_algebra_typo", "required_for_consistent_solution":True,
                      "description":"From 3y=-9x+c+4, the intercept is (c+4)/3, not /9; likewise the c=0 intercept is 4/3. Shapes and existing II-only key are unchanged."})
    elif ma_id == "q-71391":
        proposed += "\n\nThe function is defined only when $y\\ne0$. Thus each of these loci excludes any points with $y=0$. Statements II and III classify the implicit conic shapes; the actual ellipse and circle level sets omit the points $(\\pm\\sqrt{2},0)$."
        notes.append({"kind":"solution_domain_qualification", "required_for_consistent_solution":False,
                      "description":"The rational-function domain y!=0 removes two points from the named ellipse/circle and one point from each c=3 line. The existing key classifies conic shape. Preserve it and explicitly qualify the omitted points; a strict full-locus reading would need a separate content decision."})
    return notes, proposed if notes else None

def main():
    held_path = REPORT / "direct-candidates.json"
    provisional_path = REPORT / "direct-format-provisional.json"
    solutions_path = REPORT / "direct-worked-solutions.json"
    metadata_path = REPORT / "readiness-metadata.json"
    held = {q["id"]:q for q in json.loads(held_path.read_text())["held"]}
    qs = [q for q in json.loads(provisional_path.read_text()) if q["id"] in held]
    solutions = {q[":db/id"]:q[":question/worked-solution"] for q in json.loads(solutions_path.read_text())}
    metadata = {q[":db/id"]:q for q in json.loads(metadata_path.read_text())}
    current_path = OUT.parent / "review-snapshot.json"
    current = {q[":db/id"]:q for chunk in json.loads(current_path.read_text())["questions"] for q in chunk}
    assert len(qs) == len(held) == len(PROOFS) == 33
    reviews = []
    for q in qs:
        evidence = []
        for kp in q["kps"]:
            path = REPORT / f"sources/{kp['id']}.json"
            source = json.loads(path.read_text())
            raw = next(x for x in source[":knowledge-point/questions"] if x[":db/id"] == q["id"])
            assert raw[":question/problem"] == q["problem"]
            assert raw[":question/answer-fields"] == q["fields"]
            evidence.append({"path":str(path.relative_to(ROOT)),"sha256":digest(path),
                             "question_pointer":f":knowledge-point/questions[:db/id={q['id']}]"})
        field = q["fields"][0]
        assert len(q["fields"]) == 1
        key = field[":answer-field/correct"]
        assert subset(key[":answer/value"]) == q["correct_labels"]
        mfield = metadata[q["id"]][":question/answer-fields"][0]
        assert mfield[":answer-field/correct"][":db/id"] == key[":db/id"]
        group, proofs, truths = PROOFS[q["ma_id"]]
        assert len(proofs) == len(truths) == len(q["atomic_options"])
        atoms = [{**a,"truth":bool(t),"proof":p} for a,t,p in zip(q["atomic_options"],truths,proofs)]
        derived = [a["label"] for a in atoms if a["truth"]]
        assert derived == q["correct_labels"], (q["ma_id"],derived,q["correct_labels"])
        mapping = [{"answer_eid":a[":db/id"],"value":a[":answer/value"],"labels":subset(a[":answer/value"])} for a in field[":answer-field/choices"]]
        assert all(set(a["labels"]) <= {x["label"] for x in atoms} for a in mapping)
        assert len({tuple(sorted(a["labels"])) for a in mapping}) == len(mapping)
        assert any(a["answer_eid"] == key[":db/id"] and a["labels"] == derived for a in mapping)
        start = re.search(r"^(?:- |I\. )",q["problem"],re.M)
        assert start
        prefix = q["problem"][:start.start()].rstrip()
        prompt = prefix + "\n\nSelect all that apply.\n\n" + "\n".join(f"- **{a['label']}.** {a['text']}" for a in atoms)
        notes, proposed_solution = repairs(q["ma_id"],solutions[q["id"]])
        row = {
            "id":q["id"],"question_eid":q["id"],"ma_id":q["ma_id"],"math_academy_id":q["ma_id"],
            "decision":"convert","classification":group,
            "reason":"Finite independently testable statement list; every old choice maps uniquely to a subset. Stored database key retained and independently checked against the source problem.",
            "historical_hold_reasons":held[q["id"]]["reasons"],
            "captured_basis":1534,"captured_database":"math","source_evidence":evidence,
            "kps":q["kps"],"difficulty":q["difficulty"],"problem":q["problem"],"fields":q["fields"],
            "database_key":{"field_eid":field[":db/id"],"answer_eid":key[":db/id"],"value":key[":answer/value"],"labels":derived},
            "atomic_options":atoms,"choice_mapping":mapping,"source_choice_to_checked_labels":mapping,
            "correct_labels":derived,"proposed_prompt":prompt,"problem_after":prompt,
            "worked_solution":solutions[q["id"]],"content_repairs":notes,
            "key_evidence":"Existing database key in raw source snapshot and matching readiness metadata; independent exact proof recorded per statement. No study-vault keys used.",
            "key_change":False,"preserve_difficulty_memberships":True,
            "learner_mapping_rule":"For every old choice, select exactly its mapped labels, even if wrong; explicit false for all other atomic fields. Root must reconcile current uses, memberships, ownership and metadata before preparation.",
            "live_state_reconciliation":"pending_root","preview_status":"not_prepared","commit_status":"not_submitted",
            "unavailable_evidence":[],
        }
        if proposed_solution is not None:
            row["proposed_worked_solution"] = proposed_solution
        # Reconcile exact current text without overwriting rendering fixes from
        # historical discovery. Mathematical text and old answer meanings must
        # still agree; only whitespace and escaped set braces changed here.
        c = current[q["id"]]
        assert re.sub(r"\s+", " ",c[":question/problem"]) == re.sub(r"\s+", " ",q["problem"])
        cf = c[":question/answer-fields"][0]
        assert len(c[":question/answer-fields"]) == 1
        assert cf[":answer-field/correct"][":db/id"] == key[":db/id"]
        assert [(a[":db/id"],a[":answer/value"]) for a in cf[":answer-field/choices"]] == [(a["answer_eid"],a["value"]) for a in mapping]
        normal_solution = lambda s: s.replace(r"\{", "{").replace(r"\}", "}")
        assert normal_solution(c[":question/worked-solution"]) == normal_solution(solutions[q["id"]])
        row["historical_problem"] = row["problem"]
        row["historical_worked_solution"] = row["worked_solution"]
        row["current_source"] = c
        row["problem"] = c[":question/problem"]
        row["fields"] = c[":question/answer-fields"]
        row["worked_solution"] = c[":question/worked-solution"]
        row["content_repairs"], proposed_current_solution = repairs(q["ma_id"], row["worked_solution"])
        if proposed_current_solution is not None:
            row["proposed_worked_solution"] = proposed_current_solution
        row["current_text_changes"] = {"problem":row["historical_problem"]!=row["problem"],"worked_solution":row["historical_worked_solution"]!=row["worked_solution"]}
        row["current_source_evidence"] = {"path":str(current_path.relative_to(ROOT)),"question_eid":q["id"],"sha256":digest(current_path)}
        row["live_state_reconciliation"] = "Exact current prompt, solution, old option text/IDs and key reconciled; incoming uses and ownership pending root."
        reviews.append(row)
    counts = {
        "reviewed":len(reviews),"convert":len(reviews),"retain_radio":0,"needs_evidence":0,"key_changes":0,
        "atomic_options":sum(len(q["atomic_options"]) for q in reviews),
        "old_choices_mapped":sum(len(q["choice_mapping"]) for q in reviews),
        "knowledge_points":len({k["id"] for q in reviews for k in q["kps"]}),
        "classes":dict(Counter(q["classification"] for q in reviews)),
        "questions_with_required_solution_repairs":sum(any(n["required_for_consistent_solution"] for n in q["content_repairs"]) for q in reviews),
        "questions_with_domain_qualification":sum(q["classification"]=="level_curve_domain_qualification" for q in reviews),
    }
    result = {
        "database":"math","basis":1534,"database_writes":0,"counts":counts,
        "scope":"Independent review of the 33 historical held statements. No live-state assumptions or transaction preparation.",
        "reviewer_source":":agent/gpt-6.1-sol-high",
        "evidence_files":[{"path":str(p.relative_to(ROOT)),"sha256":digest(p)} for p in [held_path,provisional_path,solutions_path,metadata_path,current_path]],
        "questions":reviews,
    }
    (OUT / "held-statements.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    text = ["# Held statement review", "", "Reviewed all 33 historical held cases at discovery basis 1534. No database writes or existing artifact edits.","",
            f"All 33 support checkbox conversion under their stored source keys: {counts['atomic_options']} atomic statements and {counts['old_choices_mapped']} complete old-choice mappings across {counts['knowledge_points']} KPs. No missing keys, key changes, or unavailable capture evidence.","",
            "The 28 cases without source-verdict conflicts were held because the scanner did not recognize wording such as 'only statements', 'also true', or bare Roman labels. Independent proofs and raw source comparisons resolve these holds.","",
            "Seven worked solutions need corrections while preserving their existing keys:","",
            "- q-2459, q-2469, q-2471: VI is a typo for source statement IV.",
            "- q-334851: remove stray +1, mark II false, and correct the signed/two-sided infinity arguments using absolute ratios.",
            "- q-335020: mark III false; its own computation already establishes not O(1).",
            "- q-71892: the type-II horizontal bounds constrain x, not y.",
            "- q-71402: dividing 3y=-9x+c+4 gives intercept (c+4)/3, not /9.","",
            "q-71391 additionally needs a domain qualification: y!=0 removes two points from the implicit ellipse and circle. Its existing II/III key uses conic-shape classification. The review preserves that convention and records the exact omissions; a strict full-locus interpretation would require a separate content decision.","",
            "The JSON separates conversion-only proposed prompts from proposed worked-solution repairs. Root must reconcile current state and decide which explicit solution repairs to include before creating or previewing transactions.","",
            "| Class | Questions |","|---|---|",
            *[f"| {k} | {v} |" for k,v in sorted(counts["classes"].items())],"",
            "Reproduce this isolated file analysis with `python3 reviews/review_held_statements.py`. It reads historical JSON snapshots only and asserts every source prompt/field, key, option mapping and independently derived verdict."]
    (OUT / "held-statements.md").write_text("\n".join(text)+"\n")
    print(json.dumps(counts,indent=2))

if __name__ == "__main__":
    main()
