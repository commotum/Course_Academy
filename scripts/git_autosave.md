# Autosave recovery and batch pushes

The five-minute timer is still enabled and running. It invokes
`~/.local/bin/course-academy-autosave`, which runs `scripts/git_autosave.py`.
The service has an unlimited startup timeout; it is not being stopped by a
five-minute timeout.

On **October 11, 2026 at 08:39:45 PDT**, autosave had staged batch 2/21,
but `git commit` failed because `.git/index.lock` already existed. The previous
batch, commit `86f302fd3b`, had pushed successfully at 08:39:41. At 08:49:48,
autosave recovered the abandoned lock but then refused to continue because
changes remained staged. That guard repeated on later timer runs. The current
655 staged paths match the failed batch's path count. The journal does not
identify which competing process created the lock.

The journal also reports failures allocating inotify watches. Those warnings
did not prevent the service from starting. Disk space was available (637 GiB)
and filesystem inode use was 6% when inspected.

The October 13 dry run found roughly **870,000 worktree paths / 89.3 GiB**,
plus **655 staged paths / 64.4 MiB**. Capture workers are still producing files,
so these counts change. Default limits yield about **1,500 worktree batches**.
Four untracked manifest files are larger than 100 MiB.

Those two verified manifests have since been compacted into two activity-record
parts each, with small manifest indices. Their duplicated capture payloads and
`.previous` backups were removed after verifying that all 48 original capture
files matched. These four files no longer require Git LFS. Refresh the dry-run
report below for the current backlog.

## Inspect

Run from the repository root:

```bash
python3 scripts/git_autosave.py --repo . --dry-run --report .local/autosave-backlog.json
```

This reads Git state and writes the requested report. It does not change the
index or HEAD, recover locks, fetch, or push. Oversized paths are listed in the
report's `oversized` array.

## Start recovery

For an initial, bounded recovery run:

```bash
python3 scripts/git_autosave.py --repo . --resume-staged --max-batches 5 --budget-seconds 3600
```

To process the backlog for up to an hour instead, omit `--max-batches`:

```bash
python3 scripts/git_autosave.py --repo . --resume-staged --budget-seconds 3600
```

Use `--resume-staged` for the initial recovery of the reviewed staged backlog.
It preserves an index backup in `.git/autosave/index.before-recovery.*` and
records the approved staged blob IDs. Later runs automatically recognize and
resume their own pending staged blobs:

```bash
python3 scripts/git_autosave.py --repo . --budget-seconds 3600
```

The existing five-minute timer already points to the updated script. After the
initial recovery, subsequent timer runs can continue with its default
25-minute budget. The shared advisory lock prevents manual recovery and timer
runs from overlapping. No timer or service changes are required.

## Oversized files

GitHub blocks ordinary Git files larger than 100 MiB, and bounds each push at
2 GiB. The script leaves unconfigured oversized files local, reports them, and
returns status 1 while they remain. Splitting commits cannot make a single
oversized blob acceptable. These limits are documented in
[GitHub's file-size guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
and [repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).

Git LFS is installed on this machine. For oversized worktree files listed in a
fresh report, configure just those paths before starting recovery:

```bash
git lfs install --local
python3 - <<'PY'
import json
import subprocess
from pathlib import Path
report = json.loads(Path('.local/autosave-backlog.json').read_text())
for item in report['oversized']:
    if item['source'] == 'worktree':
        subprocess.run(['git', 'lfs', 'track', '--filename', item['path']], check=True)
PY
```

This writes `.gitattributes` and installs the local LFS hook. The batch script
recognizes `filter=lfs` paths, checks the actual staged pointer sizes, and
allows the LFS hook to upload their full contents. Review the resulting
`.gitattributes` before recovery. These configuration commands have not been
run against the working repository.

## Resume behavior and limits

- Each new chunk contains at most 2,000 paths or about 64 MiB of staged blobs.
  A permitted file larger than the byte budget gets its own chunk. Actual
  staged blob sizes are checked after staging, so a growing file cannot hide
  an oversized blob behind an earlier size estimate.
- Each chunk is committed and pushed before the next chunk. Pending local
  commits are pushed oldest first, one commit per request, before staging new
  content. A failed push retries the same commit up to three times, then stops.
- Commits use a private index, avoiding the normal index refresh lock that
  caused the original failure. The private index preserves cached file metadata
  so each chunk does not rehash the entire repository. The original index retains staged snapshots,
  deletions, and newer unstaged worktree edits correctly as HEAD advances.
- Failed commits leave a durable record of owned staged blobs. Unexpected
  staged changes stop the script for review. Existing unapproved staged
  changes require the explicit recovery flag.
- Capture workers may continue writing content. Avoid other processes that
  stage, commit, switch branches, or rewrite history during recovery. Recent
  or active index locks pause staging; verified abandoned locks are backed up.
- Remote divergence stops the script. It never force-pushes, rebases, resets
  the worktree, or rewrites existing history. A previously committed giant
  object or giant commit may still require a separate history repair.
- The time budget is checked between chunks. An in-progress Git operation may
  finish after the budget. `--push-timeout` defaults to 300 seconds per network
  operation; index writes are allowed to finish and clean up their locks.
- Chunking addresses request size and resumability. It does not guarantee that
  GitHub will accept an arbitrarily large repository or bypass LFS quotas.

Verified with temporary local bare remotes, including index-lock collision,
failed commit and push recovery, staged-versus-unstaged preservation, unusual
paths, deletion, remote divergence, LFS pointer filtering, oversized files,
and bounded continuation. Dry-run reports inspect the backlog without performing
commits or pushes. Live progress from the regular service is available with
`journalctl --user -u course-academy-autosave.service -f`.
