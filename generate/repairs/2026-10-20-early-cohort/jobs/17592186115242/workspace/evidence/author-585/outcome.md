# Verification outcome

Status: unsupported because the retained historical-inventory acceptance criterion still fails. No new runtime construction defect was demonstrated by the latest feedback.

Reproduction: `/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory` exits 1 for five captured stored questions. Complete records and generation metadata remain in `evidence/generated-records.json`; exact identities remain in `affected-inventory.json`. All generated inventory items were audited, with none untested. The 64/64 result is a possible learner-history witness, not a claim about every actual learner.

Verification: `/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/author-585` exits 1 only for finding 591f580cadb749294588. commands.json contains exact subprocess commands and results. Four generator regressions, 17 source-bank replays, delivery of 14 records with conditional shortcut checks, relevant/irrelevant coefficient controls, 7 accepted and 28 rejected native-grader responses, and relocation pass. Protected package/input hashes match. Reused actual-UI rendering remains bound to the unchanged proposal; question-002.png was visually inspected this pass.

The five-replacement proposal in `evidence/repair-3/inventory-repair-proposal.json` verifies but remains unapplied. The retained finding explicitly calls for separate inventory remediation and fresh capture. Generator edits cannot change stored candidates. Database changes and publication are prohibited here; the strict failure has not been waived or hidden. No runtime, engine, source, database or publication changes were made.
