# Repair result

The seeded entry point now emits a raw JSON array and accepts `--difficulty easy --count 5 --seed 0 --format json`, runs from a relocated runtime-only package, and produces five deliverable questions. Runtime dependencies are Python 3.13.5 and SymPy 1.14.0. The manifest bundles the entry point, source snapshot, shared math-format helper, captured-inventory fingerprints and pinned requirements only.

The reported CLI failure was reproduced before editing (`evidence/before-cli.json`). The repair history has an empty findings array and two events; the first is identified by code `legacy_packaging_or_sampling`; that event code is used in `repair-regressions.json`. Its executable suite also retains the concrete shortcut and source-ambiguity checks discovered during this repair.

New sampling preserves the source Gaussian-elimination stages and five-choice radio contracts. It chooses the decisive second-row result first, constructs the supplied RHS from it, and derives every displayed matrix and solution from that system. All choices use the same normalized coefficient block, and all offered matrix/point pairs are internally consistent. The ordered bank stays fixed across controlled target changes. Exact captured banks remain audit-only source replays. The two newly supplied complete sources are included. Revised banks do not count an already stored mathematical system as new practice.

Fidelity: all 10 complete supplied banks replay exactly (50 choices, 40 distractors), including the independently reproduced q-10512 ambiguity. Its original source is preserved, while normal generation supports its coefficient family with an unambiguous bank. The two unrated incomplete captures remain evidence, without invented difficulty, keys or solutions.

Correctness: the existing independent readback validator checks printed matrices, exact linear systems, every row operation, unique complete choice objects, and the displayed back-substitution arithmetic. The current suite passes 81 generated cases covering all profiles, all five target roles, and scale boundaries (71 semantic instances).

Grading: one native-grader batch passes 405 responses (81 accepted, 324 rejected). A second batch checks 50 responses on actual delivery-normalized records (10 accepted, 40 rejected). No unresolved grading cases or engine changes.

Variation and delivery: shared filtering accepts 29/33 easy and 42/48 moderate test records; the ten skipped records are deliberate duplicate choice permutations. All five target outcomes survive every profile. The full normal catalogs retain 64 easy and 83 moderate semantic systems after captured-inventory exclusion, with every target rank still present. The exact five-question runner sample passes 5/5 delivery checks and has no stored-system overlap under an independent parsed-row witness. Live learner history and configured selection weights were not accessed. Read-only inspection of question_selection.rs establishes that configured selection uses difficulty then fresh candidates, without a content-rank filter.

Rendering: `evidence/render-records.json` is byte-content equivalent as JSON to the renderer's saved input. All four easy profiles were rendered in the unmodified learning UI; the final screenshots were visually inspected. Matrices, augmentation bars, row operations, choices, braces and solution conclusions are readable, with no exposed TeX, overflow or stale values.

Inventory: all three stored generated instances were reproduced with exact archived generation metadata and IDs. Two exhibit the unique-consistency shortcut; one exhibits a fixed-median shortcut throughout its supported scale family. Stored matrix display-wrapper migrations were explicitly reproduced and independently checked as the same mathematical objects. See `affected-inventory.json` and `evidence/inventory-generated-records.json`. Its evidence_path entries are relative to the job's supplied author-2 evidence root (`../workspace/...`) so every written artifact remains in the authorized workspace. Twelve original captures are recorded separately and never marked generated. Nothing was published or written to the database.

Run from this workspace with the job's Python:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python checks/check_all.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

`check_all.py` invokes the source/CLI/mathematical/native suite, actual shared delivery filtering plus shortcut checks, and stored-inventory reproduction. Full delivery commands are saved in `evidence/delivery-variation.json`; native inputs and outputs are retained. Earlier material under `17592186059775/reference` and the old review files is historical evidence, excluded from the runtime package. This report and the current evidence supersede their older coverage claims.

Limits: finite source-coefficient families, bounded numerical constants, no claim about transfer to arbitrary matrices, no hard band, and inventory exclusion fixed at captured basis 5461. Canonical/source replay is an audit interface and preserves known source errors; it is not the normal sampling path. Publication and independent approval remain the runner's responsibility.

## Latest targeted continuation (2026-10-22)

The latest count failure was reproduced before implementation. `--difficulty easy --count 5 --seed 0 --format json` returned `{"instances": [...]}`. The runner decodes only raw arrays, `records`, `questions`, or one `question`; it therefore obtained no records. The earlier test accepted `instances` directly, so its passing result did not establish runner compatibility. This supersedes that earlier CLI-contract claim.

The runtime change is one line: emit the batch as a raw array. Mathematical construction, source coverage, bank repairs and semantic-inventory exclusion are preserved. The relocated strict CLI test runs with the runner's `-E -s -B` flags and decoding rules, requires exact zero/one/five counts, checks both supported bands, deterministic five-record output, unique IDs and difficulty, unchanged runtime files, and explicit finite-limit failure. The existing registered suite now starts with that check. History has no named findings; the existing first-event code remains the registration ID and covers both packaging events.

Commands executed from this workspace using `/home/jake/Developer/Course_Academy/.venv/bin/python`:

```sh
python checks/check_cli_contract.py
python checks/check_all.py
python 17592186059775.py --difficulty easy --count 5 --seed 0 --format json
python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/continuation-render-records.json --output evidence/continuation-render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

Evidence: `evidence/latest-failure-reproduced.log` records the strict pre-fix failure; `evidence/before-retained-regressions.log` records the earlier suite passing despite it; `evidence/cli-contract.json` records the corrected runner-contract checks; `evidence/after-registered-regressions.log` records the full passing registered suite. The suite rechecked ten complete source banks, 81 mathematical readbacks / 405 native responses, 50 delivered native responses, all five target ranks per profile before and after delivery, five of five requested CLI records delivered, and all three stored generated instances reproduced. `evidence/latest-cli-records.json` matches the current runner sample. Both new shared-UI screenshots in `evidence/continuation-render/` were visually inspected: no exposed TeX, clipping, stale values or unreadable math.

No engine, database, publication or other-job edits. Finite limits remain 64 easy and 83 moderate semantic instances against captured basis 5461. Live inventory and learner-history selection remain untested.
