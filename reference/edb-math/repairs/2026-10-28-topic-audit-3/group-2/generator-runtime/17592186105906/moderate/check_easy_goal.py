"""Regression: every band retains the full sine-area and subtraction task."""
import argparse,json
from pathlib import Path
from triangle_complement_contract import inspect_record
ap=argparse.ArgumentParser();ap.add_argument('--candidate-records',type=Path,required=True);a=ap.parse_args()
records=json.loads(a.candidate_records.read_text())
for r in records:inspect_record(r)
print(json.dumps({'status':'passed','count':len(records),'bands':'all'}))
