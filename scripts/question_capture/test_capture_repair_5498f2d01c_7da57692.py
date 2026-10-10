import ast
import copy
import re
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
import assessment

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14095701/diagnostics/1791637321225588461/page.html')

class DiagnosticFullCreditTests(unittest.TestCase):
    def setUp(self):
        soup = BeautifulSoup(EVIDENCE.read_text(), 'html.parser')
        q = soup.find(id='question-184579')
        self.assertIsNotNone(q)
        self.metadata = {'id':q['id'], 'kp_href':q.select_one('.questionKP')['href'],
                         'kp_title':q.select_one('.questionKP').get_text(strip=True),
                         'result':q.select_one('.answerResult').get_text(strip=True)}
        self.assertEqual(self.metadata['result'], 'Full Credit')
        self.assertEqual(self.metadata['kp_href'], '/topics/4343#13279')
        source = Path(assessment.__file__).read_text()
        fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'assessment_history')
        self.loop = next(n for n in fn.body if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == 'question')
        self.loop_source = ast.get_source_segment(source, self.loop)
        self.guard = next(n for n in ast.walk(fn) if isinstance(n, ast.If) and any(isinstance(x, ast.Raise) and 'Assessment question has no source KP or grade' in ast.unparse(x) for x in n.body))

    def canonicalize(self, original=False):
        metadata = [copy.deepcopy(self.metadata)]
        if original:
            metadata[0]['source_result'] = metadata[0]['result']
        else:
            exec(compile(ast.Module(body=[copy.deepcopy(self.loop)], type_ignores=[]), '<metadata-loop>', 'exec'), {'metadata':metadata})
        return metadata[0]

    def rejected(self, q):
        source = re.fullmatch(r'/topics/(\d+)#(\d+)', q['kp_href'] or '')
        return eval(compile(ast.Expression(copy.deepcopy(self.guard.test)), '<history-guard>', 'eval'), {'q':q, 'source':source})

    def test_original_reader_rejects_authentic_full_credit(self):
        self.assertTrue(self.rejected(self.canonicalize(original=True)))

    def test_full_credit_is_accepted_and_authentic_label_retained(self):
        q = self.canonicalize()
        self.assertEqual(q['result'], 'Correct')
        self.assertEqual(q['source_result'], 'Full Credit')
        self.assertFalse(self.rejected(q))

    def test_missing_kp_still_fails(self):
        q = self.canonicalize()
        q['kp_href'] = None
        self.assertTrue(self.rejected(q))

    def test_unknown_grade_still_fails(self):
        self.metadata['result'] = 'Pending'
        q = self.canonicalize()
        self.assertEqual(q['source_result'], 'Pending')
        self.assertTrue(self.rejected(q))

    def test_no_credit_is_not_promoted(self):
        self.metadata['result'] = 'No Credit'
        q = self.canonicalize()
        self.assertEqual(q['result'], 'No Credit')
        self.assertEqual(q['source_result'], 'No Credit')

if __name__ == '__main__':
    unittest.main()
