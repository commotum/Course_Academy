# Reciprocal integration with logarithmic constants

Pure generator: `../17592186105720.py --difficulty moderate|hard --count 5 --seed 0 --format json|markdown`.

Run `.venv/bin/python generate/scratch/17592186105720/validate.py` from the repository root to replay five supported complete source banks and exhaust all 79 profile/parameter cases. `check-engine` reuses the existing application's in-memory `learning::grade_field` harness; it performs no database operations. Mathematical correctness is checked independently of ID-selection grading. `review.md` shows originals, replays and changed-parameter variants side by side.

`replenish.py` reuses the configured EDB reader, contributor, native predicates and durable request integration. It acquires the application's `api.lock`, checks the current basis and lineage, excludes retained presentations and reservations, validates stock, deduplicates tasks, checks new UUIDs, previews exact EDN, saves the request, submits with a basis guard and verifies exact-basis readback while holding the lock. Unknown receipts are recovered under the original request key. Only this KP's additive generated content and generator registration can appear in the transaction datoms; all originals and learner history are preserved.

`capabilities.json` documents excluded source profiles, unsupported easy, finite limits and sampling policy. Requests, previews, receipts and verification are retained in `reference/replenishment/`; the requested job result records the verified outcome and explicit exceptions. A fresh native inventory read remains separate from the mathematically validated pool because legacy source defects are intentionally preserved.
