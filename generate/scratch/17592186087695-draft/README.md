# Identifying a Zero Matrix — private steps3–7 draft

Script: `generate/scratch/17592186087695-draft.py`. Evidence is confined to this directory. Registered numeric script/tree/pycs are unchanged; no database/registration/engine writes or commits.

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186087695-draft/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186087695-draft/render.py
.venv/bin/python generate/scratch/17592186087695-draft.py --difficulty all --count 1 --format json
```

Rendering requires a temporary localhost server and installed read-only Chromium; this sandbox needs the command's approved escalation. No packages installed. The native helper is `generate/scratch/17592186059716-draft/check-engine`; all42 recorded hashes are verified against `reference/grader-build.json` before grading. The old current/check-engine binary is not used.

The strict public API is generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), with generate_easy/moderate/hard. Plain field_type values are checkbox or radio; observed profiles and parameters are in source-cases.json. Canonical is an explicit separate template. Moderate/hard are same-method authored/uncalibrated placements, not source-observed higher difficulty. Finite shape/support variety suffices for recognition without adding another matrix skill.

Seven MA practice cases replay every prompt and complete bank (40 choices);15 captured correct designations match. Two missing keys are independently inferred and two missing solutions are authored. Four of five captured solutions are exact; q-126201 minimally repairs its false witness i12 to i21. One independent captured inventory record is complete and separate. One canonical is restored from original screenshot evidence. See classification.md for provenance and scope limits, validation.json and engine-report.json for detailed QA, review.md/json for all originals and42 labeled variants, render-report.json/renders for actual player output, registered-baseline.json and owned-freeze.json for integrity.
