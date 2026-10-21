# Repair state

Implemented: authored complete offset banks choose correct numeric rank before
coefficient sampling; no sign-extremum invariant. Fractional hard templates
accept and sample v=0. q-74691 complete source profile added with surviving-row
sign corrected. Valid bank collisions use an explicitly labelled whole-bank
fallback. Earlier source repairs retained. Runtime manifest trimmed to required
local files and pinned SymPy; repository-relative runtime lookup removed.

Validation milestone: original acceptance failures reproduced in
baseline-acceptance.json, now all pass. `checks/validate_repair.py` passes 157
printed-record checks, including 17 source banks, canonical replay, changed
profiles, zero roots and controlled counterfactuals. Native grader accepts 53
correct submissions and rejects 212 wrong submissions, none unresolved.
Shared delivery accepts 48/48 easy samples and 5/5 replacement batch records.
Historical inventory replay identifies the same five affected questions.
First six UI screenshots pass; easy and q-74691 screenshots visually inspected.

Completed: post-delivery probes preserve all five numeric ranks in both easy
sign groups (sign-extremum succeeds 16/48, formerly 48/48). Eight template pairs
change only b and update printed answers and actual grades. Sampler traces show
no bank rejection. Relocated CLI matches the five-record batch. Final native
grader: 74 accepted, 296 rejected, zero unresolved. Eleven UI cases rendered;
six screenshots inspected, including q-74691, relevant coefficient changes and
zero roots. All three declared retained regressions pass. Exact commands and
results: evidence/commands.json. Five historical affected records are listed in
affected-inventory.json with complete replay evidence; inventory remains unchanged.
No unfinished implementation or validation steps. Independent review is next.
