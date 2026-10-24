"""Small, fail-closed validation of an independent generator review."""
import json
from pathlib import Path
import uuid


REVIEW_POLICY_VERSION = 4
CHECKS = ("source_replay", "math", "variety", "decision_variation", "scope", "grading", "rendering", "packaging")
FINDING_KINDS = ("restriction", "drift", "math", "grading", "rendering",
                 "source_fidelity", "decision_shortcut", "packaging", "evidence", "inventory")


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
    if not conditional:
        raise ValueError("decision_variation requires a conditional shortcut probe")
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


def validate_review(result, evidence_root):
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
    if accepted:
        try:
            saved_analysis = json.loads((Path(evidence_root) / "source-analysis.json").read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("independent source analysis must be readable JSON") from error
        if not isinstance(saved_analysis, dict) or not saved_analysis:
            raise ValueError("independent source analysis must be a nonempty JSON object")
    checks = result.get("checks")
    if not isinstance(checks, dict) or set(checks) != set(CHECKS):
        raise ValueError("review must contain exactly the eight named checks")
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
    if checks["decision_variation"]["status"] == "passed":
        _decision_evidence(checks["decision_variation"], evidence_root)
    if checks["scope"]["status"] == "passed":
        _solution_path_evidence(checks["scope"], evidence_root)
    findings = result.get("findings")
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")
    for finding in findings:
        if not isinstance(finding, dict) or finding.get("kind") not in FINDING_KINDS:
            raise ValueError("finding has invalid kind")
        for key in ("description", "reproduction", "requested_change"):
            _text(finding.get(key), f"finding.{key}")
        _strings(finding.get("source_refs"), "finding.source_refs")
    if accepted and findings:
        raise ValueError("accepted review cannot have unresolved findings")
    if verdict == "revise" and not findings:
        raise ValueError("revise requires actionable findings")
    if any(finding["kind"] == "inventory" for finding in findings):
        _inventory_evidence(evidence_root)
