"""Read captured MathML for bases whose archive widths need more evidence."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import collections
import hashlib
import importlib.util
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
REPAIR = HERE.parent
ROOT = REPAIR.parents[3]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


repair = load("captured_hat_repair", REPAIR / "repair.py")
history = load("captured_hat_renderer", ROOT / "scripts/import_historical_question_content.py")
metadata = {value[":db/id"]: value for value in json.loads((REPAIR / "evidence/metadata.json").read_text())}
candidates = json.loads((REPAIR / "candidates.json").read_text())
files = [ROOT / name for name in subprocess.run(["rg", "--files", "reference/mathacademy"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()]
cache = {}
widths_path = HERE / "supplemental-widths.json"
widths = json.loads(widths_path.read_text()) if widths_path.exists() else {}
archive_path = REPAIR / "source/structured-widths.json"
resolved = (json.loads(archive_path.read_text()) if archive_path.exists() else {}) | widths
unresolved = []
for candidate in candidates:
    bases = {value["base"] for value in repair.structured_occurrences(candidate["value"])}
    bases = {base for base in bases if base not in resolved and
             str(candidate["entity"]) + "|" + str(candidate["attribute_id"]) + "|" + base not in resolved}
    if not bases:
        continue
    meta = metadata[candidate["entity"]]
    if ":answer-field/_choices" in meta:
        meta = meta[":answer-field/_choices"][":question/_answer-fields"]
    source_id = meta.get(":question/math-academy-id")
    if source_id and source_id.startswith("q-"):
        qid = source_id[2:]
        pattern = re.compile(r"q-?" + qid + r"(?:-|\.|$)")
        choices = [path for path in files if pattern.search(path.name)
                   and (path.suffix == ".html" or path.suffix == ".json" and "question-capture" in path.parts)]
    elif meta.get(":tutorial/math-academy-id") == 14794:
        choices = [path for path in files if path.name == "tutorial-14794.html"]
    else:
        continue
    found = collections.defaultdict(list)
    for path in choices:
        if path not in cache:
            data = path.read_bytes()
            if path.suffix == ".json":
                content = json.loads(data).get("html", "")
            else:
                content = data.decode()
            soup = BeautifulSoup(content, "html.parser")
            accents = []
            for mover in soup.find_all("mover"):
                children = mover.find_all(recursive=False)
                if len(children) != 2 or children[1].name != "mo" or children[1].get_text().strip() not in ("^", "ˆ"):
                    continue
                renderer = history.Renderer(None)
                base = renderer.m(children[0])
                if renderer.errors:
                    continue
                attrs = children[1].attrs
                command = "hat" if attrs.get("stretchy") == "false" else "widehat"
                accents.append({"base": base, "command": command, "source_file": str(path),
                                "source_sha256": hashlib.sha256(data).hexdigest(),
                                "source_identity": source_id or "tutorial-14794",
                                "operator_attributes": attrs, "mathml": str(mover)})
            cache[path] = accents
        for accent in cache[path]:
            if accent["base"] in bases:
                found[accent["base"]].append(accent)
    for base in bases:
        possibilities = {value["command"] for value in found[base]}
        if len(possibilities) != 1:
            unresolved.append({"entity": candidate["entity"], "attribute_id": candidate["attribute_id"],
                               "source_identity": source_id, "base": base, "commands": sorted(possibilities),
                               "source_files": [str(path) for path in choices]})
            continue
        key = str(candidate["entity"]) + "|" + str(candidate["attribute_id"]) + "|" + base
        first = found[base][0]
        widths[key] = {"command": first["command"], "source_identity": first["source_identity"],
                       "source_file": first["source_file"], "source_sha256": first["source_sha256"],
                       "operator_attributes": first["operator_attributes"], "mathml": first["mathml"],
                       "matching_source_occurrences": len(found[base]),
                       "all_matching_source_widths_agree": True}
(HERE / "supplemental-widths.json").write_text(json.dumps(widths, ensure_ascii=False, indent=2) + "\n")
(HERE / "supplemental-unresolved.json").write_text(json.dumps(unresolved, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"field_base_widths": len(widths), "commands": dict(collections.Counter(value["command"] for value in widths.values())), "unresolved": len(unresolved), "source_files_read": len(cache)}, indent=2))
