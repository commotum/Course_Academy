# Author 722 — 2026-10-22

Preserved completed runtime repairs, executable regressions and five staged
replacements. Read feedback, all five retained findings, source and instructional
context, and required generator/validation documents. Inspected tutorial diagram
and two retained actual-UI screenshots. No runtime change is justified by the
latest historical-inventory finding.

First reproduction:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`
Exit 1: five affected stored records, 64/64 shortcut successes in the retained
possible new-seen history. All generated inventory records were tested.

Validation:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/recheck_status.py --output evidence/author-722`
Exit 1 solely for finding 591f580cadb749294588. Four current-generator checks
pass; 17 complete source banks replay; 14 records preserve contrasts after
shared delivery; native grader accepts 7 correct and rejects 28 wrong choices.
Dependency/relocation checks and replacement mapping verification pass.

Status unsupported under the full delivery contract. No database, publication,
engine or runtime changes. The remaining finding explicitly requests the
separate inventory-remediation workflow, followed by fresh capture and strict
recheck. The Python generator cannot replace stored candidates in the selector;
verified in engine/rust/question_selection.rs:125-204. Do not weaken that check
or substitute hypothetical replacements for captured records.
Evidence: evidence/author-722/commands.json, results.json, inventory-results.json,
disposition.json and instructional-review.md. Reuse existing replacement proposal
at evidence/repair-3/inventory-repair-proposal.json for independent review.
