"""Read complete learner operands, ordered dot-product factors and whole banks."""
import sys
sys.dont_write_bytecode = True
import copy, hashlib, importlib.util, json, re
from pathlib import Path
import sympy as s

R = Path(__file__).resolve().parent
K = 17592186100866
D = R.parents[2] / f"generate/scratch/{K}-draft"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

G = load("root_column2_generator", D.with_suffix(".py"))
F = load("root_column2_math_format", R.parents[2] / "scripts/question_capture/math_format.py")

def number(text):
    text = text.strip()
    while text.startswith("(") and text.endswith(")"):
        text = text[1:-1].strip()
    assert re.fullmatch(r"[+-]?\s*\d+(?:\.\d+)?", text), text
    return s.Rational(text.replace(" ", ""))

def arrays(text):
    return [[[cell.strip() for cell in row.split("&")] for row in match[1].split(chr(92)*2)]
            for match in re.finditer(r"\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}", text, re.S)]

def numerical(matrix):
    return s.Matrix([[number(cell) for cell in row] for row in matrix])

def signature(text):
    matrices = arrays(text)
    if matrices:
        assert len(matrices) == 1
        matrix = numerical(matrices[0])
        assert matrix.shape == (2, 1)
        return tuple(matrix)
    return (number(text),)

C = dict(records=0, prompt_cells=0, printed_operand_cells=0, ordered_dot_factors=0,
         retained_or_evaluated_cells=0, complete_answer_values=0, whole_method_banks=0,
         source_prompts=0, source_solutions=0, source_fields=0, source_values=0,
         source_keys=0, source_missing_keys=0)

def check(record):
    q = record["question"]
    shown = arrays(q[":question/problem"])
    assert len(shown) == 2
    A, V = map(numerical, shown)
    assert A.shape == (2, 2) and V.shape == (2, 1)
    target = A * V
    a, b, c, d = list(A)
    u, v = list(V)
    r, t = list(target)
    C["prompt_cells"] += 6
    for field in q[":question/answer-fields"]:
        values = [signature(answer[":answer/value"]) for answer in field[":answer-field/choices"]]
        assert len(values) == len(set(values))
        if ":answer-field/correct" in field:
            correct = next(answer for answer in field[":answer-field/choices"]
                           if answer[":answer/id"] == field[":answer-field/correct"][1])
            wanted = tuple(target) if field[":answer-field/type"].endswith("/radio") else (target[int(field[":answer-field/key"][-1])-1],)
            assert signature(correct[":answer/value"]) == wanted
        if field[":answer-field/type"].endswith("/blank"):
            assert "{{" + field[":answer-field/key"] + "}}" in q[":question/problem"]
        if len(values) == 5 and not record["generation"]["evidence_only"]:
            profile = record["generation"]["bank_profile"]
            if profile == "source-method:q-13564":
                expected = [(r,t),(-r,-t),(r,-t),(-r,t),(v,u)]
            elif profile == "source-method:q-126511":
                expected = [(r,t),(a+b,c+d),(-a-b,-c-d),(t,r),(a,c)]
            elif profile == "source-method:q-13565":
                expected = [(r,t),(-t,-r),(r,-t),(-r,-t),(-t,r)]
            elif profile == "source-method:q-13555":
                expected = [(r,t),(r,r),(r,-t),(-r,-t),(-r,t)]
            else:
                assert profile == "authored-method"
                expected = [(r,t),tuple(A.T*V),(a*u,c*u),(b*v,d*v),(t,r)]
            assert len(set(expected)) == 5 and set(values) == set(expected)
            C["whole_method_banks"] += 1
        C["complete_answer_values"] += len(values)
    if ":question/worked-solution" not in q:
        return
    solution = q[":question/worked-solution"]
    matrices = arrays(solution)
    named = record["generation"]["template"].startswith("named")
    assert len(matrices) == (9 if named else 11)
    dot_rows = []
    stars = 0
    for index, matrix in enumerate(matrices):
        if len(matrix[0]) == 2:
            assert numerical(matrix) == A
            assert numerical(matrices[index+1]) == V
            C["printed_operand_cells"] += 6
            continue
        if index and len(matrices[index-1][0]) == 2:
            continue
        assert len(matrix) == 2 and all(len(row) == 1 for row in matrix)
        for row_index, row in enumerate(matrix):
            cell = row[0]
            if cell == "∗":
                assert row_index == 1
                stars += 1
            elif r"\cdot" in cell:
                match = re.fullmatch(r"(.*?)\\cdot\s*(.*?)\+(.*?)\\cdot\s*(.*?)", cell)
                assert match
                operands = [number(part) for part in match.groups()]
                assert operands == [A[row_index,0],V[0],A[row_index,1],V[1]]
                dot_rows.append(row_index)
                C["ordered_dot_factors"] += 4
            else:
                assert number(cell) == target[row_index]
                C["retained_or_evaluated_cells"] += 1
    assert dot_rows == [0,1] and stars == 2
    if named:
        label = re.search(r"Find \$([A-Z][a-z])\$", q[":question/problem"])[1]
        assert "Therefore, \n$" + label + "=" in solution
    assert numerical(matrices[-1]) == target
    assert solution.count("Multiplying the first row, we get") == 1
    assert solution.count("Multiplying the second row, we get") == 1
    C["records"] += 1

