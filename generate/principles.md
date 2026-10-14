# Question Generation Principles

1. **Establish fidelity first.** Faithfully reproduce the source questions before extending them.
2. **Provide sufficient variety.** Extend faithful templates when they cannot produce a sufficiently varied question bank.
3. **Stay within scope.** Every variation must preserve the knowledge point’s intended skill and difficulty level.

## 1. Establish fidelity first

Reproduce the observed prompts, answer-field types, complete answer banks, and worked-solution templates at the original parameters. Preserve the shared wording, mathematical structure, and solution steps; mathematical correctness alone does not establish fidelity. Verify source replication before introducing extensions, and document source errors so they are not copied into generated questions.

## 2. Provide sufficient variety

Faithful replication is the starting requirement. Assess whether the recovered templates can produce enough meaningfully different questions for repeated practice. When source coverage is too narrow, add variations grounded in the same mathematical method and instructional purpose. Distinguish authored extensions from observed templates, and validate their answers, distractors, and worked solutions with the same care.

Use a stable mathematical and instructional backbone with explicitly defined variable slots. Preserve the method, expression structure, answer-field contract, and ordered worked-solution stages. Sample values or eligible targets within those slots, then derive every dependent part from the same instance. An example's particular target or position is not automatically a template constraint; keep it fixed when its role is essential to the assessed method. Define the permitted variations before implementation, and do not invent new operators, response formats, or reasoning steps merely to increase variety. When the evidence is sparse, use conservative same-method variations and record their limits.

## 3. Stay within scope

Check proposed variations against the lesson context, prerequisites, and the reasoning required at the intended difficulty. Vary the application while keeping the assessed skill and workload comparable; do not introduce other topics, additional skills, or branches that expand the knowledge point’s scope. Variations within one difficulty level have no instructional progression. Each question should stand on its own as another instance of the same skill at the same level.

## Math content format

All generated content must follow [the shared UI math convention](../docs/math-content.md).
Use `scripts/question_capture/math_format.py` to format matrices and systems,
normalize prose and bare math answers before computing IDs, and validate the public
generator output. Keep coefficient and augmented matrix roles explicit. Source
replication checks should compare mathematical content separately from normalized
presentation; malformed captured TeX must not be reproduced in served content.
