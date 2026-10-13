"""Necessary prompt clarifications; proposed artifacts only, no EDB access."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[7]
IDS = ["q-71391","q-141209","q-141212","q-141218","q-38300","q-38305"]

def main():
    original_reviews = {q["ma_id"]:q for name in ["held-statements.json","held-exceptions.json"]
                        for q in json.loads((OUT/name).read_text())["questions"]}
    snapshot = OUT.parent / "review-snapshot.json"
    current = {q[":question/math-academy-id"]:q
               for chunk in json.loads(snapshot.read_text())["questions"] for q in chunk}
    rows = []
    for mid in IDS:
        review = original_reviews[mid]
        q = current[mid]
        assert q[":question/problem"] == review["problem"]
        converted = review["proposed_prompt"]
        atoms = review["atomic_options"]
        list_after = converted[converted.index("- **I.**"):]
        row = {
            "id":review["id"], "question_eid":review["id"], "ma_id":mid,
            "decision":"convert_with_necessary_prompt_clarification",
            "necessary":True, "necessity":"necessary_to_make_the_preserved_database_key_unambiguous",
            "original_prompt":review.get("historical_problem", q[":question/problem"]),
            "current_prompt":q[":question/problem"],
            "conversion_only_prompt":converted,
            "correct_labels":review["correct_labels"],
            "database_key":q[":question/answer-fields"][0][":answer-field/correct"],
            "key_change":False,
            "atomic_options":atoms, "choice_mapping":review["choice_mapping"],
            "original_solution_preserved":q[":question/worked-solution"],
            "source_evidence":{"path":str(snapshot.relative_to(ROOT)),"sha256":hashlib.sha256(snapshot.read_bytes()).hexdigest(),"question_eid":review["id"]},
            "source_list_preserved":True, "source_equations_preserved":True,
            "preview_status":"not_prepared", "commit_status":"not_submitted",
        }
        if mid == "q-71391":
            prefix = r"For the function $f(x,y)=\frac{2{x}^{2}+3{y}^{2}-4}{{y}^{2}}$, clear the denominator in $f(x,y)=c$ and classify the resulting conic equation in the entire $xy$-plane, including points excluded from the function's domain. Which of the following statements are true?"
            row.update({
                "issue_kind":"level_set_vs_associated_conic_equation",
                "rationale":"The current prompt names actual level curves of a rational function. They contain only points in its domain y!=0. The stored II/III key and source solution instead classify the complete conic equations obtained after clearing the denominator. Explicitly asking for these equations resolves the mismatch without changing any equation, listed case or key.",
                "without_clarification":{"interpretation":"Level curve means the complete set of domain-valid points with f(x,y)=c.","correct_labels":[],"proof":"c=3 gives two vertical lines each missing its y=0 point, not a hyperbola. c=0 gives the ellipse 2x^2+3y^2=4 minus (+/-sqrt(2),0), so not the entire ellipse. c=1 gives x^2+y^2=2 minus the same two points, so not the entire circle. Under this strict full-locus reading, all three statements are false."},
                "with_clarification_proof":"Clearing the denominator gives 2x^2+(3-c)y^2=4. In the entire plane, c=3 gives two lines x=+/-sqrt(2), c=0 gives an ellipse, and c=1 gives a circle. Thus exactly II and III apply.",
                "optional_solution_addition":"The original function has domain y!=0. The statements classify the full conic equations after clearing the denominator; the actual domain-restricted level sets omit (+/-sqrt(2),0).",
                "solution_change_required":False,
                "optional_prompt_repairs":[],
            })
        elif mid in {"q-141209","q-141212","q-141218"}:
            prefix = "Which of the following integrals have finite bounds of integration and an integrand that is unbounded at an endpoint or an interior point of the interval (improper integrals of the second kind on a finite interval)?"
            alternate = {"q-141209":["II","III"],"q-141212":["I","III"],"q-141218":["I","II"]}[mid]
            mixed = {"q-141209":"III has an infinite lower bound and an interior pole at x=0 in 1/x^3.",
                     "q-141212":"I has an infinite upper bound and an interior pole at x=1 in 1/(sqrt(x)-1).",
                     "q-141218":"II has an infinite upper bound and interior poles at x=pi/2+k*pi, k>=0, in sec(x)."}[mid]
            row.update({
                "issue_kind":"mixed_improper_integral_vs_finite_interval_second_kind",
                "rationale":"The source key uses an exclusive classification: second kind means a finite interval with an unbounded integrand, while an infinite interval is put in the first-kind category even when it also contains poles. The current prompt does not specify exclusivity. Explicit finite bounds state the intended selection predicate and remove dependence on naming conventions.",
                "without_clarification":{"interpretation":"A singular integrand makes an integral Type II even when it also has an infinite bound; it may be both Type I and Type II.","correct_labels":alternate,"proof":mixed+" This supplies an additional valid selection under a nonexclusive standard taxonomy."},
                "with_clarification_proof":"Apply the two explicit conditions, finite bounds and an unbounded integrand, to each displayed integral. "+" ".join(a["proof"]for a in atoms)+" Therefore the stored subset is correct under the clarified predicate.",
                "external_definition_evidence":[{
                    "title":"Athabasca University, Mathematics 266 Study Guide, Example 3.49 (printed page 114; PDF page 124)",
                    "url":"https://math266r8.athabascau.ca/266StudyGuide.pdf",
                    "relevance":"This university's own guide classifies the integral of 1/x from zero to infinity as both Type 1 and Type 2. Thus the original prompt cannot rely on universally exclusive categories."}],
                "optional_solution_addition":"The infinite-domain option also has singularities. It is excluded here because the question specifically asks for finite bounds; mixed improper integrals can exhibit both kinds of improperness.",
                "solution_change_required":False,
                "optional_prompt_repairs":[],
            })
        else:
            # Only the missing premise changes; preserve every displayed statement.
            prefix = converted.split("\n\nSelect all that apply.",1)[0]
            assert "If $T$ maps" in prefix
            prefix = prefix.replace("If $T$ maps", "If the linear transformation $T$ maps",1)
            slope = "(s,-3s)" if mid=="q-38300" else "(5s,6s)"
            row.update({
                "issue_kind":"missing_linear_map_premise",
                "rationale":"Rank-nullity and matrix nullity require a linear transformation. Onto a line alone neither provides a standard matrix nor guarantees a nontrivial zero fibre. The source solution explicitly invokes linearity, so supplying that premise recovers the intended problem rather than silently assuming an unstated restriction.",
                "without_clarification":{"interpretation":"T may be any map onto the specified line.","correct_labels":"underdetermined; II is not implied, and nullity is undefined for a general nonlinear map",
                    "proof":"Define s(u,v)=u if u!=0, and s(0,v)=v^2. This function is onto R and its zero fibre is only (0,0). The nonlinear map T(u,v)="+slope+" maps onto the specified line, yet T^{-1}(0)={(0,0)}. Thus even interpreting kernel as the zero fibre does not establish statement II. If kernel/nullity are reserved for linear maps, their use itself needs the missing linearity premise."},
                "with_clarification_proof":"A linear map R^2 onto the given nonzero line has rank 1. Rank-nullity yields nullity 2-1=1, so its kernel is nontrivial and II is true. "+" ".join(a["proof"]for a in atoms if a["label"]!="II"),
                "solution_change_required":False,
                "optional_prompt_repairs":[{"description":"Use a separate matrix symbol in statement III to avoid overloading T as both transformation and its standard matrix.","necessary":False}] if mid=="q-38305" else [],
            })
        proposed = prefix+"\n\nSelect all that apply.\n\n"+list_after
        assert proposed.count("Select all that apply.")==1
        assert proposed[proposed.index("- **I.**"):]==list_after
        row["proposed_prompt"] = proposed
        row["problem_after"] = proposed
        row["proposed_prompt_clarified_unlabelled"] = prefix+"\n\n"+"\n\n".join("- "+a["text"] for a in atoms)
        rows.append(row)
    result={"database_writes":0,"counts":{"reviewed":6,"necessary_prompt_clarifications":6,"optional_only":0,"key_changes":0,"required_solution_changes":0},
            "scope":"Supersedes the earlier nonblocking qualification assessment for these six cases. All must use the exact clarified prompt before preparing a key-preserving checkbox conversion.",
            "questions":rows}
    (OUT/"semantic-qualifications.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    (OUT/"semantic-qualifications.md").write_text("# Necessary semantic clarifications\n\nAll six cases need a prompt clarification to make their retained keys unambiguous. The earlier classification of these qualifications as nonblocking is superseded.\n\n- q-71391: ask for the full conic equations after clearing the denominator, since the actual level sets omit domain-excluded points.\n- q-141209, q-141212, q-141218: explicitly require finite bounds. Infinite-domain options also have poles and qualify as both types under a nonexclusive convention; [Athabasca University's Example 3.49](https://math266r8.athabascau.ca/266StudyGuide.pdf) uses that convention.\n- q-38300, q-38305: explicitly state that T is a linear transformation before applying rank-nullity. An arbitrary map onto a line can have a singleton zero fibre.\n\nExact original/current prompts, clarified conversion prompts, alternate readings and independent proofs are in semantic-qualifications.json. Equations, source list text, old-choice mappings and stored keys are preserved. No database writes.\n")
    print(json.dumps(result["counts"],indent=2))

if __name__=="__main__": main()
