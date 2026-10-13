# Assessment weight implementation — 2026-10-11

User approved the five-piece proposal and instructed implementation.

The live policy now owns one assessment child, with initial 50/40/10 and
remedial 45/40/15. Transaction source is `:agent/gpt-6.1-sol-high`; committed
basis is 1179. Existing lesson/review child records and values were verified
unchanged at that exact basis. No new schema attributes or entity specs were
introduced. The existing six-weight spec and policy predicate were ensured.

The shared reader accepts assessments and exposes an explicit initial/remedial
phase API. Ordinary assessment assembly reads initial weights from the
synchronized policy snapshot and errors on missing assessment configuration.
Existing lesson/review count-based phases remain unchanged. Future retakes can
request the stored remedial distribution explicitly; their scheduling/builder,
topic-selection changes, and adaptive difficulty remain later work. Already
assembled quizzes keep their question sets.

Schema documentation and default seed were updated on the SSD and in the
workspace mirrors. The initialization seed was not rerun against the live DB.
Live updates must target existing child records rather than recreate anonymous
children through the seed.

Validation: 106 engine unit tests and 46 native API tests passed. Two optional
live integration tests remained ignored. The native tests cover required
remedial fields, both phases, changed database snapshots, frozen assembled
steps, and existing review/assessment behavior. The selection tests cover
updated distributions, ownership, duplicates, invalid totals, and unchanged
lesson/review phase cutoffs. Both live API endpoints returned basis 1179 after
the app-only deployment restart. Database and writer services were preserved.

The stock CLI preview lacks the application's native policy callback. The
preserved `preview.rs` uses the existing callback and exact speculative EDB
execution; its preview matched the committed scope and provenance.

Evidence: `intent.json`, `transaction.edn`, `preview.edn`, `receipt.edn`,
`after.edn`, `provenance.edn`, `verification.json`, and
`deployment-verification.json`. `commit.py` preserves and reconciles the
original request key, hash, source, and basis guard.
