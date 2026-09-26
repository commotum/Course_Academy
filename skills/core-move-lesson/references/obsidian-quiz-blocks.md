# Quiz-Block Guidance Moved

Quiz-block schemas, supported types, canonical field names, feedback placement, and
validation now belong to `$quiz-block-factory`:

- `/Users/jake/Developer/study/util/skills/quiz-block-factory/SKILL.md`
- `/Users/jake/Developer/study/util/skills/quiz-block-factory/references/quiz-block-schema.md`
- `/Users/jake/Developer/study/util/skills/quiz-block-factory/references/feedback-standard.md`

Invoke that skill before creating or changing quiz blocks. Core-move lessons should
still default to `radio` for ordinary multiple-choice practice, but they must use the
factory's canonical structure, substantive corrective feedback, and validator. Do not
duplicate schema guidance in this reference; that would allow the two skills to drift.