if __name__ == "__main__":
    frozen = json.loads((R/"refresh-2026-10-14/sources"/f"{K}.json").read_text())
    assert json.loads((D/"source.json").read_text()) == frozen
    originals = {q[":question/math-academy-id"]:q for q in frozen["record"][":knowledge-point/questions"]}
    for case in json.loads((D/"source-cases.json").read_text()):
        record = G.generate(case["level"], template=case["template"],
                            parameters=case["parameters"], profile=case["bank_profile"])
        check(record)
        q, old = record["question"], originals[case["source_id"]]
        assert q[":question/problem"] == F.normalize_prose(old[":question/problem"])
        C["source_prompts"] += 1
        for key in (":question/difficulty",":question/worked-solution",":question/answer-fields"):
            assert (key in q) == (key in old)
        if ":question/worked-solution" in old:
            assert q[":question/worked-solution"] == F.normalize_prose(old[":question/worked-solution"])
            C["source_solutions"] += 1
        assert len(q[":question/answer-fields"]) == len(old[":question/answer-fields"])
        for field, source_field in zip(q[":question/answer-fields"],old[":question/answer-fields"]):
            assert field[":answer-field/key"] == source_field[":answer-field/key"]
            assert field[":answer-field/type"] == source_field[":answer-field/type"][":db/ident"]
            assert sorted(signature(a[":answer/value"]) for a in field[":answer-field/choices"]) == sorted(signature(a[":answer/value"]) for a in source_field[":answer-field/choices"])
            assert (":answer-field/correct" in field) == (":answer-field/correct" in source_field)
            if ":answer-field/correct" in source_field:
                answer = next(a for a in field[":answer-field/choices"] if a[":answer/id"] == field[":answer-field/correct"][1])
                assert signature(answer[":answer/value"]) == signature(source_field[":answer-field/correct"][":answer/value"])
                C["source_keys"] += 1
            else:
                C["source_missing_keys"] += 1
            C["source_fields"] += 1
            C["source_values"] += len(source_field[":answer-field/choices"])
    records = json.loads((R/f"qa/{K}-sampled.json").read_text())
    for record in records:
        check(record)
    probe = copy.deepcopy(records[0])
    solution = probe["question"][":question/worked-solution"]
    first_dot = next(matrix[0][0] for matrix in arrays(solution) if r"\cdot" in matrix[0][0])
    bad_dot = first_dot.replace(r"\cdot", "+", 1)
    probe["question"][":question/worked-solution"] = solution.replace(first_dot, bad_dot, 1)
    saved = C.copy()
    try:
        check(probe)
    except AssertionError:
        pass
    else:
        raise AssertionError("Missing multiply operation survived with unchanged answer")
    C.clear();C.update(saved)
    proof = dict(status="passed", kp_id=K, readback=C,
                 missing_dot_operation_rejected=True,
                 script_sha256=hashlib.sha256(D.with_suffix(".py").read_bytes()).hexdigest())
    (R/f"qa/{K}-root-readback.json").write_text(json.dumps(proof,indent=2)+"\n")
    print(json.dumps(proof))
