"""Checks for observational units and evidence classification in band analysis."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.analyze_encompassing import analyze, collapse, discover, load_graph, timestamp, wilson
from scripts.analyze_kp_effects import answers, mixed_groups
from scripts.estimate_encompassing_frequency import cadence, estimate


class EncompassingAnalysisTests(unittest.TestCase):
    def test_shared_topic_is_one_observation(self):
        before = {('1', '7'): (2, 10, 'T'), ('2', '7'): (2, 12, 'T')}
        after = {('1', '7'): (3, 20, 'T'), ('2', '7'): (3, 22, 'T')}
        rows, conflicts = collapse(before, after)
        self.assertEqual(rows, {'7': (2, 3, 10, 22, ['1', '2'])})
        self.assertEqual(conflicts, [])

    def test_disagreement_and_absence_are_not_progress_loss(self):
        before = {('1', '7'): (2, 10, 'T'), ('2', '7'): (2, 12, 'T'),
                  ('1', '8'): (4, 10, 'Missing')}
        after = {('1', '7'): (3, 20, 'T'), ('2', '7'): (2, 22, 'T')}
        rows, conflicts = collapse(before, after)
        self.assertEqual(rows, {})
        self.assertEqual(conflicts, ['7'])

    def test_source_grade_overrides_planned_correct_answer(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            run = root/'reference/mathacademy/question-capture/42'
            (run/'knowledge-state').mkdir(parents=True)
            (run/'knowledge-state/review-completed.json').write_text(json.dumps({
                'task_id': 42, 'started_at': '2026-10-11T00:00:00Z',
                'finished_at': '2026-10-11T00:00:10Z', 'courses': [], 'changes': []}))
            (run/'state.json').write_text(json.dumps({'task_type': 'review',
                'topic_id': 7, 'questions': {'q1': {'intended': 'C', 'actual_result': 'Incorrect',
                    'after': {'result': 'Correct'}}}}))
            events = discover(root)
            self.assertEqual(events[0]['grades'], ['Incorrect'])
            self.assertEqual(events[0]['account'], 'foundations')

    def test_small_samples_keep_wide_intervals(self):
        lo, hi = wilson(2, 2)
        self.assertLess(lo, .5)
        self.assertAlmostEqual(hi, 1.)
        self.assertIsNone(wilson(0, 0))

    def test_timestamp_formats_agree(self):
        self.assertEqual(timestamp('1970-01-01T00:01:00Z'), timestamp(60))

    def test_analysis_never_pools_account_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            events = []
            for account, after_color in [('foundations', 'rgb(120, 182, 237)'),
                                          ('linear', 'rgb(165, 207, 243)')]:
                before_path, after_path = root/(account+'-before.json'), root/(account+'-after.json')
                def data(color, at):
                    return {'courses': [{'course_id': 1, 'captured_at': at,
                        'topics': [{'topic_id': 8, 'color': color, 'title': 'T'}]}]}
                before_path.write_text(json.dumps(data('rgb(165, 207, 243)', 10)))
                after_path.write_text(json.dumps(data(after_color, 25)))
                events.append(dict(account=account, task_id='42', source='7', kind='review',
                    pipeline='legacy', path=str(after_path), before_path=str(before_path),
                    time=20, finished_at=25, late=False, grades=['Correct'], outcome='passed',
                    logged=[], first_answer_at=None, earned_xp=5))
            report = analyze(root, 'linear', events)
            self.assertEqual(report['summary']['activities'], 1)
            self.assertEqual(report['changes'], [])
            self.assertEqual(report['pairs'], [])
            self.assertEqual({e['account'] for e in report['activity_audit']}, {'linear'})

    def test_curriculum_graph_uses_one_basis(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            context = root/'.local/capture/linear/context'
            context.mkdir(parents=True)
            (context/'76.json').write_text(json.dumps({'basis': 1, 'graph': {'7': ['8']}}))
            (context/'76-new.json').write_text(json.dumps({'basis': 2, 'graph': {'7': ['9']}}))
            names, graph, sources = load_graph(root, 'linear')
            self.assertEqual(graph, {'7': ['9']})
            self.assertEqual([s['basis'] for s in sources], [2])

    def test_kp_answers_join_current_attempts_and_use_actual_grade(self):
        with tempfile.TemporaryDirectory() as folder:
            run = Path(folder)
            (run/'content.json').write_text(json.dumps({
                'questions': [{'math_academy_id': 'q-1', 'knowledge_point': 'KP', 'difficulty': 'hard'}],
                'attempts': [{'question': {'math_academy_id': 'q-1'}, 'grade': 'Incorrect',
                              'intended': 'C', 'last_observation': {'grade': 'Correct'}}]}))
            self.assertEqual(answers(str(run/'post-activity.json'), 'current'),
                [{'kp': 'KP', 'grade': 'Incorrect', 'question_id': 'q-1', 'difficulty': 'hard'}])

    def test_matched_effects_never_cross_source_or_target(self):
        rows = [{'source': 'A', 'target': 'T', 'rise': True},
                {'source': 'B', 'target': 'T', 'rise': False},
                {'source': 'A', 'target': 'U', 'rise': False}]
        signature = lambda x: (x['source'], x['target'])
        self.assertEqual(mixed_groups(rows, signature), [])
        rows.append({'source': 'A', 'target': 'T', 'rise': False})
        self.assertEqual(mixed_groups(rows, signature), [[rows[0], rows[-1]]])

    def test_frequency_counts_flat_waits_and_trailing_activities(self):
        events = [{'before':a,'after':b} for a,b in [(1,1),(1,1),(1,3),(3,3),(3,4),(4,4)]]
        result = cadence(events)
        self.assertEqual(result['crossing_activity_numbers'], [3,5])
        self.assertEqual(result['activities_to_each_crossing'], [3,2])
        self.assertEqual(result['trailing_activities_without_crossing'], 1)
        self.assertEqual(result['frequency_weight_estimate'], 2/6)
        self.assertEqual(result['summed_upward_band_steps'], 3)
        self.assertEqual(result['multi_band_rising_activities'], 1)

    def test_frequency_does_not_turn_declines_into_credit(self):
        result = cadence([{'before':3,'after':2}, {'before':2,'after':2}])
        self.assertEqual(result['rising_activities'], 0)
        self.assertEqual(result['falling_activities'], 1)
        self.assertEqual(result['trailing_activities_without_crossing'], 2)
        self.assertEqual(result['frequency_weight_estimate'], 0)
        self.assertIsNone(cadence([])['frequency_weight_estimate'])

    def test_single_activity_pair_gets_a_frequency_estimate(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            event = dict(account='linear', task_id='42', source='1961', kind='review',
                         time=20, grades={'Correct':3,'Incorrect':2})
            exposure = dict(task_id='42', kind='review', before=1, after=2, quality_class=3,
                            background_up_rate=.1, snapshot='saved-snapshot.json')
            pair = dict(source='1961',target='2211',source_title='Source',target_title='Target',
                        graph_relation='prerequisite',prerequisite_distance=1,passed_exposures=[exposure])
            (root/'linear.json').write_text(json.dumps(dict(account='linear',
                activity_audit=[event],changes=[],pairs=[pair])))
            report = estimate(root,'linear')
            self.assertEqual(len(report['proposals']),1)
            self.assertEqual(report['proposals'][0]['eligible_activities'],1)
            self.assertEqual(report['proposals'][0]['crossing_activity_numbers'],[1])
            self.assertEqual(report['proposals'][0]['frequency_weight_estimate'],1.)


if __name__ == '__main__':
    unittest.main()
