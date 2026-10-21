#!/usr/bin/env python3
"""Commit and push a repository in bounded, restartable batches."""

import argparse
from datetime import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import tempfile
import time


MAX_FILE_BYTES = 100 * 1024**2


def staged_entries(git):
    """Read exact staged blobs, without rename detection or index refresh."""
    fields = git("diff", "--cached", "--raw", "--no-renames", "--no-abbrev", "-z",
                 capture=True).stdout.split(b"\0")
    entries = []
    for metadata, path in zip(fields[0::2], fields[1::2]):
        if not metadata:
            continue
        _, mode, _, oid, status = metadata.split()
        if status == b"U":
            raise RuntimeError("Unmerged index entries need manual resolution")
        entries.append((path, mode, oid))
    objects = list(dict.fromkeys(oid for _, mode, oid in entries if mode not in (b"000000", b"160000")))
    sizes = {}
    if objects:
        result = git("cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)",
                     capture=True, input=b"\n".join(objects) + b"\n")
        for line in result.stdout.splitlines():
            oid, kind, size = line.split()
            if kind != b"blob":
                raise RuntimeError("Staged file does not point to a blob")
            sizes[oid] = int(size)
    return [(path, mode, oid, sizes.get(oid, 0)) for path, mode, oid in entries]


def batches_for(items, max_files, max_bytes):
    """Items end with their byte count; permitted large files stand alone."""
    batch, size = [], 0
    for item in items:
        if batch and (len(batch) >= max_files or size + item[-1] > max_bytes):
            yield batch, size
            batch, size = [], 0
        batch.append(item)
        size += item[-1]
    if batch:
        yield batch, size


def entry_records(entries):
    return {os.fsdecode(path): [mode.decode(), oid.decode()] for path, mode, oid, _ in entries}


