# Verification evidence

- `.venv/bin/python generate/scratch/17592186105734/validate.py`: pass; 18 source cases, 18 changed source cases, 180 authored records, 76 signed implicit-product checks. Native engine 94 accepted / 138 rejected / 0 unresolved.
- Imported `generate/runs/current/triangle-readback.py` directly without shared writes: all 24 masks at seeds 30–41, 288 actual-token records passed. Results in independent-readback.json.
- `.venv/bin/python generate/scratch/17592186105734.py --difficulty all --seed 8 --count 2 --format json`: six CLI records; each independently validated from its actual prompt and math, saved in cli-smoke.json.

Original source stage math: 16 valid, one known reduced-basis typo; all 17 valid after exactly the documented q-128008 j→k repair. Raw and repaired solution fidelities are separate. q-20028 has no observed solution/key; its complete reconstruction is authored and cannot count toward exact missing evidence. Complete bank values still match all five choices.

The real engine fixture is memory-only. freeze.json records the final generator and evidence SHA-256 hashes plus native engine binary/source hashes. No database operations or shared file writes were performed.
