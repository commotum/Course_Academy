"""Daily displayed XP, date rollover and per-account progress scopes."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from browser import CaptureBrowser
from capture import arguments
from core import atomic_json
from dashboard import EXTRACT_STATS, record, xp_pair
from fleet import progress_line
from progress import capture, targets

URLS=['https://mathacademy.com/courses/106/progress?unitId=679',
      'https://mathacademy.com/courses/55/progress',
      'https://mathacademy.com/courses/54/progress']


class DashboardTests(unittest.TestCase):
    def test_daily_totals_keep_penalties_deduplicate_and_ignore_yesterday(self):
        rows=[{'task_id':1,'day':'Today','kind':'lesson','points':'8/13 XP'},
              {'task_id':2,'day':'Today','kind':'review','points':'-2/5 XP'},
              {'task_id':3,'day':'Today','kind':'diagnostic','points':'57 XP'},
              {'task_id':4,'day':'Yesterday','kind':'lesson','points':'10/10 XP'}]
        observed={'percent':'70%','course_href':'/courses/136/progress','completed':rows}
        with tempfile.TemporaryDirectory() as work,patch('dashboard.local_date',return_value='2026-10-07'):
            first=record(work,observed)
            second=record(work,observed)
            # Later queues can show fewer rows; already observed tasks are retained.
            partial=record(work,{**observed,'completed':rows[:1]})
            self.assertEqual(first['daily_xp'],{'date':'2026-10-07','earned':63,'base':75,'tasks':3})
            self.assertEqual(first['daily_xp'],second['daily_xp'])
            self.assertEqual(first['daily_xp'],partial['daily_xp'])
            self.assertEqual(first['percent_complete'],70)
            self.assertEqual(first['course_id'],136)
            with patch('dashboard.local_date',return_value='2026-10-08'):
                self.assertEqual(record(work,{**observed,'completed':[]})['daily_xp']['earned'],0)
            self.assertEqual(len(json.loads((Path(work)/'daily-xp.json').read_text())),2)

    def test_fixed_awards_and_large_numbers_use_displayed_points(self):
        self.assertEqual(xp_pair('1,234 / 2,000 XP'),{'earned':1234,'base':2000})
        self.assertEqual(xp_pair('0/10 XP'),{'earned':0,'base':10})
        self.assertEqual(xp_pair('57 XP'),{'earned':57,'base':57})
        self.assertIsNone(xp_pair('Loading'))
        self.assertIn('Today 237/388 XP',progress_line({'daily_xp':{'earned':237,'base':388},'percent_complete':70}))
        self.assertIn('70% [#######---]',progress_line({'percent_complete':70}))

    def test_exact_progress_urls_are_frozen_and_keep_foundations_defaults(self):
        args=arguments(['run',*[part for url in URLS for part in ('--progress-url',url)]])
        self.assertEqual(args.progress_course_ids,[106,55,54])
        self.assertEqual(targets(args),tuple(URLS))
        self.assertTrue(args.progress_course_ids_explicit)
        self.assertEqual(targets(args,{'progress_urls':URLS[:1]}),tuple(URLS[:1]))
        self.assertEqual(targets(arguments(['run'])),(113,111,136))
        for bad in ('https://mathacademy.com/learn','https://mathacademy.com/courses/54/progress?unitId=bad'):
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                arguments(['run','--progress-url',bad])

    def test_snapshot_visits_exact_urls_and_validates_each_course(self):
        reader=Mock();reader.args=SimpleNamespace(settle_ms=0)
        reader.page.evaluate.side_effect=[
            {'declared_topics':['1 topic'],'units_html':'<div id="units"></div>',
             'rows':[{'title':'A topic','href':f'/topics/1?courseId={cid}','color':'white'}]}
            for cid in (106,55,54)]
        with tempfile.TemporaryDirectory() as work:
            result=capture(reader,work,'lesson-completed',123,URLS)
        self.assertEqual([c.args[0] for c in reader.navigate.call_args_list],URLS)
        self.assertEqual([c['course_id'] for c in result['courses']],[106,55,54])
        self.assertEqual(result['courses'][0]['selected_unit_id'],679)
        self.assertTrue(all(c.kwargs=={'force':True} for c in reader.navigate.call_args_list))

    def test_completed_snapshot_recovery_keeps_url_scope_without_reopening_pages(self):
        args=SimpleNamespace(timeout_ms=500,progress_urls=URLS,progress_course_ids=[106,55,54])
        reader=CaptureBrowser(Mock(),args,None,None)
        state={'task_id':123,'task_type':'lesson','progress_urls':URLS}
        saved={'task_id':123,'finished_at':'saved','changes':[],
               'courses':[{'course_id':cid,'source_url':url,'topics':[]} for cid,url in zip((106,55,54),URLS)]}
        with tempfile.TemporaryDirectory() as work:
            atomic_json(Path(work)/'knowledge-state/lesson-completed.json',saved)
            reader.knowledge_snapshot(state,work,'lesson-completed')
        self.assertIn('lesson-completed',state['knowledge_snapshots'])
        self.assertIsNone(reader.progress_reader)


class DashboardDOMTests(unittest.TestCase):
    def test_real_dom_uses_today_task_points_and_course_percent_not_goal_points(self):
        from playwright.sync_api import sync_playwright
        html='''<a id="courseNameLink" href="/courses/54/progress">Multivariable Calculus</a>
        <div id="coursePercentComplete">12.5%</div><div id="dailyGoalPoints">999/50 XP</div>
        <div id="completedTasks">
          <div class="taskCompleted" id="task-1"><input class="taskCompletedDate" value="Today">
            <span class="taskTypeLocked">Lesson</span><span class="taskPoints">8<span>/</span><span>13 XP</span></span></div>
          <div class="taskCompleted" id="task-2"><input class="taskCompletedDate" value="Yesterday">
            <span class="taskTypeLocked">Review</span><span class="taskPoints">4/7 XP</span></div>
        </div>'''
        with sync_playwright() as runtime:
            browser=runtime.chromium.launch(headless=True)
            try:
                page=browser.new_page(offline=True);page.set_content(html)
                observed=page.evaluate(EXTRACT_STATS)
                with tempfile.TemporaryDirectory() as work:stats=record(work,observed)
                self.assertEqual(stats['daily_xp']['earned'],8)
                self.assertEqual(stats['daily_xp']['base'],13)
                self.assertEqual(stats['percent_complete'],12.5)
            finally:browser.close()


if __name__=='__main__':unittest.main()
