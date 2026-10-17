"""Inventory captured assessment questions without changing captures or the database.

The finalized result questions are the unit of observation. Attempts and observed
steps are corroborating evidence, not additional question occurrences. Numeric
history URL fragments are preserved as source anchors; they are not assumed to be
EDB knowledge-point IDs. Import ``collect`` to reuse this extraction.
"""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re


class HistoryHeader(HTMLParser):
    """Read explicit history question identities, KP links, and question numbers."""

    def __init__(self):
        super().__init__()
        self.question_ids = []
        self.links = []
        self.numbers = []
        self.active = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "div" and "question" in classes:
            match = re.fullmatch(r"question-(\d+)", attrs.get("id", ""))
            if match:
                self.question_ids.append("q-" + match[1])
        if tag == "a" and "questionKP" in classes:
            self.links.append({"href": attrs.get("href", ""), "title": ""})
            self.active, self.parts = "a", []
        elif tag == "span" and "questionNumber" in classes:
            self.active, self.parts = "span", []

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.active:
            text = " ".join("".join(self.parts).split())
            if tag == "a":
                self.links[-1]["title"] = text
            else:
                match = re.fullmatch(r"(\d+)\.?", text)
                if match:
                    self.numbers.append(int(match[1]))
            self.active, self.parts = None, []


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def numeric(value):
    value = str(value) if value is not None else ""
    return value if value.isdigit() else None


