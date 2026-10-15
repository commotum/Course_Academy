"""Independent printed matrix, cofactor operands, statements and checkbox readback."""
import sys
sys.dont_write_bytecode = True
import copy, hashlib, importlib.util, json, re
from pathlib import Path
import sympy as s

R = Path(__file__).resolve().parent
K = 17592186059848
D = R.parents[2] / f"generate/scratch/{K}-draft"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

P = load("root_singular_scalar", R / "ode-scalar-parser.py")
G = load("root_singular_generator", D.with_suffix(".py"))

def scalar(text):
    return P.scalar(text.strip().rstrip(".,"))

def same(a, b):
    return s.simplify(a - b) == 0

def arrays(text):
    found = []
    pattern = r"\\begin\{(aligned|bmatrix|vmatrix)\}((?:(?!\\begin\{).)*?)\\end\{\1\}"
    for match in re.finditer(pattern, text, re.S):
        body = match[2]
        if "=" in body:
            continue
        rows = [row.split("&") for row in body.split(chr(92) * 2)]
        if len(rows) not in (2, 3) or any(len(row) != len(rows) for row in rows):
            continue
        found.append((match, s.Matrix([[scalar(cell) for cell in row] for row in rows])))
    return found

def signed_terms(text):
    text = text.strip()
    depth = 0
    start = 0
    terms = []
    for i, char in enumerate(text):
        if char in "({[":
            depth += 1
        elif char in ")}]":
            depth -= 1
        elif char in "+-" and depth == 0 and i > start and text[start:i].strip():
            terms.append(text[start:i])
            start = i
    assert depth == 0
    terms.append(text[start:])
    return terms

def parentheses(text):
    depth = 0
    start = None
    result = []
    for i, char in enumerate(text):
        if char == "(":
            if depth == 0:
                start = i
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                result.append(text[start + 1:i])
    assert depth == 0
    return result

C = dict(records=0, prompt_cells=0, determinant_cells=0, minor_cells=0,
         separate_cofactor_coefficients=0, separate_minor_products=0,
         evaluated_cofactor_operands=0, complete_stage_equalities=0,
         statements=0, Boolean_values=0, conclusions=0, workload_checks=0)

