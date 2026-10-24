# 4. Template Extraction

Use the question families identified by [Classify](3-classify.md), analyzing each difficulty and answer-field combination separately.

Use the filtered instructional capture and its current source-eligibility ledger.
Archived multistep parts and retired questions cannot supply a standalone family.
Do not reconstruct their omitted prior context during template extraction. An
independent extension needs explicit support from eligible examples or teaching;
record that support instead of citing the entire captured question pool.

1. Describe each source question specifically: number forms and properties, expression structures, functions and operators, relations, variable roles, constraints, notation, Markdown layout, answer fields, choices, and solution sequence; do not generalize yet.
2. Write one brief generalized description of the family's shared mathematical pattern, required response, and instructional purpose. State the learner's required operation before choosing random parameters.
3. List each question's components, mapping every original choice to its source field, parameters, exact value, recipe, and choice-bank profile alongside the prompt and solution components.
4. Extract one reusable prompt/solution template with a stable backbone and explicitly defined variable slots, identifying fixed, variable, optional, and conditional components, parameter constraints, and the calculations needed to keep every component consistent.

Define the backbone before choosing variation: the assessed method, expression structure, supplied information, roles of the requested objects, answer-field contract, and ordered solution stages. For each variable slot, record its role, allowed values or targets, constraints, and dependent prompt, answer, solution, and plot components. Slots can select eligible cells, edges, points, or terms as well as numerical values. Give a mathematical or instructional reason for structural components kept fixed; repetition in sparse examples alone does not establish a constraint.

Separately identify answer-bearing roles: which object qualifies, which term survives, where decisive evidence appears, which rule case applies, and what response is correct. Distinguish the rule governing a role from its assignment in the source example. Record which assignments can change within scope, which must remain fixed and why, and the decision cases that normal sampling must exercise. Do not freeze a correct-label set, answer position, or recognizable template-to-answer mapping merely because source replay requires that assignment at the original parameters. The independent reviewer must be able to challenge these declared constraints.

Keep variation inside that definition. A changed target must preserve its role and comparable workload, and every reference to it must change together. Do not introduce new operations, question forms, or solution stages to make examples look different. Preserve a specific target when changing it would alter the method. Document conservative same-method generalizations separately from observed source parameters, retaining the original parameters for replay.

For example, a route-matrix sum can keep three unknowns, the expression `a+b+c`, ordinary headings, and three route-count explanations as its backbone. A template with one loop query and two other directed queries can vary their eligible cells and letter assignments while retaining that mix. A fixed B→B target is an example value of the loop slot. Changing the sum to a product, adding multistep journeys, or varying the number of unknowns is outside this template's slots.

Use broad feature categories that cover different mathematical topics. Record properties such as sign, exactness, or perfect-power structure when they affect the method or difficulty. Preserve nested structure and operator inputs; naming an operation alone does not describe its template.

Record domains and branch restrictions alongside the expressions. Flag source errors and retain the original evidence with the supported correction so the generator does not reproduce incorrect mathematics.

Record prerequisite support for each reasoning step and the final displayed answer form, including the exact fragment required by a blank. Identify operator inputs whose structure must remain visible. A CAS rewrite that changes how the learner recognizes the answer is an additional reasoning step: it needs in-scope support and an explicit solution transition. Source fidelity measured only up to algebraic equivalence can hide this defect.

Preserve the source's step-by-step wording and operative stages as a parameterized solution template. Each sampled question has one concrete worked solution, independent of the learner's chosen answer. Its values, target names, directions, and conditional grammar come from that instance; “fixed solution” does not mean reusing the source's literal targets. Separate observed choice patterns from inferred distractor recipes. For blanks, preserve the supplied notation and the exact expression or equation fragment expected; do not add distractors or feedback absent from the source.

Account for every incorrect choice before merging recipes. Record each transformation as a parameterized expression or operation sequence, including compound mistakes and altered constants; a label such as “wrong scale” is insufficient. Recipes can depend on prompt parameters and intermediate calculations as well as the correct answer. If the underlying mistake is unclear, retain the observed expression pattern and mark its interpretation unresolved instead of replacing it with a plausible alternative.

For each source choice, record whether its recipe reproduces the complete mathematical value at the original parameters. Group recipes into the complete banks observed together, preserving any conditions on their use. Retain distinct profiles when one template has different banks, and flag unmapped choices before generator implementation. Record observed parameter values and features separately from proposed sampling bounds so source values such as negative shifts are not accidentally excluded.

Retain representative source IDs and unresolved differences with each template. If plots occur in the prompt, answers, or solution, call [Plot Extraction](5-plot-extraction.md) and attach its plot specification. Then continue with [Template Generator](6-template-generator.md); templates without plots go there directly.
