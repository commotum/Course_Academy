#!/usr/bin/env python3
"""Regression for a complete-bank surface rule. Exit 1 when it answers every case.
Uses only displayed banks. A success with this probe alone never certifies a repair.
Run against independently chosen controlled case(s) or an explicit candidate batch.
"""
import sys
sys.dont_write_bytecode=True
import argparse
import audit
p=argparse.ArgumentParser();p.add_argument('--candidate-records',required=True);p.add_argument('--output',required=True);args=p.parse_args()
records=audit.load(args.candidate_records)
assert records
r=audit.probes(records)
r['defect_reproduced']=r['correct']==r['total']
audit.save(args.output,r)
print(f"bank-only cue: {r['correct']}/{r['total']}; random choice baseline 1/5; defect_reproduced={r['defect_reproduced']}")
sys.exit(1 if r['defect_reproduced'] else 0)
