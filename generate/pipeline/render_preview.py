#!/usr/bin/env python3
"""Render generated records through the unmodified learning UI without a database."""
import argparse
import hashlib
import http.server
import json
import mimetypes
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
from urllib.parse import parse_qs, unquote, urlparse

REPO = Path(__file__).resolve().parents[2]

VISIBLE_DOM_AUDIT = r"""() => {
        const root = document.querySelector('.lesson-content');
        const visible = element => {
          // The native select stores TeX values for the rich UI; learners see
          // its rendered trigger/menu instead. aria-hidden alone is not a
          // visibility test, so keep this exception specific to that control.
          if (element.closest('select.answer-select-native[aria-hidden="true"]')) return false;
          const style = getComputedStyle(element);
          return style.visibility !== 'hidden' && style.visibility !== 'collapse'
            && style.display !== 'none' && element.getClientRects().length > 0;
        };
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        const rawTex = [], codeMath = [];
        let node;
        while ((node = walker.nextNode())) {
          if (!visible(node.parentElement) || node.parentElement.closest('mjx-container,math,script,style,textarea,math-field')) continue;
          if (/\\(?:begin|end)\{|\\(?:eqalign|dfrac|frac|sqrt)\b|\$\$|\[\/?math\]/.test(node.textContent)) rawTex.push(node.textContent.slice(0,200));
          if (node.parentElement.closest('pre,code') && /\$|\\(?:begin|dfrac|frac)/.test(node.textContent)) codeMath.push(node.textContent.slice(0,200));
        }
        return {
        rawTex, codeMath,
        internalFieldLabels:[...root.querySelectorAll('.answer-field legend,.response-summary')]
          .filter(visible).map(node=>node.textContent.trim()).filter(text=>/^Answer:\s*(answer|selection)(?:\s|[·:]|$)/i.test(text)),
        mathContainers:document.querySelectorAll('mjx-container').length,
        mathErrors:[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error')].filter(visible).map(node=>node.textContent),
        brokenImages:[...document.images].filter(image=>!image.complete || !image.naturalWidth).map(image=>image.src),
        danglingGlyphs:[...document.querySelectorAll('mjx-container use')].map(node=>node.getAttribute('href') || node.getAttribute('xlink:href'))
          .filter(href=>href?.startsWith('#') && !document.getElementById(href.slice(1))),
        text:document.querySelector('.lesson-content').innerText,
        fonts:document.fonts.status
      }}"""

