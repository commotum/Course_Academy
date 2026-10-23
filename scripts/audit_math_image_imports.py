#!/usr/bin/env python3
"""Audit an immutable EDB export for formulas stored as images; never writes EDB.

Read every exported string, classify referenced SVG bytes, and connect raster
files to original SVG capture metadata. Reports retain every entity/attribute,
occurrence offset, current value hash, transaction, source and ownership context.
Unknown raster assets remain explicit review items, never assumed to be diagrams.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

IMAGE = re.compile(r"images/[0-9a-f]{2}/[0-9a-f]{64}\.(?:png|svg|jpg|jpeg|gif|webp|avif)")
PARENTS = {
    "topic/knowledge-points", "knowledge-point/canonical-example", "knowledge-point/questions",
    "question/answer-fields", "answer-field/choices", "activity/steps", "step/content",
    "multistep/steps", "assigned-problem/content",
}
META = {
    "question/id", "question/math-academy-id", "tutorial/id", "tutorial/math-academy-id",
    "tutorial/title", "topic/id", "topic/math-academy-id", "topic/title",
    "knowledge-point/id", "knowledge-point/title", "activity/id", "activity/title",
    "activity/scope", "answer-field/id", "answer-field/key", "answer-field/type",
    "answer-field/correct", "answer/id", "answer/type", "db/ident",
}


def svg_kind(text: str) -> tuple[str, str]:
    """Use structural MathJax evidence, not an SVG extension or formula-like pixels."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        # Captured browser outerHTML may contain HTML-only markup inside titles.
        if re.search(r'data-mml-node=["\']math["\']', text) and re.search(r'\bwidth=["\'][^"\']+ex["\']', text):
            return "math-svg", "MathJax math root and ex dimensions in captured outerHTML"
        return "invalid-svg", "XML parsing failed; inspect source"
    local = lambda n: n.tag.rsplit("}", 1)[-1]
    if local(root) != "svg":
        return "invalid-svg", "root is not SVG"
    math_roots = {n for n in root.iter() if n.get("data-mml-node") == "math"}
    ex = root.get("width", "").endswith("ex") and root.get("height", "").endswith("ex")
    if math_roots:
        parents = {child: node for node in root.iter() for child in node}
        drawing = {"path", "use", "text", "line", "polyline", "polygon", "circle", "ellipse", "rect", "image"}
        outside = False
        for node in root.iter():
            if local(node) not in drawing:
                continue
            cur = node
            while cur in parents and cur not in math_roots and local(cur) not in ("defs", "title"):
                cur = parents[cur]
            if cur not in math_roots and local(cur) not in ("defs", "title"):
                outside = True
        if not outside or ex:
            return "math-svg", "MathJax data-mml-node=math covers the formula rendering"
        return "mixed-math-graphic", "MathJax labels plus drawing outside math roots"
    if ex and ("MathJax" in text or "MJX-" in text or "currentColor" in text or "STIXWEB" in text):
        return "math-svg", "legacy MathJax glyph rendering with ex dimensions"
    return "non-math-svg", "no whole-formula MathJax signature"


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            if isinstance(child, (dict, list)):
                yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            if isinstance(child, (dict, list)):
                yield from objects(child)


def capture_index(paths: list[Path], relevant_hashes: set[str]):
    index = defaultdict(list)
    stats = Counter()
    for path in paths:
        try:
            value = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise ValueError(f"Cannot audit capture evidence {path}: {exc}") from exc
        stats["files_read"] += 1
        for obj in objects(value):
            if obj.get("tag") != "svg" or not isinstance(obj.get("html"), str):
                continue
            html = obj["html"]
            hashes = {obj.get("sha256"), obj.get("original_svg_sha256"), hashlib.sha256(html.encode()).hexdigest()}
            for key in ("path", "original_svg_path"):
                if isinstance(obj.get(key), str):
                    hashes.add(Path(obj[key]).stem)
            hashes &= relevant_hashes
            if not hashes:
                continue
            kind, reason = svg_kind(html)
            info = {"file": str(path), "kind": kind, "reason": reason,
                    "tag": "svg", "representation": obj.get("representation"),
                    "original_path": obj.get("path")}
            for digest in hashes:
                if len(index[digest]) < 5 and info not in index[digest]:
                    index[digest].append(info)
            stats["relevant_svg_records"] += 1
    return index, dict(stats)


