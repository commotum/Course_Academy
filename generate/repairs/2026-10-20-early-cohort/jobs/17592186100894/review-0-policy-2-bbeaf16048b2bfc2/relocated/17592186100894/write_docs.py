import json
from pathlib import Path
p=Path(__file__).parent
j=json.loads((p/'source.json').read_text());qs=j['record'][':knowledge-point/questions']
rows=[]
for q in qs:
 f=q[':question/answer-fields'][0];mid=q[':question/math-academy-id'];shape='denominator' if mid=='q-355560' else 'logarithm argument' if mid=='q-355576' else 'RHS expression' if f[':answer-field/type'][':db/ident'].endswith('blank') else 'whole equation'
 rows.append(f"| {mid} | {q[':question/difficulty'][':db/ident'].split('/')[-1]} | {f[':answer-field/type'][':db/ident'].split('/')[-1]} | {f[':answer-field/key']} | {shape} | {len(f[':answer-field/choices'])} | none |")
(p/'classification.md').write_text(f'''# Classification

Database math, immutable source basis {j['basis']}, lineage {j['lineage']}.
KP 17592186100894: {j['record'][':knowledge-point/title']}.
All 24 source practice questions were pulled together, with full fields, choices,
correct designations, solutions, generator reference and canonical example.
No registered generator or saved job `.generated` file existed at initial read.

| Source | Difficulty | Type | Key | Response | Options | Plot rating |
|---|---|---|---|---|---:|---|
'''+ '\n'.join(rows)+'''

There are 23 observed prompt/value/stage families: q-355577 and q-355582 share
one exponential RHS blank family, differing only in initial ordinate. The other
sources retain separate expression structures, field fragments, or solution
stages. Each radio source has its own complete empirical bank profile; no choices
are pooled. Each blank has no distractor profile. 22 families are supported for
replay and translation (23 source questions); q-104058 is excluded.

No prompt, answer, or solution in the captured KP needs a plot. All images are
absent; standalone mathematical notation is not a plot.

q-104058 has no classical IVP solution: at x=1,y=1 its derivative coefficient
1/(xy)-1/x is zero, but the right side is 2. Its source is retained unchanged,
and the implicit curve is not misrepresented as a differentiable solution.

Easy and moderate are supported by observed questions and their exact methods.
Hard has no observed source form in this KP. The bounded supported policy adds
no new integration, response, or solution stages to invent a hard form. Hard
remains unsupported for this package, generated 0, shortage 5. New source
evidence reopens classification; unsupported does not mean mathematically
impossible forever.
''')
(p/'template-extraction.md').write_text('''# Template extraction

`source.json` retains every original prompt, solution, field-owned choice and
correct reference, including the excluded source. `choice-ledger.json` assigns
every supported source option to its field and complete empirical bank profile,
its exact original expression and the transformation that reproduces it. It
records unresolved error intent rather than inventing distractor explanations.
`source-fidelity.json` reports complete bank matches, missing and extra options.

The backbone is rearrangement to a separable equation, integration of the source
integrands, the same explicit inversion or implicit form, applying the initial
condition, and the source's final particular solution. The response stays a
whole radio equation, an RHS blank, a logarithm argument, or a denominator.
The original solution sentences and ordered calculations are retained. Documented
corrections are separate from immutable source evidence; see `validation.json`.

Observed values are the exact source expressions and initial data in
`source.json` and the independent `MODELS` table. The only sampling parameter is
the integer h in [-4,4]. h=0 is source replay; new instances use h != 0. This
is an explicitly narrow same-method generalization: replace each supplied x
argument by x-h and each initial abscissa x0 by x0+h. Derivative and differential
notation, y(x), integration-variable prose, field keys, choice counts, branch
assumptions and initial ordinates remain fixed. All complete source choices
undergo the same substitution; no shuffled/seed identities add inventory.

The derivative of x-h is 1, so this preserves the rearrangement, primitives,
constant evaluations and inversion stages. Numeric evaluations in the source
initial-condition calculation remain equal because (x0+h)-h=x0. A blank's
supplied numerator must change with h; the denominator fragment changes too.

The domain is the connected real interval containing the translated initial
point on which the original equation and solution exist. Exponential/log and
root branches are retained, including the positive y assumptions in q-355559
and q-79425 and 0<x-h<pi in q-104065. Singular initial data are rejected;
q-104058 is never sampled. ODE residuals and initial-value residuals are checked
symbolically, independently reading the rendered equation and initial data.

`slot-coverage.json` covers all nine values of h for all 23 supported source
profiles. `review.md` places each full original beside its h=2 variant.
The changed-initial-abscissa mutation holds the ODE fixed and proves that stale
initial-condition references/keys fail validation. Complete source-bank replay
is distinct from mathematical correctness and the native grading checks.

The finite translation policy permits at most 8 new tasks per source profile
before deduplication (184 upper bound across levels). This is a capacity bound,
not a claim of 184 currently available tasks; existing content, canonical tasks,
learner presentations, reservations and mathematical collisions are excluded
again at preparation. Exhaustion yields finite-limit with shortages explicit.
''')
(p/'plot-extraction.md').write_text('''# Plot extraction and generation

No plots occur in the 24 source questions' prompts, banks or solutions. Their
role is fully symbolic. Plot rating none; no assets to render, publish or hash.
The generator creates no images, and the asset manifest is empty.
''')
(p/'README.md').write_text('''# Rearranging and separating IVPs

Generator: `generate/scratch/17592186100894.py`.
Run from the repository root with `.venv/bin/python`:

```sh
.venv/bin/python generate/scratch/17592186100894/validate.py
.venv/bin/python generate/scratch/17592186100894.py --difficulty easy --seed 7
.venv/bin/python generate/scratch/17592186100894.py --difficulty moderate --template q-355560 --shift 2 --format markdown
.venv/bin/python generate/scratch/17592186100894/replenish.py
```

Easy/moderate only. Complete observed banks; deterministic content identities;
finite exact x translations; no seed/choice-order duplication. Source evidence
is immutable. q-104058 is inconsistent and excluded. Hard is unsupported by
this bounded package and remains a shortage, not a filled band.

Classification, template extraction, source-bank replay, mathematical audits,
real learner grading, slot coverage and original/variant review are retained
here. `reference/replenishment/` retains each preparation basis, exact typed EDN,
preview, fsynced durable intent, receipt and exact-basis readback. Publication
holds the shared application `api.lock` through inventory, submission and
readback, uses configured application contributor `:application/ca-engine`,
and adds only this KP's generator and validated content.
''')
print('classification and template documentation saved')
