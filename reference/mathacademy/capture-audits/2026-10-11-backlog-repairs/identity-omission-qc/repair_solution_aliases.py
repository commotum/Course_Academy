"""Finite own-original PNG source repairs; no live browser/profile actions."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import threading
from urllib.parse import urljoin

REPO = Path(__file__).resolve().parents[5]
ARCHIVE = REPO / 'reference/mathacademy/capture-audits/2026-10-11-completeness-repairs'
sys.path.insert(0, str(ARCHIVE))
import run_later_repairs as driver
from playwright.sync_api import sync_playwright
from scripts.browser.adapter import EXTRACT
from scripts.browser.assets import solution_image_bindings
from scripts.config import Config
from scripts.database.pipeline import DatabasePipeline
from scripts.storage import atomic_json, file_lock, read_json

TARGETS = {'14122998': ('differential', 'q-181771'), '14123192': ('multivariable', 'q-226134')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=TARGETS)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--proof-only', action='store_true')
    args = parser.parse_args()
    account, question_id = TARGETS[args.task]
    directory = REPO / 'reference/mathacademy/capture' / account / args.task
    config = Config(account=account, solver_model='gpt-6.1-sol', codex_bin=str(ARCHIVE / 'archived-codex'))
    protected = [directory / name for name in ('checkpoint.json', 'capture-complete.json', 'browser-state.json')]
    if not args.apply:
        protected += [directory / name for name in ('content.json', 'history-content.json')]
    before = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
    active = read_json(config.state_root / 'active.json', {}) or {}
    if active.get('directory') == str(directory):
        raise ValueError('Never repair an active capture')
    if (directory / 'database/request.json').exists():
        raise ValueError('An existing immutable request must resolve separately before source revision')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        context.route('**/*', lambda route: route.abort())
        try:
            page = context.new_page()
            records = list((directory / 'observations').glob('history-solution-' + question_id + '-*.json'))
            if len(records) != 1:
                raise ValueError('Require a unique own saved solution source')
            saved = read_json(records[0])
            markup = saved['html']
            page.set_content(markup)
            node = page.locator('[id=' + json.dumps(saved['dom_id']) + ']')
            if node.count() != 1 or saved['dom_id'] != 'questionExplanation-' + question_id[2:]:
                raise ValueError('Original owning source root differs')
            parsed = node.evaluate(EXTRACT)
            for asset in parsed['assets']:
                if asset.get('source_url'):
                    asset['source_url'] = urljoin(saved.get('source_url') or 'https://mathacademy.com/', asset['source_url'])
                if not any(old.get('source_url') == asset.get('source_url') and old.get('tag') == asset['tag']
                           for old in saved.get('assets', [])):
                    raise ValueError('Fresh alias source URL differs from its original saved binding')
            prior = read_json(directory / 'browser-state.json')['live_records'][question_id]
            bindings = solution_image_bindings(parsed, prior)
            if not bindings or len(bindings) != len(parsed['assets']) or parsed['errors']:
                raise ValueError('Every own solution asset must have a verified original binding')
            proof = {'question_id': question_id, 'source_file': str(records[0]),
                'source_dom_id': parsed['dom_id'], 'source_html_sha256': hashlib.sha256(markup.encode()).hexdigest(),
                'prior_dom_id': prior.get('dom_id'), 'prior_question_id': prior.get('math_academy_id'),
                'bindings': [{'failed_alias_url': next(a['source_url'] for a in parsed['assets'] if a['index'] == index),
                             'original_source_url': original.get('source_url'),
                             'validation': original['original_image_validation']} for index, original in bindings.items()]}
            atomic_json(Path(__file__).parent / (args.task + '-alias-proof.json'), proof)
            pipeline = DatabasePipeline(config, threading.Event())
            if args.proof_only:
                outcome = {'status': 'source_proven', 'task_id': args.task,
                           'statement': 'Source-only proof; package and saved-order outbox remain unchanged'}
            else:
                if read_json(directory / 'database/result.json', {}).get('status') not in ('verified', 'no_changes'):
                    raise ValueError('The original pending package must first reach a normal terminal import')
                outcome = driver.recovery.reprocess(config, directory, page, apply=args.apply)
                if args.apply and outcome['status'] == 'verified':
                    with file_lock(config.database_lock):
                        outcome['repeat_preview'] = pipeline.process(directory, apply=False)
                    if outcome['repeat_preview']['status'] != 'no_changes':
                        raise ValueError('Verified source repair did not repeat as a no-op')
            after = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
            if before != after:
                raise ValueError('Protected original capture source changed')
            outcome['protected_originals'] = before
            outcome['question_id'] = question_id
            action = 'proof-only' if args.proof_only else 'applied' if args.apply else 'prepared'
            atomic_json(Path(__file__).parent / (args.task + '-' + action + '.json'), outcome)
            print(outcome, flush=True)
        finally:
            context.close()
            browser.close()


if __name__ == '__main__':
    main()
