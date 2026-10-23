"""Strict independent regression: repeated quarter-exponent factors equal a half exponent."""
from review import *
import subprocess
r=g.generate('hard',66081,'reciprocal_exp_root_blank',parameters=dict(a=1,b=1,c=1,u=2))
response='8*exp(-1/4)*exp(-1/4)/(5*sqrt(5))'
assert eq(parse(key(r)),8*s.exp(-s.Rational(1,4))*s.exp(-s.Rational(1,4))/(5*s.sqrt(5)))
save('grading-failure-records.json',[r]);save('grading-failure-math.json',{'visible_prompt_check':mathcheck(r),'response':response,'exact_difference':str(s.simplify(parse(key(r))-8*s.exp(-s.Rational(1,4))*s.exp(-s.Rational(1,4))/(5*s.sqrt(5))))})
save('grading-failure-input.json',[{'label':'repeated quarter exponential factors','record':r,'checks':[{'submitted':response,'expected':'accepted','purpose':'two exp(-1/4) factors equal exp(-1/2)'}]}])
cmd=['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(ROOT/'grading-failure-input.json'),str(ROOT/'grading-failure-results.json')]
p=subprocess.run(cmd,capture_output=True,text=True);save('grading-failure-execution.json',{'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});print(p.stderr);sys.exit(p.returncode)
