"""Renderer runtime selection must work in the service's minimal PATH."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'generate/pipeline'))
from render_preview import resolve_node


class RendererRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.playwright = self.root / 'runtime/node_modules/playwright'
        self.playwright.mkdir(parents=True)
        self.home = patch('render_preview.Path.home', return_value=self.root / 'home')
        self.home.start()

    def tearDown(self):
        self.home.stop()
        self.temp.cleanup()

    def node(self, path, version):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'#!/bin/sh\nprintf "{version}\\n"\n')
        path.chmod(0o755)
        return path

    def test_bundled_runtime_avoids_old_system_node(self):
        bundled = self.node(self.root / 'runtime/bin/node', 'v22.19.0')
        self.node(self.root / 'system/node', 'v18.19.1')
        self.assertEqual(resolve_node(self.playwright, environment={'PATH': str(self.root / 'system')}), str(bundled))

    def test_current_path_node_is_a_valid_fallback(self):
        node = self.node(self.root / 'system/node', 'v20.19.0')
        self.assertEqual(resolve_node(self.playwright, environment={'PATH': str(node.parent)}), str(node))

    def test_explicit_override_is_checked_and_honored(self):
        self.node(self.root / 'runtime/bin/node', 'v22.19.0')
        chosen = self.node(self.root / 'chosen/node', 'v24.1.0')
        self.assertEqual(resolve_node(self.playwright, environment={'COURSE_ACADEMY_NODE_EXECUTABLE': str(chosen)}), str(chosen))
        old = self.node(self.root / 'old/node', 'v18.19.1')
        with self.assertRaisesRegex(RuntimeError, 'Node >=20'):
            resolve_node(self.playwright, node=str(old), environment={})

    def test_missing_or_old_runtime_fails_before_browser_work(self):
        self.node(self.root / 'system/node', 'v18.19.1')
        with self.assertRaisesRegex(RuntimeError, 'v18.19.1'):
            resolve_node(self.playwright, environment={'PATH': str(self.root / 'system')})


class VisibleMathAuditTests(unittest.TestCase):
    """Exercise the exact DOM audit in Chromium, including opened menu text."""
    def test_hidden_backing_values_are_ignored_but_visible_raw_tex_fails(self):
        import json
        import subprocess
        from render_preview import VISIBLE_DOM_AUDIT
        playwright = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'
        browser = next(iter(sorted(Path.home().glob('.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell'), reverse=True)), None)
        if not playwright.exists() or browser is None:
            self.skipTest('Installed Playwright and Chromium are required')
        node = resolve_node(playwright)
        source = r'''
const {chromium} = require(PLAYWRIGHT);
const audit = AUDIT;
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:BROWSER, args:['--disable-dev-shm-usage']});
  try {
    const page = await browser.newPage();
    await page.setContent(String.raw`<main class="lesson-content">
      <select class="answer-select-native sr-only" aria-hidden="true"><option>\frac{1}{x}</option></select>
      <span class="answer-select-value"><mjx-container>1/x</mjx-container></span>
      <button id="open" onclick="document.querySelector('#menu').hidden=false">Open</button>
      <span id="menu" hidden><button class="answer-select-option">\sqrt{x}</button></span>
    </main>`);
    const closed = await page.evaluate(audit);
    await page.click('#open');
    const opened = await page.evaluate(audit);
    await page.evaluate(() => document.querySelector('.answer-select-option').innerHTML='<mjx-container>√x</mjx-container>');
    const repaired = await page.evaluate(audit);
    await page.evaluate(() => {
      const text = document.createElement('span'); text.setAttribute('aria-hidden','true');
      text.textContent=String.raw`\frac{a}{b}`; document.querySelector('main').append(text);
    });
    const visibleAriaHidden = await page.evaluate(audit);
    console.log(JSON.stringify({closed,opened,repaired,visibleAriaHidden}));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1});
'''.replace('PLAYWRIGHT', json.dumps(str(playwright))).replace('BROWSER', json.dumps(str(browser))).replace('AUDIT', VISIBLE_DOM_AUDIT)
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / 'audit.cjs'
            script.write_text(source)
            result = subprocess.run([node, str(script)], capture_output=True, text=True, timeout=45, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['closed']['rawTex'], [])
        self.assertEqual(report['opened']['rawTex'], [r'\sqrt{x}'])
        self.assertEqual(report['repaired']['rawTex'], [])
        self.assertEqual(report['visibleAriaHidden']['rawTex'], [r'\frac{a}{b}'])

    def test_visible_display_delimiters_fail_outside_rendered_math(self):
        import json
        import subprocess
        from render_preview import VISIBLE_DOM_AUDIT
        playwright = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'
        browser = next(iter(sorted(Path.home().glob('.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell'), reverse=True)), None)
        if not playwright.exists() or browser is None:
            self.skipTest('Installed Playwright and Chromium are required')
        source = r'''
const {chromium} = require(PLAYWRIGHT);
const audit = AUDIT;
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:BROWSER, args:['--disable-dev-shm-usage']});
  try {
    const page = await browser.newPage();
    await page.setContent('<main class="lesson-content"><p>$$ {</p><mjx-container>$$</mjx-container><p hidden>$$ hidden</p><p>Costs $5</p></main>');
    const broken = await page.evaluate(audit);
    await page.evaluate(() => document.querySelector('p').innerHTML='<mjx-container>x+y&gt;0</mjx-container>');
    const repaired = await page.evaluate(audit);
    console.log(JSON.stringify({broken,repaired}));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1});
'''.replace('PLAYWRIGHT', json.dumps(str(playwright))).replace('BROWSER', json.dumps(str(browser))).replace('AUDIT', VISIBLE_DOM_AUDIT)
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / 'delimiters.cjs'
            script.write_text(source)
            result = subprocess.run([resolve_node(playwright), str(script)], capture_output=True, text=True, timeout=45, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['broken']['rawTex'], ['$$ {'])
        self.assertEqual(report['repaired']['rawTex'], [])
