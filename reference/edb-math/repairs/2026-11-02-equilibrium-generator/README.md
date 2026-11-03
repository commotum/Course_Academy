# Equilibrium-identification repair

Published to math at **T12353** on 2026-11-03; live readback and grading verified at **T12354**.

Topic **17592186051068 — Equilibrium Solutions of First-Order ODEs**, KP **17592186166788 — Identifying Equilibrium Solutions of a Differential Equation**.

The reported generated question **17592186694294** now gives the equivalent unwrapped equation rather than adding `y+1` to both sides. Its worked solution keeps `(c−1)² ln(c−1)+e⁻²` intact, checks the original domain, and tests the supplied constants in that same residual. It explicitly shows the logarithm values, including `ln(e⁻¹)=−1`. Its choices, correct keys, question/field/answer identities and saved responses are unchanged. Only its prompt and worked solution changed.

The registered generator is version **2.0.0**:

`generators/4f/4fd06a5b0cf48eeed6d10418e1b6cad209e39ef6a90fedc95a4468179725ac42/generator.py`

- Removed the artificial cancelling wrapper from moderate sampling.
- Preserved useful factored and shifted expressions instead of expanding them before substitution. Solutions rearrange once, state the domain, and follow one residual rather than returning to separate left/right calculations.
- Removed the easy prompt's supplied equilibrium criterion. Required function-value conversions appear in feedback.
- Easy uses small unshifted expressions; moderate adds a real rearrangement or a small translation. Hard introduces a domain decision with both an excluded candidate and a valid non-equilibrium candidate. Four hard candidates allow one or two correct answers without making domain checking sufficient to answer the bank.
- Pools cycle through the supported mathematical families, reject repeated equations within a batch, and retain checks for recurring position, sign and numerical-rank shortcuts. Small polynomial parameters and compact candidate arithmetic control incidental work.
- Long equations and candidate checks wrap across rows. Actual desktop and phone geometry checks detect clipping independently of MathJax parse success.

**13 unused old generated questions retired; 15 new unused questions added, five per band.** Used questions 17592186694170 and 17592186694225 remain unchanged. The reported used question received the equivalent prompt and clearer feedback described above. All six imported practice questions, the canonical example, observed imported level coverage, existing response ownership and learner history are preserved.

The imported evidence remains [the source review](../../audits/2026-11-01-equilibrium-17592186694294/README.md): q-95572, q-96070, q-160422, q-160419 and q-96072 are the five complete easy banks. The logarithm source legitimately uses `y′+e²=y² ln(y)`. Source q-96071 is unclassified and incomplete; it was left unchanged. The canonical example e-8409 also rearranges once and checks a residual. There are **no imported moderate/hard anchors** here; those bands are controlled authored extensions, not a claim about imported calibration.

The shared publisher now rejects criterion-giving prompts, switches to `L(c)`/`R(c)`, lost residual structure, wrong labels/keys, gratuitous cancelling copies, and hard banks answerable solely by domain membership. It independently derives domains from logarithms and denominators before cancellation. Wrapped equations remain eligible. Author/reviewer prompts and the template-generator instructions document the construction rules. The learning service was reloaded for the shared checks.

Verification retained here:

- **56 regression tests passed**, including the reported logarithmic case, complete source banks, all supported families, original-domain keys, negative controls and delivery behavior.
- Independent high-precision evaluation of the original sides and domains verified all 50 new candidate keys. The actual publication filter retained all 15 questions without duplicates.
- **180 native grading checks passed**: visible candidate values, printed ODE/model agreement with changed-constant rejection controls, and both Boolean choices for every new field. No unresolved cases.
- All 15 new questions and the reported repair passed desktop and 390px phone UI rendering, with no overflowing display math, raw TeX or math errors. Three active phone examples also passed. Representative long logarithmic and reported-question screenshots were visually inspected.
- The immutable package reproduced every delivered band outside the repository and after installation. The local scratch entrypoint uses identical package bytes.
- **69 live grading checks passed**, including each correct complete response and each single-checkbox flip, for all 15 new questions and the reported repair. No learner attempts were created. Fresh availability is five per band.
- The durable request, receipt and exact as-of readback verify that only the intended registration, new entities, retirement flags and reported text changed. See `verification.json`, `publication/`, and `completion.json`.

Reproduction: `validate.py`, `render_all.py`, `deploy.py`, `verify_live.py`, and `tests/test_equilibrium_pedagogy.py`. The exact authored pool is `candidate-pool.json`; delivery-normalized records are retained under `delivery/` and `publication/`.
