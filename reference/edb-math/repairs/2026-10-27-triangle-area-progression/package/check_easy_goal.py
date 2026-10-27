#!/usr/bin/env python3
"""Regression: easy practice retains triangle calculation and area subtraction."""
import argparse,json,re,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--candidate-records',type=Path,required=True);a=ap.parse_args()
records=json.loads(a.candidate_records.read_text());failures=[]
for r in records:
 q=r['question']
 if not q[':question/difficulty'].endswith('/easy'):continue
 prompt=q[':question/problem'];sol=q[':question/worked-solution']
 checks={'two_sides':len(re.findall(r'\$[A-D]{2}=',prompt))==2,
         'included_angle':'meet at a right angle' in prompt,
         'calculate_not_copy':'has area $' not in prompt,
         'both_worked_steps':r'\frac12' in sol and 'Subtract the quadrilateral area' in sol}
 if not all(checks.values()):failures.append({'question_id':q[':question/id'],'checks':checks})
report={'status':'failed' if failures else 'passed','count':len(records),'failures':failures}
print(json.dumps(report,indent=2));sys.exit(bool(failures))