def run(snapshot: Path, math_root: Path, evidence_paths: list[Path], output: Path):
    records = defaultdict(dict)
    parents = defaultdict(set)
    uses = defaultdict(list)
    facts = []
    counts = Counter()
    string_counts = Counter()
    noncanonical = []
    for line in snapshot.open():
        row = json.loads(line)
        eid, attr, value = row["e"], row["a"], row["v"]
        counts[attr] += 1
        if attr in META:
            records[eid][attr] = value
        if attr in PARENTS:
            parents[value].add(eid)
        if attr in ("task-item/content", "task-item/responses"):
            parents[value].add(eid)
        if not isinstance(value, str):
            continue
        string_counts[attr] += 1
        matches = list(IMAGE.finditer(value))
        if matches:
            fact = {**row, "value_sha256": hashlib.sha256(value.encode()).hexdigest(),
                    "images": [{"path": m[0], "start": m.start(), "end": m.end()} for m in matches]}
            facts.append(fact)
            for m in matches:
                uses[m[0]].append((eid, attr))
        # Surface image syntaxes that a canonical-path scan would otherwise miss.
        stripped = IMAGE.sub("", value)
        if re.search(r'!\[[^\]]*\]\((?!\))|<(?:img|svg)\b|data:image/', stripped, re.I):
            noncanonical.append({**row, "reason": "noncanonical or embedded image syntax"})
    hashes = {Path(p).stem for p in uses}
    evidence, evidence_stats = capture_index(evidence_paths, hashes)
    assets = {}
    for relative in sorted(uses):
        path = math_root / relative
        info = {"uses": len(uses[relative]), "capture_evidence": evidence.get(path.stem, [])}
        if not path.is_file():
            info.update(kind="missing-asset", reason="referenced bytes unavailable")
        else:
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != path.stem:
                raise ValueError(f"Image bytes do not match their address: {path}")
            if path.suffix == ".svg":
                kind, reason = svg_kind(raw.decode())
                info.update(kind=kind, reason=reason)
            else:
                kinds = {e["kind"] for e in info["capture_evidence"]}
                kind = ("math-raster" if "math-svg" in kinds else
                        "mixed-math-graphic" if "mixed-math-graphic" in kinds else
                        "captured-non-math-raster" if "non-math-svg" in kinds else "unclassified-raster")
                info.update(kind=kind, reason="linked original SVG metadata" if kinds else "no SVG evidence; retain for raster/source review")
        assets[relative] = info

    def context(eid):
        seen, todo = set(), deque([eid])
        while todo:
            node = todo.popleft()
            if node in seen:
                continue
            seen.add(node)
            r = records.get(node, {})
            # Presentation backrefs are evidence, not a path to unrelated content.
            todo.extend(parents[node])
            if "activity/scope" in r:
                todo.append(r["activity/scope"])
        return [{"entity": n, **records[n]} for n in sorted(seen) if n in records]

    findings, review = [], []
    for fact in facts:
        affected = [m for m in fact["images"] if assets[m["path"]]["kind"] in ("math-svg", "math-raster")]
        uncertain = [m for m in fact["images"] if assets[m["path"]]["kind"] not in ("math-svg", "math-raster", "non-math-svg", "captured-non-math-raster")]
        if affected:
            findings.append({**fact, "math_images": affected, "context": context(fact["e"])})
        if uncertain:
            review.append({"entity": fact["e"], "attribute": fact["a"], "images": uncertain})
    output.mkdir(parents=True, exist_ok=True)
    def save(name, value):
        (output / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    save("assets.json", assets)
    save("findings.json", findings)
    save("raster-and-graphic-review.json", review)
    save("noncanonical-image-review.json", noncanonical)
    by_kind = Counter()
    for item in findings:
        for image in item["math_images"]:
            by_kind[assets[image["path"]]["kind"]] += 1
    summary = {"basis_t": json.loads(snapshot.with_suffix(".manifest.json").read_text())["basis_t"],
        "snapshot": str(snapshot), "exported_facts_scanned": sum(counts.values()),
        "string_facts_scanned": sum(string_counts.values()), "string_attributes_scanned": dict(string_counts),
        "image_bearing_facts": len(facts), "image_occurrences": sum(len(f["images"]) for f in facts),
        "unique_image_assets": len(assets), "assets_by_kind": dict(Counter(a["kind"] for a in assets.values())),
        "confirmed_affected_entities": len({f["e"] for f in findings}),
        "confirmed_affected_attributes": len(findings), "confirmed_math_image_occurrences": sum(by_kind.values()),
        "confirmed_occurrences_by_kind": dict(by_kind),
        "confirmed_attributes_by_name": dict(Counter(f["a"] for f in findings)),
        "confirmed_attributes_by_transaction": dict(Counter(f["t"] for f in findings)),
        "noncanonical_image_facts": len(noncanonical), "capture_evidence": evidence_stats}
    save("summary.json", summary)
    with (output / "affected.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["entity", "attribute", "math_image_occurrences", "current_t", "source", "topic_ids", "question_ma_id", "tutorial_ma_id", "current_value_sha256"])
        for f in findings:
            topics = sorted({r["topic/math-academy-id"] for r in f["context"] if "topic/math-academy-id" in r})
            own = records[f["e"]]
            writer.writerow([f["e"], f["a"], len(f["math_images"]), f["t"], f["source"], ";".join(map(str, topics)), own.get("question/math-academy-id", ""), own.get("tutorial/math-academy-id", ""), f["value_sha256"]])
    print(json.dumps(summary, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("snapshot", type=Path)
    p.add_argument("--math-root", type=Path, default=Path("/media/jake/SSD/EDB/math"))
    p.add_argument("--evidence-list", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    run(a.snapshot, a.math_root, [Path(line) for line in a.evidence_list.read_text().splitlines() if line], a.output)


if __name__ == "__main__":
    main()