# Use the installed browser driver; do not install a second rendering stack.
BROWSER_SCRIPT = r"""
const fs = require('fs');
const config = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const { chromium } = require(config.playwright);
const audit = __VISIBLE_DOM_AUDIT__;
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:config.browser,
    args:['--disable-dev-shm-usage']});
  const reports = [];
  try {
    for (let index = 0; index < config.count; index++) {
      const context = await browser.newContext({viewport:{width:1280,height:1000},deviceScaleFactor:1});
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      await page.route('**/*', route => new URL(route.request().url()).origin === config.origin
        ? route.continue() : route.abort());
      await page.goto(config.origin + '/learn?activityId=' + index, {waitUntil:'networkidle'});
      await page.locator('.lesson-content').waitFor();
      // Lazy images in the worked solution also need to load before a full-page capture.
      await page.evaluate(async () => {
        for (const image of document.images) image.loading = 'eager';
        if (window.MathJax?.startup?.promise) await MathJax.startup.promise;
        await document.fonts.ready;
      });
      await page.waitForLoadState('networkidle');
      await page.evaluate(async () => {
        if (window.MathJax?.typesetPromise) await MathJax.typesetPromise();
        await document.fonts.ready;
        await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      });
      const state = await page.evaluate(audit);
      const stem = config.output + '/question-' + String(index + 1).padStart(3,'0');
      await page.screenshot({path:stem+'.png',fullPage:true,animations:'disabled'});
      fs.writeFileSync(stem+'.html',await page.content());
      state.dropdowns = [];
      // The completed preview intentionally disables inputs. Load an active
      // presentation through the same unmodified UI to exercise real menus.
      if (await page.locator('.answer-select-trigger').count()) {
        await page.goto(config.origin + '/learn?activityId=' + index + '-active', {waitUntil:'networkidle'});
        await page.locator('.lesson-content').waitFor();
        await page.evaluate(async () => {
          for (const image of document.images) image.loading = 'eager';
          if (window.MathJax?.startup?.promise) await MathJax.startup.promise;
          if (window.MathJax?.typesetPromise) await MathJax.typesetPromise();
          await document.fonts.ready;
          await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
        });
        const triggers = page.locator('.answer-select-trigger');
        for (let optionIndex = 0; optionIndex < await triggers.count(); optionIndex++) {
          const trigger = triggers.nth(optionIndex);
          if (await trigger.isDisabled()) throw new Error('Active preview dropdown is disabled');
          await trigger.click();
          await page.evaluate(async () => {
            if (window.MathJax?.typesetPromise) await MathJax.typesetPromise();
            await document.fonts.ready;
            await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
          });
          const menu = await page.evaluate(audit);
          menu.screenshot = stem + '-dropdown-' + (optionIndex + 1) + '.png';
          menu.open = await trigger.getAttribute('aria-expanded') === 'true';
          await page.screenshot({path:menu.screenshot,fullPage:true,animations:'disabled'});
          state.dropdowns.push(menu);
          await page.keyboard.press('Escape');
        }
      }
      state.index=index; state.screenshot=stem+'.png'; state.javascriptErrors=errors;
      state.passed=!errors.length && !state.mathErrors.length && !state.brokenImages.length
        && !state.danglingGlyphs.length && !state.rawTex.length && !state.codeMath.length
        && !state.internalFieldLabels.length && state.fonts==='loaded'
        && (!config.expectedMath[index] || state.mathContainers>0)
        && state.dropdowns.every(menu => menu.open && !menu.rawTex.length && !menu.codeMath.length
          && !menu.mathErrors.length && !menu.brokenImages.length && !menu.danglingGlyphs.length
          && !menu.internalFieldLabels.length && menu.fonts === 'loaded');
      reports.push(state);
      await context.close();
    }
  } finally { await browser.close(); }
  const report={renderer:'unmodified ui/Learning.html and learning.js',database_writes:0,
    passed:reports.every(item=>item.passed),cases:reports};
  fs.writeFileSync(config.output+'/rendering.json',JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({passed:report.passed,count:reports.length,report:config.output+'/rendering.json'}));
  if (!report.passed) process.exitCode=1;
})().catch(error=>{console.error(error);process.exitCode=1});
""".replace("__VISIBLE_DOM_AUDIT__", VISIBLE_DOM_AUDIT)


def enum(value):
    return str(value[":db/ident"] if isinstance(value, dict) else value).split("/")[-1]


def answer_id(value):
    if isinstance(value, dict):
        return str(value[":answer/id"])
    if isinstance(value, (list, tuple)) and len(value) == 2 and value[0] == ":answer/id":
        return str(value[1])
    return str(value)


def preview(record, index, *, active=False):
    question = record.get("question", record)
    fields = []
    for number, field in enumerate(question[":question/answer-fields"]):
        choices = [{"id": str(answer[":answer/id"]), "type": enum(answer[":answer/type"]),
                    "value": answer[":answer/value"], "feedback": answer.get(":answer/feedback", "")}
                   for answer in field[":answer-field/choices"]]
        correct_id = answer_id(field[":answer-field/correct"])
        correct = next(answer for answer in choices if answer["id"] == correct_id)
        kind = enum(field[":answer-field/type"])
        fields.append({"id": field.get(":answer-field/id", number), "key": field[":answer-field/key"],
                       "type": kind, "answerType": correct["type"], "choices": choices,
                       "correctAnswer": correct, "response": {"value": correct["value"], "choiceId": correct_id}})
    step = {"kind": "question", "contentId": index + 1, "status": "correct", "problem": question[":question/problem"],
            "solution": question.get(":question/worked-solution", ""), "fields": fields}
    if active:
        step['status'] = 'started'
        for field in fields:
            field.pop('response', None)
    return {"activityId": str(index), "title": "Generator review", "type": "lesson", "steps": [step],
            "courseId": "review", "learner": {"id": 1, "name": "Offline review"}}


def resolve_node(playwright, node=None, environment=None):
    """Prefer Playwright's installed runtime over an incompatible system Node."""
    environment = os.environ if environment is None else environment
    explicit = node or environment.get('COURSE_ACADEMY_NODE_EXECUTABLE')
    candidates = [explicit] if explicit else [
        Path(playwright).parent.parent / 'bin/node',
        Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',
        shutil.which('node', path=environment.get('PATH')),
    ]
    checked, failures = set(), []
    for candidate in candidates:
        if not candidate:
            continue
        executable = shutil.which(str(candidate), path=environment.get('PATH'))
        if not executable or executable in checked:
            continue
        checked.add(executable)
        try:
            result = subprocess.run([executable, '--version'], capture_output=True,
                                    text=True, check=True, timeout=5)
            version = re.fullmatch(r'v(\d+)\.\d+\.\d+\s*', result.stdout)
            if version and int(version[1]) >= 20:
                return executable
            failures.append(f'{executable}: {result.stdout.strip()}')
        except (OSError, subprocess.SubprocessError) as error:
            failures.append(f'{executable}: {error}')
    raise RuntimeError('Playwright requires Node >=20. Set --node or '
                       'COURSE_ACADEMY_NODE_EXECUTABLE to an installed compatible runtime. '
                       + '; '.join(failures))


