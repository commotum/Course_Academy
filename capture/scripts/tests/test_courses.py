from pathlib import Path
import tempfile
import unittest
from scripts.config import Config
from scripts.courses import course_label, parse_current_course, record_current_course
from scripts.monitor import snapshot
from scripts.storage import atomic_json


class CourseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config(repo_root=self.root, account='linear')

    def test_enrollment_comes_from_header_not_review_course(self):
        html = '<a id="courseNameLink" href="/courses/76/progress">Methods of Proof</a><div class="taskCourseNameUnlocked">Precalculus</div>'
        self.assertEqual(parse_current_course(html), {'course_id': '76', 'course_name': 'Methods of Proof'})
        record_current_course(self.config, html, 'https://mathacademy.com/learn')
        self.assertEqual(self.config.course_id, '76')
        self.assertEqual(course_label(self.config), 'Methods of Proof')
        self.assertEqual(snapshot(self.config)['label'], 'Methods of Proof')

    def test_observed_enrollment_wins_over_old_profile_and_survives_pages_without_header(self):
        atomic_json(self.root / '.local/question_capture-workers/linear/profile-auth.json', {'course_id': '55'})
        record_current_course(self.config, '<a id="courseNameLink" href="/courses/76/progress">Methods of Proof</a>')
        self.assertEqual(Config(repo_root=self.root, account='linear').course_id, '76')
        self.assertEqual(record_current_course(self.config, '<div>Question</div>'), {})
        self.assertEqual(course_label(self.config), 'Methods of Proof')
        record_current_course(self.config, '<a id="courseNameLink" href="/courses/145/progress">Mathematics for Machine Learning</a>')
        self.assertEqual(snapshot(self.config)['label'], 'Mathematics for Machine Learning')
        self.assertEqual(self.config.account, 'linear')


if __name__ == '__main__':
    unittest.main()
