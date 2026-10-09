import html
import json
import re
import unittest
from pathlib import Path
from browser import history_kp_matches

DIAGNOSTIC = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/differential/14042403/diagnostics/1791451825754856047')

class TaylorHistoryTitleRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        state = json.loads((DIAGNOSTIC / 'state.json').read_text())
        cls.topic = state['topic_id']
        cls.live = state['questions']['q-83463']['content']['knowledge_point']
        page = (DIAGNOSTIC / 'page.html').read_text()
        preceding = page[:page.index('id="question-83463"')]
        raw = re.findall(r'<div class="kpTitle">(.*?)</div>', preceding, re.S)[-1]
        cls.history = re.sub(r'^KP \d+\.\s*', '', html.unescape(re.sub('<[^>]+>', '', raw))).strip()

    def test_observed_exact_title_pair_recovers(self):
        self.assertEqual(self.topic, 36)
        self.assertEqual(self.live, 'Finding the a General Term for the Derivative of a Taylor Series')
        self.assertEqual(self.history, 'Finding the General Term for the Derivative of a Taylor Series')
        self.assertTrue(history_kp_matches(self.topic, self.live, self.history))

    def test_alias_does_not_merge_other_topics_or_skills(self):
        self.assertFalse(history_kp_matches(37, self.live, self.history))
        self.assertFalse(history_kp_matches(self.topic, self.live, self.history.replace('Derivative', 'Integral')))
        self.assertFalse(history_kp_matches(self.topic, self.live, self.history + 's'))
        self.assertFalse(history_kp_matches(self.topic, self.history, self.live))
