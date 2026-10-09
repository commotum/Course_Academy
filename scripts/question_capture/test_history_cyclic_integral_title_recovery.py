import html
import json
import re
import unittest
from pathlib import Path
from browser import history_kp_matches

DIAGNOSTIC=Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14042486/diagnostics/1791452799444534801')

class CyclicIntegralHistoryTitleRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state=json.loads((DIAGNOSTIC/'state.json').read_text())
        page=(DIAGNOSTIC/'page.html').read_text()
        cls.history=[re.sub(r'^KP \d+\.\s*','',html.unescape(re.sub('<[^>]+>','',raw))).strip()
                     for raw in re.findall(r'<div class="kpTitle">(.*?)</div>',page,re.S)]
        cls.pairs=[(cls.state['examples']['e-498']['knowledge_point'],cls.history[1]),
                   (cls.state['examples']['e-7313']['knowledge_point'],cls.history[2])]

    def test_observed_two_title_pairs_recover_with_stable_example_mapping(self):
        self.assertEqual(self.state['topic_id'],424)
        for live,history in self.pairs:
            self.assertEqual(history,live.replace('of a Exponential','of an Exponential'))
            self.assertTrue(history_kp_matches(424,live,history))
        record=self.state['questions']['q-49609']
        self.assertEqual(record['kp_id'],self.state['examples']['e-498']['knowledge_point_id'])
        self.assertEqual(record['content']['knowledge_point'],self.pairs[0][0])

    def test_aliases_reject_other_topics_and_other_integral_skills(self):
        for live,history in self.pairs:
            self.assertFalse(history_kp_matches(425,live,history))
            self.assertFalse(history_kp_matches(424,history,live))
            self.assertFalse(history_kp_matches(424,live,history+'s'))
        self.assertFalse(history_kp_matches(424,self.pairs[0][0],self.pairs[1][1]))
        self.assertFalse(history_kp_matches(424,self.pairs[1][0],self.pairs[0][1]))
