# Triangle area private revalidation draft

This unregistered private draft preserves the registered numeric script and its complete evidence/cache tree. Its immutable source, topic, and lesson wrappers remain at math basis1356: this KP has no refreshed source wrapper. All six practice records are original Math Academy questions. canonical.json is separate supporting evidence; independent-inventory.json records that no independently authored captured practice exists in this wrapper.

Run from repository root:

```sh
.venv/bin/python -B generate/scratch/17592186105903-draft/validate.py
.venv/bin/python -B generate/scratch/17592186105903-draft/render.py
.venv/bin/python -B generate/scratch/17592186105903-draft/verify-baseline.py
.venv/bin/python -B generate/scratch/17592186105903-draft.py --difficulty all --count 2 --format json
```

The player render requires local loopback HTTP and Chromium. It uses the actual player Markdown/fieldControl routines and real mountInlineFields, MathLive, DOMPurify, marked and MathJax modules. render-report.json records32 rendered records and26 screenshots. Full-size PNGs live in renders; reference/player-contact.png shows representative easy radio, easy blank, moderate and hard records.

The difference from the previously approved script was a generator UUID constant and normal calculator requirement. The private draft additionally normalizes shared math content before computing IDs, validates normal public output and rejects unintended C0 controls. revalidation.json records21 normal learner-payload comparisons against the reviewed code (byte-identical apart from the calculator attribute) and six byte-identical original raw replays. Prior source/raster/scope proof remains in reference with its exact reviewed SHA. Rendering/math functions are unchanged; fresh math/native/render checks were also run.

validation.json separates six exact prompts/banks (18 values), five available exact worked solutions and five recorded designations from one genuinely missing original solution/rating/designation. All84 normal sampled records pass independent displayed-stage/bank/geometry checks. Stage-omission and C0 mutations are detected. Eighteen cold/cache full-record comparisons and concurrent fresh renders pass. All five eligible easy families are sampled by default.

Current native grader SHA33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617 grades367 checks across89 records:89 accepted,278 rejected, zero unexpected/unresolved results. reference/grader-provenance.json verifies42 current source/library/binary/dependency hashes. Equivalent extra trailing-zero precision in rounded blanks is rejected by the native form rule; these known restrictions are tested explicitly and are not claimed as accepted equivalents.

Scope and evidence limits remain those in classification.md and template-extraction.md. Moderate decimal-side work and hard isosceles angle-sum work are authored policies, not observed MA labels. Three opaque historical banks are public raw evidence profiles only. The original sine-precision error and included-side prose typo remain raw and ineligible, with two minimal normal repairs. No inverse-area, quadrilateral, vector, or height method is added.

immutable-baseline.json contains the original numeric script plus recursive numeric evidence/cache and matching sibling pyc pathset/hashes:808 paths,775 files. verify-baseline.py must pass after work. freeze.json lists all final private files except itself. Root approval is pending. No database writes, registration, engine edits, shared-file edits, or commits were performed by this draft workflow.
