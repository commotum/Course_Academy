"""Exercise the current DOM extractor on saved originals, without network access."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / 'source-manifest.json').read_text())
extractor = (ROOT / 'scripts/question_capture/dom.js').read_text()
results = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.route('**/*', lambda route: route.abort())
    for row in manifest:
        result = {'entity': row['entity'], 'mid': row['mid']}
        for role in ['prompt_sources', 'solution_sources']:
            sources = row[role]
            if not sources:
                continue
            # Prefer complete saved DOM over the original lesson's old SVG
            # representation. Preserve both links in source-manifest.json.
            source = next((s for s in sources if s['role'] == 'saved original DOM'), sources[0])
            page.set_content('<div id="audit-source">' + source['html'] + '</div>')
            node = page.locator('#audit-source > *').first
            try:
                extracted = node.evaluate(extractor)
                result[role] = {'source': source['path'], **{k: v for k, v in extracted.items() if k not in ['html', 'assets']}}
            except Exception as error:
                result[role] = {'source': source['path'], 'error': str(error)}
        results.append(result)
    browser.close()
(HERE / 'current-extractor-results.json').write_text(json.dumps(results, indent=2) + '\n')
errors = [{'entity': r['entity'], 'role': role, 'error': r[role].get('error'), 'errors': r[role].get('errors')}
          for r in results for role in ['prompt_sources', 'solution_sources'] if role in r
          and (r[role].get('error') or r[role].get('errors'))]
print(json.dumps({'records': len(results), 'extractor_errors': errors}, indent=2))
