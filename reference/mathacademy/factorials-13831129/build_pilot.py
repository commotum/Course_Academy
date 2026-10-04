#!/usr/bin/env python3
"""Build this nine-question content pilot; no learner or activity writes."""
import json
import math
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXISTING = {"q-73002", "q-5371"}
KPS = {
    "Evaluating Factorials": "bc445253-146a-5448-9bf3-d5b6c0d4c1f0",
    "Evaluating the Factorial of Zero": "8d084334-b89a-5a33-9373-086018cdfbc3",
    "Evaluating a Quotient of Factorials": "203386bf-cdf1-5a78-92fd-36fababfb971",
}
# Newly authored options; these are not claimed to be recovered MA choices.
DISTRACTORS = {
    "q-122027": ["3628800", "3991680", "479001600", "11"],
    "q-122033": ["72", "30", "12", "5040"],
    "q-73003": ["4", "12", "16", "120"],
    "q-73005": ["8", "5040", "322560", "56"],
    "q-124403": ["24", "1", "120", "5"],
    "q-124400": ["0", "5041", "7", "40320"],
    "q-73014": ["110", "7920", "39916800"],
}
EXPECTED = {
    "q-73002": math.factorial(2) * math.factorial(3),
    "q-122027": math.factorial(11),
    "q-122033": math.factorial(3) * math.factorial(4),
    "q-73003": math.factorial(4),
    "q-73005": math.factorial(8),
    "q-124403": math.factorial(4) + math.factorial(0),
    "q-124400": math.factorial(0) * math.factorial(7),
    "q-5371": math.factorial(6) // math.factorial(3),
    "q-73014": math.factorial(11) // math.factorial(8),
}


def quote(value):
    return json.dumps(value, ensure_ascii=False)


def identity(kind, source):
    return uuid.uuid5(uuid.NAMESPACE_URL, f"course-academy:ma:{kind}:{source}")


def edn_uuid(value):
    return f'#uuid "{value}"'


def build():
    data = json.loads((ROOT / "content.json").read_text())
    forms, review = [], []
    for q in data["questions"]:
        key, numeric = q["math_academy_id"], q["math_academy_id"][2:]
        correct = q["correct_answer_from_solution"]
        assert correct == str(EXPECTED[key])
        assert q["knowledge_point"] in KPS
        assert "Your Answer" not in q["worked_solution"]
        # Preserve existing problem statements, fields, correct refs and choices.
        if key in EXISTING:
            forms.append(
                '{:db/id [:question/math-academy-id ' + quote(key) + '] '
                ':question/difficulty :question.difficulty/' + q["difficulty"] + ' '
                ':question/worked-solution ' + quote(q["worked_solution"]) + ' '
                ':db/ensure [:question/validate]}'
            )
            choices = q["source_choices"]
            assert correct in choices
            if q["observed_answer_value"]:
                assert q["observed_answer_value"] in choices
        else:
            choices = [correct, *DISTRACTORS[key]]
            assert len(choices) == len(set(choices)) == (4 if key == "q-73014" else 5)
            if q["observed_answer_value"]:
                assert q["observed_answer_value"] in choices
            answers = []
            for i, value in enumerate(choices):
                answers.append(
                    '{:db/id ' + quote(f"{key}-value-{i}") + ' '
                    ':answer/id ' + edn_uuid(identity("answer", f"{numeric}:1:pilot:{value}")) + ' '
                    ':answer/type :answer.type/math :answer/value ' + quote(value) + ' '
                    ':db/ensure [:answer/validate]}'
                )
            field = (
                '{:answer-field/id ' + edn_uuid(identity("field", f"{numeric}:1")) + ' '
                ':answer-field/key "selection" :answer-field/type :answer-field.type/radio '
                ':answer-field/choices [' + ' '.join(answers) + '] '
                ':answer-field/correct ' + quote(f"{key}-value-0") + ' '
                ':db/ensure [:answer-field/validate]}'
            )
            problem = q["problem"].replace('}.$', '}$.' )
            forms.append(
                '{:db/id ' + quote(key) + ' '
                ':question/id ' + edn_uuid(identity("question", numeric)) + ' '
                ':question/math-academy-id ' + quote(key) + ' '
                ':question/problem ' + quote(problem) + ' '
                ':question/difficulty :question.difficulty/' + q["difficulty"] + ' '
                ':question/worked-solution ' + quote(q["worked_solution"]) + ' '
                ':question/answer-fields [' + field + '] :db/ensure [:question/validate]}'
            )
            forms.append(
                '{:db/id [:knowledge-point/id ' + edn_uuid(KPS[q["knowledge_point"]]) + '] '
                ':knowledge-point/questions [' + quote(key) + '] '
                ':db/ensure [:knowledge-point/validate]}'
            )
        review.append({
            "math_academy_id": key,
            "operation": "enrich existing" if key in EXISTING else "create and link",
            "knowledge_point": q["knowledge_point"],
            "difficulty": q["difficulty"],
            "field_type": "radio",
            "field_type_basis": "existing exact-ID field" if key in EXISTING else "inferred from existing questions in the same KP; user directed",
            "correct_answer": correct,
            "choices": choices,
            "choices_basis": "original MA capture; unchanged" if key in EXISTING else "authored distractors; 72 also observed for q-122033",
        })
    payload = '[\n' + '\n'.join(forms) + '\n]\n'
    assert not any(':' + p + '/' in payload for p in (
        'learner', 'learner-task', 'task-item', 'progress', 'performance', 'policy',
        'activity', 'step', 'tutorial', 'topic',
    ))
    (ROOT / "transaction.edn").write_text(payload)
    (ROOT / "review.json").write_text(json.dumps(review, indent=2) + '\n')
    lines = [
        '# Factorials question pilot', '',
        '[Source lesson results](https://mathacademy.com/learn?taskId=13831129).', '',
        'Two existing questions receive missing difficulty and worked solutions. '
        'Seven new questions receive problems, difficulty, worked solutions, one radio field each, '
        'and links to the existing Factorials KPs. The original source capture contains six '
        'multiple-choice questions across these three KPs; the user directed matching those types.', '',
        'New distractors below are authored, except 72 was also observed on the result page. '
        'Correct answers were extracted from the solutions and checked by evaluating the factorial expressions. '
        'No learner, task-item, activity, progress, or engine policy facts are written. '
        'Canonical examples and existing question options are preserved. The authored 11/8 distractor was removed at the user’s request; q-73014 has four choices.', '',
        '| Question | Operation | KP | Difficulty | Correct | Other choices |',
        '|---|---|---|---|---|---|',
    ]
    for q in review:
        other = ', '.join(v for v in q['choices'] if v != q['correct_answer'])
        lines.append(f"| {q['math_academy_id']} | {q['operation']} | {q['knowledge_point']} | {q['difficulty']} | {q['correct_answer']} | {other} |")
    lines.extend(['', '## Captured worked solutions', ''])
    for q in data['questions']:
        lines.extend(['### ' + q['math_academy_id'], '', q['problem'], '', q['worked_solution'], ''])
    (ROOT / "review.md").write_text('\n'.join(lines))
    print(f"Prepared {len(review)} questions: 2 enrichments, 7 additions, 7 KP links.")


if __name__ == '__main__':
    build()
