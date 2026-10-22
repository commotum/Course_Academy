# Author-424 outcome

The first executed test reproduced retained finding 591f580cadb749294588:
five historical v2 generated questions still carry the sign-only extreme-choice
shortcut. The retained possible learner-history scenario succeeds 64/64 times;
this is a witness, not a prediction of every learner history.

All four current-generator regressions pass. These check full source replay
(17 five-choice banks plus the canonical system), independently parsed systems,
zero roots, and finite batch contrasts before and after shared delivery filtering
(14 accepted records in three batches). Native grading accepts 7 independently
correct choices and rejects 28 incorrect choices. Exact dependencies,
determinism, and relocated execution pass. The previously generated UI screenshot
in evidence/repair-3/render/question-001.png was visually reinspected: equations,
choices, augmented matrices, row operation and solution are readable without
clipping. Rendering was reused because runtime files and representative records
are unchanged. The source tutorial classification flowchart was also inspected.

No runtime implementation change is justified by the latest finding. Current
banks assign the correct numeric rank before sampling coefficients; the CLI
selects a seed window with sign-subgroup contrasts. Both completed repairs are
preserved. Historical records instead come from archived v2 output. They remain
in the captured inventory because the learner selector reads stored records,
not this package. Changing source scope, generator filters, expected test
results, or captured data would conceal rather than repair that state.

The supplied finding explicitly requests a separate inventory-remediation
workflow. The existing one-to-one replacement proposal was verified against the
current generator and shared delivery output; it remains unapplied. The missing
step is external inventory remediation followed by a fresh capture and strict
recheck. Repeating author-only generator retries against the unchanged capture
cannot accomplish that step. Status remains unsupported because the required
stored-pool check fails, not because the source skill or easy generator is
unsupported. No database writes, publication, other-job edits, or source-file
changes were performed. All five finding declarations remain strict.

Commands and results: commands.json, results.json, initial-reproduction.json.
Historical records: ../generated-records.json.
Proposed external reconciliation: ../repair-3/inventory-repair-proposal.json.
