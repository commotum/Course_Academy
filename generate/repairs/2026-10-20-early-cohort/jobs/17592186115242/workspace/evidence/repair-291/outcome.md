# Author result

Status: unsupported. The generator's four retained construction/source/batch
regressions pass; the historical-inventory regression remains failing.

The latest reproduction verifies all five complete historical records against
the supplied inventory and reproduces 64/64 sign-only shortcut successes in the
retained possible learner-history scenario. See initial-reproduction.json and
../repair-2/inventory-results.json. These are captured inventory claims; live
learner history and current database state are not available in this task.

The retained recheck passes 17 practice source banks and canonical replay,
zero-root reachability, fractional bare-k elimination, conditional numeric-rank
and position probes, relevant/irrelevant counterfactuals, shared delivery (14/14),
native grading (7 correct accepted, 28 wrong rejected), exact dependency versions,
and relocated execution. Commands and complete results are in commands.json and
results.json. The verified replacement mapping remains in
../repair-3/inventory-repair-proposal.json. The candidate and protected captured
inputs have unchanged hashes, so retained rendering remains applicable;
../repair-3/render/question-002.png was visually inspected again.

The family-wide construction fixes already exist: independent correct numeric
rank/spacing, collision fallback preserving valid zero roots, the q-74691 source
profile, and finite easy-batch selection retaining sign-group contrasts. No new
runtime defect was demonstrated. The unresolved cause is old stored banks:
engine/rust/question_selection.rs selects candidate entities from snapshots and
does not invoke this Python generator to replace their answers. Changing the
generator cannot alter those stored entities. Runtime/source-family narrowing,
editing the captured inventory, or weakening the regression would conceal the
failure rather than repair it.

Finding 591f580cadb749294588 explicitly requires the separate inventory-remediation
workflow. Apply the staged proposal only through that authorized workflow, then
capture fresh inventory and rerun the retained strict check. Database changes are
prohibited here. No database content, engine files, or published images changed.
