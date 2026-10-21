"""Real process locks and shared state protect concurrent cohort workers."""
from contextlib import ExitStack
import fcntl
import multiprocessing as mp
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from generator_cohort import CampaignStore, slot_lock_path, supervise
from inventory_jobs import save


def claim_and_hold(directory,locks,slot,ready,release):
    store=CampaignStore(directory)
    with slot_lock_path(Path(directory),slot).open('a') as worker:
        fcntl.flock(worker,fcntl.LOCK_EX)
        item,kp_lock=store.claim(Path(locks),slot)
        with kp_lock:
            ready.put((slot,item['kp']))
            release.wait(10)
            item.update(state='verified',test_slot=slot)
            store.update(item)


class ParallelCohortTests(unittest.TestCase):
    def setup_store(self,directory,count=6):
        directory=Path(directory);locks=directory/'locks';locks.mkdir()
        save(directory/'cohort.json',{'cutoff':'2026-10-16','captured_basis':1,
            'learner':'test','items':[{'kp':i,'state':'pending',
            'priority_subjects':['linear algebra'] if i<3 else []} for i in range(count)]})
        return CampaignStore(directory),locks

    def test_three_processes_claim_priority_jobs_and_keep_all_completions(self):
        with tempfile.TemporaryDirectory() as t:
            store,locks=self.setup_store(t)
            ctx=mp.get_context('spawn');ready=ctx.Queue();release=ctx.Event()
            children=[ctx.Process(target=claim_and_hold,args=(t,str(locks),slot,ready,release)) for slot in range(3)]
            try:
                for child in children:child.start()
                claims=[ready.get(timeout=10) for _ in children]
                self.assertEqual({kp for _,kp in claims},{0,1,2})
                status=store.status()
                self.assertEqual(len(status['active_jobs']),3)
                self.assertEqual(status['states'],{'running':3,'pending':3})
                release.set()
                for child in children:
                    child.join(10);self.assertEqual(child.exitcode,0)
                status=store.status()
                self.assertEqual(status['states'],{'verified':3,'pending':3})
                with store.locked() as campaign:
                    self.assertEqual({i['test_slot'] for i in campaign['items'][:3]},set(range(3)))
            finally:
                release.set()
                for child in children:
                    if child.is_alive():child.terminate()
                    child.join(10)

    def test_running_job_reclaimed_only_after_actual_lock_release(self):
        with tempfile.TemporaryDirectory() as t:
            store,locks=self.setup_store(t,2)
            item,held=store.claim(locks,0)
            try:
                other,other_lock=store.claim(locks,1)
                try:
                    self.assertEqual(other['kp'],1)
                    self.assertIsNone(store.claim(locks,2))
                finally:other_lock.close()
            finally:held.close()
            resumed,resumed_lock=store.claim(locks,2)
            try:
                self.assertEqual(resumed['kp'],item['kp'])
                self.assertEqual(resumed['worker_slot'],2)
            finally:resumed_lock.close()

    def test_pause_and_capacity_limit_stop_new_claims_but_preserve_inflight_updates(self):
        with tempfile.TemporaryDirectory() as t:
            store,locks=self.setup_store(t)
            item,held=store.claim(locks,0)
            try:
                marker=Path(t)/'stop-after-current';marker.touch()
                self.assertIsNone(store.claim(locks,1))
                item['state']='verified';store.update(item)
                marker.unlink()
                next_item,next_lock=store.claim(locks,1)
                try:
                    next_item['state']='pending';store.update(next_item,capacity_error='limit')
                    self.assertIsNone(store.claim(locks,2))
                    self.assertEqual(store.status()['states']['verified'],1)
                finally:next_lock.close()
            finally:held.close()

    def test_supervisor_restarts_only_the_failed_slot(self):
        with tempfile.TemporaryDirectory() as t:
            store,_=self.setup_store(t)
            failed=Mock();failed.poll.return_value=1
            healthy_a=Mock();healthy_a.poll.side_effect=[None,0]
            healthy_b=Mock();healthy_b.poll.side_effect=[None,0]
            replacement=Mock();replacement.poll.return_value=0
            with patch('generator_cohort.subprocess.Popen',side_effect=[failed,healthy_a,healthy_b,replacement]) as launch, \
                    patch('generator_cohort.time.monotonic',side_effect=[0,0,0,0,16]), \
                    patch('generator_cohort.time.sleep'):
                supervise(t,3)
            slots=[c.args[0][-1] for c in launch.call_args_list]
            self.assertEqual(slots,['0','1','2','0'])
            self.assertEqual(store.status()['worker_count'],3)

    def test_slot_locks_preserve_legacy_exclusion_and_exactly_three_slots(self):
        with tempfile.TemporaryDirectory() as t, ExitStack() as stack:
            directory=Path(t)
            self.assertEqual(slot_lock_path(directory,0),directory/'worker.lock')
            for slot in range(3):
                first=stack.enter_context(slot_lock_path(directory,slot).open('a'))
                fcntl.flock(first,fcntl.LOCK_EX|fcntl.LOCK_NB)
                second=stack.enter_context(slot_lock_path(directory,slot).open('a'))
                with self.assertRaises(BlockingIOError):fcntl.flock(second,fcntl.LOCK_EX|fcntl.LOCK_NB)
            with self.assertRaises(ValueError):slot_lock_path(directory,3)


if __name__=='__main__':unittest.main()
