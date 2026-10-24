# Question Generation Principles

1. **Establish fidelity first.** Faithfully reproduce the source questions before extending them.
2. **Provide meaningful variety.** Vary eligible answer-bearing relationships so repeated success continues to require the intended skill.
3. **Stay within scope.** Every variation must preserve the knowledge point’s intended skill and difficulty level.

## 1. Establish fidelity first

Establish source eligibility before fidelity. Multistep parts belong to their full activity, and retired questions are not standalone generator templates. Generated copies do not inherit the original's structural containment, so trace their source lineage explicitly. Supplying missing prior context does not authorize converting an excluded part into standalone practice. Preserve the original activity and learner history; rebuild practice families from eligible teaching and standalone evidence.

Reproduce the observed prompts, answer-field types, complete answer banks, and worked-solution templates at the original parameters. Preserve the shared wording, mathematical structure, and solution steps; mathematical correctness alone does not establish fidelity. Verify source replication before introducing extensions, and document source errors so they are not copied into generated questions.

## 2. Provide sufficient variety

Faithful replication is the starting requirement. Assess whether the recovered templates can produce enough meaningfully different questions for repeated practice. When source coverage is too narrow, add variations grounded in the same mathematical method and instructional purpose. Distinguish authored extensions from observed templates, and validate their answers, distractors, and worked solutions with the same care.

Define the learner's operation before the random parameters: what must the learner inspect, distinguish, infer, calculate, or construct? Use a stable mathematical and instructional backbone with explicitly defined variable slots. Preserve the method, answer-field contract, prerequisites, and intended workload. Sample values or eligible targets within those slots, then derive every dependent part from the same instance. An example's particular target, qualifying label, surviving term, correct-choice count, or position is not automatically a template constraint. For every fixed feature, give a mathematical or instructional reason; resemblance to the source arrangement is insufficient. Define permitted variations before implementation, and do not invent new operators, response formats, or reasoning steps merely to increase variety. When the evidence is sparse, use conservative same-method variations and record their limits.

Guard against **surface variation with a fixed decision structure**: this is a descriptive name for questions whose values or appearance change while incidental cues still predict the answer or the action producing it. Unique text, hashes, numerical answers, option shuffles, or a large parameter space do not establish meaningful practice. For example, varying all matrix entries still leaves a shortcut if cancellation always means "choose A"; varying matrix shapes still leaves one if H and M always qualify within a recognizable template. Preserve the rule deciding correctness without automatically preserving which source objects satisfy it.

Validate the specification as well as its implementation. Identify eligible answer-bearing roles and decision cases, justify fixed assignments, and measure coverage within recognizable templates and cue groups. Use controlled changes to relevant evidence to verify that prompts, answers, explanations, and actual grading respond together; changing irrelevant evidence should preserve the response when the task implies that it should. Probe simple strategies based on labels, positions, counts, layout, or template identity. Check the distribution surviving rejection, deduplication, difficulty filtering, and inventory selection, since those steps can remove meaningful cases. Report source fidelity, item correctness, grading, and pedagogical variation separately.

Do not force randomness or reject useful simplifications that express the target skill. Finite families, fixed outcomes, and repetition can be justified for a stated instructional purpose; explain their limits instead of treating them as evidence of broader mastery. Coverage is an obligation grounded in the skill, not a universal count or balance quota. A passing audit supports its tested cases and shortcut claims, not the absence of every possible shortcut.

## 3. Stay within scope

Check proposed variations against the lesson context, prerequisites, and the reasoning required at the intended difficulty. Vary the application while keeping the assessed skill and workload comparable; do not introduce other topics, additional skills, or branches that expand the knowledge point’s scope. Variations within one difficulty level have no instructional progression. Each question should stand on its own as another instance of the same skill at the same level.

## Math content format

All generated content must follow [the shared UI math convention](../docs/math-content.md).
Use `scripts/question_capture/math_format.py` to format matrices and systems,
normalize prose and bare math answers before computing IDs, and validate the public
generator output. Keep coefficient and augmented matrix roles explicit. Source
replication checks should compare mathematical content separately from normalized
presentation; malformed captured TeX must not be reproduced in served content.
