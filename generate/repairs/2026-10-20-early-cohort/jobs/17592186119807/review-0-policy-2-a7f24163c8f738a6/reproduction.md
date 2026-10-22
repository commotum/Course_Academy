Run from this evidence directory with `PYTHONDONTWRITEBYTECODE=1`.

Python executable: `/home/jake/Developer/Course_Academy/.venv/bin/python`.
Repository: `/home/jake/Developer/Course_Academy`.

- `python audit.py` creates the complete 46-record finite catalog, fresh seeds 31,83,211,4001,99173,20261021; source replays; boundary tests; exact-arithmetic checks; and batched native grader inputs. Here `python` means the absolute executable above.
- `python finish-tests.py` creates the single-component consistency counterexample and checks relocation under evidence_root. It initially writes a regression script; the retained regression-checks.py has the broader role-variation assertion rather than demanding one exact new target.
- `python controls.py` constructs the irrelevant name-change fixture from that counterexample.
- `python regression-checks.py` exits1 on the current package: four missing source profiles, no consistent c/d-labelled cases, and a perfect numeric-order shortcut in the exact batch. Run individual cases with `RequiredCases.test_all_source_profiles`, `RequiredCases.test_consistency_role_can_change`, or `RequiredCases.test_actual_batch_has_counterexample_to_second_largest` as arguments. These are intentionally failing acceptance checks, not passing self-certification.
- `python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery-batch` accepts5/5. Replace batch.json/output by catalog.json/delivery-catalog to reproduce46 ->36, with10 duplicates. No assets are used.
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json` tests270 responses. Repeat with controlled-grader-input.json/controlled-grader-report.json for15 controlled responses.
- `python delivery-grading.py`, then the same native executable with delivery-grader-input.json/delivery-grader-report.json, tests25 responses after publisher ID normalization.
- `python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-all --asset-root . --limit 12` renders representative raw records and translation controls.
- Repeat renderer with controlled-render-records.json/render-controls/limit3 and delivery-batch/accepted.json/render-delivered/limit5 for consistency/label controls and the exact surviving batch.
- `python build-report.py` derives final decision evidence and checks package byte hashes; it does not modify the package.

Publication preparation, repair-history and repair-preflight files were absent. No earlier independent review was supplied. The captured inventory at basis5400 contains exactly the14 supplied source exercise IDs and no stored generated instances. affected-inventory.json is empty on that verified basis, not because the generator shortcuts were absent.

The raw-choice-position hypothesis was withdrawn after actual UI inspection: learning.js choiceOrder reorders choices using item/field/answer identities. Numeric rank and vector names survive that stage. Selection is inspected from question_selection.rs: a positive moderate weight selects uniformly from eligible moderate entities; zero excludes that band; no policy chooses the lowest ID. Learner history removes candidates. No concrete learner/policy/task IDs were supplied, so there is no claim of the next exact chosen entity. Perfect subgroup and batch cues survive any nonempty eligible subset of that subgroup/batch.
