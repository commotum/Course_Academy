# Limit operator and display notation: q-339068

Reported question **17592186314749 / q-339068** belongs to topic **1717**, “Limits of Exponential Functions.” Reads were pinned to **T8383**. The notation repair committed at **T8394**.

The question stored `${lim}_{x\to 2}{4}^{x/2}=$`. Its four-letter appearance is not a changed limit or a greater-than relation: the condition is **x → 2**, and the correct answer remains **4**. The earliest retained question assertion at **T108**, attributed to `:org/Math-Academy`, already contains the malformed operator.

Two issues combine:

1. `{lim}` is a group of ordinary letters, not the TeX operator `\lim`. A subscript on this ordinary atom sits on its right even in display math.
2. The standalone prompt uses inline `$…$`. Even a correct `\lim` normally uses a side condition in inline style; a main displayed limit should use display math when the condition is intended underneath.

The repaired prompt is:

```tex
$$
\lim_{x\to 2}{4}^{x/2}=
$$
{{field-1}}
```

The original question, field, answer and correct-link identities are unchanged. Its answer value is still `4`.

## Source and reproduced cause

The archived topic HTML contains nine limit-bearing MathML formulas. These explicitly represent a limit as `<munder><mo data-mjx-texclass="OP">lim</mo>…</munder>`, with original display/block or displaystyle information. The generic importer previously converted that structure to `{lim}_{…}`, losing the operator role. Historical bare MathML `display="block"` was also missed by a branch that recognized only MathJax-container `display="true"`.

The exact practice question q-339068 is not present in this earlier archived lesson page; its own retained database history establishes the imported malformed value. The archived family formulas and importer code provide the source-shape reproduction, not a claim to possess that practice question's original HTML. [Source MathML](source-limit-mathml.json), [question history](history.json).

## Lesson repair and verification

- Corrected **111 formula blocks in 72 fields across 39 question/example records**: 38 problems and 34 worked solutions. Recovered `{lim}_{…}` and `lim_(x → …)` operator forms, and corrected two malformed `\lim_\limits{…}` prompt forms.
- Promoted **38 main prompt expressions** from inline to display math. Existing displayed formulas and the lesson's already-correct tutorials remain intact. Original operands, tendencies, answers, field markers, source identities, image references and learner history are preserved.
- Actual player rendering verified all 72 changed fields with zero final MathJax or page errors. The original malformed forms also produced no syntax errors, so typesetting success alone was insufficient.
- Visually inspected the reported question. DOM geometry confirms that its repaired limit has an under-condition centered within **0.22px** of the operator, below the operator rather than alongside it. [Before](target-before.png), [after](target-after.png), [geometry](target-geometry.json).
- Native EDB speculative validation, exact receipt datoms and committed readback passed. Only reviewed question content and the transaction timestamp changed. [Preparation](preparation.json), [transaction](transaction.edn), [verification](verification.json).

This is a notation-focused lesson repair, not a mathematical correctness/completion audit of every question or a database-wide migration.

## Prevention

Both browser extractors and the historical renderer now preserve a MathML `munder` limit as a real `\lim` operator, and recognize bare MathML `display="block"`. The shared semantic formatter repairs the identified legacy forms only when a tendency condition identifies a limit. Explicit font/text/operator arguments remain protected. No shared UI workaround was added.

Validation passed: **29 shared math-format tests**, **10 browser/historical importer tests**, and **3 historical matrix/display regressions**. The limit regression checks all three importers, and the brace tests verify that an entire limit remains inside its original underbrace rather than moving the condition or label outside it. No generator is registered on any of this lesson's three knowledge points.
