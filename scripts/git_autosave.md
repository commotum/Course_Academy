# Autosave recovery and batch pushes

## October 21 diagnosis

The last successful timer push was `e970b7e901` on October 17 at 15:42 PDT.
The next `git add` returned an error for the ignored embedded preview repository
`reference/edb-math/repairs/2026-10-17-triangular-generator/activity/native/preview`.
Despite the error, Git had staged 402 other paths (46.3 MiB). Autosave exited
before saving ownership of those blobs, so every later run stopped with
“Existing staged changes need review.” This was a partial staging failure,
not an authentication failure or the timer being disabled.

Staging now happens in a temporary index. Paths that vanish or become ignored
are removed before retrying. Before publishing a successful index, autosave
acquires Git's normal index lock, verifies that HEAD and the original index
have not changed, and records the exact staged blob IDs. It then atomically
replaces the index. Failed staging leaves the real index untouched. An
interruption after publication leaves a batch the next run can recognize.
Unexpected manual staging still stops autosave for review.

Ignore checks run only for untracked candidates with `git check-ignore
--no-index`. A live probe of 200 paths completed in 5 ms with that option;
the default index-aware check exceeded the three-second probe timeout and
the service's first such check had already spent over a minute on CPU.
Tracked files remain eligible even when they match an ignore rule.

The October 21 inventory found 1,121,682 worktree paths (134.84 GiB), plus the
stranded staged batch. This included 38 untracked capture manifests totaling
4.27 GiB that exceeded the ordinary Git blob limit. At the user's request,
those exact paths are now ignored in the root `.gitignore` and remain local.
No files were deleted or converted to LFS. Capture workers can change these
counts while recovery runs.

## Automatic operation

The checked-in units are in `scripts/systemd/course-academy-autosave.*`.
The service invokes `scripts/git_autosave.py` directly. Install or refresh them
from the repository root:

```bash
install -m 644 scripts/systemd/course-academy-autosave.service scripts/systemd/course-academy-autosave.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now course-academy-autosave.timer
systemctl --user restart course-academy-autosave.timer
systemctl --user start --no-block course-academy-autosave.service
```

The timer starts one minute after activation and resumes five minutes after
the service finishes. `OnUnitInactiveSec` schedules from completion, including
when a backlog run takes longer than five minutes. Each service run works for
about 25 minutes, checking its budget between chunks. Index writes can finish
after the budget; the service has no startup timeout.

- New chunks contain at most 2,000 paths or approximately 64 MiB of staged
  blobs. A permitted single file larger than that budget gets its own chunk.
  Actual staged sizes are checked again after filtering/staging.
- Each chunk is committed and pushed before the next. Previously committed
  local history is pushed oldest first, one commit per request. Failed pushes
  retry the same commit up to three times, with a 300-second timeout per
  network operation. The next run retries any remaining local commit first.
- A shared advisory lock prevents manual recovery and timer runs overlapping.
  Commits also use a private index so a concurrent status refresh cannot
  derail them. Other processes must not stage, commit, or switch branches
  during autosave; detected index or HEAD changes stop the run safely.
- Remote divergence stops the script. It never force-pushes, rebases, or
  rewrites existing history. Splitting an already committed giant object
  requires separate history repair.
- New oversized files are skipped and reported while other chunks continue.
  Add exact ignore rules if those files should remain local. Ignoring a path
  does not remove it if it is already tracked.

GitHub enforces a [2 GB push limit](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits)
and [blocks ordinary files above 100 MiB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
Chunking bounds individual transfers; the full backlog still takes time to
upload and increases the remote repository's size.

## Inspect progress

```bash
journalctl --user -u course-academy-autosave.service -f
systemctl --user list-timers course-academy-autosave.timer
python3 scripts/git_autosave.py --repo . --dry-run --report .local/autosave-backlog.json
```

Dry run writes the optional report without changing the index or HEAD,
recovering locks, fetching, or pushing. Inventorying a million paths can take
several minutes. The report's `oversized` array identifies files requiring
separate handling; ignored files are excluded.

## Manual bounded recovery

```bash
python3 scripts/git_autosave.py --repo . --max-batches 5 --budget-seconds 3600
```

To approve a reviewed, stranded staged batch once, add `--resume-staged`.
This backs up the original index in `.git/autosave/index.before-recovery.*`
and records its exact blob IDs before committing it in bounded chunks.
Later runs resume owned batches without that flag. Recent or active index
locks pause work; verified abandoned locks are preserved before recovery.

## Verification

```bash
python3 -m unittest discover -s tests -p test_git_autosave.py -v
```

Integration tests use real temporary bare remotes to cover partial `git add`
failure, ignore-rule races, concurrent staging, commit/push retry, preservation
of staged versions and newer worktree edits, deletions, unusual paths, remote
divergence, LFS filtering, oversized files, index-lock collisions, and bounded
continuation.
