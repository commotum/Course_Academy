# Current state — 2026-10-22, author-182

Preserved the repaired runtime and manifest byte for byte. Read feedback, both retained findings, history, prior state, required generator documentation and the existing instructional account. No new generator defect was demonstrated; no instructional or runtime change is justified by the evidence-only finding.

Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1. Installed `scripts/generator_pipeline.py:723` rejects the byte-identical package before retained regressions or sampling, despite the latest independent finding requesting an evidence-only correction.

Affected checks rerun using the pinned Python with `-B`:

- `checks/check_evidence_contract.py`: exit 1 solely at installed handoff. The corrected evidence bundle passes actual review validation, two relocated roots and negative controls. Current records, 12 source captures and three reproduced generated inventory records bind.
- `checks/check_batch_selection.py`: exit 0. The reported pivot/rank shortcut succeeds 1/5 before and after delivery; the historical 5/5 failure remains a negative control. Ten profiles and five answer roles are checked. Five delivered records and 25 native grading responses pass.

Commands, logs, results and unchanged runtime hashes: `evidence/author182-verification.json`. Visually reinspected retained actual-UI screenshot `evidence/author8-render/question-001.png`; readable matrices, choices and solution with no visible clipping. No new render was run because runtime is unchanged. Fresh CLI relocation, deterministic replay, count limits and ten complete source-bank replay checks pass. Retained UI inputs match the fresh delivered endpoints; earlier rendering evidence remains retained.

The strict failing regression remains registered in `repair-regressions.json`. The uninstalled correction is `runner-fix/evidence-only-rejection.patch`; the corrected historical evidence is staged at `evidence/contract-correction` with `evidence/contract-installation.json`. Neither historical acceptance nor a staged patch proves current independent approval or installation.

Next unfinished action belongs to the runner owner: review/apply the staged runner correction outside this workspace, then rerun installed handoff and retained regressions before sampling and fresh independent review. Workspace-only authorization prohibits that runner edit and external evidence installation. No external writes, publication, database writes or engine edits occurred. Repeating authoring with unchanged permissions cannot resolve this blocker; changing runtime bytes solely to evade its identity gate would not repair it.
