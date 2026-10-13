# Coplanarity scratch generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186105908/validate.py
.venv/bin/python generate/scratch/17592186105908.py --difficulty all --count 2 --seed 8 --format markdown
```

Normal API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three level entrypoints. Authored method banks default to `profile="method"`; parameters contain complete `vectors` and `variable`. `linear` supports all three levels, `quadratic` supports the observed moderate scope. Explicit invalid inputs raise rather than resample.

Public source evidence: `generate("moderate", template="q-128436", parameters={"shift":0}, profile="source:q-128436:raw")`. Every `source-cases.json` entry replays using that API. `shift` coherently replaces the original unknown by `(unknown+shift)` and translates every scalar/root choice by minus the shift. Original banks are opaque evidence recipes, not inferred error operations, and never the normal default bank. `:normalized` evidence profiles infer the two missing correct refs/solutions/ratings and repair q-18266's wrong singleton designation. Both source profiles are labeled `evidence_only=true` and `eligible_for_learning=false`; authored defaults have the inverse flags. raw profiles deliberately retain source errors and omissions. The exact source-bank recipe has unknown pedagogical intent, an explicitly retained interpretation limit rather than unresolved mathematical correctness.

All normal choices use determinant method operations, and each complete five-option bank is accepted or rejected as a whole. Radios shuffle deterministically. Content UUIDs depend on prompt, fixed solution and the complete displayed bank; seeds/order and profile aliases do not enter identity. Mathematical fingerprints depend on canonical displayed vectors and exclude banks and letter aliases. Metadata stays outside learner fields.

No plots, database writes, engine changes, or registration. The validator checks exact full source content, all displayed determinant/isolation stages, full scalar/root-set choice semantics, formatting, bounds, identities, seed variety, and the compiled native grader. Raw grading's q-18266 singleton acceptance is a source correctness exception; two raw sources with missing refs cannot form native fixtures. They are verified and graded in repaired evidence separately.

Parent QA repaired the completed q-18268 solution to name its actual supplied vectors p,q,r; the validator now checks every formal triple against prompted names. Available original solution strings remain exact.
