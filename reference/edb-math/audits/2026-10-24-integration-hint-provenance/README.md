# Provenance of the supplied integration hints

Read-only audit. Current flagged/source evidence at **T6720**; broader related-prompt scan at **T6723**. No questions, generators, or learner data were changed.

## Direct finding

The standard primitive formulas and endpoint-value hints in the three flagged generated questions were **authored additions**. No matching support appears in the imported prompts for their own KPs: **50 practice questions and 3 canonical examples checked**.

| Generated question | KP | Added pre-answer help | Own imported practice / canonical |
|---|---|---|---:|
|17592186678417|17592186068918, trig quotients|The primitive of 1/u is ln\|u\|+C|19 /1|
|17592186678190|17592186068916, reciprocal trig linear arguments|The csc-cot primitive, plus csc(π/6)=2 and csc(π/2)=1|19 /1|
|17592186678090|17592186068915, sine/cosine linear arguments|The primitive of sin(u) is −cos(u)+C|12 /1|

The stored generator metadata confirms `provided_primitive: true` for all three, and `provided_endpoint_values: true` for 78190. Its `band_origin` explicitly describes an authored scaffolding/response extension. See the original package records under `reference/edb-math/repairs/2026-10-24-trig-scaffolding/`.

Representative imported source prompts, retained with solutions in `representative-sources.json`:

- **q-49557 /17592186069378**, same quotient KP: calculate ∫2cos(y)/sin(y)dy. It supplies no logarithm primitive.
- **q-13524 /17592186580882**, same reciprocal-trig KP: calculate ∫csc(2x)cot(2x)dx fromπ/6 toπ/4. It supplies no primitive or endpoint-value table.
- **q-10061 /17592186237798**, same linear-trig KP: calculate ∫sin(2x)dx. It supplies no sine primitive.

The formulas and reasoning are present in instructional explanations and worked solutions. That does not mean the same support is part of the assessed question. The imported introduction tutorial **17592186070016** explicitly assumes familiarity with integrating cos(x), then teaches how to extend that knowledge to cos(3x) by substitution. “Integrating Trigonometric Functions” is also an explicit prerequisite topic in the captured source context. See `instructional-context.json`.

## Actual imported scaffolding elsewhere

A broader scan covered **2,036 unique imported prompts across 183 related integration/substitution KPs** from the retained related-KP catalog. This is a scoped database audit, not a claim about every question Math Academy has ever published. Hint-word searches locate candidates; the examples below were inspected directly.

- **q-49529 /17592186332733**, KP17592186064209: gives u=2x−1 and asks which integral is equivalent to ∫x√(2x−1)dx from1 to3. The assessed task stops at transformation.
- **q-49532 /17592186392689**, same KP: gives u=3−2x² and likewise asks for an equivalent integral.
- **q-152641 /17592186275287**, KP17592186192837: directs the learner to use u=√x to evaluate an improper integral. This is explicit substitution support even in a full-evaluation task.
- **q-49785 /17592186332775**, KP17592186068800: supplies a partial-fraction decomposition, then asks for its integral. This isolates integration from finding the decomposition.
- **q-39154 /17592186198969**, KP17592186198396: explicitly hints which order of integration to use in a triple integral.

These establish that imported questions use **targeted, task-specific support**. They do not establish a policy of supplying familiar primitive formulas and standard endpoint values throughout ordinary trig-substitution practice. No imported prompt in the three directly relevant KPs does that.

## Assessment of our change

The added help was intended to isolate substitution and reduce incidental recall after the earlier difficulty failures. That is a pedagogical rationale, not evidence of Math Academy source fidelity or measured benefit. Applying it universally went beyond the source-backed repair. Normal practice can reasonably retrieve mastered prerequisite formulas; guided exercises can explicitly provide support for a limited stage or a particular unfamiliar step. A worked solution should still explain all conversions regardless of the prompt's level of support.

My recommendation is to omit the blanket primitive reminders and routine endpoint facts from these ordinary full-calculation bands, while retaining justified task-specific support and explicitly guided transformation exercises. This audit does not apply that change.

## Additional provenance question

**17592186678309 is generated**, from the refreshed pool for KP17592186068917, “Integrating Products Containing Trigonometric Functions Using Substitution,” within topic17592186050489. Its prompt supplies u=x³ and asks for the transformed form of ∫x²csc²(x³)dx. It has no Math Academy import ID; its entity and generated record are retained in the trig-scaffolding publication evidence and the prior exact-question UI audit.
