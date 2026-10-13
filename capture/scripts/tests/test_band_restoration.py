"""Guard the observational units and censoring used to compare activity types."""
import json
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from scripts.analyze_band_restoration import analyze, common_scope, compact_snapshot, followup
from scripts.extract_assessed_topics import extract
from scripts.progress import PALETTE


COLORS = {band: 'rgb(%s)' % ', '.join(map(str, rgb)) for rgb, band in PALETTE.items()}


def course(course_id, at, bands):
    return {'course_id': str(course_id), 'captured_at': at,
            'topics': [{'topic_id': str(topic), 'color': COLORS[band],
                        'title': 'Topic ' + str(topic)} for topic, band in bands.items()]}


class RestorationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def save(self, name, value):
        path = self.folder / name
        path.write_text(json.dumps(value))
        return str(path)

    def fixture(self, kind='assessment', before_courses=None, after_courses=None):
        before = self.save('before.json', {'courses': before_courses or [course('10', 100, {'1': 1, '2': 1, '3': 5})]})
        after = self.save('after.json', {'courses': after_courses or [course('10', 200, {'1': 6, '2': 2, '3': 2})]})
        audit = {'account': 'linear', 'task_id': '1000', 'kind': kind,
                 'source': None if kind in ('assessment', 'multistep') else '1',
                 'time': 150, 'finished_at': 200, 'pipeline': 'legacy',
                 'outcome': None if kind in ('assessment', 'multistep') else 'passed',
                 'grades': {'Correct': 2, 'Incorrect': 1},
                 'exclusion_reasons': ['multiple_or_nonpractice_origins'] if kind == 'assessment' else []}
        source = {'account': 'linear', 'activity_audit': [audit],
                  'sources': [{'account': 'linear', 'task_id': '1000', 'path': after, 'before_path': before}]}
        assessed = {'1000': {'topics': ['1', '2'], 'questions': [
            {'topic': '1', 'grade': 'Correct'}, {'topic': '2', 'grade': 'Correct'},
            {'topic': '2', 'grade': 'Incorrect'}]}}
        return source, assessed

    def test_valid_multi_topic_assessment_needs_no_single_source_or_pass_label(self):
        source, assessed = self.fixture()
        stats, jumps = common_scope(source, assessed)
        self.assertEqual(stats['groups']['kind:assessment']['topic_opportunities'], 3)
        self.assertEqual(stats['groups']['direct_kind:assessment']['topic_opportunities'], 2)
        self.assertEqual(stats['groups']['kind:assessment']['falls'], 1)
        self.assertEqual(stats['groups']['kind:assessment']['one_to_six'], 1)
        self.assertEqual(len(jumps), 1)
        self.assertIsNone(jumps[0]['source'])
        self.assertTrue(jumps[0]['direct'])
        self.assertEqual(jumps[0]['target_question_grades'], {'Correct': 1})

    def test_lesson_review_assessment_and_multistep_share_topic_denominator(self):
        totals = []
        for kind in ('lesson', 'review', 'assessment', 'multistep'):
            with self.subTest(kind=kind):
                source, assessed = self.fixture(kind=kind)
                stats, _ = common_scope(source, assessed)
                row = stats['groups']['kind:' + kind]
                totals.append((row['topic_opportunities'], row['large_jump_targets'], row['falls']))
        self.assertEqual(totals, [(3, 1, 1)] * 4)

    def test_unchanged_targets_remain_in_the_denominator(self):
        source, assessed = self.fixture(after_courses=[course('10', 200, {'1': 1, '2': 1, '3': 5})])
        stats, jumps = common_scope(source, assessed)
        self.assertEqual(stats['groups']['kind:assessment']['topic_opportunities'], 3)
        self.assertEqual(stats['groups']['kind:assessment']['rises'], 0)
        self.assertFalse(jumps)

    def test_course_change_is_not_matched_as_topic_progress(self):
        source, assessed = self.fixture(after_courses=[course('11', 200, {'1': 6, '2': 2, '3': 2})])
        stats, jumps = common_scope(source, assessed)
        self.assertFalse(stats['groups'])
        self.assertFalse(jumps)

    def test_agreeing_course_displays_count_once_and_conflicts_are_removed(self):
        for band, expected in ((6, 1), (3, 0)):
            with self.subTest(second_course_band=band):
                source, assessed = self.fixture(
                    before_courses=[course('10', 100, {'1': 1}), course('11', 101, {'1': 1})],
                    after_courses=[course('10', 200, {'1': 6}), course('11', 201, {'1': band})])
                stats, jumps = common_scope(source, assessed)
                self.assertEqual(len(jumps), expected)
                if expected:
                    self.assertEqual(stats['groups']['kind:assessment']['topic_opportunities'], 1)
                else:
                    self.assertEqual(stats['exclusions']['course_conflicting_topics'], 1)

    def test_intervening_activity_invalidates_all_task_types_equally(self):
        for kind in ('review', 'lesson', 'assessment', 'multistep'):
            source, assessed = self.fixture(kind=kind)
            source['activity_audit'].append(dict(source['activity_audit'][0], task_id='other', time=175))
            stats, jumps = common_scope(source, assessed)
            self.assertFalse(jumps, kind)
            self.assertFalse(stats['groups'], kind)

    def test_snapshot_keeps_courses_separate_and_quarantines_duplicate_identity(self):
        path = self.save('ambiguous.json', {'observations': {'courses': [
            course('10', 100, {'1': 1}), course('11', 100, {'1': 6}),
            course('10', 100, {'1': 3})]}})
        snapshot = compact_snapshot(path, {'1'})
        self.assertNotIn(('10', '1'), snapshot)
        self.assertEqual(snapshot[('11', '1')][1], 6)

    def test_diagnostic_boundary_censors_reversal_after_it(self):
        result = followup([(1800, 6, 'ordinary'), (10800, 1, 'after-diagnostic')], 0, 1, 6, 7200)
        self.assertIsNone(result['first_return_to_baseline'])
        self.assertTrue(result['right_censored_6h'])
        self.assertEqual(result['censor_reason'], 'next_diagnostic')
        self.assertEqual(result['observations'], 1)

    def test_partial_fall_differs_from_loss_of_entire_gain(self):
        result = followup([(1800, 2, 'partial')], 0, 1, 6, None)
        self.assertFalse(result['endpoint_never_fell'])
        self.assertTrue(result['retained_some_gain'])
        self.assertIsNone(result['first_return_to_baseline'])
        result = followup([(1800, 1, 'reversed')], 0, 1, 6, None)
        self.assertFalse(result['retained_some_gain'])
        self.assertEqual(result['first_return_to_baseline']['hours'], 0.5)

    def test_distant_read_alone_does_not_establish_six_hour_retention(self):
        result = followup([(7 * 3600, 1, 'distant-reversal')], 0, 1, 6, None)
        self.assertEqual(result['observations'], 0)
        self.assertFalse(result['same_course_coverage_6h'])

    def test_boundary_reversal_does_not_count_as_confirmed_persistence(self):
        result = followup([(1800, 6, 'early'), (6.1 * 3600, 1, 'boundary')], 0, 1, 6, None)
        self.assertTrue(result['same_course_coverage_6h'])
        self.assertTrue(result['endpoint_never_fell'])  # Strictly within six hours only.
        self.assertFalse(result['confirmed_endpoint_through_6h'])
        self.assertFalse(result['confirmed_some_gain_through_6h'])
        result = followup([(1800, 6, 'early'), (6.1 * 3600, 2, 'boundary')], 0, 1, 6, None)
        self.assertFalse(result['confirmed_endpoint_through_6h'])
        self.assertTrue(result['confirmed_some_gain_through_6h'])

    def test_white_source_initialization_has_a_separate_denominator(self):
        source, assessed = self.fixture(kind='lesson',
            before_courses=[course('10', 100, {'1': 0, '2': 1})],
            after_courses=[course('10', 200, {'1': 1, '2': 6})])
        stats, jumps = common_scope(source, assessed)
        self.assertEqual(stats['direct_lesson_initialization']['all'],
                         {'activities': 1, 'after_band_counts': {'1': 1}})
        self.assertEqual(stats['groups']['kind:lesson']['topic_opportunities'], 1)
        self.assertEqual(len(jumps), 1)
        self.assertEqual(jumps[0]['target'], '2')

    def test_assessment_topic_identity_ignores_incidental_solution_links(self):
        self.assertEqual(extract({'html': '<a href="/topics/22">solution link</a>'}), [])
        self.assertEqual(extract({'html': '<a class="questionKP other" href="/topics/22#kp-3">KP</a>'}), ['22'])
        self.assertEqual(extract({'topic_id': 11, 'html': '<a class="questionKP" href="/topics/22#kp">KP</a>'}), ['11', '22'])

    def prepare_timeline_fixture(self, conflicting_copy=False):
        source, assessed = self.fixture()
        cloned = self.save('cloned-baseline.json', {'courses': [course('10', 200, {'1': 1 if conflicting_copy else 6})]})
        final = self.save('final.json', {'courses': [course('10', 500, {'1': 1 if conflicting_copy else 6})]})
        source['activity_audit'].append(dict(source['activity_audit'][0], task_id='1001',
            kind='review', source='2', time=450, finished_at=500, outcome='passed', exclusion_reasons=[]))
        source['sources'].append({'account': 'linear', 'task_id': '1001', 'path': final, 'before_path': cloned})
        self.save('linear.json', source)
        (self.folder / 'timing-magnitude').mkdir()
        self.save('timing-magnitude/linear.json', {'account': 'linear', 'observations': [], 'activity_batches': []})
        (self.folder / 'restoration-analysis').mkdir()
        self.save('restoration-analysis/assessment-topics.json', {'accounts': {'linear': assessed}})

    def test_reused_next_activity_baseline_does_not_add_a_new_read(self):
        self.prepare_timeline_fixture()
        with contextlib.redirect_stdout(io.StringIO()):
            result = analyze(self.folder, 'linear')
        self.assertEqual(result['method']['unique_course_topic_reads'], 3)
        self.assertEqual(len(result['events']), 1)
        self.assertEqual(result['events'][0]['contexts'][0]['followup']['observations'], 1)

    def test_conflicting_same_time_baseline_copy_is_quarantined(self):
        self.prepare_timeline_fixture(conflicting_copy=True)
        with contextlib.redirect_stdout(io.StringIO()):
            result = analyze(self.folder, 'linear')
        self.assertEqual(result['method']['conflicting_same_time_topic_reads_quarantined'], 1)
        self.assertEqual(result['method']['unique_course_topic_reads'], 2)

    def test_mismatched_account_reports_are_rejected(self):
        self.save('linear.json', {'account': 'multivariable'})
        (self.folder / 'timing-magnitude').mkdir()
        self.save('timing-magnitude/linear.json', {'account': 'linear'})
        with self.assertRaises(AssertionError):
            analyze(self.folder, 'linear')


if __name__ == '__main__':
    unittest.main()
