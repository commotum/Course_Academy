# Global database audit at basis 3291

This directory contains a read-only snapshot of all current tutorial content,
question prompts, existing worked solutions, and answer values. It also retains
source identities and ownership links to questions, KPs, and topics. No course
filter was applied and no database or generator was modified.

`summary.json` is the compact report. `affected-fields.csv` and
`affected-lessons.json` identify primary-source candidates and intervening
changes. The `secondary-` files keep broader source-structure predicates
separate. Candidate queues are evidence for contextual repair; they are not
global string-replacement instructions. Missing solutions remain deferred.

The global snapshot contains 449,174 content fields: 6,115 tutorials, 70,682
prompts, 55,934 existing worked solutions, and 316,443 answer values. Original
import comparison covers 139,520 fields from all 41 archived import files;
every archived file matches the original manifest's SHA-256. Their identities
all map to current entities. Later captured or generated content is included in
the snapshot but cannot be proven corrupt through original-import equality.

The primary queue requires all three conditions: a reviewed source witness of
the first-fragment extraction defect, an exact normalized mathematical-body
match inside the original imported field, and byte-for-byte equality between
that entire original field and the entire current field. Changed fields remain
review items, never presumed repaired. Source witnesses retain field positions
and source ordinals, including ambiguous repeated formulas.

## Reproduction

`export.rs` is a read-only native peer exporter derived from
`scripts/export_edb_snapshot.rs`. It explicitly fixes the database value to
basis 3291; `identity.json` records the database lineage. `build-command.json`
records the native build arguments and caches the executable under `.local/`.
The native JSONL preserves exact field strings and transaction/source
attribution. `native-compression.json` binds the losslessly compressed archive
to its uncompressed SHA-256. The earlier `snapshot.py`/`evidence` files retain
bounded CLI read probes; the complete export is the native archive.

From the repository root, the offline derivation is:

```sh
.venv/bin/python reference/mathacademy/repairs/2026-10-16-import-root-cause/database/analyze.py
.venv/bin/python reference/mathacademy/repairs/2026-10-16-import-root-cause/database/join_source.py
.venv/bin/python reference/mathacademy/repairs/2026-10-16-import-root-cause/database/join_source.py --secondary
.venv/bin/python reference/mathacademy/repairs/2026-10-16-import-root-cause/database/compress.py
```

The analyzer reads either `native.jsonl` or `native.jsonl.gz`. Source joining
likewise reads either plain or gzip-compressed baseline comparison. Large
derived snapshot files use `.gz`; `derived-compression.json` verifies their
uncompressed and compressed hashes. Candidate queues and reports remain plain
JSON/JSONL/CSV for review. The source stream hashes are bound separately in the
primary and secondary comparison summaries. Independent queue QA lives in the
parent repair's `review` directory.
