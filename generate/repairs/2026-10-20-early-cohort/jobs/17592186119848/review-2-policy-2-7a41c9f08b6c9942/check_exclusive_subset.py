"""Reproduce the changed sampler's incidental exclusive-answer shortcut.
Run: .venv/bin/python -B check_exclusive_subset.py --input batch.json --report exclusive-subset-results.json
Exit 1 means a repeated eligible-two subset group forces exclusive answers.
Use --native-input to save actual learner-grader cases, with exact Fraction ranks.
"""
import argparse,json,re,collections
from pathlib import Path
from audit_delivery import info,matrices,rank,shortcut_group
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--native-input',type=Path);a=p.parse_args()
records=json.loads(a.input.read_text());rows=[];cases=[]
for rec in records:
 x=info(rec)
 if not shortcut_group(x) or x['profile']!='q-139965':continue
 # Read the qualifying evidence for A only, then assume mutual exclusion.
 guess=['A'] if rank(matrices(rec['question'])['A'])==x['target'] else ['C']
 field=rec['question'][':question/answer-fields'][0]
 choice=next(c for c in field[':answer-field/choices'] if sorted(set(re.findall(r'\$([A-E])\$',c[':answer/value'])))==guess)
 outcome='accepted' if guess==x['matches'] else 'rejected'
 rows.append({'question_id':x['question_id'],'parameters':rec['generation']['parameters'],'truth':x['matches'],'guess':guess,'expected_grade':outcome,'ranks':x['ranks'],'shapes':x['shapes']})
 cases.append({'label':'Inspect A, assume C opposite; '+x['question_id'],'record':rec,'checks':[{'field_index':0,'submitted_answer_id':choice[':answer/id'],'expected':outcome,'purpose':'Independent shortcut: inspect A pivots only; choose A-only if A qualifies else C-only, without inspecting C'}]})
failed=len(rows)>1 and all(len(r['truth'])==1 for r in rows)
report={'passed':not failed,'input':str(a.input),'cue':'rank3; shape multiset2x4,3x4,5x5; dimension-excluded B; compatible subset-radio bank','strategy':'Inspect rank(A) only. If rank(A)=3 choose A-only, otherwise choose C-only. Never inspect C.','successes':sum(r['expected_grade']=='accepted' for r in rows),'attempts':len(rows),'baseline':2/3,'baseline_explanation':'Same-layout catalog has equally many A-only,C-only,A+C-only records. This shortcut succeeds for the two singleton cases and fails the legitimate pair case.','defect':failed,'records':rows}
a.report.write_text(json.dumps(report,indent=2)+'\n')
if a.native_input:a.native_input.write_text(json.dumps(cases,indent=2)+'\n')
print(json.dumps({'passed':not failed,'successes':report['successes'],'attempts':len(rows),'record_ids':[r['question_id'] for r in rows]}));raise SystemExit(1 if failed else 0)
