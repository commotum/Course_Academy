"""Offline audit probes. No agent processes, database calls, or production edits."""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
from generator_pipeline import CodexSession
from generator_investigation import _rank


def probe_cache():
    with TemporaryDirectory(prefix="generator-audit-cache-") as directory:
        path = Path(directory)
        original = {"status": "ready", "summary": "Result from earlier source context"}
        (path / "result.json").write_text(json.dumps(original))
        with patch("generator_pipeline.subprocess.Popen", side_effect=AssertionError("No agent may launch")) as process:
            result = CodexSession(ROOT)("investigate", {"source_sha256": "changed-source", "workspace": str(path)}, path)
        return {
            "existing_result_returned_unchanged": result == original,
            "new_prompt_saved": (path / "prompt.txt").exists(),
            "subprocess_launched": process.called,
            "scope": "Direct offline call of current CodexSession; caller stages may add checks. This proves the session cache itself does not bind result to new context.",
        }


def probe_rank():
    target = {":db/id": 1, ":knowledge-point/title": "Integrating substitution", ":knowledge-point/key-prerequisites": [{":db/id": 900}]}
    complete = [{":db/id": i, ":knowledge-point/title": "Integrating substitution", ":knowledge-point/key-prerequisites": []} for i in range(2, 27)]
    complete.append({":db/id": 100, ":knowledge-point/title": "Recognizing derivatives", ":knowledge-point/key-prerequisites": [{":db/id": 900}]})
    titles = [{k: row[k] for k in (":db/id", ":knowledge-point/title")} for row in complete]
    titles.sort(key=lambda row: _rank(row, target))
    first_ids = {row[":db/id"] for row in titles[:25]}
    first = min((row for row in complete if row[":db/id"] in first_ids), key=lambda row: _rank(row, target))
    global_best = min(complete, key=lambda row: _rank(row, target))
    return {
        "first_group_best": first[":db/id"],
        "global_best_by_same_rank_function": global_best[":db/id"],
        "globally_better_candidate_outside_first_group": global_best[":db/id"] not in first_ids,
        "scope": "Synthetic reconstruction of two-stage metadata ranking with current _rank; not a claim about a particular live donor.",
    }


if __name__ == "__main__":
    result = {"session_cache": probe_cache(), "reference_ranking": probe_rank()}
    assert result["session_cache"]["existing_result_returned_unchanged"]
    assert not result["session_cache"]["new_prompt_saved"]
    assert not result["session_cache"]["subprocess_launched"]
    assert result["reference_ranking"]["globally_better_candidate_outside_first_group"]
    print(json.dumps(result, indent=2))
