"""Offline demonstration of MathJax processing bare environments inside SVG titles.

This reproduces a possible origin of the historical DOM shape, not the exact
historical website configuration. No database, capture, or source files change.
"""
import hashlib
import html
import importlib.util
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BUNDLE = ROOT / "ui/vendor/mathjax/tex-svg.js"
OLD_PARSER = Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py')
SOURCE = r"A=\begin{bmatrix}1&2\\3&4\end{bmatrix},\quad x=\begin{bmatrix}5\\6\end{bmatrix}"
HTML = ('<div id="fixture"><span class="mjpage"><svg xmlns="http://www.w3.org/2000/svg">'
        '<title>' + html.escape(SOURCE) + '</title><text>Retained SVG drawing</text>'
        '</svg></span></div>')


def run():
    spec = importlib.util.spec_from_file_location('historical_lesson_parser_trigger', OLD_PARSER)
    old = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = old
    spec.loader.exec_module(old)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for exclude_title in (False, True):
            page = browser.new_page()
            page.route("**/*", lambda route: route.abort())
            page.set_content(HTML)
            config = {"startup": {"typeset": False}, "options": {"enableMenu": False}}
            if exclude_title:
                config["options"]["skipHtmlTags"] = ["script", "noscript", "style", "textarea", "pre", "code", "annotation", "annotation-xml", "title"]
            page.evaluate("config => window.MathJax = config", config)
            page.add_script_tag(path=str(BUNDLE))
            page.evaluate("async () => { await MathJax.startup.promise; await MathJax.typesetPromise([document.querySelector('#fixture')]); }")
            record = page.locator("#fixture > span > svg > title").evaluate("""title => ({
                html: title.outerHTML,
                text: title.textContent,
                nested_containers: title.querySelectorAll('mjx-container').length,
                mathml_fragments: title.querySelectorAll('math').length,
                surrounding_text: [...title.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(''),
            })""")
            record.update(exclude_title=exclude_title, configuration=config)
            node = BeautifulSoup('<span class="mjpage"><svg>' + record['html'] + '</svg></span>', 'html.parser').select_one('.mjpage')
            record['historical_extractor_output'] = old.extract_math_from_node(node)[0]
            results.append(record)
            page.close()
        browser.close()
    report = {"scope": "Offline MathJax SVG reproduction; historical site used CHTML and its exact configuration is not established here",
              "bundle": str(BUNDLE), "bundle_sha256": hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
              "old_parser": str(OLD_PARSER), "old_parser_sha256": hashlib.sha256(OLD_PARSER.read_bytes()).hexdigest(),
              "source_title": SOURCE, "results": results}
    report['checks'] = {'default_processing_retypesets_both_matrix_environments': results[0]['nested_containers'] == 2,
                       'excluding_titles_preserves_exact_source': results[1]['text'] == SOURCE and results[1]['nested_containers'] == 0,
                       'old_selector_loses_both_labels_and_second_matrix': results[0]['historical_extractor_output'].replace(' ', '') == '[1|2;3|4]'}
    (HERE / "reproduction.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps([{k: v for k, v in row.items() if k not in ("html", "configuration")} for row in results], indent=2))
    assert all(report['checks'].values()), report['checks']


if __name__ == "__main__":
    run()
