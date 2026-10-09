"""Saved source conflicts have bounded, activity-scoped diagnosis budgets."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from capture_repair import evidence_version,failure_key,legacy_failure_key,next_failure,migrate_ledger
from core import atomic_json

class CaptureRetryBudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.args=SimpleNamespace(output=self.root/'captures',state_dir=self.root/'state',edb_bin=None)
    def diagnostic(self,task,number,uncertain=True):
        d=self.args.output/str(task);p=d/'diagnostics'/str(number)/'error.json';p.parent.mkdir(parents=True)
        r={'phase':'activity','task_id':task,'exception_type':'ValueError',
           'message':'Solver is uncertain; question saved for review' if uncertain else 'Unknown widget'}
        atomic_json(p,r);atomic_json(d/'state.json',{'task_id':task,'questions':{}})
        (p.parent/'page.html').write_text('volatile editor '+str(number));(p.parent/'page.png').write_bytes(str(number).encode())
        atomic_json(d/'q-1-before.json',{'problem':'Separate improper integrals','fields':[{'key':'a','type':'blank'}],'result':None})
        return p,r
    def record(self,p,r,status='failed',attempts=2):
        return {failure_key(r):{'attempts':attempts,'source_version':'one','status':status,
            'evidence_version':evidence_version(p),'diagnostic':str(p)}}
    def test_strict_repair_schema_requires_every_property(self):
        from capture_repair import SCHEMA,INSTRUCTIONS
        def check(schema):
            if schema.get('type')=='object':
                self.assertFalse(schema['additionalProperties'])
                self.assertEqual(set(schema['required']),set(schema['properties']))
                for field in schema['properties'].values():check(field)
            elif schema.get('type')=='array':check(schema['items'])
        check(SCHEMA)
        self.assertEqual(SCHEMA['properties']['retry_on_source_change'],{'type':'boolean'})
        self.assertIn('set retry_on_source_change=true',INSTRUCTIONS)
    def test_older_diagnostic_cannot_reopen_latest_interaction_failure(self):
        old,r=self.diagnostic(1,1,False);new,r=self.diagnostic(1,2,False)
        ledger=self.record(new,r)
        with patch('capture_repair.source_version',return_value='one'):
            self.assertIsNone(next_failure(self.args,ledger))
    def test_full_page_pixels_and_bookkeeping_do_not_reopen_solver_conflict(self):
        old,r=self.diagnostic(1,1);ledger=self.record(old,r,'blocked')
        new,r=self.diagnostic(1,2)
        atomic_json(new.parents[2]/'state.json',{'task_id':1,'questions':{},'deferred_error':{'diagnostics':'new'},'updated_at':99})
        self.assertEqual(evidence_version(old),evidence_version(new))
        with patch('capture_repair.source_version',return_value='one'):
            self.assertIsNone(next_failure(self.args,ledger))
    def test_activity_collision_does_not_block_other_task(self):
        first,r=self.diagnostic(1,1);ledger=self.record(first,r,'blocked')
        other,r2=self.diagnostic(2,2)
        self.assertNotEqual(failure_key(r),failure_key(r2))
        with patch('capture_repair.source_version',return_value='one'):
            self.assertEqual(next_failure(self.args,ledger)[0],other)
    def test_source_conflict_ignores_unrelated_code_but_changed_source_reopens(self):
        p,r=self.diagnostic(1,1);ledger=self.record(p,r,'blocked');ledger[failure_key(r)]['retry_on_source_change']=False
        with patch('capture_repair.source_version',return_value='two'):
            self.assertIsNone(next_failure(self.args,ledger))
            atomic_json(p.parents[2]/'q-1-before.json',{'problem':'Corrected shared finite cutoff','fields':[]})
            self.assertEqual(next_failure(self.args,ledger)[0],p)
    def test_grade_input_and_interaction_source_changes_reopen(self):
        p,r=self.diagnostic(1,1);ledger=self.record(p,r,'blocked');ledger[failure_key(r)]['retry_on_source_change']=False
        atomic_json(p.parents[2]/'q-1-after.json',{'problem':'Separate improper integrals','result':'Correct','worked_solution':'Authoritative explanation'})
        with patch('capture_repair.source_version',return_value='one'):
            self.assertEqual(next_failure(self.args,ledger)[0],p)
        p2,r2=self.diagnostic(2,2,False);ledger=self.record(p2,r2)
        with patch('capture_repair.source_version',return_value='two'):
            self.assertEqual(next_failure(self.args,ledger)[0],p2)
    def test_queued_resume_reuses_source_conflict_then_recovers_changed_evidence(self):
        from capture import queued_resume
        p,r=self.diagnostic(1,1);ledger=self.record(p,r,'blocked')
        ledger[failure_key(r)]['retry_on_source_change']=False
        atomic_json(self.args.state_dir/'capture-repair/failures.json',ledger)
        atomic_json(p.parents[2]/'state.json',{'task_id':1,'questions':{},'deferred_error':{'diagnostics':str(p.parent)}})
        with patch('capture_repair.source_version',return_value='two'):
            self.assertIsNone(queued_resume(self.args,[{'task_id':1}],set()))
            atomic_json(p.parents[2]/'q-1-before.json',{'problem':'Corrected source','fields':[]})
            self.assertEqual(queued_resume(self.args,[{'task_id':1}],set()),p.parents[2].resolve())
    def test_current_deferred_error_supersedes_old_resolved_interaction_diagnostic(self):
        old,r1=self.diagnostic(1,1,False);current,r=self.diagnostic(1,2)
        atomic_json(current.parents[2]/'state.json',{'task_id':1,'questions':{},'deferred_error':{'diagnostics':str(current.parent)}})
        ledger=self.record(current,r,'blocked');ledger[failure_key(r)]['retry_on_source_change']=False
        with patch('capture_repair.source_version',return_value='two'):
            self.assertIsNone(next_failure(self.args,ledger))
            other,r2=self.diagnostic(2,3,False)
            self.assertEqual(next_failure(self.args,ledger)[0],other)
    def test_applied_or_resolved_repairs_still_resume_saved_activity(self):
        from capture import queued_resume
        p,r=self.diagnostic(1,1)
        atomic_json(p.parents[2]/'state.json',{'task_id':1,'questions':{},'deferred_error':{'diagnostics':str(p.parent)}})
        for status in ('applied','resolved'):
            ledger=self.record(p,r,status)
            atomic_json(self.args.state_dir/'capture-repair/failures.json',ledger)
            with patch('capture_repair.source_version',return_value='one'):
                self.assertEqual(queued_resume(self.args,[{'task_id':1}],set()),p.parents[2].resolve())
    def test_budget_retains_previously_exhausted_evidence_versions(self):
        p,r=self.diagnostic(1,1);entry=self.record(p,r)[failure_key(r)]
        old=evidence_version(p);entry.update(evidence_version='different',attempts=1,attempt_versions={old+':one':2})
        with patch('capture_repair.source_version',return_value='one'):
            self.assertIsNone(next_failure(self.args,{failure_key(r):entry}))
    def test_legacy_jobs_restore_budget_and_preserve_originals(self):
        p,r=self.diagnostic(1,1);key=legacy_failure_key(r)
        old={'attempts':1,'status':'blocked','diagnostic':str(p),'source_version':'one',
             'summary':'The displayed separate improper integrals diverge.','job':'original-job'}
        ledger={key:dict(old)}
        for n in range(2):
            job=self.args.state_dir/'capture-repair'/(key[:10]+'-'+str(n));job.mkdir(parents=True)
            atomic_json(job/'input.json',{'report':r,'diagnostics':str(p.parent)})
            atomic_json(job/'result.json',{'status':'blocked','summary':old['summary']})
        other,r2=self.diagnostic(2,2)
        for n in range(2,4):
            job=self.args.state_dir/'capture-repair'/(key[:10]+'-'+str(n));job.mkdir(parents=True)
            atomic_json(job/'input.json',{'report':r2,'diagnostics':str(other.parent)})
            atomic_json(job/'result.json',{'status':'blocked','summary':old['summary']})
        migrate_ledger(self.args,ledger)
        self.assertEqual(ledger[failure_key(r2)]['attempts'],2)
        self.assertEqual(ledger[key],old)
        entry=ledger[failure_key(r)];self.assertEqual(entry['attempts'],2);self.assertEqual(len(entry['migrated_jobs']),2)
        self.assertFalse(entry['retry_on_source_change'])
        with patch('capture_repair.source_version',return_value='two'):
            self.assertIsNone(next_failure(self.args,ledger))

if __name__=='__main__':unittest.main()
