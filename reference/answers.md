# Answer Key Schema Recommendations

The current lesson JSON does not capture correct answers. To support a later
answer-provision stage, add a canonical `answer_key` object to each question and
use `status: "MA_ANSWER_MISSING"` as the parse-friendly marker for unanswered
questions.

## Type Mapping

| `DATA/Lesson-Data/Questions.csv` type | Cardinality | Quiz Blocks type | Answer shape |
| --- | --- | --- | --- |
| `multiple-choice` | `single` | `radio` | one correct choice |
| `select-list` | `single` or `multi` | `select` | one correct option per select blank |
| `free-response` | `single` or `multi` | `free` or `blank` | reference answer or blank answers |

## Missing Answer Marker

Use a real JSON field instead of a comment:

```json
"answer_key": {
  "status": "MA_ANSWER_MISSING",
  "quiz_type": "radio",
  "answer_cardinality": "single"
}
```

This makes missing answers easy to locate:

```bash
rg '"status": "MA_ANSWER_MISSING"' DATA/Lessons
```

## Multiple Choice

For `multiple-choice` questions, add a top-level answer key and nullable
correctness fields on each choice.

```json
"answer_key": {
  "status": "MA_ANSWER_MISSING",
  "quiz_type": "radio",
  "answer_cardinality": "single",
  "correct_choice": null
},
"choices": [
  {
    "choice_index": 1,
    "label": "a",
    "correct": null
  }
]
```

Later, the answer stage can set either or both:

```json
"correct_choice": "a"
```

```json
"correct": true
```

## Select List

For `select-list` questions, each select blank needs its own correct option.
Add stable option ids so later stages can set `correct_option_id` without
depending on rendered option text.

```json
"answer_key": {
  "status": "MA_ANSWER_MISSING",
  "quiz_type": "select",
  "answer_cardinality": "multi",
  "select_answers": [
    {
      "select_index": 1,
      "correct_option_id": null
    }
  ]
}
```

Each option should also carry a stable id and nullable correctness field:

```json
{
  "index": 3,
  "option_id": "select-1-option-3",
  "correct": null
}
```

## Free Response

For open free-response questions, use `free` and store an optional reference
answer.

```json
"answer_key": {
  "status": "MA_ANSWER_MISSING",
  "quiz_type": "free",
  "answer_cardinality": "single",
  "correct": null
}
```

## Fill In The Blank

For fill-in-the-blank style questions, use `blank` with non-exact grading. This
avoids requiring exact LaTeX or building a math-equivalence parser too early.

```json
"answer_key": {
  "status": "MA_ANSWER_MISSING",
  "quiz_type": "blank",
  "answer_cardinality": "multi",
  "require_exact": false,
  "blank_answers": [
    {
      "blank_index": 1,
      "dom_id": "freeResponseTextbox-1",
      "correct": null
    }
  ]
}
```

## Renderer Consumption

`md.py` should prefer filled answer fields in this order:

- `choices[].correct` for `radio` and `checkbox`
- `select_lists[].options[].correct` or `answer_key.select_answers[]` for `select`
- `answer_key.correct` for `free`
- `answer_key.blank_answers[]` for `blank`

The `answer_key` object should be treated as the canonical schema. Nullable
`correct` fields on choices and options are convenience fields for rendering.