def file_digest(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.digest()


def recover_stale_index_lock(index_lock, repo, cache, log):
    """Preserve an abandoned lock only after checking its age and ownership."""
    try:
        before = index_lock.lstat()
    except FileNotFoundError:
        return True
    if (not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid()
            or time.time() - before.st_mtime < 10 * 60):
        return False
    # fuser catches open descriptors held by Git and by other applications.
    holders = subprocess.run(["fuser", str(index_lock)], capture_output=True)
    if holders.returncode != 1 or holders.stdout.strip():
        return False
    # A Git process can briefly close the descriptor before renaming the lock.
    # Keep the lock if any Git command is still operating in this repository.
    for process in Path("/proc").iterdir():
        if not process.name.isdigit():
            continue
        try:
            if process.stat().st_uid != os.getuid():
                continue
            arguments = (process / "cmdline").read_bytes().split(b"\0")
            if not arguments or os.path.basename(os.fsdecode(arguments[0])) != "git":
                continue
            cwd = (process / "cwd").resolve(strict=True)
            if cwd == repo or repo in cwd.parents:
                return False
            # Also recognize Git invoked from elsewhere with -C/--git-dir,
            # or an explicit GIT_DIR / GIT_WORK_TREE / GIT_INDEX_FILE.
            if any(os.fsencode(str(repo)) in argument for argument in arguments[1:]):
                return False
            environment = (process / "environ").read_bytes().split(b"\0")
            for entry in environment:
                key, separator, value = entry.partition(b"=")
                if separator and key in {b"GIT_DIR", b"GIT_WORK_TREE", b"GIT_INDEX_FILE"}:
                    target = Path(os.fsdecode(value))
                    if not target.is_absolute():
                        target = cwd / target
                    target = target.resolve()
                    if target == repo or repo in target.parents:
                        return False
        except (FileNotFoundError, ProcessLookupError):
            continue
        except OSError:
            # Unreadable process state cannot establish that recovery is safe.
            return False
    try:
        after = index_lock.lstat()
    except FileNotFoundError:
        return True
    if ((before.st_ino, before.st_mtime_ns, before.st_ctime_ns, before.st_size)
            != (after.st_ino, after.st_mtime_ns, after.st_ctime_ns, after.st_size)):
        return False
    backups = cache / f"{repo.name.lower().replace('_', '-')}-autosave-repair"
    backups.mkdir(parents=True, exist_ok=True)
    backup = backups / f"index.lock.{time.time_ns()}"
    index_lock.rename(backup)
    log(f"Recovered unused index.lock older than 10 minutes; preserved at {backup}.")
    return True



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--batch-files', type=int, default=2000)
    parser.add_argument('--batch-bytes', type=int, default=64 * 1024**2)
    parser.add_argument('--budget-seconds', type=int, default=25 * 60)
    parser.add_argument('--max-batches', type=int, help='Stop after this many successful pushes')
    parser.add_argument('--push-timeout', type=int, default=300)
    parser.add_argument('--push-attempts', type=int, default=3)
    parser.add_argument('--resume-staged', action='store_true',
                        help='Explicitly approve recovery of existing staged blobs, in chunks')
    parser.add_argument('--dry-run', action='store_true',
                        help='Inspect backlog without changing Git state or contacting the remote')
    parser.add_argument('--report', type=Path, help='Write a JSON backlog report (also with --dry-run)')
    args = parser.parse_args()
    if min(args.batch_files, args.batch_bytes, args.budget_seconds,
           args.push_timeout, args.push_attempts) <= 0 or (args.max_batches is not None and args.max_batches <= 0):
        parser.error('limits and time budget must be positive')
    if args.batch_bytes > 512 * 1024**2:
        parser.error('batch-bytes must be at most 512 MiB to leave headroom below the GitHub push limit')
    repo = args.repo.resolve()
    cache = Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache')))
    os.environ['GIT_OPTIONAL_LOCKS'] = '0'
    os.environ['GIT_TERMINAL_PROMPT'] = '0'
    os.environ.setdefault('GIT_SSH_COMMAND', 'ssh -o BatchMode=yes -o ConnectTimeout=30')

    def log(message):
        print(message, flush=True)

    def git(*command, capture=False, check=True, timeout=None, input=None, index=None):
        env = os.environ.copy()
        if index is not None:
            env['GIT_INDEX_FILE'] = str(index)
        invocation = ['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', *command]
        process = subprocess.Popen(invocation, cwd=repo, env=env, start_new_session=True,
                                   stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,
                                   stdout=subprocess.PIPE if capture else None,
                                   stderr=subprocess.PIPE if capture else None)
        try:
            stdout, stderr = process.communicate(input=input, timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            raise
        result = subprocess.CompletedProcess(invocation, process.returncode, stdout, stderr)
        if check and result.returncode:
            if stderr:
                log(os.fsdecode(stderr).rstrip())
            raise subprocess.CalledProcessError(result.returncode, invocation, stdout, stderr)
        return result

    def git_path(name):
        path = Path(os.fsdecode(git('rev-parse', '--git-path', name, capture=True).stdout).strip())
        return path if path.is_absolute() else repo / path

    index_path = git_path('index')
    state_dir = git_path('autosave')
    state_file = state_dir / 'staged.json'

    def head():
        return git('rev-parse', 'HEAD', capture=True).stdout.decode().strip()

    def blocked():
        for name in ('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply'):
            if git_path(name).exists():
                log(f'Autosave paused: {name} exists.')
                return True
        index_lock = git_path('index.lock')
        if index_lock.exists() and not recover_stale_index_lock(index_lock, repo, cache, log):
            log('Autosave paused: index.lock is recent, in use, or cannot be verified as abandoned.')
            return True
        if git('ls-files', '--unmerged', '-z', capture=True).stdout:
            raise RuntimeError('Unmerged entries need manual resolution')
        return False

    def save_owner(entries):
        state_dir.mkdir(parents=True, exist_ok=True)
        temporary = state_file.with_suffix('.tmp')
        with temporary.open('w') as output:
            json.dump({'head': head(), 'entries': entry_records(entries)}, output)
            output.flush()
            os.fsync(output.fileno())
        temporary.replace(state_file)

    def owns(entries):
        if not state_file.exists():
            return False
        owner = json.loads(state_file.read_text())
        if git('merge-base', '--is-ancestor', owner['head'], 'HEAD', check=False).returncode:
            return False
        approved = owner['entries']
        return all(approved.get(path) == value for path, value in entry_records(entries).items())

    def inventory():
        tracked = git('ls-files', '--modified', '--deleted', '-z', capture=True).stdout
        added = git('ls-files', '--others', '--exclude-standard', '-z', capture=True).stdout
        tracked_paths = set(tracked.split(b'\0'))
        pending = list(dict.fromkeys(p for p in (tracked + added).split(b'\0') if p))
        items, oversized, large_candidates = [], [], []
        for path in pending:
            full_path = repo / os.fsdecode(path)
            try:
                info = full_path.lstat()
                # Git stores symlink targets, not the target file's contents.
                size = info.st_size if not stat.S_ISDIR(info.st_mode) else 0
            except FileNotFoundError:
                size = 0
            if size >= MAX_FILE_BYTES:
                large_candidates.append((path, size))
            else:
                items.append((path, size))
        lfs_bytes = 0
        if large_candidates:
            attributes = git('check-attr', '-z', 'filter', '--stdin', capture=True,
                             input=b'\0'.join(p for p, _ in large_candidates) + b'\0').stdout.split(b'\0')
            lfs_paths = {path for path, _, value in zip(attributes[0::3], attributes[1::3], attributes[2::3])
                         if value == b'lfs'}
            for path, size in large_candidates:
                if path in lfs_paths:
                    # The clean filter stores a small pointer in the Git pack;
                    # the LFS pre-push hook uploads the full object separately.
                    items.append((path, 256))
                    lfs_bytes += size
                else:
                    oversized.append({'path': os.fsdecode(path), 'bytes': size, 'source': 'worktree'})
        entries = staged_entries(git)
        for path, _, _, size in entries:
            if size >= MAX_FILE_BYTES:
                oversized.append({'path': os.fsdecode(path), 'bytes': size, 'source': 'index'})
        report = {
            'head': head(), 'staged_paths': len(entries),
            'staged_bytes': sum(e[-1] for e in entries),
            'worktree_paths': len(pending), 'worktree_bytes': sum(i[-1] for i in items)
                + sum(i['bytes'] for i in oversized if i['source'] == 'worktree')
                + lfs_bytes - 256 * len(lfs_paths if large_candidates else ()),
            'lfs_worktree_bytes': lfs_bytes,
            'worktree_batches': sum(1 for _ in batches_for(items, args.batch_files, args.batch_bytes)),
            'batch_files': args.batch_files, 'batch_bytes': args.batch_bytes,
            'oversized': oversized, 'index_lock_present': git_path('index.lock').exists(),
        }
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + '\n')
        log(f"Backlog: {report['staged_paths']} staged paths ({report['staged_bytes'] / 1024**2:.1f} MiB); "
            f"{len(pending)} worktree paths ({report['worktree_bytes'] / 1024**3:.2f} GiB), "
            f"approximately {report['worktree_batches']} worktree batches.")
        for item in oversized:
            log(f"Needs Git LFS or separate storage: {item['path']!r} ({item['bytes']} bytes, {item['source']}).")
        return entries, items, tracked_paths, oversized

    if args.dry_run:
        inventory()
        log('Dry run only: no commits, index changes, lock recovery, fetches, or pushes performed.')
        return 0

    cache.mkdir(parents=True, exist_ok=True)
    with (cache / f"{repo.name.lower().replace('_', '-')}-autosave.lock").open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            log('Autosave is already running; skipping.')
            return 0
        state_dir.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        pushed = 0

        def limit_reached():
            return (time.monotonic() - started >= args.budget_seconds
                    or (args.max_batches is not None and pushed >= args.max_batches))

        if blocked():
            return 1
        branch_result = git('symbolic-ref', '-q', '--short', 'HEAD', capture=True, check=False)
        if branch_result.returncode:
            raise RuntimeError('HEAD is detached')
        branch = branch_result.stdout.decode().strip()
        remote = git('config', '--get', f'branch.{branch}.remote', capture=True).stdout.decode().strip()
        remote_ref = git('config', '--get', f'branch.{branch}.merge', capture=True).stdout.decode().strip()
        upstream = git('rev-parse', '--symbolic-full-name', '@{u}', capture=True).stdout.decode().strip()
        if not remote_ref.startswith('refs/heads/') or remote == '.':
            raise RuntimeError('Autosave requires an upstream branch on a remote repository')
        entries = staged_entries(git)
        if entries and not (args.resume_staged or owns(entries)):
            raise RuntimeError('Existing staged changes need review; use --dry-run, then --resume-staged to recover them')
        if entries and args.resume_staged:
            state_dir.mkdir(parents=True, exist_ok=True)
            backup = state_dir / f'index.before-recovery.{time.time_ns()}'
            shutil.copy2(index_path, backup)
            save_owner(entries)
            log(f'Preserved the original staged index at {backup}.')

        # Refresh the actual remote tip; never force-push or automatically merge.
        git('fetch', '--no-tags', remote, f'{remote_ref}:{upstream}', timeout=args.push_timeout)
        if git('merge-base', '--is-ancestor', upstream, 'HEAD', check=False).returncode:
            raise RuntimeError('Remote branch is ahead or diverged; reconcile it manually before autosaving')

        def push(revision):
            nonlocal pushed
            for attempt in range(1, args.push_attempts + 1):
                try:
                    git('push', '--porcelain', remote, f'{revision}:{remote_ref}', timeout=args.push_timeout)
                    pushed += 1
                    log(f'Pushed {revision[:12]}; {pushed} push checkpoints this run.')
                    return
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    if attempt == args.push_attempts:
                        raise
                    log(f'Push attempt {attempt} failed; retrying the same commit in 5 seconds.')
                    time.sleep(5)

        # Push previously committed history in order before creating anything else.
        # One existing giant commit cannot be split without rewriting history.
        pending_commits = git('rev-list', '--first-parent', '--reverse', f'{upstream}..HEAD', capture=True).stdout.splitlines()
        for revision in pending_commits:
            if limit_reached():
                log('Run limit reached; rerun to continue from the last successful push.')
                return 0
            push(revision.decode())

        def drain_staged():
            """Commit subsets of the real index using a private index; leave its blobs intact."""
            nonlocal entries
            entries = staged_entries(git)
            if not entries:
                state_file.unlink(missing_ok=True)
                return True
            if not owns(entries):
                raise RuntimeError('Staged contents changed outside autosave; review before continuing')
            permitted = [entry for entry in entries if entry[-1] < MAX_FILE_BYTES]
            for batch, byte_count in batches_for(permitted, args.batch_files, args.batch_bytes):
                if limit_reached():
                    log('Run limit reached between batches; rerun to resume.')
                    return False
                current = staged_entries(git)
                if not owns(current):
                    raise RuntimeError('Another process changed staged contents; stopping')
                current_records = entry_records(current)
                if any(current_records.get(os.fsdecode(p)) != [m.decode(), o.decode()] for p, m, o, _ in batch):
                    raise RuntimeError('Another process committed or changed this staged batch; stopping')
                base = head()
                log(f'Committing {len(batch)} staged paths, {byte_count / 1024**2:.1f} MiB.')
                with tempfile.TemporaryDirectory(prefix='commit-', dir=state_dir) as directory:
                    private_index = Path(directory) / 'index'
                    # Preserve cached file metadata for unchanged tracked files.
                    # A fresh read-tree makes commit rehash the entire worktree.
                    shutil.copy2(index_path, private_index)
                    git('read-tree', '--reset', base, index=private_index)
                    records = b''.join(mode + b' ' + oid + b'\t' + path + b'\0'
                                       for path, mode, oid, _ in batch)
                    git('update-index', '-z', '--index-info', input=records, index=private_index)
                    if head() != base:
                        raise RuntimeError('HEAD changed during batch preparation; stopping')
                    stamp = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %z')
                    # git commit refreshes only the private index. A status scan
                    # holding the normal index.lock cannot derail this commit.
                    git('commit', '--quiet', '-m', f'autosave: {stamp} (chunk {pushed + 1})', index=private_index)
                push(head())
            entries = staged_entries(git)
            if entries:
                for path, _, _, size in entries:
                    log(f'Uncommitted oversized staged blob: {os.fsdecode(path)!r} ({size} bytes).')
                return False
            state_file.unlink(missing_ok=True)
            return True

        if not drain_staged():
            return 1 if any(e[-1] >= MAX_FILE_BYTES for e in entries) else 0
        if limit_reached():
            log('Run limit reached; next run resumes from the remaining worktree changes.')
            return 0
        entries, items, tracked_paths, oversized = inventory()
        vanished = 0
        for batch, byte_count in batches_for(items, args.batch_files, args.batch_bytes):
            if limit_reached():
                log('Run limit reached; next run resumes from the remaining worktree changes.')
                return 1 if oversized else 0
            if blocked():
                return 1
            if staged_entries(git):
                raise RuntimeError('Another process staged changes; stopping')
            paths = [path for path, _ in batch]

            def surviving(candidates):
                # Ignore rules can change after inventory, including rules for
                # embedded repositories. Never force-add an ignored path.
                result = git('check-ignore', '-z', '--stdin', capture=True, check=False,
                             input=b'\0'.join(candidates) + b'\0')
                if result.returncode not in (0, 1):
                    raise RuntimeError('Cannot inspect ignore rules; retry on the next run')
                ignored = set(result.stdout.split(b'\0'))
                return [p for p in candidates if p not in ignored
                        and (p in tracked_paths or os.path.lexists(repo / os.fsdecode(p)))]

            current_paths = surviving(paths)
            vanished += len(paths) - len(current_paths)
            log(f'Staging {len(current_paths)} paths, estimated {byte_count / 1024**2:.1f} MiB.')
            # git add can update the index even when it exits with an error.
            # Prepare in isolation, then record exact blob ownership BEFORE
            # atomically publishing the index. Failures leave the real index
            # untouched; interruption after publication is safely resumable.
            with tempfile.TemporaryDirectory(prefix='stage-', dir=state_dir) as directory:
                private_index = Path(directory) / 'index'
                base = head()
                shutil.copy2(index_path, private_index)
                original_digest = file_digest(private_index)
                private_git = lambda *a, **kw: git(*a, **kw, index=private_index)
                if staged_entries(private_git):
                    raise RuntimeError('Another process staged changes during preparation; stopping')
                while current_paths:
                    with tempfile.NamedTemporaryFile(prefix='paths-', dir=state_dir) as pathspec:
                        pathspec.write(b'\0'.join(current_paths) + b'\0')
                        pathspec.flush()
                        try:
                            private_git('--literal-pathspecs', 'add', '-A',
                                        f'--pathspec-from-file={pathspec.name}', '--pathspec-file-nul')
                            break
                        except subprocess.CalledProcessError:
                            remaining = surviving(current_paths)
                            if remaining == current_paths:
                                raise
                            vanished += len(current_paths) - len(remaining)
                            log('Paths vanished or became ignored during staging; retrying surviving paths.')
                            current_paths = remaining
                if not current_paths:
                    continue
                entries = staged_entries(private_git)
                expected_paths = set(current_paths)
                if any(entry[0] not in expected_paths for entry in entries):
                    raise RuntimeError('Unexpected staged paths in private index; stopping')
                if not entries:
                    continue
                index_lock = git_path('index.lock')
                # O_EXCL respects every other Git writer. Compare the full index
                # while holding the lock so no concurrent staging gets replaced.
                with index_lock.open('xb') as output:
                    try:
                        if head() != base or file_digest(index_path) != original_digest:
                            raise RuntimeError('HEAD or index changed during staging; retry on the next run')
                        save_owner(entries)
                        with private_index.open('rb') as source:
                            shutil.copyfileobj(source, output)
                        output.flush()
                        os.fsync(output.fileno())
                        index_lock.replace(index_path)
                    finally:
                        index_lock.unlink(missing_ok=True)
            if not drain_staged():
                return 1 if any(e[-1] >= MAX_FILE_BYTES for e in entries) else 0
        log(f'Snapshot complete; {vanished} vanished paths; {len(oversized)} oversized files remain local.')
        return 1 if oversized else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError, RuntimeError, ValueError) as error:
        print(f'Autosave stopped: {error}. Completed commits and pushes are preserved; rerun to retry.', flush=True)
        raise SystemExit(1)
