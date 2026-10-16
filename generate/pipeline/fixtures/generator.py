"""Synthetic matrix-entry review control; never publish to a real database."""
import argparse
import json
from pathlib import Path
import random
import uuid

CONFIG = json.loads(Path(__file__).with_name("behavior.json").read_text())


def ident(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "course-academy-review-control:" + text))


def generate(seed=0, parameters=None):
    rng = random.Random(seed)
    matrix = parameters["matrix"] if parameters is not None else [[rng.randint(-9, 9) for _ in range(2)] for _ in range(2)]
    if parameters is not None:
        row, column = parameters["row"], parameters["column"]
        operation = "entry"
    elif CONFIG["sampling"] == "fixed_entry":
        row, column, operation = 0, 0, "entry"
    elif CONFIG["sampling"] == "diagonal_sum":
        row, column, operation = 0, 0, "sum"
    else:
        row, column, operation = rng.randrange(2), rng.randrange(2), "entry"
    tex = r"\begin{pmatrix}" + str(matrix[0][0]) + "&" + str(matrix[0][1]) + r"\\" + str(matrix[1][0]) + "&" + str(matrix[1][1]) + r"\end{pmatrix}"
    if operation == "sum":
        value = matrix[0][0] + matrix[1][1]
        target = "a_{11}+a_{22}"
        solution = f"The diagonal entries are ${matrix[0][0]}$ and ${matrix[1][1]}$. Adding them gives ${target}={value}$."
    else:
        value = matrix[row][column]
        target = "a_{" + str(row + 1) + str(column + 1) + "}"
        solution = f"The first index is {row + 1}, so use row {row + 1}. The second index is {column + 1}, so use column {column + 1} of that row. Thus ${target}={value}$."
    prompt = f"For $A={tex}$, find ${target}$. {{{{answer}}}}"
    qid = ident(prompt)
    aid = ident(qid + ":" + str(value))
    answer = {":answer/id": aid, ":answer/type": ":answer.type/math", ":answer/value": str(value)}
    field = {":answer-field/id": ident(qid + ":field"), ":answer-field/key": "answer",
             ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [answer],
             ":answer-field/correct": [":answer/id", aid]}
    return {
        "knowledge_point": {"db_id": 1, "id": ident("kp"), "title": "Synthetic matrix-entry review control"},
        "question": {":question/id": qid, ":question/difficulty": ":question.difficulty/easy",
                     ":question/problem": prompt, ":question/worked-solution": solution,
                     ":question/answer-fields": [field]},
        "generation": {"seed": seed, "parameters": {"matrix": matrix, "row": row, "column": column},
                       "operation": operation, "synthetic_review_control": True},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--difficulty", choices=["easy"], default="easy")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--format", choices=["json"], default="json")
    args = parser.parse_args()
    print(json.dumps([generate(args.seed + index) for index in range(args.count)]))


if __name__ == "__main__":
    main()
