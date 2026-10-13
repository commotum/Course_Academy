# 3. Classify

When [Inventory](2-inventory.md) finds a shortage and no generator exists for the knowledge point:

- Read all its source practice questions at one database basis, including difficulty, Markdown, answer fields, choices, correct values, worked solutions, and plot references.
- Identify the answer-field types used at each difficulty level, preserving questions with multiple fields or mixed types.
- Group questions into distinct Markdown/value templates within each difficulty level.
- Within each template, identify distinct source choice-bank patterns rather than assuming every question uses the same distractor recipes.
- Determine whether each template requires new plots when its parameters change, rather than merely containing existing plots.
- Classify each template's plot requirements as **none**, **light**, **moderate**, or **heavy**.
- Record each difficulty's field types, template count, and each template's plot rating, with representative source question IDs.

Treat changed numbers as variants of one template. Keep different prompt structures, worked-solution sequences, answer shapes, and field layouts separate; a blank expecting an equation's left-hand side differs from one expecting its right-hand side.

A shared prompt and worked solution can have several choice-bank profiles. Track those profiles separately from the Markdown/value template count, with every source question assigned to a profile; blanks have no distractor profile.

Plots include mathematical graphs and diagrams. **None** means no new plots are needed, including templates that reuse unchanged assets. **Light** means occasional simple figures; **moderate** means recurring figures that carry part of the problem; **heavy** means plots are central to most variants or require substantial construction. Inspect plot content and its role; plot counts alone do not establish the rating. Standalone math rendered from LaTeX does not count as a plot.

Use efficient [$edb](../../skills/edb/SKILL.md) reads and preserve the database basis with the classification. Flag missing questions, unreadable plots, or unresolved template differences instead of guessing; canonical examples may support the analysis but do not count as practice questions.
