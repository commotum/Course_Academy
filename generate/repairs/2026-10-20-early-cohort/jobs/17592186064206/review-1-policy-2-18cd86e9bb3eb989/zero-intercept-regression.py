"""Strict regression for malformed affine rendering; exits 1 on current package.
Usage: context-python zero-intercept-regression.py [--package PATH] [--candidate-records FILE]
"""
import sys
sys.dont_write_bytecode=True
import argparse,json,pathlib,re
import audit
p=argparse.ArgumentParser();p.add_argument('--package',default=str(pathlib.Path(__file__).resolve().parent.parent/'workspace'));p.add_argument('--candidate-records');p.add_argument('--output',default='zero-intercept-regression.json');a=p.parse_args()
m=audit.load(a.package)
records=audit.read(a.candidate_records) if a.candidate_records else [m.generate(parameters=[2,1,0],seed=70519)]
results=[]
for r in records:
 q=r['question'];n,slope,b=r['generation']['parameters'];den=re.search(r'\\d?frac\{(\d+)\}\{([^}]+)\}',q[':question/problem'])[2]
 rendered=audit.expr(den);expected=slope*audit.s.Symbol('x')+b
 passed=audit.s.expand(rendered-expected)==0
 results.append({'id':q[':question/id'],'parameters':[n,slope,b],'denominator_tex':den,'parsed_denominator':str(rendered),'expected_denominator':str(expected),'passed':bool(passed),'record':r})
pathlib.Path(a.output).write_text(json.dumps({'command':sys.argv,'passed':all(r['passed'] for r in results),'checks':results},indent=2))
print(json.dumps({'passed':all(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'total':len(results)}));sys.exit(0 if all(r['passed'] for r in results) else 1)
