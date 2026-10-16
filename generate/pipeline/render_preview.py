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

# Use the installed browser driver; do not install a second rendering stack.
BROWSER_SCRIPT = r"""
const fs = require('fs');
const config = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const { chromium } = require(config.playwright);
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
      const state = await page.evaluate(() => ({
        mathContainers:document.querySelectorAll('mjx-container').length,
        mathErrors:[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error')].map(node=>node.textContent),
        brokenImages:[...document.images].filter(image=>!image.complete || !image.naturalWidth).map(image=>image.src),
        danglingGlyphs:[...document.querySelectorAll('mjx-container use')].map(node=>node.getAttribute('href') || node.getAttribute('xlink:href'))
          .filter(href=>href?.startsWith('#') && !document.getElementById(href.slice(1))),
        text:document.querySelector('.lesson-content').innerText,
        fonts:document.fonts.status
      }));
      const stem = config.output + '/question-' + String(index + 1).padStart(3,'0');
      await page.screenshot({path:stem+'.png',fullPage:true,animations:'disabled'});
      fs.writeFileSync(stem+'.html',await page.content());
      state.index=index; state.screenshot=stem+'.png'; state.javascriptErrors=errors;
      state.passed=!errors.length && !state.mathErrors.length && !state.brokenImages.length
        && !state.danglingGlyphs.length && state.fonts==='loaded'
        && (!config.expectedMath[index] || state.mathContainers>0);
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
"""


def enum(value):
    return str(value[":db/ident"] if isinstance(value, dict) else value).split("/")[-1]


def answer_id(value):
    if isinstance(value, dict):
        return str(value[":answer/id"])
    if isinstance(value, (list, tuple)) and len(value) == 2 and value[0] == ":answer/id":
        return str(value[1])
    return str(value)


def preview(record, index):
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
    return {"activityId": str(index), "title": "Generator review", "type": "lesson", "steps": [step],
            "courseId": "review", "learner": {"id": 1, "name": "Offline review"}}


def render(records, output, asset_roots, browser=None, playwright=None):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    ui = REPO / "ui"
    roots = [Path(root).resolve() for root in asset_roots]
    browser = browser or next(iter(sorted(Path.home().glob(".cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"), reverse=True)), None)
    playwright = playwright or os.environ.get("COURSE_ACADEMY_PLAYWRIGHT_MODULE") or Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright"
    if not browser or not Path(browser).is_file() or not Path(playwright).exists() or not shutil.which("node"):
        raise RuntimeError("Installed Node Playwright, node, and Chromium headless shell are required; use --browser/--playwright for existing alternatives")

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            path = unquote(parsed.path)
            if path == "/api/developer-mode":
                data, kind = json.dumps({"enabled": True}).encode(), "application/json"
            elif path == "/api/preview":
                try:
                    index = int(parse_qs(parsed.query)["activityId"][0])
                    data, kind = json.dumps(preview(records[index], index)).encode(), "application/json"
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
        config = {"browser": str(browser), "playwright": str(playwright), "count": len(records), "expectedMath": expected_math,
                  "output": str(output), "origin": f"http://127.0.0.1:{server.server_port}"}
        (output / "browser-config.json").write_text(json.dumps(config))
        (output / "render-browser.cjs").write_text(BROWSER_SCRIPT)
        (output / "input.json").write_text(json.dumps(records, indent=2) + "\n")
        (output / "ui-hashes.json").write_text(json.dumps({name: hashlib.sha256((ui / name).read_bytes()).hexdigest()
            for name in ("Learning.html", "learning.js", "question-fields.js", "mathjax-config.js")}, indent=2) + "\n")
        subprocess.run(["node", str(output / "render-browser.cjs"), str(output / "browser-config.json")],
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
    args = parser.parse_args()
    records = json.loads(args.input.read_text())
    if isinstance(records, dict):
        records = records.get("records", records.get("questions", [records]))
    if not isinstance(records, list) or not records or args.limit < 1:
        parser.error("input must contain records and --limit must be positive")
    render(records[:args.limit], args.output, [args.math_root, args.input.resolve().parent, *args.asset_root],
           args.browser, args.playwright)


if __name__ == "__main__":
    main()
