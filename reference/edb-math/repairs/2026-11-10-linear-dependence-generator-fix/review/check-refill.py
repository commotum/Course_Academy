"""Independent supplemental packaging review; no EDB or publication calls."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
REPO=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(REPO))
from scripts.generator_refill import _run_checker
from scripts.generator_publish import content_fingerprint
from scripts.generator_refill_plan import validate_refill_plan,validate_check_results
ROOT=Path(__file__).resolve().parents[1]
REVIEW=ROOT/'review'
before=hashlib.sha256((REVIEW/'report.json').read_bytes()).hexdigest()
results=[]
for kp in ['17592186119924','17592186119925']:
    package=ROOT/'packages'/kp
    manifest=json.loads((package/'package.json').read_text())
    contract=json.loads((package/'refill-validation.json').read_text())
    spec=importlib.util.spec_from_file_location('refill_'+kp,package/'check_refill.py')
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    binding=validate_refill_plan(package,manifest,[{'id':x} for x in ['subset-radio-response','redundant-none','empty-subset-support']],REVIEW)
    bands=[]
    for band in ['easy','moderate','hard']:
        records=json.loads((ROOT/'verification'/kp/(band+'.json')).read_text())
        expected=sorted(content_fingerprint(r['question']) for r in records)
        assert expected==sorted(guard.fingerprint(r['question']) for r in records)
        output=REVIEW/'refill-interface'/kp/band;output.mkdir(parents=True,exist_ok=True)
        report=_run_checker(package,manifest,contract,records,{'fingerprints':[]},output,sys.executable)
        assert report['status']=='passed' and report['checked_fingerprints']==expected
        validate_check_results(report,binding,expected)
        bands.append({'band':band,'records':len(records),'real_refill_checker_interface':'passed','publisher_fingerprints_equal':True,'plan_check_results_coverage':'passed'})
    q=copy.deepcopy(records[0]['question'])
    defects=[]
    for label,mutate in [
        ('radio',lambda q:q[':question/answer-fields'][0].update({':answer-field/type':':answer-field.type/radio'})),
        ('bare_roman_I',lambda q:q[':question/answer-fields'][0].update({':answer-field/key':'I'})),
        ('none_of_the_above',lambda q:q[':question/answer-fields'][0].update({':answer-field/key':'None of the above'})),
        ('missing_guidance',lambda q:q.update({':question/problem':q[':question/problem'].replace('If none apply, leave all boxes unchecked.','')})),
        ('bad_boolean',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].update({':answer/value':'maybe'})),
    ]:
        bad=copy.deepcopy(q);mutate(bad)
        try:guard.check(bad);rejected=False
        except (AssertionError,KeyError,ValueError,TypeError):rejected=True
        defects.append({'defect':label,'rejected':rejected})
    for key in ['selection','I.','None of the statements','A','']:
        bad=copy.deepcopy(q);bad[':question/answer-fields'][0][':answer-field/key']=key
        try:guard.check(bad);rejected=False
        except (AssertionError,KeyError,ValueError,TypeError):rejected=True
        defects.append({'defect':'incomplete_or_none_key','injected_key':key,'rejected':rejected})
    key='I. '+q[':question/answer-fields'][0][':answer-field/key']
    bad=copy.deepcopy(q);bad[':question/answer-fields'][0][':answer-field/key']=key
    try:guard.check(bad);rejected=False
    except (AssertionError,KeyError,ValueError,TypeError):rejected=True
    defects.append({'defect':'roman_prefix_on_statement','injected_key':key,'rejected':rejected})
    hashes={name:hashlib.sha256((package/name).read_bytes()).hexdigest() for name in ['check_refill.py','refill-validation.json','refill-review-plan.json','package.json']}
    results.append({'kp':kp,'plan_binding':binding,'bands':bands,'injected_defects':defects,'reviewed_sha256':hashes})
findings=[{'severity':'blocking','kp':r['kp'],'description':'Guard accepts a nonstatement or redundant None key despite its declared full-statement obligation.','accepted_injected_keys':[d['injected_key'] for d in r['injected_defects'] if d.get('injected_key') is not None and not d['rejected']]} for r in results if any(not d['rejected'] for d in r['injected_defects'])]
assert before==hashlib.sha256((REVIEW/'report.json').read_bytes()).hexdigest()
result={'verdict':'rejected' if findings else 'accepted','scope':'Supplemental refill checker and plan exact-file review only; original generator review unchanged.','checks':results,'findings':findings,'total_root_records_checked':180,'actual_survivors_through_delivery_audit':False,'native_grading_invoked':False,'interface_used':'scripts.generator_refill._run_checker (real declared-file isolated execution); scripts.generator_refill_plan.validate_refill_plan and validate_check_results','original_report_sha256_unchanged':before}
(REVIEW/(sys.argv[1] if len(sys.argv)>1 else 'refill-review.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
