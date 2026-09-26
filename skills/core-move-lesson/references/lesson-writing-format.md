# Lesson Writing Format

Use this shape for final Markdown lesson files.

```markdown
# Lesson Title

## Table of Contents

- [Introduction](#introduction)
- [First Skill Section](#first-skill-section)
- [Second Skill Section](#second-skill-section)
- [Common Trap Or Variant](#common-trap-or-variant)

## Prerequisites

- ...

---

<a id="introduction"></a>
## Introduction

Name the problem context, the recognition cue, and the core move.

---

<a id="first-skill-section"></a>
## First Skill Section

**Example:** ...

**Explanation**

...

```quiz
type: radio
id: q-1
content: |-
  ...
options:
- id: a
  content: |-
    ...
  feedback: |-
    Diagnose the specific misconception represented by this option, then contrast it with the rule that controls the answer.
- id: b
  content: |-
    ...
  correct: true
  feedback: |-
    State the governing rule in natural language, apply it to the prompt, and finish with the requested conclusion.
```

---

## Summary

Compress the cue, rule, procedure, and main trap.
```

## Style Rules

- Keep paragraphs short.
- Put display equations in `$$...$$`.
- Wrap inline math in `$...$`.
- Do not mention "Math Academy", "active learning", "core move", or pipeline mechanics inside the student-facing lesson unless the user asks for meta commentary.
- Prefer concrete section titles over generic labels like "Step 1".
- Use `**Example:**`, then `**Explanation**`, then a quiz block.
- Do not use raw checklist multiple choice in final output.
- Follow `$quiz-block-factory` for quiz structure and feedback placement. Every
  generated radio or checkbox option needs substantive, response-specific feedback.

## Quiz Placement

Each example section should have one quiz block with 1-2 closely matched questions when possible. If a section is purely introductory, it may have no quiz block, but later sections must include practice.
