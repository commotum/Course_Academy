"""Validate a verifier's final report and its recorded evidence."""
import argparse
import json
from pathlib import Path
import re
import sys
import uuid
import hashlib

try:
    from .generator_evidence import FORMATS, batch_sha256, record_sha256, validate_tool_report
except ImportError:
    from generator_evidence import FORMATS, batch_sha256, record_sha256, validate_tool_report


REVIEW_POLICY_VERSION = 6
DIFFICULTIES = ("easy", "moderate", "hard")
CHECKS = ("source_replay", "math", "variety", "decision_variation", "scope", "grading", "rendering", "packaging", "progression")
FINDING_KINDS = ("restriction", "drift", "math", "grading", "rendering",
                 "source_fidelity", "decision_shortcut", "packaging", "evidence", "inventory")
SOURCE_FIELDS = ('skill', 'reasoning_steps', 'invariants', 'permitted_variations', 'source_refs')


def evidence_only_review(result):
    """Route missing/corrupt review evidence back to the independent reviewer.

    This identifies who must repair the result; it does not approve the package
    or relax any evidence check. Mixed reports still require generator repairs.
    """
    if not isinstance(result, dict) or result.get("verdict") not in {"revise", "unsupported"}:
        return False
    findings = result.get("findings")
    return (isinstance(findings, list) and bool(findings)
            and all(isinstance(finding, dict) and finding.get("kind") == "evidence"
                    for finding in findings))


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")


def _strings(value, label, required=False):
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{label} must contain nonempty strings")
    if required and not value:
        raise ValueError(f"{label} must not be empty")


def _evidence(paths, root, label, required=False):
    _strings(paths, label, required)
    root = Path(root).resolve()
    for item in paths:
        relative = Path(item)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"{label}: evidence must be relative to the evidence directory")
        try:
            path = (root / relative).resolve()
        except (OSError, RuntimeError) as error:
            raise ValueError(f"{label}: unreadable evidence: {item}") from error
        if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"{label}: missing, empty, or escaping evidence: {item}")


def _rows(report, key, fields, root, *, samples=True):
    rows = report.get(key)
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"decision_variation.{key} must contain evidence")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"decision_variation.{key} entry must be an object")
        for field in fields:
            _text(row.get(field), f"decision_variation.{key}.{field}")
        if samples:
            _evidence(row.get("sample_refs"), root, f"decision_variation.{key}.sample_refs", required=True)
    return rows


