#!/usr/bin/env python3
"""Reject ordinary staged blobs that cannot be pushed to GitHub."""
import os
from pathlib import Path
import subprocess
import sys

from git_autosave import MAX_FILE_BYTES, staged_entries


def oversized(repo=None, limit=MAX_FILE_BYTES):
    def git(*args, capture=False, input=None):
        return subprocess.run(['git',*args],cwd=repo,input=input,capture_output=capture,check=True)
    return [(os.fsdecode(path),size)for path,mode,oid,size in staged_entries(git)if size>=limit]


def main():
    large=oversized()
    for path,size in large:
        print(f'Cannot commit {path}: staged blob is {size/1024**2:.2f} MiB (limit: below 100 MiB).',file=sys.stderr)
    if large:
        print('Compress generated exports, keep them outside Git, or configure Git LFS before staging.',file=sys.stderr)
    return bool(large)


if __name__=='__main__':sys.exit(main())
