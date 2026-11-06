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
import sys
from urllib.parse import parse_qs, unquote, urlparse

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from scripts.generator_evidence import implementation_hashes, record_sha256, sha256_file

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
        // noUndefined renders unknown commands as mtext, not merror. SVG
        // mtext contains glyph references, so textContent alone misses them.
        mathErrors:[
          ...[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error')].filter(visible).map(node=>node.textContent),
          ...[...document.querySelectorAll('mjx-container [data-mml-node="mtext"],mjx-container mjx-mtext')]
            .filter(visible).map(node=>node.textContent || [...node.querySelectorAll('use[data-c]')]
              .map(glyph=>String.fromCodePoint(parseInt(glyph.getAttribute('data-c'),16))).join(''))
            .filter(text=>/\\[A-Za-z]+/.test(text))
        ],
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
    for (const index of config.selectedIndices) {
    for (const presentation of config.states) {
    for (const viewport of config.viewports) {
      const context = await browser.newContext({viewport,deviceScaleFactor:1});
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      await page.route('**/*', route => new URL(route.request().url()).origin === config.origin
        ? route.continue() : route.abort());
      await page.goto(config.origin + '/learn?activityId=' + index + (presentation === 'active' ? '-active' : ''), {waitUntil:'networkidle'});
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
      const filename = 'question-' + String(index + 1).padStart(3,'0') + '-' + presentation + '-' + viewport.width + 'x' + viewport.height;
      const stem = config.output + '/' + filename;
      await page.screenshot({path:stem+'.png',fullPage:true,animations:'disabled'});
      fs.writeFileSync(stem+'.html',await page.content());
      // Wide prose math and option labels may scroll in outer prose containers.
      // Retain the left-edge screenshot above, then inspect the hidden right edge.
      state.horizontalMath = await page.evaluate(() =>
        [...document.querySelectorAll('.lesson-content mjx-container, .lesson-content .choice .prose, .lesson-content .worked-solution > .prose')]
          .filter(node => node.getClientRects().length && node.clientWidth > 0
            && !node.closest('details:not([open])')
            && node.scrollWidth > node.clientWidth + 3
            // SVG intrinsic scrollWidth may exceed its responsive drawn width.
            // Audit only formulas whose drawn SVG actually exceeds the viewport.
            && [...node.querySelectorAll('svg')].some(svg => svg.getBoundingClientRect().width > node.clientWidth + 3))
          .map(node => {
            node.scrollLeft = node.scrollWidth;
            return {tagName:node.tagName, className:node.className, clientWidth:node.clientWidth, scrollWidth:node.scrollWidth,
              overflowX:getComputedStyle(node).overflowX, scrollLeft:node.scrollLeft};
          }));
      if (state.horizontalMath.length) {
        state.horizontalMathScreenshot = filename + '-math-scroll-right.png';
        await page.screenshot({path:config.output + '/' + state.horizontalMathScreenshot,
          fullPage:true,animations:'disabled'});
        await page.evaluate(() => {
          for (const node of document.querySelectorAll('.lesson-content mjx-container, .lesson-content .choice .prose, .lesson-content .worked-solution > .prose')) node.scrollLeft = 0;
        });
      }
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
          menu.screenshot = filename + '-dropdown-' + (optionIndex + 1) + '.png';
          menu.state = 'active';
          menu.open = await trigger.getAttribute('aria-expanded') === 'true';
          await page.screenshot({path:config.output + '/' + menu.screenshot,fullPage:true,animations:'disabled'});
          state.dropdowns.push(menu);
          await page.keyboard.press('Escape');
        }
      }
      state.index=index; state.screenshot=filename+'.png'; state.javascriptErrors=errors;
      state.state=presentation; state.viewport=viewport; state.record_sha256=config.recordSha256[index];
      state.passed=!errors.length && !state.mathErrors.length && !state.brokenImages.length
        && !state.danglingGlyphs.length && !state.rawTex.length && !state.codeMath.length
        && !state.internalFieldLabels.length && state.fonts==='loaded'
        && state.horizontalMath.every(math => ['auto','scroll'].includes(math.overflowX)
          && math.scrollLeft > 0)
        && (!config.expectedMath[presentation][index] || state.mathContainers>0)
        && state.dropdowns.every(menu => menu.open && !menu.rawTex.length && !menu.codeMath.length
          && !menu.mathErrors.length && !menu.brokenImages.length && !menu.danglingGlyphs.length
          && !menu.internalFieldLabels.length && menu.fonts === 'loaded');
      reports.push(state);
      await context.close();
    }
    }
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


def select_indices(records, indices=None, limit=None):
    if not isinstance(records, list) or not records:
        raise ValueError('rendering requires nonempty input records')
    selected = list(range(len(records))) if indices is None else list(indices)
    if not selected or len(set(selected)) != len(selected) or any(type(i) is not int or not 0 <= i < len(records) for i in selected):
        raise ValueError('representative indices must be distinct valid zero-based record indices')
    if limit is not None:
        if type(limit) is not int or limit < 1:
            raise ValueError('limit must be positive')
        selected = selected[:limit]
    return selected


def parse_viewport(value):
    match = re.fullmatch(r'(\d+)x(\d+)', value)
    if not match or min(map(int, match.groups())) < 1:
        raise argparse.ArgumentTypeError('viewport must be positive WIDTHxHEIGHT')
    return dict(zip(('width', 'height'), map(int, match.groups())))


