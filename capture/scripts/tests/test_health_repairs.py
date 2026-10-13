"""Regression checks for source integrity and explicit progress anomalies."""
from copy import deepcopy
import tempfile
from pathlib import Path
from unittest.mock import Mock,patch
import unittest

from scripts.monitor_data import capture_integrity
from scripts import monitor_data
from scripts.progress import compare_progress
from scripts.config import Config
from scripts.recovery import repair_saved_capture
from scripts.storage import atomic_json,read_json
from scripts.tests.test_database import question
from scripts.post_activity import record_progress_health


def progress(color,at):
    percent={'course_id':'113','displayed_progress':'6%' if color=='white' else '98%'}
    return {'observed_at':at,'dashboard_course_progress':percent,'dashboard':{'course_progress':percent},'courses':[{'course_id':'113','topics':[
        {'topic_id':str(i),'title':str(i),'circle_style':'background: '+color+';'}for i in range(100)]}]}


class HealthRepairsTests(unittest.TestCase):
    def test_batch_receipt_parsing_is_shared_and_changed_receipts_are_rechecked(self):
        request={'request_key':'shared','snapshot_edn':'{"attributes" [[1 :question/math-academy-id]] "entities" [{:question/math-academy-id "q-1"}]}'}
        receipt='{:edb/committed true :edb/tx-data [[9 1 "q-2" 8 7 true]]}'
        monitor_data._RECEIPT_CACHE.clear()
        with patch.object(monitor_data,'loads',wraps=monitor_data.loads)as parse:
            for _ in range(20):self.assertEqual(monitor_data._receipt_ids(request,receipt),{'q-2'})
            self.assertEqual(parse.call_count,2)
            changed=receipt.replace('"q-2"','"q-3"')
            self.assertEqual(monitor_data._receipt_ids(request,changed),{'q-3'})
            self.assertEqual(parse.call_count,4)
        with self.assertRaises(ValueError):
            monitor_data._receipt_ids(request,receipt.replace('committed true','committed false'))
    def test_late_diagnostic_read_cannot_clear_a_current_progress_warning(self):
        with tempfile.TemporaryDirectory()as temp:
            config=Config(repo_root=Path(temp))
            atomic_json(config.state_root/'progress-health.json',{'113':{'warning':'Unverified','observed_at':100}})
            activity={'task_id':'old','kind':'diagnostic','course_id':'113'}
            record_progress_health(config,activity,{'observed_at':200,'late_read':True},{'anomalies':[]})
            self.assertEqual(read_json(config.state_root/'progress-health.json')['113']['warning'],'Unverified')
    def test_source_repair_queues_whole_activity_without_a_small_direct_commit(self):
        with tempfile.TemporaryDirectory()as temp:
            config=Config(repo_root=Path(temp),account='linear',math_root=Path(temp)/'math')
            directory=config.output_root/'77';q=question()
            activity={'task_id':'77','kind':'review','topic_id':'1','title':'Addition'}
            content={**activity,'questions':[q],'canonical_examples':[],'tutorials':[]}
            atomic_json(directory/'content.json',content)
            atomic_json(directory/'checkpoint.json',{'activity':activity,'steps':[],'presentations':{},
                'history':content,'judgments':{'questions:q-11':{'question_id':'q-11','record_kind':'questions','answers':[]}}})
            atomic_json(directory/'capture-complete.json',{'completed_at':100})
            marker=(directory/'capture-complete.json').read_bytes()
            with patch('scripts.recovery.DatabasePipeline',side_effect=AssertionError('Direct commit forbidden')):
                result=repair_saved_capture(config,directory,Mock())
            self.assertEqual(result['status'],'queued')
            queued=read_json(next(config.spool_root.glob('*.json')))
            self.assertEqual(queued['status'],'pending')
            self.assertEqual(queued['attempts'],0)
            self.assertEqual((directory/'capture-complete.json').read_bytes(),marker)
            self.assertFalse((config.state_root/'xp.json').exists())
    def test_large_lesson_progress_change_is_not_attributed_to_the_lesson(self):
        before=progress('white',100);after=progress('rgb(23,107,181)',200)
        originals=deepcopy((before,after))
        result=compare_progress(before,after,activity_kind='lesson')
        self.assertTrue(result['comparison_available'])
        self.assertEqual(len(result['changes']),100)
        self.assertFalse(result['attribution_available'])
        self.assertEqual(result['anomalies'][0]['course_id'],'113')
        self.assertEqual((before,after),originals)

    def test_diagnostic_and_slow_changes_do_not_trigger_lesson_anomaly(self):
        before=progress('white',100);after=progress('rgb(23,107,181)',200)
        self.assertEqual(compare_progress(before,after,activity_kind='diagnostic')['anomalies'],[])
        after['observed_at']=5000
        self.assertEqual(compare_progress(before,after,activity_kind='lesson')['anomalies'],[])

    def test_prerequisite_color_propagation_without_percentage_jump_is_not_flagged(self):
        before=progress('white',100);after=progress('rgb(23,107,181)',200)
        after['dashboard']['course_progress']['displayed_progress']='7%'
        self.assertEqual(compare_progress(before,after,activity_kind='lesson')['anomalies'],[])

    def test_pending_repairs_remain_visible_and_protected_corrections_are_separate(self):
        items=[{'capture_directory':'/one','status':'pending','result':{'omissions':[
            {'kind':'question','id':'q-1','reason':'Missing source'},
            {'kind':'question','id':'q-1','reason':'Missing controls'},
            {'kind':'review','reason':'Incomplete activity'}]}},
            {'capture_directory':'/two','status':'verified','result':{'omissions':[
                {'kind':'question','id':'q-2','constraint':'separately_attributed_correction'}]}}]
        self.assertEqual(capture_integrity(items),{'capture_gap_items':1,'capture_gap_activities':1,'preserved_corrections':1})


if __name__=='__main__':
    unittest.main()
