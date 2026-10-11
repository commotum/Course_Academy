"""Observed topic colors stay course-qualified and separate from learner state."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from scripts.browser.parsing import parse_progress
from scripts.config import Config
from scripts.post_activity import record
from scripts.progress import compare_progress
from scripts.storage import atomic_json, read_json


def course(identity, color='white', *, topic='1060', captured_at=None):
    return {'course_id': str(identity), 'captured_at': captured_at,
            'topics': [{'topic_id': str(topic), 'title': 'Shared topic',
                        'circle_style': 'border: none; background: ' + color + ';'}]}


class ProgressComparisonTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.config = Config(repo_root=self.root)
        self.directory = self.config.output_root / 'task'
        self.activity = {'task_id': 'task', 'kind': 'review', 'topic_id': '1060'}
        atomic_json(self.directory / 'capture-complete.json', {'completed_at': 100})

    def test_parser_preserves_authored_colors_and_maps_only_known_palette(self):
        colors = ['white', 'rgb(210, 231, 249)', 'rgb(165,207,243)', 'rgb(120, 182, 237)',
                  'rgb(74, 158, 232)', 'rgb(29, 134, 226)', 'rgb(23, 107, 181)',
                  'purple', 'var(--progress)', '']
        rows = ''.join('<tr><td><a class="topicLink" href="/topics/%s?courseId=111">Topic</a>'
                       '<span class="topicCircle" style="background: %s;"></span></td></tr>' % (index, color)
                       for index, color in enumerate(colors))
        result = parse_progress('<table class="moduleTopics">' + rows + '</table>', 111)
        topics = result['topics']
        self.assertEqual([topic['display_band'] for topic in topics], [0, 1, 2, 3, 4, 5, 6, None, None, None])
        self.assertEqual([topic['color_status'] for topic in topics[-3:]], ['unknown', 'unknown', 'missing'])
        self.assertEqual(topics[2]['color'], 'rgb(165,207,243)')
        self.assertEqual(topics[2]['circle_style'], 'background: rgb(165,207,243);')

    def test_completed_read_compares_shared_topics_separately_by_course(self):
        baseline = {'observed_at': 50, 'progress': [course(111, captured_at=48), course(136, captured_at=49)]}
        atomic_json(self.config.state_root / 'progress.json', baseline)
        observation = {'observed_at': 101, 'courses': [course(111, 'rgb(165, 207, 243)', captured_at=102),
                                                      course(136, captured_at=103)],
                       'completion': {'earned_xp': 5}}
        record(self.config, self.activity, self.directory, {}, observation)
        comparison = read_json(self.directory / 'progress-comparison.json')
        self.assertTrue(comparison['comparison_available'])
        self.assertEqual(comparison['compared_topic_count'], 2)
        self.assertEqual(len(comparison['changes']), 1)
        change = comparison['changes'][0]
        self.assertEqual((change['course_id'], change['topic_id']), ('111', '1060'))
        self.assertEqual((change['before_band'], change['after_band']), (0, 2))
        self.assertEqual((change['before_observed_at'], change['after_observed_at']), (48, 102))
        self.assertEqual(read_json(self.directory / 'progress-before.json'), baseline)
        saved = read_json(self.directory / 'post-activity.json')
        self.assertEqual(saved['progress_comparison'], comparison)
        self.assertEqual(saved['observation_history'][0]['progress_comparison'], comparison)
        self.assertIn('not exact FIRe', comparison['limitations'])

    def test_conflicting_link_course_is_excluded_without_losing_valid_rows(self):
        hrefs = ['/topics/1060?courseId=111', '/topics/1061', '/topics/1062?courseId=136']
        rows = ''.join('<tr><td><a class="topicLink" href="%s">Topic</a>'
                       '<span class="topicCircle" style="background: %s;"></span></td></tr>' % (href, color)
                       for href, color in zip(hrefs, ['white', 'white', 'rgb(23, 107, 181)']))
        parsed = parse_progress('<table class="moduleTopics">' + rows + '</table>', 111)
        self.assertEqual([topic['topic_id'] for topic in parsed['topics']], ['1060', '1061'])
        issue = {'reason': 'conflicting_course_identity', 'course_id': '111', 'topic_id': '1062',
                 'href': hrefs[2], 'source_course_ids': ['136']}
        self.assertEqual(parsed['parse_issues'], [issue])
        baseline = course(111)
        baseline['topics'].extend([course(111, topic=topic)['topics'][0] for topic in ('1061', '1062')])
        comparison = compare_progress({'progress': [baseline]}, {'courses': [parsed]})
        self.assertEqual(comparison['compared_topic_count'], 2)
        self.assertEqual(comparison['changes'], [])
        self.assertIn({**issue, 'side': 'current'}, comparison['uncompared_topics'])

    def test_late_retry_uses_immutable_task_baseline_and_actual_read_time(self):
        baseline = {'observed_at': 50, 'progress': [course(111, captured_at=50)]}
        atomic_json(self.config.state_root / 'progress.json', baseline)
        first = {'observed_at': 101, 'missing': ['progress'], 'completion': {'earned_xp': 5}}
        record(self.config, self.activity, self.directory, {}, first)
        atomic_json(self.config.state_root / 'progress.json',
                    {'observed_at': 150, 'progress': [course(111, 'rgb(210, 231, 249)', captured_at=150)]})
        late = {'observed_at': 200, 'late_read': True,
                'courses': [course(111, 'rgb(165, 207, 243)', captured_at=202)]}
        record(self.config, self.activity, self.directory, {}, late)
        record(self.config, self.activity, self.directory, {}, late)  # Replay after interrupted handoff.
        self.assertEqual(read_json(self.directory / 'progress-before.json'), baseline)
        saved = read_json(self.directory / 'post-activity.json')
        self.assertEqual([item['observed_at'] for item in saved['observation_history']], [101, 200])
        first_comparison, late_comparison = [item['progress_comparison'] for item in saved['observation_history']]
        self.assertFalse(first_comparison['comparison_available'])
        self.assertEqual(first_comparison['unavailable_reason'], 'no_current_topics')
        self.assertTrue(late_comparison['late_read'])
        self.assertEqual((late_comparison['baseline_observed_at'], late_comparison['observed_at']), (50, 200))
        self.assertEqual(late_comparison['changes'][0]['before_band'], 0)
        self.assertEqual(late_comparison['changes'][0]['after_observed_at'], 202)
        self.assertEqual(saved['completion']['earned_xp'], 5)
        self.assertEqual(sum(day['earned_xp'] for day in read_json(self.config.state_root / 'daily-xp.json').values()), 5)

    def test_missing_courses_or_topics_are_uncompared_not_false_losses(self):
        first = course(111)
        first['topics'].append({'topic_id': '1061', 'title': 'Missing row', 'color': 'white'})
        before = {'progress': [first, course(136)]}
        result = compare_progress(before, {'courses': [course(111, 'rgb(210,231,249)')]})
        self.assertEqual(len(result['changes']), 1)
        self.assertEqual(result['compared_topic_count'], 1)
        self.assertEqual({(item['course_id'], item['topic_id'], item['reason']) for item in result['uncompared_topics']},
                         {('111', '1061', 'missing_in_current'), ('136', '1060', 'missing_in_current')})

    def test_unknown_color_is_preserved_as_unknown_and_missing_color_is_not_zero(self):
        before = {'progress': [course(111)]}
        result = compare_progress(before, {'courses': [course(111, 'purple')]})
        self.assertEqual(result['changes'][0]['after_color'], 'purple')
        self.assertIsNone(result['changes'][0]['after_band'])
        self.assertEqual(result['changes'][0]['after_color_status'], 'unknown')
        missing = course(111)
        missing['topics'][0].pop('circle_style')
        result = compare_progress(before, {'courses': [missing]})
        self.assertFalse(result['comparison_available'])
        self.assertEqual(result['changes'], [])
        self.assertEqual(result['uncompared_topics'][0]['reason'], 'missing_color')

    def test_no_baseline_and_empty_current_are_explicitly_unavailable(self):
        record(self.config, self.activity, self.directory, {}, {'observed_at': 101, 'courses': [course(111)]})
        comparison = read_json(self.directory / 'progress-comparison.json')
        self.assertFalse(comparison['comparison_available'])
        self.assertEqual(comparison['unavailable_reason'], 'no_baseline_topics')
        self.assertEqual(comparison['changes'], [])
        self.assertEqual(read_json(self.directory / 'progress-before.json'), {})
        later = compare_progress({'progress': [course(111)]}, {'courses': []})
        self.assertFalse(later['comparison_available'])
        self.assertEqual(later['unavailable_reason'], 'no_current_topics')
        self.assertEqual(later['changes'], [])

    def test_equivalent_known_spellings_and_unchanged_colors_are_not_changes(self):
        before = {'progress': [course(111, 'white'), course(136, 'rgb(165, 207, 243)')]}
        after = {'courses': [course(111, '#fff'), course(136, 'rgb(165,207,243)')]}
        result = compare_progress(before, after)
        self.assertTrue(result['comparison_available'])
        self.assertEqual(result['compared_topic_count'], 2)
        self.assertEqual(result['changes'], [])

    def test_duplicate_topic_identity_is_not_arbitrarily_compared(self):
        before = {'progress': [course(111)]}
        duplicate = course(111)
        duplicate['topics'].append({**deepcopy(duplicate['topics'][0]), 'color': 'rgb(165,207,243)'})
        result = compare_progress(before, {'courses': [duplicate]})
        self.assertEqual(result['changes'], [])
        self.assertFalse(result['comparison_available'])
        self.assertTrue(any(item['reason'] == 'duplicate_topic_identity' for item in result['uncompared_topics']))


if __name__ == '__main__':
    unittest.main()
