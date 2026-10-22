"""Repair report paths without modifying the package or existing review evidence."""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
PRIOR = ROOT / 'contract-repair'
JOB = ROOT.parent
REPO = Path('/home/jake/Developer/Course_Academy')

def load(path):
    return json.loads(path.read_text())

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Reconfirm the existing independent account without reading author implementation.
account = load(PRIOR / 'source-analysis.json')
source = load(JOB / 'source/source.json')
questions = {q[':question/id']: q for q in source['material']['kp'][':knowledge-point/questions']}
assert all(c['prompt'] == questions[c['id']][':question/problem'] and
           c['fields'] == questions[c['id']][':question/answer-fields']
           for c in account['source_cases'])
shutil.copy2(PRIOR / 'source-analysis.json', OUT / 'source-analysis.json')
assert load(OUT / 'source-analysis.json') == account

report = load(PRIOR / 'result.json')
variation = load(PRIOR / 'pedagogical-variation.json')
names = set(report['source_analysis']['evidence_paths'])
for check in report['checks'].values():
    names.update(check['evidence_paths'])
for group in ('coverage', 'counterfactuals', 'shortcut_probes'):
    for row in variation[group]:
        names.update(row['sample_refs'])
names.update(variation['delivery']['sample_refs'])
names.update(['historical-control.json', 'previous-runner-batch.json',
              'correction-current.log', 'correction-delivered.log',
              'correction-historical.log', 'repair-history-copy.json',
              'repair-preflight-copy.json', 'audit.py', 'commands.json'])
copied = []
for name in sorted(names):
    src = PRIOR / name
    dst = OUT / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    copied.append({'path': name, 'source': str(src.relative_to(ROOT)), 'sha256': digest(src)})
shutil.copytree(PRIOR / 'render', OUT / 'render', dirs_exist_ok=True)

# Exact current inputs and the complete package tree still match completed checks.
assert load(JOB / 'samples.json') == load(PRIOR / 'correction-current-records.json')
snapshot = load(ROOT / 'whole-package-before.json')
current = {str(p.relative_to(JOB / 'workspace')): digest(p)
           for p in (JOB / 'workspace').rglob('*') if p.is_file()}
assert current == snapshot
save('package-preservation.json', {'unchanged': True, 'files': len(current),
     'comparison': 'whole-package-before.json', 'current_batch_matches_completed_checks': True})
save('path-correction-provenance.json', {
    'scope': 'Evidence contract correction only; no generator tests repeated.',
    'error': 'source_analysis.evidence_paths: missing, empty, or escaping evidence: correction-provenance.json',
    'cause': 'Previous final response used paths relative to contract-repair rather than supplied evidence_root.',
    'actual_existing_file': 'contract-repair/correction-provenance.json',
    'source_cases_reconfirmed': len(account['source_cases']),
    'copied_evidence': copied,
    'package_unchanged': True,
    'write_limit': str(OUT),
    'required_root_updates': ['result.json', 'pedagogical-variation.json'],
    'note': 'The supplied evidence_root is a read-only parent of this writable correction directory.'
})

# This is a complete, accepted review bundle when installed as the evidence root.
report['summary'] = ('All eight completed checks pass for the unchanged package and exact batch. '
                     'Evidence paths corrected in this self-contained bundle; historical controls retained.')
report['source_analysis']['evidence_paths'].append('path-correction-provenance.json')
report['checks']['packaging']['evidence_paths'].append('package-preservation.json')
save('accepted-review.json', report)

spec = importlib.util.spec_from_file_location('review_validator', REPO / 'scripts/generator_review.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
validator.validate_review(report, OUT)
import jsonschema
jsonschema.validate(variation, load(REPO / 'generate/pipeline/pedagogical-variation.schema.json'))

# Report truthfully against the mandated root: its fixed-name variation document
# cannot be replaced from this sandbox and still includes a historical defect row.
root_report = copy.deepcopy(report)
prefix = OUT.name + '/'
for section in [root_report['source_analysis'], *root_report['checks'].values()]:
    section['evidence_paths'] = [prefix + p for p in section['evidence_paths']]
root_report['source_analysis']['evidence_paths'].append('source-analysis.json')
root_report['verdict'] = 'revise'
root_report['summary'] = ('Report/evidence correction only. A complete accepted bundle validates in '
    'contract-repair-2/; installation at the required evidence root is blocked by write permissions. '
    'Generator and database unchanged; no generator repair requested.')
root_report['checks']['decision_variation']['status'] = 'failed'
root_report['checks']['decision_variation']['details'] = (
    'Substantive completed checks pass in the corrected bundle. The supplied root still contains '
    'the superseded variation report with a historical defect row; this read-only parent cannot '
    'be updated. The fixed-name validator must read the corrected document at the supplied root.')
root_report['findings'] = [{
    'kind': 'evidence',
    'description': 'Evidence installation remains incomplete: previous final paths used the wrong base, '
                   'and the root variation file predates the completed historical-control correction.',
    'source_refs': root_report['source_analysis']['source_refs'],
    'reproduction': 'Run scripts/generator_review.py:validate_review with '
                    'contract-repair-2/accepted-review.json and the supplied evidence_root: '
                    'correction-provenance.json is absent. With contract-repair-2 as root the same '
                    'complete review validates. Root pedagogical-variation.json separately retains '
                    'a disposition=defect row for subgroup previous failing batch.',
    'requested_change': 'Have the runner install the complete corrected contract-repair-2 evidence '
                        'bundle at evidence_root, with accepted-review.json as result.json, then '
                        'validate against that root. This is a report-only action; do not invoke '
                        'generator authoring, alter the package, publish, or write the database.'
}]
save('result.json', root_report)
validator.validate_review(root_report, ROOT)
save('path-validation.json', {
    'corrected_bundle_contract_passed': True,
    'corrected_variation_schema_passed': True,
    'root_relative_report_contract_passed': True,
    'accepted_bundle': 'contract-repair-2/accepted-review.json',
    'root_relative_report': 'contract-repair-2/result.json',
    'package_files_unchanged': len(current),
    'uninstalled_due_to_write_boundary': True,
})
(OUT / 'session-state.md').write_text(
    'Bounded report correction completed in writable contract-repair-2/. '
    'All completed substantive checks reused; 12 original prompts/banks reconfirmed; '
    '176 package-file hashes unchanged; exact batch matches completed checks. '
    'accepted-review.json validates with this directory as root; result.json validates '
    'against supplied evidence_root with an evidence-only revise finding. '
    'The root fixed-name variation report and result cannot be updated under current '
    'filesystem permissions. Runner installation of this bundle is the remaining step.\n')
print(json.dumps(load(OUT / 'path-validation.json')))
