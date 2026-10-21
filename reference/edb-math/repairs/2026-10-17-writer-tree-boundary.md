# Writer connection failures from an outdated EDB library

The study app intermittently returned
`transport/unavailable: No such file or directory (os error 2)` because the
writer removed `/tmp/edb-math/writer.sock` while exiting after repeated background
indexing failures. PostgreSQL continued accepting connections. The writer's
automatic restart counter reached 120 during diagnosis.

The underlying failure was `tree/unapplied-edit`. A directory's first leaf used
its own narrower routing key rather than inheriting the directory's sparse lower
bound. An edit could fall inside the directory's range but outside every leaf
range. The working EDB checkout already corrected this in both ordinary merging
and no-history pair discovery in `src/index/tree/mod.rs`.

The EDB release library was dated October 11, before the October 14 source fix.
The installed writer was built October 16, but still linked that older library.
Rebuilding the writer alone had therefore not incorporated the fix.

## Repair and checks

- An isolated snapshot with the original committed tree implementation failed
  `merge_first_leaf_inherits_sparse_parent_range` with the same error.
- With the existing source fix, the EDB unit suite passed: 60 passed, 3 ignored
  because they require disposable PostgreSQL catalogs. The regression covers all
  six index orders in current and history modes.
- Both native writer lifecycle tests passed.
- Rebuilt the EDB release library, rebuilt the Course Academy writer, atomically
  installed it, and restarted only `course-academy-writer.service` at
  22:36:51 PDT on October 17.
- The writer completed its background indexing job at basis 3803. Inspection at
  22:38:51 showed index basis advancing from 2944 to 3803, index lag falling from
  859 to zero, and zero reported shallow inspection problems. The service had
  zero automatic restarts after installation.
- `/api/profile` and `/api/activity` returned HTTP 200 with valid JSON.

The previous executable is retained at
`/media/jake/SSD/EDB/math/bin/course-academy-transactor.before-tree-fix-20261017`.
Installation hashes and observation records are in `.local/edb-build/`.

Use `bash scripts/build_local_edb_writer.sh` for future rebuilds. It checks EDB
source through Cargo before linking the writer. Installation commands are in
the project README.