def collect(root):
    """Return a reproducible inventory of all completed current assessments."""
    root = Path(root).resolve()
    captures = root / "reference/mathacademy/capture"
    rows, assessments, exclusions, ambiguities = [], [], [], []
    source_manifest = {}
    observed_kinds = Counter()

    def source(path):
        path = Path(path)
        if not path.is_absolute():
            path = root / path
        label = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        raw = path.read_bytes()
        source_manifest[label] = sha256(raw)
        return label, raw, source_manifest[label]

    for activity_path in sorted(captures.glob("*/*/activity.json")):
        activity = json.loads(activity_path.read_bytes())
        observed_kinds[str(activity.get("kind"))] += 1
        if activity.get("kind") != "assessment":
            continue
        task_dir = activity_path.parent
        account, task_id = task_dir.parent.name, task_dir.name
        task_key = f"{account}/{task_id}"
        content_path = task_dir / "content.json"
        complete_path = task_dir / "capture-complete.json"
        missing = [p.name for p in (content_path, complete_path) if not p.exists()]
        if missing:
            exclusions.append({"task_key": task_key, "reason": "incomplete_capture", "missing": missing})
            continue

        activity_file, _, activity_hash = source(activity_path)
        content_file, raw, content_hash = source(content_path)
        content = json.loads(raw)
        complete_file, raw, complete_hash = source(complete_path)
        completed = json.loads(raw)
        task_issues = []
        for key in ("task_id", "kind", "course_id", "title"):
            if str(activity.get(key)) != str(content.get(key)):
                task_issues.append({"reason": "activity_content_conflict", "field": key,
                                    "activity": activity.get(key), "content": content.get(key)})
        if str(activity.get("task_id")) != task_id:
            task_issues.append({"reason": "directory_task_id_conflict"})
        if str(completed.get("task_id")) != task_id:
            task_issues.append({"reason": "completion_task_id_conflict"})

        questions = content.get("questions", [])
        if not isinstance(questions, list):
            exclusions.append({"task_key": task_key, "reason": "questions_not_a_list"})
            continue
        expected = activity.get("details", {}).get("question_count")
        if expected is not None and int(expected) != len(questions):
            task_issues.append({"reason": "declared_question_count_mismatch", "declared": expected,
                                "captured": len(questions)})
        attempt_map = defaultdict(list)
        for attempt in content.get("attempts", []):
            attempt_map[attempt.get("question", {}).get("math_academy_id")].append(attempt)
        task_rows = []
        for index, q in enumerate(questions, 1):
            qid = q.get("math_academy_id")
            issues = []
            if not re.fullmatch(r"q-\d+", qid or ""):
                issues.append({"reason": "missing_permanent_question_id"})
            headers = {}
            for key in ("html", "raw_html"):
                if q.get(key):
                    parsed = HistoryHeader()
                    parsed.feed(q[key])
                    headers[key] = parsed
            history_path = q.get("html_path")
            history_file = history_hash = None
            if history_path and Path(history_path).exists():
                history_file, history_raw, history_hash = source(history_path)
                parsed = HistoryHeader()
                parsed.feed(history_raw.decode("utf-8"))
                headers["history_file"] = parsed
            else:
                issues.append({"reason": "missing_history_file", "path": history_path})

            topic_candidates = {numeric(q.get("topic_id"))} - {None}
            anchor_candidates = {numeric(q.get(k)) for k in (
                "knowledge_point_source_id", "knowledge_point_id", "kp_id")} - {None}
            hrefs = {q.get("kp_href")} - {None, ""}
            numbers = set()
            for origin, header in headers.items():
                if header.question_ids != [qid]:
                    issues.append({"reason": "history_question_id_conflict", "origin": origin,
                                   "observed": header.question_ids})
                if len(header.links) != 1 or len(header.numbers) != 1:
                    issues.append({"reason": "history_header_shape", "origin": origin,
                                   "links": len(header.links), "numbers": header.numbers})
                hrefs.update(link["href"] for link in header.links)
                numbers.update(header.numbers)
            for href in hrefs:
                match = re.search(r"/topics/(\d+)#(\d+)(?:$|[?&])", href)
                if match:
                    topic_candidates.add(match[1])
                    anchor_candidates.add(match[2])
                else:
                    issues.append({"reason": "unrecognized_kp_href", "href": href})
            if len(topic_candidates) != 1:
                issues.append({"reason": "ambiguous_topic_id", "candidates": sorted(topic_candidates)})
            if len(anchor_candidates) != 1:
                issues.append({"reason": "ambiguous_raw_kp_anchor", "candidates": sorted(anchor_candidates)})
            position = q.get("sequence_position")
            if numbers != {position} or position != index:
                issues.append({"reason": "question_order_conflict", "array_position": index,
                               "sequence_position": position, "header_numbers": sorted(numbers)})
            attempts = attempt_map.get(qid, [])
            for attempt in attempts:
                aq = attempt.get("question", {})
                if aq.get("sequence_position") != position:
                    issues.append({"reason": "attempt_order_conflict"})
                if numeric(aq.get("topic_id")) not in ({None} | topic_candidates):
                    issues.append({"reason": "attempt_topic_conflict"})
            if len(attempts) > 1:
                issues.append({"reason": "multiple_attempt_records", "count": len(attempts)})

            row = {
                "occurrence_id": f"{task_key}/{qid or index}", "account": account,
                "task_id": task_id, "task_key": task_key, "title": activity.get("title"),
                "course_id": numeric(activity.get("course_id")), "question_id": qid,
                "question_number": position if numbers == {position} else None,
                "array_position": index, "sequence_position": position,
                "question_order_evidence": "explicit result-header number corroborated by content array"
                if numbers == {position} and position == index else "unresolved",
                "raw_knowledge_point_id": q.get("knowledge_point_id"),
                "raw_kp_id": q.get("kp_id"),
                "knowledge_point_source_id": q.get("knowledge_point_source_id"),
                "raw_kp_anchor_id": next(iter(anchor_candidates)) if len(anchor_candidates) == 1 else None,
                "source_example_id": q.get("source_example_id"),
                "topic_id": next(iter(topic_candidates)) if len(topic_candidates) == 1 else None,
                "topic_title": q.get("topic_title"), "kp_title": q.get("knowledge_point"),
                "kp_href": q.get("kp_href"), "difficulty": q.get("difficulty"),
                "grade": q.get("grade"), "source_grade": q.get("source_grade"),
                "problem": q.get("problem"), "captured_at": q.get("captured_at"),
                "source_file": content_file, "source_sha256": content_hash,
                "source_json_pointer": f"/questions/{index - 1}",
                "history_html_file": history_file, "history_html_sha256": history_hash,
                "attempt_record_count": len(attempts),
                "history_without_attempt": not attempts,
                "issues": issues,
            }
            task_rows.append(row)
            rows.append(row)
            if issues:
                ambiguities.append({"occurrence_id": row["occurrence_id"], "issues": issues})

        topics = defaultdict(list)
        for row in task_rows:
            topics[row["topic_id"]].append(row)
        question_ids = [row["question_id"] for row in task_rows]
        if len(question_ids) != len(set(question_ids)):
            task_issues.append({"reason": "duplicate_question_ids_within_assessment"})
        extra_attempts = sorted(str(k) for k in attempt_map if k not in question_ids)
        if extra_attempts:
            task_issues.append({"reason": "attempts_absent_from_final_questions", "question_ids": extra_attempts})
        assessment = {
            "account": account, "task_id": task_id, "task_key": task_key,
            "title": activity.get("title"), "course_id": numeric(activity.get("course_id")),
            "assessment_id": activity.get("details", {}).get("test_id"),
            "retake": activity.get("details", {}).get("retake"),
            "completed_at": completed.get("completed_at"), "question_count": len(task_rows),
            "declared_question_count": expected, "attempt_count": len(content.get("attempts", [])),
            "question_ids": question_ids,
            "topics": [{"topic_id": topic, "question_count": len(group),
                        "question_ids": [q["question_id"] for q in group],
                        "kp_anchor_ids": sorted({q["raw_kp_anchor_id"] for q in group if q["raw_kp_anchor_id"]}),
                        "kp_titles": sorted({q["kp_title"] for q in group if q["kp_title"]})}
                       for topic, group in sorted(topics.items(), key=lambda pair: str(pair[0]))],
            "activity_file": activity_file, "activity_sha256": activity_hash,
            "source_file": content_file, "source_sha256": content_hash,
            "completion_file": complete_file, "completion_sha256": complete_hash,
            "issues": task_issues,
        }
        assessments.append(assessment)
        if task_issues:
            ambiguities.append({"task_key": task_key, "issues": task_issues})

    by_question = defaultdict(list)
    by_task = defaultdict(list)
    for row in rows:
        by_question[row["question_id"]].append(row["occurrence_id"])
    for task in assessments:
        by_task[task["task_id"]].append(task["task_key"])
    duplicate_questions = {k: v for k, v in by_question.items() if len(v) > 1}
    duplicate_tasks = {k: v for k, v in by_task.items() if len(v) > 1}
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(), "schema_version": 1,
        "methodology": {
            "selection": "activity.json kind=assessment, with content.json and capture-complete.json",
            "question_unit": "One finalized content.questions item per account/task/question; attempts are not appended.",
            "source_identity": "Explicit permanent q-ID and numeric topic/KP links from result HTML, cross-checked against saved metadata and the on-disk history fragment.",
            "kp_identity_caveat": "raw_kp_anchor_id is the source /topics/{topic}#{anchor} fragment. It is not automatically an EDB knowledge-point/id or a canonical-example ID.",
            "order": "Question order is the quiz result-header question number, not the KP position within its lesson.",
            "topic_labels": "The result header labels the KP, not the topic; missing topic titles remain null until an authoritative identity join.",
            "missing_attempts": "Final result history includes unanswered questions; these are retained in the assessment sample.",
            "deduplication": "Report duplicate task and permanent question IDs explicitly; never merge different assessment occurrences silently.",
            "title_matching": "No title-only identity inference.",
        },
        "summary": {
            "assessment_count": len(assessments), "question_occurrences": len(rows),
            "unique_question_ids": len(by_question), "unique_topic_ids": len({q["topic_id"] for q in rows if q["topic_id"]}),
            "unique_raw_kp_anchors": len({q["raw_kp_anchor_id"] for q in rows if q["raw_kp_anchor_id"]}),
            "assessments_by_account": dict(Counter(t["account"] for t in assessments)),
            "assessments_by_course_id": dict(Counter(t["course_id"] for t in assessments)),
            "questions_by_account": dict(Counter(q["account"] for q in rows)),
            "questions_by_course_id": dict(Counter(q["course_id"] for q in rows)),
            "question_difficulty": dict(Counter(q["difficulty"] for q in rows)),
            "question_grades": dict(Counter(q["grade"] for q in rows)),
            "questions_without_attempts": sum(q["history_without_attempt"] for q in rows),
            "questions_missing_raw_knowledge_point_id": sum(q["raw_knowledge_point_id"] is None for q in rows),
            "questions_with_source_example_id": sum(q["source_example_id"] is not None for q in rows),
            "question_order_verified": sum(q["question_order_evidence"] != "unresolved" for q in rows),
            "source_header_files_verified": sum(q["history_html_file"] is not None for q in rows),
            "observed_activity_kinds": dict(observed_kinds), "excluded_assessments": len(exclusions),
            "ambiguous_records": len(ambiguities),
        },
        "assessments": assessments, "questions": rows, "exclusions": exclusions,
        "ambiguities": ambiguities, "duplicate_question_ids": duplicate_questions,
        "duplicate_task_ids": duplicate_tasks, "source_manifest": source_manifest,
        "script_sha256": sha256(Path(__file__).read_bytes()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = collect(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result["summary"], indent=2))
    if result["ambiguities"]:
        raise SystemExit("Inventory written with unresolved evidence conflicts; inspect ambiguities.")


if __name__ == "__main__":
    main()
