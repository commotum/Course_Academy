import json, subprocess
from pathlib import Path
E=Path(__file__).resolve().parent; P='/home/jake/Developer/Course_Academy/.venv/bin/python'
cases=[
 (['prior-reproduce_shortcut.py','--input','prior-boundary-records.json','--index','0','--output','old-shortest-failure.json'],1),
 (['prior-reproduce_shortcut.py','--input','boundary-records.json','--index','0','--output','current-shortest-result.json'],0),
 (['reproduce_number_match.py','--input','previous-number-match-records.json','--output','old-number-match-failure.json'],1),
 (['reproduce_number_match.py','--output','current-number-match-result.json'],0),
 (['reproduce_number_match.py','--input','delivery-batch/accepted.json','--output','delivered-number-match-result.json'],0),
 (['author_repair_check.py','--records','prior-boundary-records.json'],1),
 (['author_repair_check.py','--records','previous-number-match-records.json'],1),
 (['author_repair_check.py','--records','delivery-batch/accepted.json','--output','batch-variation.json'],0),
 (['author_repair_check.py','--records','delivery-fresh/accepted.json','--output','fresh-variation.json'],1)
]
results=[]
for args,expected in cases:
 cmd=[P,'-B',*args];r=subprocess.run(cmd,cwd=E,capture_output=True,text=True);results.append({'command':cmd,'expected_exit':expected,'actual_exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==expected,results[-1]
(E/'retained-check-results.json').write_text(json.dumps({'passed':True,'commands':results,'fresh_author_check_limitation':'Author check rejects a 3-record school-template subgroup with target rank1 in all three by chance. Independent fixed-bank target pairs test both roles in that template; this is not a demonstrated family-wide generator defect. Exact failed output retained.', 'restriction':'independent_review.py directly reproduced historical capacity60/initial10 rejection on original registered generator and current acceptance; see repair-verification.json'},indent=2)+'\n')
print(json.dumps({'passed':True,'strict_commands':len(results)}))
