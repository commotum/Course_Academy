The current generator's four retained construction and batch regressions pass.
Source replay covers all 17 practice banks; shared delivery preserves the tested
contrasts on 14 records. Native grading accepts 7 correct choices and rejects
28 wrong choices. Relocation and pinned dependency checks pass. Runtime files,
manifest, source and inventory match the protected bindings. Existing actual-UI
screenshot evidence/repair-3/render/question-001.png was visually reinspected;
equations, choices and worked solution are legible without visible clipping.

Finding 591f580cadb749294588 remains a failure: the exact inventory regression
reproduces five stored historical banks and the 64/64 possible-history shortcut.
All non-source inventory records were tested. Source questions are not tagged
as generated. The finding expressly requests a separate inventory-remediation
workflow; question_selection.rs selects stored entity candidates without calling
this Python package. No workspace generator edit can change those stored banks.
The latest feedback establishes no additional construction defect.

The five replacement records and mapping in
evidence/repair-3/inventory-repair-proposal.json remain verified and unapplied.
The next state-changing action is independent review and application of that
proposal, followed by fresh inventory capture. The user's prohibition on database
changes prevents that action here. Do not weaken the regression or substitute
the proposed pool for captured inventory. Further author retries with these
unchanged inputs cannot resolve this criterion.

Current commands and results: commands.json and results.json alongside this file.
The initial direct command was job Python -B checks/batch_regressions.py --finding
inventory (exit 1); checks/recheck_status.py --output evidence/author-976 then
reran all five retained findings and the affected verification (exit 1 solely
for the historical pool). No runtime, engine, publication or database changes
were made. Status remains unsupported for the delivered historical pool.
