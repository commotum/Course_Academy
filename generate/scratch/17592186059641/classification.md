# Classification

Captured database **math**, basis **1356**, lineage **01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1**. `source.json` is an unchanged capture wrapper. Ten practice sources are fully covered: four easy, four moderate, two unrated. Every source has one `selection` radio field and five mathematical choices. There are no plots, images, coordinate readings or angle evaluations.

| Level | Practice sources | Observed layout | Exact replay masks / banks |
|---|---|---|---|
| easy | q-119362, q-65229, q-65241, q-65242 | one five-choice radio | 4 / 4 |
| moderate | q-119367, q-119371, q-65243, q-72711 | one five-choice radio | 4 / 4 |
| unrated | q-65163, q-65193 | one five-choice radio; no correct ref | 2 / 2 |
| hard | none | authored radio and optional blank | 0 observed |

Ten exact masks preserve prompt order, complete banks, shared prose, and solution row sequence individually; they do not imply ten distinct skills. The mathematical patterns are a pure-function monomial GCF, a mixed-function monomial GCF, a GCF with an opposite-function residual, a GCF with the same-function residual, and complementary squared residual terms. Source prose differences (explicit factor versus generic factor, conclusion wording, extra collection row), term order, and the two malformed solution blocks remain visible in their respective masks.

The two unrated examples receive an **authored easy assignment** only in completed repaired output. Raw public replay omits difficulty, worked solution and correct reference exactly as captured. Their mathematically derived winners are cos(angle) and sin²(angle)cos(angle), respectively. These inferences are not counted as matched original designations.

## Curriculum boundary and all-level policy

The owning topic is 207, Simplifying Expressions Using the Pythagorean Identity. Its actual linked route is Introduction → Expanding Parentheses KP → this Factoring KP → Rational Expression KP → Common Denominator KP, reconstructed from `activity/first-step` and `step/next`. The named key prerequisite is Factoring Polynomials Using GCFs (topic 353). This KP's canonical example factors sin² from sin⁴+sin²cos², then substitutes the Pythagorean identity. The neighboring quotient and common-denominator examples belong to separate KPs and are excluded.

Easy defaults use one monomial GCF of total degree 1–3, two terms, coefficient ±1–5. Mixed powers are supported by both q-65193 (unrated) and q-65241 (easy). Moderate defaults use three terms and one GCF with a residual requiring either linear collection or a second identity. Coefficients are ±1–4. Those are unordered equal-level families, not a progression. Hard is an explicitly authored missing-level extension: four terms arranged as two disjoint monomial GCF pairs, with odd factor degree 1 or 3 and coefficients ±1–4. It repeats the same source operation twice; no reciprocal identities, rational manipulation, angle identities, evaluation, root extraction or expanded-parentheses branch is introduced. The hard label is a design claim grounded in the same GCF prerequisite, canonical factoring move and moderate repeated-identity scope.

Normal default fields remain radio. Optional blank layouts at every authored level ask for the complete simplified expression and include `{{selection}}`. Blanks are an authored layout extension, not a recovered source field.

## Finite substantive variation

Exclude angle aliases, option order and layout from task counts. Fully enumerated authored catalogs contain **90 easy, 252 moderate, 256 hard = 598 distinct displayed mathematical tasks**. Moderate has 272 candidate parameter sets; 16 cancel the defining same-factor collection demand, and 4 create an equivalent complete-bank collision (a=±3, b=∓2, either linear factor). The entire instance is rejected. Easy and hard have no rejected catalog members. Each sampled and explicit call uses the same bounds and complete-bank collision checks.

Raw source profiles additionally expose sine/cosine symmetry of complete original expression patterns. q-65241 is mathematically symmetric, so its swap adds no task. Symbols and source bank aliases never inflate task counts. Observed bank intentions cannot be uniquely recovered from scalar expressions; authored defaults therefore use separately labeled explicit operation banks.

## Anomalies and denominator discipline

q-119362's identity block incorrectly starts with cos² where cos³ is required. q-65229's corresponding block omits the angle on cos². Both public raw profiles preserve the error and are marked evidence-only. Repaired profiles make precisely those mathematical repairs. All eight captured solutions replay byte-for-byte; six are mathematically correct. Completed repaired output has ten correct solutions, including two explicitly authored solutions for previously absent ones. The canonical example also omits an argument on cos², recorded as context evidence rather than an eleventh practice source.

Decoded-byte inspection finds **zero literal backslash-u2061 escapes** and **54 actual U+2061 function-application characters** in the 50 choice strings. The per-bank counts are recorded in `validation.json`. No nonexistent escape corruption is claimed. Repaired profiles use conventional trigonometric LaTeX; this is presentation normalization, distinct from the two mathematical changes. Original correct objects may spell the same value differently from their owned choice; designation fidelity follows their answer UUID, and raw choice text remains unchanged.
