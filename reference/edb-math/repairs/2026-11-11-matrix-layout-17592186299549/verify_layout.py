"""Verify field positions and identities in every real-UI render."""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

H = Path(__file__).resolve().parent
records = json.loads((H/'lesson-preview-records.json').read_text())
rendering = json.loads((H/'lesson-render/rendering.json').read_text())
assert rendering['passed']
verified = 0
for index, record in enumerate(records, 1):
    q = record['question']
    authored = BeautifulSoup(q[':question/problem'], 'html.parser')
    expected = [[re.search(r'\{\{([^{}]+)\}\}', cell.text)[1] for cell in row.select('td')]
                for row in authored.select('.matrix-answer-brackets tr')]
    assert expected
    identities = {f[':answer-field/key']: f[':answer-field/id'] for f in q[':question/answer-fields']}
    for state in ('active', 'completed'):
        for width in (390, 1280):
            path = H/'lesson-render'/f'question-{index:03d}-{state}-{width}x1000.html'
            dom = BeautifulSoup(path.read_text(), 'html.parser')
            actual = [[cell.select_one('.field-location')['data-field-key'] for cell in row.select('td')]
                      for row in dom.select('.matrix-answer-brackets tr')]
            assert actual == expected, (path.name, actual, expected)
            controls = dom.select('.matrix-answer-brackets .field-location')
            assert len(controls) == len(identities)
            for control in controls:
                assert control.select_one('.answer-inline')['data-field-id'] == identities[control['data-field-key']]
                if state == 'active':
                    field = control.select_one('math-field')
                    assert field is not None and field.get('data-read-only') == 'false'
                    assert not field.text.strip(), (path.name, 'Answer leaked into active input')
            verified += 1
result = {'passed': True, 'questions': len(records), 'rendered_states_and_viewports': verified,
          'field_positions_and_identities_preserved': True, 'active_inputs_enabled_and_empty': True}
(H/'layout-verification.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
