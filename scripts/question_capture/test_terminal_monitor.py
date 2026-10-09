"""Chart scaling and readable terminal cards at common terminal widths."""
import re
import unittest

from terminal_monitor import bars, render


class MonitorTests(unittest.TestCase):
    def rows(self):
        return [{'window':name,'status':'RUNNING' if i==0 else 'COMPLETE',
                 'percent_complete':12.5,'daily_xp':{'earned':30,'base':50},
                 'activity_counts':{'lesson':2,'review':3},'database_questions':{'added':5,'updated':10},
                 'recent_activities':[{'earned':xp} for xp in (0,10,20,40)],'detail':'Capturing lesson'}
                for i,name in enumerate(['Mathematical Foundations','Linear Algebra','Multivariable Calculus','Differential Equations'])]

    def test_bars_share_scale_keep_last_twenty_and_show_zero_and_penalties(self):
        self.assertEqual(bars([{'earned':10},{'earned':20},{'earned':40}],40,length=3),'▂▄█')
        self.assertEqual(bars([{'earned':-2},{'earned':0}],40,length=2),'↓·')
        self.assertEqual(bars([{'earned':1}]*21,8),'▁'*20)

    def test_cards_fit_eighty_columns_and_eighteen_rows_without_graded_counts(self):
        text=render(self.rows(),80)
        self.assertEqual(len(text.splitlines()),18)
        self.assertTrue(all(len(line)<=80 for line in text.splitlines()))
        self.assertIn('Differential Equations',text)
        self.assertIn('30/50 XP',text)
        self.assertIn('L2 R3',text)
        self.assertIn('DB +5 new / 10 existing',text)
        self.assertIn('0–40 XP',text)
        self.assertNotIn('graded',text.lower())
        colored=render(self.rows(),80,color=True)
        self.assertEqual(re.sub(r'\x1b\[[0-9;]*m','',colored),text)

    def test_blocked_card_and_heading_are_visible_at_eighty_columns(self):
        rows=self.rows()
        rows[1].update(status='BLOCKED',detail='2 queued activities await recovery')
        text=render(rows,80)
        self.assertIn('1 running · 1 blocked',text)
        self.assertIn('BLOCKED',text)
        self.assertIn('2 queued activities',text)
        self.assertTrue(all(len(line)<=80 for line in text.splitlines()))
        self.assertEqual(re.sub(r'\x1b\[[0-9;]*m','',render(rows,80,color=True)),text)
