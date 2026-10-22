"""Fail on the demonstrated fixed-A shortcut. All reads/writes are review-local.
Usage: python3 -B check_batch_decisions.py --input batch.json --report batch-regression.json
"""
import argparse,json
from pathlib import Path
from audit_delivery import info,shortcut_group
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
rows=[info(r) for r in json.loads(a.input.read_text())];group=[r for r in rows if shortcut_group(r)]
forced=[]
if len(group)>1:
 for lab in ('A','C'):
  truths=[lab in r['matches'] for r in group]
  if len(set(truths))==1:forced.append({'label':lab,'qualifies':truths[0]})
report={'passed':not forced,'input':str(a.input),'group':'rank 3; shapes 2x4, 3x4, 5x5; B excluded by rows','group_count':len(group),'forced_eligible_roles':forced,'records':group,'rule':'Repeated deliveries in this recognizable subgroup must not make an eligible label answer-bearing by identity. Check conditional batch coverage, not only the larger catalog.'}
a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':not forced,'group_count':len(group),'forced':forced}));raise SystemExit(0 if not forced else 1)