def _decision_evidence(check, root):
    """Require inspectable distribution evidence, not a proxy diversity score.

    The independent reviewer judges pedagogical meaning. This gate checks that
    those judgments and reproducible observations exist and report no defects.
    """
    name = "pedagogical-variation.json"
    if name not in check["evidence_paths"]:
        raise ValueError("decision_variation requires pedagogical-variation.json")
    try:
        report = json.loads((Path(root) / name).read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("pedagogical variation evidence must be readable JSON") from error
    if not isinstance(report, dict):
        raise ValueError("pedagogical variation evidence must be an object")
    _text(report.get("learner_operation"), "decision_variation.learner_operation")
    _rows(report, "fixed_features", ("feature", "justification"), root, samples=False)
    _rows(report, "answer_roles", ("role", "eligible_variation", "observed"), root, samples=False)
    _rows(report, "coverage", ("case", "result"), root)
    pairs = _rows(report, "counterfactuals", ("kind", "change", "expected", "observed", "justification"), root)
    if {pair["kind"] for pair in pairs} != {"relevant", "irrelevant"}:
        raise ValueError("decision_variation needs relevant and irrelevant counterfactuals")
    for pair in pairs:
        if pair.get("status") not in {"passed", "not_applicable"}:
            raise ValueError("decision_variation has a failed or untested counterfactual")
    applicability = report.get('shortcut_applicability', {})
    if not isinstance(applicability, dict) or applicability.get('status') not in {'applicable', 'not_applicable'}:
        raise ValueError('decision_variation requires shortcut applicability')
    _text(applicability.get('reason'), 'shortcut applicability reason')
    _evidence(applicability.get('sample_refs'), root, 'shortcut applicability evidence', required=True)
    probes = report.get('shortcut_probes')
    if applicability['status'] == 'not_applicable':
        if probes != []:
            raise ValueError('not-applicable shortcut assessment must not fabricate probes')
    else:
        probes = _rows(report, "shortcut_probes", ("cue", "subgroup", "scope", "strategy", "conclusion"), root)
    conditional = False
    for probe in probes:
        scope = probe["scope"]
        if scope not in {"overall", "within_template", "other_recognizable_subgroup"}:
            raise ValueError("decision_variation shortcut scope is invalid")
        conditional |= scope != "overall"
        correct, total, baseline = (probe.get(key) for key in ("correct", "total", "baseline"))
        if type(correct) is not int or type(total) is not int or not 0 <= correct <= total or total <= 0:
            raise ValueError("decision_variation shortcut counts must be observed whole counts")
        if type(baseline) not in (int, float) or not 0 <= baseline <= 1:
            raise ValueError("decision_variation shortcut baseline must be a probability")
        if probe.get("disposition") not in {"not_predictive", "intended_skill"}:
            raise ValueError("decision_variation has an unresolved decision shortcut")
        if probe.get('claim') not in {'diagnostic', 'confirmed'}:
            raise ValueError('shortcut probe requires diagnostic or confirmed claim')
        if probe['claim'] == 'confirmed':
            confirmation = probe.get('confirmation', {})
            if not isinstance(confirmation, dict) or confirmation.get('method') not in {'fresh_cases', 'invariant', 'finite_pool'}:
                raise ValueError('confirmed shortcut needs fresh cases, invariant or finite-pool evidence')
            for key in ('allowed_information', 'bypassed_work', 'subgroup_selection', 'mechanism'):
                _text(confirmation.get(key), 'shortcut confirmation.' + key)
            _evidence(confirmation.get('evidence_paths'), root, 'shortcut confirmation evidence', required=True)
            if confirmation['method'] == 'fresh_cases':
                _evidence(confirmation.get('discovery_refs'), root, 'shortcut discovery evidence', required=True)
                _evidence(confirmation.get('confirmation_refs'), root, 'shortcut held-out evidence', required=True)
                if set(confirmation['discovery_refs']) & set(confirmation['confirmation_refs']):
                    raise ValueError('fresh shortcut confirmation must be separate from discovery inputs')
                discovered = {hashlib.sha256((Path(root) / name).read_bytes()).hexdigest() for name in confirmation['discovery_refs']}
                confirmed = {hashlib.sha256((Path(root) / name).read_bytes()).hexdigest() for name in confirmation['confirmation_refs']}
                if discovered & confirmed:
                    raise ValueError('fresh shortcut confirmation cannot relabel the same evidence bytes')
    if applicability['status'] == 'applicable' and not conditional:
        exception = report.get('conditional_probe_not_applicable', {})
        if not isinstance(exception, dict):
            raise ValueError('conditional shortcut applicability must be an explicit judgment')
        _text(exception.get('reason'), 'conditional shortcut applicability reason')
        _evidence(exception.get('sample_refs'), root, 'conditional shortcut applicability evidence', required=True)
    delivery = report.get("delivery")
    if not isinstance(delivery, dict):
        raise ValueError("decision_variation needs delivered-distribution evidence")
    _strings(delivery.get("stages_examined"), "decision_variation.delivery.stages_examined", required=True)
    _text(delivery.get("result"), "decision_variation.delivery.result")
    _evidence(delivery.get("sample_refs"), root, "decision_variation.delivery.sample_refs", required=True)
    _strings(report.get("limitations"), "decision_variation.limitations")


def _solution_path_evidence(check, root):
    """Require the reviewer's observed answer transitions, not equivalence alone."""
    name = "solution-paths.json"
    if name not in check["evidence_paths"]:
        raise ValueError("scope requires solution-paths.json")
    try:
        report = json.loads((Path(root) / name).read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("solution paths evidence must be readable JSON") from error
    if not isinstance(report, dict) or not isinstance(report.get("cases"), list) or not report["cases"]:
        raise ValueError("solution paths requires nonempty cases")
    for case in report["cases"]:
        if not isinstance(case, dict):
            raise ValueError("solution path case must be an object")
        for key in ("template", "field_key", "final_expression", "keyed_answer", "domain", "conclusion"):
            _text(case.get(key), "solution_path." + key)
        if (not isinstance(case.get('record_sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', case['record_sha256'])
                or type(case.get('field_index')) is not int or case['field_index'] < 0):
            raise ValueError('solution path must identify an actual record and field index')
        _evidence(case.get("sample_refs"), root, "solution_path.sample_refs", required=True)
        if case.get("status") != "passed":
            raise ValueError("solution path is failed or untested")
        conversions = case.get("conversions")
        if not isinstance(conversions, list):
            raise ValueError("solution path conversions must be a list")
        for conversion in conversions:
            if not isinstance(conversion, dict):
                raise ValueError("solution path conversion must be an object")
            for key in ("rule", "scope_source", "shown_step"):
                _text(conversion.get(key), "solution_path.conversion." + key)
            if conversion.get("status") != "passed":
                raise ValueError("solution path contains an unsupported or unshown conversion")
        # A conversion control is applicable only when this path changes form.
        # No fabricated CAS/trig exercise is required for a direct answer path.
        if conversions:
            control = case.get('conversion_control')
            if not isinstance(control, dict):
                raise ValueError('solution path with conversions requires conversion_control')
            for key in ('candidate', 'reason', 'method'):
                _text(control.get(key), 'solution_path.conversion_control.' + key)
            if control.get('expected') != 'rejected' or control.get('observed') != 'rejected':
                raise ValueError('conversion control must demonstrate rejection of the unsupported path')
            if control.get('status') != 'passed':
                raise ValueError('solution path conversion control is failed or untested')
            _evidence(control.get('sample_refs'), root, 'solution_path.conversion_control.sample_refs', required=True)


def _source_account(value, label):
    if not isinstance(value, dict):
        raise ValueError(label + ' must be an object')
    _text(value.get('skill'), label + '.skill')
    for field in SOURCE_FIELDS[1:]:
        _strings(value.get(field), label + '.' + field, required=True)
    return {field: value[field] for field in SOURCE_FIELDS}


def validate_source_account_checkpoint(path, expected_sha256=None):
    """Read substantive account; only the runner may establish its first digest."""
    path = Path(path)
    _source_account(json.loads(path.read_text()), 'initial source analysis')
    identity = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected_sha256 is not None and identity != expected_sha256:
        raise ValueError('source analysis differs from the runner-preserved initial account')
    return identity


def _source_analysis_evidence(analysis, root, binding):
    """Keep the initial independent account distinct from later justified changes."""
    root = Path(root)
    initial_path = root / 'source-analysis.json'
    identity = binding.get('initial_source_analysis_sha256')
    if not isinstance(identity, str) or not re.fullmatch(r'[0-9a-f]{64}', identity):
        raise ValueError('accepted review requires runner-preserved initial source account identity')
    validate_source_account_checkpoint(initial_path, identity)
    try:
        initial = _source_account(json.loads(initial_path.read_text()), 'initial source analysis')
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError('independent source analysis must be readable JSON') from error
    final = _source_account(analysis, 'source_analysis')
    amendment_name = 'source-analysis-amendments.json'
    if amendment_name not in analysis['evidence_paths']:
        if final != initial:
            raise ValueError('changed source analysis requires linked source-analysis-amendments.json')
        return
    amendment = json.loads((root / amendment_name).read_text())
    if not isinstance(amendment, dict) or amendment.get('initial_sha256') != hashlib.sha256(initial_path.read_bytes()).hexdigest():
        raise ValueError('source analysis amendment does not match the preserved initial account')
    if _source_account(amendment.get('final_source_analysis'), 'amended source analysis') != final:
        raise ValueError('amended source analysis differs from final report')
    changes = amendment.get('amendments')
    if not isinstance(changes, list) or not changes:
        raise ValueError('source analysis amendments require a reason and evidence')
    for change in changes:
        if not isinstance(change, dict):
            raise ValueError('source analysis amendment must be an object')
        _text(change.get('reason'), 'source analysis amendment reason')
        _strings(change.get('source_refs'), 'source analysis amendment source_refs', required=True)
        _evidence(change.get('evidence_paths'), root, 'source analysis amendment evidence_paths', required=True)
        _text(change.get('preserved_obligation'), 'source analysis amendment preserved obligation')
        _evidence([change.get('valid_case_ref')], root, 'source analysis amendment valid counterexample', required=True)


def _field_shape(record):
    question = record.get('question')
    fields = question.get(':question/answer-fields') if isinstance(question, dict) else None
    if not isinstance(fields, list) or not fields:
        raise ValueError('learner obligation coverage requires actual answer fields')
    if any(not isinstance(field, dict) for field in fields):
        raise ValueError('learner obligation answer fields must be objects')
    return [field.get(':answer-field/type') for field in fields]


def _learner_obligations(result, root, records_by_band, reports, *, exemplars=False):
    """Bind judgments to outputs, not infer the truth of those judgments."""
    name = 'learner-obligations.json'
    if name not in result['checks']['progression']['evidence_paths']:
        raise ValueError('progression requires record-linked learner-obligations.json')
    _evidence([name], root, 'learner obligations', required=True)
    account = json.loads((root / name).read_text())
    if not isinstance(account, dict):
        raise ValueError('learner obligations must be an object')
    families = account.get('families')
    if not isinstance(families, list) or not families:
        raise ValueError('learner obligations must declare material families')
    by_family = {}
    for family in families:
        if not isinstance(family, dict):
            raise ValueError('material family must be an object')
        for key in ('id', 'operation', 'support', 'response', 'reason'):
            _text(family.get(key), 'material family.' + key)
        _strings(family.get('source_refs'), 'material family source_refs', required=True)
        if family['id'] in by_family:
            raise ValueError('duplicate material family')
        by_family[family['id']] = family
    bands = account.get('bands', {})
    if not isinstance(bands, dict) or set(bands) != set(DIFFICULTIES):
        raise ValueError('learner obligations must cover all three bands')
    representatives = account.get('representatives')
    if not isinstance(representatives, list) or not representatives or any(not isinstance(row, dict) for row in representatives):
        raise ValueError('learner obligations need inspected representatives')
    if any(not isinstance(row.get('record_sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', row['record_sha256']) for row in representatives):
        raise ValueError('representative needs an actual record fingerprint')
    by_rep = {row.get('record_sha256'): row for row in representatives}
    if len(by_rep) != len(representatives):
        raise ValueError('duplicate learner obligation representative')
    used_reps, used_families = set(), set()
    actual = {}
    for band, (records, fallback) in records_by_band.items():
        actual.update({record_sha256(record): record for record in records})
        row = bands[band]
        if not isinstance(row, dict):
            raise ValueError('band learner obligations must be an object')
        _text(row.get('progression'), band + ' actual learner-work progression comparison')
        if fallback:
            justification = row.get('no_survivor_fallback', {})
            if not isinstance(justification, dict):
                raise ValueError('no-survivor fallback must be an explicit judgment')
            _text(justification.get('reason'), band + ' no-survivor fallback reason')
            _evidence(justification.get('evidence_paths'), root, 'no-survivor fallback evidence', required=True)
        elif row.get('no_survivor_fallback'):
            raise ValueError('raw fallback is only permitted when delivery has no survivors')
        mappings = row.get('records')
        identities = {record_sha256(record) for record in records}
        if (not isinstance(mappings, list) or any(not isinstance(mapping, dict) or any(not isinstance(mapping.get(k), str)
                for k in ('record_sha256', 'representative_sha256', 'family')) for mapping in mappings) or len(mappings) != len(identities)
                or {mapping.get('record_sha256') for mapping in mappings} != identities):
            raise ValueError(band + ' learner obligations omit actual delivered records')
        family_representatives = {}
        for mapping in mappings:
            member, representative, family = (mapping.get(k) for k in ('record_sha256', 'representative_sha256', 'family'))
            if family not in by_family or representative not in identities or representative not in by_rep:
                raise ValueError('material family lacks an actual same-band representative')
            if by_rep[representative].get('family') != family:
                raise ValueError('representative material family differs from coverage mapping')
            _text(mapping.get('reason'), 'representative coverage reason')
            if exemplars and representative != member:
                raise ValueError('every exemplar requires its own independent inspection')
            if _field_shape(actual[member]) != _field_shape(actual[representative]):
                raise ValueError('representative does not cover actual response field shapes')
            family_representatives.setdefault(family, set()).add(representative)
            used_reps.add(representative); used_families.add(family)
    if used_reps != set(by_rep) or used_families != set(by_family):
        raise ValueError('learner obligations contain uncovered representatives or material families')
    paths = json.loads((root / 'solution-paths.json').read_text())['cases']
    by_path = {}
    for case in paths:
        key = (case.get('record_sha256'), case.get('field_index'))
        if key in by_path:
            raise ValueError('duplicate solution path for final response field')
        by_path[key] = case
    expected_paths = set()
    for identity, representative in by_rep.items():
        record = actual[identity]
        for key in ('given', 'preservation', 'difficulty_justification'):
            _text(representative.get(key), 'learner obligation.' + key)
        _strings(representative.get('required_work'), 'learner required work', required=True)
        steps = representative.get('source_reasoning_steps')
        if (not isinstance(steps, list) or not steps or any(type(i) is not int or not 0 <= i < len(result['source_analysis']['reasoning_steps']) for i in steps)):
            raise ValueError('learner obligation must identify applicable source reasoning steps')
        exemptions = representative.get('source_step_exemptions', [])
        if not isinstance(exemptions, list):
            raise ValueError('source-step exemptions must be explicit judgments')
        exempted = set()
        for exemption in exemptions:
            if not isinstance(exemption, dict):
                raise ValueError('source-step exemption must be an object')
            index = exemption.get('index')
            if type(index) is not int or index in exempted or index in steps:
                raise ValueError('invalid or duplicate source-step exemption')
            _text(exemption.get('reason'), 'source-step exemption reason')
            exempted.add(index)
        if set(steps) | exempted != set(range(len(result['source_analysis']['reasoning_steps']))):
            raise ValueError('representative must account for every source reasoning obligation')
        fields = record['question'][':question/answer-fields']
        judgments = representative.get('fields')
        if (not isinstance(judgments, list) or any(not isinstance(row, dict) for row in judgments) or len(judgments) != len(fields)
                or {row.get('field_index') for row in judgments} != set(range(len(fields)))):
            raise ValueError('representative must assess every actual answer field')
        render_cases = [case for report in reports.values() if FORMATS[report['format']] == 'rendering'
                        for case in report['cases'] if case['record_sha256'] == identity]
        viewports = {(case['viewport']['width'], case['viewport']['height']) for case in render_cases}
        paired = {viewport for viewport in viewports if {case['state'] for case in render_cases
            if (case['viewport']['width'], case['viewport']['height']) == viewport} == {'active', 'completed'}}
        if not paired:
            raise ValueError('each representative requires paired active/completed rendering')
        narrow = representative.get('narrow_layout', {})
        if not isinstance(narrow, dict) or narrow.get('status') not in {'required', 'not_applicable'}:
            raise ValueError('representative must assess narrow-layout applicability')
        _text(narrow.get('reason'), 'narrow-layout applicability reason')
        if narrow['status'] == 'required' and not any(width <= 480 for width, _ in paired):
            raise ValueError('applicable narrow layout needs paired narrow rendering')
        for judgment in judgments:
            index = judgment['field_index']; field = fields[index]
            _text(judgment.get('endpoint'), 'actual field response endpoint')
            requested = []
            for path, report in reports.items():
                if FORMATS[report['format']] != 'grading':
                    continue
                data = json.loads((root / path).parent.joinpath(report['input_file']).read_text())
                for item in data:
                    if record_sha256(item['record']) == identity:
                        requested.extend(check for check in item['checks'] if check.get('field_index', 0) == index)
            for check in requested:
                _text(check.get('purpose'), 'native control independent justification')
            if not ({'accepted', 'rejected'} <= {check.get('expected') for check in requested}):
                raise ValueError('each represented field needs accepted and wrong-response native coverage')
            if not any(check.get('control') == 'wrong' and check['expected'] == 'rejected' for check in requested):
                raise ValueError('wrong-response coverage needs an identified independent control')
            equivalence = judgment.get('equivalence', {})
            if not isinstance(equivalence, dict) or equivalence.get('status') not in {'tested', 'not_applicable'}:
                raise ValueError('field requires equivalent-response applicability judgment')
            _text(equivalence.get('reason'), 'equivalence applicability reason')
            if equivalence['status'] == 'tested' and not any(check.get('control') == 'equivalent' and check['expected'] == 'accepted' for check in requested):
                raise ValueError('applicable equivalent response needs a native acceptance control')
            key = (identity, index); expected_paths.add(key)
            case = by_path.get(key)
            if case is None:
                raise ValueError('scope omits an actual representative response field')
            correct = field[':answer-field/correct']
            correct = correct[-1] if isinstance(correct, list) else correct.get(':answer/id') if isinstance(correct, dict) else correct
            answer = next((choice for choice in field[':answer-field/choices'] if str(choice[':answer/id']) == str(correct)), None)
            if answer is None or case['keyed_answer'] != answer[':answer/value']:
                raise ValueError('solution path keyed answer differs from actual final field')
            if case['field_key'] != field[':answer-field/key']:
                raise ValueError('solution path field key differs from actual final field')
            review = case.get('conversion_review', {})
            if not isinstance(review, dict) or review.get('status') not in {'none', 'verified', 'formatting_only'}:
                raise ValueError('solution path needs explicit conversion verification')
            _text(review.get('reason'), 'conversion verification reason')
            _evidence(review.get('evidence_paths'), root, 'conversion verification evidence', required=True)
            if case['conversions']:
                if review['status'] != 'verified':
                    raise ValueError('conversion path must be explicitly verified')
            elif case['final_expression'] != case['keyed_answer'] and review['status'] != 'formatting_only':
                raise ValueError('different solution/key forms require a conversion or justified formatting-only judgment')
            elif review['status'] == 'verified':
                raise ValueError('verified conversion must identify its steps')
    if set(by_path) != expected_paths:
        raise ValueError('solution paths must cover exactly the representative final response fields')


def _tool_evidence(result, root, binding, *, exemplars=False):
    """Require recognized inputs/results while leaving semantic sufficiency to review."""
    root = Path(root)
    reports = {}
    paths = set()
    for check in result['checks'].values():
        paths.update(check['evidence_paths'])
    for band in result['band_verification'].values():
        paths.update(band['evidence_paths'])
    # Delivery may be linked from the existing variation evidence.
    variation = json.loads((root / 'pedagogical-variation.json').read_text())
    paths.update(variation['delivery']['sample_refs'])
    for path in paths:
        report = validate_tool_report(root / path, root, engine_sha256=binding.get('grader_sha256'))
        if report is not None:
            reports[path] = report
    for kind in ('grading', 'rendering'):
        if not any(FORMATS[reports[path]['format']] == kind for path in result['checks'][kind]['evidence_paths'] if path in reports):
            raise ValueError(kind + ' requires a recognized input-bound tool report')
    delivery_paths = set(result['checks']['decision_variation']['evidence_paths']) | set(variation['delivery']['sample_refs'])
    if not any(FORMATS[reports[path]['format']] == 'delivery' for path in delivery_paths if path in reports):
        raise ValueError('decision_variation requires a recognized delivery report')
    records_by_band = {}
    for band, claim in result['band_verification'].items():
        cited = [reports[path] for path in claim['evidence_paths'] if path in reports]
        deliveries = [r for r in cited if FORMATS[r['format']] == 'delivery' and r['batch_sha256'] == claim['batch_sha256']]
        if not deliveries:
            raise ValueError(f'{band} requires delivery evidence for its final batch')
        raw_records, delivered_records = {}, {}
        for report in deliveries:
            report_path = next(root / path for path in claim['evidence_paths'] if reports.get(path) is report)
            for name in ('source', 'inventory'):
                captured_path = report_path.parent / report['captured_inputs'][name]['file']
                if binding.get(name + '_hash') is not None and batch_sha256(json.loads(captured_path.read_text())) != binding[name + '_hash']:
                    raise ValueError(f'{band} delivery uses a different captured {name}')
            for record in json.loads((report_path.parent / report['input_file']).read_text()):
                raw_records[record_sha256(record)] = record
            for record in json.loads((report_path.parent / report['accepted_file']).read_text()):
                delivered_records[record_sha256(record)] = record
        records = set(delivered_records or raw_records)
        records_by_band[band] = (list((delivered_records or raw_records).values()), not bool(delivered_records))
        for kind in ('grading', 'rendering'):
            relevant = [r for r in cited if FORMATS[r['format']] == kind and set(r['checked_record_sha256']) & records]
            if not relevant:
                raise ValueError(f'{band} requires {kind} evidence on actual final records')
            if kind == 'rendering':
                states = {case['state'] for report in relevant for case in report['cases'] if case['record_sha256'] in records}
                if states != {'active', 'completed'}:
                    raise ValueError(f'{band} requires unanswered and completed rendering evidence')
    _learner_obligations(result, root, records_by_band, reports, exemplars=exemplars)


def _inventory_evidence(root):
    """Require the reviewer's handoff before any runner-owned pool action.

    This validates evidence completeness, not retirement eligibility. Original
    source and canonical questions may have valid defect reports but remain
    protected by the pool repairer's separate live eligibility checks.
    """
    name = "affected-inventory.json"
    _evidence([name], root, "inventory findings require affected-inventory.json", required=True)
    try:
        report = json.loads((Path(root) / name).read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("affected-inventory.json must contain readable JSON") from error
    rows = report.get("affected_questions") if isinstance(report, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("affected-inventory.json requires nonempty affected_questions")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("affected-inventory.json entries must be objects")
        try:
            if not isinstance(row.get("question_id"), str):
                raise ValueError
            uuid.UUID(row["question_id"])
        except ValueError as error:
            raise ValueError("affected-inventory.json requires exact question UUIDs") from error
        if type(row.get("entity_id")) is not int or row["entity_id"] <= 0:
            raise ValueError("affected-inventory.json requires positive integer entity IDs")
        for key in ("finding", "reproduction"):
            _text(row.get(key), "affected-inventory." + key)
        _evidence([row.get("evidence_path")], root, "affected-inventory.evidence_path", required=True)


def _band_verification(result, evidence_root, binding, accepted):
    """Check the verifier's explicit results against the runner's final batches.

    Approval concerns generated capabilities, not which sampled records were
    published. The reviewer judges quality; these checks prevent an omitted,
    failed, or stale difficulty band from inheriting another band's approval.
    """
    bands = result.get("band_verification")
    if bands is None and not accepted:
        return
    if not isinstance(bands, dict) or set(bands) != set(DIFFICULTIES):
        raise ValueError("band_verification must contain exactly easy, moderate, and hard")
    if binding is None and accepted:
        try:
            binding = json.loads((Path(evidence_root) / "final-binding.json").read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("accepted review requires the runner's final-binding.json") from error
    batches = binding.get("verification_batches") if isinstance(binding, dict) else None
    if accepted and (not isinstance(batches, dict) or set(batches) != set(DIFFICULTIES)):
        raise ValueError("accepted review requires final verification batches for all three bands")
    for band in DIFFICULTIES:
        row = bands[band]
        if not isinstance(row, dict):
            raise ValueError(f"band_verification.{band} must be an object")
        status = row.get("status")
        if status not in {"passed", "failed", "not_applicable"}:
            raise ValueError(f"band_verification.{band}: invalid status")
        _text(row.get("details"), f"band_verification.{band}.details")
        _evidence(row.get("evidence_paths"), evidence_root,
                  f"band_verification.{band}.evidence_paths", required=status == "passed")
        claimed_hash = row.get("batch_sha256")
        if not isinstance(claimed_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", claimed_hash):
            raise ValueError(f"band_verification.{band} requires a valid batch_sha256")
        if accepted and status != "passed":
            raise ValueError(f"accepted review requires passing {band}")
        if batches is not None:
            batch = batches.get(band) if isinstance(batches, dict) else None
            if not isinstance(batch, dict) or claimed_hash != batch.get("batch_hash"):
                raise ValueError(f"band_verification.{band} does not match the final batch")


def validate_exemplar_review(result, evidence_root, binding):
    """Same verifier's pre-construction review; every anchor is representative.

    Runtime replay/packaging checks describe the example artifact at this stage,
    not a nonexistent generator. Semantic judgments remain the verifier's work.
    """
    for row in binding.get('verification_batches', {}).values():
        if row.get('count', 1) != 1:
            raise ValueError('exemplar review requires exactly one example per band')
    return validate_review(result, evidence_root, binding, exemplars=True)


def validate_review(result, evidence_root, binding=None, *, exemplars=False, allow_legacy_completed=False):
    """Validate structure and on-disk evidence; never infer pedagogical truth.

    Raises ValueError for malformed verdicts or an acceptance without evidence.
    Negative verdicts remain valid when a missing capability prevents a check.
    """
    if not isinstance(result, dict):
        raise ValueError("review must be an object")
    verdict = result.get("verdict")
    if verdict not in ("accepted", "revise", "unsupported"):
        raise ValueError("invalid review verdict")
    accepted = verdict == "accepted"
    if accepted and binding is None:
        try:
            binding = json.loads((Path(evidence_root) / 'final-binding.json').read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("accepted review requires the runner's final-binding.json") from error
    _text(result.get("summary"), "summary")
    analysis = result.get("source_analysis")
    if not isinstance(analysis, dict):
        raise ValueError("source_analysis must be an object")
    _text(analysis.get("skill"), "source_analysis.skill")
    for key in ("reasoning_steps", "invariants", "permitted_variations", "source_refs"):
        _strings(analysis.get(key), f"source_analysis.{key}", required=accepted)
    _evidence(analysis.get("evidence_paths"), evidence_root,
              "source_analysis.evidence_paths", required=accepted)
    if accepted and "source-analysis.json" not in analysis["evidence_paths"]:
        raise ValueError("accepted review requires independent source-analysis.json")
    if accepted and not allow_legacy_completed:
        _source_analysis_evidence(analysis, evidence_root, binding)
    checks = result.get("checks")
    if not isinstance(checks, dict) or set(checks) != set(CHECKS):
        raise ValueError("review must contain exactly the nine named checks")
    for name in CHECKS:
        check = checks[name]
        if not isinstance(check, dict):
            raise ValueError(f"{name} must be an object")
        status = check.get("status")
        if status not in ("passed", "failed", "not_applicable"):
            raise ValueError(f"{name}: invalid status")
        _text(check.get("details"), f"{name}.details")
        _evidence(check.get("evidence_paths"), evidence_root, f"{name}.evidence_paths",
                  required=status == "passed")
        if accepted and status != "passed":
            raise ValueError(f"accepted review requires passing {name}")
    if checks["decision_variation"]["status"] == "passed" and not allow_legacy_completed:
        _decision_evidence(checks["decision_variation"], evidence_root)
    if checks["scope"]["status"] == "passed" and not allow_legacy_completed:
        _solution_path_evidence(checks["scope"], evidence_root)
    _band_verification(result, evidence_root, binding, accepted)
    # This private caller capability is only for runner-confirmed historical
    # completed publication recovery. It is not exposed by the validator CLI,
    # exemplar gate or agent report and cannot approve active/unpublished work.
    if accepted and not allow_legacy_completed:
        _tool_evidence(result, evidence_root, binding, exemplars=exemplars)
        if not exemplars:
            plan = binding.get('refill_plan')
            if not isinstance(plan, dict) or plan.get('path') != 'refill-review-plan.json':
                raise ValueError('accepted generator review requires runner-bound refill review plan')
            name = plan['path']
            if name not in checks['packaging']['evidence_paths']:
                raise ValueError('packaging must assess the refill review plan')
            _evidence([name], evidence_root, 'refill review plan', required=True)
            if hashlib.sha256((Path(evidence_root) / name).read_bytes()).hexdigest() != plan.get('sha256'):
                raise ValueError('refill review plan differs from runner binding')
    findings = result.get("findings")
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")
    for finding in findings:
        if not isinstance(finding, dict) or finding.get("kind") not in FINDING_KINDS:
            raise ValueError("finding has invalid kind")
        for key in ("description", "reproduction", "requested_change"):
            _text(finding.get(key), f"finding.{key}")
        _strings(finding.get("source_refs"), "finding.source_refs")
    if accepted and any(finding['kind'] != 'inventory' for finding in findings):
        raise ValueError("accepted review cannot have unresolved findings")
    if verdict == "revise" and not findings:
        raise ValueError("revise requires actionable findings")
    # Historical inventory observations are not publication prerequisites.
    # In particular, an incomplete import is valid partial evidence, not a
    # database repair request. A real pool mutation validates its separate
    # exact-question evidence at the mutation boundary.


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--result', required=True, type=Path)
    parser.add_argument('--evidence-root', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = json.loads(args.result.read_text())
        validate_review(result, args.evidence_root)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({'valid': False, 'error': str(error)}), file=sys.stderr)
        return 1
    print(json.dumps({'valid': True, 'verdict': result['verdict'],
                      'review_policy_version': REVIEW_POLICY_VERSION}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
