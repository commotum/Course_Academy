#!/usr/bin/env python3
"""Commit and push a repository in bounded, restartable batches."""

import argparse
from datetime import datetime
import fcntl
import os
from pathlib import Path
import subprocess
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--batch-files", type=int, default=2000)
    parser.add_argument("--batch-bytes", type=int, default=64 * 1024**2)
    parser.add_argument("--budget-seconds", type=int, default=25 * 60)
    args = parser.parse_args()
    if min(args.batch_files, args.batch_bytes, args.budget_seconds) <= 0:
        parser.error("batch limits and time budget must be positive")
    repo = args.repo.resolve()
    cache = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
    cache.mkdir(parents=True, exist_ok=True)
    os.environ["GIT_OPTIONAL_LOCKS"] = "0"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.environ.setdefault("GIT_SSH_COMMAND", "ssh -o BatchMode=yes")

    def log(message):
        print(message, flush=True)

    def git(*command, capture=False, check=True, timeout=None):
        return subprocess.run(
            ["git", "-c", "gc.auto=0", "-c", "maintenance.auto=false", *command],
            cwd=repo, capture_output=capture, check=check, timeout=timeout,
        )

    def git_path(name):
        path = Path(os.fsdecode(git("rev-parse", "--git-path", name, capture=True).stdout).strip())
        return path if path.is_absolute() else repo / path

    def blocked():
        for name in ("index.lock", "MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD",
                     "rebase-merge", "rebase-apply"):
            if git_path(name).exists():
                log(f"Autosave paused: {name} exists; no locks removed automatically.")
                return True
        return False

    def push():
        # A failed push ends the run. The next run pushes this commit first,
        # so a network outage never grows into one enormous pending push.
        git("push", timeout=300)

    with (cache / f"{repo.name.lower().replace('_', '-')}-autosave.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            log("Autosave is already running; skipping.")
            return 0
        started = time.monotonic()
        if blocked():
            return 1
        git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", capture=True)
        if git("symbolic-ref", "-q", "HEAD", capture=True, check=False).returncode:
            log("Autosave paused: HEAD is detached.")
            return 1
        if git("diff", "--cached", "--quiet", check=False).returncode:
            log("Autosave paused: existing staged changes need review before batching.")
            return 1
        push()

        # Save tracked edits first, then additions. NUL delimiters and literal
        # pathspecs keep spaces, newlines, and wildcard characters intact.
        tracked = git("ls-files", "--modified", "--deleted", "-z", capture=True).stdout
        added = git("ls-files", "--others", "--exclude-standard", "-z", capture=True).stdout
        tracked_paths = set(tracked.split(b"\0"))
        pending = list(dict.fromkeys(path for path in (tracked + added).split(b"\0") if path))
        log(f"Snapshot: {len(pending)} pending paths; batches of at most "
            f"{args.batch_files} paths / {args.batch_bytes / 1024**2:g} MiB "
            "(a larger permitted file gets its own batch).")
        batches = []
        batch = []
        size = 0
        oversized = []
        for path in pending:
            full_path = repo / os.fsdecode(path)
            try:
                file_size = full_path.lstat().st_size if not full_path.is_dir() else 0
            except FileNotFoundError:
                file_size = 0
            if file_size >= 100 * 1024**2:
                oversized.append(path)
                log(f"Skipped file requiring Git LFS: {os.fsdecode(path)!r} ({file_size} bytes)")
                continue
            if batch and (len(batch) >= args.batch_files or size + file_size > args.batch_bytes):
                batches.append((batch, size))
                batch, size = [], 0
            batch.append(path)
            size += file_size
        if batch:
            batches.append((batch, size))

        saved = 0
        vanished = 0
        for number, (paths, byte_count) in enumerate(batches, 1):
            if time.monotonic() - started >= args.budget_seconds:
                log(f"Time budget reached between batches; {saved} paths saved. Next run resumes.")
                return 1 if oversized else 0
            if blocked():
                return 1
            if git("diff", "--cached", "--quiet", check=False).returncode:
                log("Autosave paused: another process staged changes between batches.")
                return 1
            log(f"Batch {number}/{len(batches)}: {len(paths)} paths, {byte_count / 1024**2:.1f} MiB.")
            # Capture workers remove temporary, untracked files while we run.
            # Missing tracked files must stay in the batch to save deletions.
            def still_pending(candidates):
                return [path for path in candidates
                        if path in tracked_paths or os.path.lexists(repo / os.fsdecode(path))]

            current_paths = still_pending(paths)
            vanished += len(paths) - len(current_paths)
            # Do not impose a hard timeout on an index-writing command. Git
            # must finish or clean up its own lock before the service exits.
            while current_paths:
                with tempfile.NamedTemporaryFile(prefix="autosave-paths-", dir=cache) as pathspec:
                    pathspec.write(b"\0".join(current_paths) + b"\0")
                    pathspec.flush()
                    try:
                        git("--literal-pathspecs", "add", "-A", f"--pathspec-from-file={pathspec.name}",
                            "--pathspec-file-nul")
                        break
                    except subprocess.CalledProcessError:
                        remaining = still_pending(current_paths)
                        if remaining == current_paths:
                            raise
                        vanished += len(current_paths) - len(remaining)
                        log("Temporary files vanished during staging; retrying surviving paths.")
                        current_paths = remaining
            if not current_paths:
                log("All untracked paths in this batch vanished; skipping.")
                continue
            result = git("diff", "--cached", "--quiet", check=False).returncode
            if result == 0:
                log("No remaining changes in this batch.")
                continue
            if result != 1:
                raise RuntimeError("Could not inspect staged changes")
            stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
            git("commit", "--quiet", "-m", f"autosave: {stamp} (batch {number}/{len(batches)})")
            revision = git("rev-parse", "--short", "HEAD", capture=True).stdout.decode().strip()
            push()
            saved += len(current_paths)
            log(f"Pushed {revision}; {saved}/{len(pending)} snapshot paths processed.")
        log(f"Snapshot complete: {saved} paths processed; {vanished} vanished temporary paths; "
            f"{len(oversized)} oversized files skipped.")
        return 1 if oversized else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError, RuntimeError) as error:
        print(f"Autosave stopped: {error}. Completed pushes are preserved; next run retries.", flush=True)
        raise SystemExit(1)
