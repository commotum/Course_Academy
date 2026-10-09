import json
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE = Path(__file__).with_name('dom.js')
EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14054087/example-5032.json')
ADDED = "        if (n.getAttribute('notation') === null || n.getAttribute('notation') === 'longdiv') return '\\\\enclose{longdiv}{' + cs.join('') + '}';\n"


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


class LongDivisionEnclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text()
        cls.saved = json.loads(EVIDENCE.read_text())
        cls.markups = [markup for markup in re.findall(
            r'<menclose\b[^>]*>.*?</menclose>', cls.saved['html'], re.S)
            if ET.fromstring(markup).get('notation') is None]
        if not cls.markups:
            raise AssertionError('Missing saved default long-division enclosure')

    def render(self, markup, source=None):
        source = self.source if source is None else source
        renderer = source[source.index('  const greek ='):source.index('  function render(n)')]
        shim = '''const p = JSON.parse(require('fs').readFileSync(0, 'utf8'));
function hydrate(n) {
  if (n.nodeType === 3) return n;
  n.getAttribute = k => n.attrs[k] ?? null;
  n.childNodes = n.childNodes.map(hydrate);
  n.children = n.childNodes.filter(c => c.nodeType === 1);
  n.children.forEach((c, i) => c.nextElementSibling = n.children[i + 1] || null);
  return n;
}
const errors = [];
'''
        code = shim + renderer + '\nprocess.stdout.write(JSON.stringify({value:m(hydrate(p)), errors}));'
        process = subprocess.run(['node', '-e', code],
                                 input=json.dumps(dom_tree(ET.fromstring(markup))),
                                 text=True, capture_output=True, check=True, timeout=10)
        return json.loads(process.stdout)

    def test_original_failure_from_saved_markup(self):
        report = json.loads((EVIDENCE.parent/'diagnostics/1791478250261185954/error.json').read_text())
        self.assertIn('Unsupported MathML enclosure', report['message'])
        original = self.source.replace(ADDED, '')
        for markup in self.markups:
            with self.subTest(markup=markup):
                self.assertIn('Unsupported MathML enclosure', self.render(markup, original)['errors'])

    def test_default_enclosure_preserves_every_visible_child(self):
        for markup in self.markups:
            root = ET.fromstring(markup)
            root.tag = 'math'
            plain = self.render(ET.tostring(root, encoding='unicode'))
            enclosed = self.render(markup)
            self.assertEqual(plain['errors'], [])
            self.assertEqual(enclosed['errors'], [])
            self.assertEqual(enclosed['value'], r'\enclose{longdiv}{' + plain['value'] + '}')
            self.assertIn('12', enclosed['value'])
            self.assertIn('25', enclosed['value'])

    def test_explicit_longdiv_matches_default(self):
        for markup in self.markups:
            explicit = markup.replace('<menclose>', '<menclose notation="longdiv">', 1)
            self.assertEqual(self.render(explicit), self.render(markup))

    def test_unknown_or_combined_notation_still_fails(self):
        for notation in ('radical', 'longdiv radical', ''):
            markup = self.markups[0].replace('<menclose>', '<menclose notation="' + notation + '">', 1)
            with self.subTest(notation=notation):
                self.assertEqual(self.render(markup)['errors'], ['Unsupported MathML enclosure'])


if __name__ == '__main__':
    unittest.main()
