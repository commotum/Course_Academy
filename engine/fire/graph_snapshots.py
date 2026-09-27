"""Read saved graph SVG colors as display observations, not FIRe state.

Only local saved files are read. The compatible legacy public renderer maps its
``topic.repetition`` display field to colors; the server's relationship between
that field and FIRe's continuous repetition count is not supplied.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


LEGACY_COLORS = {
    "rgb(210, 231, 249)": "numeric-case-1",
    "rgb(165, 207, 243)": "numeric-case-2",
    "rgb(120, 182, 237)": "numeric-case-3",
    "rgb(74, 158, 232)": "numeric-case-4",
    "rgb(29, 134, 226)": "numeric-case-5",
    "rgb(23, 107, 181)": "truthy-default-not-numeric-1-through-5",
    "rgb(242, 242, 242)": "gray-no-numeric-constraint",
}
RENDERER_SOURCES = {
    "legacy": {"url": "https://mathacademy.com/js/knowledge-graph.js", "sha256": "9faf1eee0a0ee09c7e66c4da4db791088ab44ade2af23d317631d5bb71c90c79"},
    "newer": {"url": "https://mathacademy.com/js/student-knowledge-graph.js", "sha256": "094e279fd063cc926db7a583ab6a693fe519349bd5406a0cc2ac8cd1c2a351cb"},
}


def _source(path):
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _utc(value):
    return datetime.fromtimestamp(int(value), timezone.utc).isoformat()


def parse_saved_graph(path: str | Path) -> dict:
    """Preserve exact node IDs/fills; do not infer repetition from dark/gray."""
    path = Path(path)
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    nodes = []
    for node in root.iter():
        if "node" not in node.attrib.get("class", "").split():
            continue
        children = {child.tag.rsplit("}", 1)[-1]: child for child in node}
        if "title" not in children or "ellipse" not in children:
            raise ValueError(f"Missing node title/ellipse in {path}")
        topic = (children["title"].text or "").strip()
        if not topic.isdigit():
            raise ValueError(f"Nonnumeric graph topic ID: {topic!r}")
        ellipse = children["ellipse"]
        fill = ellipse.attrib.get("fill")
        nodes.append({
            "topic_id": topic, "fill": fill,
            "stroke_width": ellipse.attrib.get("stroke-width"),
            "legacy_display_category": LEGACY_COLORS.get(fill, "unrecognized-color"),
        })
    if len({node["topic_id"] for node in nodes}) != len(nodes):
        raise ValueError(f"Duplicate topic ID inside graph {path}")
    return {
        "source": _source(path), "root_id": root.attrib.get("id"),
        "legacy_renderer_compatible": root.attrib.get("id") == "graph" and all(
            node["stroke_width"] == "0" and node["fill"] in LEGACY_COLORS for node in nodes
        ),
        "node_count": len(nodes), "nodes": nodes,
    }


def _git_provenance(repo: Path, path: Path) -> dict:
    relative = path.relative_to(repo)
    try:
        value = subprocess.check_output(
            ["git", "-C", str(repo), "log", "-1", "--format=%H|%aI|%cI", "--", str(relative)],
            text=True, timeout=15,
        ).strip()
        changed = subprocess.check_output(
            ["git", "-C", str(repo), "diff", "--name-only", "HEAD", "--", str(relative)],
            text=True, timeout=15,
        ).strip()
        fields = value.split("|")
        return {"last_path_commit": fields[0], "author_time": fields[1], "committer_time": fields[2], "working_tree_differs_from_head": bool(changed)} if len(fields) == 3 else {"tracked_commit": None}
    except (subprocess.SubprocessError, OSError) as error:
        return {"unavailable": str(error)}


def build_graph_audit(ma_root: str | Path, progress_path: str | Path, *, include_git: bool = True) -> dict:
    ma_root, progress_path = Path(ma_root), Path(progress_path)
    log_path = ma_root / "PIPELINE/Math-Academy/0-Ingest/1-Course-Source/_course_progress_state.jsonl"
    script_path = log_path.with_name("course-source.py")
    logs = [json.loads(line) for line in log_path.read_text().splitlines() if line.strip()]
    completed_by_path = defaultdict(list)
    started_by_course = defaultdict(list)
    for row in logs:
        if row["status"] == "started":
            started_by_course[str(row["course_id"])].append(row)
        elif row["status"] == "completed" and row.get("graph_html_path"):
            completed_by_path[row["graph_html_path"]].append(row)
    graphs = []
    all_colors = Counter()
    all_categories = Counter()
    topic_colors = defaultdict(set)
    topic_categories = defaultdict(set)
    for path in sorted((ma_root / "COURSES/Math-Academy").rglob("Graph-*.html")):
        graph = parse_saved_graph(path)
        records = completed_by_path[str(path)]
        completions = sorted(records, key=lambda row: int(row["ts"]))
        latest = completions[-1] if completions else None
        bounds = None
        if latest:
            starts = [row for row in started_by_course[str(latest["course_id"])] if int(row["ts"]) <= int(latest["ts"])]
            bounds = {"last_started_utc": _utc(max(starts, key=lambda row: int(row["ts"]))["ts"]) if starts else None, "completed_utc": _utc(latest["ts"])}
        graph.update({
            "course_id": str(latest["course_id"]) if latest else None,
            "course_name": latest["name"] if latest else None,
            "capture_log_completion_records": len(completions),
            "capture_log_bounds": bounds,
            "learner_id": None,
            "git": _git_provenance(ma_root, path) if include_git else None,
        })
        graphs.append(graph)
        for node in graph["nodes"]:
            all_colors[node["fill"]] += 1
            all_categories[node["legacy_display_category"]] += 1
            topic_colors[node["topic_id"]].add(node["fill"])
            topic_categories[node["topic_id"]].add(node["legacy_display_category"])
    with progress_path.open(newline="", encoding="utf-8") as stream:
        history = list(csv.DictReader(stream))
    history_topics = {row["topic-id"] for row in history if row["topic-id"]}
    overlap = sorted(history_topics & set(topic_colors), key=int)
    conflicting = sorted((topic for topic, colors in topic_colors.items() if len(colors) > 1), key=int)
    capture_times = [graph["capture_log_bounds"]["completed_utc"] for graph in graphs if graph["capture_log_bounds"]]
    logged_completion_times = [_utc(row["ts"]) for records in completed_by_path.values() for row in records]
    return {
        "schema_version": 1,
        "sources": {"progress": _source(progress_path), "capture_log": _source(log_path), "capture_script": _source(script_path), "public_renderer_assets": RENDERER_SOURCES, "public_renderer_retrieved_date": "2026-09-26"},
        "summary": {
            "saved_graphs": len(graphs), "node_occurrences": sum(graph["node_count"] for graph in graphs),
            "unique_topic_ids": len(topic_colors), "legacy_compatible_graphs": sum(graph["legacy_renderer_compatible"] for graph in graphs),
            "color_counts": dict(sorted(all_colors.items())), "conditional_display_category_counts": dict(sorted(all_categories.items())),
            "conflicting_color_topic_count": len(conflicting), "history_topic_overlap_count": len(overlap),
            "history_topics_with_conflicting_colors": sorted(set(conflicting) & history_topics, key=int),
            "first_capture_log_completion_utc": min(capture_times, default=None), "last_capture_log_completion_utc": max(capture_times, default=None),
            "all_logged_graph_completion_records": len(logged_completion_times),
            "earliest_completion_including_overwritten_paths_utc": min(logged_completion_times, default=None),
            "verified_numeric_fire_states": 0, "verified_fire_transitions": 0,
        },
        "interpretation": {
            "observed": "Node topic IDs and exact fill colors in per-course saved HTML; capture-log times and Git commit provenance.",
            "conditional_mapping": "Palette, #graph root and zero stroke widths match the legacy public renderer. Numeric-case-1..5 refer only to numeric switch cases of its topic.repetition display field, conditional on that historical renderer being used.",
            "default_caveat": "Dark default does not mean >=6: every truthy value unequal to numeric 1..5, including fractions or strings, reaches default. Gray supplies no numeric repetition constraint.",
            "state_caveat": "April capture renderer version, learner identity and server mapping between display repetition and FIRe repNum/stability are not recorded. The newer renderer uses a different stability-to-HSL mapping and must not be inverted on these legacy colors.",
            "course_caveat": "Capture script switches active course before loading /learn and saving #graph. Cross-course differences are preserved, not reconciled into a single learner state or treated as before/after transitions.",
            "time_caveat": "Started/completed times bound the logging operation, not an authenticated answer or state timestamp; Git dates corroborate file provenance, not exact capture time. History completion times have no verified zone.",
        },
        "conflicting_color_topic_ids": conflicting,
        "history_overlap": [
            {"topic_id": topic, "fills": sorted(topic_colors[topic]), "conditional_display_categories": sorted(topic_categories[topic]), "history_task_ids": [row["task-id"] for row in history if row["topic-id"] == topic]}
            for topic in overlap
        ],
        "graphs": graphs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ma-root", type=Path, required=True)
    parser.add_argument("--progress", type=Path, default=Path("reference/progress.csv"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--without-git", action="store_true")
    args = parser.parse_args()
    audit = build_graph_audit(args.ma_root, args.progress, include_git=not args.without_git)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit["summary"], indent=2))


if __name__ == "__main__":
    main()
