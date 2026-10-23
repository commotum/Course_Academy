# Author results

Fidelity: all 12 complete easy source profiles reproduce their equations, complete five-choice banks and correct vector. Restored q-20450; removed its stray equals sign. q-20451 has no supplied correct link or solution and remains an explicitly incomplete source. No diagram evidence or generated assets are needed.

Correctness: `checks/math_witness.py` parses visible equations and vectors and solves them independently with exact arithmetic. It checks the unique correct bank member and every displayed substitution equality for 143 records: 12 source replays, 60 controlled variants, 60 normal samples and 11 concrete/legacy counterexamples. No generator metadata is used as mathematical ground truth.

Grading: the real native learner engine passed 715 answer-ID submissions: 143 correct choices accepted and 572 incorrect choices rejected, with no unresolved outcomes. Every option in each controlled bank is tested both as a correct response and as a distractor under changed RHSs.

Decision variation: 12 recognizable coefficient/notation profiles each have one identical visible bank supporting five different answers under controlled RHS changes. All 60 survive actual delivery normalization/deduplication. A deterministic bank-only sign/equality/extremum/tie/count/position rule therefore cannot exceed 1/5 on any controlled group; this subsumes all review bank-only rules. The two exact old banks at scales 4 and 3 are retained as five-role counterfactuals as well. Irrelevant seed changes with explicit mathematical controls preserve the whole question. A small normal-stream sample tests five seeds per profile; its observed positions are 0, 1 and 3 (not a claim of exhaustive random-seed coverage). Constructor controls exercise every eligible role, and the code samples all five uniformly without role-dependent rejection.

Delivery: controlled 60/60, normal 60/60, candidate batch 5/5 survive; each surviving system is semantically distinct within its input. Generation rejects unsupported difficulties and invalid scales/counts, and CLI deduplication uses the system fingerprint rather than UUID or seed. No target-dependent validity rejection occurs: invertible coordinate transforms preserve five distinct vectors and the unit-triangular matrix makes exactly one of them correct. There is no balance quota. Selector source inspection is recorded separately; live learner histories and weighting policies were not supplied.

Rendering: visually inspected all four `render-final/question-00N.png` screenshots. They cover restored q-20450 replay and a signed variant, q-129453 with a changed correct role, and a fractional angle-vector variant. Equations, controls, fractions and full solutions are legible. Initial screenshots showed horizontal clipping in long substitution lines despite a passing DOM report; splitting substituted equations and solved equalities into separate displays fixed it.

Packaging: only entrypoint, adjacent source JSON and pinned requirements are runtime files. Exact installed versions match the manifest; deterministic five-record generation and relocation passed. No runtime imports from the repository, database operations, image publication or writes to another job are needed.

Inventory: all 13 supplied inventory records at basis 5578 are original source IDs, with no generated metadata. No historical generated records exist in this captured inventory to test or repair. `affected-inventory.json` is empty for this verified reason, not because the inventory was untested. No claim about later live inventory is made.

Both retained generator findings have executable regressions in `repair-regressions.json`. No independent-review approval or publication is claimed.