def render(records, output, asset_roots, browser=None, playwright=None, node=None, *,
           states=('active', 'completed'), viewports=None, indices=None, limit=None):
    selected = select_indices(records, indices, limit)
    if not states or any(state not in ('active', 'completed') for state in states):
        raise ValueError('states must contain active or completed')
    viewports = viewports or [{'width': 1280, 'height': 1000}]
    if any(any(type(v.get(k)) is not int or v[k] < 1 for k in ('width', 'height')) for v in viewports):
        raise ValueError('viewports require positive integer width and height')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    ui = REPO / "ui"
    roots = [Path(root).resolve() for root in asset_roots]
    browser = browser or next(iter(sorted(Path.home().glob(".cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"), reverse=True)), None)
    playwright = playwright or os.environ.get("COURSE_ACADEMY_PLAYWRIGHT_MODULE") or Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright"
    if not browser or not Path(browser).is_file() or not Path(playwright).exists():
        raise RuntimeError("Installed Node Playwright, node, and Chromium headless shell are required; use --browser/--playwright for existing alternatives")
    node = resolve_node(playwright, node)
    renderer_code = implementation_hashes([Path(__file__)])
    served_files = {}
    changed_resources = set()

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
                if file.resolve().is_relative_to(REPO):
                    resource = str(file.resolve().relative_to(REPO))
                    identity = hashlib.sha256(data).hexdigest()
                    if resource in served_files and served_files[resource] != identity:
                        changed_resources.add(resource)
                    served_files[resource] = identity
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
        expected_math = {state: [] for state in states}
        for record in records:
            question = record.get("question", record)
            for state in states:
                prose = question.get(":question/problem", "") + (question.get(":question/worked-solution", "") if state == 'completed' else '')
                expected_math[state].append(bool(re.search(r"\$|\\\(|\\\[|\\begin\{", prose)) or any(
                    enum(answer[":answer/type"]) == "math" for field in question[":question/answer-fields"]
                    if state == 'completed' or enum(field[":answer-field/type"]) != 'blank'
                    for answer in field[":answer-field/choices"]))
        identities = [record_sha256(record) for record in records]
        config = {"browser": str(browser), "playwright": str(playwright), "node": node, "count": len(records),
                  "expectedMath": expected_math, "selectedIndices": selected, "states": list(states), "viewports": viewports,
                  "recordSha256": identities, "output": str(output), "origin": f"http://127.0.0.1:{server.server_port}"}
        (output / "browser-config.json").write_text(json.dumps(config))
        (output / "render-browser.cjs").write_text(BROWSER_SCRIPT)
        (output / "input.json").write_text(json.dumps(records, indent=2) + "\n")
        (output / "ui-hashes.json").write_text(json.dumps({name: hashlib.sha256((ui / name).read_bytes()).hexdigest()
            for name in ("Learning.html", "learning.js", "math-protection.js", "question-fields.js", "mathjax-config.js")}, indent=2) + "\n")
        subprocess.run([node, str(output / "render-browser.cjs"), str(output / "browser-config.json")],
                       check=True, timeout=max(90, 45 * len(selected) * len(states) * len(viewports)))
        report_path = output / "rendering.json"
        report = json.loads(report_path.read_text())
        implementation = {**renderer_code, **served_files}
        changed_resources.update(name for name, identity in implementation.items() if sha256_file(REPO / name) != identity)
        if changed_resources:
            raise ValueError('Renderer resources changed during inspection: ' + ', '.join(sorted(changed_resources)))
        for case in report['cases']:
            if case.get('horizontalMathScreenshot'):
                case['horizontalMathScreenshotSha256'] = sha256_file(output / case['horizontalMathScreenshot'])
            for captured in [case, *case.get('dropdowns', [])]:
                captured['screenshot_sha256'] = sha256_file(output / captured['screenshot'])
        report.update({"format": "course-academy-rendering-v1", "input_file": "input.json",
                       "input_sha256": sha256_file(output / "input.json"), "record_sha256": identities,
                       "checked_record_sha256": [identities[i] for i in selected],
                       "selection": {"input_count": len(records), "selected_indices": selected,
                                     "omitted_indices": [i for i in range(len(records)) if i not in selected]},
                       "implementation_sha256": implementation,
                       "runtime": {"browser_sha256": sha256_file(browser), "node_sha256": sha256_file(node)}})
        report_path.write_text(json.dumps(report, indent=2) + "\n")
        return report
    finally:
        server.shutdown()
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--asset-root", action="append", default=[])
    parser.add_argument("--math-root", default=os.environ.get("EDB_MATH_ROOT", "/media/jake/SSD/EDB/math"))
    parser.add_argument("--limit", type=int, default=None, help="Explicit cap; omitted records are reported")
    parser.add_argument("--indices", help="Comma-separated zero-based representative record indices")
    parser.add_argument("--state", choices=("active", "completed", "both"), default="both")
    parser.add_argument("--viewport", type=parse_viewport, action="append", help="WIDTHxHEIGHT; repeat for relevant layouts")
    parser.add_argument("--browser")
    parser.add_argument("--playwright")
    parser.add_argument("--node", help="Existing Node >=20 executable; otherwise prefer the bundled runtime")
    args = parser.parse_args()
    records = json.loads(args.input.read_text())
    if isinstance(records, dict):
        records = records.get("records", records.get("questions", [records]))
    if not isinstance(records, list) or not records or (args.limit is not None and args.limit < 1):
        parser.error("input must contain records and --limit must be positive")
    try:
        indices = [int(value) for value in args.indices.split(",")] if args.indices is not None else None
        render(records, args.output, [args.math_root, args.input.resolve().parent, *args.asset_root],
               args.browser, args.playwright, args.node, indices=indices, limit=args.limit,
               states=("active", "completed") if args.state == "both" else (args.state,), viewports=args.viewport)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