def check(record):
    q = record["question"]
    matrix_arrays = arrays(q[":question/problem"])
    assert len(matrix_arrays) == 1
    matrix = matrix_arrays[0][1]
    assert matrix.shape == (3, 3)
    determinant = s.expand(matrix.det())
    C["prompt_cells"] += 9
    name = re.search(r"matrix \$([A-Z])\$ given below", q[":question/problem"])[1]
    claims = re.findall(r"(?m)^- \*\*(I|II|III)\.\*\* (.*)$", q[":question/problem"])
    assert [label for label, _ in claims] == ["I", "II", "III"]
    truths = []
    for _, text in claims:
        equality = re.fullmatch(r"\$det\(([A-Z])\)=(.*?)\$", text)
        if equality:
            assert equality[1] == name
            truths.append(same(scalar(equality[2]), determinant))
        else:
            assert "$" + name + "$" in text and "singular matrix" in text
            truths.append(determinant != 0 if "not" in text else determinant == 0)
        C["statements"] += 1
    fields = {field[":answer-field/key"]: field for field in q[":question/answer-fields"]}
    assert set(fields) == {"I", "II", "III"}
    for (key, _), truth in zip(claims, truths):
        field = fields[key]
        assert field[":answer-field/type"] == ":answer-field.type/checkbox"
        answers = field[":answer-field/choices"]
        assert len(answers) == 2 and {a[":answer/value"] for a in answers} == {"false", "true"}
        correct = next(a[":answer/value"] for a in answers
                       if a[":answer/id"] == field[":answer-field/correct"][1])
        assert (correct == "true") == truth
        C["Boolean_values"] += 2

    solution = q[":question/worked-solution"]
    displayed = arrays(solution)
    assert len(displayed) == 4 and displayed[0][1] == matrix
    C["determinant_cells"] += 9
    minors = [matrix.minor_submatrix(0, j) for j in range(3)]
    coefficients = [matrix[0, 0], -matrix[0, 1], matrix[0, 2]]
    for (_, shown), expected in zip(displayed[1:], minors):
        assert shown == expected
        C["minor_cells"] += 4
    protected = solution
    for index, (match, _) in reversed(list(enumerate(displayed))):
        protected = protected[:match.start()] + f"ZZ{index}ZZ" + protected[match.end():]
    block = re.search(r"\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$", protected, re.S)[1]
    rows = block.split(chr(92) * 2)
    assert len(rows) in (5, 6)
    sides = [row.split("=", 1)[1].strip() for row in rows]
    assert sides[0] == "ZZ0ZZ"
    expression = sides[1]
    symbols = [P.u, P.v, P.k]
    for j, symbol in enumerate(symbols, 1):
        expression = expression.replace(f"ZZ{j}ZZ", str(symbol))
    expression = scalar(expression)
    assert all(same(s.diff(expression, symbol), coefficient)
               for symbol, coefficient in zip(symbols, coefficients))
    assert same(expression, sum(symbol * coefficient
                                for symbol, coefficient in zip(symbols, coefficients)))
    C["separate_cofactor_coefficients"] += 3
    products = [(minor[0, 0] * minor[1, 1], minor[0, 1] * minor[1, 0]) for minor in minors]
    terms = signed_terms(sides[2])
    assert len(terms) == 3
    for term, coefficient, (first, second) in zip(terms, coefficients, products):
        assert same(scalar(term), coefficient * (first - second))
        if coefficient == 0:
            assert scalar(term) == 0
            continue
        groups = parentheses(term)
        assert groups
        operands = signed_terms(groups[-1])
        assert len(operands) == 2
        assert same(scalar(operands[0]), first) and same(scalar(operands[1]), -second)
        C["separate_minor_products"] += 2
    compact = signed_terms(sides[3])
    nonzero = [(coefficient, minor.det(), pair) for coefficient, minor, pair
               in zip(coefficients, minors, products) if coefficient != 0]
    assert len(compact) == len(nonzero)
    for term, (coefficient, value, pair) in zip(compact, nonzero):
        if len(rows) == 5 and coefficient == 1:
            operands = signed_terms(parentheses(term)[-1])
            assert len(operands) == 2
            assert same(scalar(operands[0]), pair[0]) and same(scalar(operands[1]), -pair[1])
        else:
            operands = term.split(r"\cdot")
            assert len(operands) == 2
            assert same(scalar(operands[0]), coefficient) and same(scalar(operands[1]), value)
        C["evaluated_cofactor_operands"] += 2
    for side in sides:
        for j, (_, shown) in enumerate(displayed):
            side = side.replace(f"ZZ{j}ZZ", "(" + s.latex(shown.det()) + ")")
        assert same(scalar(side), determinant)
        C["complete_stage_equalities"] += 1
    stated = re.search(r"Since \$det\(" + name + r"\)=(.*?)\$", solution)[1]
    stated = stated.removesuffix(r"\ne 0")
    assert same(scalar(stated), determinant)
    assert ("**not** singular" in solution) == (determinant != 0)
    ending = solution.split("Therefore,", 1)[1]
    selected = re.findall(r"\b(?:III|II|I)\b", ending)
    assert selected == [label for (label, _), truth in zip(claims, truths) if truth]
    C["conclusions"] += 1
    level = q[":question/difficulty"].split("/")[-1]
    radical_entries = sum(not value.is_Rational for value in matrix)
    if level == "easy":
        assert all(value.is_Integer for value in matrix)
    elif level == "moderate":
        assert radical_entries <= 3
    else:
        assert radical_entries >= 6
    C["workload_checks"] += 1
    C["records"] += 1

