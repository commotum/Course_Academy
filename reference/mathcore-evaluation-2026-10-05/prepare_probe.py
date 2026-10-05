"""Prepare saved-answer coverage and explicit equivalence/correctness probes.

The reused TeX interpreter is an authoring aid. This adapter is only an
evaluation fixture: it does not establish safe learner-input parsing.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_historical_question_formats import MathExpression


class PreservedConstants(MathExpression):
    def atom(self):
        token = self.peek()
        if token in (r"\pi", "e", "i") and token not in self.symbols:
            self.take()
            # Constants retain their names instead of becoming float literals.
            return ("constant", {r"\pi": "pi", "e": "e", "i": "(0+1i)"}[token])
        return super().atom()


def emit(tree):
    kind = tree[0]
    if kind == "num":
        return "(" + format(tree[1], ".17g") + ")"
    if kind in ("var", "constant"):
        return tree[1]
    if kind == "func":
        return tree[1] + "(" + emit(tree[2]) + ")"
    # Preserve a square root as a function call when the source used one.
    if kind == "^" and tree[2] == ("/", ("num", 1.0), ("num", 2.0)):
        return "sqrt(" + emit(tree[1]) + ")"
    return "(" + emit(tree[1]) + kind + emit(tree[2]) + ")"


base = ROOT / "reference/mathacademy/history-question-import-2026-10-04/format-audit"
readiness = json.loads((base / "runtime-readiness.json").read_text())
blocked = {q["math_academy_id"] for q in readiness["questions"] if not q["accepted_by_current_grader"]}
questions = json.loads((base / "questions.json").read_text())["questions"]
fields = []
for q in questions:
    if q["math_academy_id"] not in blocked:
        continue
    # In sigma/Riemann prompts, i is an index. In vector prompts it is a basis
    # label. In complex-number prompts it is the imaginary unit.
    symbolic_i = any(word in q["knowledge_point"] for word in ("Riemann", "Sigma", "Vector"))
    for f in q["answer_fields"]:
        row = {"question_id": q["math_academy_id"], "topic_id": q["topic_id"],
               "knowledge_point": q["knowledge_point"], "field_key": f["key"],
               "original": f["correct_value"], "adapted": None}
        try:
            parsed = PreservedConstants(f["correct_value"], symbols=("i",) if symbolic_i else ())
            row.update(adapted=emit(parsed.tree), variables=sorted(parsed.variables))
        except (ValueError, IndexError, RecursionError) as error:
            row["adapter_error"] = str(error)
        fields.append(row)

pairs = []
def pair(label, a, b, equivalent=True, question_id=None):
    pairs.append(dict(label=label, a=a, b=b, expected_equivalent=equivalent, question_id=question_id))

pair("combine like terms", "x+x", "2*x")
pair("commute coefficient", "7*b", "b*7", question_id="q-216930")
pair("factor common coefficient", "400*a+20*b", "20*(20*a+b)", question_id="q-167208")
pair("reorder polynomial", "x^2+11*x-28", "-28+11*x+x^2", question_id="q-288849")
pair("factor quadratic", "x^2-5*x-50", "(x-10)*(x+5)", question_id="q-288850")
pair("factor another quadratic", "x^2-30*x+200", "(x-10)*(x-20)", question_id="q-167228")
pair("expand partial sum", "k*(3-k)", "3*k-k^2", question_id="q-349085")
pair("negative power", "(-11)/x", "(-11)*x^(-1)", question_id="q-339941")
pair("expand rational denominator", "2/(x^2+1)^2", "2/(x^4+2*x^2+1)", question_id="q-344032")
pair("radical simplification", "2*sqrt(10)", "sqrt(40)", question_id="q-241753")
pair("rationalize conjugate", "(sqrt(6)-sqrt(2))/4", "1/(sqrt(6)+sqrt(2))", question_id="q-332492")
pair("rationalize geometric sum", "3*sqrt(3)/(sqrt(3)-1)", "(9+3*sqrt(3))/2", question_id="q-133330")
pair("rationalize variable radical positive x", "1/(3*sqrt(x))", "sqrt(x)/(3*x)", question_id="q-142993")
pair("trig Pythagorean identity", "sin(x)^2+cos(x)^2", "1")
pair("cosecant reciprocal", "csc(x)", "1/sin(x)", question_id="q-313722")
pair("odd sine", "sin(-x)", "-sin(x)", question_id="q-274499")
pair("linear same symbol cancellation", "x-x", "0")
pair("remove multiplication by one", "1*x", "x")
pair("remove addition of zero", "x+0", "x")
pair("rational arithmetic", "1/3+1/6", "1/2")
pair("wrong coefficient", "7*b", "8*b", False)
pair("wrong sign", "(-11)/x", "11/x", False)
pair("wrong polynomial constant", "x^2-5*x-50", "x^2-5*x-49", False)
pair("wrong trig identity", "sin(x)^2+cos(x)^2", "2", False)
pair("tiny nonzero coefficient must stay nonzero", "0.00000000000000001*x", "0", False)
pair("distinct large integers", "9007199254740992", "9007199254740993", False)

behavior = []
def behavior_case(label, expression, variables=None):
    behavior.append(dict(label=label, expression=expression, variables=variables or {}))

behavior_case("standard unary-minus precedence expects -4", "-x^2", {"x": 2})
behavior_case("standard numeric unary-minus precedence expects -4", "-2^2")
behavior_case("explicit negative square expects +4", "(-x)^2", {"x": 2})
behavior_case("implicit multiplication", "7b", {"b": 2})
behavior_case("adjacent single-letter variables", "ab", {"a": 2, "b": 3})
behavior_case("sqrt evaluable", "sqrt(10)")
behavior_case("ln evaluable", "ln(5)")
behavior_case("sec evaluable", "sec(0)")
behavior_case("csc evaluable", "csc(1)")
behavior_case("cot evaluable", "cot(1)")
behavior_case("bare imaginary unit", "8*i")
behavior_case("explicit imaginary unit", "8*(0+1i)")
behavior_case("undefined real logarithm", "ln(-1)")
behavior_case("zero denominator must stay undefined", "0*(1/0)")

output = {"fields": fields, "pairs": pairs, "behavior": behavior,
          "question_count": len(blocked),
          "source_sha256": hashlib.sha256((base / "questions.json").read_bytes()).hexdigest()}
(HERE / "inputs.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"blocked_questions": len(blocked), "answer_fields": len(fields),
                  "adapter_successes": sum(f["adapted"] is not None for f in fields), "equivalence_probes": len(pairs)}))
