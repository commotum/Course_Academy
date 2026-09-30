#!/usr/bin/env python3
"""Preview or apply generated reconciliation batches to the local EDB database."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--database", default=os.environ.get("EDB_DATABASE", "course-academy-v2"))
    parser.add_argument("--endpoint", default=os.environ.get("EDB_ENDPOINT", "/tmp/course-academy-edb-v2/writer.sock"))
    parser.add_argument("--report-dir", type=Path, default=Path(".local/edb/reconciliation/commits"))
    args = parser.parse_args()
    if not os.environ.get("EDB_POSTGRES_URL"):
        parser.error("Set EDB_POSTGRES_URL for the local database.")
    edb = os.environ.get("EDB_BIN", "/home/jake/Developer/EDB/target/release/edb")
    args.report_dir.mkdir(parents=True, exist_ok=True)
    for path in args.files:
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        request_key = f"ma-reconcile-{digest}"
        common = ["--database", args.database, "--file", str(path)]
        with tempfile.TemporaryFile() as preview:
            subprocess.run([edb, "with", *common], check=True, stdout=preview)
        if not args.apply:
            print(f"Validated {path}", flush=True)
            continue
        report = args.report_dir / f"{digest}.edn"
        with report.open("wb") as output:
            subprocess.run(
                [edb, "transact", *common, "--endpoint", args.endpoint,
                 "--request-key", request_key, "--timeout-ms", "180000"],
                check=True, stdout=output,
            )
        result = report.read_text()
        if not result.startswith("{:edb/committed true"):
            raise RuntimeError(f"Commit not confirmed; retain request key {request_key} and inspect {report}")
        basis = re.search(r":edb/basis-t (\d+)", result)
        record = {"file": str(path), "sha256": digest, "request_key": request_key,
                  "basis_t": int(basis[1]) if basis else None,
                  "replayed": ":edb/replayed true" in result, "report": str(report)}
        with (args.report_dir / "journal.jsonl").open("a") as journal:
            journal.write(json.dumps(record) + "\n")
        print(f"Committed {path} at basis {record['basis_t']}", flush=True)


if __name__ == "__main__":
    main()
