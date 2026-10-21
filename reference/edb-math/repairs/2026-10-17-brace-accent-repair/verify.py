"""Verify exact repair datoms, full projections, and immutable committed readback.

Default mode inspects only saved noncommitting preview evidence.  --commit
verifies the receipt and reads the exact db-after basis in batches of 250.
Neither mode submits a transaction.
"""
from concurrent.futures import ThreadPoolExecutor
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "Cargo.toml").exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads
from scripts.generator_publish import Publisher

HERE = Path(__file__).resolve().parent
ALLOWED_ATTRIBUTES = {":question/problem", ":question/worked-solution", ":tutorial/content"}
BATCH_SIZE = 250


def by_id(rows):
    return sorted(rows, key=lambda value: value[":db/id"])


def verify(commit=False):
    plan = json.loads((HERE / "plan.json").read_text())
    changes = json.loads((HERE / "changes.json").read_text())
    transaction = (HERE / "transaction.edn").read_text()
    assert hashlib.sha256(transaction.encode()).hexdigest() == plan["transaction_sha256"]
    assert len(changes) == plan["changed_attributes"] == 1688
    assert len({change["entity"] for change in changes}) == plan["changed_entities"] == 1615
    assert sum(change["repaired_brace_occurrences"] for change in changes) == plan["repaired_brace_occurrences"] == 4372
    edits = {(change["entity"], change["attribute"]): change for change in changes}
    assert len(edits) == len(changes)
    for change in changes:
        assert change["attribute"] in ALLOWED_ATTRIBUTES
        assert change["before"] != change["after"]
        assert not re.search("[⏟⏞︷︸]", change["after"])

    attrs = dict(loads((HERE / "evidence/attributes.edn").read_text()))
    preview = loads((HERE / "preview.edn").read_text())
    report = loads((HERE / "receipt.edn").read_text()) if commit else preview
    assert preview[":edb/committed"] is False
    assert preview[":edb/speculative"] is True
    assert report[":edb/committed"] is commit
    assert report[":edb/db-before-t"] == preview[":edb/db-before-t"] == plan["snapshot_basis"]
    assert ":edb/report-error" not in report
    if commit:
        assert report[":edb/basis-t"] == report[":edb/db-after-t"]
        assert report[":edb/db-after-t"] == preview[":edb/db-after-t"]

    expected_datoms = {(change["entity"], change["attribute"], change[stage], added)
                       for change in changes for stage, added in [("before", False), ("after", True)]}
    assert len(expected_datoms) == 2 * len(changes)
    actual_datoms = []
    for entity, attribute, value, tx, source, added in report[":edb/tx-data"]:
        assert source == plan["source_eid"]
        attr = str(attrs[attribute])
        if attr != ":db/txInstant":
            actual_datoms.append((entity, attr, value, added))
    assert len(actual_datoms) == len(expected_datoms)
    assert set(actual_datoms) == expected_datoms, (set(actual_datoms) - expected_datoms, expected_datoms - set(actual_datoms))

    seen_edits = set()

    def apply_expected(value):
        if isinstance(value, dict):
            for attr in value:
                key = value.get(":db/id"), str(attr)
                if key in edits:
                    edit = edits[key]
                    assert value[attr] == edit["before"]
                    value[attr] = edit["after"]
                    seen_edits.add(key)
                else:
                    apply_expected(value[attr])
        elif isinstance(value, list):
            for child in value:
                apply_expected(child)

    groups = loads((HERE / "native-pulls.edn").read_text())
    assert {name for name, _, _ in groups} == {"questions", "tutorials"}
    expected_projections = {}
    for name, pattern, ids in groups:
        before = loads((HERE / f"preview-{name}-before.edn").read_text())
        after = loads((HERE / f"preview-{name}-after.edn").read_text())
        evidence = loads((HERE / f"evidence/{name}.edn").read_text())
        assert len(before) == len(after) == len(ids) == len(set(ids))
        assert {value[":db/id"] for value in before} == set(ids)
        assert by_id(before) == by_id(evidence), (name, "preview input differs from saved snapshot")
        expected = copy.deepcopy(before)
        apply_expected(expected)
        assert by_id(expected) == by_id(after), (name, "unexpected projected change")
        expected_projections[name] = {value[":db/id"]: value for value in after}
    assert seen_edits == set(edits), ("an intended edit is absent from the full projections", set(edits) - seen_edits)

    readback_batches = 0
    if commit:
        intent = json.loads((HERE / "commit-intent.json").read_text())
        assert intent["submission_authorized"] is True
        assert intent["transaction_edn"] == transaction
        assert intent["transaction_sha256"] == plan["transaction_sha256"]
        assert intent["basis"] == plan["snapshot_basis"]
        assert intent["expected_lineage"] == plan["lineage"]
        assert intent["database"] == plan["database"]
        assert intent["source_edn"] == plan["source"]
        client = Publisher.from_environment(source=plan["source"]).client
        status = client.status()
        assert status["database"] == plan["database"]
        assert status["lineage"] == plan["lineage"]
        basis = report[":edb/db-after-t"]
        assert status["basis"] >= basis
        batches = [(name, pattern, ids[offset:offset + BATCH_SIZE], offset)
                   for name, pattern, ids in groups for offset in range(0, len(ids), BATCH_SIZE)]
        readback_batches = len(batches)

        def read(batch):
            name, pattern, ids, offset = batch
            rows = client.query("[:find (pull ?e " + pattern + ") :in $ [?e ...] :where [?e _ _]]",
                                [ids], HERE / "readback", name + "-" + str(offset), basis)
            actual = [value for [value] in rows]
            assert len(actual) == len(ids)
            assert {value[":db/id"] for value in actual} == set(ids)
            expected = [expected_projections[name][entity] for entity in ids]
            assert by_id(actual) == by_id(expected), (name, offset, "committed readback differs")
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(read, batches))

    result = {
        "passed": True, "committed": commit,
        "basis_before": report[":edb/db-before-t"], "basis_after": report[":edb/db-after-t"],
        "changed_attributes": len(changes), "changed_entities": plan["changed_entities"],
        "repaired_brace_occurrences": plan["repaired_brace_occurrences"],
        "exact_expected_datoms_only": True, "complete_projections_match": True,
        "verified_groups": [name for name, _, _ in groups],
        "saved_snapshot_matches_preview_input": True,
        "no_answer_values_ids_banks_keys_or_historical_responses_changed": True,
        "difficulty_curriculum_links_and_lesson_routes_preserved": True,
        "missing_solutions_and_keys_preserved": True,
        "no_raw_brace_glyphs_in_repaired_fields": True,
        "readback_basis": report[":edb/db-after-t"] if commit else None,
        "readback_batch_size": BATCH_SIZE if commit else None,
        "readback_batches": readback_batches,
        "transaction_sha256": plan["transaction_sha256"],
    }
    (HERE / ("commit-verification.json" if commit else "preview-verification.json")).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    verify(parser.parse_args().commit)
