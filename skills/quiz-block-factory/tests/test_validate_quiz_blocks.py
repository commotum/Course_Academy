#!/usr/bin/env python3
"""Regression tests for the quiz-block-factory validator."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_quiz_blocks import (  # noqa: E402
    COMMON_ROOT_FIELDS,
    MULTI_QUESTION_FIELDS,
    OPTION_FIELDS,
    QUESTION_FIELDS,
    TYPE_ROOT_FIELDS,
    Issue,
    validate_file,
)


class QuizBlockFieldTests(unittest.TestCase):
    def validate_issues(
        self,
        markdown: str,
        *,
        strict_ids: bool = False,
        require_radio_shuffle: bool = False,
        require_feedback: bool = False,
        lint_feedback: bool = False,
    ) -> list[Issue]:
        args = SimpleNamespace(
            allow_no_quiz=False,
            allow_raw_mcq=False,
            require_radio_practice=False,
            require_radio_shuffle=require_radio_shuffle,
            strict_ids=strict_ids,
            require_feedback=require_feedback,
            lint_feedback=lint_feedback,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lesson.md"
            path.write_text(markdown, encoding="utf-8")
            issues, _ = validate_file(path, args)
        return issues

    def validate(self, markdown: str) -> list[str]:
        return [issue.message for issue in self.validate_issues(markdown)]

    def test_radio_rejects_root_feedback(self) -> None:
        issues = self.validate(
            """```quiz
type: radio
content: Question?
options:
- content: A
  correct: true
- content: B
feedback: This belongs on an option.
```
"""
        )
        self.assertIn("unknown top-level field for radio quiz: feedback", issues)

    def test_radio_accepts_option_feedback(self) -> None:
        issues = self.validate(
            """```quiz
type: radio
content: Question?
options:
- content: A
  correct: true
  feedback: Correct.
- content: B
  feedback: Try again.
```
"""
        )
        self.assertEqual([], issues)

    def test_radio_accepts_common_root_fields(self) -> None:
        issues = self.validate(
            """```quiz
type: radio
id: q-1
content: Question?
gated: true
shuffle: true
options:
- content: A
  correct: true
- content: B
```
"""
        )
        self.assertEqual([], issues)

    def test_require_radio_shuffle_rejects_missing_or_false(self) -> None:
        for shuffle_line in ("", "shuffle: false\n"):
            with self.subTest(shuffle_line=shuffle_line):
                issues = self.validate_issues(
                    f"""```quiz
type: radio
content: Question?
{shuffle_line}options:
- content: A
  correct: true
- content: B
```
""",
                    require_radio_shuffle=True,
                )
                self.assertIn("radio quiz must set shuffle: true", [issue.message for issue in issues])

    def test_require_radio_shuffle_accepts_true(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
content: Question?
shuffle: true
options:
- content: A
  correct: true
- content: B
```
""",
            require_radio_shuffle=True,
        )
        self.assertEqual([], issues)

    def test_quoted_root_feedback_is_still_rejected(self) -> None:
        markdown = """```quiz
type: radio
content: Question?
options:
- content: A
  correct: true
- content: B
"feedback": This belongs on an option.
```
"""
        issues = self.validate_issues(markdown)
        feedback_issue = next(issue for issue in issues if "feedback" in issue.message)
        self.assertEqual("unknown top-level field for radio quiz: feedback", feedback_issue.message)
        self.assertEqual(8, feedback_issue.line)

    def test_quoted_canonical_keys_are_parsed_as_the_same_fields(self) -> None:
        issues = self.validate_issues(
            """```quiz
"type": radio
"id": q-quoted
"content": Question?
"options":
- "id": a
  "content": A
  "correct": true
- "id": b
  "content": B
```
""",
            strict_ids=True,
        )
        self.assertEqual([], issues)

    def test_blank_accepts_root_feedback(self) -> None:
        issues = self.validate(
            """```quiz
type: blank
content: The answer is ==42==.
feedback: Check the arithmetic.
require_exact: false
```
"""
        )
        self.assertEqual([], issues)

    def test_blank_accepts_math_input_mode(self) -> None:
        issues = self.validate(
            """```quiz
type: blank
id: q-math
input_mode: math
require_exact: true
content: Rewrite the expression: ==(x+3)^2-2==
feedback: Complete the square before combining the outside constant.
```
"""
        )
        self.assertEqual([], issues)

    def test_blank_rejects_unknown_input_mode(self) -> None:
        issues = self.validate(
            """```quiz
type: blank
content: The answer is ==42==.
input_mode: latex
```
"""
        )
        self.assertIn("input_mode must be text or math", issues)

    def test_blank_accepts_two_display_math_gaps_on_one_row(self) -> None:
        issues = self.validate(
            r"""```quiz
type: blank
input_mode: math
content: |-
  $$
  x=(==a==)^2+==b==
  $$
```
"""
        )
        self.assertEqual([], issues)

    def test_blank_accepts_display_math_gaps_on_separate_rows(self) -> None:
        issues = self.validate(
            r"""```quiz
type: blank
input_mode: math
content: |-
  $$
  \begin{aligned}
  a &= ==1== \\
  b &= ==2==
  \end{aligned}
  $$
```
"""
        )
        self.assertEqual([], issues)

    def test_radio_rejects_blank_only_require_exact(self) -> None:
        issues = self.validate(
            """```quiz
type: radio
content: Question?
require_exact: false
options:
- content: A
  correct: true
- content: B
```
"""
        )
        self.assertIn("unknown top-level field for radio quiz: require_exact", issues)

    def test_free_accepts_root_feedback_and_correct(self) -> None:
        issues = self.validate(
            """```quiz
type: free
content: Explain the result.
correct: A reference answer.
feedback: Compare signs and units.
```
"""
        )
        self.assertEqual([], issues)

    def test_require_feedback_rejects_missing_radio_option_feedback(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
id: q-1
content: Question?
options:
- id: a
  content: A
  correct: true
  feedback: A rule applied to this situation gives A.
- id: b
  content: B
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertIn("option 2 is missing nonempty feedback", [issue.message for issue in issues])

    def test_feedback_lint_rejects_generic_and_duplicate_feedback(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
id: q-1
content: Question?
options:
- id: a
  content: A
  correct: true
  feedback: Correct.
- id: b
  content: B
  feedback: Correct.
```
""",
            lint_feedback=True,
        )
        messages = [issue.message for issue in issues]
        self.assertTrue(any("generic or opaque" in message for message in messages))
        self.assertTrue(any("duplicates feedback" in message for message in messages))

    def test_rejects_unknown_nested_option_field(self) -> None:
        issues = self.validate(
            """```quiz
type: radio
content: Question?
options:
- content: A
  correct: true
  explanation: Not a supported option field.
- content: B
```
"""
        )
        self.assertIn("unknown field for option 1: explanation", issues)

    def test_canonical_checkbox_with_feedback(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: checkbox
id: q-checkbox
content: Select every true statement.
options:
- id: a
  content: A
  correct: true
  feedback: The governing definition makes A true here.
- id: b
  content: B
  feedback: B confuses the limiting case with the present condition.
```
""",
            strict_ids=True,
            require_feedback=True,
            lint_feedback=True,
        )
        self.assertEqual([], issues)

    def test_canonical_select_with_question_feedback(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: select
id: q-select
content: Classify each case.
options:
- id: left
  content: Left
- id: right
  content: Right
questions:
- id: q-select-a
  content: Negative direction
  correct_option: left
  feedback: Negative direction corresponds to left under the stated axis convention.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertEqual([], issues)

    def test_canonical_multi_select_with_local_options(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: multi-select
id: q-multi
content: Choose one answer per row.
questions:
- id: q-multi-a
  content: First row
  options:
  - id: yes
    content: Yes
  - id: no
    content: No
  correct_option: yes
  feedback: The defining condition is satisfied, so this row is yes.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertEqual([], issues)

    def test_canonical_noodle_requires_resolved_bijection(self) -> None:
        valid = self.validate_issues(
            """```quiz
type: noodle
id: q-noodle
content: Match each role.
options:
- id: position
  content: Position
- id: velocity
  content: Velocity
questions:
- id: q-noodle-a
  content: Location relative to equilibrium
  correct_option: position
  feedback: Position records location relative to equilibrium.
- id: q-noodle-b
  content: Direction of motion
  correct_option: velocity
  feedback: Velocity records direction of motion through its sign.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertEqual([], valid)

        invalid = self.validate(
            """```quiz
type: noodle
content: Match each role.
options:
- id: position
  content: Position
- id: velocity
  content: Velocity
questions:
- content: First role
  correct_option: missing
- content: Second role
  correct_option: missing
```
"""
        )
        self.assertTrue(any("does not match an option id" in message for message in invalid))

    def test_free_reference_and_blank_feedback_requirements(self) -> None:
        free_issues = self.validate_issues(
            """```quiz
type: free
id: q-free
content: Explain the physical reason.
correct: A complete response states the rule and applies it to this case.
feedback: Check the sign convention and the variable roles before comparing.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertEqual([], free_issues)

        blank_issues = self.validate_issues(
            """```quiz
type: blank
id: q-blank
content: The requested value is ==42==.
feedback: The governing relation gives $42$ in the requested units.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertEqual([], blank_issues)

        missing_free_feedback = self.validate_issues(
            """```quiz
type: free
id: q-free-missing-feedback
content: Explain the physical reason.
correct: A complete response states the rule and applies it.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertIn(
            "free quiz is missing nonempty feedback",
            [issue.message for issue in missing_free_feedback],
        )

    def test_strict_block_id_does_not_use_an_option_id(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
content: Question?
options:
- id: a
  content: A
  correct: true
- id: b
  content: B
```
""",
            strict_ids=True,
        )
        self.assertIn("quiz block is missing id", [issue.message for issue in issues])

    def test_strict_multi_question_id_does_not_use_a_nested_option_id(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: multi-select
id: q-multi
content: Choose one.
questions:
- content: First row
  options:
  - id: yes
    content: Yes
  - id: no
    content: No
  correct_option: yes
  feedback: The defining condition makes yes the applicable label.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        self.assertIn(
            "multi-select question 1 is missing id",
            [issue.message for issue in issues],
        )

    def test_boolean_fields_must_be_yaml_booleans(self) -> None:
        issues = self.validate(
            """```quiz
type: radio
id: q-bools
content: Question?
gated: yes
shuffle: "true"
options:
- id: a
  content: A
  correct: "true"
- id: b
  content: B
```
"""
        )
        self.assertIn("gated must be true or false", issues)
        self.assertIn("shuffle must be true or false", issues)
        self.assertIn("option 1 correct must be true or false", issues)
        self.assertIn("radio quiz requires exactly one correct: true option", issues)

    def test_blank_require_exact_must_be_a_yaml_boolean(self) -> None:
        issues = self.validate(
            """```quiz
type: blank
id: q-blank
content: Enter ==42==.
require_exact: no
```
"""
        )
        self.assertIn("require_exact must be true or false", issues)

    def test_blank_answer_may_contain_a_single_equals_sign(self) -> None:
        issues = self.validate(
            """```quiz
type: blank
id: q-equation
content: Solve for the variable: ==x=2==.
feedback: Isolate the variable and enter the complete equation.
```
"""
        )
        self.assertEqual([], issues)

    def test_inline_comments_do_not_change_scalar_types_or_ids(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
id: q-comments # stable block id
content: Question?
gated: false # remains a boolean
options:
- id: a # stable option id
  content: "A # literal hash"
  correct: true # remains a boolean
- id: b
  content: B
```
""",
            strict_ids=True,
        )
        self.assertEqual([], issues)

    def test_ids_must_be_yaml_text(self) -> None:
        unquoted = self.validate_issues(
            """```quiz
type: radio
id: 123
content: Question?
options:
- id: true
  content: A
  correct: true
- id: b
  content: B
```
""",
            strict_ids=True,
        )
        messages = [issue.message for issue in unquoted]
        self.assertIn("quiz block id must be nonempty YAML text", messages)
        self.assertIn("option 1 id must be nonempty YAML text", messages)

        quoted = self.validate_issues(
            """```quiz
type: radio
id: "123"
content: Question?
options:
- id: "true"
  content: A
  correct: true
- id: b
  content: B
```
""",
            strict_ids=True,
        )
        self.assertEqual([], quoted)

    def test_select_rejects_feedback_on_ignored_option_level(self) -> None:
        issues = self.validate(
            """```quiz
type: select
id: q-select
content: Classify the case.
options:
- id: left
  content: Left
  feedback: This renderer never displays option-bank feedback.
- id: right
  content: Right
questions:
- id: q-select-a
  content: Negative direction
  correct_option: left
  feedback: Negative direction corresponds to left under this axis convention.
```
"""
        )
        self.assertIn(
            "option 1 feedback is not rendered for this quiz type; move it to the question",
            issues,
        )

    def test_null_or_collection_content_is_not_nonempty_text(self) -> None:
        null_root = self.validate(
            """```quiz
type: free
id: q-null
content: null
```
"""
        )
        self.assertIn("quiz block is missing nonempty content", null_root)

        collection_option = self.validate(
            """```quiz
type: radio
id: q-collection
content: Question?
options:
- id: a
  content: {not: text}
  correct: true
- id: b
  content: B
```
"""
        )
        self.assertIn("option 1 is missing nonempty content", collection_option)

    def test_numeric_and_boolean_content_are_runtime_coercible_scalars(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
id: q-scalars
content: false
options:
- id: a
  content: 2.5
  correct: true
- id: b
  content: false
```
""",
            strict_ids=True,
        )
        self.assertEqual([], issues)

    def test_duplicate_fields_and_nested_issue_lines_are_reported(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
id: q-duplicate
content: Question?
content: Duplicate prompt.
options:
- id: a
  content: A
  correct: true
  explanation: Unsupported.
- id: b
  content: B
```
"""
        )
        duplicate = next(issue for issue in issues if "duplicate top-level" in issue.message)
        unknown = next(issue for issue in issues if "explanation" in issue.message)
        self.assertEqual(5, duplicate.line)
        self.assertEqual(10, unknown.line)

    def test_duplicate_quiz_ids_are_rejected(self) -> None:
        issues = self.validate(
            """```quiz
type: free
id: duplicate
content: First prompt.
```

```quiz
type: free
id: duplicate
content: Second prompt.
```
"""
        )
        self.assertIn("duplicate quiz block id: duplicate", issues)

    def test_empty_content_and_feedback_are_rejected(self) -> None:
        issues = self.validate_issues(
            """```quiz
type: radio
id: q-empty
content: |-

options:
- id: a
  content: A
  correct: true
  feedback: |-

- id: b
  content: B
  feedback: A concrete misconception explanation.
```
""",
            strict_ids=True,
            require_feedback=True,
        )
        messages = [issue.message for issue in issues]
        self.assertIn("quiz block is missing nonempty content", messages)
        self.assertIn("option 1 is missing nonempty feedback", messages)

    def test_json_schema_field_sets_do_not_drift_from_validator(self) -> None:
        schema_path = Path(__file__).resolve().parents[1] / "schemas" / "quiz-block.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        definitions = schema["$defs"]

        self.assertEqual(OPTION_FIELDS, set(definitions["option"]["properties"]))
        self.assertEqual(QUESTION_FIELDS, set(definitions["question"]["properties"]))
        self.assertEqual(MULTI_QUESTION_FIELDS, set(definitions["multiQuestion"]["properties"]))
        self.assertEqual("\\S", definitions["text"]["pattern"])
        names = {
            "radio": "radio",
            "checkbox": "checkbox",
            "select": "select",
            "multi-select": "multiSelect",
            "noodle": "noodle",
            "free": "free",
            "blank": "blank",
        }
        for quiz_type, definition_name in names.items():
            expected = COMMON_ROOT_FIELDS | TYPE_ROOT_FIELDS[quiz_type]
            self.assertEqual(expected, set(definitions[definition_name]["properties"]))

        self.assertEqual(
            {"type": "string", "minLength": 1, "pattern": "\\S"},
            definitions["id"],
        )
        for definition_name in ["option", "question", "multiQuestion", *names.values()]:
            self.assertEqual(
                {"$ref": "#/$defs/id"},
                definitions[definition_name]["properties"]["id"],
            )
        for definition_name in ("question", "multiQuestion"):
            self.assertEqual(
                {"$ref": "#/$defs/id"},
                definitions[definition_name]["properties"]["correct_option"],
            )
        self.assertEqual(1, definitions["radio"]["properties"]["options"]["minContains"])
        self.assertEqual(1, definitions["radio"]["properties"]["options"]["maxContains"])
        self.assertIn("shuffle", definitions["radio"]["required"])
        self.assertEqual({"const": True}, definitions["radio"]["properties"]["shuffle"])
        self.assertEqual(1, definitions["checkbox"]["properties"]["options"]["minContains"])

    def test_core_move_compatibility_wrapper_delegates_to_factory_cli(self) -> None:
        wrapper = (
            Path(__file__).resolve().parents[2]
            / "core-move-lesson"
            / "scripts"
            / "validate_quiz_blocks.py"
        )
        markdown = """```quiz
type: radio
id: q-wrapper
content: Question?
options:
- id: a
  content: A
  correct: true
- id: b
  content: B
```
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lesson.md"
            path.write_text(markdown, encoding="utf-8")
            result = subprocess.run(
                [str(wrapper), str(path), "--strict-ids"],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("quiz block validation passed: 1 block(s) checked", result.stdout)


if __name__ == "__main__":
    unittest.main()
