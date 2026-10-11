# Prepared learner-history migration

Status: prepared and validated in memory; **not committed**. The user requires an explicit go-ahead before any database transaction. The application changes are also not activated in the running service.

The source is `course-academy-v2` at basis 2892. The proposed destination is `math` at basis 252. The transaction uses `:application/ca-engine` (17592186407927) as the source of every new fact. `intent.json` records the exact transaction digest, retry key, and destination basis guard.

The import contains:

- 1,041 topic-progress records, including sparse imported baseline records without invented retention state.
- Four completed and six paused lesson attempts, with all 88 presentation records and their ordering/continuation markers.
- 44 saved responses and the original 40 correct / 4 incorrect outcomes. Historical outcomes are not regraded.
- 8,344.367 working seconds and 37 earned XP.
- The original overall performance totals; the old selected course if the destination still has none.
- Six original baseline topic entities missing from the destination, and the original FIRe policy and its two question-selection weight records (the destination has no policy).

`supplemental-mapping.json` documents reconciliation of changed question, field, and answer identities. There are 24 question mappings by verified Math Academy identity and equivalent problem text. Selected answer choices use the corresponding current-field choices; seven formula changes are presentation-only, and image replacements have matching file hashes. Seven learner-entered blank answers are retained verbatim. Two absent historical answer fields and their 13 choices are restored so their saved responses remain readable. The supplemental transaction is in `supplemental.edn`.

All 16 explicit progress instants and saved task/item durations are retained. Original start/pause/resume/completion timestamps are archived in `old/status-history.edn` (506 assertion/retraction rows), but destination lifecycle timestamps will be the import time. The runtime timing change recognizes imported paused/terminal histories and uses the saved duration as a checkpoint, then adds new working time when resumed. No synthetic starts are added and no schema changes are proposed.

The old paused assignment and untouched locked/unlocked task queue are excluded. The 470 request journals are neither replayed nor deleted.

`application-preview.json`, when present with `status: passed`, records the in-memory application preview: schema predicates, engine attribution, lesson rendering, saved responses, durations, and speculative resumes. It does not represent a commit. The importer refuses to apply without a successful preview matching the transaction digest and prepared destination basis. A changed destination requires a refreshed preparation and preview before submission.

After the user's go-ahead, activate the tested application changes, submit the guarded transaction, and verify every imported attribute from the committed snapshot. Until then, do not run the importer's `apply` action.