def render(records, output, asset_roots, browser=None, playwright=None, node=None):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    ui = REPO / "ui"
    roots = [Path(root).resolve() for root in asset_roots]
    browser = browser or next(iter(sorted(Path.home().glob(".cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"), reverse=True)), None)
    playwright = playwright or os.environ.get("COURSE_ACADEMY_PLAYWRIGHT_MODULE") or Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright"
    if not browser or not Path(browser).is_file() or not Path(playwright).exists():
        raise RuntimeError("Installed Node Playwright, node, and Chromium headless shell are required; use --browser/--playwright for existing alternatives")
    node = resolve_node(playwright, node)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            path = unquote(parsed.path)
            if path == "/api/developer-mode":
                data, kind = json.dumps({"enabled": True}).encode(), "application/json"
            elif path == "/api/preview":
                try:
                    identity = parse_qs(parsed.query)["activityId"][0]
                    active = identity.endswith('-active')
                    index = int(identity.removesuffix('-active'))
                    data, kind = json.dumps(preview(records[index], index, active=active)).encode(), "application/json"
                except (IndexError, KeyError, ValueError):
                    self.send_error(400); return
            else:
                file = None
                if path == "/learn":
                    file = ui / "Learning.html"
                elif path.startswith("/ui/"):
                    candidate = (ui / path[4:]).resolve()
                    if candidate.is_relative_to(ui):
                        file = candidate
                elif path == "/api/asset":
                    relative = Path(parse_qs(parsed.query).get("path", [""])[0])
                    for root in roots:
                        candidate = (root / relative).resolve()
                        if candidate.is_relative_to(root) and candidate.is_file():
                            file = candidate; break
                if file is None or not file.is_file():
                    self.send_error(404); return
                data, kind = file.read_bytes(), mimetypes.guess_type(file)[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.end_headers()
            self.wfile.write(data)

        def do_POST(self):
            self.send_error(405, "Review fixture has no mutation routes")

        def log_message(self, *_args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        expected_math = []
        for record in records:
            question = record.get("question", record)
            prose = question.get(":question/problem", "") + question.get(":question/worked-solution", "")
            expected_math.append(bool(re.search(r"\$|\\\(|\\\[|\\begin\{", prose)) or any(
                enum(answer[":answer/type"]) == "math" for field in question[":question/answer-fields"]
                for answer in field[":answer-field/choices"]))
        config = {"browser": str(browser), "playwright": str(playwright), "node": node, "count": len(records), "expectedMath": expected_math,
                  "output": str(output), "origin": f"http://127.0.0.1:{server.server_port}"}
        (output / "browser-config.json").write_text(json.dumps(config))
        (output / "render-browser.cjs").write_text(BROWSER_SCRIPT)
        (output / "input.json").write_text(json.dumps(records, indent=2) + "\n")
        (output / "ui-hashes.json").write_text(json.dumps({name: hashlib.sha256((ui / name).read_bytes()).hexdigest()
            for name in ("Learning.html", "learning.js", "math-protection.js", "question-fields.js", "mathjax-config.js")}, indent=2) + "\n")
        subprocess.run([node, str(output / "render-browser.cjs"), str(output / "browser-config.json")],
                       check=True, timeout=max(90, 45 * len(records)))
    finally:
        server.shutdown()
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--asset-root", action="append", default=[])
    parser.add_argument("--math-root", default=os.environ.get("EDB_MATH_ROOT", "/media/jake/SSD/EDB/math"))
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--browser")
    parser.add_argument("--playwright")
    parser.add_argument("--node", help="Existing Node >=20 executable; otherwise prefer the bundled runtime")
    args = parser.parse_args()
    records = json.loads(args.input.read_text())
    if isinstance(records, dict):
        records = records.get("records", records.get("questions", [records]))
    if not isinstance(records, list) or not records or args.limit < 1:
        parser.error("input must contain records and --limit must be positive")
    render(records[:args.limit], args.output, [args.math_root, args.input.resolve().parent, *args.asset_root],
           args.browser, args.playwright, args.node)


if __name__ == "__main__":
    main()
