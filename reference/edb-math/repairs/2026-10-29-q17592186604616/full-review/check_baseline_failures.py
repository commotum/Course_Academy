"""Determine whether the four broader-suite failures predate this table change."""
import json,sys,unittest
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R/'scripts/question_capture'),str(R)]
import browser,test_capture,test_matrix_capture
new=(R/'scripts/question_capture/table_html.js').read_text();new=new[new.index('function sourceHTMLTable'):].strip();old=(H/'baseline-source-table-helper.js').read_text();old=old[old.index('function sourceHTMLTable'):].strip();assert new in browser.EXTRACT
baseline=browser.EXTRACT.replace(new,old,1);browser.EXTRACT=baseline;test_capture.EXTRACT=baseline
original=test_matrix_capture.MatrixCaptureTests.setUpClass.__func__
def setup(cls):original(cls);cls.source=baseline
test_matrix_capture.MatrixCaptureTests.setUpClass=classmethod(setup)
suite=unittest.TestSuite([test_matrix_capture.MatrixCaptureTests('test_percent_identifier_is_literal_content_in_mathml'),test_matrix_capture.MatrixCaptureTests('test_saved_four_by_three_matrix_retains_every_cell'),test_capture.DOMTests('test_empty_zero_width_mathjax_formula_is_not_a_missing_visual_asset'),test_capture.DOMTests('test_real_submitting_dropdown_checkpoint_recovers_without_submit')]);result=unittest.TestResult();suite.run(result)
rows=[{'test':t.id(),'kind':kind,'details':details}for kind,items in [('failure',result.failures),('error',result.errors)]for t,details in items];assert len(rows)==4,(result.testsRun,rows)
report={'baseline_failures_reproduced':True,'tests':result.testsRun,'original_table_helper_used':True,'failures':rows,'database_writes':0};(H/'preexisting-capture-test-failures.json').write_text(json.dumps(report,indent=2)+'\n');print('All four broader-suite failures also occur with the original table extractor; they predate this repair')
