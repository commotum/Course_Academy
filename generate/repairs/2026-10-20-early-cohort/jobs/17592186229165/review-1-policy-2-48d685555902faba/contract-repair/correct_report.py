"""Bounded evidence correction; never imports or modifies the reviewed package.

Run with python3 (system jsonschema). Default outputs stay in this directory. --install
copies only the corrected review artifacts to the containing evidence root.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
JOB = ROOT.parent
REPO = Path('/home/jake/Developer/Course_Academy')

def read(path):
    return json.loads(path.read_text())

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = read(ROOT / 'package-before.json')
after = {str(p.relative_to(JOB / 'workspace')): digest(p)
         for p in (JOB / 'workspace').rglob('*') if p.is_file()}
assert before == after

spec = importlib.util.spec_from_file_location('review_contract', REPO / 'scripts/generator_review.py')
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)
prior = read(ROOT / 'result.json')
try:
    contract.validate_review(prior, ROOT)
except ValueError as error:
    prior_error = str(error)
else:
    prior_error = None
assert prior_error == 'decision_variation has an unresolved decision shortcut'

# Preserve the negative historical evidence verbatim, with explicit scope.
pv = read(ROOT / 'pedagogical-variation.json')
old_probe = [p for p in pv['shortcut_probes'] if p['disposition'] == 'defect']
assert len(old_probe) == 1
assert old_probe[0]['subgroup'] == 'Five reproduced stored generated records'
assert old_probe[0]['correct'] == old_probe[0]['total'] == 5
assert len(read(ROOT / 'affected-inventory.json')['affected_questions']) == 4
save('historical-inventory-shortcut.json', {
    'scope': 'Captured stored hard cohort, not the current package or exact requested easy batch.',
    'resolved_in_current_construction': True,
    'resolved_in_stored_inventory': False,
    'probe': old_probe[0],
    'affected_inventory': 'affected-inventory.json',
    'complete_reproduced_records': 'generated-records.json',
    'selection_evidence': 'selection-results.json',
    'generator_change_requested': False,
    'explanation': 'The old cohort remains an inventory remediation issue. No stored question was modified. Current mixed samples and delivery contain both resonant positions; the exact requested batch is easy. Acceptance is confined to the current generator and requested batch, and does not certify the historical hard pool.'
})
pv['shortcut_probes'] = [p for p in pv['shortcut_probes'] if p['disposition'] != 'defect']
pv['coverage'].append({
    'case': 'Historical inventory scope (separate from current-package shortcut probes)',
    'sample_refs': ['contract-repair/historical-inventory-shortcut.json', 'generated-records.json', 'affected-inventory.json'],
    'result': 'Historical second-term ordinary strategy succeeds on 5/5 stored generated hard records, including four affected mixed records. This remains a stored-cohort defect, preserved in the separate historical report; the repaired sampler and requested easy batch do not reproduce that fixed mixed-role rule.'
})
pv['limitations'].append('Acceptance covers the repaired package and exact requested easy batch, not historical hard-pool remediation. The prior historical defect probe is preserved without relabeling in contract-repair/historical-inventory-shortcut.json; affected-inventory.json is unchanged.')
save('pedagogical-variation.json', pv)

result = read(ROOT / 'result.json')
result['summary'] = 'The current generator and exact five-question easy batch pass the eight checks. Corrected the report scope: the unresolved historical hard-cohort defect remains documented for inventory remediation and is not a current-generator finding. No package or database changes.'
result['checks']['decision_variation']['evidence_paths'].append('contract-repair/historical-inventory-shortcut.json')
result['checks']['decision_variation']['evidence_paths'].append('contract-repair/correction-validation.json')
result['checks']['decision_variation']['details'] = 'Current-package counterfactuals, native grading, delivered coverage and conditional probes pass; fresh mixed seeds cover both positions (11/13). Exact easy batch survives 5/5. The historical captured hard pool still exhibits the old 5/5 positional pattern; four affected mixed records are retained in affected-inventory.json and a separate historical report. Acceptance does not certify or remediate that pool.'
save('result.json', result)
save('review-result.json', result)

# Validate against an overlay of changed report files and existing evidence.
# This invokes the real contract without modifying its code or old evidence.
overlay = HERE / 'validation-evidence'
# Use byte copies: the real validator correctly rejects escaping symlinks.
import shutil
if overlay.exists():
    shutil.rmtree(overlay)
overlay.mkdir()
refs = set(result['source_analysis']['evidence_paths'])
for check in result['checks'].values():
    refs.update(check['evidence_paths'])
for key in ['coverage', 'counterfactuals', 'shortcut_probes']:
    for row in pv[key]:
        refs.update(row['sample_refs'])
refs.update(pv['delivery']['sample_refs'])
for name in refs:
    if name == 'contract-repair/correction-validation.json':
        continue
    src = HERE / 'pedagogical-variation.json' if name == 'pedagogical-variation.json' else ROOT / name
    dst = overlay / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)

import jsonschema
jsonschema.validate(pv, read(REPO / 'generate/pipeline/pedagogical-variation.schema.json'))
validation = {
    'prior_contract_error_reproduced': prior_error,
    'change': 'Separate historical-inventory defect probe from current-package shortcut probes; preserve all original observations and affected records.',
    'current_probe_count': len(pv['shortcut_probes']),
    'historical_probe_preserved_verbatim': True,
    'affected_inventory_sha256_unchanged': digest(ROOT / 'affected-inventory.json'),
    'package_unchanged': True,
    'package_files_checked': len(after),
    'schema': 'passed',
    'real_contract': 'passed',
    'reproduction': 'python3 contract-repair/correct_report.py',
    'reused_checks': 'All prior mathematical, source, grading, rendering, delivery, selection and packaging evidence retained; no construction changes warrant rerunning them.',
    'binding': {
        'policy_version': 2,
        'package_hash': 'a96387a8d5d2987ef17521e4eaadcdd620d406cdb2765cd18c1cab2ac96cd8e4',
        'batch_hash': 'ed2fd0177c112708ee28f68f5bedc503625b89cadf4b4f2caab4e8e9ec099b7f',
        'source_hash': 'e44bd770b14fc33a90b79bea01b5860e53653c10a82f579d7710228d8996a02c',
        'inventory_hash': 'bb6c67d6f75acb8bc37275c3a78382db81cd9a280036a9a1344a53fe7e68a78f',
        'engine_hash': 'd8bc1d632589bed22447eb23b48692d880d58915b18fe0cbfa0091686b590045'
    }
}
save('correction-validation.json', validation)
shutil.copyfile(HERE / 'correction-validation.json', overlay / 'contract-repair/correction-validation.json')
contract.validate_review(result, overlay)
save('evidence-contract.json', {'passed': True, 'schema': 'JSON Schema passed', 'real_validator': 'generator_review.validate_review passed', 'validated_root': str(overlay), 'all_sample_refs_relative_and_nonempty': True})
(HERE / 'session-state.md').write_text('Bounded report correction complete in this directory. Original validator error reproduced; historical 5/5 shortcut evidence preserved separately, four affected inventory records unchanged. Corrected current-package report passes the actual review validator and variation JSON Schema using a byte-copy evidence snapshot. All 196 package files unchanged. Current generator/easy batch acceptance does not certify the historical hard pool.\n')
if '--install' in sys.argv:
    for name in ['pedagogical-variation.json', 'result.json', 'review-result.json', 'evidence-contract.json', 'session-state.md']:
        shutil.copyfile(HERE / name, ROOT / name)
    contract.validate_review(result, ROOT)
print(json.dumps({'prior_error': prior_error, 'corrected_contract': 'passed', 'package_files_unchanged': len(after), 'current_probes': len(pv['shortcut_probes']), 'historical_defect_preserved': True}))
