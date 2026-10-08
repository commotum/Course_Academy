import json
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE = Path(__file__).with_name('dom.js')
EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/differential/14040374/diagnostics/1791438030867231439/page.html')
ADDED = "        if (n.getAttribute('notation') === 'left right') return '\\\\left|' + cs.join('') + '\\\\right|';\n"


def dom_tree(element):
    children = []
    if element.text:
        children.append({'nodeType': 3, 'textContent': element.text})
    for child in element:
        children.append(dom_tree(child))
        if child.tail:
            children.append({'nodeType': 3, 'textContent': child.tail})
    return {'nodeType': 1, 'localName': element.tag, 'attrs': element.attrib,
            'textContent': ''.join(element.itertext()), 'childNodes': children}


class DeterminantEnclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text()
        matches = re.findall(r'<menclose\b[^>]*>.*?</menclose>', EVIDENCE.read_text(), re.S)
        if len(matches) != 1:
            raise AssertionError('Expected one saved enclosure')
        cls.markup = matches[0]
        if ET.fromstring(cls.markup).get('notation') != 'left right':
            raise AssertionError('Unexpected saved enclosure notation')

    def render(self, markup, source=None):
        source = self.source if source is None else source
        renderer = source[source.index('  const greek ='):source.index('  function render(n)')]
        shim = '''const p = JSON.parse(require('fs').readFileSync(0, 'utf8'));
function hydrate(n) {
  if (n.nodeType === 3) return n;
  n.getAttribute = k => n.attrs[k] ?? null;
  n.childNodes = n.childNodes.map(hydrate);
  const elements = n.childNodes.filter(c => c.nodeType === 1);
  elements.forEach((c, i) => c.nextElementSibling = elements[i + 1] || null);
  return n;
}
const errors = [];
'''
        code = shim + renderer + '\nprocess.stdout.write(JSON.stringify({value:m(hydrate(p)), errors}));'
        process = subprocess.run(['node', '-e', code],
                                 input=json.dumps(dom_tree(ET.fromstring(markup))),
                                 text=True, capture_output=True, check=True, timeout=10)
        return json.loads(process.stdout)

    def test_original_saved_failure(self):
        original = self.source.replace(ADDED, '')
        item = self.render(self.markup, original)
        self.assertEqual(item['errors'], ['Unsupported MathML enclosure'])

    def test_determinant_preserves_all_entries(self):
        item = self.render(self.markup)
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['value'],
                         r'\left|\begin{aligned}2-\lambda  & 3 \\ -3 & 2-\lambda \end{aligned}\right|')
        root = ET.fromstring(self.markup)
        inner = ''.join(ET.tostring(child, encoding='unicode') for child in root)
        plain = self.render('<math>' + inner + '</math>')
        self.assertEqual(plain['errors'], [])
        self.assertEqual(item['value'], r'\left|' + plain['value'] + r'\right|')

    def test_unsupported_notations_still_fail(self):
        for notation in ('left right radical', 'radical', 'left'):
            with self.subTest(notation=notation):
                markup = self.markup.replace('notation="left right"', 'notation="' + notation + '"')
                self.assertEqual(self.render(markup)['errors'], ['Unsupported MathML enclosure'])

if __name__ == '__main__':
    unittest.main()
