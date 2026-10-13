# Solving for an Unknown Given the Determinant

Local generator stops after steps 3–7. No database writes or registrations.

Verify with `.venv/bin/python generate/scratch/17592186059849/validate.py`.
Regenerate evidence with `.venv/bin/python generate/scratch/17592186059849/build-evidence.py`.
Preview with `.venv/bin/python generate/scratch/17592186059849.py --difficulty all --seed 17 --count 2 --format markdown`.

24 source questions (17 radios, 7 blank questions / 10 fields). All source banks are explicit profiles; source values replay through coefficient expressions. Default radio banks are separately authored determinant/equation mistakes. All three levels are supported. Unrated q-9657 and q-9852 have authored moderate/hard assignments and independently inferred correct answers, so two original designation matches remain unavailable. Source prose/method is shared but intermediate worked-solution row rendering is standardized; see validation.json for that fidelity limitation. No plots are needed.

Source profiles are the source ID; authored radio profiles prefix `authored:`. `generate(level, seed, template, field_type, parameters, profile)` accepts original coefficient arrays and rejects invalid explicit parameters. `source-cases.json` contains all original calls. `review.md` includes originals, two variants per observed matrix/bank, and one authored default per radio source. Identity depends on mathematical parameters, field layout and complete bank rather than seed/order.

## Parent QA corrections

Question identity includes the rendered prompt, solution, complete bank and version. Shared source prose and punctuation were restored for five replay cases. The initial expanded determinant sum uses the actual rendered sign, preventing a missing plus sign before a parenthesized term; every displayed determinant equality is now independently checked, including the initial minor expansion. Parent replay checks cover all95 source values and90 independently parsed generated questions.
