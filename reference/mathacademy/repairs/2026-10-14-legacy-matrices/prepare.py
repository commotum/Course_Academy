"""Prepare the small legacy-matrix follow-up, using the production capture code."""
import hashlib
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
examples = [(17592186059576, 'example-4683.html', 'step-17170'),
            (17592186059577, 'example-4684.html', 'step-17171')]
if '--lesson-equations' in sys.argv:
    HERE = HERE / 'lesson-equations'
    examples = [(17592186059578, 'example-4685.html', 'step-17173'),
                (17592186059579, 'example-4686.html', 'step-17174')]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import dumps, loads, kw

source = (ROOT / 'scripts/question_capture/dom.js').read_text()
helper = source[source.index('  function legacyMatrixTex('):source.index('  const assets =')]
before = loads((HERE / 'before.edn').read_text())
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.route('**/*', lambda route: route.abort())
    after = page.evaluate('(records) => {const errors=[];' + helper +
                          '; const result=records.map(([e,a,t])=>[e,a,legacyMatrixTex(t)]);'
                          'if(errors.length)throw Error(errors.join(";"));return result;}', before)
    recovered = {}
    for eid, name, dom_id in examples:
        page.set_content((ROOT / 'scripts/question_capture/fixtures/matrices' / name).read_text())
        item = page.locator('#' + dom_id).evaluate(source)
        assert not item['errors'] and not item['assets'], item
        recovered[eid] = item
        for record in after:
            if record[0] == eid:
                record[2] = item['problem' if record[1] == ':question/problem' else 'worked_solution']
    browser.close()

forms, changes = [], []
for (eid, attr, old), (new_eid, new_attr, new) in zip(before, after):
    assert (eid, attr) == (new_eid, new_attr)
    if old == new:
        continue
    assert r'\matrix' not in new, (eid, attr)
    forms.append([kw(':db/cas'), eid, kw(attr), old, new])
    changes.append({'entity': eid, 'attribute': str(attr), 'before': old, 'after': new})
(HERE / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
(HERE / 'expected.edn').write_text(dumps([[f[1], f[2], f[4]] for f in forms]))
transaction = HERE / 'transaction.edn'
transaction.write_text(dumps(forms))
digest = hashlib.sha256(transaction.read_bytes()).hexdigest()
(HERE / 'commit-intent.json').write_text(json.dumps({
    'database': 'math', 'source': ':application/ca-engine', 'endpoint': '/tmp/edb-math/writer.sock',
    'file': str(transaction), 'sha256': digest, 'request_key': 'legacy-matrix-repair-' + digest,
    'fields': len(forms), 'entities': len(set(f[1] for f in forms)),
}, indent=2) + '\n')
print(f'Prepared {len(forms)} fields on {len(set(f[1] for f in forms))} entities')
