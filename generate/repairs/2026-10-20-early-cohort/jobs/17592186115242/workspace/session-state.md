# Current state

Completed generator repairs, manifest, all five strict finding checks, and the
unapplied five-record replacement proposal are preserved. No runtime, database,
engine, source, publication or image changes in this pass.

Latest verification: evidence/repair-320/commands.json, results.json and outcome.md.
Command: job Python -B checks/recheck_status.py --output evidence/repair-320.
The first executed check reproduced the inventory failure (exit 1): five historical
banks; 64/64 successes in the retained possible-history witness. Four generator
regressions pass. Source replay, shared delivery (14/14), counterfactual checks,
native grading (7 accepted, 28 rejected), dependencies, relocation and proposal
hash bindings pass. Existing rendering evidence is retained without rerendering.
Affected-inventory references resolve relative to author-320.

Next unfinished action is separate inventory remediation using
 evidence/repair-3/inventory-repair-proposal.json, followed by fresh inventory
capture and the strict regression. Database changes are prohibited here. Do not
weaken tests, substitute hypothetical inventory, or repeat unchanged author passes.
Current status: unsupported.
