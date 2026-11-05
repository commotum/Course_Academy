# 4. Template Extraction

Use the question families identified by [Classify](3-classify.md), analyzing each difficulty and answer-field combination separately.

1. Describe each source question specifically: number forms and properties, expression structures, functions and operators, relations, variable roles, constraints, notation, Markdown layout, answer fields, choices, and solution sequence; do not generalize yet.
2. Write one brief generalized description of the family's shared mathematical pattern, required response, and instructional purpose.
3. List each question's components, mapping every original choice to its source field, parameters, exact value, recipe, and choice-bank profile alongside the prompt and solution components.
4. Extract one reusable Markdown/value template, identifying fixed, variable, optional, and conditional components, parameter constraints, and the calculations needed to keep every component consistent.

Use broad feature categories that cover different mathematical topics. Record properties such as sign, exactness, or perfect-power structure when they affect the method or difficulty. Preserve nested structure and operator inputs; naming an operation alone does not describe its template.

Record domains and branch restrictions alongside the expressions. Flag source errors and retain the original evidence with the supported correction so the generator does not reproduce incorrect mathematics.

Keep the original step-by-step wording and one fixed worked solution per question. Separate observed choice patterns from inferred distractor recipes. For blanks, preserve the supplied notation and the exact expression or equation fragment expected; do not add distractors or feedback absent from the source.

Account for every incorrect choice before merging recipes. Record each transformation as a parameterized expression or operation sequence, including compound mistakes and altered constants; a label such as “wrong scale” is insufficient. Recipes can depend on prompt parameters and intermediate calculations as well as the correct answer. If the underlying mistake is unclear, retain the observed expression pattern and mark its interpretation unresolved instead of replacing it with a plausible alternative.

For each source choice, record whether its recipe reproduces the complete mathematical value at the original parameters. Group recipes into the complete banks observed together, preserving any conditions on their use. Retain distinct profiles when one template has different banks, and flag unmapped choices before generator implementation. Record observed parameter values and features separately from proposed sampling bounds so source values such as negative shifts are not accidentally excluded.

Retain representative source IDs and unresolved differences with each template. If plots occur in the prompt, answers, or solution, call [Plot Extraction](5-plot-extraction.md) and attach its plot specification. Then continue with [Template Generator](6-template-generator.md); templates without plots go there directly.
