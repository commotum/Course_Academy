"""Record the focused HTML-boundary regression and exact reload hashes."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
hash_file = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
owned = {
    'scripts/question_capture/math_format.py': 'math_format-before.py',
    'scripts/question_capture/activities.py': 'activities-before.py',
    'capture/scripts/database/text.py': 'database-text-before.py',
    'scripts/question_capture/test_activities.py': 'test_activities-before.py',
    'capture/scripts/tests/test_database_math_content.py': 'test_database_math_content-before.py',
}
hashes = {path: {'before': hash_file(HERE / before), 'after': hash_file(ROOT / path)}
          for path, before in owned.items()}
tests = []
for name, pythonpath, modules in (
    ('legacy-html-and-math-format', 'scripts/question_capture',
     ['scripts/question_capture/test_activities.py', 'scripts/question_capture/test_math_format.py']),
    ('active-html-and-fill-only', 'capture',
     ['scripts.tests.test_database_math_content', 'scripts.tests.test_capture_fill_only']),
):
    command = ['.venv/bin/python', '-m', 'unittest', *modules]
    result = subprocess.run(command, cwd=ROOT, env={**os.environ, 'PYTHONPATH': pythonpath},
                            capture_output=True, text=True)
    output = result.stdout + result.stderr
    (HERE / (name + '.log')).write_text(output)
    count = re.search(r'Ran (\d+) tests?', output)
    assert result.returncode == 0 and count, output
    tests.append({'name': name, 'command': command, 'PYTHONPATH': pythonpath,
                  'test_count': int(count[1]), 'exit_code': result.returncode,
                  'log': name + '.log', 'passed': True})

proof = json.loads((HERE / 'active-path-after.json').read_text())
assert all(proof['checks'].values())
reloaded = json.loads((HERE / 'workers/after.json').read_text())
reload_matches = {path: hashes[path]['after'] == value
                  for path, value in reloaded['code_hashes'].items()}
assert all(reload_matches.values())
report = {
    'passed': True,
    'scope': 'Pure source TeX at two HTML-to-Markdown boundaries, before HTML whitespace collapse',
    'cause': 'Real percent comments lose their line boundary when HTML text whitespace collapses; the first comment can hide the remainder of a formula. Legacy matrix row delimiters also require source line boundaries.',
    'repair': 'normalize_source_tex removes real comments while preserving line endings and escaped percent signs, then canonicalizes legacy TeX before either HTML renderer collapses whitespace. Mixed TeX/MathML titles stay whole graphics, including titles with nested fragment annotations.',
    'active_main_path': 'capture/scripts/browser/adapter.py loads extract.js and evaluates it in _read for _lesson. extract.js preserves pure SVG-title newlines. database/prepare.py uses formatted_prose; database/math_content.py prose calls database/text.py markdown, which passes ordinary Markdown through. This main browser path is unchanged and retains line-scoped comments correctly.',
    'active_fallback': 'capture/scripts/database/text.py markdown accepts raw HTML; pure-title conversion now calls the cached formatter.normalize_source_tex before NavigableString whitespace collapsing. Supported raw HTML calls through database/math_content.py prose are covered.',
    'legacy_path': 'scripts/question_capture/browser.py capture_lesson imports activities.capture_lesson. activities._formula_html now normalizes pure titles before html_to_markdown collapses whitespace. New capture workers do not import this legacy activities module.',
    'reload': 'Active workers import database.text and cache the shared formatter module, so previously running workers were checkpoint-stopped and restarted by the parent with the same commands, accounts and answer profiles. No browser extractor change was needed.',
    'policy': 'Complete captures, saved requests, answer fields, correct answers, entered answers and missing solutions are untouched; existing fill-only regression suite passes.',
    'source_proof': 'active-path-after.json',
    'source_checks': proof['checks'],
    'mixed_title_asset_check': 'verification.json',
    'files': hashes,
    'tests': tests,
    'total_tests': sum(t['test_count'] for t in tests),
    'worker_reload_hash_matches': reload_matches,
    'worker_reload_evidence': 'workers/after.json',
}
(HERE / 'html-converter-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'passed': True, 'tests': report['total_tests'],
                  'worker_reload_hash_matches': reload_matches,
                  'manifest_sha256': hash_file(HERE / 'html-converter-verification.json')}, indent=2))
