"""Read-only feature probes of the checked-in extractors; no app/API requests."""
import json, sys
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from import_historical_question_content import Renderer

cases = {
    'normal_greek': '<mi mathvariant="normal">Π</mi>',
    'bold_vector': '<mi mathvariant="bold">v</mi>',
    'double_struck': '<msup><mi mathvariant="double-struck">R</mi><mn>3</mn></msup>',
    'red_cross_with_1em': '<mn>1</mn><mo>≠</mo><mn>0</mn><mspace width="1em"/><mstyle mathcolor="red"><mo>×</mo></mstyle>',
    **{'spacing_' + width: '<mi>a</mi><mspace width="' + width + '"/><mi>b</mi>'
       for width in ('0em', '-0.167em', '0.167em', '1em', '2em')},
}
result = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.route('**/*', lambda route: route.abort())
    for name, body in cases.items():
        math = '<math>' + body + '</math>'
        row = {'case': name, 'source_mathml': math, 'outputs': {}}
        for path in ('capture/scripts/browser/extract.js', 'scripts/question_capture/dom.js'):
            page.set_content('<div id="fixture"><div class="questionWidget-text">' + math + '</div></div>')
            extracted = page.locator('#fixture').evaluate((ROOT / path).read_text())
            row['outputs'][path] = {'tex': extracted['problem'], 'errors': extracted['errors']}
        renderer = Renderer(0)
        row['outputs']['scripts/import_historical_question_content.py'] = {
            'tex': renderer.m(BeautifulSoup(math, 'html.parser').math), 'errors': renderer.errors}
        result.append(row)
    browser.close()
(HERE / 'extractor-feature-probes.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
