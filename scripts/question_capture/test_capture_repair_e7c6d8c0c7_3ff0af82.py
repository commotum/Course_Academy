import ast
import json
import re
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

SOURCE = Path(__file__).with_name('browser.py')
ACTIVITY = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/multivariable/14038412')
ADDED = "        (3570, 'Expressing Part of a Shifted Sphere in Spherical Coordinates'):\n            'Expressing a Shifted Sphere or Part of a Shifted Sphere in Spherical Coordinates',\n"


def matcher(source):
    parsed = ast.parse(source)
    functions = [node for node in parsed.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name in ('kp_title_identity', 'history_kp_matches')]
    if len(functions) != 2:
        raise AssertionError('Expected both production title helpers')
    namespace = {'re': re}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), 'exec'), namespace)
    return namespace['history_kp_matches']


class SavedShiftedSphereTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text()
        cls.current = staticmethod(matcher(cls.source))
        state = json.loads((ACTIVITY / 'state.json').read_text())
        cls.topic_id = state['topic_id']
        assert cls.topic_id == 3570
        page = BeautifulSoup((ACTIVITY / 'diagnostics/1791446422954279316/page.html').read_text(), 'html.parser')
        cls.pairs = {}
        for question in page.select('.kp .question'):
            mid = question['id'].replace('question-', 'q-')
            title = question.find_parent(class_='kp').select_one('.kpTitle').get_text().strip()
            title = re.sub(r'^KP \d+\.\s*', '', title).strip()
            record = state['questions'][mid]
            cls.pairs[mid] = (record['content']['knowledge_point'], title)
        assert set(cls.pairs) == set(state['questions'])
        assert len(cls.pairs) == 20

    def test_original_saved_failure(self):
        self.assertEqual(self.source.count(ADDED), 1)
        original = matcher(self.source.replace(ADDED, '', 1))
        rejected = {mid for mid, pair in self.pairs.items()
                    if not original(self.topic_id, *pair)}
        self.assertEqual(rejected, {'q-161850', 'q-161882', 'q-161854', 'q-161888', 'q-161844'})

    def test_all_saved_mappings_pass(self):
        for mid, pair in self.pairs.items():
            with self.subTest(question=mid):
                self.assertTrue(self.current(self.topic_id, *pair))

    def test_alias_does_not_allow_unrelated_mappings(self):
        live, history = self.pairs['q-161850']
        self.assertNotEqual(live, history)
        self.assertFalse(self.current(3571, live, history))
        self.assertFalse(self.current(3570, history, live))
        self.assertFalse(self.current(3570, live, history + 's'))
        self.assertFalse(self.current(3570, live + 's', history))
        unrelated = self.pairs['q-161833'][0]
        self.assertFalse(self.current(3570, unrelated, history))
        self.assertFalse(self.current(3570, live, unrelated))


if __name__ == '__main__':
    unittest.main()
