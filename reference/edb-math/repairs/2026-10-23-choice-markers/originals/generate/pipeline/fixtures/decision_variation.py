"""Synthetic distribution controls for review tests; never publish these questions.

The broken controls are mathematically correct. Their incidental labels predict
responses. The identity control deliberately has a fixed answer: its stated
teaching objective is recognizing that identity, not general determinant skill.
"""
import random
import uuid


def matrix_tex(values):
    return r"\begin{pmatrix}" + r"\\".join("&".join(map(str, row)) for row in values) + r"\end{pmatrix}"


def record(prompt, choices, correct, solution, seed):
    def ident(value):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, "decision-variation-control:" + value))

    qid = ident(prompt)
    answers = [{":answer/id": ident(qid + value), ":answer/type": ":answer.type/math",
                ":answer/value": value} for value in choices]
    random.Random(seed).shuffle(answers)
    field = {":answer-field/id": ident(qid + ":field"), ":answer-field/key": "selection",
             ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": answers,
             ":answer-field/correct": [":answer/id", ident(qid + correct)]}
    return {"question": {":question/id": qid, ":question/difficulty": ":question.difficulty/easy",
                         ":question/problem": prompt, ":question/worked-solution": solution,
                         ":question/answer-fields": [field]}}


def distributivity(seed=0, *, repaired=False, matrices=None, survivor=None):
    rng = random.Random(seed)
    if matrices is None:
        # Separate ranges keep all displayed answer matrices distinct.
        matrices = {label: [[rng.randint(1, 9) + 20 * i for _ in range(2)] for _ in range(2)]
                    for i, label in enumerate("ABC")}
    survivor = survivor or ("ABC"[seed % 3] if repaired else "A")
    other = "B" if survivor == "A" else "A"
    left, right = sorted((survivor, other))
    if repaired and (seed // 3) % 2:
        left, right = right, left
    scale = 2 + (seed // 6) % 3 if repaired else 2
    subtract_left = scale - (left == survivor)
    subtract_right = scale - (right == survivor)
    expression = f"{scale}({left}+{right})-{subtract_left}{left}-{subtract_right}{right}"
    definitions = ", ".join(f"${label}={matrix_tex(value)}$" for label, value in matrices.items())
    prompt = f"Given {definitions}, evaluate ${expression}$. {{{{selection}}}}"
    choices = [f"{label}={matrix_tex(value)}" for label, value in matrices.items()]
    correct = f"{survivor}={matrix_tex(matrices[survivor])}"
    solution = (f"Distribute and collect terms: ${expression}="
                f"({scale}-{subtract_left}){left}+({scale}-{subtract_right}){right}={correct}$.")
    return record(prompt, choices, correct, solution, seed)


SUBSETS = ("F", "H", "M", "FH", "FM", "HM")


def classification(seed=0, *, repaired=False, matrices=None, collection=None):
    rng = random.Random(seed)
    collection = collection or ("I" if seed % 2 == 0 else "II")
    if matrices is None:
        qualifying = SUBSETS[(seed // 2) % len(SUBSETS)] if repaired else ("HM" if collection == "I" else "F")
        matrices = {}
        for label in "FHM":
            value = [[rng.randint(-9, 9), 0], [0, rng.randint(-9, 9)]]
            if label not in qualifying:
                row, col = ((0, 1), (1, 0))[rng.randrange(2)]
                value[row][col] = rng.choice((-7, -3, 2, 8))
            matrices[label] = value
    qualifying = "".join(label for label in sorted(matrices)
                         if matrices[label][0][1] == matrices[label][1][0] == 0)
    subset = lambda labels: r"\{" + ",".join(labels) + r"\}"
    definitions = ", ".join(f"${label}={matrix_tex(value)}$" for label, value in matrices.items())
    prompt = (f"Collection {collection}. Given {definitions}, which set contains exactly the diagonal "
              "matrices? {{selection}}")
    details = " ".join(f"{label}: off-diagonal entries are {value[0][1]} and {value[1][0]}."
                       for label, value in matrices.items())
    solution = f"A matrix is diagonal exactly when both off-diagonal entries vanish. {details} Select ${subset(qualifying)}$."
    return record(prompt, [subset(labels) for labels in ("", *SUBSETS, "FHM")], subset(qualifying), solution, seed)


def equal_row_identity(seed=0):
    """A narrow identity exercise, not a sample of general determinant problems."""
    rng = random.Random(seed)
    a, b = rng.randint(1, 20), rng.randint(1, 20)
    prompt = ("Use the equal-row determinant identity to evaluate "
              f"$\\det({matrix_tex([[a, b], [a, b]])})$. {{{{selection}}}}")
    solution = f"The rows are equal, so the determinant is zero: {a}*{b}-{b}*{a}=0."
    return record(prompt, ["0", "1", "-1"], "0", solution, seed)
