# Shorthand fraction follow-up

See ../2026-11-03-fraction-fences-database/README.md for the full database-wide repair.

The fixed-basis residual census at T12449 identified 15 additional attributes requiring sizing after valid single-token fraction arguments were supported: nine worked solutions and six math answer values. They do not overlap the main pass's repaired fields. Exact guarded native readback verified all 15 changes at T12454 in one durable, archived transaction. Mathematical tokens, identities, correct links, learner history and every unrelated attribute are preserved.

Six answer matching identities and one choice bank passed verification, with no introduced identical choices and no raw learner submissions changed. Eight actual formula patterns rendered through the learner UI. Baseline and final grading evidence is retained for 32 cases on eight complete questions; two unowned questions cannot use the topic-scoped grading route and remain separately documented. They are still covered by exact content readback and mathematical-token preservation.

build.py recreates the reviewed plan from the archived parent residual census and captured answer types. deploy.py retains the original transaction request and exact readback evidence. preflight.py, identity.py, render.py and verify_live.py preserve the validation. The final whole-database census is in the parent directory.