if __name__ == "__main__":
    records = json.loads((R / f"qa/{K}-sampled.json").read_text())
    for case in json.loads((D / "source-cases.json").read_text()):
        records.append(G.generate(case["level"], seed=337, template=case["template"],
                                  parameters=case["parameters"], profile=case["bank_profile"]))
    for record in records:
        check(record)
    def prose(text):
        return re.sub(r"\s+", " ", re.sub(r"\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)", "@", text, flags=re.S).replace("*", "")).strip()
    original = {q[":question/math-academy-id"]: q for q in json.loads((D / "source.json").read_text())["record"][":knowledge-point/questions"]}
    fidelity = dict(current_prompts=0, current_solutions=0, current_fields=0, current_values=0, current_keys=0, historical_fields=0, historical_values=0, historical_keys=0, historical_missing_keys=0)
    for case in json.loads((D / "source-cases.json").read_text()):
        generated = G.generate(case["level"], template=case["template"], parameters=case["parameters"], profile=case["bank_profile"])["question"]
        source = original[case["source_id"]]
        assert arrays(source[":question/problem"])[0][1] == arrays(generated[":question/problem"])[0][1]
        assert prose(source[":question/problem"]) == prose(generated[":question/problem"])
        assert prose(source[":question/worked-solution"]) == prose(generated[":question/worked-solution"])
        source_arrays = [matrix for _, matrix in arrays(source[":question/worked-solution"])]
        generated_arrays = [matrix for _, matrix in arrays(generated[":question/worked-solution"])]
        assert source_arrays == generated_arrays
        fidelity["current_prompts"] += 1
        fidelity["current_solutions"] += 1
        actual_fields = {field[":answer-field/key"]: field for field in generated[":question/answer-fields"]}
        for field in source[":question/answer-fields"]:
            actual = actual_fields[field[":answer-field/key"]]
            assert field[":answer-field/type"][":db/ident"] == actual[":answer-field/type"]
            assert sorted(a[":answer/value"] for a in field[":answer-field/choices"]) == sorted(a[":answer/value"] for a in actual[":answer-field/choices"])
            key = next(a[":answer/value"] for a in actual[":answer-field/choices"] if a[":answer/id"] == actual[":answer-field/correct"][1])
            assert key == field[":answer-field/correct"][":answer/value"]
            fidelity["current_fields"] += 1
            fidelity["current_values"] += len(field[":answer-field/choices"])
            fidelity["current_keys"] += 1
    historical = json.loads((D / "reference/source-basis-1356.json").read_text())
    assert historical == json.loads((R / f"sources/{K}.json").read_text())
    for source in historical["record"][":knowledge-point/questions"]:
        replay = G.generate("easy", profile="historical:" + source[":question/math-academy-id"])["question"]
        assert arrays(source[":question/problem"])[0][1] == arrays(replay[":question/problem"])[0][1]
        assert prose(source[":question/problem"]) == prose(replay[":question/problem"])
        assert len(source[":question/answer-fields"]) == len(replay[":question/answer-fields"])
        for old, actual in zip(source[":question/answer-fields"], replay[":question/answer-fields"]):
            assert sorted(a[":answer/value"] for a in old[":answer-field/choices"]) == sorted(a[":answer/value"] for a in actual[":answer-field/choices"])
            assert (":answer-field/correct" in old) == (":answer-field/correct" in actual)
            if ":answer-field/correct" in old:
                key = next(a[":answer/value"] for a in actual[":answer-field/choices"] if a[":answer/id"] == actual[":answer-field/correct"][1])
                assert key == old[":answer-field/correct"][":answer/value"]
                fidelity["historical_keys"] += 1
            else:
                fidelity["historical_missing_keys"] += 1
            fidelity["historical_fields"] += 1
            fidelity["historical_values"] += len(old[":answer-field/choices"])
    probe = copy.deepcopy(next(record for record in records if arrays(record["question"][":question/problem"])[0][1][0, 0] == 0))
    solution = probe["question"][":question/worked-solution"]
    first_minor = arrays(solution)[1][0]
    first_cell = first_minor[2].split("&", 1)[0]
    changed_body = first_minor[2].replace(first_cell, s.latex(scalar(first_cell) + 1), 1)
    changed_matrix = first_minor[0].replace(first_minor[2], changed_body, 1)
    probe["question"][":question/worked-solution"] = solution[:first_minor.start()] + changed_matrix + solution[first_minor.end():]
    saved_counts = C.copy()
    try:
        check(probe)
    except AssertionError:
        pass
    else:
        raise AssertionError("Wrong zero-coefficient minor survived independent readback")
    C.clear(); C.update(saved_counts)
    proof = dict(status="passed", kp_id=K, readback=C, source_fidelity=fidelity, zero_coefficient_wrong_minor_rejected=True,
                 script_sha256=hashlib.sha256(D.with_suffix(".py").read_bytes()).hexdigest())
    (R / f"qa/{K}-root-readback.json").write_text(json.dumps(proof, indent=2) + "\n")
    print(json.dumps(proof))
