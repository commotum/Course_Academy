"""Exercise restart and index preservation against real temporary Git repositories."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/git_autosave.py'
spec = importlib.util.spec_from_file_location('git_autosave', SCRIPT)
autosave = importlib.util.module_from_spec(spec)
spec.loader.exec_module(autosave)


class AutosaveTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / 'work'
        self.remote = self.root / 'remote.git'
        self.env = dict(os.environ, XDG_CACHE_HOME=str(self.root / 'cache'),
                        GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
        for key in ('GIT_INDEX_FILE', 'GIT_DIR', 'GIT_WORK_TREE'):
            self.env.pop(key, None)
        subprocess.run(['git', 'init', '--bare', '-q', str(self.remote)], check=True, env=self.env)
        subprocess.run(['git', 'init', '-q', '-b', 'master', str(self.repo)], check=True, env=self.env)
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        (self.repo / 'original').write_text('base\n')
        (self.repo / 'deleted').write_text('delete me\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'initial')
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '-qu', 'origin', 'master')
        self.base = self.git('rev-parse', 'HEAD')

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, env=self.env).decode().strip()

    def run_script(self, *args, expected=0, env=None):
        result = subprocess.run(['python3', str(SCRIPT), '--repo', str(self.repo),
                                 '--push-attempts', '1', *args], env=env or self.env,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def remote_head(self):
        return subprocess.check_output(['git', '--git-dir', str(self.remote), 'rev-parse', 'master']).decode().strip()

    def git_wrapper(self, body):
        """Inject races/failures at the actual Git subprocess boundary."""
        directory = self.root / 'bin'
        directory.mkdir()
        real_git = subprocess.check_output(['which', 'git']).decode().strip()
        wrapper = directory / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport os,sys,subprocess\nfrom pathlib import Path\n'
                           f'real_git={real_git!r}\nargs=sys.argv[1:]\n' + body +
                           '\nos.execv(real_git, [real_git,*args])\n')
        wrapper.chmod(0o755)
        return dict(self.env, PATH=str(directory) + os.pathsep + self.env['PATH'])

    def test_partial_git_add_failure_does_not_strand_shared_index(self):
        for name in ('a', 'b'):
            (self.repo / name).write_text(name)
        original_index = (self.repo / '.git/index').read_bytes()
        env = self.git_wrapper(
            'if "add" in args:\n'
            ' subprocess.run([real_git,"add","a"], check=True)\n'
            ' sys.exit(1)\n')
        self.run_script(env=env, expected=1)
        self.assertEqual((self.repo / '.git/index').read_bytes(), original_index)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
        self.assertEqual(self.remote_head(), self.base)
        self.run_script()
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertEqual(self.remote_head(), self.git('rev-parse', 'HEAD'))

    def test_ignore_rule_change_during_add_retries_without_force_adding(self):
        for name in ('a', 'ignored'):
            (self.repo / name).write_text(name)
        env = self.git_wrapper(
            'if "add" in args and not Path(".gitignore").exists():\n'
            ' Path(".gitignore").write_text("ignored\\n")\n')
        result = self.run_script(env=env)
        self.assertIn('became ignored', result.stdout)
        self.assertEqual(self.git('ls-tree', '--name-only', 'HEAD', 'ignored'), '')
        self.assertEqual(self.git('show', 'HEAD:a'), 'a')
        self.run_script()
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_concurrent_staging_is_not_replaced(self):
        (self.repo / 'a').write_text('autosave')
        env = self.git_wrapper(
            'if "add" in args:\n'
            ' Path("external").write_text("manual staging")\n'
            ' env=os.environ.copy(); env.pop("GIT_INDEX_FILE",None)\n'
            ' subprocess.run([real_git,"add","external"],env=env,check=True)\n')
        self.run_script(env=env, expected=1)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'external')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertFalse((self.repo / '.git/index.lock').exists())
        self.run_script(expected=1)

    def test_dry_run_does_not_mutate_index_or_head_or_recover_lock(self):
        (self.repo / 'new').write_text('new')
        self.git('add', 'new')
        index = (self.repo / '.git/index').read_bytes()
        lock = self.repo / '.git/index.lock'
        lock.write_text('leave this alone')
        self.run_script('--dry-run', '--report', str(self.root / 'report.json'))
        self.assertEqual(index, (self.repo / '.git/index').read_bytes())
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertEqual(lock.read_text(), 'leave this alone')
        self.assertFalse((self.repo / '.git/autosave').exists())
        self.assertFalse((self.root / 'cache').exists())
        self.assertEqual(json.loads((self.root / 'report.json').read_text())['staged_paths'], 1)

    def test_unapproved_stage_is_left_alone(self):
        (self.repo / 'new').write_text('new')
        self.git('add', 'new')
        index = (self.repo / '.git/index').read_bytes()
        self.run_script(expected=1)
        self.assertEqual(index, (self.repo / '.git/index').read_bytes())
        self.assertEqual(self.remote_head(), self.base)

    def test_staged_recovery_preserves_staged_version_deletion_and_unstaged_edit(self):
        (self.repo / 'original').write_text('staged\n')
        (self.repo / 'deleted').unlink()
        (self.repo / 'space [x]\nfile').write_text('unusual path')
        self.git('add', '-A')
        staged_index = (self.repo / '.git/index').read_bytes()
        (self.repo / 'original').write_text('newer worktree\n')
        self.run_script('--resume-staged', '--batch-files', '1', '--max-batches', '3')
        self.assertEqual(self.git('show', 'HEAD:original'), 'staged')
        self.assertEqual((self.repo / 'original').read_text(), 'newer worktree\n')
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
        self.assertEqual(self.remote_head(), self.git('rev-parse', 'HEAD'))
        backup = next((self.repo / '.git/autosave').glob('index.before-recovery.*'))
        self.assertEqual(backup.read_bytes(), staged_index)
        self.run_script('--batch-files', '1')
        self.assertEqual(self.git('show', 'HEAD:original'), 'newer worktree')

    def test_partial_staged_recovery_resumes_without_explicit_flag(self):
        for name in ('a', 'b', 'c'):
            (self.repo / name).write_text(name)
        self.git('add', '-A')
        self.run_script('--resume-staged', '--batch-files', '1', '--max-batches', '1')
        self.assertEqual(len(self.git('diff', '--cached', '--name-only').splitlines()), 2)
        self.run_script('--batch-files', '1')
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertEqual(self.git('rev-list', '--count', f'{self.base}..HEAD'), '3')

    def test_worktree_chunks_push_each_commit_and_resume(self):
        for name in ('a', 'b', 'c'):
            (self.repo / name).write_bytes(b'x' * 7)
        self.run_script('--batch-bytes', '10', '--max-batches', '1')
        self.assertEqual(self.remote_head(), self.git('rev-parse', 'HEAD'))
        self.assertEqual(self.git('rev-list', '--count', f'{self.base}..HEAD'), '1')
        self.run_script('--batch-bytes', '10')
        self.assertEqual(self.git('rev-list', '--count', f'{self.base}..HEAD'), '3')
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_failed_push_is_retried_before_another_commit_is_created(self):
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        for name in ('a', 'b'):
            (self.repo / name).write_text(name)
        self.run_script('--batch-files', '1', expected=1)
        pending = self.git('rev-parse', 'HEAD')
        self.assertNotEqual(pending, self.base)
        self.assertEqual(self.remote_head(), self.base)
        hook.unlink()
        self.run_script('--batch-files', '1', '--max-batches', '1')
        self.assertEqual(self.remote_head(), pending)
        self.assertEqual(self.git('rev-parse', 'HEAD'), pending)
        self.run_script('--batch-files', '1')
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_failed_commit_leaves_owned_stage_for_automatic_retry(self):
        hook = self.repo / '.git/hooks/pre-commit'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        (self.repo / 'new').write_text('new')
        self.run_script(expected=1)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'new')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        hook.unlink()
        self.run_script()
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertEqual(self.remote_head(), self.git('rev-parse', 'HEAD'))

    def test_existing_history_is_pushed_one_commit_at_a_time(self):
        revisions = []
        for name in ('a', 'b', 'c'):
            (self.repo / name).write_text(name)
            self.git('add', name)
            self.git('commit', '-qm', name)
            revisions.append(self.git('rev-parse', 'HEAD'))
        self.run_script('--max-batches', '2')
        self.assertEqual(self.remote_head(), revisions[1])
        self.assertEqual(self.git('rev-parse', 'HEAD'), revisions[2])
        self.run_script()
        self.assertEqual(self.remote_head(), revisions[2])

    def test_lfs_tracked_large_file_is_staged_as_pointer(self):
        # A small clean filter models LFS without requiring network or LFS storage.
        self.git('config', 'filter.lfs.clean', 'python3 -c "import sys; sys.stdin.buffer.read(); print(\'pointer\')"')
        self.git('config', 'filter.lfs.smudge', 'cat')
        (self.repo / '.gitattributes').write_text('large filter=lfs\n')
        with (self.repo / 'large').open('wb') as output:
            output.truncate(autosave.MAX_FILE_BYTES)
        self.run_script()
        self.assertEqual(self.git('show', 'HEAD:large'), 'pointer')
        self.assertEqual((self.repo / 'large').stat().st_size, autosave.MAX_FILE_BYTES)

    def test_external_stage_invalidates_autosave_ownership(self):
        for name in ('a', 'b'):
            (self.repo / name).write_text(name)
        self.git('add', '-A')
        self.run_script('--resume-staged', '--batch-files', '1', '--max-batches', '1')
        (self.repo / 'external').write_text('manual change')
        self.git('add', 'external')
        self.run_script(expected=1)
        self.assertEqual(self.git('rev-list', '--count', f'{self.base}..HEAD'), '1')

    def test_oversized_worktree_file_stays_local_while_other_files_push(self):
        large = self.repo / 'large'
        with large.open('wb') as output:
            output.truncate(autosave.MAX_FILE_BYTES)
        (self.repo / 'small').write_text('okay')
        self.run_script(expected=1)
        self.assertEqual(self.git('show', 'HEAD:small'), 'okay')
        self.assertEqual(self.git('status', '--porcelain'), '?? large')

    def test_remote_divergence_stops_without_committing(self):
        clone = self.root / 'other'
        subprocess.run(['git', 'clone', '-q', str(self.remote), str(clone)], check=True, env=self.env)
        subprocess.run(['git', '-C', str(clone), '-c', 'user.name=Other', '-c', 'user.email=other@example.invalid',
                        'commit', '--allow-empty', '-qm', 'remote update'], check=True, env=self.env)
        subprocess.run(['git', '-C', str(clone), 'push', '-q'], check=True, env=self.env)
        (self.repo / 'local').write_text('pending')
        self.run_script(expected=1)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_normal_index_lock_during_commit_does_not_block_private_index(self):
        wrapper_dir = self.root / 'bin'
        wrapper_dir.mkdir()
        real_git = subprocess.check_output(['which', 'git']).decode().strip()
        wrapper = wrapper_dir / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport os,sys,subprocess\nfrom pathlib import Path\n'
                           'args=sys.argv[1:]\nlock=Path.cwd()/".git/index.lock"\n'
                           'collision="commit" in args\n'
                           'if collision: lock.write_text("simulated concurrent status")\n'
                           f'if collision: (Path.cwd()/".git/stat-cache").write_bytes(subprocess.check_output([{real_git!r},"ls-files","--debug","original"]))\n'
                           f'try: result=subprocess.run([{real_git!r},*args])\n'
                           'finally:\n if collision: lock.unlink()\n'
                           'sys.exit(result.returncode)\n')
        wrapper.chmod(0o755)
        (self.repo / 'new').write_text('new')
        env = dict(self.env, PATH=str(wrapper_dir) + os.pathsep + self.env['PATH'])
        self.run_script(env=env)
        self.assertNotIn('mtime: 0:0', (self.repo / '.git/stat-cache').read_text())
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertEqual(self.remote_head(), self.git('rev-parse', 'HEAD'))


if __name__ == '__main__':
    unittest.main()
