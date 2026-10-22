# Verification outcome

Status: unsupported. Existing runtime repairs are preserved; no new generator defect was demonstrated.

First command: `/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory` exited 1: five affected stored questions, with 64/64 sign-extremum shortcut successes in the retained possible-history scenario. The scenario is a conditional witness, not a claim about actual learner histories.

Then `/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/repair-311` exited 1 solely for finding 591f580cadb749294588. See commands.json and results.json. Four generator findings pass, including 17 complete source-bank replays, canonical replay, controlled counterfactuals, 14 accepted delivery records with subgroup contrasts, native grading (7 accepted, 28 rejected), exact dependencies and relocation. Runtime, manifest and captured inputs match the retained hashes. The existing replacement proposal and its complete records were verified again; nothing was applied.

The historical failure arises from five persisted v2 answer banks. The native selector reads supplied stored candidate entities and difficulty, independently of this Python entrypoint. Altering the generator cannot change those captured banks or remove the persisted candidates. The retained finding explicitly requires the separate inventory-remediation workflow. This task prohibits database changes, and engine_repair_allowed is false. Neither a runtime value patch, a new sampling window nor hypothetical replacement inventory resolves this failure. The strict regression remains failing.

Next required action is external: independently review and apply the existing evidence/repair-3/inventory-repair-proposal.json through the separately authorized workflow, preserve source questions and learner history, recapture inventory, and recheck the selectable pool. Further unchanged workspace passes cannot perform that action.

Reused actual-UI screenshot evidence/repair-3/render/question-002.png was visually reinspected: system, five choices, matrices, elimination and worked solution are legible and agree (k=12). No new render was necessary because runtime and source hashes are unchanged. No images were published, and no database, engine, source, publication or other job files were changed.
