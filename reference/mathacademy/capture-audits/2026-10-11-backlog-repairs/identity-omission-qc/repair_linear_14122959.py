"""Finite authored-only source repair for one completed, inactive lesson."""
import argparse
import hashlib
from pathlib import Path
import sys
import shutil
import threading

REPO = Path(__file__).resolve().parents[5]
ARCHIVE = REPO / 'reference/mathacademy/capture-audits/2026-10-11-completeness-repairs'
sys.path.insert(0, str(ARCHIVE))
import run_later_repairs as driver
from playwright.sync_api import sync_playwright
from scripts.config import Config
from scripts.database.pipeline import DatabasePipeline
from scripts.storage import atomic_json, read_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    directory = REPO / 'reference/mathacademy/capture/linear/14122959'
    config = Config(account='linear', solver_model='gpt-6.1-sol', codex_bin=str(ARCHIVE / 'archived-codex'))
    protected = [directory / 'checkpoint.json', directory / 'capture-complete.json']
    protected += [config.state_root / name for name in ('xp.json', 'daily-xp.json', 'retakes.json')
                  if (config.state_root / name).is_file()]
    if not args.apply:
        protected += [directory / 'content.json', directory / 'history-content.json']
    before = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
    if (directory / 'database/request.json').exists():
        raise ValueError('An immutable request must resolve before source revision')
    if read_json(directory / 'database/result.json', {}).get('status') not in ('verified', 'no_changes'):
        raise ValueError('Only a completed terminal import can receive this repair')
    active = read_json(config.state_root / 'active.json', {}) or {}
    if active.get('directory') == str(directory):
        raise ValueError('Do not repair an active capture')
    # Shared source fixes can advance the version between preview and apply.
    # Reuse only the archive driver's hash-checked authored request cache.
    repair = directory / 'repairs' / ('completeness-' + driver.recovery.version()[:16])
    if args.apply and not (repair / 'solver/session.json').exists():
        prepared = read_json(Path(__file__).parent / 'linear-14122959-prepared.json', {})
        seed = Path(prepared.get('repair', '/not-a-prepared-repair')) / 'solver'
        if seed.is_dir() and list(seed.glob('*-restriction.json')) and seed.parent != repair:
            shutil.copytree(seed, repair / 'solver', dirs_exist_ok=True)
            session = read_json(repair / 'solver/session.json', {})
            session['session_id'] = None
            session['generation'] = session.get('generation', 0) + 1
            session.pop('topic_catalog', None)
            atomic_json(repair / 'solver/session.json', session)
            atomic_json(repair / 'solver/active-process.json', {})
            atomic_json(repair / 'solver-cache-seed.json', {'from': str(seed),
                'cache_policy': 'Exact hash-validated authored-only requests; changed source reviewed afresh'})
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        context.route('**/*', lambda route: route.abort())
        try:
            outcome = driver.recovery.reprocess(config, directory, context.new_page(), apply=args.apply)
        finally:
            context.close()
            browser.close()
    after = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
    if before != after:
        raise ValueError('Protected original capture or learner ledger changed')
    outcome['protected_originals'] = before
    if args.apply and outcome['status'] == 'verified':
        outcome['repeat_preview'] = DatabasePipeline(config, threading.Event()).process(directory, apply=False)
        if outcome['repeat_preview']['status'] != 'no_changes':
            raise ValueError('Verified source revision did not produce a no-op repeat preview')
    atomic_json(Path(__file__).parent / ('linear-14122959-applied.json' if args.apply else 'linear-14122959-prepared.json'), outcome)
    print(outcome, flush=True)


if __name__ == '__main__':
    main()
