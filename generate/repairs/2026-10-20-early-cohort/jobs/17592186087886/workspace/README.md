This package repairs the legacy runtime closure and a displayed-equation grouping defect, but is **unsupported for handoff** because retained answer banks expose reliable answer-length shortcuts. See evidence/shortcut-regression.json and evidence/pedagogical-variation.json. The strict shortcut regression intentionally exits nonzero while this persists.

The seeded entry point is `17592186087886.py`; `package.json` declares its complete runtime closure and easy default band. It preserves all eight supplied source questions and complete banks, with a finite 48-task coefficient/argument domain. The seven-family candidate implementation was retained and extended only to restore the missing supplied q-90600 source. No images or database content were published or changed.

Reproduce from this workspace with `/home/jake/Developer/Course_Academy/.venv/bin/python`:

- `checks/check_package.py`: passing static closure, exact dependencies, isolated declared-files-only relocation, deterministic five-item CLI, immutable runtime files.
- `checks/validate_math.py`: passing eight exact source prompt/solution replays and complete banks, 48 independently parsed banks and all worked algebra stages, boundary rejection, eight stale-solution negative controls, relevant parameter changes and irrelevant ordering changes.
- `checks/check_shortcuts.py`: **failing** current-generator shortest-answer counterexample for all five fresh q-90600 parameter cases, after actual shared delivery filtering.
- `checks/check_inventory_shortcuts.py`: read-only replay audit; four original source records exhibit demonstrated family cues. Their original identities and original-source status are retained in the audit evidence.
- `checks/check_variation.py`: full before/after-delivery position/count/length probes; reports failures, and does not certify overall readiness.

`evidence/commands.md` records the shared native grader, delivery and UI renderer commands and outcomes. The four screenshots under evidence/render were visually inspected for grouped coefficients, nested functions, fraction legibility and the full worked solutions. Mathematical and rendering success do not override the failed shortcut check.

The directory `17592186087886/` also retains historical analyses and validation artifacts from basis 2418. Use the new instructional-account.md and evidence/ results for current claims; do not run the old database replenishment utility. Its runtime package is not declared, and it was not invoked in this repair.
