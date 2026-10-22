"""Serialize finite-generator registration, with exact requests and readback."""
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning

KP=17592186184172
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY=(HERE/'reference/source-query.edn').read_text()
def read_kp(path, basis):
    rows = DB.query(QUERY, [KP], path, 'kp', basis)
    assert len(rows) == 1
    return rows[0][0]


def inventory(binary, path):
    result = subprocess.run([str(binary), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=DB.env, capture_output=True, text=True, check=True, timeout=55)
    response = json.loads(result.stdout); assert response['ok']
    inv = response['data']; assert inv['lineage'] == LINEAGE
    save(path, inv)
    with tempfile.TemporaryDirectory(prefix='rank-nullity-inventory-') as temporary:
        snapshot = Path(temporary)/'snapshot.json'
        result = subprocess.run([str(binary), 'math', LEARNER, DB.args.endpoint], input='{"action":"export-test-snapshot"}', env={**DB.env, 'LEARNING_SNAPSHOT_PATH': str(snapshot)}, capture_output=True, text=True, check=True, timeout=55)
        assert json.loads(result.stdout)['ok']
        counts = path.with_name(path.stem+'-counts.json')
        subprocess.run([str(HERE/'inspect-inventory'), str(snapshot), str(counts)], check=True, timeout=55)
    available = json.loads(counts.read_text())
    assert available['basis'] == inv['basis'] == DB.basis(), 'Basis advanced; fresh inventory required'
    return inv, available

